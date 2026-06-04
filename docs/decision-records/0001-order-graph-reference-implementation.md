# Decision Record 0001: Order Graph Reference Implementation

## Status

Accepted for controlled exploration.

## Context

ChaOS began as a documentation-first architecture repository. Its purpose is to make reusable system design portable across future projects without forcing a specific vendor, programming language, database, application framework, or deployment model.

The Order Graph is the first candidate reference implementation of ChaOS. It applies the core ChaOS model to a concrete system that turns fragmented tool data into shared organizational understanding.

This decision record exists because adding implementation work creates architectural risk. If implementation is added without boundaries, ChaOS may drift from a reusable architecture constitution into a single product, app, or tool-specific codebase.

## Decision

ChaOS may include an Order Graph reference implementation track.

The reference implementation must remain subordinate to ChaOS Core. It must demonstrate the architecture without redefining ChaOS as a product, startup, CRM, workflow engine, AI agent platform, or coding framework.

The implementation track must begin with documentation, schemas, fixtures, and deterministic local transformations before any production integrations, user interfaces, databases, or autonomous agents are added.

## Rationale

The Order Graph is a concrete expression of the existing ChaOS model:

```text
Entity -> Signal -> Decision -> Outcome -> Feedback
```

It extends the model into a practical operating layer:

```text
Domain -> Entity -> Source Record -> Relationship -> Signal -> State -> Decision -> Action -> Outcome -> Feedback
```

This lets ChaOS prove that its architecture can be applied to real tool data while preserving the original principle that humans and agents must understand the system before implementation choices are made.

## Scope

The initial Order Graph track may define:

- The Order Graph concept
- Canonical object definitions
- JSON schemas for portable contracts
- Example fixtures
- Deterministic local transformation logic
- Testing gates
- Human review points
- Decision records for material changes

The initial Order Graph track must not add:

- Production integrations
- Database infrastructure
- Authentication
- A hosted application
- Autonomous write actions
- Vendor-specific assumptions as core requirements
- Hidden or untraceable decision logic

## Alternatives Considered

### Continue documentation only

This preserves the original repository boundary but does not test whether ChaOS patterns can produce useful, inspectable systems.

### Build a full application immediately

This would move too quickly and violate the repository's architecture-first purpose. It would likely create tool-specific complexity before the core model has been proven.

### Keep Order Graph in a separate repository

This may become appropriate later. For now, keeping the reference implementation inside ChaOS helps ensure that implementation remains governed by ChaOS laws, standards, and review gates.

## Expected Consequences

The repository will gain an implementation track, but that track must be visibly separated from ChaOS Core.

Future maintainers must be able to tell the difference between:

- ChaOS Core patterns that every project may inherit
- Order Graph reference implementation choices that demonstrate one possible application

If an implementation pattern proves generally reusable, it may be proposed back into ChaOS Core through a future decision record.

## Feedback Plan

The Order Graph track must stop at predefined testing gates.

At each gate, the reviewer must ask:

1. Does this remove more complexity than it adds?
2. Is the logic inspectable by a human?
3. Are source records, assumptions, and decisions traceable?
4. Are we recommending before automating?
5. Has the system avoided vendor lock-in?
6. Is this still ChaOS, or has it become a product too early?

## Approval Boundary

This decision approves starting the Order Graph reference implementation track.

It does not approve production deployment, real customer data ingestion, autonomous actions, or vendor-specific integrations.
