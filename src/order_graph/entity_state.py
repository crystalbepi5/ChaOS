"""Explainable entity state computation for fake Order Graph fixtures.

Entity state must explain itself from generated entities, generated signal
links, and local fixture evidence. This module uses deterministic rule labels
instead of hidden scores.

It must not perform black-box scoring, external enrichment, LLM calls,
database lookups, recommendation automation, or production state computation.
"""

from __future__ import annotations

from .models import JsonObject

COMPUTED_AT = "2026-01-13T09:00:00Z"
PRIORITY_ORDER = {
    "high_priority_human_review": 1,
    "medium_priority_review": 2,
    "low_priority_or_monitor_only": 3,
    "no_current_priority_evidence": 4,
}


def compute_entity_states(
    entities_output: JsonObject,
    signal_links_output: JsonObject,
    signals_fixture: JsonObject,
    source_fixture: JsonObject,
) -> JsonObject:
    """Compute deterministic entity states from visible local evidence."""

    index = _build_state_index(entities_output, signal_links_output, signals_fixture, source_fixture)
    account_states = [_state_for_account(entity, index) for entity in index["account_entities"]]
    unresolved_states = [_state_for_unresolved_case(case) for case in index["unresolved_cases"]]
    states = sorted(
        [*account_states, *unresolved_states],
        key=lambda state: (
            PRIORITY_ORDER.get(str(state.get("state_label")), 99),
            str(state.get("entity_id") or state.get("entity_state_id")),
        ),
    )

    return {
        "builder_mode": "entity_state_computation",
        "source_inputs": [
            "entities.json",
            "signal-links.json",
            "signals.json",
            "source-records.json",
        ],
        "fixture_set": entities_output.get("fixture_set") or signals_fixture.get("fixture_set"),
        "computed_at": COMPUTED_AT,
        "state_model": "deterministic_fixture_rules_v0",
        "state_rules": [
            {
                "rule_id": "resolved_contact_reply",
                "description": "A linked high-confidence email reply supports human review because it is explicit recent engagement.",
            },
            {
                "rule_id": "recent_intent_signal",
                "description": "A linked intent signal with expected_state_support=true supports account review.",
            },
            {
                "rule_id": "stale_low_confidence_signal",
                "description": "A linked signal with expected_state_support=false remains traceable but must not raise priority.",
            },
            {
                "rule_id": "missing_structured_entity_evidence",
                "description": "Unlinked signals and unresolved records must preserve uncertainty instead of inventing state.",
            },
        ],
        "computed_entity_states": states,
        "ranked_entity_state_preview": _ranked_preview(states),
        "unlinked_signals_preserved": signal_links_output.get("unlinked_signals", []),
        "warnings": [
            "Entity states are computed from generated entities, generated signal links, and local fixture evidence only.",
            "No numeric scoring, hidden weighting, external enrichment, LLM reasoning, or automated action is performed.",
            "Unlinked signals do not support entity state until structured entity evidence exists.",
        ],
    }


def _state_for_account(entity: JsonObject, index: JsonObject) -> JsonObject:
    entity_id = str(entity.get("entity_id"))
    linked_signals = _linked_signals_for_entity(entity_id, index)
    supporting_signals = [signal for signal in linked_signals if signal.get("expected_state_support") is True]
    non_supporting_signals = [signal for signal in linked_signals if signal.get("expected_state_support") is not True]
    source_record_ids = [str(record_id) for record_id in entity.get("source_traceability", [])]
    source_cases = _fixture_cases_for_sources(source_record_ids, index)
    rule_ids = _supporting_rule_ids(supporting_signals, non_supporting_signals)

    state_label = _state_label_for_rules(rule_ids)
    confidence = _confidence_for_state(state_label)

    return {
        "entity_state_id": f"state_{entity_id}_computed",
        "entity_id": entity_id,
        "computed_at": COMPUTED_AT,
        "state_label": state_label,
        "priority_band": _priority_band_for_state(state_label),
        "score_or_priority_if_applicable": None,
        "score_explanation": "No numeric score is computed. Priority is assigned by visible deterministic rule labels.",
        "primary_reason": _primary_reason(entity, state_label, supporting_signals, non_supporting_signals),
        "supporting_rule_ids": rule_ids,
        "supporting_signals": _signal_ids(supporting_signals),
        "signals_present_but_not_supporting_priority": _signal_ids(non_supporting_signals),
        "supporting_source_records_or_relationships": _supporting_evidence(entity, entity_id, index),
        "unknowns": _unknowns_for_state(state_label),
        "confidence": confidence,
        "recommended_next_decision_or_action_if_applicable": _recommended_action_for_state(state_label),
        "fixture_cases": source_cases,
        "explanation_inputs": {
            "entity_source_records": source_record_ids,
            "generated_signal_link_ids": [
                str(link.get("link_id")) for link in index["links_by_entity"].get(entity_id, [])
            ],
            "signal_fixture_ids": _signal_ids(linked_signals),
        },
    }


