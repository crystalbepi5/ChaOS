# Order Graph Testing Gates

This document defines the gates that must be passed before Order Graph implementation work may progress.

## Purpose

The gates exist to prevent the Order Graph reference implementation track from becoming a chaotic implementation.

Each gate requires visible evidence, pass criteria, fail criteria, allowed next work, and work that remains prohibited. A gate is not passed because the next step feels obvious. A gate passes only when the required evidence exists and a human reviewer can inspect it.

## How This Fits Into ChaOS

ChaOS requires systems to be understandable by humans first. The Order Graph testing gates make that requirement operational.

The gates enforce the Order Graph sequence:

```text
Architecture boundary -> Core contracts -> Fixture proof -> Identity resolution -> Signal attachment -> Explainable state -> Deterministic recommendation -> Human override -> Real integration consideration
```

The gates also preserve the core ChaOS laws:

- Do not optimize chaos into more chaos.
- Every component must remove more complexity than it adds.
- Context is a dependency. Minimize it.
- Systems must be understandable by humans first.
- Recommend before automating.
- Prefer inspectable systems over intelligent systems.
- Every decision must be traceable.

## Gate 0: Architecture Boundary Approved

### Purpose

Confirm that the Order Graph reference implementation track has an approved boundary before implementation begins.

### Required Evidence

- Accepted decision record for the Order Graph reference implementation track
- Complete Order Graph overview
- Build roadmap
- Testing gates
- Explicit list of prohibited work

### Pass Criteria

- The boundary explains what the Order Graph is and is not.
- The boundary prohibits production integrations, real customer data ingestion, databases, frontends, autonomous actions, and vendor lock-in at this stage.
- A future maintainer can explain why implementation must start with documentation, contracts, fixtures, and deterministic local tests.

### Fail Criteria

- The track implies a production app.
- The track depends on a vendor or production tool.
- The boundary is unclear or scattered across private context.
- A reviewer cannot identify what work remains prohibited.

### Work Allowed After Pass

- Define canonical Order Graph objects.
- Draft contracts in documentation.
- Prepare schema proposals when justified.

### Work Still Prohibited

- Source code
- `src/` directory
- Production integrations
- Real customer data
- Databases
- Frontend apps
- Autonomous agents
- Vendor-specific implementation choices

## Gate 1: Core Schemas Validate

### Purpose

Confirm that the canonical Order Graph objects can be represented by inspectable contracts.

### Required Evidence

- Canonical object definitions for Domain, Entity, SourceRecord, EntityRelationship, Signal, EntityState, Decision, Action, Outcome, and Feedback
- Schema or contract validation method when schemas are introduced
- Example objects that pass validation
- Example invalid objects that fail validation

### Pass Criteria

- Required fields are clear.
- Object responsibilities do not overlap confusingly.
- Validation catches missing or malformed required fields.
- Contracts preserve source references and traceability.

### Fail Criteria

- Entity and SourceRecord are confused.
- Signal and EntityState are confused.
- Decision and Action are confused.
- Contracts depend on vendor-specific fields as core requirements.
- Validation cannot be inspected by a human.

### Work Allowed After Pass

- Create fixture-only source records.
- Create expected fixture outputs.
- Test resolution against fake/sample data.

### Work Still Prohibited

- Production app code
- Real integrations
- Production data ingestion
- Database migrations
- Frontend interfaces
- Autonomous actions

## Gate 2: Fixture Data Resolves Into Expected Entities

### Purpose

Confirm that fake/sample source records resolve into expected durable entities.

### Required Evidence

- Fixture source records
- Expected resolved entities
- Expected unresolved cases
- Identity resolution rules
- Test results showing actual output matches expected output

### Pass Criteria

- Same domain resolves to likely same account when supporting evidence is strong.
- Different domain resolves to different account.
- Same email resolves to same person.
- Same name but different company resolves to different person.
- Weak match is marked unresolved instead of guessed.

### Fail Criteria

- Weak matches are guessed.
- Different people or accounts are merged without evidence.
- Unresolved cases are treated as errors.
- Resolution logic cannot explain why records were joined or separated.

### Work Allowed After Pass

- Add signal fixture examples.
- Test signal attachment to resolved entities.

### Work Still Prohibited

- Real identity resolution
- Production matching
- Machine learning matchers
- Fuzzy matching without explanation
- Automatic merges
- Production integrations

## Gate 3: Signals Attach Correctly Without Duplication

### Purpose

Confirm that signals live once and attach to every relevant entity through relationships.

### Required Evidence

- Signal fixtures
- Expected signal objects
- Expected signal-to-entity relationships
- Duplication checks
- Test results showing one stored signal can appear in multiple entity views

### Pass Criteria

- Each signal has one source object.
- Each signal can attach to multiple relevant entities.
- Account, person, opportunity, workflow, or other views can show the signal without duplicating it.
- Signal attachment is traceable to source records and relationships.

### Fail Criteria

- The same signal is copied into multiple storage locations.
- Entity views disagree about the same signal.
- Signals are physically nested under only one entity type.
- Attachment logic is hidden or tool-specific.

### Work Allowed After Pass

- Compute entity state from source records, relationships, signals, outcomes, and feedback.

### Work Still Prohibited

