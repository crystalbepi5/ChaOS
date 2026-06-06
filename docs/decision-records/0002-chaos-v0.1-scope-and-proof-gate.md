# Decision Record 0002: ChaOS v0.1 Scope And Proof Gate

## Context

Concept-review feedback validated the core ChaOS thesis, but it raised governance concerns that must be addressed before ChaOS expands further.

The concerns were:

- ChaOS may create abstraction tax if every project must translate messy reality into ChaOS vocabulary.
- The core model needs State as a first-class primitive.
- The semantic system model and workflow model overlap unless their distinction is explicit.
- ChaOS is not yet a portable constitution for other humans.
- ChaOS must prove it accelerates real builds, not only grow as a meta-framework.
- Pattern versioning and upstreaming rules are needed before projects silently fork ChaOS patterns.
- A two-week proof gate is needed to force practical use on a real build.

## Decision

ChaOS v0.1 is defined as:

- A personal architecture operating system.
- A local proof harness.
- A reusable pattern library under pressure test.

ChaOS v0.1 is not yet:

- A universal framework.
- A portable constitution for other humans.
- A production application framework.
- A deployed system.
- An agent platform.
- A replacement for domain-specific judgment.

The core semantic model is updated from:

```text
Entity -> Signal -> Decision -> Outcome -> Feedback
```

to:

```text
Entity -> Signal -> State -> Decision -> Outcome -> Feedback
```

ChaOS must explicitly distinguish the semantic system model from the workflow execution model.

ChaOS must document abstraction tax, pattern versioning, inheritance, upstreaming classifications, and a two-week proof gate.

## Rationale

ChaOS must stay useful before it becomes portable. A framework that grows faster than its proof creates maintenance burden and may make real projects slower.

State belongs in the core model because ChaOS needs a visible place for interpreted conditions that are not raw signals, final decisions, outcomes, or feedback.

Pattern inheritance must be explicit so downstream projects do not silently fork ChaOS or hide friction.

## Alternatives Considered

### Keep v0.1 framed as a portable constitution

Rejected. That claim is premature until other maintainers can use ChaOS successfully without private context.

### Keep State inside Decision or Outcome

Rejected. That hides interpretation and weakens traceability.

### Add implementation tooling to enforce the rules

Rejected for this PR. The current need is documentation and governance clarity, not code, CLIs, validators, schemas, agents, UI, integrations, package changes, or deployment work.

## Expected Consequences

- ChaOS v0.1 will make more honest claims.
- Projects using ChaOS will need to record inheritance, adaptations, bypasses, and upstreaming classifications.
- Major framework expansion will pause unless ChaOS proves practical leverage on a real build within two weeks.
- The semantic model and workflow model will be easier to apply without treating them as competing frameworks.

## Feedback Plan

Use the two-week proof gate on a real build such as Account Plan Tracker, BDR prioritization artifact, Meeting Cost Counter, Vowel, or another small workflow that can ship quickly.

Evaluate whether ChaOS reduced decision or design time, clarified requirements, prevented rework, improved Codex prompts, improved PR audit quality, or produced a working artifact faster.
