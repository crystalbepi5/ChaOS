"""Local validation report for generated Order Graph fixture outputs.

The report validates generated entities, generated signal links, and generated
entity states against inspectable local expectations. It must not use external
systems, LLM judgment, hidden scoring, or production validation behavior.
"""

from __future__ import annotations

from .models import JsonObject


def generate_validation_report(
    entities_output: JsonObject,
    signal_links_output: JsonObject,
    entity_states_output: JsonObject,
    signals_fixture: JsonObject,
) -> JsonObject:
    """Validate generated graph outputs with deterministic local checks."""

    checks = [
        _check_signal_links_reference_entities(entities_output, signal_links_output),
        _check_signal_link_tuples_are_unique(signal_links_output),
        _check_email_reply_links_multiple_entities(signal_links_output),
        _check_meeting_signal_is_unlinked(signal_links_output, entity_states_output),
        _check_entity_states_reference_entities(entities_output, entity_states_output),
        _check_entity_state_signal_inputs_exist(signals_fixture, entity_states_output),
        _check_entity_state_link_inputs_exist(signal_links_output, entity_states_output),
        _check_entity_states_do_not_use_numeric_scores(entity_states_output),
        _check_zenith_unresolved_state_is_preserved(entity_states_output),
        _check_stale_signal_does_not_drive_high_priority(entity_states_output),
        _check_expected_state_projection_is_absent(entity_states_output),
    ]
    failed_checks = [check for check in checks if check["status"] != "pass"]

    return {
        "builder_mode": "local_validation_report",
        "validated_outputs": [
            "entities.json",
            "signal-links.json",
            "entity-states.json",
        ],
        "validation_status": "pass" if not failed_checks else "fail",
        "check_count": len(checks),
        "failed_check_count": len(failed_checks),
        "checks": checks,
        "warnings": [
            "This report validates local fake fixture outputs only.",
            "Validation is deterministic and inspectable by humans.",
            "No external APIs, LLM judgment, databases, UI, agents, integrations, or deployment work are used.",
        ],
    }


def _check_signal_links_reference_entities(entities_output: JsonObject, signal_links_output: JsonObject) -> JsonObject:
    entity_ids = _entity_ids(entities_output)
    missing = [
        link
        for link in _generated_signal_links(signal_links_output)
        if link.get("entity_id") not in entity_ids
    ]
    return _check(
        "signal_links_reference_generated_entities",
        "Every generated signal link must reference a generated entity.",
        not missing,
        {"missing_entity_references": missing},
    )


def _check_signal_link_tuples_are_unique(signal_links_output: JsonObject) -> JsonObject:
    seen = set()
    duplicates = []
    for link in _generated_signal_links(signal_links_output):
        key = (
            link.get("signal_id"),
            link.get("entity_id"),
            link.get("relationship_role"),
        )
        if key in seen:
            duplicates.append(key)
        seen.add(key)

    return _check(
        "signal_link_tuples_are_unique",
        "Signal links must be unique by signal_id, entity_id, and relationship_role.",
        not duplicates,
        {"duplicate_link_tuples": duplicates},
    )


def _check_email_reply_links_multiple_entities(signal_links_output: JsonObject) -> JsonObject:
    signal_id = "sig_out_email_reply_taylor_001"
    linked_entities = sorted(
        str(link.get("entity_id"))
        for link in _generated_signal_links(signal_links_output)
        if link.get("signal_id") == signal_id
    )
    return _check(
        "email_reply_links_multiple_entities",
        "The email reply signal must attach through links to Contact, Account, and Sequence entities.",
        len(linked_entities) == 3,
        {"signal_id": signal_id, "linked_entities": linked_entities},
    )


def _check_meeting_signal_is_unlinked(signal_links_output: JsonObject, entity_states_output: JsonObject) -> JsonObject:
    signal_id = "sig_calendar_meeting_nova_001"
    linked = [
        link
        for link in _generated_signal_links(signal_links_output)
        if link.get("signal_id") == signal_id
    ]
    preserved = [
        signal
        for signal in entity_states_output.get("unlinked_signals_preserved", [])
        if isinstance(signal, dict) and signal.get("signal_id") == signal_id
    ]
    return _check(
        "meeting_signal_preserves_uncertainty",
        "The meeting signal must remain unlinked until structured outcome-to-entity evidence exists.",
        not linked and bool(preserved),
        {
            "signal_id": signal_id,
            "generated_links": linked,
            "preserved_unlinked_entries": preserved,
        },
    )


def _check_entity_states_reference_entities(entities_output: JsonObject, entity_states_output: JsonObject) -> JsonObject:
    entity_ids = _entity_ids(entities_output)
    missing = [
        state
        for state in _computed_entity_states(entity_states_output)
        if state.get("entity_id") and state.get("entity_id") not in entity_ids
    ]
    return _check(
        "entity_states_reference_generated_entities",
        "Resolved entity states must reference generated entities.",
        not missing,
        {"missing_entity_state_references": missing},
    )


