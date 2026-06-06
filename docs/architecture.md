# ChaOS Architecture

This document exists to describe the first working architecture of ChaOS as a system. It connects the constitutional documents, structured schemas, workflow definitions, examples, governance rules, and Meta-Agent into one readable operating model.

## Purpose

ChaOS is documentation-first architecture. Its v0.1 responsibility is to help one maintainer think, build, and audit more clearly before it claims to be portable for other maintainers.

ChaOS v0.1 is a personal architecture operating system, a local proof harness, and a reusable pattern library under pressure test. It is not yet a universal framework, portable constitution for other humans, production application framework, deployed system, agent platform, or replacement for domain-specific judgment.

The architecture is intentionally simple:

- Markdown defines meaning.
- JSON Schema defines inspectable structure.
- YAML defines workflow contracts.
- CSV provides concrete examples.
- The Meta-Agent reviews the repository and recommends improvements.

## System Layers

ChaOS has six architectural layers:

1. Constitution: `README.md`, `AGENTS.md`, and the core documents in `docs/`.
2. Governance: v0.1 scope, abstraction tax, inheritance, upstreaming, and proof-gate rules.
3. Models: entity-signal-state-decision-outcome-feedback and trigger-input-processing-decision-action-feedback.
4. Agents: documented agent specifications with purpose, inputs, logic, outputs, evaluation, and guardrails.
5. Evaluation: rubrics and feedback practices that turn outputs into learning.
6. Review: the Meta-Agent process that observes ChaOS, diagnoses gaps, recommends improvements, and waits for human approval.

## How The Pieces Fit Together

The constitutional documents define the laws and language. The governance layer defines when ChaOS is allowed to expand and when a project may adapt or bypass inherited patterns. The models define reusable patterns. The schemas make those patterns inspectable. The workflows show how work moves. The examples prove the patterns can be understood without production application code.

Templates provide a usable intake layer. They help humans and agents capture project context before applying workflow contracts.

The Meta-Agent sits above the repository as a reviewer, not an autonomous editor. It reads selected files, identifies contradictions and risks, and writes a Markdown report. It does not apply its own recommendations.

Context Sufficiency Assessment sits before Architecture Generation when business context is incomplete, ambiguous, conflicting, or inherited from private memory. It separates known facts, reasonable inferences, and unknown information before ChaOS generates architecture.

Architecture Generation transforms sufficient business context into a reviewable Architecture Starter Package. It may generate project summaries, entity models, workflow models, agent definitions, governance requirements, risks, guardrails, and evaluation criteria. It must not create implementation requirements or approve architecture changes automatically.

## Semantic Model And Workflow Model

The semantic system model describes what the system knows and how that knowledge changes over time:

```text
Entity -> Signal -> State -> Decision -> Outcome -> Feedback
```

The workflow execution model describes how a specific run, event, or user action moves through the system:

```text
Trigger -> Input -> Processing -> Decision -> Action -> Feedback
```

A workflow is usually an execution over the semantic model, not a competing framework.

## Current Implementation Boundary

Version 0.1 allows a command-line Meta-Agent review script and local proof-harness work such as the Order Graph reference implementation track. These local artifacts may prove concepts, validation boundaries, and audit patterns.

The script may:

- Read selected repository files
- Combine them into review context
- Send that context to an LLM
- Save a Markdown review report

The script may not:

- Modify architecture files based on its own recommendations
- Add hidden state
- Use a database
- Depend on a frontend
- Introduce infrastructure
- Treat model output as approval

ChaOS v0.1 must not claim production portability until it proves practical leverage on real builds.

## Abstraction Tax Boundary

ChaOS must pay for itself. If applying ChaOS to a project creates more translation cost than delivery leverage, the project may adapt, bypass, or fork the pattern, but the reason must be recorded.

Abstraction tax must be evaluated through real builds, not through framework expansion.

## Proof Gate

ChaOS must be used to accelerate a real build within two weeks of major framework expansion. If it cannot demonstrate practical leverage, expansion pauses.

The proof gate must evaluate whether ChaOS reduced decision or design time, clarified requirements, prevented rework, improved Codex prompts, improved PR audit quality, or produced a working artifact faster.

## Example

A future project inherits ChaOS to design an account plan tracker. The project may define accounts as entities, account activity as signals, account warmth as state, follow-up recommendations as decisions, completed outreach as outcomes, and acceptance or rejection as feedback. If the full workflow model adds more ceremony than leverage, the project may bypass that pattern, but it must record the reason and classify the bypass.

## Future Considerations

Future versions may add project inheritance templates, richer evaluation reports, or optional adapters for implementation tools. Those additions must happen only after the simple review loop and real-build proof gate demonstrate practical leverage.
