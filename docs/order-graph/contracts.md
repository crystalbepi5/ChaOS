# Order Graph Core Contracts

This document defines the authoritative plain-language contracts for the Order Graph core objects.

## Purpose

The contracts document exists so future Order Graph PRs can create fixtures, validation checks, and deterministic local transformation logic without guessing what each object means or owns.

Contracts define what each Order Graph object means, what it must contain conceptually, how it relates to other objects, how humans can validate it, and how it can fail.

Contracts are not JSON schemas, database schemas, API contracts, or code models. Those may be created later only after the contracts are reviewed and approved.

## How This Fits Into ChaOS

ChaOS requires humans to understand the system before implementation. These contracts operationalize the Order Graph model in plain language before the project creates fixtures, schemas, scripts, local engines, integrations, UI, agents, or deployment work.

This document supports Gate 1: Core contracts validate.

It also follows the sequencing source in `docs/order-graph/technical-requirements-and-development-roadmap.md`. That roadmap defines when future PRs may introduce fixtures, validation checks, and deterministic local transformation logic. This contract document defines the object obligations those future PRs must satisfy.

## Core Model

The Order Graph uses this model:

```text
Domain -> Entity -> Source Record -> Relationship -> Signal -> State -> Decision -> Action -> Outcome -> Feedback
```

The contracts in this document make that model reviewable. Each object must have a clear purpose, required conceptual fields, relationship boundaries, examples, validation expectations, and failure modes.

## Contract Standards

Every Order Graph object contract must satisfy these standards:

- The object must remove confusion about ownership or responsibility.
- The object must preserve traceability to source records, evidence, assumptions, or review decisions.
- The object must remain implementation-neutral.
- The object must not depend on a specific vendor, database, programming language, API, or model provider.
- The object must be understandable by a future maintainer without private context.
- The object must include failure modes so reviewers can reject weak or premature implementations.

## Domain

### Purpose

A Domain is the business function or operating area the graph is modeling.

The Domain prevents unrelated objects from being merged across contexts. It defines the operating boundary for entities, source records, rules, and success measures.

### Required Conceptual Fields

A Domain must conceptually include:

- Domain identifier
- Name
- Business function
- Owner or responsible team
- Primary objective
- Success metric
- Allowed entity types
- Active rules or constraints

### Relationships

A Domain contains or bounds:

- Entities
- SourceRecords
- EntityRelationships
- Signals
- EntityStates
- Decisions
- Actions
- Outcomes
- Feedback

A Domain may share source systems with another Domain, but the meaning of entities and state must remain domain-specific unless a future contract defines cross-domain behavior.

### Example

Domain: GTM / Sales

Business function: revenue generation

Owner or responsible team: revenue operations

Primary objective: prioritize accounts for human review

Success metric: reviewed recommendations that lead to qualified meetings

Allowed entity types: Account, Contact, Opportunity, User, Sequence

### Validation Expectations

A valid Domain must:

- Have a stable identifier and name.
- Name the business function it represents.
- Identify an owner or responsible team.
- State the primary objective and success metric.
- List allowed entity types.
- Name active rules or constraints that affect interpretation.
- Be narrow enough for a human reviewer to understand what belongs inside it.

### Failure Modes

A Domain fails review when:

- The domain is too broad.
- The domain overlaps another domain without explanation.
- The domain has no owner.
- The domain success metric is unclear.
- The domain is defined by a vendor instead of a business function.
- The domain allows entities that do not share a meaningful operating context.

## Entity

### Purpose

An Entity is the canonical business object ChaOS cares about inside a domain.

The Entity is not a raw tool record. It is the durable object that receives signals, holds state, becomes the subject of decisions, produces outcomes, and accumulates feedback.

### Required Conceptual Fields

An Entity must conceptually include:

- Entity identifier
- Domain identifier
- Entity type
- Canonical name
- Canonical keys
- Source traceability
- Confidence
- Current state reference

Canonical keys are the stable matching clues used to identify the entity, such as canonical domain for an Account or email for a Contact. Canonical keys must remain explainable and must not hide matching assumptions.

### Relationships

An Entity may relate to:

- Domain as its operating boundary
- SourceRecords as evidence
- EntityRelationships as connections to other entities
- SignalEntityLinks as signal attachments
- EntityState as current interpretation
- Decisions as recommendations or classifications
- Actions as approved or executed steps
- Outcomes as observed results
- Feedback as structured learning

### Example

Entity: Account

Canonical name: Acme Example Co

