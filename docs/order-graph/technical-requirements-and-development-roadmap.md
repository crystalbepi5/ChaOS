# Order Graph Technical Requirements and Development Roadmap

## 1. Purpose

This document adapts an incremental application-building approach to ChaOS, but replaces "build the app now" with "define gated requirements before implementation."

This document is the bridge between Order Graph architecture and future implementation.

It exists so future Codex runs can build the Order Graph methodically through small, reviewable PRs. It defines requirements, object expectations, testing strategy, and a gated PR roadmap without approving application code, production integrations, databases, UI work, autonomous agents, or deployment architecture.

This document fits into ChaOS by turning the existing Order Graph overview, roadmap, testing gates, and decision record into a practical development sequence. It must remain subordinate to ChaOS Core and must not convert ChaOS into a premature product.

Example use: a future maintainer can read this document before opening an implementation PR and know which gate they are targeting, what evidence they need, and what remains prohibited.

Future consideration: this document may be revised after real fixture reviews reveal missing requirements, but revisions must preserve the gated sequence.

## 2. Product Vision

ChaOS turns fragmented business tool data into org-wide understanding.

The Order Graph creates a shared, time-aware understanding layer for humans, reports, workflows, automation, and eventually AI agents. It does this by resolving scattered source records into durable entities, preserving traceability, attaching independent signals to relevant entities, computing explainable state, and producing reviewable recommendations.

The vision is not to make a smarter dashboard or a larger CRM. The vision is to make business reality easier to inspect. A human must be able to ask what happened, where the evidence came from, why a recommendation exists, what action followed, and what outcome changed future understanding.

The first useful expression of this vision is a deterministic, traceable recommendation workflow: Top 10 accounts to focus today and why.

## 3. Business Requirements

### REQ-OG-001: The system must resolve fragmented source records into canonical entities.

Description: The system must identify when records from different sources describe the same durable entity.

Rationale: Organizations often have partial records spread across tools. Without canonical entities, downstream state and recommendations become fragmented.

Acceptance criteria:

- Source records can be linked to a canonical entity when evidence supports the match.
- Weak matches are marked unresolved instead of guessed.
- The reason for each resolution is visible.

Example: A Salesforce-like account record and an Outreach-like account record with the same canonical domain resolve into one Account entity.

### REQ-OG-002: The system must preserve source record traceability.

Description: Every canonical entity, signal, state value, decision, action, outcome, and feedback record must trace back to the source records or assumptions that informed it.

Rationale: Traceability keeps the system inspectable and prevents hidden business logic.

Acceptance criteria:

- Source name and source record identifier are preserved conceptually for each source record.
- Derived objects can explain which source records contributed to them.
- Missing source references fail review.

Example: A priority recommendation references the source records and signals that supported it.

### REQ-OG-003: The system must treat signals as independent time-based objects.

Description: Signals must be stored conceptually as independent observed facts, events, patterns, or changes.

Rationale: One signal may affect multiple entities. Independent signals prevent duplicated or conflicting truth.

Acceptance criteria:

- Each signal has one conceptual identity.
- Each signal has an observed time or time window.
- Signals are not physically nested as exclusive children of a single entity type.

Example: A meeting booked signal exists once and may attach to an Account, Contact, Opportunity, and Workflow.

### REQ-OG-004: The system must attach signals to relevant entities through relationships.

Description: Signals must connect to entities through explicit relationships such as SignalEntityLink.

Rationale: Relationship-based attachment lets different entity views display the same signal without duplicating it.

Acceptance criteria:

- Signal-to-entity links are explicit.
- A signal may attach to more than one entity.
- Entity views must not create duplicate signal objects.

Example: An email reply signal attaches to both the Contact who replied and the Account that owns the relationship.

### REQ-OG-005: The system must compute entity state from traceable source records and signals.

Description: Entity state must be derived from visible evidence such as source records, relationships, signals, outcomes, and feedback.

Rationale: State is only useful when humans can understand why it exists.

Acceptance criteria:

- Each state field has visible supporting evidence.
- Unknown or insufficient evidence produces an unknown or unresolved state.
- State computation is deterministic for the same input.

Example: Account renewal risk increases because product usage dropped, a support ticket escalated, and renewal date is approaching.

### REQ-OG-006: The system must produce explainable recommendations.

