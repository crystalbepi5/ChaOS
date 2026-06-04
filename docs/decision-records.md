# Decision Records

This document defines how ChaOS records important decisions. It exists because every decision must be traceable.

## Purpose

Decision records preserve context, rationale, alternatives, consequences, and feedback plans. They help future maintainers understand why the system changed.

## When To Create A Decision Record

Create a decision record when a change affects:

- Architectural laws
- Core system model
- Core workflow model
- Core agent model
- Meta-Agent behavior
- Schemas
- Evaluation standards
- Change management standards
- Project inheritance rules

## Decision Record Structure

Each decision record must include:

- Title
- Status
- Date
- Context
- Decision
- Rationale
- Alternatives considered
- Consequences
- Feedback plan

## Example

Title: Use Markdown, JSON Schema, YAML, and CSV for Version 0.1

Status: Accepted

Context: ChaOS needs a first version that is portable, inspectable, and not tied to an implementation stack.

Decision: Use Markdown for constitutional documents, JSON Schema for structured contracts, YAML for workflows, and CSV for examples.

Rationale: These formats are readable, durable, widely supported, and easy for both humans and agents to inspect.

Alternatives considered: A database, documentation website, code framework, or automation platform.

Consequences: The repository remains simple, but later implementation work must map these artifacts into working systems.

Feedback plan: Review whether future projects can inherit the structure without additional scaffolding.

## Future Considerations

Future versions may store decision records as individual files. Version 0.1 defines the pattern before multiplying documents.
