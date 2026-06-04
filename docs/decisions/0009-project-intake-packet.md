# Decision 0009: Project Intake Packet

## Status

Accepted

## Purpose

Create a directly usable intake artifact for turning raw project ideas into ChaOS-ready context.

## Context

ChaOS now has approved workflows for Context Sufficiency Assessment and Architecture Generation. Those workflows define how reasoning moves, but a user still needs a simple front door for capturing the business context before those workflows begin.

Without an intake artifact, context may remain scattered across conversation, private memory, notes, or assumptions. That would weaken the laws that context is a dependency and every decision must be traceable.

## Decision

ChaOS adds a `templates/` directory and a first reusable template:

- `templates/project-intake-packet.md`

The Project Intake Packet is a fillable Markdown document. It must help a human or agent capture project context, identify context risk, and route the project to Context Sufficiency Assessment, Architecture Generation, or no generation yet.

The template may be copied into future projects or used directly during a ChaOS review. It must remain plain Markdown and must not require software, databases, forms, automation, or vendor tools.

## Rationale

The Project Intake Packet makes ChaOS actively usable without turning ChaOS into an application. It creates a concrete first step that a human can complete and an agent can inspect.

The artifact removes more complexity than it adds because it reduces blank-page ambiguity, private-memory dependence, and unsupported Architecture Generation.

## Alternatives Considered

### Build An App Or Form

Rejected because ChaOS must remain documentation-first. A Markdown template is more inspectable, portable, and maintainable.

### Add Separate Templates For Every Model

Rejected for now because multiple templates would create more surfaces before the intake pattern is proven.

### Keep Intake Inside README Instructions

Rejected because README guidance is useful for orientation but not enough for reusable project capture.

## Consequences

Expected benefits:

- Clearer project intake
- Less private context
- Faster routing to the right workflow
- More consistent Architecture Generation inputs
- A usable artifact that does not introduce implementation creep

Expected tradeoff:

- The repository gains a new top-level directory. This is acceptable because the directory contains reusable artifacts, not product code.

## Feedback Plan

Future project reviews must record whether the Project Intake Packet captured enough context to route the project correctly.

If repeated use shows missing sections or unnecessary sections, ChaOS must update the template and record the reason when the change affects inheritance behavior.

## Examples

A founder with a rough product idea can complete the packet before asking for Architecture Generation.

A coding agent can use the packet to separate direct context from assumptions before proposing architecture.

A future project can keep the completed packet as an evidence artifact alongside its Architecture Starter Package.

## Future Considerations

Future versions may add focused templates for Architecture Starter Packages, Context Sufficiency Assessment outputs, or project inheritance reviews.

ChaOS must not add additional templates until repeated use shows that one packet has become too broad or difficult to maintain.