Description: Recommendations must state what is recommended and why.

Rationale: A recommendation without explanation cannot be audited, trusted, or improved.

Acceptance criteria:

- Each recommendation references supporting entities, signals, state, outcomes, or feedback.
- Each recommendation includes uncertainty or unknowns when relevant.
- Recommendations remain reviewable by humans.

Example: The system recommends focusing on Account A because buying intent increased, a stakeholder replied, and the account has no recent human follow-up.

### REQ-OG-007: The system must capture outcomes and feedback.

Description: The system must preserve what happened after recommendations and what humans learned from the result.

Rationale: Outcomes and feedback let the system improve instead of repeating unreviewed assumptions.

Acceptance criteria:

- Outcomes connect to decisions or actions.
- Feedback can record acceptance, rejection, correction, or review notes.
- Feedback remains traceable to the recommendation it evaluates.

Example: A human rejects a recommendation because the account is already disqualified, and that rejection becomes feedback.

### REQ-OG-008: The system must recommend before automating.

Description: The system must prove recommendation quality before any autonomous action is considered.

Rationale: Recommendation creates a lower-risk learning loop. Automation must be earned.

Acceptance criteria:

- Early workflows produce recommendations only.
- Human review is required before any action boundary expands.
- Autonomous write actions remain prohibited until a future decision record approves them.

Example: The top-10 workflow recommends accounts to review; it does not send outreach or update a CRM.

### REQ-OG-009: The system must avoid vendor lock-in.

Description: Core Order Graph concepts must not depend on one vendor, tool, platform, database, model provider, or CRM.

Rationale: ChaOS is portable architecture. Vendor assumptions would make the Order Graph less reusable.

Acceptance criteria:

- Source records are modeled generically.
- Vendor-like examples are labeled as examples, not requirements.
- No core requirement depends on a specific external system.

Example: Salesforce-like records may be used in fixtures, but the contract remains SourceRecord.

### REQ-OG-010: The system must remain inspectable by a human.

Description: A human reviewer must be able to understand inputs, transformations, decisions, outputs, and failure modes.

Rationale: Inspectability is the trust boundary for future implementation.

Acceptance criteria:

- Logic is documented before it is implemented.
- Test outputs are small enough to review.
- Hidden model reasoning, hidden weighting, and opaque vendor logic fail review.

Example: A reviewer can trace why an account appears in the top-10 list without reading private chat history or trusting a model response.

## 4. Stakeholders and Users

### Builder / Maintainer

They need clear contracts, gate boundaries, file targets, and merge criteria.

They must not be forced to understand private conversation history or unstated business assumptions.

Risk introduced: they may implement too early or add abstractions before the graph spine is proven.

### Operator / Business User

They need recommendations that explain what to review and why.

They must not be forced to understand schemas, code, identity resolution internals, or vendor-specific mapping details.

Risk introduced: they may ask for dashboards or automation before recommendations are tested.

### Reviewer / Manager

They need pass/fail criteria, audit notes, risk visibility, and the ability to challenge recommendations.

They must not be forced to understand implementation internals to know whether a gate passed.

Risk introduced: they may approve work because it feels useful instead of because the gate evidence exists.

### Analyst / Reporting User

They need consistent entities, traceable source records, stable state definitions, and reusable outputs.

They must not be forced to reconcile conflicting tool records manually.

Risk introduced: they may treat early fixture outputs as production analytics.

### Agent / Automation Consumer

They need structured, traceable context that can support future recommendations.

They must not be forced to infer missing rules, invent data, or act without approval boundaries.

Risk introduced: agents may overreach, hide uncertainty, or convert recommendations into actions.

### Future Integrations Owner

They need clear readiness criteria before connecting real systems.

They must not be forced to reverse-engineer why a vendor was selected or how data should be governed.

Risk introduced: they may let a vendor shape the core model before the graph is proven.

## 5. Non-Goals

This roadmap does not approve:

- Production app development
- Real integrations
- Real customer data ingestion
- Databases
- Frontend UI
- Authentication
- LLM reasoning
- Autonomous write actions
- Dashboards
- Deployment architecture

It also does not approve hidden business logic, broad data ingestion, vendor-specific architecture, or implementation work outside the relevant gate.

## 6. Architecture Principles

