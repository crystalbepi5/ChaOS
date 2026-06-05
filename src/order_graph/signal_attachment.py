"""Deterministic signal attachment for fake Order Graph fixtures.

Signals live once as independent objects. This module creates explicit
SignalEntityLink-style records that attach each signal to generated entities
without duplicating the signal object.

It must not perform fuzzy matching, external enrichment, LLM calls, database
lookups, state computation, or production signal attachment.
"""

from __future__ import annotations

from .models import JsonObject
from .normalize import normalize_domain, normalize_email


def generate_signal_links(
    signals_fixture: JsonObject,
    entities_output: JsonObject,
    source_fixture: JsonObject,
) -> JsonObject:
    """Generate deterministic signal links from local signals and entities."""

    signals = signals_fixture.get("signals", [])
    if not isinstance(signals, list):
        raise ValueError("signals must be a list")

    index = _build_entity_index(entities_output, source_fixture)
    links_by_key: dict[tuple[str, str, str], JsonObject] = {}
    unlinked_signals: list[JsonObject] = []

    for signal in signals:
        if not isinstance(signal, dict):
            continue

        links = _links_for_signal(signal, index)
        if not links:
            unlinked_signals.append(
                {
                    "signal_id": signal.get("signal_id"),
                    "reason": _unlinked_reason_for_signal(signal),
                }
            )
            continue

        for link in links:
            key = (
                str(link.get("signal_id")),
                str(link.get("entity_id")),
                str(link.get("relationship_role")),
            )
            links_by_key[key] = link

    links = sorted(
        links_by_key.values(),
        key=lambda item: (
            str(item.get("signal_id")),
            str(item.get("entity_id")),
            str(item.get("relationship_role")),
        ),
    )

    return {
        "builder_mode": "signal_attachment",
        "source_fixture": "signals.json",
        "fixture_set": signals_fixture.get("fixture_set"),
        "storage_model_principle": [
            "Signals live once as independent time-based objects.",
            "Signals attach to every relevant entity through generated links.",
            "Entity views must use links instead of duplicating the underlying signal object.",
        ],
        "generated_signal_links": links,
        "unlinked_signals": unlinked_signals,
        "warnings": [
            "Signal links are generated from local fixture evidence only.",
            "No fuzzy matching, external enrichment, LLM reasoning, or state computation is performed.",
        ],
    }


def _links_for_signal(signal: JsonObject, index: JsonObject) -> list[JsonObject]:
    signal_type = signal.get("signal_type")

    if signal_type == "intent_spike":
        return _intent_links(signal, index)
    if signal_type == "email_reply":
        return _email_reply_links(signal, index)
    if signal_type == "meeting_booked":
        return _meeting_links(signal, index)
    if signal_type == "website_visit":
        return _website_visit_links(signal, index)

    return []


def _intent_links(signal: JsonObject, index: JsonObject) -> list[JsonObject]:
    source_record_id = _source_record_id_from_signal(signal)
    account = _entity_for_source_record(index, source_record_id, "Account")
    if not account:
        return []

    return [
        _link(
            signal,
            account,
            "target_account",
            signal.get("strength_or_weight", "medium"),
            signal.get("confidence", "medium"),
            f"Signal source record {source_record_id} resolves to Account {account['entity_id']}.",
        )
    ]


def _email_reply_links(signal: JsonObject, index: JsonObject) -> list[JsonObject]:
    source_record_id = _source_record_id_from_signal(signal)
    source_record = index["source_records_by_id"].get(source_record_id, {})
    contact = _entity_for_source_record(index, source_record_id, "Contact")
    account = _account_for_contact_source_record(index, source_record)
    sequence = _sequence_for_contact_source_record(index, source_record)

    links = []
    if contact:
        links.append(
            _link(
                signal,
                contact,
                "actor",
                "high",
                signal.get("confidence", "high"),
                f"Reply source record {source_record_id} resolves to Contact {contact['entity_id']}.",
            )
        )
    if account:
        links.append(
            _link(
                signal,
                account,
                "parent_account",
                "high",
                signal.get("confidence", "high"),
                f"Reply source record {source_record_id} carries email/company evidence for Account {account['entity_id']}.",
            )
        )
    if sequence:
        links.append(
            _link(
                signal,
                sequence,
                "source_workflow",
                "medium",
                signal.get("confidence", "high"),
                f"Reply source record {source_record_id} references sequence fixture evidence for {sequence['entity_id']}.",
            )
        )
    return links


def _meeting_links(signal: JsonObject, index: JsonObject) -> list[JsonObject]:
    # The current meeting signal references an outcome fixture path, not a
    # source record or structured entity reference. Summary text is not a safe
    # structured key, so the signal must remain unlinked until the fixture
    # supplies explicit entity evidence.
    return []


