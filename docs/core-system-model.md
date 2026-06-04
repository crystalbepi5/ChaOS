# Core System Model

This document defines the central model of ChaOS:

Entity -> Signal -> Decision -> Outcome -> Feedback

It exists because every future project needs a stable way to describe what exists, what is observed, what choices are made, what happens next, and what is learned.

## Overview

The model is industry-agnostic. A project can change the business context while preserving the architecture.

In a sales system, an entity may be an account. In a medical spa system, an entity may be a client. In an RFP research system, an entity may be an opportunity. The model remains the same.

## Entity

### Meaning

An entity is the thing the system cares about. It is the durable object that receives signals, becomes the subject of decisions, produces outcomes, and accumulates feedback.

### Why It Exists

Without clear entities, systems confuse events, people, records, and goals. Entity clarity prevents downstream confusion.

### Interactions

Signals describe changes or observations about an entity. Decisions are made about or because of an entity. Outcomes alter the state of an entity. Feedback improves how the system understands similar entities in the future.

### Example Implementations

- Sales OS: Account, contact, opportunity
- MedSpa CRM: Client, appointment, treatment plan
- RFP Research: RFP, agency, requirement
- AI Agent System: Task, user request, knowledge artifact

## Signal

### Meaning

A signal is an observed fact, event, pattern, or change that may influence a decision.

### Why It Exists

Systems need to separate raw observation from interpretation. A signal does not decide; it informs.

### Interactions

Signals attach to entities and feed decisions. Signal quality affects decision quality. Feedback may later change which signals are considered important.

### Example Implementations

- A prospect opened a pricing page.
- A client missed an appointment.
- An RFP requires SOC 2 compliance.
- A user repeatedly edits the same generated output.

## Decision

### Meaning

A decision is a chosen interpretation, recommendation, classification, priority, or next step.

### Why It Exists

Systems create value when they help humans or agents decide what should happen next.

### Interactions

Decisions consume signals, produce actions or recommendations, and should be traceable to rationale. Outcomes reveal whether decisions were useful.

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

Outcomes update the entity state and become evidence for feedback. Outcomes may confirm, weaken, or overturn prior assumptions.

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

Feedback modifies future signal weighting, decision criteria, workflow design, agent prompts, documentation, and evaluation standards.

### Example Implementations

- Human rejected the recommendation because the lead was already disqualified.
- Evaluation found that the agent over-weighted urgency.
- A workflow failed because input validation was weak.
- A project inherited ChaOS successfully but needed a new decision record type.

## Cross-Domain Example

| Domain | Entity | Signal | Decision | Outcome | Feedback |
| --- | --- | --- | --- | --- | --- |
| Sales | Account | Pricing page visit | Recommend outreach | Meeting booked | Signal was useful |
| MedSpa | Client | Missed appointment | Recommend retention call | Client rescheduled | Add grace-period rule |
| RFP | Opportunity | Requirement mismatch | Recommend no-bid | Team declined RFP | Improve fit criteria |
| AI Agent | Task | User corrected output | Recommend prompt update | Better next output | Add evaluation case |

## Future Considerations

Future versions may add formal notation, lifecycle states, or implementation adapters. Version 0.1 keeps the model intentionally simple so every future project can inherit it.