### Order before intelligence

Meaning: the system must establish clear objects, relationships, state, and traceability before adding intelligent behavior.

Future PRs must respect this by proving structure before model usage, ranking, or automation.

### Contracts before schemas

Meaning: object responsibilities, required fields, relationships, examples, and validation expectations must be defined in plain language before JSON schemas, database schemas, API contracts, or code are created.

Future PRs must respect this by completing `docs/order-graph/contracts.md` before implementation artifacts.

### Fixtures before integrations

Meaning: fake, human-reviewable examples must prove the model before real data or tool connections are considered.

Future PRs must respect this by using only fake fixture data until the relevant gates pass.

### Determinism before agents

Meaning: the system must produce the same output for the same input before agent reasoning is introduced.

Future PRs must respect this by building deterministic local checks before LLM or agent workflows.

### Recommendations before automation

Meaning: the system must recommend reviewable next actions before it performs actions automatically.

Future PRs must respect this by prohibiting automatic outreach, CRM writes, task creation, or other autonomous write actions.

### Traceability before optimization

Meaning: the system must preserve evidence and rationale before optimizing speed, scoring, ranking, or scale.

Future PRs must respect this by making every derived output traceable to inputs.

### Human review before scale

Meaning: human reviewers must be able to inspect and challenge recommendations before the system expands.

Future PRs must respect this by preserving review and override paths.

## 7. Core System Model

ChaOS Core uses:

```text
Entity -> Signal -> Decision -> Outcome -> Feedback
```

The Order Graph extends that into:

```text
Domain -> Entity -> Source Record -> Relationship -> Signal -> State -> Decision -> Action -> Outcome -> Feedback
```

Domain bounds the business area so unrelated things are not merged across contexts.

Entity is the durable thing the system cares about, such as an account, contact, customer, opportunity, ticket, workspace, or workflow.

Source Record is the record from a tool or source that contributes evidence.

Relationship connects records, entities, signals, decisions, actions, outcomes, and feedback.

Signal is an independent time-based observation that may influence state or decisions.

State is the current interpreted condition of an entity based on visible evidence.

Decision is a recommendation, classification, priority, or next step.

Action records what happened after a decision or recommendation.

Outcome records the result of an action.

Feedback records human review, correction, evaluation, or learning from outcomes.

## 8. Core Object Requirements

### Domain

Purpose: bound the business context for entities and records.

Required fields, conceptually: domain identifier, domain name, purpose, allowed entity types, source boundary.

Relationships: contains entities and source records.

Example: GTM / Sales.

Validation expectations: the domain must be named, understandable, and separate from unrelated domains.

Failure modes: vague domain names, accidental cross-domain merging, or vendor-defined domains.

### Entity

Purpose: represent the durable thing the system cares about.

Required fields, conceptually: entity identifier, entity type, domain, display name, status or lifecycle marker, source record references.

Relationships: linked to source records, signals, state, decisions, actions, outcomes, and feedback.

Example: Account entity for Acme Example Co.

Validation expectations: entity type and domain must be clear, and source references must be traceable.

Failure modes: confusing source records with entities, merging weak matches, or creating entities without evidence.

### SourceRecord

Purpose: preserve a record from a specific source before it becomes interpreted.

Required fields, conceptually: source name, source record identifier, source record type, observed fields, observed time or import time, raw source reference.

Relationships: may link to one or more entities through identity resolution.

Example: Salesforce-like Account record with domain, company name, owner, and stage.

Validation expectations: source identity and record identity must be present.

Failure modes: losing source traceability, treating source fields as canonical truth, or importing real customer data too early.

### EntityRelationship

Purpose: connect entities or connect source records to entities with a visible reason.

Required fields, conceptually: relationship identifier, relationship type, source object, target object, evidence, confidence or certainty label.

Relationships: links source records, entities, and other graph objects.

Example: SourceRecord belongs_to Entity because canonical domain matches.

Validation expectations: relationship type and evidence must be understandable.

Failure modes: hidden matching logic, unsupported merges, or relationships without rationale.

### Signal

Purpose: represent an independent time-based observation.

Required fields, conceptually: signal identifier, signal type, observed time, source reference, description, evidence.

Relationships: links to entities through SignalEntityLink.

Example: Intent spike observed on a target account.

