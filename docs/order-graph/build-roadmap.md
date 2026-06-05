# Order Graph Build Roadmap

This document defines the controlled build sequence for the Order Graph reference implementation track.

## Purpose

The roadmap exists to keep Order Graph work methodical, inspectable, and bounded. It names what each phase may create, what remains prohibited, the critical test point, and the stop condition before the next phase may begin.

The goal is not to build a product quickly. The goal is to prove the graph spine before ChaOS considers real integrations, databases, frontends, autonomous agents, or vendor-specific implementation choices.

## How This Fits Into ChaOS

The Order Graph applies the ChaOS core model:

```text
Entity -> Signal -> Decision -> Outcome -> Feedback
```

It extends that model into a reference implementation track:

```text
Domain -> Entity -> Source Record -> Relationship -> Signal -> State -> Decision -> Action -> Outcome -> Feedback
```

This roadmap keeps that track subordinate to ChaOS laws. Each phase must remove more complexity than it adds, preserve human inspectability, and stop before implementation outruns understanding.

## Phase 0: Architecture Boundary

### Purpose

Establish the boundary for the Order Graph reference implementation track.

### What Gets Created

- Decision record for the Order Graph reference implementation track
- Overview document
- Build roadmap
- Testing gates
- Explicit list of prohibited work

### What Must Not Be Added Yet

- Source code
- `src/` directory
- Production integrations
- Real customer data ingestion
- Databases
- Frontend apps
- API connectors
- Autonomous agents
- Vendor-specific implementation choices

### Critical Test Point

A future maintainer can explain what the Order Graph is, what it is not, and where the implementation boundary sits.

### Stop Condition

Stop if the boundary is unclear, if the work starts implying a product, or if documentation cannot explain why the track exists.

## Phase 1: Order Graph Contract

### Purpose

Define the canonical objects and relationships that future fixture-only work must follow.

### What Gets Created

Canonical object definitions for:

- Domain
- Entity
- SourceRecord
- EntityRelationship
- Signal
- EntityState
- Decision
- Action
- Outcome
- Feedback

The contract may also define required fields, allowed relationship types, and traceability rules in plain language.

### What Must Not Be Added Yet

- Application code
- Database schema
- ORM models
- API contracts
- Vendor-specific field mappings
- Real tool integrations
- Automated decision logic

### Critical Test Point

A reviewer can map a simple GTM example into the canonical objects without guessing which object owns which responsibility.

### Stop Condition

Stop if the contract cannot distinguish entities from source records, signals from state, decisions from actions, or outcomes from feedback.

## Phase 2: Fixture-Only Proof

### Purpose

Prove the contract using fake/sample fixture data only.

### What Gets Created

- Small fixture examples
- Sample GTM source records
- Expected entity outputs
- Expected relationship outputs
- Expected signal attachments
- Expected state outputs

Fixtures must use fake names, fake companies, fake domains, and fake events.

### What Must Not Be Added Yet

- Real customer data
- Imported production records
- Secrets
- Vendor credentials
- External API calls
- Production connectors
- User interface

### Critical Test Point

Fixture data resolves into expected entities, relationships, signals, and states in a way a human can inspect.

### Stop Condition

Stop if fixture examples require private explanation, hide assumptions, or cannot prove traceability from source records to graph objects.

## Phase 3: Tiny Local Engine

### Purpose

Describe and later build a small deterministic local transformation engine that converts fixtures into graph outputs.

### What Gets Created

- A narrow transformation plan
- Deterministic transformation rules
- Local-only execution boundary
- Expected input and output examples
- Reviewable transformation logs when implementation begins

### What Must Not Be Added Yet

- Production app
- Hosted service
- Database
- Frontend
- Background jobs
- External integrations
- Model-driven transformations
- Autonomous actions

### Critical Test Point

Given the same fixture input, the local engine produces the same graph output every time.

### Stop Condition

Stop if transformation logic becomes opaque, non-deterministic, model-dependent, or difficult for a human to inspect.

## Phase 4: Identity Resolution Tests

### Purpose

Test whether source records resolve into durable entities without unsafe guessing.

### What Gets Created

- Identity resolution test cases
- Expected resolved and unresolved outputs
- Explanation of match strength
- Explicit unresolved state for weak matches

