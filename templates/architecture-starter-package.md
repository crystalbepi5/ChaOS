# Architecture Starter Package

This template exists to capture the standard output of Architecture Generation.

## Purpose

Use this package after Project Intake and, when required, Context Sufficiency Assessment. The package turns sufficient business context into reviewable architecture.

## How This Fits Into ChaOS

This package follows the ChaOS workflow path:

Project Intake

-> Context Sufficiency Assessment when context is risky

-> Architecture Generation

-> Architecture Starter Package

-> Human Review

-> Implementation Decision

This package is not an implementation plan. It must not define software, databases, infrastructure, frontend screens, orchestration, model providers, or autonomous actions unless those details are listed only as constraints or blocked implementation questions.

## 1. Package Metadata

Project name:

Prepared by:

Date:

Source intake packet:

Context Sufficiency Assessment used:

- Yes
- No

If no, reason sufficiency assessment was not required:

If human-approved exception, approver and known risk:

## 2. Context Sufficiency Result

Readiness decision:

- READY
- PARTIAL
- NEEDS CLARIFICATION
- DO NOT GENERATE YET

Known facts used:

| Fact | Source |
| --- | --- |
|  |  |

Reasonable inferences used:

| Inference | Supporting fact or pattern |
| --- | --- |
|  |  |

Unknowns affecting this package:

| Unknown | Affected section |
| --- | --- |
|  |  |

Unsupported assumptions excluded:

## 3. Package Section Status

| Section | Status | Reason |
| --- | --- | --- |
| Project Summary |  |  |
| Entity Model |  |  |
| Workflow Model |  |  |
| Agent Definition |  |  |
| Governance Requirements |  |  |
| Risks |  |  |
| Guardrails |  |  |
| Evaluation Criteria |  |  |
| Open Questions |  |  |

Allowed statuses:

- Complete
- Partial
- Blocked
- Not applicable

## 4. Project Summary

One-sentence project description:

Problem being addressed:

Complexity this project is meant to remove:

Primary users:

Decision owners:

Human approval boundaries:

## 5. Entity Model

Primary entities:

| Entity | Definition | Status |
| --- | --- | --- |
|  |  |  |

Entity -> Signal -> Decision -> Outcome -> Feedback mapping:

| Entity | Signal | Decision | Outcome | Feedback |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

Blocked or partial entity sections:

## 6. Workflow Model

Workflow name:

Trigger -> Input -> Processing -> Decision -> Action -> Feedback mapping:

| Stage | Specific content | Evidence status |
| --- | --- | --- |
| Trigger |  |  |
| Input |  |  |
| Processing |  |  |
| Decision |  |  |
| Action |  |  |
| Feedback |  |  |

Responsibilities:

Failure modes:

Evaluation methods:

Blocked or partial workflow sections:

## 7. Agent Definition

Agent needed:

- Yes
- No
- Unknown

If no, mark this section Not applicable.

Agent name:

Purpose:

Inputs:

Processing logic:

Outputs:

Evaluation:

Examples:

Failure modes:

Guardrails:

Approval required for:

Blocked or partial agent sections:

## 8. Governance Requirements

Decisions requiring human approval:

Architecture changes requiring decision records:

Actions that must remain recommendation-only:

Data, privacy, safety, trust, legal, or contractual constraints:

Candidate concepts referenced:

Candidate concepts must remain pressure labels unless separately approved.

## 9. Risks

| Risk | Evidence | Mitigation or guardrail |
| --- | --- | --- |
|  |  |  |

Risks caused by missing context:

Risks caused by premature implementation:

Risks caused by automation:

## 10. Guardrails

The system must not:

List prohibited assumptions, decisions, actions, automations, or implementation moves.

The system must:

List required behaviors, review boundaries, traceability rules, or feedback practices.

Human review is required before:

List decisions or actions that cannot proceed without human approval.

## 11. Evaluation Criteria

Architecture quality criteria:

| Criterion | Strong evidence | Weak evidence |
| --- | --- | --- |
| Clarity |  |  |
| Traceability |  |  |
| Portability |  |  |
| Feedback |  |  |
| Simplicity |  |  |

Project-specific success criteria:

Feedback to capture after review:

## 12. Open Questions

Entity questions:

Workflow questions:

Agent questions:

Governance questions:

Evaluation questions:

Questions that block implementation decisions:

## 13. Human Review Decision

Review decision:

- Accept
- Revise
- Defer
- Reject

Reviewer:

Date:

Required revisions:

Decision record required:

- Yes
- No

If yes, reason:

Implementation decision allowed:

- Yes
- No

If yes, allowed implementation scope:

If no, blocked reason:

## 14. Feedback Capture

Accepted sections:

Revised sections:

Deferred sections:

Rejected sections:

Reasons for revisions or rejections:

Lessons for future Architecture Generation:

Potential ChaOS-level improvements:

## Example Use

A project intake packet for a customer follow-up system is marked PARTIAL because workflow ownership is unknown. The starter package completes the Entity Model and Risks sections, marks Workflow Model as partial, marks Agent Definition as blocked, and lists workflow ownership questions under Open Questions.

## Future Considerations

If repeated starter packages show stable field requirements, ChaOS may later add a schema or generator. ChaOS must not automate generation until the recommendation pattern has proven useful through human review.
