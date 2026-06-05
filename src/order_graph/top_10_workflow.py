"""Deterministic top-10 account workflow for fake Order Graph fixtures.

This workflow consumes generated entity states and local validation evidence.
It produces recommendations for human review only. It must not automate
outreach, write to CRM, call external systems, use LLMs, or hide ranking logic.
"""

from __future__ import annotations

from .models import JsonObject

PRIORITY_ORDER = {
    "high": 1,
    "medium": 2,
}


def generate_top_10_account_workflow(
    entities_output: JsonObject,
    entity_states_output: JsonObject,
    validation_report_output: JsonObject,
) -> JsonObject:
    """Generate deterministic top-10 account recommendations for human review."""

    validation_status = validation_report_output.get("validation_status")
    validation_passed = validation_status == "pass"
    recommendations = []

    if validation_passed:
        account_names = _account_names_by_id(entities_output)
        ranked_states = sorted(
            _recommendable_account_states(entity_states_output),
            key=_recommendation_sort_key,
        )
        recommendations = [
            _recommendation(rank, state, account_names)
            for rank, state in enumerate(ranked_states[:10], start=1)
        ]

    return {
        "builder_mode": "top_10_account_workflow",
        "workflow_name": "Top 10 accounts to focus today and why",
        "source_inputs": [
            "entities.json",
            "entity-states.json",
            "validation-report.json",
        ],
        "validation_status_required": "pass",
        "validation_status_observed": validation_status,
        "recommendation_status": "generated" if validation_passed else "blocked_by_validation",
        "recommendation_count": len(recommendations),
        "recommendations": recommendations,
        "excluded_account_states": _excluded_account_states(entity_states_output, _account_names_by_id(entities_output)),
        "ranking_policy": [
            "Only resolved Account entity states may be recommended.",
            "Unresolved states must not be recommended.",
            "No-current-priority states must not be recommended.",
            "Low-priority or monitor-only states must remain traceable but must not be recommended for focus today.",
            "Recommendations sort by priority band in this order: high, medium.",
            "Ties sort by entity identifier for deterministic output.",
            "Numeric scores are not used.",
        ],
        "human_review_guardrails": [
            "Recommendations are review prompts only.",
            "The workflow must not automate outreach.",
            "The workflow must not write to CRM or any production system.",
            "A human must decide whether any follow-up action is appropriate.",
        ],
        "warnings": [
            "This workflow uses local fake fixture outputs only.",
            "No external APIs, LLMs, databases, UI, agents, integrations, or deployment work are used.",
            "Ranking is deterministic and inspectable from generated entity state fields.",
        ],
    }


def _recommendable_account_states(entity_states_output: JsonObject) -> list[JsonObject]:
    states = entity_states_output.get("computed_entity_states", [])
    if not isinstance(states, list):
        return []
    return [
        state
        for state in states
        if isinstance(state, dict)
        and state.get("entity_id")
        and state.get("priority_band") in PRIORITY_ORDER
    ]


def _excluded_account_states(entity_states_output: JsonObject, account_names: dict[str, str]) -> list[JsonObject]:
    excluded = []
    states = entity_states_output.get("computed_entity_states", [])
    if not isinstance(states, list):
        return excluded
    for state in states:
        if not isinstance(state, dict) or not state.get("entity_id"):
            continue
        priority_band = state.get("priority_band")
        if priority_band in PRIORITY_ORDER:
            continue
        entity_id = str(state.get("entity_id"))
        excluded.append(
            {
                "entity_id": entity_id,
                "account_name": account_names.get(entity_id),
                "entity_state_id": state.get("entity_state_id"),
                "state_label": state.get("state_label"),
                "priority_band": priority_band,
                "reason": _exclusion_reason(state),
                "traceable_signals": state.get("supporting_signals", []),
                "signals_present_but_not_supporting_priority": state.get("signals_present_but_not_supporting_priority", []),
            }
        )
    return sorted(excluded, key=lambda item: str(item.get("entity_id")))


def _recommendation_sort_key(state: JsonObject) -> tuple[int, str]:
    priority_band = str(state.get("priority_band"))
    return (
        PRIORITY_ORDER.get(priority_band, 99),
        str(state.get("entity_id")),
    )


def _recommendation(rank: int, state: JsonObject, account_names: dict[str, str]) -> JsonObject:
    entity_id = str(state.get("entity_id"))
    return {
        "rank": rank,
        "entity_id": entity_id,
        "account_name": account_names.get(entity_id),
        "entity_state_id": state.get("entity_state_id"),
        "priority_band": state.get("priority_band"),
        "state_label": state.get("state_label"),
        "why_this_account": state.get("primary_reason"),
        "recommended_next_decision": state.get("recommended_next_decision_or_action_if_applicable"),
        "supporting_rule_ids": state.get("supporting_rule_ids", []),
        "supporting_signals": state.get("supporting_signals", []),
        "signals_present_but_not_supporting_priority": state.get("signals_present_but_not_supporting_priority", []),
        "supporting_source_records_or_relationships": state.get("supporting_source_records_or_relationships", []),
        "unknowns": state.get("unknowns", []),
        "confidence": state.get("confidence"),
        "explanation_inputs": state.get("explanation_inputs", {}),
        "automation_boundary": "recommendation_only_no_outreach_no_crm_write",
    }


def _exclusion_reason(state: JsonObject) -> str:
    if state.get("priority_band") == "low":
        return "State is low-priority or monitor-only, so it remains traceable but is not recommended for focus today."
    return "State has no current priority evidence, so it is not recommended for focus today."


def _account_names_by_id(entities_output: JsonObject) -> dict[str, str]:
    names = {}
    entities = entities_output.get("canonical_entities", [])
    if not isinstance(entities, list):
        return names
    for entity in entities:
        if not isinstance(entity, dict):
            continue
        if entity.get("entity_type") != "Account":
            continue
        entity_id = entity.get("entity_id")
        canonical_name = entity.get("canonical_name")
        if entity_id and canonical_name:
            names[str(entity_id)] = str(canonical_name)
    return names
