# Local-Real Identity Normalization

## Why This File Exists

This file defines the first local-real identity normalization expectations for the Order Graph.

The local CSV adapter now creates SourceRecord-shaped outputs. The local builder can now consume those imported SourceRecords as a handoff artifact. The next risk is whether future identity logic will normalize messy imported domain values in a visible way, or quietly blend adapter mapping, normalization, and entity merging into one hidden step.

This document prevents that drift. It separates adapter mapping, builder handoff, normalization, and future identity resolution.

## Purpose

The purpose of this document is to answer one narrow question:

```text
How must imported account domain values be normalized before they may become future identity-resolution evidence?
```

This stage implements a deterministic helper for normalization evidence only. It does not implement an identity resolver, graph expansion path, or builder output path for normalized evidence.

## How This Fits Into The Pipeline

The local-real path must remain staged:

```text
CSV adapter -> imported SourceRecords -> builder handoff -> normalization evidence -> future identity resolution
```

Each stage has a separate responsibility.

### CSV Adapter

The CSV adapter maps local fake or sanitized CSV rows into SourceRecord-shaped output.

The CSV adapter must preserve imported values exactly. It must not normalize domains for identity resolution.

### Builder Handoff

The builder handoff consumes imported SourceRecords and writes local handoff output.

The builder handoff must preserve imported values exactly. It must not merge entities, generate graph outputs, or treat normalized evidence as already approved.

### Normalization Evidence

Normalization evidence may derive a normalized domain from an imported domain value.

Normalization must be deterministic, visible, and inspectable. It must record what input value produced each normalized value.

The helper lives at:

```text
src/order_graph/local_real_identity_normalization.py
```

The helper returns derived evidence only. It must not change adapter output, change builder handoff output, merge records, create entities, attach signals, compute states, recommend actions, or create review records.

### Future Identity Resolution

Future identity resolution may use normalized domains as evidence only after normalization outputs are wired into a visible local-real artifact and reviewed.

Future identity resolution must not merge records by account name alone.

## Fixture

The expectation fixture lives at:

```text
examples/order-graph/local-real/identity-normalization-cases.json
```

The fixture covers clean and messy local-real domain values, including:

- `acme.example`
- `https://www.acme.example`
- `www.acme.example`
- `https://acme.example/`
- `HTTPS://WWW.ACME.EXAMPLE/`
- values with paths
- blank domains
- missing domains
- malformed text
- weak domain-like values without enough evidence

The fixture is human-reviewable by design. It remains the expectation source for the helper.

## What Normalization May Do

Normalization may:

- Lowercase domain evidence.
- Remove `http://` or `https://` when a valid host remains.
- Remove a leading `www.` when a valid host remains.
- Remove a trailing slash when a valid host remains.
- Ignore URL paths for identity evidence when the host is valid.
- Produce warnings when a value contains extra URL structure.
- Return `null` when the value is missing, malformed, or too weak.
- Preserve the original imported value in traceable output.

## What Normalization Must Not Do

Normalization must not:

- Change adapter raw values.
- Change imported SourceRecord handoff values.
- Guess a missing domain.
- Add a domain suffix to weak values such as `acme`.
- Treat account names as domains.
- Merge records by account name alone.
- Treat malformed text as identity truth.
- Hide warnings for malformed or weak values.
- Expand imported SourceRecords into entities in the normalization step.

## Why Mapping And Normalization Are Separate

Adapter mapping answers:

```text
What did the local export provide, and which approved SourceRecord field may hold it?
```

Identity normalization answers:

```text
What deterministic identity evidence can be derived from the imported value?
```

Those questions must stay separate because preserving imported values protects traceability. A reviewer must be able to see both the original imported value and the later normalized evidence.

If the adapter normalizes values too early, future reviewers cannot tell whether a value came from the export or from ChaOS processing. That would weaken auditability.

## Examples Of Use

A reviewer may call the helper directly from a local Python check and compare it against `identity-normalization-cases.json`.

The helper exposes:

- `normalize_local_real_domain(input_domain)`
- `normalize_local_real_domain_as_dict(input_domain)`
- `verify_identity_normalization_cases(fixture)`

A future validation PR may check that:

- Adapter output still preserves imported values exactly.
- Builder handoff output still preserves imported values exactly.
- Normalization output records derived values separately.
- Missing domains remain unresolved candidates.
- Malformed domains produce warnings or unresolved candidates.
- Account-name-only matching remains prohibited.

## Failure Modes

This normalization boundary fails if:

- Adapter output starts changing imported domain values.
- Builder handoff output starts changing imported domain values.
- Missing domains are guessed.
- Malformed values are cleaned into identities without warnings.
- Account names create identity matches without strong domain evidence.
- Normalization silently triggers entity merging.
- Graph expansion is added before local-real identity expectations are approved.

## Future Considerations

The next likely PR is `Write local-real normalization evidence output`.

That PR may wire the helper into a deterministic local output file for imported SourceRecords. It must still avoid full local-real identity resolution, signal linking, entity states, recommendations, human review records, UI, agents, LLM calls, live integrations, CRM writes, databases, package changes, or deployment work.
