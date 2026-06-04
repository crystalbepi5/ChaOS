# Project Intake Packet

This template exists to capture enough project context for ChaOS to route the work responsibly.

## Purpose

Use this packet before Context Sufficiency Assessment or Architecture Generation. The packet turns a raw idea into visible context, known assumptions, and a routing decision.

## How This Fits Into ChaOS

This packet feeds the ChaOS workflow path:

Project Intake

-> Context Sufficiency Assessment when context is risky

-> Architecture Generation when context is sufficient

-> Human Review

-> Implementation Decision

The packet is not an implementation plan. It must not define software, databases, infrastructure, frontend screens, orchestration, or autonomous actions unless those details are business constraints that must be considered later.

## 1. Project Snapshot

Project name:

One-sentence description:

Primary human owner:

Date:

Current stage:

- Idea
- Existing manual process
- Existing software/process
- Architecture review
- Other:

## 2. Problem And Purpose

What problem exists?

Why does this problem matter now?

What complexity must this project remove?

What must stay human-controlled?

## 3. Users And Roles

Primary users:

Decision owners:

People affected by the system:

People who must approve changes:

Unknown roles:

## 4. Entity Model Inputs

Primary entities the system cares about:

Entity definitions that are clear:

Entity definitions that are ambiguous:

Signals currently observed:

Decisions the system must support:

Outcomes that matter:

Feedback that must be captured:

## 5. Workflow Inputs

What starts the work?

What information is required before work can proceed?

What processing or interpretation happens?

What decision is made or recommended?

What action happens after approval?

What feedback is captured after the action?

## 6. Agent Inputs

Is an agent needed?

- Yes
- No
- Unknown

If yes, what decision or recommendation does the agent support?

Allowed inputs:

Forbidden inputs:

Expected outputs:

Human approval boundaries:

Failure modes:

Guardrails:

## 7. Governance And Constraints

Decisions that require human approval:

Actions that must not be automated:

Existing policies, laws, or contractual constraints:

Privacy, safety, or trust concerns:

Vendor, tool, or platform constraints:

Constraints that are preferences, not requirements:

## 8. Context Quality

Known facts:

| Fact | Source |
| --- | --- |
|  |  |

Reasonable inferences:

| Inference | Supporting fact or pattern |
| --- | --- |
|  |  |

Unknowns:

| Unknown | Architecture section affected |
| --- | --- |
|  |  |

Private-memory context:

Unsupported assumptions that must not become architecture:

Conflicting information:

## 9. Readiness Routing

Choose one routing decision.

- READY: Enough context exists for full Architecture Generation.
- PARTIAL: Some architecture sections can be generated, but others are blocked.
- NEEDS CLARIFICATION: Clarifying questions must be answered before full generation.
- DO NOT GENERATE YET: Minimum context is missing.

Routing decision:

Allowed Architecture Starter Package sections:

- Project Summary
- Entity Model
- Workflow Model
- Agent Definition
- Governance Requirements
- Risks
- Guardrails
- Evaluation Criteria
- Open Questions

Blocked sections:

Reason for blocked sections:

## 10. Clarifying Questions

Entity questions:

Workflow questions:

Agent questions:

Governance questions:

Evaluation questions:

## 11. Evaluation Criteria

How will we know the architecture was useful?

What would make the architecture misleading or unsafe?

What evidence must be preserved for future review?

What feedback must be collected after human review?

## Example Use

A user describes a new customer follow-up system. The packet captures accounts as entities, missed replies as signals, follow-up recommendations as decisions, booked meetings as outcomes, and accepted or rejected recommendations as feedback. If ownership and approval rules are unclear, the routing decision becomes NEEDS CLARIFICATION instead of forcing a full architecture.

## Future Considerations

If this packet becomes too broad, ChaOS may split it into smaller templates for intake, sufficiency assessment, and starter packages. That split must happen only after repeated use proves the single packet creates more complexity than it removes.