Canonical keys: `acme.example`, normalized account name

Source traceability: Salesforce-like Account, Outreach-like Account, 6sense-like Company

Confidence: high because canonical domain and normalized name align

### Validation Expectations

A valid Entity must:

- Have a stable identifier.
- Belong to one Domain.
- Have a clear entity type.
- Preserve source traceability.
- State the evidence and confidence behind its canonical identity.
- Avoid treating weak matches as confirmed identity.
- Reference current state only when an EntityState exists.

### Failure Modes

An Entity fails review when:

- The entity is confused with a source record.
- The entity has no stable identity.
- The entity is over-merged from weak matches.
- The entity has no traceable source evidence.
- The entity crosses domains without a documented rule.
- The entity hides uncertainty about its identity.

## SourceRecord

### Purpose

A SourceRecord is a vendor/tool/system-specific record that may describe or partially describe a real-world entity.

The SourceRecord preserves source truth before the Order Graph interprets it. It is evidence, not the canonical object.

### Required Conceptual Fields

A SourceRecord must conceptually include:

- Source record identifier
- Source system
- Source object type
- Source native ID
- Raw/source values
- Normalized values
- Ingested or observed timestamp
- Source reference
- Status or freshness marker when known

### Relationships

A SourceRecord may relate to:

- Domain as the operating boundary where it is interpreted
- Entity through identity resolution evidence
- Signal when the source record contains or causes a time-based observation
- EntityState when source data contributes to state
- Decision when source data supports a recommendation

A SourceRecord must not replace Entity. It may describe an Entity, support an Entity, or remain unresolved.

### Example

SourceRecord: Salesforce-like Account

Source system: Salesforce-like CRM

Source object type: Account

Source native ID: fake-account-001

Raw/source values: account name, website, owner, stage

Normalized values: normalized name, canonical domain

### Validation Expectations

A valid SourceRecord must:

- Preserve source system and native ID.
- Keep raw/source values conceptually separate from normalized values.
- Include a timestamp for ingestion or observation.
- Preserve a source reference.
- Remain vendor-specific only at the source-record layer.
- Avoid becoming canonical truth without resolution evidence.

### Failure Modes

A SourceRecord fails review when:

- The source record is treated as canonical truth.
- The source record loses its source reference.
- Source-specific fields leak into core contracts.
- Deleted or stale records are treated as current without status.
- Raw values and normalized values are mixed without explanation.
- The source record is resolved into an Entity without visible evidence.

## EntityRelationship

### Purpose

An EntityRelationship connects two canonical entities.

It makes entity-to-entity structure explicit, directional, and reviewable.

### Required Conceptual Fields

An EntityRelationship must conceptually include:

- Relationship identifier
- Source entity
- Target entity
- Relationship type
- Direction
- Confidence
- Evidence
- Effective time range if relevant

### Relationships

An EntityRelationship connects Entity to Entity.

It may be supported by SourceRecords, Signals, Actions, Outcomes, or Feedback, but it must preserve the evidence that justifies the relationship.

### Example

Relationship: Contact belongs to Account

Source entity: Contact Jane Example

Target entity: Account Acme Example Co

Direction: Contact -> Account

Evidence: email domain and CRM-like association match

### Validation Expectations

A valid EntityRelationship must:

- Connect two valid Entities.
- Name the relationship type.
- State direction clearly.
- Preserve evidence.
- Include confidence.
- Include an effective time range when the relationship may change over time.

### Failure Modes

An EntityRelationship fails review when:

- Relationship direction is ambiguous.
- Relationship exists without evidence.
- Relationship duplicates another relationship.
- Relationship is treated as permanent when it is time-bound.
- Relationship connects raw SourceRecords instead of canonical Entities.
- Relationship type is too vague to validate.

## Signal

### Purpose

A Signal is an independent time-based observation, event, pattern, or change that may influence state or decisions.

Signals must live once and attach to entities through SignalEntityLink.

### Required Conceptual Fields

A Signal must conceptually include:

- Signal identifier
- Signal type
- Source system
- Occurred at timestamp
- Observed at timestamp if different
- Raw payload or source reference
- Normalized summary
- Strength or weight if applicable
- Confidence
- Expiration or stale-after rule if applicable

### Relationships

A Signal may relate to:

- SourceRecord as source evidence
- Entity through SignalEntityLink
- EntityState as supporting evidence
- Decision as rationale
- Outcome or Feedback when future learning changes signal interpretation

