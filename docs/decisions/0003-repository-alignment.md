# Decision 0003: Repository Alignment After First Meta-Agent Review

Status: Accepted

Date: 2026-06-02

## Context

The first Meta-Agent review was saved at `docs/journal/0001-meta-agent-review.md`. The review found that the repository structure documentation had drifted from the actual repository after the first working Meta-Agent CLI was added.

The review also found that `docs/meta-agent.md` referenced `schemas/system-event.schema.json`, but the repository contains `schemas/system-model.schema.json`.

## Decision

Accept the Meta-Agent recommendation to align the repository documentation with the current repository state.

Approved changes:

1. Update `docs/repository-structure.md` so it accurately reflects the current repository, including `agents/`, `scripts/`, `.env.example`, and `docs/journal/`.
2. Add `docs/journal/README.md` explaining that journal entries are review artifacts, not approved architecture changes.
3. Fix the stale schema reference in `docs/meta-agent.md` from `schemas/system-event.schema.json` to `schemas/system-model.schema.json`.

## Rationale

This is an alignment cleanup, not a new architecture change. The repository should teach future maintainers what exists and how to interpret review artifacts.

Accurate structure documentation supports the ChaOS laws that context is a dependency, systems should be understandable by humans first, and every decision should be traceable.

## Alternatives Considered

- Leave the drift unresolved until a larger version update.
- Add a new `schemas/system-event.schema.json` to match the stale reference.
- Remove the Meta-Agent CLI from the repository to preserve the original documentation-only boundary.

These alternatives were rejected because they either preserve confusion, add unnecessary structure, or undo already approved useful review tooling.

## Consequences

The repository structure documentation will match the current files more closely. Journal entries will have an explicit interpretation boundary. The Meta-Agent example will reference an existing schema.

No new architecture, agents, schemas, frontend, database, Docker, or infrastructure are introduced by this decision.

## Feedback Plan

Future Meta-Agent reviews should check whether repository structure documentation remains aligned with the actual repository and whether journal entries remain clearly separated from approved decisions.

