# Order Graph Overview

This document defines the Order Graph reference implementation track for ChaOS.

## Purpose

The Order Graph exists to make fragmented business tool data understandable before ChaOS moves toward implementation, automation, or agents.

The core definition is:

```text
The Order Graph is the structured, time-aware map ChaOS builds from fragmented tool data.
```

This file explains what the Order Graph is, how it fits into ChaOS, how it extends the core model, and what boundaries must remain in place while the reference implementation track is still being proven.

## What The Order Graph Is

The Order Graph is a structured map of business reality across tools, records, signals, actions, outcomes, and feedback.

Many organizations have important context scattered across CRMs, outreach tools, spreadsheets, analytics tools, support systems, notes, and human memory. Each tool has partial truth. The Order Graph creates a shared structure for understanding those fragments without pretending any one tool is the whole system.

The Order Graph is time-aware because business understanding changes. A signal observed last week, a meeting booked yesterday, and an outcome recorded today affect how an entity is understood now.

## What The Order Graph Is Not

The Order Graph is not a production app.

It is not a database design.

It is not a CRM, workflow engine, AI agent platform, frontend, integration hub, or vendor-specific tool.

It must not ingest real customer data, perform autonomous actions, depend on production integrations, or make hidden decisions at this stage.

The reference implementation track is allowed to define documentation, contracts, fixtures, deterministic local transformations, and testing gates. It is not allowed to become a product before the graph spine is proven.

## How It Fits Into ChaOS

ChaOS starts from the core model:

```text
Entity -> Signal -> Decision -> Outcome -> Feedback
```

The Order Graph extends that model into a more concrete reference implementation track:

```text
Domain -> Entity -> Source Record -> Relationship -> Signal -> State -> Decision -> Action -> Outcome -> Feedback
```

This extension does not replace the ChaOS core model. It gives the model a practical shape for business tool data.

The Order Graph helps ChaOS answer:

- What entities exist?
- Which source records describe them?
- Which records may refer to the same real-world thing?
- What signals have occurred over time?
- Which entities are affected by each signal?
- What state can be computed from visible evidence?
- What decisions or recommendations are justified?
- What actions happened?
- What outcomes and feedback changed future understanding?

## Core Objects

### Domain

A domain is a bounded business area, such as GTM / Sales, Customer Success, Support, Finance, or Delivery.

A domain prevents unrelated entities from being merged just because names look similar. For example, an account in a GTM domain and an account in a finance domain may not mean the same thing.

### Entity

An entity is the durable thing the system cares about.

Examples include account, person, opportunity, workflow, task, ticket, invoice, project, or vendor.

Entities receive signals, hold state, become the subject of decisions, produce outcomes, and accumulate feedback.

### Source Record

A source record is a record from a specific tool or source.

Examples include a Salesforce Account, Outreach Account, 6sense Company, LinkedIn Company, support ticket, spreadsheet row, meeting note, or analytics event.

Source records must remain traceable. The Order Graph must preserve which tool or source contributed each record.

### Relationship

A relationship connects objects in the graph.

Relationships can connect:

- Source records to entities
- Signals to entities
- People to accounts
- Opportunities to accounts
- Actions to decisions
- Outcomes to actions
- Feedback to outcomes

Relationships must make attachment visible instead of hiding logic in a tool-specific record shape.

### Signal

A signal is an observed fact, event, pattern, or change that may influence state, decisions, or actions.

Signals live once as independent time-based objects.

Signals attach to every relevant entity through relationships.

Entity views may show signals under accounts, people, opportunities, workflows, or other objects without duplicating the underlying signal.

This distinction matters because one signal may affect many entities. A meeting booked may affect an account, a person, an opportunity, and a workflow. The signal must not be physically duplicated under each object because duplicated signals create conflicting truth.

### State

State is the current interpreted condition of an entity based on visible records, signals, outcomes, and feedback.

State must be explainable. If an account has a priority score, buying stage, or recommended next action, the Order Graph must show which source records and signals contributed to that state.

### Decision

A decision is a chosen interpretation, recommendation, classification, priority, or next step.

At this stage, decisions must be recommendations or reviewable outputs. They must not become autonomous actions.

### Action

An action is what happened after a decision or recommendation.