Validation expectations: signal identity, time, source, and meaning must be clear.

Failure modes: duplicated signals, timeless signals, or signals treated as decisions.

### SignalEntityLink

Purpose: attach one signal to every relevant entity without duplicating the signal.

Required fields, conceptually: link identifier, signal reference, entity reference, attachment reason, source evidence.

Relationships: connects Signal to Entity.

Example: Email reply signal links to Contact and Account.

Validation expectations: the signal must exist once, and each link must explain relevance.

Failure modes: copied signals, missing links, or entity views that disagree about the same signal.

### EntityState

Purpose: describe the current interpreted condition of an entity.

Required fields, conceptually: entity reference, state fields, supporting signals, supporting source records, unknowns, computed time, explanation.

Relationships: depends on entities, source records, signals, outcomes, and feedback.

Example: Account has high priority because intent increased and a stakeholder replied.

Validation expectations: every state field must be explainable from visible evidence.

Failure modes: black-box scoring, hidden weighting, invented state, or missing unknowns.

### Decision

Purpose: record a recommendation, priority, classification, or next step.

Required fields, conceptually: decision identifier, entity reference, recommendation, rationale, supporting state, confidence, unknowns, review status.

Relationships: links to state, actions, outcomes, and feedback.

Example: Recommend human follow-up for Account A.

Validation expectations: rationale and evidence must be visible.

Failure modes: recommendation without reason, overconfidence, or implied automation.

### Action

Purpose: record what happened after a decision or recommendation.

Required fields, conceptually: action identifier, decision reference, actor, action type, time, approval boundary, result note.

Relationships: follows a decision and precedes an outcome.

Example: Human reviewed the recommendation and created a follow-up task in a fixture.

Validation expectations: action must be authorized and traceable.

Failure modes: autonomous write actions, silent changes, or action without decision.

### Outcome

Purpose: record what happened after an action.

Required fields, conceptually: outcome identifier, action reference, entity reference, outcome type, observed time, evidence.

Relationships: links actions to feedback and future state.

Example: Meeting booked after human follow-up.

Validation expectations: outcome must connect to the decision or action it evaluates.

Failure modes: mistaking activity for outcome, missing outcome evidence, or detached outcomes.

### Feedback

Purpose: preserve human review, correction, evaluation, or learning.

Required fields, conceptually: feedback identifier, related decision/action/outcome/state, reviewer or source, feedback type, explanation, time.

Relationships: updates future interpretation of signals, state, and decisions.

Example: Reviewer rejects recommendation because the account is already disqualified.

Validation expectations: feedback must connect to the thing it evaluates.

Failure modes: vague feedback, unconnected feedback, or ignored rejected recommendations.

## 9. First Critical Success Path

Given fake GTM records from Salesforce-like, Outreach-like, and 6sense-like sources,
ChaOS resolves source records into canonical Account and Contact entities,
attaches independent signals to those entities,
computes account state,
and produces a deterministic top-10 account recommendation list with traceable reasons.

This is the first useful workflow because it exercises the full Order Graph spine without requiring real integrations, real customer data, dashboards, agents, or deployment architecture.

It tests:

```text
source records -> identity resolution -> signal attachment -> state computation -> ranking -> explanation
```

A future reviewer can inspect each step and decide whether the graph is producing understandable recommendations before any automation is considered.

## 10. Development Strategy

The Order Graph must be built in small PRs.

Each PR must target a specific gate.

Each PR must include audit notes.

No PR may expand scope just because the next step is obvious.

Each PR must state what changed, what did not change, what remains prohibited, and which evidence proves the targeted gate is closer to passing.

If a PR introduces a new artifact type, it must explain why the existing docs are insufficient and why the new artifact removes more complexity than it adds.

## 11. Gated PR Roadmap

### PR 1: Define Order Graph core contracts

Objective: define the plain-language object contracts that make Gate 1 reviewable.

Files likely changed: `docs/order-graph/contracts.md`.

Work allowed: plain-language contracts, object requirements, examples, validation expectations.

Work prohibited: JSON schemas, code, database schemas, API schemas, fixtures.

Gate targeted: Gate 1: Core contracts validate.

Required tests or checks: human review against object responsibility clarity, required fields, relationships, examples, validation expectations, and traceability.

