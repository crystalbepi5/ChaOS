# Account Plan Tracker Abstraction Tax Log

## Why This File Exists

This file records whether ChaOS vocabulary helps or hurts the Account Plan Tracker proof.

ChaOS v0.1 must pay for itself. If applying ChaOS creates more translation cost than delivery leverage, the project may adapt, bypass, or reject patterns, but the reason must be recorded.

## Purpose

The purpose of this log is to track abstraction tax during the proof gate without pretending the proof is complete.

## Current Status

Initial abstraction tax status: `not_yet_measured`

Proof status: `implementation_proof_started_not_concluded`

Implementation proof artifact:

```text
examples/proof-gates/account-plan-tracker/static-prototype/index.html
```

## Where ChaOS Vocabulary Helped

Initial observations:

- Entity helps separate Account, Contact/persona, Action item, Owner, and Review.
- Signal helps prevent raw observations from becoming recommendations too early.
- State helps name account readiness without treating readiness as action permission.
- Decision helps keep next action recommendations traceable.
- Outcome and Feedback help prevent the tool from becoming a static planning document.
- Workflow model helps outline a small review loop without assuming integrations.

## Where ChaOS Vocabulary Felt Forced

Initial observations:

- Account planning may naturally use terms like play, gap, priority, and next step more than generic ChaOS vocabulary.
- The full workflow model may be heavier than needed for a narrow MVP.
- Contact/persona may not need to become a full entity in the first build.
- State labels may need domain-native wording for BDR users.

## Concepts That Do Not Map Cleanly Yet

- Play: could be an entity, decision option, or template.
- Owner: could be an entity, assignment field, or workflow responsibility.
- Account plan: could be an entity, artifact, or view over account state.
- Priority: could be state, decision, or UI ordering.
- Persona gap: could be signal, state, or missing input.

## Estimated Translation Cost

Current estimate: `medium_unknown`

Reason:

The ChaOS model gives useful structure, but several account-planning concepts need careful mapping before implementation. The proof should measure whether this mapping saves time later.

## Estimated Reuse Benefit

Current estimate: `medium_promising`

Reason:

The model already helps separate evidence, interpretation, recommendation, outcome, and feedback. That separation should reduce rework if the MVP becomes a build prompt.

## Continue, Adapt, Or Pause

Current recommendation: `continue_with_limited_mvp_scope`

Rationale:

ChaOS appears useful enough to create a clearer Account Plan Tracker starter package and static prototype, but the proof must stay focused on a buildable artifact. If more framework concepts are needed before a useful next implementation step emerges, the proof should pause and record failure risk.

## Pattern Adaptation Records

| Pattern | Current handling | Classification | Reason |
| --- | --- | --- | --- |
| Core semantic model | Use with State first-class. | `project_specific_exception` | The model maps well enough for MVP planning. |
| Core workflow model | Adapt to one lightweight review loop. | `project_specific_exception` | Full workflow decomposition may be too heavy. |
| Core agent model | Bypass. | `project_specific_exception` | No agent behavior is needed for first proof. |
| Production integration model | Bypass. | `project_specific_exception` | Live integrations would hide whether the planning artifact is useful. |

## Proof Review Questions

At the decision deadline, update this log with answers to:

- Did ChaOS reduce ambiguity?
- Did ChaOS reduce design time?
- Did ChaOS create unnecessary translation work?
- Did the starter package become a useful Codex build prompt?
- Did the static prototype make the Account Plan Tracker easier to evaluate?
- Did any pattern deserve `candidate_upstream_improvement`?
- Did any pattern reveal `breaking_abstraction`?
- Did any pattern become a `rejected_pattern`?

## Failure Watch

The proof should be considered at risk if:

- More documents are needed before a build prompt can be written.
- The MVP cannot be explained in account-planning language.
- ChaOS terms replace domain clarity instead of improving it.
- The proof produces framework refinement but no implementation-ready next step.
