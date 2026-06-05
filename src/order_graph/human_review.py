"""Human review override model for local Order Graph recommendations.

This module turns generated top-10 account recommendations into reviewable
decision records. It must not execute the decisions, write to external systems,
or treat fixture examples as actual human approval.
"""

from __future__ import annotations

from .models import JsonObject

REVIEW_ACTIONS = [
    "accept",
    "reject",
    "revise",
    "flag",
]


def generate_human_review_override_model(top_10_output: JsonObject) -> JsonObject:
    """Generate deterministic human review records and examples."""

    recommendations = _recommendations(top_10_output)
    reviewable_recommendations = [
        _reviewable_recommendation(recommendation) for recommendation in recommendations
    ]
    review_examples = _review_examples(reviewable_recommendations)

    return {
        "builder_mode": "human_review_override_model",
        "workflow_name": "Human review override model for top-10 account recommendations",
        "source_inputs": [
            "top-10-accounts.json",
        ],
        "review_model_status": "generated_model_only",
        "reviewable_recommendation_count": len(reviewable_recommendations),
        "review_example_count": len(review_examples),
        "reviewable_recommendations": reviewable_recommendations,
        "review_record_requirements": [
            "Each human review record must reference one generated recommendation.",
            "Each human review record must use one allowed review action: accept, reject, revise, or flag.",
            "Each human review record must include a human-readable reason.",
            "Reject, revise, and flag records must preserve the correction or concern instead of hiding it.",
            "Review records must not execute outreach, CRM writes, task creation, or production changes.",
        ],
        "review_action_policy": {
            "accept": "Reviewer agrees the recommendation is reasonable for human consideration; acceptance still must not trigger outreach or CRM writes.",
            "reject": "Reviewer disagrees with the recommendation and records the reason so the bad or weak logic remains visible.",
            "revise": "Reviewer changes the suggested decision text or priority interpretation while preserving the original recommendation.",
            "flag": "Reviewer marks a recommendation for logic review, fixture improvement, or missing evidence investigation.",
        },
        "local_review_examples": review_examples,
        "feedback_preservation_rules": [
            "Rejected recommendations must remain visible with rejection reasons.",
            "Revisions must keep both the original recommendation and the revised text.",
            "Flags must name the concern and the evidence that caused it when available.",
            "Future feedback must connect to the recommendation, entity, state, and supporting evidence it evaluates.",
        ],
        "automation_boundaries": [
            "review_feedback_only_no_outreach_no_crm_write",
            "no_autonomous_acceptance",
            "no_production_task_creation",
        ],
        "warnings": [
            "This output is a local review model, not a review UI.",
            "Fixture examples demonstrate record shape only and must not be treated as real human approval.",
            "No external APIs, LLMs, databases, UI, agents, integrations, CRM writes, outreach actions, or deployment work are used.",
        ],
    }


def _recommendations(top_10_output: JsonObject) -> list[JsonObject]:
    recommendations = top_10_output.get("recommendations", [])
    if not isinstance(recommendations, list):
        return []
    return [item for item in recommendations if isinstance(item, dict)]


def _reviewable_recommendation(recommendation: JsonObject) -> JsonObject:
    recommendation_id = _recommendation_id(recommendation)
    return {
        "recommendation_id": recommendation_id,
        "source_recommendation_rank": recommendation.get("rank"),
        "entity_id": recommendation.get("entity_id"),
        "account_name": recommendation.get("account_name"),
        "entity_state_id": recommendation.get("entity_state_id"),
        "priority_band": recommendation.get("priority_band"),
        "state_label": recommendation.get("state_label"),
        "original_recommendation": recommendation.get("recommended_next_decision"),
        "original_rationale": recommendation.get("why_this_account"),
        "supporting_signals": recommendation.get("supporting_signals", []),
        "supporting_rule_ids": recommendation.get("supporting_rule_ids", []),
        "unknowns": recommendation.get("unknowns", []),
        "allowed_review_actions": REVIEW_ACTIONS,
        "review_status": "awaiting_human_review",
        "action_boundary": "review_record_only",
    }


def _review_examples(reviewable_recommendations: list[JsonObject]) -> list[JsonObject]:
    if not reviewable_recommendations:
        return []

    first = reviewable_recommendations[0]
    second = reviewable_recommendations[1] if len(reviewable_recommendations) > 1 else first

    return [
        _review_record(
            first,
            "accept",
            "Reviewer agrees the evidence is sufficient for manual follow-up consideration.",
        ),
        _review_record(
            second,
            "reject",
            "Reviewer rejects the recommendation because the active stakeholder is still unknown.",
        ),
        _review_record(
            second,
            "revise",
            "Reviewer revises the recommendation to monitor until stakeholder evidence exists.",
            revised_recommendation="monitor account until an active stakeholder is confirmed; do not prioritize for follow-up today",
        ),
        _review_record(
            first,
            "flag",
            "Reviewer flags the recommendation because meeting outcome evidence remains unlinked.",
            flag_type="missing_structured_evidence",
        ),
    ]


def _review_record(
    recommendation: JsonObject,
    review_action: str,
    reason: str,
    revised_recommendation: str | None = None,
    flag_type: str | None = None,
) -> JsonObject:
    recommendation_id = str(recommendation.get("recommendation_id"))
    review_record = {
        "review_record_id": f"review_{review_action}_{recommendation_id}",
        "record_type": "local_fixture_review_example",
        "recommendation_id": recommendation_id,
        "entity_id": recommendation.get("entity_id"),
        "entity_state_id": recommendation.get("entity_state_id"),
        "review_action": review_action,
        "review_status_after_record": _status_after(review_action),
        "reviewer": "fixture_human_reviewer",
        "reason": reason,
        "preserved_original_recommendation": recommendation.get("original_recommendation"),
        "preserved_original_rationale": recommendation.get("original_rationale"),
        "feedback_target": {
            "recommendation_id": recommendation_id,
            "entity_id": recommendation.get("entity_id"),
            "entity_state_id": recommendation.get("entity_state_id"),
            "supporting_signals": recommendation.get("supporting_signals", []),
        },
        "automation_boundary": "feedback_only_no_action_taken",
    }
    if revised_recommendation:
        review_record["revised_recommendation"] = revised_recommendation
    if flag_type:
        review_record["flag_type"] = flag_type
    return review_record


def _recommendation_id(recommendation: JsonObject) -> str:
    rank = recommendation.get("rank")
    entity_id = recommendation.get("entity_id")
    return f"rec_top10_{rank}_{entity_id}"


def _status_after(review_action: str) -> str:
    return {
        "accept": "accepted_for_manual_review",
        "reject": "rejected_with_reason",
        "revise": "revised_by_human",
        "flag": "flagged_for_logic_review",
    }[review_action]
