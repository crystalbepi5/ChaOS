"""Validate local-real draft entity output boundaries.

Draft entities are review artifacts only. This report checks that the draft
output remains linked to account identity candidates without becoming canonical
entities.
"""

from __future__ import annotations

from typing import Any

JsonObject = dict[str, Any]


def _check(check_id: str, description: str, passed: bool, details: JsonObject | None = None) -> JsonObject:
    return {
        "check_id": check_id,
        "description": description,
        "passed": passed,
        "details": details or {},
    }


def _draft_entities(draft_entities_output: JsonObject) -> list[JsonObject]:
    return [
        draft_entity
        for draft_entity in draft_entities_output.get("draft_entities", [])
        if isinstance(draft_entity, dict)
    ]


def _candidate_by_id(account_candidates_output: JsonObject) -> dict[str, JsonObject]:
    candidates: dict[str, JsonObject] = {}
    for candidate in account_candidates_output.get("identity_candidates", []):
        if not isinstance(candidate, dict):
            continue
        candidate_id = candidate.get("candidate_id")
        if isinstance(candidate_id, str) and candidate_id:
            candidates[candidate_id] = candidate
    return candidates


def _unresolved_source_record_ids(account_candidates_output: JsonObject) -> set[str]:
    source_record_ids: set[str] = set()
    for unresolved in account_candidates_output.get("unresolved_candidates", []):
        if not isinstance(unresolved, dict):
            continue
        source_record_id = unresolved.get("source_record_id")
        if isinstance(source_record_id, str) and source_record_id:
            source_record_ids.add(source_record_id)
    return source_record_ids


def _draft_source_record_ids(draft_entities: list[JsonObject]) -> set[str]:
    source_record_ids: set[str] = set()
    for draft_entity in draft_entities:
        for source_record_id in draft_entity.get("source_record_ids", []):
            if isinstance(source_record_id, str) and source_record_id:
                source_record_ids.add(source_record_id)
    return source_record_ids


def _drafts_reference_existing_candidates(
    draft_entities: list[JsonObject],
    candidates: dict[str, JsonObject],
) -> bool:
    return all(draft.get("source_candidate_id") in candidates for draft in draft_entities)


def _drafts_preserve_candidate_source_records(
    draft_entities: list[JsonObject],
    candidates: dict[str, JsonObject],
) -> bool:
    for draft_entity in draft_entities:
        candidate = candidates.get(str(draft_entity.get("source_candidate_id")))
        if candidate is None:
            return False
        if draft_entity.get("source_record_ids") != candidate.get("source_record_ids"):
            return False
    return True


def _drafts_preserve_normalized_domain_basis(
    draft_entities: list[JsonObject],
    candidates: dict[str, JsonObject],
) -> bool:
    for draft_entity in draft_entities:
        candidate = candidates.get(str(draft_entity.get("source_candidate_id")))
        if candidate is None:
            return False
        identity_basis = draft_entity.get("identity_basis", {})
        if not isinstance(identity_basis, dict):
            return False
        if identity_basis.get("basis_type") != "normalized_domain":
            return False
        if identity_basis.get("normalized_domain") != candidate.get("normalized_domain"):
            return False
    return True


def _drafts_are_not_canonical(draft_entities: list[JsonObject]) -> bool:
    for draft_entity in draft_entities:
        if draft_entity.get("status") != "draft_not_canonical":
            return False
        if "entity_id" in draft_entity or "canonical_entity_id" in draft_entity:
            return False
    return True


def _unresolved_candidates_stay_unresolved(
    draft_entities: list[JsonObject],
    account_candidates_output: JsonObject,
) -> bool:
    return not (_unresolved_source_record_ids(account_candidates_output) & _draft_source_record_ids(draft_entities))


def _account_name_only_matching_prohibited(draft_entities_output: JsonObject, draft_entities: list[JsonObject]) -> bool:
    boundaries = draft_entities_output.get("boundaries", [])
    boundary_text = " ".join(str(boundary) for boundary in boundaries)
    if "Account-name-only matching remains prohibited" not in boundary_text:
        return False

    for draft_entity in draft_entities:
        if "account_name" in draft_entity or "account_names" in draft_entity:
            return False
        must_not_do = draft_entity.get("must_not_do", [])
        if "merge_by_account_name_only" not in must_not_do:
            return False
    return True


def generate_local_real_draft_entity_validation_report(
    draft_entities_output: JsonObject,
    account_candidates_output: JsonObject,
    output_files: list[str],
) -> JsonObject:
    """Generate deterministic validation checks for local-real draft entities."""

    draft_entities = _draft_entities(draft_entities_output)
    candidates = _candidate_by_id(account_candidates_output)
    checks = [
        _check(
            "draft_entity_artifact_exists",
            "Draft entity output must use the local-real draft entity builder mode.",
            draft_entities_output.get("builder_mode") == "local_real_draft_entity_output",
            {"builder_mode": draft_entities_output.get("builder_mode")},
        ),
        _check(
            "drafts_reference_existing_candidates",
            "Every draft entity must reference an existing account identity candidate.",
            _drafts_reference_existing_candidates(draft_entities, candidates),
            {"draft_entity_count": len(draft_entities), "candidate_count": len(candidates)},
        ),
        _check(
            "drafts_preserve_candidate_source_records",
            "Draft entities must preserve source record identifiers from their source candidates.",
            _drafts_preserve_candidate_source_records(draft_entities, candidates),
        ),
        _check(
            "drafts_preserve_normalized_domain_basis",
            "Draft entities must preserve normalized domain identity basis from their source candidates.",
            _drafts_preserve_normalized_domain_basis(draft_entities, candidates),
        ),
        _check(
            "drafts_are_not_canonical_entities",
            "Draft entities must remain draft-only and must not expose canonical entity identifiers.",
            _drafts_are_not_canonical(draft_entities),
        ),
        _check(
            "unresolved_candidates_stay_unresolved",
            "Unresolved candidates must not become draft entities.",
            _unresolved_candidates_stay_unresolved(draft_entities, account_candidates_output),
            {
                "unresolved_source_record_ids": sorted(_unresolved_source_record_ids(account_candidates_output)),
                "draft_source_record_ids": sorted(_draft_source_record_ids(draft_entities)),
            },
        ),
        _check(
            "entities_json_not_generated",
            "The local-real imported path must not write entities.json while producing draft entities.",
            "entities.json" not in output_files,
            {"output_files": output_files},
        ),
        _check(
            "account_name_only_matching_prohibited",
            "Draft entity output must explicitly prohibit account-name-only matching.",
            _account_name_only_matching_prohibited(draft_entities_output, draft_entities),
        ),
    ]
    failed_checks = [check for check in checks if not check["passed"]]

    return {
        "builder_mode": "local_real_draft_entity_validation",
        "status": "passed" if not failed_checks else "failed",
        "check_count": len(checks),
        "failed_check_count": len(failed_checks),
        "checks": checks,
        "failed_checks": failed_checks,
        "boundaries": [
            "This report validates local-real draft entity output only.",
            "This report does not create canonical entities.",
            "Draft entities must not be written to entities.json.",
            "Unresolved candidates must remain unresolved.",
            "Account-name-only matching remains prohibited.",
        ],
    }