Actions may include human follow-up, routing, review, status recording, task creation in a fixture, or other bounded behavior. Production write actions are prohibited at this stage.

### Outcome

An outcome is what happened after an action.

Examples include meeting booked, no response, SAL accepted, opportunity created, closed won, or closed lost.

Outcomes prevent the system from mistaking activity for progress.

### Feedback

Feedback is structured learning from outcomes, human review, corrections, and evaluation.

Feedback changes how future signals, state, and decisions are interpreted.

## Why Signals Live Independently

Signals must exist as independent objects because signals are often relevant to more than one entity.

If a signal is physically nested only under an account, a person view may miss it. If the same signal is copied under multiple objects, the graph may create conflicting versions of the same event.

The Order Graph uses this storage and view distinction:

```text
Signals live once as independent time-based objects.
Signals attach to every relevant entity through relationships.
Entity views may show signals under accounts, people, opportunities, workflows, or other objects without duplicating the underlying signal.
```

This makes the system inspectable. A future maintainer can ask where a signal came from, when it happened, which entities it affects, and how it influenced state or decisions.

## GTM Example

Domain: GTM / Sales

Entity: Account

Source records:

- Salesforce Account
- Outreach Account
- 6sense Company
- LinkedIn Company

Signals:

- Intent spike
- Email reply
- Website visit
- Meeting booked
- Opportunity created

State:

- Priority score
- Buying stage
- Active stakeholders
- Last meaningful touch
- Recommended next action

Outcome:

- Meeting booked
- No response
- SAL accepted
- Opportunity created
- Closed won/lost

In this example, an account may be represented by several source records across tools. The Order Graph resolves those records into a durable account entity when the matching evidence is strong enough.

Signals then attach to the account and to other relevant entities. For example, an email reply may attach to a person, account, and opportunity. The signal lives once, while each entity view can display it.

The account state may compute a priority score or recommended next action, but the reason must remain visible. The state must show which source records, signals, and outcomes contributed to the recommendation.

## Customer Success Example

Domain: Customer Success

Entity: Customer

Source records:

- CRM Account
- Support account
- Product workspace
- Contract record

Signals:

- Product usage drop
- Support ticket escalation
- Renewal date approaching
- New executive sponsor
- NPS response

State:

- Health score
- Renewal risk
- Active issues
- Expansion potential
- Recommended next action

Outcome:

- Renewal saved
- Expansion created
- Churned
- Support issue resolved

In this example, the customer may appear across commercial, support, product, and contract systems. The Order Graph keeps those source records traceable while resolving them into one durable customer entity when the evidence supports that resolution.

Signals attach to the customer and to other relevant entities, such as support tickets, product workspaces, stakeholders, or renewal workflows. The customer state must explain why the customer is healthy, at risk, ready for expansion, or in need of review.

This example keeps the Order Graph portable. The model must serve business understanding across domains, not only GTM or sales prioritization.

## Org-Wide Understanding Before Automation

The Order Graph supports org-wide understanding before it supports automation or AI agents.

That ordering matters.

First, ChaOS must prove that fragmented records can be resolved into inspectable entities.

Second, signals must attach correctly without duplication.

Third, entity state must be explainable.

Fourth, recommendations must be deterministic and reviewable.

Only after those gates pass may future work consider real integrations, automation, or agents.

## Examples Of Use

A sales leader wants to know which accounts deserve attention today. The Order Graph can combine source records, signals, states, outcomes, and feedback to produce a reviewable top-10 account recommendation.

A customer success leader wants to identify customers at renewal risk. The Order Graph can combine usage signals, support escalations, stakeholder changes, renewal dates, outcomes, and feedback into a reviewable recommendation.

A future maintainer wants to understand why an account or customer was prioritized. The Order Graph can trace the recommendation back to source records, signals, state computation, decisions, actions, outcomes, and feedback.

A reviewer finds a bad recommendation. The graph can preserve the correction as feedback instead of hiding the failure in a model prompt or dashboard note.

## Future Considerations

Future work may define schemas, fixture data, deterministic local transformation logic, identity resolution tests, signal attachment tests, and entity state computation.

Future work must stop at the testing gates defined for the Order Graph track.

Real integrations, databases, frontends, autonomous actions, and vendor-specific implementation choices must remain deferred until the graph spine is proven with fixtures and deterministic local tests.