A Signal must not own an Entity. A Signal must not become a Decision.

### Example

Signal: Intent spike

Source system: 6sense-like intent source

Occurred at timestamp: fake date in fixture

Observed at timestamp: fake import date in fixture

Normalized summary: account showed elevated interest in pricing topic

Confidence: medium

Stale-after rule: 30 days unless refreshed

### Validation Expectations

A valid Signal must:

- Have one conceptual identity.
- Include a time anchor.
- Preserve source traceability.
- State its type and normalized summary.
- Include confidence when interpretation is uncertain.
- Include staleness rules when the signal weakens over time.
- Attach to entities only through SignalEntityLink.

### Failure Modes

A Signal fails review when:

- Signal is duplicated under multiple entities.
- Signal is treated as a decision.
- Signal has no timestamp.
- Signal has no source traceability.
- Signal is stale but still over-weighted.
- Signal strength or confidence is hidden.

## SignalEntityLink

### Purpose

A SignalEntityLink attaches one signal to one relevant entity.

This allows the same signal to be viewed under multiple entities without duplicating the signal.

### Required Conceptual Fields

A SignalEntityLink must conceptually include:

- Link identifier
- Signal identifier
- Entity identifier
- Relationship role
- Relevance weight
- Evidence or matching rule
- Confidence

### Relationships

A SignalEntityLink connects one Signal to one Entity.

A Signal may have many SignalEntityLinks. An Entity may have many SignalEntityLinks. Each link must explain why the signal matters to that entity.

### Example

Signal: Email reply

SignalEntityLink 1: email reply links to Contact as actor

SignalEntityLink 2: email reply links to Account as parent account

SignalEntityLink 3: email reply links to Sequence as source workflow

### Validation Expectations

A valid SignalEntityLink must:

- Reference one existing Signal.
- Reference one existing Entity.
- State the relationship role.
- Explain relevance.
- Include confidence.
- Preserve the evidence or matching rule.

### Failure Modes

A SignalEntityLink fails review when:

- Signal is physically duplicated instead of linked.
- Link role is unclear.
- Link attaches a signal to the wrong entity.
- Link confidence is hidden.
- Link relevance is asserted without evidence.
- Multiple links conflict without explanation.

## EntityState

### Purpose

EntityState is the computed current understanding of an entity based on source records, relationships, signals, actions, outcomes, and rules.

EntityState must explain itself. It must not hide scoring logic, ignore unknowns, or pretend uncertainty is certainty.

### Required Conceptual Fields

An EntityState must conceptually include:

- Entity state identifier
- Entity identifier
- Computed at timestamp
- State label
- Score or priority if applicable
- Primary reason
- Supporting signals
- Supporting source records or relationships
- Unknowns
- Confidence
- Recommended next decision or action if applicable

### Relationships

An EntityState may depend on:

- Entity as the subject
- SourceRecords as evidence
- EntityRelationships as context
- Signals and SignalEntityLinks as observed inputs
- Actions, Outcomes, and Feedback as learning inputs
- Decision as a downstream recommendation

### Example

EntityState: Account priority state

State label: active buying signal

Score: 82

Primary reason: intent spike and email reply occurred within the active review window

Supporting signals: intent spike, email reply

Unknowns: no confirmed budget owner

Recommended next decision: route to human review for outreach recommendation

### Validation Expectations

A valid EntityState must:

- Reference one Entity.
- Include a computed time.
- State the current label or status.
- Explain score or priority when present.
- Reference supporting signals and source evidence.
- Preserve unknowns.
- State confidence.
- Produce the same state for the same inputs when deterministic rules are used.

### Failure Modes

An EntityState fails review when:

- State cannot explain itself.
- State overclaims confidence.
- State ignores unknowns.
- State is not reproducible.
- State uses hidden logic.
- State is confused with a Decision.
- State depends on stale signals without a staleness rule.

## Decision

### Purpose

A Decision is a chosen interpretation, classification, recommendation, priority, or next step.

A Decision is not an Action. It names what the system recommends or classifies, why it recommends it, and what evidence supports it.

### Required Conceptual Fields

A Decision must conceptually include:

- Decision identifier
- Entity identifier
- Decision type
- Decision summary
- Rationale
- Supporting signals
- Supporting state
- Confidence
- Unknowns
- Reviewer or approver if applicable
- Review status

### Relationships

A Decision may relate to:

- Entity as the subject
- EntityState as the interpreted condition
- Signal and SignalEntityLink as supporting evidence
- Action as the follow-on step
- Outcome as later evidence
- Feedback as review or correction

