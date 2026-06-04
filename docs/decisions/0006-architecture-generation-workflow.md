# Decision 0006: Architecture Generation Workflow

## Status

Accepted

## Purpose

Formalize Architecture Generation as a supported ChaOS activity.

## Context

ChaOS has successfully completed:

- Meta-Agent Reviews
- Project Inheritance Reviews
- Architecture Generation Test for the RFP Discovery Agent

The Architecture Generation Test demonstrated that business context can be transformed into an architecture starter package without requiring new architecture.

## Decision

Architecture Generation is recognized as a supported ChaOS workflow.

The workflow is:

Business Context

-> Architecture Generation

-> Architecture Starter Package

-> Human Review

-> Implementation Decision

Architecture Generation outputs may include:

- Project Summary
- Entity Model
- Workflow Model
- Agent Definition
- Governance Requirements
- Risks
- Guardrails
- Evaluation Criteria

Architecture Generation may reference:

- Constitutional Concepts
- Candidate Concepts
- Existing Governance

Architecture Generation may not:

- Create constitutional concepts
- Create governance decisions
- Approve architecture changes
- Create implementation requirements automatically

Human review remains required.

## Rationale

Architecture Generation supports the ChaOS goal of reducing the cost of starting over. It allows a project to begin from reusable constitutional concepts rather than a blank page.

The RFP Discovery Agent test showed that ChaOS can transform business context into a structured architecture starter package using existing models:

- Entity -> Signal -> Decision -> Outcome -> Feedback
- Trigger -> Input -> Processing -> Decision -> Action -> Feedback
- Purpose -> Inputs -> Processing Logic -> Outputs -> Evaluation -> Examples

This preserves the documentation-first philosophy because Architecture Generation produces reviewable architecture, not implementation.

Architecture Generation also keeps business context visible. ChaOS does not eliminate business context; it gives that context a reusable architectural shape.

## Alternatives Considered

### Continue Using Inheritance Reviews Only

Rejected because inheritance reviews answer whether a project can inherit ChaOS, but they do not fully capture the value of using ChaOS to generate the first architecture draft.

Architecture Generation is a distinct activity that tests whether ChaOS can reduce startup effort directly.

### Generate Implementation Plans Directly

Rejected because implementation planning would move too quickly toward software design, infrastructure, databases, workflow engines, or automation.

ChaOS should generate architecture before implementation.

### Allow Generated Architecture To Become Authoritative

Rejected because generated architecture is not governance. Architecture Starter Packages are review artifacts until humans approve decisions through the established governance process.

## Consequences

Expected benefits:

- Faster project startup
- Consistent architecture
- Reduced blank-page cost
- Reuse of constitutional concepts
- Clearer separation between architecture generation and implementation planning
- Better evidence about which ChaOS concepts transfer across projects

Architecture Generation remains subordinate to existing governance and does not authorize automatic changes to ChaOS or to any project.

## Feedback Plan

Future architecture generation tests should evaluate:

- Architecture quality
- Reusability
- Consistency
- Candidate concept pressure
- Reduction of startup effort
- Whether generated packages remain useful after human review
- Whether generation creates unnecessary complexity

Future tests should not automatically create constitutional concepts, governance decisions, implementation requirements, agents, schemas, workflows, databases, frontends, infrastructure, or orchestration layers.

## Conclusion

ChaOS reduces startup effort by generating architecture, not by eliminating business context.

