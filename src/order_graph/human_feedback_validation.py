"""Local validation for human review feedback examples.

The report validates generated human review records against inspectable local
expectations. It must not persist reviews, approve actions, write to external
systems, or treat fixture examples as real human decisions.
"""

from __future__ import annotations

from .models import JsonObject

REQUIRED_ACTIONS = {"accept", "reject", "revise", "flag"}
REQUIRED_MODEL_BOUNDARIES = {
    "review_feedback_only_no_outreach_no_crm_write",
    "no_autonomous_acceptance",
    "no_production_task_creation",
}


def generate_human_feedback_validation_report(
    top_10_output: JsonObject,
    human_review_output: JsonObject,
) -> JsonObject:
    """Validate generated human review examples with deterministic checks."""

    checks = [
        _check_review_examples_reference_recommendations(top_10_output, human_review_output),
        _check_review_examples_cover_required_actions(human_review_output),
        _check_review_examples_include_reasons(human_review_output),
        _check_review_examples_preserve_original_context(human_review_output),
        _check_revision_examples_preserve_revised_text(human_review_output),
        _check_feedback_targets_match_review_records(human_review_output),
        _check_automation_boundaries_are_feedback_only(human_review_output),
    ]
    failed_checks = [check for check in checks if check["status"] != "pass"]

    return {
        "builder_mode": "human_feedback_validation_report",
        "validated_outputs": [
            "top-10-accounts.json",
            "human-review-overrides.json",
        ],
        "validation_status": "pass" if not failed_checks else "fail",
        "check_count": len(checks),
        "failed_check_count": len(failed_checks),
        "checks": checks,
        "warnings": [
            "This report validates local fake review examples only.",
            "Validation is deterministic and inspectable by humans.",
            "No persistence, UI, external APIs, LLM judgment, databases, agents, integrations, CRM writes, outreach actions, or deployment work are used.",
        ],
    }


def _check_review_examples_reference_recommendations(top_10_output: JsonObject, human_review_output: JsonObject) -> JsonObject:
    recommendation_ids = _recommendation_ids(top_10_output)
    missing = [
        example
        for example in _review_examples(human_review_output)
        if example.get("recommendation_id") not in recommendation_ids
    ]
    return _check(
        "review_examples_reference_generated_recommendations",
        "Every review example must reference one generated top-10 recommendation.",
        not missing,
        {"missing_recommendation_references": missing},
    )


def _check_review_examples_cover_required_actions(human_review_output: JsonObject) -> JsonObject:
    observed_actions = {
        str(example.get("review_action"))
        for example in _review_examples(human_review_output)
        if example.get("review_action")
    }
    missing_actions = sorted(REQUIRED_ACTIONS - observed_actions)
    unexpected_actions = sorted(observed_actions - REQUIRED_ACTIONS)
    return _check(
        "review_examples_cover_required_actions",
        "Review examples must cover accept, reject, revise, and flag actions.",
        not missing_actions and not unexpected_actions,
        {
            "observed_actions": sorted(observed_actions),
            "missing_actions": missing_actions,
            "unexpected_actions": unexpected_actions,
        },
    )


def _check_review_examples_include_reasons(human_review_output: JsonObject) -> JsonObject:
    missing_reasons = [
        example
        for example in _review_examples(human_review_output)
        if not example.get("reason")
    ]
    return _check(
        "review_examples_include_reasons",
        "Every review example must include a human-readable reason.",
        not missing_reasons,
        {"missing_reason_examples": missing_reasons},
    )


def _check_review_examples_preserve_original_context(human_review_output: JsonObject) -> JsonObject:
    missing_context = [
        example
        for example in _review_examples(human_review_output)
        if not example.get("preserved_original_recommendation")
        or not example.get("preserved_original_rationale")
    ]
    return _check(
        "review_examples_preserve_original_context",
        "Every review example must preserve original recommendation text and rationale.",
        not missing_context,
        {"missing_original_context_examples": missing_context},
    )


def _check_revision_examples_preserve_revised_text(human_review_output: JsonObject) -> JsonObject:
    missing_revisions = [
        example
        for example in _review_examples(human_review_output)
        if example.get("review_action") == "revise" and not example.get("revised_recommendation")
    ]
    return _check(
        "revision_examples_preserve_revised_text",
        "Revise examples must include revised recommendation text.",
        not missing_revisions,
        {"missing_revised_text_examples": missing_revisions},
    )


def _check_feedback_targets_match_review_records(human_review_output: JsonObject) -> JsonObject:
    mismatches = []
    for example in _review_examples(human_review_output):
        target = example.get("feedback_target", {})
        if not isinstance(target, dict):
            mismatches.append({"review_record_id": example.get("review_record_id"), "reason": "missing_feedback_target"})
            continue
        for key in ("recommendation_id", "entity_id", "entity_state_id"):
            if target.get(key) != example.get(key):
                mismatches.append(
                    {
                        "review_record_id": example.get("review_record_id"),
                        "field": key,
                        "record_value": example.get(key),
                        "target_value": target.get(key),
                    }
                )
    return _check(
        "feedback_targets_match_review_records",
        "Feedback targets must match the recommendation, entity, and state referenced by the review record.",
        not mismatches,
        {"feedback_target_mismatches": mismatches},
    )


def _check_automation_boundaries_are_feedback_only(human_review_output: JsonObject) -> JsonObject:
    model_boundaries = set(human_review_output.get("automation_boundaries", []))
    missing_model_boundaries = sorted(REQUIRED_MODEL_BOUNDARIES - model_boundaries)
    invalid_examples = [
        example
        for example in _review_examples(human_review_output)
        if example.get("automation_boundary") != "feedback_only_no_action_taken"
    ]
    return _check(
        "automation_boundaries_are_feedback_only",
        "Human review output must preserve feedback-only automation boundaries.",
        not missing_model_boundaries and not invalid_examples,
        {
            "missing_model_boundaries": missing_model_boundaries,
            "invalid_example_boundaries": invalid_examples,
        },
    )


def _recommendation_ids(top_10_output: JsonObject) -> set[str]:
    ids = set()
    recommendations = top_10_output.get("recommendations", [])
    if not isinstance(recommendations, list):
        return ids
    for recommendation in recommendations:
        if not isinstance(recommendation, dict):
            continue
        ids.add(f"rec_top10_{recommendation.get('rank')}_{recommendation.get('entity_id')}")
    return ids


def _review_examples(human_review_output: JsonObject) -> list[JsonObject]:
    return [
        example
        for example in human_review_output.get("local_review_examples", [])
        if isinstance(example, dict)
    ]


def _check(check_id: str, requirement: str, passed: bool, observed: JsonObject) -> JsonObject:
    return {
        "check_id": check_id,
        "status": "pass" if passed else "fail",
        "requirement": requirement,
        "observed": observed,
    }
