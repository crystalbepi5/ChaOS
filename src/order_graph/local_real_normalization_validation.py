"""Validation checks for local-real normalization evidence output.

These checks validate the handoff and evidence artifacts only. They do not
perform identity resolution or approve graph expansion.
"""

from __future__ import annotations

from typing import Any

JsonObject = dict[str, Any]

_PROHIBITED_GRAPH_OUTPUTS = {
    "entities.json",
    "signal-links.json",
    "entity-states.json",
    "top-10-accounts.json",
    "human-review-overrides.json",
    "human-feedback-validation.json",
}


def _check(check_id: str, passed: bool, detail: str) -> JsonObject:
    return {
        "check_id": check_id,
        "passed": passed,
        "detail": detail,
    }


def _source_records_by_id(source_records_output: JsonObject) -> dict[str, JsonObject]:
    records_by_id: dict[str, JsonObject] = {}
    for source_record in source_records_output.get("source_records", []):
        if not isinstance(source_record, dict):
            continue
        source_record_id = source_record.get("source_record_id")
        if isinstance(source_record_id, str):
            records_by_id[source_record_id] = source_record
    return records_by_id


def _imported_domain_value(source_record: JsonObject) -> str | None:
    normalized_values = source_record.get("normalized_values", {})
    if not isinstance(normalized_values, dict):
        return None
    domain = normalized_values.get("domain")
    if domain is None:
        return None
    return str(domain)


def _missing_or_weak_domains_are_unresolved(evidence_output: JsonObject) -> bool:
    for evidence_record in evidence_output.get("evidence_records", []):
        if not isinstance(evidence_record, dict):
            return False
        evidence = evidence_record.get("normalization_evidence", {})
        if not isinstance(evidence, dict):
            return False
        if evidence.get("normalized_domain") is not None:
            continue

        status = str(evidence.get("status", ""))
        allowed_use = evidence.get("allowed_use", [])
        warnings = evidence.get("warnings", [])
        if not status.endswith("unresolved_candidate"):
            return False
        if not isinstance(allowed_use, list) or "warning" not in allowed_use:
            return False
        if not isinstance(warnings, list) or not warnings:
            return False
    return True


def _imported_values_are_preserved(source_records_output: JsonObject, evidence_output: JsonObject) -> bool:
    source_records_by_id = _source_records_by_id(source_records_output)
    for evidence_record in evidence_output.get("evidence_records", []):
        if not isinstance(evidence_record, dict):
            return False
        source_record_id = evidence_record.get("source_record_id")
        if not isinstance(source_record_id, str) or source_record_id not in source_records_by_id:
            return False
        expected_domain = _imported_domain_value(source_records_by_id[source_record_id])
        if evidence_record.get("imported_domain_value") != expected_domain:
            return False
    return True


def _derived_evidence_is_separate(source_records_output: JsonObject, evidence_output: JsonObject) -> bool:
    if "evidence_records" in source_records_output:
        return False
    for source_record in source_records_output.get("source_records", []):
        if not isinstance(source_record, dict):
            return False
        if "normalization_evidence" in source_record:
            return False
    return bool(evidence_output.get("evidence_records"))


def generate_local_real_normalization_validation_report(
    source_records_output: JsonObject,
    evidence_output: JsonObject,
    output_files: list[str],
) -> JsonObject:
    """Validate local-real normalization evidence without graph expansion."""

    source_record_count = int(source_records_output.get("source_record_count", 0))
    evidence_record_count = int(evidence_output.get("evidence_record_count", 0))
    output_file_set = set(output_files)
    boundaries = evidence_output.get("boundaries", [])

    checks = [
        _check(
            "identity_normalization_evidence_exists",
            evidence_output.get("builder_mode") == "local_real_identity_normalization_evidence"
            and "evidence_records" in evidence_output,
            "identity-normalization-evidence.json must be generated as a local evidence artifact.",
        ),
        _check(
            "source_record_count_matches_evidence_record_count",
            source_record_count == evidence_record_count,
            "Every imported SourceRecord must have one normalization evidence record.",
        ),
        _check(
            "imported_values_are_preserved",
            _imported_values_are_preserved(source_records_output, evidence_output),
            "Evidence imported_domain_value must match the adapter-preserved SourceRecord value exactly.",
        ),
        _check(
            "derived_evidence_is_separate",
            _derived_evidence_is_separate(source_records_output, evidence_output),
            "Normalization evidence must live outside SourceRecords.",
        ),
        _check(
            "missing_malformed_or_weak_domains_remain_unresolved_or_warning_oriented",
            _missing_or_weak_domains_are_unresolved(evidence_output),
            "Evidence without a normalized domain must remain unresolved and warning-oriented.",
        ),
        _check(
            "no_graph_outputs_generated",
            not (_PROHIBITED_GRAPH_OUTPUTS & output_file_set),
            "Imported SourceRecord mode must not generate entities, signals, states, recommendations, or review records.",
        ),
        _check(
            "account_name_only_matching_remains_prohibited",
            isinstance(boundaries, list)
            and "Account-name-only matching remains prohibited." in boundaries,
            "The evidence artifact must preserve the account-name-only matching prohibition.",
        ),
    ]

    failed_checks = [check for check in checks if not check["passed"]]
    return {
        "builder_mode": "local_real_normalization_evidence_validation",
        "status": "passed" if not failed_checks else "failed",
        "check_count": len(checks),
        "failed_check_count": len(failed_checks),
        "checks": checks,
        "failed_checks": failed_checks,
        "boundaries": [
            "This validation checks imported SourceRecord and normalization evidence artifacts only.",
            "This validation does not perform identity resolution.",
            "This validation does not create entities, signal links, entity states, recommendations, or review records.",
            "Account-name-only matching remains prohibited.",
        ],
    }