PR audit checklist: answer the standard Order Graph audit questions and confirm no implementation artifacts were added.

Merge criteria: contracts are clear enough for a future maintainer to map GTM and Customer Success examples without guessing.

Stop condition: stop if object responsibilities overlap or if schemas/code are introduced before plain-language contracts pass review.

### PR 2: Add GTM fixture data

Objective: create fake GTM fixture data and expected outputs for identity resolution, signal attachment, and state preparation.

Files likely changed: `examples/order-graph/gtm/source-records.json`, `examples/order-graph/gtm/signals.json`, `examples/order-graph/gtm/expected-entities.json`, `examples/order-graph/gtm/expected-signal-links.json`, `examples/order-graph/gtm/expected-entity-states.json`.

Work allowed: fake data only, human-reviewable expected outputs, ambiguous identity examples.

Work prohibited: real company data, code, external API calls.

Gate targeted: Gate 2: Fixture data resolves into expected entities.

Required tests or checks: manual fixture review for fake data, clean cases, messy cases, ambiguous cases, weak matches, and expected outputs.

PR audit checklist: confirm fixtures preserve source traceability and contain no real customer data.

Merge criteria: fixtures are small enough for humans to inspect and include expected outputs.

Stop condition: stop if fixtures use real data or require private explanation.

### PR 3: Add contract validation checks

Objective: document deterministic validation expectations for contracts and fixtures.

Files likely changed: `docs/order-graph/validation-checks.md`.

Work allowed: validation checklist, deterministic test expectations, fixture review rules.

Work prohibited: LLM validation, database validation, external API calls, hidden business logic.

Gate targeted: Gate 1 and Gate 2 support.

Required tests or checks: reviewer can use the checklist without code.

PR audit checklist: confirm validation remains human-inspectable and does not create hidden logic.

Merge criteria: validation expectations catch missing fields, malformed records, weak matches, and traceability gaps.

Stop condition: stop if validation requires an implementation artifact before the gate allows it.

### PR 4: Add deterministic graph builder skeleton

Objective: add the smallest local-only skeleton for transforming fixture input into graph output, only if prior gates allow code.

Files likely changed: `src/order_graph/__init__.py`, `src/order_graph/build_graph.py`, `src/order_graph/normalize.py`, `src/order_graph/models.py`.

Work allowed: local file input, local file output, simple deterministic functions.

Work prohibited: APIs, UI, database, LLM calls, production integrations.

Gate targeted: Gate 2 and Gate 3 preparation.

Required tests or checks: same fixture input produces same graph output.

PR audit checklist: confirm deterministic behavior, no external calls, no hidden business logic, and no production data path.

Merge criteria: skeleton can read fake fixtures and produce reviewable output without performing real resolution logic beyond the approved scope.

Stop condition: stop if code expands beyond a local deterministic skeleton.

### PR 5: Add identity resolution logic

Objective: implement initial deterministic identity resolution rules against fake fixtures.

Files likely changed: local Order Graph implementation files and fixture expected outputs, only after code is allowed.

Work allowed: same canonical domain -> likely same account; different canonical domain -> different account; same email -> same person; same name but different company -> different person; weak match -> unresolved, do not guess.

Work prohibited: fuzzy matching without explanation, ML matchers, automatic merges, production identity resolution.

Gate targeted: Gate 2: Fixture data resolves into expected entities.

Required tests or checks: false certainty audit, weak match handling, expected resolved and unresolved outputs.

PR audit checklist: confirm every match has visible evidence and unresolved cases are treated as disciplined outputs.

Merge criteria: identity resolution passes fake fixture cases and explains all joins and separations.

Stop condition: stop if weak matches are guessed or merged without evidence.

### PR 6: Add signal attachment logic

Objective: attach independent signals to relevant entities through SignalEntityLink.

Files likely changed: local Order Graph implementation files and expected signal link outputs, only after prior gates allow code.

Work allowed: Signal lives once. Signal attaches to relevant entities through SignalEntityLink. Entity views may display signals without duplicating the signal.

Work prohibited: duplicating signals under accounts or people, tool-specific signal ownership, real-time event processing.

Gate targeted: Gate 3: Signals attach correctly without duplication.

Required tests or checks: one signal object can appear in multiple entity views through links.

