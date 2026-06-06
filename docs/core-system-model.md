# Core System Model

This document defines the central semantic model of ChaOS:

Entity -> Signal -> State -> Decision -> Outcome -> Feedback

It exists because every future project needs a stable way to describe what exists, what is observed, what the system currently believes, what choices are made, what happens next, and what is learned.

## Overview

The model is industry-agnostic, but it is not free. A project must use this model only when the clarity and reuse benefit is greater than the translation cost.

In a sales system, an entity may be an account. In a medical spa system, an entity may be a client. In an RFP research system, an entity may be an opportunity. The model remains useful only if those domain concepts can be mapped without hiding important meaning.

## Primitive Summary

- Entity is what exists.
- Signal is what happened or was observed.
- State is what ChaOS currently believes or interprets.
- Decision is what should be done or reviewed.
- Outcome is what happened after action or review.
- Feedback is what changes future behavior or pattern confidence.

## Entity

### Meaning

An entity is the thing the system cares about. It is the durable object that receives signals, accumulates state, becomes the subject of decisions, produces outcomes, and accumulates feedback.

### Why It Exists

Without clear entities, systems confuse events, people, records, and goals. Entity clarity prevents downstream confusion.

### Interactions

Signals describe changes or observations about an entity. State interprets the current condition of an entity. Decisions are made about or because of an entity. Outcomes alter the state of an entity. Feedback improves how the system understands similar entities in the future.

### Example Implementations

- Sales OS: Account, contact, opportunity
- MedSpa CRM: Client, appointment, treatment plan
- RFP Research: RFP, agency, requirement
- AI Agent System: Task, user request, knowledge artifact

## Signal

### Meaning

A signal is an observed fact, event, pattern, or change that may influence state or a decision.

### Why It Exists

Systems need to separate raw observation from interpretation. A signal does not decide; it informs.

### Interactions

Signals attach to entities and may update state. Signal quality affects decision quality. Feedback may later change which signals are considered important.

### Example Implementations

- A prospect opened a pricing page.
- A client missed an appointment.
- An RFP requires SOC 2 compliance.
- A user repeatedly edits the same generated output.

## State

### Meaning

State is the current interpreted condition of an entity based on evidence, history, validation, and review status.

### Why It Exists

Without State, systems blur observation and decision. ChaOS must be able to say what it currently believes without pretending that belief is a fact or an approved action.

### Interactions

State is derived from entities, signals, history, validation results, and review status. Decisions use state as one input. Outcomes and feedback may confirm, change, or retire state.

### Example Implementations

- `account_is_warm`
- `identity_candidate_unresolved`
- `draft_entity_not_canonical`
- `access_review_needed`
- `context_insufficient`
- `stale_signal_detected`
- `validation_failed`

## Decision

### Meaning

A decision is a chosen interpretation, recommendation, classification, priority, or next step.

### Why It Exists

Systems create value when they help humans or agents decide what happens next.

### Interactions

Decisions consume entities, signals, state, and rationale. Decisions produce actions or recommendations and must be traceable. Outcomes reveal whether decisions were useful.

### Example Implementations

- Prioritize this lead for human follow-up.
- Recommend a client retention offer.
- Mark an RFP as a poor fit.
- Ask for clarification before generating an answer.

## Outcome

### Meaning

An outcome is what happened after a decision or action.

### Why It Exists

Outcomes prevent systems from mistaking activity for progress. A system that cannot observe outcomes cannot improve.

### Interactions

Outcomes update entity state and become evidence for feedback. Outcomes may confirm, weaken, or overturn prior assumptions.

### Example Implementations

- The prospect booked a meeting.
- The client accepted the offer.
- The RFP was declined.
- The user accepted the generated document.

## Feedback

### Meaning

Feedback is structured learning from outcomes, user responses, failures, and evaluation.

### Why It Exists

Feedback turns a system from a static process into a learning architecture.

### Interactions

Feedback modifies future signal interpretation, state rules, decision criteria, workflow design, agent prompts, documentation, and evaluation standards.

### Example Implementations

- Human rejected the recommendation because the lead was already disqualified.
- Evaluation found that the agent over-weighted urgency.
- A workflow failed because input validation was weak.
- A project inherited ChaOS successfully but needed a new decision record type.

## Semantic Model vs Workflow Model

The semantic model describes what the system knows and how that knowledge changes over time:

```text
Entity -> Signal -> State -> Decision -> Outcome -> Feedback
```

The workflow model describes how a specific run, event, or user action moves through the system:

```text
Trigger -> Input -> Processing -> Decision -> Action -> Feedback
```

A workflow is usually an execution over the semantic model. It is not a competing framework. For example, a workflow may start from a trigger, gather input about an entity, process signals into state, recommend a decision, route an action, and capture feedback.

## Cross-Domain Example

| Domain | Entity | Signal | State | Decision | Outcome | Feedback |
| --- | --- | --- | --- | --- | --- | --- |
| Sales | Account | Pricing page visit | Account is warm | Recommend outreach | Meeting booked | Signal was useful |
| MedSpa | Client | Missed appointment | Retention risk increased | Recommend retention call | Client rescheduled | Add grace-period rule |
| RFP | Opportunity | Requirement mismatch | Fit is weak | Recommend no-bid | Team declined RFP | Improve fit criteria |
| AI Agent | Task | User corrected output | Context insufficient | Recommend prompt update | Better next output | Add evaluation case |

## Future Considerations

Future versions may add formal notation, lifecycle states, or implementation adapters. Version 0.1 keeps the model intentionally simple and must prove that this vocabulary accelerates real builds before claiming broader portability.
