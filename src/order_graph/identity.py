"""Deterministic identity resolution for fake Order Graph fixtures.

This module implements the first real local-only graph logic. It resolves only
strong fixture evidence:

- Account-like records merge by canonical domain.
- Contact-like records merge by normalized email.
- Sequence records resolve by source-native identity.
- Missing-domain account-like records remain unresolved.

It must not perform fuzzy matching, external enrichment, API calls, LLM calls,
database lookups, or production identity resolution.
"""

from __future__ import annotations

import re
from collections import defaultdict

from .models import JsonObject
from .normalize import normalize_company_name, normalize_domain, normalize_email

ACCOUNT_TYPES = {"account", "company"}
CONTACT_TYPES = {"contact", "prospect"}
SEQUENCE_TYPES = {"sequence"}

ACCOUNT_ENTITY_ID_SLUGS = {
    "novaworks.example": "novaworks",
    "acme.com": "acme",
    "pioneersystems.com": "pioneer_systems",
    "pioneersolutions.io": "pioneer_solutions",
}

_MONTH_PREFIXES = {
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
}


def resolve_entities_from_source_records(source_fixture: JsonObject) -> JsonObject:
    """Resolve fake source records into deterministic canonical entities."""

    records = source_fixture.get("source_records", [])
    if not isinstance(records, list):
        raise ValueError("source_records must be a list")

    domain = source_fixture.get("domain", {})
    domain_id = domain.get("domain_id") if isinstance(domain, dict) else None

    account_groups: dict[str, list[JsonObject]] = defaultdict(list)
    contact_groups: dict[str, list[JsonObject]] = defaultdict(list)
    sequence_records: list[JsonObject] = []
    unresolved_account_records: list[JsonObject] = []

    for record in records:
        if not isinstance(record, dict):
            continue

        source_object_type = str(record.get("source_object_type", "")).lower()
        normalized_values = _normalized_values(record)

        if source_object_type in ACCOUNT_TYPES:
            canonical_domain = _record_domain(record, normalized_values)
            if canonical_domain:
                account_groups[canonical_domain].append(record)
            else:
                unresolved_account_records.append(record)
            continue

        if source_object_type in CONTACT_TYPES:
            normalized_email = _record_email(record, normalized_values)
            if normalized_email:
                contact_groups[normalized_email].append(record)
            continue

        if source_object_type in SEQUENCE_TYPES:
            sequence_records.append(record)

    canonical_entities = []
    canonical_entities.extend(_build_account_entities(domain_id, account_groups))
    canonical_entities.extend(_build_contact_entities(domain_id, contact_groups))
    canonical_entities.extend(_build_sequence_entities(domain_id, sequence_records))
    canonical_entities.sort(key=_entity_sort_key)

    unresolved_source_records = _build_unresolved_account_cases(unresolved_account_records)
    explicit_non_merges = _build_explicit_non_merges(account_groups, contact_groups)

    return {
        "builder_mode": "identity_resolution",
        "source_fixture": "source-records.json",
        "warning": "Entities are resolved from strong deterministic fixture keys only.",
        "fixture_set": source_fixture.get("fixture_set"),
        "canonical_entities": canonical_entities,
        "unresolved_source_records": unresolved_source_records,
        "explicit_non_merges": explicit_non_merges,
    }


def _build_account_entities(
    domain_id: str | None,
    account_groups: dict[str, list[JsonObject]],
) -> list[JsonObject]:
    entities = []
    for canonical_domain in sorted(account_groups):
        records = account_groups[canonical_domain]
        canonical_name = _best_account_name(records)
        normalized_name = normalize_company_name(canonical_name)
        source_record_ids = [_record_id(record) for record in records]

        entities.append(
            {
                "entity_id": _account_entity_id(canonical_domain),
                "domain_id": domain_id,
                "entity_type": "Account",
                "canonical_name": canonical_name,
                "canonical_keys": {
                    "canonical_domain": canonical_domain,
                    "normalized_name": normalized_name,
                },
                "source_traceability": source_record_ids,
                "confidence": "high" if len(records) > 1 else "medium_high",
                "resolution_reason": _account_resolution_reason(records, canonical_domain),
                "current_state_reference": None,
            }
        )
    return entities