Required identity tests:

- Same domain means likely same account.
- Different domain means different account.
- Same email means same person.
- Same name but different company means different person.
- Weak match must be marked unresolved instead of guessed.

### What Must Not Be Added Yet

- Machine learning matchers
- Fuzzy matching that cannot explain itself
- Automatic merges without review
- Real production identity resolution
- Vendor-specific matching rules as core requirements

### Critical Test Point

Each identity resolution result is explainable from visible source record evidence.

### Stop Condition

Stop if weak matches are guessed, if different entities are merged without evidence, or if unresolved cases are treated as failures instead of disciplined outputs.

## Phase 5: Signal Attachment Tests

### Purpose

Test that signals live once and attach to all relevant entities through relationships.

### What Gets Created

- Signal fixture examples
- Signal attachment expected outputs
- Relationship examples linking signals to accounts, people, opportunities, workflows, or other entities
- Duplication checks

### What Must Not Be Added Yet

- Physically nested signals under only one entity type
- Duplicated signal records for each view
- Tool-specific signal ownership as a core rule
- Real-time event processing
- Production data ingestion

### Critical Test Point

A signal appears once in storage and can be viewed from every relevant entity through relationships.

### Stop Condition

Stop if the same signal is duplicated, if entity views disagree about the signal, or if the attachment logic cannot be traced.

## Phase 6: Entity State Computation

### Purpose

Compute entity state from source records, relationships, signals, outcomes, and feedback with explainable reasons.

### What Gets Created

- State computation examples
- State fields such as priority score, buying stage, active stakeholders, last meaningful touch, and recommended next action
- Explanation records showing why each state value exists
- Tests for state changes over time

### What Must Not Be Added Yet

- Black-box scoring
- Model-only state computation
- Hidden weighting
- Production recommendations
- Autonomous actions
- Dashboard-only state with no traceability

### Critical Test Point

Every computed state value can be explained by visible inputs and deterministic rules.

### Stop Condition

Stop if state computation cannot explain itself, if scoring hides assumptions, or if state becomes a recommendation without review.

## Phase 7: First Useful Workflow

### Purpose

Define and test the first useful workflow supported by the Order Graph.

The first useful workflow is:

```text
Top 10 accounts to focus today and why.
```

### What Gets Created

- Workflow definition
- Fixture-based top-10 recommendation output
- Explanation for each recommended account
- Human review path
- Feedback capture for accepted, rejected, or revised recommendations

### What Must Not Be Added Yet

- Automatic outreach
- CRM writes
- Task creation in production systems
- Live prioritization from real data
- AI agent action loops
- Unreviewed ranking logic

### Critical Test Point

The top-10 output is deterministic, explainable, and reviewable by a human.

### Stop Condition

Stop if recommendations cannot explain why each account appears, if output changes without input changes, or if the workflow implies automatic action.

## Phase 8: Real Integrations Later

### Purpose

Explicitly defer real integrations until the graph spine is proven.

### What Gets Created

- Integration readiness criteria
- Candidate integration list only after gates pass
- Decision record draft for any proposed production integration
- Risk review for vendor lock-in and data governance

### What Must Not Be Added Yet

- Production integrations before Gate 7
- Real customer data ingestion before approval
- Vendor-specific architecture as a core requirement
- Database infrastructure without a decision record
- Frontend app without a decision record
- Autonomous actions without proven recommendation quality

### Critical Test Point

The Order Graph works with fixtures, deterministic local transformations, identity resolution tests, signal attachment tests, state computation tests, and the top-10 workflow before real integrations are considered.

### Stop Condition

Stop if integration pressure appears before the graph spine is proven or if a vendor choice starts shaping core architecture.

## Examples Of Use

A future maintainer wants to begin implementation. This roadmap tells them to start with contracts and fake fixture data, not production connectors.

A reviewer sees a proposal to add a CRM integration. This roadmap tells them to check whether Gate 7 has passed and whether a decision record exists.

A developer wants to compute account priority. This roadmap tells them to first prove identity resolution and signal attachment before computing state.

## Future Considerations

Future versions may add more detailed contracts, fixture examples, local transformation plans, or schema proposals.

Those additions must follow this roadmap and must stop at the relevant testing gate before implementation expands.