def _state_for_unresolved_case(case: JsonObject) -> JsonObject:
    fixture_case = str(case.get("fixture_case") or "unresolved_case")
    source_record_ids = [str(record_id) for record_id in case.get("source_record_ids", [])]

    return {
        "entity_state_id": f"state_unresolved_{fixture_case}",
        "entity_id": None,
        "computed_at": COMPUTED_AT,
        "state_label": "unresolved_no_canonical_entity",
        "priority_band": "unresolved",
        "score_or_priority_if_applicable": None,
        "score_explanation": "No numeric score is computed because no canonical entity exists.",
        "primary_reason": str(case.get("reason") or "Source records remain unresolved because strong identity evidence is missing."),
        "supporting_rule_ids": ["missing_structured_entity_evidence"],
        "supporting_signals": [],
        "signals_present_but_not_supporting_priority": [],
        "supporting_source_records_or_relationships": source_record_ids,
        "unknowns": case.get("unknowns_to_preserve", []),
        "confidence": "low",
        "recommended_next_decision_or_action_if_applicable": "request human clarification before resolution",
        "fixture_cases": [fixture_case],
        "explanation_inputs": {
            "entity_source_records": source_record_ids,
            "generated_signal_link_ids": [],
            "signal_fixture_ids": [],
        },
    }


def _build_state_index(
    entities_output: JsonObject,
    signal_links_output: JsonObject,
    signals_fixture: JsonObject,
    source_fixture: JsonObject,
) -> JsonObject:
    entities = [
        entity
        for entity in entities_output.get("canonical_entities", [])
        if isinstance(entity, dict)
    ]
    links = [
        link
        for link in signal_links_output.get("generated_signal_links", [])
        if isinstance(link, dict)
    ]
    signals = [
        signal
        for signal in signals_fixture.get("signals", [])
        if isinstance(signal, dict)
    ]
    source_records = [
        record
        for record in source_fixture.get("source_records", [])
        if isinstance(record, dict)
    ]

    links_by_entity: dict[str, list[JsonObject]] = {}
    for link in links:
        entity_id = link.get("entity_id")
        if entity_id:
            links_by_entity.setdefault(str(entity_id), []).append(link)

    return {
        "account_entities": [entity for entity in entities if entity.get("entity_type") == "Account"],
        "links_by_entity": links_by_entity,
        "signals_by_id": {str(signal.get("signal_id")): signal for signal in signals if signal.get("signal_id")},
        "source_records_by_id": {
            str(record.get("source_record_id")): record for record in source_records if record.get("source_record_id")
        },
        "unresolved_cases": [
            case
            for case in entities_output.get("unresolved_source_records", [])
            if isinstance(case, dict)
        ],
    }


def _linked_signals_for_entity(entity_id: str, index: JsonObject) -> list[JsonObject]:
    signals = []
    for link in index["links_by_entity"].get(entity_id, []):
        signal = index["signals_by_id"].get(str(link.get("signal_id")))
        if signal:
            signals.append(signal)
    return sorted(signals, key=lambda signal: str(signal.get("signal_id")))


def _supporting_rule_ids(supporting_signals: list[JsonObject], non_supporting_signals: list[JsonObject]) -> list[str]:
    rules = []
    if any(signal.get("signal_type") == "email_reply" for signal in supporting_signals):
        rules.append("resolved_contact_reply")
    if any(signal.get("signal_type") == "intent_spike" for signal in supporting_signals):
        rules.append("recent_intent_signal")
    if non_supporting_signals:
        rules.append("stale_low_confidence_signal")
    if not rules:
        rules.append("missing_structured_entity_evidence")
    return rules