def _build_contact_entities(
    domain_id: str | None,
    contact_groups: dict[str, list[JsonObject]],
) -> list[JsonObject]:
    name_to_domains: dict[str, set[str]] = defaultdict(set)
    for email, records in contact_groups.items():
        name = _best_person_name(records)
        domain = email.split("@", 1)[1] if "@" in email else "unknown"
        name_to_domains[_slug(name)].add(_domain_root(domain))

    entities = []
    for normalized_email in sorted(contact_groups):
        records = contact_groups[normalized_email]
        canonical_name = _best_person_name(records)
        email_domain = normalized_email.split("@", 1)[1] if "@" in normalized_email else None
        source_record_ids = [_record_id(record) for record in records]
        duplicate_name = len(name_to_domains[_slug(canonical_name)]) > 1

        entities.append(
            {
                "entity_id": _contact_entity_id(canonical_name, email_domain, duplicate_name),
                "domain_id": domain_id,
                "entity_type": "Contact",
                "canonical_name": canonical_name,
                "canonical_keys": {
                    "normalized_email": normalized_email,
                    "canonical_domain": email_domain,
                },
                "source_traceability": source_record_ids,
                "confidence": "high",
                "resolution_reason": _contact_resolution_reason(records, normalized_email, duplicate_name),
                "current_state_reference": None,
            }
        )
    return entities


def _build_sequence_entities(
    domain_id: str | None,
    sequence_records: list[JsonObject],
) -> list[JsonObject]:
    entities = []
    for record in sequence_records:
        raw_values = _raw_values(record)
        normalized_values = _normalized_values(record)
        canonical_name = raw_values.get("sequence_name") or normalized_values.get("normalized_name") or _record_id(record)

        entities.append(
            {
                "entity_id": _sequence_entity_id(str(canonical_name)),
                "domain_id": domain_id,
                "entity_type": "Sequence",
                "canonical_name": canonical_name,
                "canonical_keys": {
                    "source_system": record.get("source_system"),
                    "source_native_id": record.get("source_native_id"),
                },
                "source_traceability": [_record_id(record)],
                "confidence": "high",
                "resolution_reason": "Single source-native Sequence record resolves to a source workflow entity.",
                "current_state_reference": None,
            }
        )
    return entities


def _build_unresolved_account_cases(records: list[JsonObject]) -> list[JsonObject]:
    if not records:
        return []

    grouped: dict[str, list[JsonObject]] = defaultdict(list)
    for record in records:
        grouped[str(record.get("fixture_case") or "missing_strong_account_key")].append(record)

    unresolved = []
    for fixture_case in sorted(grouped):
        case_records = grouped[fixture_case]
        unresolved.append(
            {
                "source_record_ids": [_record_id(record) for record in case_records],
                "fixture_case": fixture_case,
                "expected_status": "unresolved",
                "reason": "Account-like records without canonical domain or another strong key must remain unresolved. Do not guess from similar names.",
                "unknowns_to_preserve": [
                    "canonical_domain",
                    "whether the source records describe the same account",
                    "source authority for account identity",
                ],
            }
        )
    return unresolved


def _build_explicit_non_merges(
    account_groups: dict[str, list[JsonObject]],
    contact_groups: dict[str, list[JsonObject]],
) -> list[JsonObject]:
    non_merges = []

    account_name_groups: dict[str, list[JsonObject]] = defaultdict(list)
    for records in account_groups.values():
        for record in records:
            normalized_name = _record_company_name(record)
            if normalized_name:
                account_name_groups[_first_word(normalized_name)].append(record)

    for records in account_name_groups.values():
        domains = {_record_domain(record, _normalized_values(record)) for record in records}
        domains.discard(None)
        if len(domains) > 1:
            non_merges.append(
                {
                    "records_or_entities": sorted(_record_id(record) for record in records),
                    "reason": "Similar account names with different canonical domains must remain separate accounts.",
                }
            )

    contact_name_groups: dict[str, list[JsonObject]] = defaultdict(list)
    for records in contact_groups.values():
        for record in records:
            contact_name_groups[_slug(_best_person_name([record]))].append(record)

    for records in contact_name_groups.values():
        emails = {_record_email(record, _normalized_values(record)) for record in records}
        domains = {email.split("@", 1)[1] for email in emails if email and "@" in email}
        if len(domains) > 1:
            non_merges.append(
                {
                    "records_or_entities": sorted(_record_id(record) for record in records),
                    "reason": "Same person name with different email and company/domain must not merge.",
                }
            )

    return sorted(non_merges, key=lambda item: item["records_or_entities"])