PR audit checklist: confirm signals are not duplicated under account/person.

Merge criteria: signal attachment is traceable and entity views agree about the same signal.

Stop condition: stop if any view creates a second copy of the same signal.

### PR 7: Add entity state computation

Objective: compute initial GTM account state from traceable evidence.

Files likely changed: local Order Graph implementation files and expected state outputs, only after prior gates allow code.

Work allowed: initial GTM account state fields `priority_score`, `current_state`, `primary_reason`, `supporting_signals`, `recommended_next_action`, `confidence`, and `unknowns`.

Work prohibited: black-box scoring, hidden weighting, model-only state computation, dashboard-only state.

Gate targeted: Gate 4: Entity state is explainable.

Required tests or checks: every state field traces back to source records, signals, outcomes, or feedback.

PR audit checklist: confirm every state field is explainable.

Merge criteria: state is deterministic for the same input and unknown evidence remains explicit.

Stop condition: stop if state cannot explain itself.

### PR 8: Add top-10 account workflow

Objective: produce the first useful workflow output.

Files likely changed: local workflow output documentation and implementation files, only after prior gates allow code.

Work allowed: Top 10 accounts to focus today and why.

Work prohibited: automatic outreach, CRM writes, task creation in production systems, live prioritization from real data, agent action loops.

Gate targeted: Gate 5: Top-10 recommendation output is deterministic.

Required tests or checks: same input produces same output, each account has a rationale, output is reviewable.

PR audit checklist: confirm the workflow recommends only and does not automate actions.

Merge criteria: top-10 output is deterministic, explainable, and traceable.

Stop condition: stop if recommendations imply automatic action.

### PR 9: Add human review and override model

Objective: define how humans accept, reject, revise, or flag recommendations.

Files likely changed: documentation and local model/output files, only after prior gates allow the artifact type.

Work allowed: Feedback, Override, ReviewDecision, RejectedRecommendationReason concepts.

Work prohibited: cosmetic review only, hidden overrides, automated acceptance, autonomous write actions.

Gate targeted: Gate 6: Human review can override or flag bad logic.

Required tests or checks: rejected recommendations preserve reasons and connect to future feedback.

PR audit checklist: confirm humans can challenge recommendations and feedback is traceable.

Merge criteria: human review is operational and not decorative.

Stop condition: stop if rejected recommendations disappear without feedback.

### PR 10: Evaluate readiness for real integrations

Objective: evaluate whether the system is ready to consider real integrations without adding them.

Files likely changed: `docs/order-graph/integration-readiness.md`.

Work allowed: readiness evaluation for Salesforce exports, Outreach exports, 6sense exports, Snowflake, Glean, API connectors, UI, and agent workflows.

Work prohibited: integrations, production data ingestion, API connectors, deployment work, autonomous actions.

Gate targeted: Gate 7: Real integrations may be considered.

Required tests or checks: Gates 0 through 6 evidence exists and integration risks are documented.

PR audit checklist: confirm a new decision record is required before any real integration work begins.

Merge criteria: readiness review distinguishes consideration from approval.

Stop condition: stop if the PR adds or implies an integration.

## 12. PR Audit Standard

Every Order Graph PR must answer:

1. What gate does this PR target?
2. What changed?
3. What did not change?
4. What remains prohibited?
5. Is every new concept traceable to existing ChaOS docs?
6. Does this remove more complexity than it adds?
7. Is the logic inspectable by a human?
8. Are source records, assumptions, and decisions traceable?
9. Are we recommending before automating?
10. Has the system avoided vendor lock-in?
11. Is this still ChaOS, or has it become a product too early?

Reviewer verdict options:

- Approve
- Approve with non-blocking notes
- Request changes
- Reject as premature implementation

A PR audit must be specific. It must name the gate, evidence, prohibited work, and merge criteria.

## 13. Testing Strategy

Testing maturity must increase with implementation maturity.

Documentation review checks whether the document explains purpose, fit, examples, future considerations, boundaries, and traceability.

Contract review checks object responsibilities, required fields, relationships, examples, validation expectations, and failure modes.

Fixture review checks fake data, expected outputs, clean cases, messy cases, ambiguous cases, weak matches, and source traceability.

Deterministic local validation checks that the same input produces the same output.

