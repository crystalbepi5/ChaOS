# Order Graph Local Engine

## Why This File Exists

This file documents the local-only implementation track for the Order Graph reference implementation.

The local engine exists because ChaOS has defined Order Graph contracts, fake GTM fixtures, validation checks, and a controlled implementation boundary. The engine must prove one small deterministic behavior at a time without introducing real integrations, databases, UI, autonomous agents, LLM validation, or hidden business logic.

This file explains what the local engine does, what it must not do, how to run it, and how it fits into the gated build path.

## Purpose

The purpose of the local engine is simple:

```text
Read fixtures. Resolve only strong evidence. Write outputs. Do not get fancy.
```

The current engine proves this spine:

```text
local fake GTM fixture files -> deterministic identity resolution -> local output files
```

It now performs first-pass identity resolution for source records with strong keys. It still does not perform signal attachment logic or entity state computation.

## How This Fits Into ChaOS

ChaOS must remain documentation-first and human-inspectable. This local engine is allowed only because prior Order Graph documents established a controlled implementation boundary.

This engine follows:

- `docs/decision-records/0001-order-graph-reference-implementation.md`
- `docs/order-graph/overview.md`
- `docs/order-graph/contracts.md`
- `docs/order-graph/testing-gates.md`
- `docs/order-graph/validation-checks.md`
- `docs/order-graph/technical-requirements-and-development-roadmap.md`

This identity-resolution step supports Gate 2 evidence and prepares for Gate 3. It does not attempt to pass Gate 3 or Gate 4.

## What The Engine Does

The engine reads fake GTM fixture files from:

```text
examples/order-graph/gtm/
```

It reads:

- `source-records.json`
- `signals.json`
- `expected-entities.json`
- `expected-signal-links.json`
- `expected-entity-states.json`

It writes deterministic local output files to:

```text
outputs/order-graph/gtm/
```

It writes:

- `entities.json`
- `signal-links.json`
- `entity-states.json`
- `build-summary.json`

## Identity Resolution Rules

The current identity resolver uses only strong deterministic fixture evidence.

Account-like records resolve when they have the same canonical domain.

Contact-like records resolve when they have the same normalized email.

Sequence records resolve by source-native identity.

Account entity identifiers use fixture-compatible canonical-domain slugs so generated entities remain coherent with projected signal-link and entity-state references.

Account-like records with no canonical domain remain unresolved unless another future approved strong key exists.

Same-name people with different emails or company domains must not merge.

Similar account names with different canonical domains must not merge.

Similar account names with missing domains must remain unresolved.

The resolver must preserve unresolved cases as valid graph output. It must not treat uncertainty as failure.

## What Still Uses Fixture Projection

Signal links still project from `expected-signal-links.json`.

Entity states still project from `expected-entity-states.json`.

Those projections remain intentional until later PRs add deterministic signal attachment and explainable state logic.

## What The Engine Must Not Do

The engine must not use fuzzy matching.

It must not infer identity from name similarity alone.

It must not enrich records from external sources.

It must not call external APIs.

It must not call an LLM.

It must not use a database.

It must not require credentials.

It must not mutate fixture input files.

It must not attach signals through new logic yet.

It must not compute entity state yet.

It must not create UI, agents, deployment configuration, real integrations, or production behavior.

## How To Run It

From the repository root, run:

```powershell
python -m src.order_graph.build_graph
```

The command prints a build summary and writes output files under:

```text
outputs/order-graph/gtm/
```

The command uses only the Python standard library.

## Output Files

### `entities.json`

This file contains generated identity-resolution output from `source-records.json`.

It includes canonical entities, unresolved source records, and explicit non-merge examples.

### `signal-links.json`

This file contains a projection of `expected-signal-links.json`.

It includes expected signal links and no-duplicate signal expectations. It also includes a warning that no signal attachment logic was performed.

### `entity-states.json`

This file contains a projection of `expected-entity-states.json`.

It includes expected entity states, the top-10 fixture preview, and state guardrails. It also includes a warning that no entity state computation was performed.

### `build-summary.json`

This file summarizes the run.

It includes:

- Builder mode.
- Source record count.
- Signal count.
- Resolved entity count.
- Unresolved record count.
- Expected signal link count.
- Expected entity state count.
- Input directory.
- Output directory.
- Output files.
- Warnings.

## Why This Exists Before More Logic

The Order Graph must prove identity behavior before it adds signal attachment, state computation, recommendations, agents, UI, or integrations.

A small deterministic identity resolver removes ambiguity about:

- Which source records can safely merge.
- Which records must remain separate.
- Which weak matches must remain unresolved.
- Which output files future logic must consume.
- Which implementation boundaries remain prohibited.

This makes future changes easier to review because later PRs can focus on one behavior at a time.

## Examples Of Use

A reviewer may run the builder and confirm that:

- The command reads only local fake fixture files.
- The command creates `outputs/order-graph/gtm/` when needed.
- The command writes stable JSON files.
- Same-domain account records resolve into one Account.
- Same-email contact records resolve into one Contact.
- Same-name people at different domains remain separate.
- Similar account names with different domains remain separate.
- Missing-domain account records remain unresolved.
- The build summary clearly states `builder_mode: identity_resolution`.

A reviewer must reject the change if the resolver guesses weak matches, calls external systems, hides logic, or acts like a production graph engine.

## Future Considerations

Future PRs may add real deterministic behavior in small steps after review gates allow it.

The next likely PR is `Add signal attachment logic`.

That future PR must remain local-only and deterministic. It must prove that signals live once and attach to every relevant entity through explicit links without duplicating signal objects.

Later PRs may add:

- Duplicate-signal checks.
- Explainable entity state computation.
- Local validation reports.
- Additional fixture cases.

Each future PR must preserve traceability, inspectability, and the gated Order Graph build sequence.