### Example

Decision: Prioritize account

Entity: Account Acme Example Co

Decision summary: recommend human follow-up today

Rationale: account has recent intent spike, email reply, and no recent human touch

Confidence: medium-high

Unknowns: buying committee not fully known

### Validation Expectations

A valid Decision must:

- Reference the entity it concerns.
- State the decision type.
- Include rationale.
- Reference supporting evidence.
- Include confidence and unknowns.
- Remain separate from Action.
- Preserve review status or approval boundary when needed.

### Failure Modes

A Decision fails review when:

- Decision lacks rationale.
- Decision is confused with an action.
- Decision has no supporting evidence.
- Decision is automated without approval.
- Decision cannot be overridden.
- Decision hides unknowns.
- Decision depends on vendor-specific fields as core requirements.

## Action

### Purpose

An Action is a recommended, approved, or executed step that follows a decision.

An Action records what happened or what is proposed to happen. Early Order Graph work may model actions in fixtures or documentation, but production write actions remain prohibited.

### Required Conceptual Fields

An Action must conceptually include:

- Action identifier
- Related decision
- Entity identifier
- Action type
- Action status
- Actor
- Approval status
- Execution timestamp if executed
- Reversibility or rollback notes if relevant

### Relationships

An Action may relate to:

- Decision as the reason for action
- Entity as the subject
- Outcome as the observed result
- Feedback as review of action quality

### Example

Action: Request human review

Related decision: prioritize account

Entity: Account Acme Example Co

Action status: recommended

Actor: system recommendation for human operator

Approval status: not executed

### Validation Expectations

A valid Action must:

- Reference a Decision.
- Reference the Entity affected.
- State action status.
- Identify actor or intended actor.
- State approval status.
- Preserve execution time if executed.
- Preserve rollback notes when the action may have durable effects.

### Failure Modes

An Action fails review when:

- Action happens without approval.
- Action updates the wrong entity.
- Action is irreversible too early.
- Action is not recorded.
- Action result is never captured.
- Action is confused with a Decision.
- Action implies production writes before approval.

## Outcome

### Purpose

An Outcome is what happened after a decision or action.

Outcomes prevent the system from mistaking activity for progress. They create evidence for future feedback and state changes.

### Required Conceptual Fields

An Outcome must conceptually include:

- Outcome identifier
- Related entity
- Related action or decision
- Outcome type
- Outcome timestamp
- Outcome value or status
- Source evidence
- Business impact if known
- Causality confidence when relevant

### Relationships

An Outcome may relate to:

- Entity as the subject
- Action or Decision as the preceding event
- SourceRecord as evidence
- EntityState as future input
- Feedback as learning from the outcome

### Example

Outcome: Meeting booked

Related entity: Account Acme Example Co

Related action: human follow-up after recommendation

Outcome timestamp: fake fixture date

Source evidence: calendar-like meeting record in fixture

Business impact: qualified meeting created

### Validation Expectations

A valid Outcome must:

- Reference the related Entity.
- Reference the Action or Decision it evaluates.
- State outcome type and time.
- Preserve evidence.
- Avoid overstating causality when causality is uncertain.
- Remain separate from Feedback.

### Failure Modes

An Outcome fails review when:

- Outcome is not connected to the action or decision that caused it.
- Outcome is too vague.
- Outcome is captured too late.
- Outcome is treated as proof when causality is uncertain.
- Outcome is confused with Feedback.
- Outcome lacks source evidence.

## Feedback

### Purpose

Feedback is structured learning from outcomes, human review, errors, overrides, and evaluation.

Feedback explains what the system or reviewer learned and how future interpretation may improve. Feedback must not silently rewrite source truth.

### Required Conceptual Fields

Feedback must conceptually include:

- Feedback identifier
- Feedback source
- Related entity
- Related decision/action/outcome
- Feedback type
- Feedback summary
- Suggested adjustment
- Reviewed status
- Feedback timestamp

### Relationships

Feedback may relate to:

- Entity as the affected subject
- Decision, Action, or Outcome as the reviewed object
- EntityState as future interpretation input
- Signal as future weighting or relevance evidence
- Domain rules when repeated feedback justifies a rule change

### Example

Feedback: Human rejected recommendation

Related decision: prioritize account

Feedback summary: account is already disqualified due to unsupported region

Suggested adjustment: add region eligibility as an unknown or rule input before prioritization

Reviewed status: accepted for future contract or validation review

