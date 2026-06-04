# Decision 0007: Modal Language Authority

## Status

Accepted

## Purpose

Define how ChaOS uses absolute and permissive language in governing documents.

## Context

ChaOS relies on documentation as architecture. Ambiguous modal language can create drift when a future maintainer or agent cannot tell whether a sentence is a requirement, preference, hypothesis, or open question.

Several governing documents used `should` for requirements that protect the architecture, including traceability, human readability, approval boundaries, and recommendation-before-automation behavior.

## Decision

ChaOS governing documents must use modal language consistently:

- `Must` means required.
- `Must not` means prohibited.
- `May` means allowed, but not required.
- `Should` is reserved for open questions, hypotheses, historical review artifacts, and future considerations.

Constitutional rules, workflow requirements, agent requirements, evaluation requirements, approval boundaries, and change management rules must use `must` or `must not`.

Journal entries and prior review artifacts may retain softer language because they preserve evidence, uncertainty, and historical reasoning. Decision records may also retain historical wording unless a later decision explicitly supersedes or clarifies the rule.

## Rationale

Absolute language reduces interpretive drift. It helps future agents understand which parts of ChaOS are binding and which parts remain exploratory.

This change supports the architectural laws that context is a dependency, systems must be understandable by humans first, and every decision must be traceable.

## Alternatives Considered

### Leave Existing Language As-Is

Rejected because `should` was carrying both requirement and preference meanings, which makes future interpretation weaker.

### Replace Every `Should` With `Must`

Rejected because journals, hypotheses, examples, and open questions need room for uncertainty. False certainty would make ChaOS less honest and less inspectable.

### Create A Separate Style Guide

Rejected for now because the rule is small enough to live in `AGENTS.md` and this decision record.

## Consequences

Expected benefits:

- Clearer requirements
- Less agent drift
- Stronger approval boundaries
- More consistent governing documents
- Better separation between architecture and evidence

Expected tradeoff:

- Some language becomes more forceful. Future maintainers must avoid using `must` for preferences that have not earned constitutional weight.

## Feedback Plan

Future reviews must check whether governing documents use `must`, `must not`, `may`, and `should` consistently.

If agents overuse absolute language for speculative ideas, ChaOS must correct the misuse through a decision record or documentation update.
