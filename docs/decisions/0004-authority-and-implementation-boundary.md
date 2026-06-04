# Decision 0004: Authority And Implementation Boundary

## Status

Accepted

## Context

The second Meta-Agent review identified several governance risks in ChaOS:

1. The source-of-truth hierarchy is implicit.
2. The repository contains support tooling, but the implementation boundary is not fully defined.
3. Multiple Meta-Agent runners exist.
4. Schemas do not have a declared authority level.
5. ChaOS risks drifting from constitution toward framework without explicit governance.

The review found that ChaOS remains primarily constitutional, but support tooling, schemas, workflows, prompts, and examples could slowly become framework-like if their authority is not bounded.

## Decision

ChaOS establishes the following authority hierarchy, implementation boundary, runner status, schema authority, support tooling philosophy, and deletion policy.

### Authority Order

1. Architectural Laws
2. Accepted Decision Records
3. `AGENTS.md`
4. `docs/architecture.md`
5. Other Documentation
6. Examples

If conflicts exist, higher authority wins.

### Implementation Boundary

Allowed:

- Documentation
- Decision records
- Journal entries
- Review tooling
- Governance tooling
- Minimal support scripts

Not allowed without explicit decision:

- Databases
- Frontends
- Workflow engines
- Autonomous self-modification
- Agent orchestration platforms
- Infrastructure layers
- Production systems

### Runner Status

PowerShell/CMD is the primary runner path.

Python is an experimental runner path.

Future decisions may revisit this if portability requirements become clearer.

### Schema Authority

Schemas are currently illustrative.

Schemas become normative only through an accepted decision record.

### Support Tooling Philosophy

Support tooling exists only to improve:

- Review quality
- Governance quality
- Documentation quality

Tooling is subordinate to the constitution.

Tooling may be removed if it stops providing value.

### Deletion Policy

Components should be removed when they are:

- Unreferenced
- Duplicative
- Generated artifacts
- Contradicted by accepted decisions
- Not demonstrably useful

## Rationale

ChaOS exists to be a constitution for reusable system architecture, not a framework that future projects must configure and maintain. These boundaries preserve that constitutional nature by making authority explicit, limiting implementation creep, and ensuring tooling serves review and governance rather than becoming the product.

The authority hierarchy gives future humans and agents a clear way to resolve conflicts. The implementation boundary allows small support scripts while preventing databases, frontends, infrastructure, production systems, and autonomous self-modification from appearing without explicit approval.

Declaring schemas illustrative prevents early structural artifacts from becoming accidental mandates. Declaring PowerShell/CMD primary and Python experimental reduces runner ambiguity without forcing premature deletion.

The deletion policy gives ChaOS a way to remove complexity, not only accumulate it.

## Alternatives Considered

### Continue Without Authority Hierarchy

Rejected because implicit authority requires private context. Future maintainers and agents need a clear way to resolve conflicts between laws, decisions, documentation, examples, and tooling.

### Treat Schemas As Normative Immediately

Rejected because the schemas have not yet been validated across enough downstream projects. Treating them as normative now would risk turning ChaOS into a framework too early.

### Allow Unrestricted Support Tooling

Rejected because unrestricted tooling would create framework creep. Support tooling is useful only while it improves review, governance, or documentation quality.

### Make Python And PowerShell Equal Authorities

Rejected because equal runner authority creates duplication risk. PowerShell/CMD is the primary runner for the current environment. Python remains experimental until portability requirements justify equal status.

## Consequences

This decision creates a clear governance boundary for future work.

Expected benefits:

- Fewer authority conflicts
- Clearer implementation limits
- Reduced framework drift
- Better control over support tooling
- Clearer schema interpretation
- Less runner ambiguity
- A formal basis for deleting unnecessary components

This decision does not add new architecture, agents, workflows, schemas, databases, frontends, infrastructure, or production systems.

## Feedback Plan

Future Meta-Agent reviews should evaluate:

- Constitutional drift
- Authority conflicts
- Tooling creep
- Framework creep
- Governance effectiveness

Reviews should identify whether this decision is being followed and whether any component has become unreferenced, duplicative, generated, contradicted by accepted decisions, or not demonstrably useful.