def _state_label_for_rules(rule_ids: list[str]) -> str:
    if "resolved_contact_reply" in rule_ids and "recent_intent_signal" in rule_ids:
        return "high_priority_human_review"
    if "recent_intent_signal" in rule_ids:
        return "medium_priority_review"
    if "stale_low_confidence_signal" in rule_ids:
        return "low_priority_or_monitor_only"
    return "no_current_priority_evidence"


def _priority_band_for_state(state_label: str) -> str:
    return {
        "high_priority_human_review": "high",
        "medium_priority_review": "medium",
        "low_priority_or_monitor_only": "low",
        "no_current_priority_evidence": "none",
        "unresolved_no_canonical_entity": "unresolved",
    }.get(state_label, "none")


def _confidence_for_state(state_label: str) -> str:
    return {
        "high_priority_human_review": "high",
        "medium_priority_review": "medium",
        "low_priority_or_monitor_only": "medium",
        "no_current_priority_evidence": "low",
    }.get(state_label, "low")


def _primary_reason(
    entity: JsonObject,
    state_label: str,
    supporting_signals: list[JsonObject],
    non_supporting_signals: list[JsonObject],
) -> str:
    name = entity.get("canonical_name") or entity.get("entity_id")
    supporting_types = sorted({str(signal.get("signal_type")) for signal in supporting_signals})
    non_supporting_types = sorted({str(signal.get("signal_type")) for signal in non_supporting_signals})

    if state_label == "high_priority_human_review":
        return f"{name} has linked supporting signals from {', '.join(supporting_types)} and must be reviewed by a human before action."
    if state_label == "medium_priority_review":
        return f"{name} has linked supporting signal evidence from {', '.join(supporting_types)}, but no linked reply or outcome evidence."
    if state_label == "low_priority_or_monitor_only":
        return f"{name} has linked signal evidence from {', '.join(non_supporting_types)}, but that evidence is marked as non-supporting for priority."
    return f"{name} has a resolved Account entity but no linked signal evidence that supports priority."


def _supporting_evidence(entity: JsonObject, entity_id: str, index: JsonObject) -> list[str]:
    source_records = [str(record_id) for record_id in entity.get("source_traceability", [])]
    link_ids = [str(link.get("link_id")) for link in index["links_by_entity"].get(entity_id, [])]
    return [*source_records, *link_ids]


def _unknowns_for_state(state_label: str) -> list[str]:
    if state_label == "high_priority_human_review":
        return [
            "budget owner not confirmed",
            "opportunity amount not known",
            "human approval still required before any action",
        ]
    if state_label == "medium_priority_review":
        return [
            "active stakeholder not known",
            "last meaningful human touch not known",
            "meeting outcome not linked through structured evidence",
        ]
    if state_label == "low_priority_or_monitor_only":
        return [
            "no recent high-confidence buying signal",
            "unclear whether historical activity reflects current interest",
            "no resolved contact activity",
        ]
    return [
        "no linked supporting signal evidence",
        "priority cannot be inferred from identity alone",
    ]


def _recommended_action_for_state(state_label: str) -> str:
    return {
        "high_priority_human_review": "recommend human review for follow-up; do not automate outreach",
        "medium_priority_review": "recommend human review only if higher-priority accounts are exhausted",
        "low_priority_or_monitor_only": "do not prioritize from stale or low-confidence signal alone",
        "no_current_priority_evidence": "do not prioritize without supporting signal evidence",
    }.get(state_label, "request human clarification before resolution")


def _fixture_cases_for_sources(source_record_ids: list[str], index: JsonObject) -> list[str]:
    cases = []
    for source_record_id in source_record_ids:
        record = index["source_records_by_id"].get(source_record_id)
        if record and record.get("fixture_case"):
            cases.append(str(record["fixture_case"]))
    return sorted(set(cases))


def _signal_ids(signals: list[JsonObject]) -> list[str]:
    return sorted(str(signal.get("signal_id")) for signal in signals if signal.get("signal_id"))


def _ranked_preview(states: list[JsonObject]) -> list[JsonObject]:
    preview = []
    for state in states:
        state_label = str(state.get("state_label"))
        if state_label not in {"high_priority_human_review", "medium_priority_review", "low_priority_or_monitor_only"}:
            continue
        preview.append(
            {
                "entity_id": state.get("entity_id"),
                "state_label": state_label,
                "reason": state.get("primary_reason"),
            }
        )
    return preview
