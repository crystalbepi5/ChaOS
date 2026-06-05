# Order Graph Validation Checks

## Why This File Exists

This file defines the review checks that must be applied before the Order Graph moves from documentation into executable validation.

The Order Graph now has core contracts and fake GTM fixture data. Those artifacts need a specific review path so future work can prove contract behavior without inventing hidden logic, premature schemas, or implementation shortcuts.

This file is not a validator. It is a human-readable validation contract for reviewers and future agents.

## Purpose

The purpose of this file is to define:

- What must be checked in the Order Graph core contracts.
- What must be checked in the GTM fixture set.
- What counts as a valid resolved entity, unresolved record, signal link, and entity state.
- What must remain out of scope until a later gate approves implementation work.

The goal is specificity, not complexity.

## How This Fits Into ChaOS

This file supports the documentation-first build path described in:

- `docs/order-graph/overview.md`
- `docs/order-graph/contracts.md`
- `docs/order-graph/build-roadmap.md`
- `docs/order-graph/testing-gates.md`
- `docs/order-graph/technical-requirements-and-development-roadmap.md`
- `examples/order-graph/gtm/README.md`

It supports Gate 1 and Gate 2 by making review expectations explicit before any code, schemas, databases, integrations, UI, autonomous agents, or deployment work is approved.

## Scope Boundary

These checks apply to documentation artifacts and fake fixture data only.

This document must not be treated as approval for:

- Local scripts.
- JSON Schema files.
- Database schemas.
- API contracts.
- TypeScript, Python, Pydantic, or ORM models.
- Real integrations.
- Real customer data.
- LLM-based validation.
- External API calls.
- UI work.
- Autonomous agents.
- Deployment work.

Any future implementation artifact must require the appropriate gate approval and a traceable decision record if it changes architecture, contracts, workflows, evaluation criteria, or agent behavior.

## Validation Philosophy

Order Graph validation must be deterministic, inspectable, and explainable by humans.

A reviewer must be able to answer:

- Which records resolve into canonical entities?
- Which records remain unresolved?
- Why does each unresolved case remain unresolved?
- Which signals link to which entities?
- Which signals support entity state?
- Which signals must not drive high-priority state?
- Which unknowns must be preserved?
- Which assumptions must remain visible?

Validation must prefer explicit evidence over inferred confidence. When evidence is weak, missing, stale, or ambiguous, the graph must preserve uncertainty instead of guessing.

## Gate Coverage

### Gate 1: Core Contracts Validate

Gate 1 checks whether the plain-language contracts are complete enough to guide future schema, fixture, and implementation work.

A Gate 1 review must confirm that each core object contract defines:

- Purpose.
- Required fields or field concepts.
- Relationships to other objects.
- Examples.
- Validation expectations.
- Failure modes.
- Unknowns that must be preserved.

Passing Gate 1 does not approve code, real integrations, databases, UI work, autonomous agents, or deployment work. It only approves moving from conceptual documentation into schema and fixture preparation.

### Gate 2: Fixture Data Resolves Into Expected Entities

Gate 2 checks whether fake fixture data can demonstrate expected graph behavior.

A Gate 2 review must confirm that fixtures include:

- Source records.
- Expected canonical entities.
- Expected unresolved records.
- Expected signal links.
- Expected entity states.
- Positive examples.
- Known-bad or unresolved examples.
- Explanations for every unresolved case.

Passing Gate 2 does not approve production data handling, real integrations, databases, UI work, autonomous agents, or deployment work.

## Contract Validation Checks

The contract document at `docs/order-graph/contracts.md` must define these objects clearly enough for a reviewer to inspect fixture behavior without additional context:

- Domain.
- Entity.
- SourceRecord.
- EntityRelationship.
- Signal.
- SignalEntityLink.
- EntityState.
- Decision.
- Action.
- Outcome.
- Feedback.

