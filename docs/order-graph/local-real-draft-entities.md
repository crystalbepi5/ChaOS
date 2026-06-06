# Local-Real Draft Entities

## Why This File Exists

This file defines expectations for local-real draft entity artifacts before ChaOS is allowed to treat them as canonical entities.

The local-real path can now produce account identity candidates, but candidates are not canonical entities. The next risk is treating candidates as final identity resolution too early. This document keeps the draft step visible and bounded.

## Purpose

The purpose of this document is to define how validated account identity candidates may become draft entities without creating canonical entities.

Draft entities are reviewable intermediate artifacts. They are not final entities and must not be written to `entities.json`.

## Pipeline Position

The local-real path must remain staged:

```text
CSV adapter -> imported SourceRecords -> normalization evidence -> candidate validation -> draft entity expectations -> draft entity output -> draft entity validation -> future canonical entity decision
```

## Expectation Fixture

The expectation fixture lives at:

```text
examples/order-graph/local-real/draft-entity-expectations.json
```

The fixture defines required fields, allowed use, prohibited actions, and unresolved handling.

## Draft Output

The local-real imported build path may write draft entities to:

```text
outputs/order-graph/local-real/draft-entities.json
```

This artifact must be separate from canonical graph outputs. It must not be named `entities.json`, and it must not approve final identity resolution.

## What Draft Entities May Do

Draft entities may:

- Reference a validated account identity candidate.
- Preserve normalized domain identity basis.
- Preserve source record identifiers.
- Preserve candidate evidence.
- Mark status as draft.
- Serve as future human review or future canonical entity input.

## What Draft Entities Must Not Do

Draft entities must not:

- Become canonical entities.
- Write `entities.json`.
- Merge by account name alone.
- Guess missing domains.
- Convert unresolved candidates into draft entities.
- Attach signals.
- Compute entity states.
- Generate recommendations.
- Create human review records.

## Failure Modes

The boundary fails if:

- A draft entity omits its source candidate.
- A draft entity lacks normalized domain identity basis.
- An unresolved candidate becomes a draft entity.
- A draft entity is treated as canonical.
- `entities.json` is written for local-real imported records.
- Account-name-only matching creates a draft entity.

## Future Considerations

The next likely PR is `Add local-real draft entity validation`.

That PR may validate the draft entity artifact against local expectations. It must still avoid canonical entity creation, `entities.json`, signal linking, entity states, recommendations, human review records, UI, agents, LLM calls, live integrations, CRM writes, databases, package changes, or deployment work.
