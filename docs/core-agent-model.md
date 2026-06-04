# Core Agent Model

This document defines the standard structure for agents in ChaOS. It exists so future projects can design agents that are understandable, testable, and portable across domains.

Every agent must contain:

- Purpose
- Inputs
- Processing Logic
- Outputs
- Evaluation
- Examples

## Why This Structure Exists

Agents become dangerous or useless when their role is vague. The core agent model forces clarity before implementation. It separates what the agent is for, what it receives, how it reasons, what it produces, and how its work is judged.

This structure also prevents agents from becoming personality-driven black boxes. An agent must be a documented system component, not a magic assistant with unclear boundaries.

## Purpose

Purpose explains why the agent exists and what complexity it removes.

A good purpose statement is narrow enough to evaluate. "Help with sales" is too broad. "Recommend next account follow-up based on recent signals and account stage" is clearer.

## Inputs

Inputs define what the agent is allowed to use. Inputs may include entities, signals, previous decisions, outcomes, user instructions, source documents, or evaluation history.

Inputs must preserve source references. If the agent uses context that is not visible, that context must be documented as a dependency.

## Processing Logic

Processing logic explains how the agent transforms inputs into outputs. This may include rules, rubrics, ranking methods, comparison steps, prompt structure, retrieval process, or human approval gates.

The processing logic must be inspectable. If an agent uses a model, the agent specification must still describe the intended reasoning path.

## Outputs

Outputs define what the agent produces. Outputs may include recommendations, summaries, classifications, decision records, review comments, patches, evaluation reports, or questions for humans.

Outputs must be structured enough to evaluate and reuse.

## Evaluation

Evaluation defines how the agent is judged. It must include acceptance criteria, failure modes, review process, and feedback capture.

Evaluation must focus on usefulness, traceability, accuracy, completeness, and alignment with architectural laws.

## Examples

Each agent must include examples from at least one domain. Reusable agents must include multiple domain examples when possible.

## How Agents Must Be Designed

1. Start with the decision or recommendation the agent supports.
2. Identify the entity and signals involved.
3. Define required inputs and forbidden inputs.
4. Specify output structure.
5. Define evaluation criteria before implementation.
6. Define approval boundaries.
7. Add examples and failure modes.

## How Agents Must Be Tested

Agents must be tested against representative examples, edge cases, ambiguous inputs, missing information, conflicting signals, and known failure scenarios.

Tests must ask:

- Did the agent use only allowed inputs?
- Did it explain its reasoning?
- Did it preserve source references?
- Did it recommend instead of acting when approval was required?
- Did it handle uncertainty honestly?
- Did the output match the expected structure?

## How Agents Must Evolve

Agents must evolve through feedback. Rejected recommendations, evaluation failures, repeated clarifications, and human corrections must become evidence for improvement.

Agent evolution must be documented. If an agent changes its purpose, inputs, outputs, or approval boundary, the change must create a decision record.

## Future Considerations

Future versions may define maturity levels for agents, reusable prompt contracts, model-provider adapters, or automated evaluation suites. Version 0.1 keeps the model vendor-neutral and documentation-first.