Each object contract must be vendor-neutral. Vendor-like examples may appear only as fake illustrative source systems. The contract must not require Salesforce, Outreach, 6sense, HubSpot, Segment, Snowflake, or any other specific platform.

Each object contract must state what evidence is strong, what evidence is weak, and when uncertainty must be preserved.

## Fixture Validation Checks

The GTM fixture set under `examples/order-graph/gtm/` must remain small enough for human review.

The fixture set must include these reviewable files:

- `source-records.json`
- `signals.json`
- `expected-entities.json`
- `expected-signal-links.json`
- `expected-entity-states.json`
- `README.md`

The fixture set must use fake organizations, fake people, fake domains, and fake source identifiers. It must not include real customer data, real prospect data, real user data, private credentials, production identifiers, or private URLs.

Each fixture file must make expected behavior inspectable without requiring a script.

## Source Record Checks

Each source record must include enough information for a reviewer to understand where the record came from and how it may resolve.

A source record must include:

- A stable fixture identifier.
- A fake source system.
- A source object type.
- A fake source-native identifier.
- Raw source values.
- Normalized values when normalization matters.
- Observed or ingested timing when timing affects interpretation.
- A source reference that remains fake and inspectable.
- A status or note when the record is incomplete, ambiguous, or unresolved.

A source record must preserve relevant unknowns. Missing domain, missing email, weak name match, stale observation, or ambiguous account evidence must remain visible in the fixture data.

## Expected Entity Checks

Expected entities must make canonical identity decisions visible.

Each expected entity must include:

- A stable expected entity identifier.
- Entity type.
- Canonical display name.
- Canonical identity keys when available.
- Source records that support the entity.
- Resolution rationale.
- Confidence or evidence strength when the fixture uses it.
- Unknowns that remain attached to the entity.

Expected entities must not hide unresolved source records by forcing them into weak canonical entities.

## Identity Resolution Checks

The GTM fixture set must demonstrate these identity behaviors:

- A clean account match where Salesforce-like Account, Outreach-like Account or Prospect, and 6sense-like Company records resolve to the same canonical Account by domain.
- A clean contact match where the same email resolves to the same canonical Contact across source records.
- A messy but resolvable account match where company name variations resolve because normalized domain is strong evidence.
- An ambiguous account case where similar names with different domains remain separate or unresolved.
- A weak person match where the same name at different companies or domains does not merge.
- A missing-domain weak account case where similar name evidence remains unresolved unless another strong key exists.

Resolution must rely on stated evidence. The fixture set must not imply that name similarity alone is enough to merge accounts or people.

## Signal Checks

Each signal must include enough information for a reviewer to determine what happened, when it happened, where it came from, and whether it can support entity state.

A signal must include:

- A stable signal identifier.
- Signal type.
- Fake source system.
- Occurred time.
- Observed time when different from occurred time.
- Source reference.
- Normalized summary.
- Confidence, strength, or weight when relevant.
- Staleness or priority notes when relevant.

The fixture set must include at least one signal that links to multiple entities.

The fixture set must include at least one stale, weak, or low-confidence signal that exists in the graph but must not drive high-priority state.

## Signal Entity Link Checks

Signal links must explain why a signal attaches to an entity.

Each expected signal link must include:

- Signal identifier.
- Target entity identifier.
- Link role.
- Evidence for the link.
- Confidence or evidence strength when relevant.
- Any preserved unknowns.

A signal may link to multiple entities when roles are explicit. For example, an email reply may link to a Contact as actor, an Account as parent account, and an Outreach-like sequence as source workflow.

A signal must not be duplicated to create multiple meanings. One signal record must keep one event identity, with multiple explicit links when needed.

## Entity State Checks

Entity state expectations must show how signals and source records support current interpretation.

Each expected entity state must include:

- Entity identifier when the state attaches to a resolved entity.
- Unresolved fixture reference when the state attaches to unresolved evidence.
- State label.
- Computed or assessed time.
- Supporting source records.
- Supporting signals.
- Primary reason.
- Confidence or evidence strength when relevant.
- Unknowns that affect interpretation.
- Recommended next action when the fixture includes one.