- Real-time signal ingestion
- Production event processing
- Tool-specific signal ownership as a core rule
- Dashboard views
- Autonomous decisions

## Gate 4: Entity State Is Explainable

### Purpose

Confirm that computed entity state can explain itself.

### Required Evidence

- State computation examples
- Input records, relationships, signals, outcomes, and feedback used for each state
- Explanation for each computed value
- Test results showing state changes when inputs change

### Pass Criteria

- Each state value traces back to visible evidence.
- Priority score, buying stage, active stakeholders, last meaningful touch, and recommended next action can be explained.
- State computation is deterministic for the same input.
- Unknown or insufficient evidence produces partial or unresolved state instead of invention.

### Fail Criteria

- State depends on hidden weighting.
- State is produced by black-box logic.
- State cannot explain which inputs affected it.
- Missing evidence is filled with assumptions.

### Work Allowed After Pass

- Define the first useful workflow.
- Produce fixture-based recommendations from explainable state.

### Work Still Prohibited

- Production recommendations
- Autonomous actions
- Black-box scoring
- Model-only state computation
- Dashboards that hide reasoning

## Gate 5: Top-10 Recommendation Output Is Deterministic

### Purpose

Confirm that the first useful workflow produces deterministic, explainable recommendations.

The first useful workflow is:

```text
Top 10 accounts to focus today and why.
```

### Required Evidence

- Fixture inputs
- Expected top-10 output
- Rationale for each account
- Determinism test results
- Evidence links from each recommendation to source records, signals, state, outcomes, or feedback

### Pass Criteria

- The same input produces the same top-10 output.
- Each account recommendation explains why it appears.
- Recommendations are reviewable by a human.
- Recommendations remain recommendations, not actions.

### Fail Criteria

- Output changes without input changes.
- Accounts appear without rationale.
- Recommendations depend on hidden logic.
- The workflow implies automatic outreach, CRM writes, or task creation.

### Work Allowed After Pass

- Add human review and override flows for recommendations.
- Capture feedback on accepted, rejected, or revised recommendations.

### Work Still Prohibited

- Automatic outreach
- Production CRM writes
- Live prioritization from real data
- Agent action loops
- Unreviewed ranking logic

## Gate 6: Human Review Can Override Or Flag Bad Logic

### Purpose

Confirm that humans can reject, revise, or flag recommendations and that feedback is captured.

### Required Evidence

- Human review workflow
- Override examples
- Rejection examples
- Feedback records tied to recommendation outputs
- Tests showing feedback can be preserved for future evaluation

### Pass Criteria

- A human can accept, reject, revise, or flag a recommendation.
- The reason for override or rejection is recorded.
- Feedback connects to the decision, action, outcome, or state it affects.
- Bad logic becomes visible evidence for improvement.

### Fail Criteria

- Human review is cosmetic.
- Overrides are not recorded.
- Rejected recommendations disappear without feedback.
- The system treats confidence as permission.

### Work Allowed After Pass

- Evaluate whether real integrations may be considered.
- Draft integration readiness criteria.
- Prepare a decision record for any proposed integration.

### Work Still Prohibited

- Production integrations without a decision record
- Real customer data ingestion without approval
- Autonomous write actions
- Vendor-specific architecture as a core requirement

## Gate 7: Real Integrations May Be Considered

### Purpose

Confirm that the graph spine is proven enough to consider production integrations.

This gate does not approve integrations. It only allows integration consideration.

### Required Evidence

- Gates 0 through 6 passed
- Fixture-only graph spine demonstrated
- Deterministic local transformation results
- Identity resolution evidence
- Signal attachment evidence
- Explainable state computation
- Deterministic top-10 recommendation output
- Human review and override evidence
- Draft decision record for any proposed real integration

### Pass Criteria

- The graph works with fake/sample data.
- The system remains inspectable and traceable.
- Human review remains required.
- Integration risks are documented.
- Vendor lock-in risk is evaluated.

### Fail Criteria

- Any prior gate is incomplete.
- The proposed integration changes core architecture without approval.
- Real data would enter before governance is ready.
- A vendor starts defining the Order Graph model.

### Work Allowed After Pass

- Consider a real integration through a separate decision record.
- Define limited integration scope.
- Define data governance requirements.
- Define rollback and review requirements.

### Work Still Prohibited

- Production integration without approved decision record
- Broad data ingestion
- Autonomous actions
- Unbounded vendor-specific implementation
- Treating Gate 7 as deployment approval

## Standing Review Checklist

Every Order Graph review must ask:

1. Does this remove more complexity than it adds?
2. Is the logic inspectable by a human?
3. Are source records, assumptions, and decisions traceable?
4. Are we recommending before automating?
5. Has the system avoided vendor lock-in?
6. Is this still ChaOS, or has it become a product too early?

## Examples Of Use

A reviewer sees a proposal to add a Salesforce connector. The reviewer checks Gate 7. If Gates 0 through 6 have not passed, the connector remains prohibited.

A developer proposes a scoring model. The reviewer checks Gate 4. If the score cannot explain itself from visible inputs, the work stops.

A workflow produces a top-10 account list. The reviewer checks Gate 5. If the output changes without input changes, the gate fails.

## Future Considerations

Future versions may add test fixture examples and validation commands for each gate.

Those additions must remain documentation-first until a decision record approves implementation work at the relevant gate.
