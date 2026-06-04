# Evaluations

This document defines how ChaOS evaluates systems, workflows, agents, and architectural changes. It exists because feedback is more valuable than prediction.

## Purpose

Evaluation turns opinions into learning. A ChaOS evaluation should make quality visible and reusable.

## Evaluation Principles

- Evaluate against stated purpose.
- Preserve evidence.
- Include human judgment.
- Capture rejected recommendations.
- Prefer inspectable rubrics.
- Connect findings to future changes.

## Core Evaluation Questions

- Is the output clear?
- Is the decision traceable?
- Does the component remove more complexity than it adds?
- Can a future maintainer understand it?
- Is the pattern portable across domains?
- Are assumptions explicit?
- Is feedback captured?

## Agent Evaluation

Agent evaluation should review:

- Input use
- Reasoning visibility
- Output structure
- Handling of uncertainty
- Approval compliance
- Usefulness of recommendations
- Alignment with architectural laws

## Workflow Evaluation

Workflow evaluation should review:

- Trigger quality
- Input completeness
- Processing transparency
- Decision quality
- Action reliability
- Feedback usefulness

## Documentation Evaluation

Documentation evaluation should review:

- Purpose
- Fit within ChaOS
- Examples
- Future considerations
- Plain language
- Absence of empty placeholder content

## Example Rubric

| Criterion | Strong | Weak |
| --- | --- | --- |
| Clarity | A new maintainer can explain the pattern after reading it once | Meaning depends on private context |
| Traceability | Decisions connect to evidence and rationale | Decisions appear without explanation |
| Portability | Pattern works across multiple domains | Pattern assumes one business type |
| Feedback | Outcomes can improve future behavior | Results are not captured |

## Future Considerations

Future versions may include automated evaluation suites. Version 0.1 defines evaluation as an architectural habit first.