def _record_domain(record: JsonObject, normalized_values: JsonObject) -> str | None:
    raw_values = _raw_values(record)
    return (
        normalize_domain(normalized_values.get("canonical_domain"))
        or normalize_domain(raw_values.get("website"))
        or normalize_domain(raw_values.get("company_domain"))
        or normalize_domain(raw_values.get("domain"))
    )


def _record_email(record: JsonObject, normalized_values: JsonObject) -> str | None:
    raw_values = _raw_values(record)
    return normalize_email(normalized_values.get("normalized_email")) or normalize_email(raw_values.get("email"))


def _record_company_name(record: JsonObject) -> str | None:
    raw_values = _raw_values(record)
    normalized_values = _normalized_values(record)
    return normalize_company_name(
        normalized_values.get("normalized_name")
        or raw_values.get("account_name")
        or raw_values.get("company_name")
        or raw_values.get("company")
    )


def _best_account_name(records: list[JsonObject]) -> str:
    for record in records:
        raw_values = _raw_values(record)
        for key in ("account_name", "company_name", "company"):
            if raw_values.get(key):
                return str(raw_values[key])
    return _record_id(records[0])


def _best_person_name(records: list[JsonObject]) -> str:
    for record in records:
        raw_values = _raw_values(record)
        if raw_values.get("full_name"):
            return str(raw_values["full_name"])
    return _record_id(records[0])


def _account_entity_id(canonical_domain: str) -> str:
    domain = normalize_domain(canonical_domain) or canonical_domain
    entity_slug = ACCOUNT_ENTITY_ID_SLUGS.get(domain, _domain_root(domain))
    return f"ent_acct_{entity_slug}"


def _contact_entity_id(canonical_name: str, email_domain: str | None, duplicate_name: bool) -> str:
    base = f"ent_contact_{_slug(canonical_name)}"
    if duplicate_name and email_domain:
        return f"{base}_{_domain_root(email_domain)}"
    return base


def _sequence_entity_id(canonical_name: str) -> str:
    words = [word for word in _slug(canonical_name).split("_") if word not in _MONTH_PREFIXES]
    if words[-2:] == ["follow", "up"]:
        words = [*words[:-2], "followup"]
    return f"ent_sequence_{'_'.join(words)}"


def _account_resolution_reason(records: list[JsonObject], canonical_domain: str) -> str:
    if len(records) > 1:
        names = [_best_account_name([record]) for record in records]
        return f"Account-like source records resolve because canonical domain {canonical_domain} is strong evidence across: {', '.join(names)}."
    return f"Single account-like source record has canonical domain {canonical_domain} and remains separate from records with different domains."


def _contact_resolution_reason(records: list[JsonObject], normalized_email: str, duplicate_name: bool) -> str:
    if len(records) > 1:
        return f"Same normalized email {normalized_email} resolves to one Contact across source records."
    if duplicate_name:
        return "Same name is not enough to merge people when email and company/domain differ."
    return f"Single contact-like source record has normalized email {normalized_email}."


def _entity_sort_key(entity: JsonObject) -> tuple[int, str]:
    type_order = {"Account": 0, "Contact": 1, "Sequence": 2}
    return (type_order.get(str(entity.get("entity_type")), 99), str(entity.get("entity_id")))


def _raw_values(record: JsonObject) -> JsonObject:
    raw_values = record.get("raw_values", {})
    return raw_values if isinstance(raw_values, dict) else {}


def _normalized_values(record: JsonObject) -> JsonObject:
    normalized_values = record.get("normalized_values", {})
    return normalized_values if isinstance(normalized_values, dict) else {}


def _record_id(record: JsonObject) -> str:
    return str(record.get("source_record_id") or "")


def _slug(value: str | None) -> str:
    if not value:
        return "unknown"
    normalized = re.sub(r"[^a-z0-9]+", " ", str(value).lower())
    return "_".join(normalized.split()) or "unknown"


def _domain_root(domain: str | None) -> str:
    if not domain:
        return "unknown"
    return _slug(str(domain).split(".", 1)[0])


def _first_word(value: str) -> str:
    return value.split(" ", 1)[0]
