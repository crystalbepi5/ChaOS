"""Generate local-real draft entities from validated account candidates.

Draft entities are intermediate review artifacts. They are not canonical entities
and must not be written to entities.json.
"""

from __future__ import annotations

from typing import Any

JsonObject = dict[str, Any]


def _draft_entity_id_for_domain(normalized_domain: str) -> str:
    return "draft_account_" + normalized_domain.lower().replace(".", "_").replace("-", "_")


def generate_local_real_draft_entities(account_candidates_output: JsonObject) -> JsonObject:
    """Generate draft account entities from account identity candidates only."""

    draft_entities: list[JsonObject] = []
    for candidate in account_candidates_output.get("identity_candidates", []):
        if not isinstance(candidate, dict):
            continue
        normalized_domain = candidate.get("normalized_domain")
        if not isinstance(normalized_domain, str) or not normalized_domain:
            continue

        draft_entities.append(
            {
                "draft_entity_id": _draft_entity_id_for_domain(normalized_domain),
                "draft_entity_type": "account",
                "source_candidate_id": candidate.get("candidate_id"),
                "identity_basis": {
                    "basis_type": "normalized_domain",
                    "normalized_domain": normalized_domain,
                },
                "source_record_ids": candidate.get("source_record_ids", []),
                "evidence": candidate.get("evidence", []),
                "status": "draft_not_canonical",
                "allowed_use": [
                    "future_human_review",
                    "future_canonical_entity_input",
                ],
                "must_not_do": [
                    "treat_as_canonical_entity",
                    "write_entities_json",
                    "merge_by_account_name_only",
                    "attach_signals",
                    "compute_state",
                    "generate_recommendations",
                ],
            }
        )

    return {
        "builder_mode": "local_real_draft_entity_output",
        "draft_entity_count": len(draft_entities),
        "source_candidate_count": len(account_candidates_output.get("identity_candidates", [])),
        "unresolved_candidate_count": len(account_candidates_output.get("unresolved_candidates", [])),
        "draft_entities": draft_entities,
        "unresolved_candidates": account_candidates_output.get("unresolved_candidates", []),
        "boundaries": [
            "This output contains draft entities only.",
            "Draft entities are not canonical entities.",
            "This output must not be written to entities.json.",
            "Unresolved candidates remain unresolved and do not become draft entities.",
            "Account-name-only matching remains prohibited.",
        ],
    }
