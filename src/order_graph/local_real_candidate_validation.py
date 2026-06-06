"""Validation checks for local-real account identity candidates.

These checks validate candidate artifacts only. They do not perform final identity
resolution and do not approve canonical entity creation.
"""

from __future__ import annotations

from typing import Any

JsonObject = dict[str, Any]


def _check(check_id: str, passed: bool, detail: str) -> JsonObject:
    return {"check_id": check_id, "passed": passed, "detail": detail}


def _evidence_by_source_record_id(evidence_output: JsonObject) -> dict[str, JsonObject]:
    evidence_by_id: dict[str, JsonObject] = {}
    for evidence_record in evidence_output.get("evidence_records", []):
        if not isinstance(evidence_record, dict):
            continue
        source_record_id = evidence_record.get("source_record_id")
        if isinstance(source_record_id, str):
            evidence_by_id[source_record_id] = evidence_record
    return evidence_by_id


def _all_source_records_represented(candidates_output: JsonObject, evidence_output: JsonObject) -> bool:
    expected_ids = set(_evidence_by_source_record_id(evidence_output))
    represented_ids: set[str] = set()
    for candidate in candidates_output.get("identity_candidates", []):
        if isinstance(candidate, dict):
            represented_ids.update(str(record_id) for record_id in candidate.get("source_record_ids", []))
    for unresolved in candidates_output.get("unresolved_candidates", []):
        if isinstance(unresolved, dict) and isinstance(unresolved.get("source_record_id"), str):
            represented_ids.add(unresolved["source_record_id"])
    return expected_ids == represented_ids


def _candidates_group_by_normalized_domain_only(candidates_output: JsonObject, evidence_output: JsonObject) -> bool:
    evidence_by_id = _evidence_by_source_record_id(evidence_output)
    for candidate in candidates_output.get("identity_candidates", []):
        if not isinstance(candidate, dict):
            return False
        normalized_domain = candidate.get("normalized_domain")
        if not isinstance(normalized_domain, str) or not normalized_domain:
            return False
        if "account_name" in candidate or "account_names" in candidate:
            return False
        for source_record_id in candidate.get("source_record_ids", []):
            evidence_record = evidence_by_id.get(str(source_record_id), {})
            normalization_evidence = evidence_record.get("normalization_evidence", {})
            if not isinstance(normalization_evidence, dict):
                return False
            if normalization_evidence.get("normalized_domain") != normalized_domain:
                return False
    return True


def _unresolved_records_remain_unresolved(candidates_output: JsonObject, evidence_output: JsonObject) -> bool:
    evidence_by_id = _evidence_by_source_record_id(evidence_output)
    unresolved_ids = {
        evidence_id
        for evidence_id, evidence_record in evidence_by_id.items()
        if isinstance(evidence_record.get("normalization_evidence"), dict)
        and evidence_record["normalization_evidence"].get("normalized_domain") is None
    }
    represented_unresolved_ids = {
        unresolved.get("source_record_id")
        for unresolved in candidates_output.get("unresolved_candidates", [])
        if isinstance(unresolved, dict)
    }
    return unresolved_ids == represented_unresolved_ids


def _no_candidate_is_final_entity(candidates_output: JsonObject) -> bool:
    for candidate in candidates_output.get("identity_candidates", []):
        if not isinstance(candidate, dict):
            return False
        if candidate.get("entity_id") or candidate.get("canonical_entity_id"):
            return False
        must_not_do = candidate.get("must_not_do", [])
        if "treat_as_final_entity" not in must_not_do:
            return False
    return True


def generate_local_real_candidate_validation_report(
    candidates_output: JsonObject,
    normalization_evidence_output: JsonObject,
    output_files: list[str],
) -> JsonObject:
    """Validate account identity candidates without creating final entities."""

    output_file_set = set(output_files)
    boundaries = candidates_output.get("boundaries", [])
    checks = [
        _check(
            "account_identity_candidates_exist",
            candidates_output.get("builder_mode") == "local_real_account_identity_candidates"
            and "identity_candidates" in candidates_output
            and "unresolved_candidates" in candidates_output,
            "account-identity-candidates.json must be generated as a local candidate artifact.",
        ),
        _check(
            "all_source_records_are_represented",
            _all_source_records_represented(candidates_output, normalization_evidence_output),
            "Every normalization evidence record must appear in either identity_candidates or unresolved_candidates.",
        ),
        _check(
            "candidates_group_by_normalized_domain_only",
            _candidates_group_by_normalized_domain_only(candidates_output, normalization_evidence_output),
            "Identity candidates must group by normalized_domain evidence only.",
        ),
        _check(
            "unresolved_records_remain_unresolved",
            _unresolved_records_remain_unresolved(candidates_output, normalization_evidence_output),
            "Records without normalized_domain must remain unresolved candidates.",
        ),
        _check(
            "no_candidate_is_final_entity",
            _no_candidate_is_final_entity(candidates_output),
            "Candidates must not include canonical entity identifiers or final entity status.",
        ),
        _check(
            "entities_json_not_generated",
            "entities.json" not in output_file_set,
            "Imported SourceRecord mode must not write entities.json.",
        ),
        _check(
            "account_name_only_matching_remains_prohibited",
            isinstance(boundaries, list)
            and "Account-name-only matching remains prohibited." in boundaries,
            "The candidate artifact must preserve the account-name-only matching prohibition.",
        ),
    ]

    failed_checks = [check for check in checks if not check["passed"]]
    return {
        "builder_mode": "local_real_account_identity_candidate_validation",
        "status": "passed" if not failed_checks else "failed",
        "check_count": len(checks),
        "failed_check_count": len(failed_checks),
        "checks": checks,
        "failed_checks": failed_checks,
        "boundaries": [
            "This validation checks account identity candidates only.",
            "This validation does not perform final identity resolution.",
            "This validation does not create canonical entities.",
            "Account-name-only matching remains prohibited.",
        ],
    }
