# Journal

This directory contains review artifacts.

Journal entries are working records of observations, diagnoses, recommendations, questions, and proposed next actions. They are not approved architecture changes by themselves.

## Purpose

The journal exists so ChaOS can preserve feedback and review history without turning every observation into a formal decision.

A journal entry may contain useful recommendations, but those recommendations require human approval before they change architectural laws, schemas, workflows, agent standards, or repository policy.

## How Journal Entries Fit Into ChaOS

Journal entries support the feedback loop:

Observe -> Diagnose -> Recommend -> Human Approval

They are evidence for future decisions. When a recommendation is accepted, the approval should be captured in a decision record under `docs/decisions/`.

## Example

`0001-meta-agent-review.md` records the first Meta-Agent review. It identifies repository alignment issues and recommends cleanup. The approved cleanup is captured separately as a decision record.

## Future Considerations

If journal entries become frequent, ChaOS may later define a naming convention by review type. For now, numbered Markdown files are sufficient.