def _website_visit_links(signal: JsonObject, index: JsonObject) -> list[JsonObject]:
    source_record_id = _source_record_id_from_signal(signal)
    account = _entity_for_source_record(index, source_record_id, "Account")
    if not account:
        return []

    return [
        _link(
            signal,
            account,
            "possible_account_activity",
            signal.get("strength_or_weight", "low"),
            signal.get("confidence", "low"),
            f"Website visit source reference points to source record {source_record_id}, which resolves to Account {account['entity_id']}.",
        )
    ]


def _build_entity_index(entities_output: JsonObject, source_fixture: JsonObject) -> JsonObject:
    entities = entities_output.get("canonical_entities", [])
    entities_by_id = {}
    entities_by_source_record = {}
    accounts_by_domain = {}
    contacts_by_email = {}
    sequences = []

    for entity in entities:
        if not isinstance(entity, dict):
            continue

        entity_id = entity.get("entity_id")
        if entity_id:
            entities_by_id[entity_id] = entity

        for source_record_id in entity.get("source_traceability", []):
            entities_by_source_record.setdefault(str(source_record_id), []).append(entity)

        canonical_keys = entity.get("canonical_keys", {})
        if not isinstance(canonical_keys, dict):
            canonical_keys = {}

        if entity.get("entity_type") == "Account":
            domain = normalize_domain(canonical_keys.get("canonical_domain"))
            if domain:
                accounts_by_domain[domain] = entity
        elif entity.get("entity_type") == "Contact":
            email = normalize_email(canonical_keys.get("normalized_email"))
            if email:
                contacts_by_email[email] = entity
        elif entity.get("entity_type") == "Sequence":
            sequences.append(entity)

    source_records_by_id = {}
    source_records = source_fixture.get("source_records", [])
    if isinstance(source_records, list):
        for record in source_records:
            if isinstance(record, dict) and record.get("source_record_id"):
                source_records_by_id[str(record["source_record_id"])] = record

    return {
        "entities_by_id": entities_by_id,
        "entities_by_source_record": entities_by_source_record,
        "accounts_by_domain": accounts_by_domain,
        "contacts_by_email": contacts_by_email,
        "sequences": sequences,
        "source_records_by_id": source_records_by_id,
    }


def _source_record_id_from_signal(signal: JsonObject) -> str | None:
    reference = signal.get("raw_payload_or_source_reference")
    if not reference:
        return None
    return str(reference).rstrip("/").rsplit("/", 1)[-1]


def _unlinked_reason_for_signal(signal: JsonObject) -> str:
    if signal.get("signal_type") == "meeting_booked":
        return "Meeting signal references an outcome fixture path, but no outcome-to-entity fixture exists yet."
    return "No generated entity link found from explicit local fixture evidence."


def _entity_for_source_record(index: JsonObject, source_record_id: str | None, entity_type: str) -> JsonObject | None:
    if not source_record_id:
        return None
    for entity in index["entities_by_source_record"].get(source_record_id, []):
        if entity.get("entity_type") == entity_type:
            return entity
    return None


def _account_for_contact_source_record(index: JsonObject, source_record: JsonObject) -> JsonObject | None:
    raw_values = source_record.get("raw_values", {}) if isinstance(source_record, dict) else {}
    normalized_values = source_record.get("normalized_values", {}) if isinstance(source_record, dict) else {}

    domain = (
        normalize_domain(normalized_values.get("canonical_domain"))
        or normalize_domain(raw_values.get("company_domain"))
        or _domain_from_email(normalized_values.get("normalized_email"))
        or _domain_from_email(raw_values.get("email"))
    )
    if not domain:
        return None
    return index["accounts_by_domain"].get(domain)


def _sequence_for_contact_source_record(index: JsonObject, source_record: JsonObject) -> JsonObject | None:
    raw_values = source_record.get("raw_values", {}) if isinstance(source_record, dict) else {}
    sequence_id = raw_values.get("sequence_id")
    sequences = index["sequences"]

    # The current fixture has one sequence entity. The prospect source record
    # carries the sequence reference, so linking to that single generated
    # Sequence is explicit enough for this fake fixture stage.
    if sequence_id and len(sequences) == 1:
        return sequences[0]
    return None


def _domain_from_email(value: str | None) -> str | None:
    email = normalize_email(value)
    if not email or "@" not in email:
        return None
    return email.split("@", 1)[1]


def _link(
    signal: JsonObject,
    entity: JsonObject,
    role: str,
    relevance_weight: object,
    confidence: object,
    evidence: str,
) -> JsonObject:
    signal_id = signal.get("signal_id")
    entity_id = entity.get("entity_id")
    return {
        "link_id": f"link_{signal_id}_to_{entity_id}_{role}",
        "signal_id": signal_id,
        "entity_id": entity_id,
        "relationship_role": role,
        "relevance_weight": relevance_weight,
        "confidence": confidence,
        "evidence_or_matching_rule": evidence,
    }