def _check_entity_state_signal_inputs_exist(signals_fixture: JsonObject, entity_states_output: JsonObject) -> JsonObject:
    signal_ids = {
        signal.get("signal_id")
        for signal in signals_fixture.get("signals", [])
        if isinstance(signal, dict)
    }
    missing = []
    for state in _computed_entity_states(entity_states_output):
        inputs = state.get("explanation_inputs", {})
        for signal_id in inputs.get("signal_fixture_ids", []) if isinstance(inputs, dict) else []:
            if signal_id not in signal_ids:
                missing.append({"entity_state_id": state.get("entity_state_id"), "signal_id": signal_id})

    return _check(
        "entity_state_signal_inputs_exist",
        "Entity state signal inputs must reference local signal fixtures.",
        not missing,
        {"missing_signal_references": missing},
    )


def _check_entity_state_link_inputs_exist(signal_links_output: JsonObject, entity_states_output: JsonObject) -> JsonObject:
    link_ids = {
        link.get("link_id")
        for link in _generated_signal_links(signal_links_output)
    }
    missing = []
    for state in _computed_entity_states(entity_states_output):
        inputs = state.get("explanation_inputs", {})
        for link_id in inputs.get("generated_signal_link_ids", []) if isinstance(inputs, dict) else []:
            if link_id not in link_ids:
                missing.append({"entity_state_id": state.get("entity_state_id"), "link_id": link_id})

    return _check(
        "entity_state_link_inputs_exist",
        "Entity state link inputs must reference generated signal links.",
        not missing,
        {"missing_link_references": missing},
    )


def _check_entity_states_do_not_use_numeric_scores(entity_states_output: JsonObject) -> JsonObject:
    numeric_scores = [
        {
            "entity_state_id": state.get("entity_state_id"),
            "score_or_priority_if_applicable": state.get("score_or_priority_if_applicable"),
        }
        for state in _computed_entity_states(entity_states_output)
        if state.get("score_or_priority_if_applicable") is not None
    ]
    return _check(
        "entity_states_do_not_use_numeric_scores",
        "Entity states must not invent numeric scores at this stage.",
        not numeric_scores,
        {"numeric_scores": numeric_scores},
    )


def _check_zenith_unresolved_state_is_preserved(entity_states_output: JsonObject) -> JsonObject:
    unresolved = [
        state
        for state in _computed_entity_states(entity_states_output)
        if state.get("state_label") == "unresolved_no_canonical_entity"
    ]
    return _check(
        "zenith_unresolved_state_is_preserved",
        "Missing-domain Zenith source records must remain unresolved.",
        len(unresolved) == 1,
        {"unresolved_states": unresolved},
    )


def _check_stale_signal_does_not_drive_high_priority(entity_states_output: JsonObject) -> JsonObject:
    stale_signal_id = "sig_web_visit_pioneer_old_001"
    high_priority_states = []
    for state in _computed_entity_states(entity_states_output):
        supporting = state.get("supporting_signals", [])
        if stale_signal_id in supporting and state.get("priority_band") == "high":
            high_priority_states.append(state)

    return _check(
        "stale_signal_does_not_drive_high_priority",
        "The stale low-confidence signal must not support high-priority state.",
        not high_priority_states,
        {"high_priority_states_from_stale_signal": high_priority_states},
    )


def _check_expected_state_projection_is_absent(entity_states_output: JsonObject) -> JsonObject:
    forbidden_keys = [
        key
        for key in ("expected_entity_states", "expected_top_10_fixture_preview")
        if key in entity_states_output
    ]
    return _check(
        "expected_state_projection_is_absent",
        "Generated entity state output must not project expected entity-state fixtures.",
        not forbidden_keys,
        {"forbidden_projection_keys": forbidden_keys},
    )


def _entity_ids(entities_output: JsonObject) -> set[object]:
    return {
        entity.get("entity_id")
        for entity in entities_output.get("canonical_entities", [])
        if isinstance(entity, dict)
    }


def _generated_signal_links(signal_links_output: JsonObject) -> list[JsonObject]:
    return [
        link
        for link in signal_links_output.get("generated_signal_links", [])
        if isinstance(link, dict)
    ]


def _computed_entity_states(entity_states_output: JsonObject) -> list[JsonObject]:
    return [
        state
        for state in entity_states_output.get("computed_entity_states", [])
        if isinstance(state, dict)
    ]


def _check(check_id: str, requirement: str, passed: bool, observed: JsonObject) -> JsonObject:
    return {
        "check_id": check_id,
        "status": "pass" if passed else "fail",
        "requirement": requirement,
        "observed": observed,
    }
