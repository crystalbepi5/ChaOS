# Decision 0005: Candidate Constitutional Concepts

## Status

Accepted

## Purpose

Establish a governance lifecycle for architectural concepts discovered through inheritance reviews.

## Context

Three inheritance reviews have been completed:

- Synapse
- Lead Prioritization Agent
- MedSpa CRM

Repeated patterns have emerged across multiple projects.

Examples:

- State / Lifecycle
- Feedback Maturity
- Actor Roles
- Learning Over Time
- Signal Evaluation
- Recommendation Explanation

The repeated appearance of these concepts creates architectural pressure.

However, repeated appearance alone is not sufficient to add concepts to the ChaOS constitution.

## Decision

ChaOS establishes the following concept maturity lifecycle:

Observed

-> Candidate Concept

-> Validated Concept

-> Constitutional Concept

### Definitions

#### Observed

Appears in a single project review.

#### Candidate Concept

Appears across multiple inheritance reviews and shows signs of reusability.

#### Validated Concept

Has accumulated evidence across multiple domains and demonstrates reusable architectural value.

#### Constitutional Concept

Has been formally approved through governance and incorporated into ChaOS.

## Current Candidate Concepts

The following concepts are recognized as candidates:

- State / Lifecycle
- Feedback Maturity
- Actor Roles
- Learning Over Time
- Signal Evaluation
- Recommendation Explanation

These concepts are not approved architecture.

They are recognized as recurring architectural pressure.

## Rules

Candidate Concepts:

- May be studied.
- May be tracked.
- May appear in future inheritance reviews.

Candidate Concepts may not:

- Become architecture automatically.
- Override existing governance.
- Create new schemas.
- Create new workflows.
- Create new agents.
- Create implementation requirements.

## Promotion Criteria

A Candidate Concept should only be considered for validation when:

- It appears across multiple domains.
- It repeatedly solves the same architectural pressure.
- Existing ChaOS concepts cannot adequately address the concern.
- Human governance determines the concept is reusable.

## Rejection Criteria

A Candidate Concept should be removed when:

- It proves project-specific.
- It stops appearing in future reviews.
- Existing ChaOS concepts already address the concern.
- The concept introduces unnecessary complexity.

## Rationale

Introducing a candidate stage prevents premature architecture growth. It allows ChaOS to notice repeated pressure without immediately expanding the constitution.

Evidence should drive constitutional evolution because ChaOS is meant to eliminate the cost of starting over, not create a larger framework by enthusiasm. A concept should become constitutional only when it has proven reusable value across projects and existing ChaOS concepts are insufficient.

The maturity lifecycle protects the distinction between observation and adoption. It lets ChaOS learn without treating every repeated idea as an architectural mandate.

## Alternatives Considered

### Immediate Constitutional Adoption

Rejected because repeated appearance is not enough evidence. Immediate adoption would risk adding concepts before their boundaries, purpose, and reusable value are clear.

### Ignoring Repeated Patterns

Rejected because repeated inheritance pressure is useful evidence. Ignoring it would prevent ChaOS from learning from real project reviews.

### Creating Architecture Directly From Inheritance Reviews

Rejected because inheritance reviews are evidence-gathering artifacts, not governance approvals. Architecture should be incorporated only through accepted decisions.

## Consequences

Expected benefits:

- Reduced architecture creep
- Better governance discipline
- Evidence-driven evolution
- Clear separation between observation and architecture
- A safer path for future constitutional growth

This decision does not approve new architecture, schemas, workflows, agents, implementation requirements, databases, frontends, infrastructure, orchestration, or production systems.

## Feedback Plan

Future inheritance reviews should:

- Track Candidate Concepts
- Measure recurrence
- Assess confidence
- Identify new candidates
- Recommend promotions or removals

Future reviews should not automatically create constitutional concepts.

## Conclusion

ChaOS evolves through evidence, not enthusiasm.

Repeated pressure creates candidates.

Governance determines adoption.

