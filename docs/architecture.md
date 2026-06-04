# ChaOS Architecture

This document exists to describe the first working architecture of ChaOS as a system. It connects the constitutional documents, structured schemas, workflow definitions, examples, and Meta-Agent into one readable operating model.

## Purpose

ChaOS is documentation-first architecture. Its first responsibility is to make reusable system thinking portable across future projects.

The architecture is intentionally simple:

- Markdown defines meaning.
- JSON Schema defines inspectable structure.
- YAML defines workflow contracts.
- CSV provides concrete examples.
- The Meta-Agent reviews the repository and recommends improvements.

## System Layers

ChaOS has five architectural layers:

1. Constitution: `README.md`, `AGENTS.md`, and the core documents in `docs/`.
2. Models: entity-signal-decision-outcome-feedback and trigger-input-processing-decision-action-feedback.
3. Agents: documented agent specifications with purpose, inputs, logic, outputs, evaluation, and guardrails.
4. Evaluation: rubrics and feedback practices that turn outputs into learning.
5. Review: the Meta-Agent process that observes ChaOS, diagnoses gaps, recommends improvements, and waits for human approval.

## How The Pieces Fit Together

The constitutional documents define the laws and language. The models define reusable patterns. The schemas make those patterns portable. The workflows show how work moves. The examples prove the patterns can be understood without implementation code.

The Meta-Agent sits above the repository as a reviewer, not an autonomous editor. It reads selected files, identifies contradictions and risks, and writes a Markdown report. It does not apply its own recommendations.

## Current Implementation Boundary

Version 0.1 allows a command-line Meta-Agent review script. The script may:

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

## Example

A future project inherits ChaOS to design a sales operating system. The project defines accounts as entities, website visits as signals, follow-up recommendations as decisions, booked meetings as outcomes, and acceptance or rejection as feedback. The Meta-Agent can later review whether the project-specific design still follows ChaOS laws.

## Future Considerations

Future versions may add project inheritance templates, richer evaluation reports, or optional adapters for implementation tools. Those additions must happen only after the simple review loop proves useful.
