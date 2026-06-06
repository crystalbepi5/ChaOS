# ChaOS v0.1 Scope

## Why This File Exists

This file defines the honest scope of ChaOS v0.1 after concept-review feedback.

The feedback validated the core ChaOS thesis, but it also identified a risk: ChaOS may become a meta-framework that creates translation work instead of accelerating real builds. This file makes that risk explicit and defines the governance rules that keep v0.1 under pressure test.

## Purpose

The purpose of this document is to clarify what ChaOS v0.1 is allowed to claim, how projects may inherit or bypass ChaOS patterns, and how ChaOS must prove practical leverage before expanding further.

ChaOS v0.1 is allowed to help one maintainer think, build, and audit more clearly before it claims to be portable for other maintainers.

## ChaOS v0.1 Is

ChaOS v0.1 is:

- A personal architecture operating system.
- A local proof harness.
- A reusable pattern library under pressure test.

## ChaOS v0.1 Is Not Yet

ChaOS v0.1 is not yet:

- A universal framework.
- A portable constitution for other humans.
- A production application framework.
- A deployed system.
- An agent platform.
- A replacement for domain-specific judgment.

## Core Model

The v0.1 semantic model is:

```text
Entity -> Signal -> State -> Decision -> Outcome -> Feedback
```

State is a first-class primitive. State is the current interpreted condition of an entity based on evidence, history, validation, and review status.

The workflow execution model is:

```text
Trigger -> Input -> Processing -> Decision -> Action -> Feedback
```

The semantic model describes what the system knows and how that knowledge changes over time. The workflow model describes how a specific run, event, or user action moves through the system. Workflows are usually executions over the semantic model, not a competing framework.

## Abstraction Tax Rule

ChaOS must pay for itself. If applying ChaOS to a project creates more translation cost than delivery leverage, the project may adapt, bypass, or fork the pattern, but the reason must be recorded.

Abstraction tax includes:

- Time spent translating domain concepts into ChaOS vocabulary.
- Extra ceremony before implementation.
- Domain mismatch with Entity, Signal, State, Decision, Outcome, or Feedback vocabulary.
- Maintainer confusion.
- Pattern reuse that saves less time than it costs.

Acceptable bypass examples include:

- A tiny project does not need the full ChaOS model.
- A domain has a better native vocabulary.
- A project needs to ship before pattern generalization is useful.

A bypass is not failure by itself. An unrecorded bypass is failure because it hides whether ChaOS helped or got in the way.

## Pattern Versioning And Inheritance

A project using ChaOS must declare:

- ChaOS pattern version inherited.
- Patterns used.
- Patterns adapted.
- Patterns bypassed.
- Reason for each adaptation or bypass.

Example:

```text
Project: Account Plan Tracker
Inherits: ChaOS v0.1
Uses:
- Context Sufficiency Assessment
- Entity/Signal/State/Decision/Outcome/Feedback
Adapts:
- Signal model narrowed to GTM account signals
Bypasses:
- Full workflow model
Reason:
- Project scope is narrow and does not need full workflow decomposition yet
```

## Upstreaming Rule

If a project modifies a ChaOS pattern, the change must be classified as one of:

- `project_specific_exception`
- `candidate_upstream_improvement`
- `breaking_abstraction`
- `rejected_pattern`

Definitions:

- `project_specific_exception`: useful only for this project.
- `candidate_upstream_improvement`: may improve ChaOS core.
- `breaking_abstraction`: reveals the current pattern does not generalize.
- `rejected_pattern`: pattern created friction and must not be reused in this project.

The purpose of this rule is to prevent silent framework fragmentation. ChaOS must know whether a downstream change is a local exception, a core improvement, or evidence that the abstraction is wrong.

## Two-Week Proof Gate

ChaOS must be used to accelerate a real build within two weeks of major framework expansion. If it cannot demonstrate practical leverage, expansion pauses.

The proof gate must ask:

- Did ChaOS reduce decision or design time?
- Did ChaOS make requirements clearer?
- Did ChaOS prevent rework?
- Did ChaOS improve Codex prompts?
- Did ChaOS improve PR audit quality?
- Did ChaOS produce a working artifact faster?

Suggested proof projects include:

- Account Plan Tracker.
- BDR prioritization artifact.
- Meeting cost counter.
- Vowel.
- Any small real workflow that can ship in under two weeks.

## Success Criteria

ChaOS v0.1 succeeds if:

- ChaOS saves time or improves clarity on at least one real build.
- The project produces a working artifact faster or with fewer design reversals.
- The abstraction tax is lower than the reuse benefit.
- Project inheritance decisions are recorded.
- Pattern adaptations and bypasses are classified.

## Failure Criteria

ChaOS v0.1 fails if:

- ChaOS grows but no real project ships.
- Applying ChaOS costs more time than it saves.
- Projects silently bypass patterns without recording why.
- The framework becomes the work instead of supporting the work.

## Examples Of Use

Before starting a small build, a maintainer may declare:

```text
Project: Meeting Cost Counter
Inherits: ChaOS v0.1
Uses:
- Context Sufficiency Assessment
- Entity/Signal/State/Decision/Outcome/Feedback
Adapts:
- Entity narrowed to Meeting
Bypasses:
- Full agent model
Reason:
- No autonomous or assistant behavior is needed for the first artifact
Proof target:
- Working artifact shipped within two weeks
```

After the build, the maintainer must record whether ChaOS reduced decision time, clarified requirements, prevented rework, improved prompts, improved audit quality, or helped ship faster.

## Future Considerations

ChaOS may claim broader portability only after real builds prove that its patterns reduce net work for maintainers other than the original creator. Until then, v0.1 must remain honest: personal architecture OS first, local proof harness second, reusable pattern library under pressure test third.
