# Decision 0010: Architecture Starter Package Template

## Status

Accepted

## Purpose

Create a standard output artifact for Architecture Generation.

## Context

ChaOS now has a Project Intake Packet, Context Sufficiency Assessment, and an Architecture Generation workflow contract. Architecture Generation needs a consistent reviewable output so generated architecture does not vary by agent memory, writing style, or hidden assumptions.

Without a standard starter package, future projects may receive architecture in inconsistent shapes. That would weaken traceability and make human review harder.

## Decision

ChaOS adds a reusable template:

- `templates/architecture-starter-package.md`

The Architecture Starter Package template is the standard output format for Architecture Generation.

It must include:

- Project Summary
- Context Sufficiency Result
- Package Section Status
- Entity Model
- Workflow Model
- Agent Definition when applicable
- Governance Requirements
- Risks
- Guardrails
- Evaluation Criteria
- Open Questions
- Human Review Decision
- Feedback Capture

The template must label sections as complete, partial, blocked, or not applicable. It must preserve Known, Inferred, and Unknown context when inherited from Context Sufficiency Assessment.

## Rationale

The template makes Architecture Generation usable and reviewable. It gives humans and agents a shared artifact for inspecting generated architecture before implementation choices begin.

This removes more complexity than it adds because it standardizes the output of an already accepted workflow without adding software, schemas, automation, infrastructure, or vendor dependencies.

## Alternatives Considered

### Let Each Agent Format Starter Packages Freely

Rejected because flexible formatting would increase hidden context and make review inconsistent.

### Create A Schema Immediately

Rejected because a Markdown template is sufficient for current use. A schema would add enforcement before repeated use proves which fields are stable.

### Combine Intake And Starter Package Into One Template

Rejected because intake captures raw context and routing, while the starter package captures generated architecture for review. Combining them would make the artifact too large and blur input with output.

## Consequences

Expected benefits:

- More consistent Architecture Generation outputs
- Easier human review
- Better traceability from intake and sufficiency assessment to generated architecture
- Clearer distinction between architecture and implementation
- Better feedback capture after review

Expected tradeoff:

- ChaOS now has two templates. This is acceptable because each template has a distinct purpose: intake captures context, and the starter package captures generated architecture.

## Feedback Plan

Future Architecture Generation tests must record whether the starter package format was useful, too broad, too narrow, or missing required review information.

If repeated use shows that some sections are unnecessary or missing, ChaOS must update the template and record the rationale when the change affects future inheritance.

## Examples

A project with READY context can receive a full starter package where entity, workflow, governance, and evaluation sections are complete.

A project with PARTIAL context can receive a starter package where supported sections are complete and unsupported sections are blocked with specific missing context.

A project with no agent need can mark Agent Definition as not applicable instead of inventing an agent.

## Future Considerations

Future versions may add completed example starter packages for common project types.

ChaOS must not add a schema or generator for this template until repeated manual use proves the stable shape of the artifact.
