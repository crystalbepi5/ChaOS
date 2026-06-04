# ChaOS Agent Handbook

This file is the operating constitution for all future coding agents working in this repository.

## Repository Purpose

ChaOS is the Chase Architecture Operating System. It is a documentation-first architecture repository for turning ideas into reusable systems. The goal is not to create application code. The goal is to create durable patterns that future projects can inherit.

Agents working here should protect the repository from becoming too specific, too clever, too tool-bound, or too dependent on the memory of its creator.

## Architectural Laws

Agents must preserve and apply the architectural laws in `docs/architectural-laws.md`:

1. Do not optimize chaos into more chaos.
2. Every component must remove more complexity than it adds.
3. Context is a dependency. Minimize it.
4. Systems should be understandable by humans first.
5. The system must survive the loss of its creator.
6. Recommend before automating.
7. Prefer inspectable systems over intelligent systems.
8. Every decision should be traceable.
9. Feedback is more valuable than prediction.
10. The simplest architecture that works is the correct architecture.

When a requested change conflicts with these laws, explain the conflict and propose a simpler alternative.

## Design Philosophy

ChaOS optimizes for clarity, reusability, portability, explainability, modularity, human comprehension, and long-term maintainability.

ChaOS avoids premature complexity, hidden logic, vendor lock-in, platform-specific assumptions, AI hype, black-box decision making, and unnecessary dependencies.

Agents should prefer explicit structure over impressive language. A good ChaOS document helps a future maintainer make better decisions.

## Documentation Standards

Every Markdown file should explain:

- Why the file exists
- What purpose it serves
- How it fits into the system
- Examples of use
- Future considerations

Do not add empty placeholder files. Do not add TODO-only documents. If a subject is not ready for a full document, add a meaningful section to an existing document and explain the assumption.

Use plain language. Define terms before relying on them. Prefer short sections and concrete examples.

## Agent Standards

Every agent specification must include:

- Purpose
- Inputs
- Processing logic
- Outputs
- Evaluation
- Examples
- Failure modes
- Guardrails

Agents should recommend before automating. They may analyze, diagnose, compare, summarize, and propose. They should not silently change architecture, policy, schemas, or evaluation criteria without human approval.

## Workflow Standards

Every workflow should follow:

Trigger -> Input -> Processing -> Decision -> Action -> Feedback

Workflow documentation must name responsibilities, failure modes, and evaluation methods for each stage. A workflow is incomplete if it describes the happy path but not how it learns from failure.

## Evaluation Standards

Every meaningful output should be evaluated against visible criteria. Evaluation should be traceable to the purpose of the system, not to vague preference.

Prefer evaluation rubrics that can be understood by humans and reused by agents. Capture both qualitative and quantitative feedback when possible.

## Change Management Standards

Architectural changes must be traceable. Use decision records when a change affects system laws, models, schemas, workflows, or agent behavior.

A good change record states:

- Context
- Decision
- Rationale
- Alternatives considered
- Expected consequences
- Feedback plan

## Working Agreement

Before adding complexity, ask what complexity is being removed. Before adding automation, ask what recommendation pattern has been proven. Before adding intelligence, ask how the system will remain inspectable.

Assume ChaOS will eventually outlive its creator.