### Validation Expectations

Valid Feedback must:

- Identify who or what provided the feedback.
- Reference what it evaluates.
- State feedback type and summary.
- Include suggested adjustment when possible.
- Preserve reviewed status.
- Avoid silently overwriting source records.

### Failure Modes

Feedback fails review when:

- Feedback is too vague to use.
- Feedback is not connected to what it evaluates.
- Feedback never changes future behavior.
- Feedback silently overrides source truth.
- Feedback is treated as an Outcome.
- Feedback hides the reviewer or source.

## Cross-Domain Examples

### GTM / Sales Example

Domain: GTM / Sales

Entities:

- Account
- Contact

SourceRecords:

- Salesforce-like Account
- Outreach-like Prospect
- 6sense-like Company

Signals:

- Intent spike
- Email reply

Signal storage and links:

- Intent spike lives once as a Signal and links to Account.
- Email reply lives once as a Signal and links to Contact as actor and Account as parent account.

EntityState:

- Account priority state uses source records, intent spike, email reply, unknowns, and confidence.

Decision:

- Recommended next action: human follow-up.

Outcome:

- Meeting booked outcome records what happened after follow-up.

### Customer Success Example

Domain: Customer Success

Entities:

- Customer
- Product workspace
- Support account
- Contract record

Signals:

- Usage drop
- Support escalation

Signal storage and links:

- Usage drop lives once as a Signal and links to Customer and Product workspace.
- Support escalation lives once as a Signal and links to Customer and Support account.

EntityState:

- Renewal risk state uses usage drop, support escalation, contract context, unknowns, and confidence.

Decision:

- Recommended next action: human renewal risk review.

Outcome:

- Renewal saved outcome records what happened after human intervention.

## Signal Storage And View Model

Signals live once as independent time-based objects.
Signals attach to every relevant entity through SignalEntityLink.
Entity views may show signals under accounts, people, opportunities, workflows, or other objects without duplicating the underlying signal.

The storage model defines where truth lives. In the Order Graph, the Signal is the truth object. It has one conceptual identity, one source reference, and one time anchor.

The view model defines how humans inspect truth. Account, person, opportunity, workflow, customer, ticket, or workspace views may show the same signal because the signal is linked to each relevant entity. Those views must not create new copies of the signal.

This distinction prevents duplicated truth. If an email reply affects a Contact, Account, and Sequence, the graph stores one Signal and three SignalEntityLinks. Each view can show the reply, but the signal itself remains one object.

## Contract Validation Checklist

Gate 1 passes only when a human reviewer can confirm:

- Every core object has a clear purpose.
- Every core object has required conceptual fields.
- Every core object defines relationships to other objects.
- Every core object includes examples.
- Every core object includes validation expectations.
- Every core object includes failure modes.
- Contracts remain implementation-neutral.
- Contracts do not require any specific vendor.
- Contracts do not introduce code, JSON schemas, database schemas, or API contracts.
- Signals live once and attach through links.
- Decisions remain separate from actions.
- Outcomes remain separate from feedback.

A reviewer must request changes if any contract depends on private context, hides a responsibility boundary, or introduces implementation artifacts before Gate 1 approval.

## What This Document Does Not Approve

This document does not approve:

- JSON schemas
- Database schemas
- API contracts
- Python models
- TypeScript types
- Pydantic models
- Fixtures
- Scripts
- Local engine code
- External integrations
- UI
- Autonomous agents
- Production deployment

This document also does not approve real customer data ingestion, production write actions, dashboard work, authentication, CI/CD, or vendor-specific architecture.

## Examples Of Use

A future maintainer can use this document to decide whether `docs/order-graph/contracts.md` satisfies Gate 1 before fixture work begins.

A reviewer can use the validation checklist to reject a proposed fixture PR if the objects are not yet clear enough to validate.

A future implementation PR can reference these contracts to prove that code is implementing approved object responsibilities instead of inventing new architecture.

## Future Considerations

Future PRs may create fixture data, validation checks, JSON schemas, or deterministic local transformation logic only when the relevant gates allow that work.

If future validation reveals that a contract is ambiguous, the contract must be revised before implementation expands.

If a contract change affects core object meaning, source traceability, relationship ownership, signal storage, decision boundaries, or approval boundaries, the change must be reviewed as an architectural change.

## Next Recommended PR

Next recommended PR: Add GTM fixture data

Only after this contracts document is reviewed and Gate 1 is approved may the project create fixture data.
