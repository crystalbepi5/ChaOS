# Order Graph Local Engine

## Why This File Exists

This file documents the first local-only implementation skeleton for the Order Graph reference implementation track.

The skeleton exists because ChaOS has now defined Order Graph contracts, fake GTM fixtures, and validation checks. The next controlled step is to prove that fixture input can become deterministic local output without introducing real integrations, databases, UI, autonomous agents, LLM validation, or hidden business logic.

This file explains what the skeleton does, what it must not do, how to run it, and how it fits into the gated build path.

## Purpose

The purpose of the local engine skeleton is simple:

```text
Read fixtures. Write outputs. Do not get fancy.
```

The skeleton proves only this spine:

```text
local fake GTM fixture files -> deterministic local output files
```

It does not prove real identity resolution, real signal attachment, or real entity state computation.

## How This Fits Into ChaOS

ChaOS must remain documentation-first and human-inspectable. This skeleton is allowed only because prior Order Graph documents established a controlled implementation boundary.

This skeleton follows:

- `docs/decision-records/0001-order-graph-reference-implementation.md`
- `docs/order-graph/overview.md`
- `docs/order-graph/contracts.md`
- `docs/order-graph/testing-gates.md`
- `docs/order-graph/validation-checks.md`
- `docs/order-graph/technical-requirements-and-development-roadmap.md`

This skeleton prepares for Gate 3 and Gate 4, but it does not attempt to pass them.

Gate 3 requires signal attachment to be correct without duplication. Gate 4 requires entity state to be explainable. This skeleton creates the local file movement needed for later PRs to test those behaviors.

## What The Skeleton Does

The skeleton reads fake GTM fixture files from:

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

For this milestone, the builder projects expected fixture files into output files. That projection is intentional. It proves the local input/output boundary before future PRs add real deterministic graph logic.

## What The Skeleton Must Not Do

The skeleton must not implement real identity resolution.

It must not decide that two accounts match.

It must not decide that two contacts match.

It must not attach signals through new logic.

It must not compute entity state.

It must not call external APIs.

It must not call an LLM.

It must not use a database.

It must not require credentials.

It must not mutate fixture input files.

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

This file contains a skeleton projection of `expected-entities.json`.

It includes canonical entities, unresolved source records, and explicit non-merge examples. It also includes a warning that no identity resolution was performed.

### `signal-links.json`

This file contains a skeleton projection of `expected-signal-links.json`.

It includes expected signal links and no-duplicate signal expectations. It also includes a warning that no signal attachment logic was performed.

### `entity-states.json`

This file contains a skeleton projection of `expected-entity-states.json`.

It includes expected entity states, the top-10 fixture preview, and state guardrails. It also includes a warning that no entity state computation was performed.

### `build-summary.json`

This file summarizes the run.

It includes:

- Builder mode.
- Source record count.
- Signal count.
- Expected entity count.
- Expected signal link count.
- Expected entity state count.
- Unresolved record count.
- Input directory.
- Output directory.
- Output files.
- Warnings.

## Why This Exists Before Real Logic

The Order Graph must prove its local spine before it adds graph intelligence.

A small deterministic skeleton removes ambiguity about:

- Which fixture files are inputs.
- Which output files future logic must produce.
- Where local outputs belong.
- How summaries are reported.
- Which implementation boundaries remain prohibited.

This makes future changes easier to review because later PRs can focus on one behavior at a time.

## Examples Of Use

A reviewer may run the builder and confirm that:

- The command reads only local fake fixture files.
- The command creates `outputs/order-graph/gtm/` when needed.
- The command writes stable JSON files.
- The output files preserve expected unresolved cases.
- The output files preserve expected signal-link examples.
- The output files preserve expected entity-state guardrails.
- The build summary clearly states `builder_mode: skeleton`.

A reviewer must reject the change if the skeleton starts making real matching decisions, calling external systems, hiding logic, or acting like a production graph engine.

## Future Considerations

Future PRs may add real deterministic behavior in small steps after review gates allow it.

The next likely PR is `Add identity resolution logic`.

That future PR must remain local-only and deterministic. It must prove account and contact resolution behavior against fake fixtures without production matching, fuzzy black-box logic, external enrichment, databases, LLMs, UI, autonomous agents, or real integrations.

Later PRs may add:

- Deterministic signal attachment logic.
- Duplicate-signal checks.
- Explainable entity state computation.
- Local validation reports.
- Additional fixture cases.

Each future PR must preserve traceability, inspectability, and the gated Order Graph build sequence.
