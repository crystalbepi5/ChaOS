# Decision 0008: Context Sufficiency Assessment

## Status

Accepted

## Purpose

Recognize Context Sufficiency Assessment as a supported ChaOS workflow before Architecture Generation.

## Context

Architecture Generation is already an accepted ChaOS activity. It transforms business context into an Architecture Starter Package without creating implementation requirements.

Journal Entry 0006, `docs/journal/0006-context-sufficiency-test-community-garden.md`, tested a limited-context community garden project and showed that ChaOS can separate known facts, reasonable inferences, and unknown information before generating architecture. The test also showed that incomplete architecture can be a disciplined output when evidence is incomplete.

Without a formal sufficiency gate, Architecture Generation could drift into filling gaps with assumptions. That would violate the laws that context is a dependency, systems must be understandable by humans first, and every decision must be traceable.

## Decision

ChaOS accepts Context Sufficiency Assessment as a supported workflow.

Context Sufficiency Assessment evaluates whether available business context is sufficient for Architecture Generation.

The workflow is:

Business Context

-> Known / Inferred / Unknown

-> Readiness Decision

-> Clarifying Questions or Architecture Generation

Architecture Generation must be preceded by Context Sufficiency Assessment when business context is incomplete, ambiguous, conflicting, or inherited from private memory.

Context Sufficiency Assessment may produce one of four readiness decisions:

- READY
- PARTIAL
- NEEDS CLARIFICATION
- DO NOT GENERATE YET

## Rationale

Context Sufficiency Assessment protects ChaOS from premature certainty. It allows the system to reduce blank-page cost without pretending missing context is known.

The workflow also makes uncertainty useful. A result of NEEDS CLARIFICATION is not a failure when it prevents unsupported architecture.

## Examples

### READY

A project provides purpose, users, primary entities, signals, decisions, outcomes, constraints, governance boundaries, and examples. ChaOS may proceed to Architecture Generation for a full starter package.

### PARTIAL

A project defines entities and outcomes but does not define workflow ownership. ChaOS may generate the entity model and outcome model, but the workflow model must remain partial or blocked.

### NEEDS CLARIFICATION

A project describes a coordination problem but does not define key terms, responsibilities, outcomes, or decision authority. ChaOS must produce clarifying questions before full Architecture Generation.

### DO NOT GENERATE YET

A project request depends almost entirely on private memory or conflicting stakeholder assumptions. ChaOS must state the minimum missing context required before generation may begin.

## Alternatives Considered

### Fold Sufficiency Into Architecture Generation

Rejected because the gate would be easier to skip or bury inside generated architecture. A separate workflow keeps the decision visible.

### Require Sufficiency Assessment Before Every Architecture Generation

Rejected because complete and well-documented business context may not need a separate sufficiency pass. The requirement applies when context is incomplete, ambiguous, conflicting, or inherited from private memory.

### Treat Context Sufficiency As A Candidate Concept Only

Rejected because the evidence from Journal Entry 0006 showed a workflow need, not only a concept label. The accepted workflow does not add a new core model, schema, agent, database, frontend, infrastructure, or automation layer.

## Consequences

Expected benefits:

- Fewer unsupported assumptions
- Clearer readiness decisions
- Better clarifying questions
- Safer Architecture Generation
- Stronger traceability between business context and generated architecture

Expected tradeoff:

- Some ambiguous projects will pause before full architecture generation. This is acceptable because disciplined incompleteness is better than confident drift.

## Feedback Plan

Future Architecture Generation tests must record whether Context Sufficiency Assessment was needed.

Future reviews must evaluate whether the readiness decision was accurate, whether clarifying questions improved the architecture, and whether generated architecture stayed within available evidence.

## Future Considerations

Future versions may add a lightweight example output format for Context Sufficiency Assessment if repeated tests show that free-form assessment records become difficult to compare.

ChaOS must not add a new schema for this workflow until repeated use proves that a structured schema would remove more complexity than it adds.
