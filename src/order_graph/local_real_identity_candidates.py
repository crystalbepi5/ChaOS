"""Generate local-real account identity candidates from normalization evidence.

Candidates are draft grouping artifacts only. They are not canonical entities and
must not be treated as final identity resolution.
"""

from __future__ import annotations

import re
from typing import Any

JsonObject = dict[str, Any]


def _candidate_id_for_domain(normalized_domain: str) -> str:
    """Create a deterministic, human-readable candidate id from a domain."""

    slug = re.sub(r"[^a-z0-9]+", "_", normalized_domain.lower()).strip("_")
    return f"local_real_account_candidate_{slug}"


def _source_record_metadata_by_id(source_records_output: JsonObject) -> dict[str, JsonObject]:
    records_by_id: dict[str, JsonObject] = {}
    for source_record in source_records_output.get("source_records", []):
        if not isinstance(source_record, dict):
            continue
        source_record_id = source_record.get("source_record_id")
        if isinstance(source_record_id, str):
            records_by_id[source_record_id] = {
                "source_record_id": source_record_id,
                "source_system": source_record.get("source_system"),
                "source_object_type": source_record.get("source_object_type"),
                "source_native_id": source_record.get("source_native_id"),
            }
    return records_by_id


def _candidate_evidence_record(evidence_record: JsonObject) -> JsonObject:
    normalization_evidence = evidence_record.get("normalization_evidence", {})
    if not isinstance(normalization_evidence, dict):
        normalization_evidence = {}

    return {
        "source_record_id": evidence_record.get("source_record_id"),
        "source_system": evidence_record.get("source_system"),
        "source_object_type": evidence_record.get("source_object_type"),
        "source_native_id": evidence_record.get("source_native_id"),
        "imported_domain_value": evidence_record.get("imported_domain_value"),
        "normalized_domain": normalization_evidence.get("normalized_domain"),
        "status": normalization_evidence.get("status"),
        "warnings": normalization_evidence.get("warnings", []),
        "allowed_use": normalization_evidence.get("allowed_use", []),
    }


def _unresolved_candidate(evidence_record: JsonObject, source_record_metadata: JsonObject) -> JsonObject:
    normalization_evidence = evidence_record.get("normalization_evidence", {})
    if not isinstance(normalization_evidence, dict):
        normalization_evidence = {}

    return {
        "source_record_id": evidence_record.get("source_record_id"),
        "source_system": source_record_metadata.get("source_system"),
        "source_object_type": source_record_metadata.get("source_object_type"),
        "source_native_id": source_record_metadata.get("source_native_id"),
        "candidate_type": "account",
        "imported_domain_value": evidence_record.get("imported_domain_value"),
        "reason": normalization_evidence.get("status", "missing_domain_unresolved_candidate"),
        "warnings": normalization_evidence.get("warnings", []),
        "allowed_use": normalization_evidence.get("allowed_use", ["warning", "human_review"]),
        "must_not_do": [
            "guess_domain",
            "merge_by_account_name_only",
            "treat_as_final_entity",
        ],
    }


def generate_local_real_account_identity_candidates(
    source_records_output: JsonObject,
    normalization_evidence_output: JsonObject,
) -> JsonObject:
    """Generate account identity candidates from normalized domain evidence only."""

    source_record_metadata = _source_record_metadata_by_id(source_records_output)
    groups_by_domain: dict[str, list[JsonObject]] = {}
    unresolved_candidates: list[JsonObject] = []

    for evidence_record in normalization_evidence_output.get("evidence_records", []):
        if not isinstance(evidence_record, dict):
            continue

        normalization_evidence = evidence_record.get("normalization_evidence", {})
        if not isinstance(normalization_evidence, dict):
            normalization_evidence = {}

        normalized_domain = normalization_evidence.get("normalized_domain")
        source_record_id = evidence_record.get("source_record_id")
        source_metadata = source_record_metadata.get(str(source_record_id), {})

        if isinstance(normalized_domain, str) and normalized_domain:
            groups_by_domain.setdefault(normalized_domain, []).append(_candidate_evidence_record(evidence_record))
        else:
            unresolved_candidates.append(_unresolved_candidate(evidence_record, source_metadata))

    identity_candidates: list[JsonObject] = []
    for normalized_domain in sorted(groups_by_domain):
        evidence = sorted(
            groups_by_domain[normalized_domain],
            key=lambda record: str(record.get("source_record_id", "")),
        )
        identity_candidates.append(
            {
                "candidate_id": _candidate_id_for_domain(normalized_domain),
                "candidate_type": "account",
                "normalized_domain": normalized_domain,
                "source_record_ids": [record.get("source_record_id") for record in evidence],
                "evidence": evidence,
                "allowed_use": ["future_draft_entity_input"],
                "must_not_do": [
                    "treat_as_final_entity",
                    "merge_by_account_name_only",
                    "write_entities_json",
                ],
            }
        )

    unresolved_candidates = sorted(
        unresolved_candidates,
        key=lambda candidate: str(candidate.get("source_record_id", "")),
    )

    return {
        "builder_mode": "local_real_account_identity_candidates",
        "source_record_count": int(source_records_output.get("source_record_count", 0)),
        "evidence_record_count": int(normalization_evidence_output.get("evidence_record_count", 0)),
        "candidate_count": len(identity_candidates),
        "unresolved_candidate_count": len(unresolved_candidates),
        "identity_candidates": identity_candidates,
        "unresolved_candidates": unresolved_candidates,
        "boundaries": [
            "This output contains account identity candidates only.",
            "This output does not create canonical entities.",
            "Candidates may be used only as future draft entity inputs after validation.",
            "Candidates are grouped by normalized domain only.",
            "Account-name-only matching remains prohibited.",
            "Missing, malformed, or weak-domain records remain unresolved candidates.",
        ],
    }