Entity state must not hide its reasoning. If priority, risk, health, or next action appears, the supporting evidence must be traceable.

Stale, weak, or low-confidence signals may be present in state context, but they must not be the sole basis for high-priority state.

## Unknowns And Unresolved Case Checks

Unknowns are part of the graph contract. They must not be erased to make the fixture look cleaner.

A record must remain unresolved when:

- It has a similar name but no strong identity key.
- It has a similar person name but a different company or domain.
- It has a missing domain and no alternative strong key.
- It has conflicting source evidence.
- Its evidence is stale and no fresh corroborating signal exists.

Each unresolved case must include a visible reason. The reason must explain what evidence is missing or why available evidence is insufficient.

## Deterministic Test Expectations

Future executable validation must be able to use the fixture set deterministically.

The same fixture inputs must produce the same expected outputs unless a later decision record changes the contracts or fixture expectations.

Validation must not depend on:

- LLM judgment.
- Hidden prompts.
- External API enrichment.
- Production systems.
- Randomness.
- Current date assumptions unless the fixture explicitly fixes the date context.

For now, these expectations remain documentation and review criteria only. They must not be converted into code until the appropriate gate approves implementation work.

## Fixture Review Procedure

A reviewer must be able to perform this review manually:

1. Read `docs/order-graph/contracts.md`.
2. Read `examples/order-graph/gtm/README.md`.
3. Inspect the source records.
4. Inspect the signals.
5. Compare expected entities against source records.
6. Compare unresolved records against stated unresolved reasons.
7. Compare expected signal links against signal roles and entity evidence.
8. Compare expected entity states against supporting records and signals.
9. Confirm stale or low-confidence signals do not drive high-priority state.
10. Confirm unknowns are preserved.

A reviewer must request changes when expected outputs cannot be traced back to source evidence.

## Pass And Fail Outcomes

A review may result in one of four outcomes.

### Pass

The contracts and fixtures are specific, inspectable, fake, deterministic, and traceable.

### Pass With Non-Blocking Notes

The contracts and fixtures satisfy the gate, but the reviewer identifies clarifications that may be handled in a later documentation PR.

### Request Changes

The contracts or fixtures contain unclear evidence, missing expected outputs, missing unresolved reasons, hidden assumptions, weak traceability, or unclear state support.

### Reject As Premature Implementation

The change introduces code, schemas, validators, integrations, database structures, UI, autonomous agents, deployment work, or external validation before the relevant gate approves it.

## Examples Of Use

A reviewer may use these checks to confirm that:

- A clean account match resolves by canonical domain.
- A clean contact match resolves by email.
- Name variations such as `ACME Corporation`, `Acme Corp.`, and `https://www.acme.com` resolve because normalized domain is strong evidence.
- Similar account names with different domains remain separate or unresolved.
- Same-name people at different domains do not merge.
- Missing-domain account records remain unresolved unless another strong key exists.
- An email reply signal links to Contact, Account, and source workflow roles without duplicating the signal.
- A stale or low-confidence signal exists in the graph but does not drive high-priority state.

## Future Considerations

These checks may later become deterministic local validation after the relevant gate approves implementation work.

Future validation may include:

- JSON Schema validation.
- Local fixture validation scripts.
- Deterministic identity-resolution checks.
- Contract-to-fixture coverage checks.
- Review reports that identify unresolved records and preserved unknowns.

Those future artifacts must remain local, inspectable, deterministic, and subordinate to the plain-language contracts.

## Next Recommended PR

The next roadmap PR is `Add deterministic graph builder skeleton`.

Before that PR begins, reviewers must confirm that Gate 2 fixture expectations are accepted. The skeleton must remain local-only and deterministic. It must not include real integrations, databases, UI, autonomous agents, deployment work, LLM validation, external API calls, or hidden business logic.