Identity resolution tests check resolved entities, unresolved cases, false certainty, and explanation quality.

Signal attachment tests check that signals live once and attach through SignalEntityLink.

State computation tests check that every state field explains itself.

Workflow output tests check deterministic top-10 recommendations and traceable reasons.

Human review tests check acceptance, rejection, revision, override, and feedback capture.

Integration readiness review checks whether Gates 0 through 6 passed before real integration consideration.

Early testing is human-inspectable and fixture-based. It must not require production data, external tools, or hidden model judgment.

## 14. Data and Fixture Strategy

Fixture rules:

- Use fake data only.
- Use no real customer data.
- Include clean cases.
- Include messy cases.
- Include ambiguous cases.
- Include weak matches.
- Include expected outputs.
- Preserve source traceability.
- Keep fixtures small enough for humans to inspect.

Fixtures must prove behavior without creating a production data path. A fixture that requires private explanation is not sufficient. A fixture that uses real company names, customer records, secrets, or production exports must not merge.

## 15. Integration Strategy

Integrations are deferred until Gate 7.

Before integrations, the system must prove:

- Contracts exist.
- Fixtures exist.
- Identity resolution works locally.
- Signals attach correctly.
- Entity state is explainable.
- Top-10 workflow is deterministic.
- Human review exists.

Gate 7 allows integration consideration only. It does not approve integrations. A new decision record must be required before real integration work begins.

Potential integration candidates may include Salesforce exports, Outreach exports, 6sense exports, Snowflake, Glean, API connectors, UI, or agent workflows. They remain candidates until a decision record approves a bounded path.

## 16. Deployment and Operations Deferral

Deployment architecture is intentionally deferred.

No hosting, auth, CI/CD, database deployment, monitoring, scaling, or environment planning should be added until a future decision record approves an application implementation track.

This deferral keeps the Order Graph focused on proving the graph spine before operational concerns shape the architecture.

## 17. Risk Register

| Risk | Description | Impact | Mitigation | Gate where it must be checked |
| --- | --- | --- | --- | --- |
| Premature productization | The track becomes an app, CRM, dashboard, or platform too early. | ChaOS loses portability and becomes product-specific. | Keep work gated, documentation-first, and audit every PR for prohibited scope. | Gate 0 and every PR |
| Vendor lock-in | A vendor-specific source, field, API, or workflow shapes the core model. | The Order Graph becomes less reusable. | Use generic contracts and label vendor-like examples as examples only. | Gate 1, Gate 7 |
| False identity matches | Weak records are merged as if they are certain. | Entity state and recommendations become wrong. | Preserve unresolved states and require visible match evidence. | Gate 2 |
| Signal duplication | The same signal is copied under multiple entities. | Views disagree and truth fragments. | Store signals once and link through SignalEntityLink. | Gate 3 |
| Untraceable recommendations | Recommendations lack visible rationale. | Humans cannot trust or improve the system. | Require evidence links, unknowns, and explanation fields. | Gate 4, Gate 5 |
| LLM overreach | Model reasoning replaces deterministic, inspectable logic. | Outputs become hard to audit. | Prohibit LLM validation and agent logic until gates approve them. | Gate 1 through Gate 6 |
| Real data leakage | Real customer data enters fixtures or tests. | Privacy, trust, and governance risk increase. | Use fake data only and audit fixtures for real records. | Gate 2 and every data PR |
| Scope creep | A PR adds the next obvious thing without approval. | Gates lose meaning. | Require PR audit notes and stop conditions. | Every PR |
| Dashboard-first thinking | UI or reporting shapes the architecture before the graph is proven. | The system optimizes display before understanding. | Defer UI and dashboards until future approval. | Gate 0 through Gate 7 |
| Automation before recommendation | The system acts before recommendation quality is proven. | Bad decisions cause real-world impact. | Require recommendations, human review, and feedback before action automation. | Gate 5, Gate 6, Gate 7 |

## 18. Final Stopping Rule

If a PR cannot explain what gate it targets, what evidence proves the gate passed, and what remains prohibited afterward, the PR must not merge.

## 19. Next Recommended PR

Next recommended PR: Define Order Graph core contracts

The next PR should create docs/order-graph/contracts.md only. It should not add schemas, fixtures, code, integrations, or implementation artifacts.
