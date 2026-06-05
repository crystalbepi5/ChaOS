# Order Graph Local Engine

## Why This File Exists

This file documents the local-only implementation track for the Order Graph reference implementation.

The local engine exists because ChaOS has defined Order Graph contracts, fake GTM fixtures, validation checks, and a controlled implementation boundary. The engine must prove one small deterministic behavior at a time without introducing real integrations, databases, UI, autonomous agents, LLM validation, or hidden business logic.

This file explains what the local engine does, what it must not do, how to run it, and how it fits into the gated build path.

## Purpose

The purpose of the local engine is simple:

```text
Read fixtures. Resolve only strong evidence. Attach signals through links. Compute explainable state. Validate locally. Do not get fancy.
```

The current engine proves this spine:

```text
local fake GTM fixture files -> deterministic identity resolution -> deterministic signal attachment -> explainable entity state -> local validation report -> local output files
```

It now performs first-pass identity resolution for source records with strong keys, first-pass signal attachment from local signal evidence, first-pass entity state computation from generated graph outputs, and a local validation report over the generated outputs.

## How This Fits Into ChaOS

ChaOS must remain documentation-first and human-inspectable. This local engine is allowed only because prior Order Graph documents established a controlled implementation boundary.

This engine follows:

- `docs/decision-records/0001-order-graph-reference-implementation.md`
- `docs/order-graph/overview.md`
- `docs/order-graph/contracts.md`
- `docs/order-graph/testing-gates.md`
- `docs/order-graph/validation-checks.md`
- `docs/order-graph/technical-requirements-and-development-roadmap.md`

This validation-report step collects local evidence before Gate 5 workflow work begins.

## What The Engine Does

The engine reads fake GTM fixture files from:

```text
examples/order-graph/gtm/
```

It reads:

- `source-records.json`
- `signals.json`

It must not read `expected-signal-links.json` to produce output links. That fixture may remain available as a human review reference, but `signal-links.json` must be generated from `signals.json`, resolved entities, and explicit local source-record evidence.

It must not read `expected-entity-states.json` to produce output states. That fixture may remain available as a human review reference, but `entity-states.json` must be generated from generated entities, generated signal links, signals, and source records.

It writes deterministic local output files to:

```text
outputs/order-graph/gtm/
```

It writes:

- `entities.json`
- `signal-links.json`
- `entity-states.json`
- `validation-report.json`
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

## Entity State Rules

Entity states must explain themselves from visible local evidence.

The current state computation uses deterministic rule labels instead of numeric scores.

The state computation may use:

- Generated Account entities.
- Generated signal links.
- Signal fixture fields.
- Source-record traceability.
- Unresolved source-record cases.

The state computation must not use `expected-entity-states.json` as implementation input.

State labels must preserve the difference between supporting evidence, non-supporting evidence, missing evidence, and unresolved identity.

Unlinked signals must not support entity state until structured entity evidence exists.

Stale or low-confidence signals may remain traceable without raising priority.

## Local Validation Report Rules

The validation report must validate generated outputs only.

The validation report may check:

- Generated signal links reference generated entities.
- Signal link tuples are unique.
- The email reply signal attaches to multiple entities through links.
- The meeting signal remains unlinked until structured entity evidence exists.
- Entity states reference generated entities or preserve unresolved identity.
- Entity state explanation inputs reference local signals and generated links.
- Entity states do not use numeric scores.
- Stale or low-confidence signals do not drive high-priority state.
- Expected fixture projection keys are absent from generated state output.

The validation report must not call external systems, use LLM judgment, introduce hidden scoring, rank accounts, recommend actions beyond existing state text, or imply production readiness.

## Signal Attachment Rules

Signals live once and attach through generated links. Views must use links instead of duplicating signal objects.

Signal attachment uses only explicit local fixture evidence:

- Signal source-record references.
- Generated entity source-record mappings.
- Canonical domains present in source records and entities.
- Normalized contact emails present in source records and entities.
- Source-native sequence evidence present in source records and entities.

A single signal may generate multiple links when the roles are explicit. For example, an email reply may attach to a Contact as actor, an Account as parent account, and a Sequence as source workflow.

Duplicate links must be prevented by the stable tuple:

```text
signal_id + entity_id + relationship_role
```

Signals with missing or unresolved entity evidence must preserve uncertainty instead of inventing links.

Meeting signals that reference only an outcome fixture path must remain unlinked until the fixture supplies structured entity evidence.

## What The Engine Must Not Do

The engine must not use fuzzy matching.

It must not infer identity from name similarity alone.

It must not enrich records from external sources.

It must not call external APIs.

It must not call an LLM.

It must not use a database.

It must not require credentials.

It must not mutate fixture input files.

It must not compute entity state with hidden numeric scoring or hidden weighting.

It must not validate outputs with hidden judgment or external systems.

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

This file contains generated signal links from `signals.json`, generated entities, and local source-record evidence.

It includes generated signal links, unlinked signal notes when applicable, storage model principles, and warnings.

### `entity-states.json`

This file contains generated entity state computation output.

It includes computed entity states, visible state rules, ranked state preview, preserved unlinked signals, and warnings.

### `validation-report.json`

This file contains deterministic local validation results for generated entities, signal links, and entity states.

It includes pass or fail status, check count, failed check count, individual check results, observed evidence, and warnings.

### `build-summary.json`

This file summarizes the run.

It includes:

- Builder mode.
- Source record count.
- Signal count.
- Resolved entity count.
- Unresolved record count.
- Generated signal link count.
- Generated entity state count.
- Validation check count.
- Failed validation check count.
- Input directory.
- Output directory.
- Output files.
- Warnings.

## Why This Exists Before More Logic

The Order Graph must prove identity, signal attachment, and explainable entity state behavior before it adds recommendations, agents, UI, or integrations.

A small deterministic local engine removes ambiguity about:

- Which source records can safely merge.
- Which records must remain separate.
- Which weak matches must remain unresolved.
- Which signals can attach to which generated entities.
- Which signals must remain single source objects.
- Which states are supported by generated links and fixture evidence.
- Which states preserve missing or weak evidence.
- Which generated outputs pass local validation checks.
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
- Signal links are generated without duplicating signal objects.
- A single signal can attach to multiple entities through explicit roles when structured evidence exists.
- The meeting signal remains unlinked because no outcome-to-entity fixture exists yet.
- Entity states are generated without reading `expected-entity-states.json`.
- Entity states use visible rule labels instead of numeric scores.
- The validation report passes with zero failed checks.
- The build summary clearly states `builder_mode: entity_state_computation`.

A reviewer must reject the change if the resolver guesses weak matches, if signal attachment duplicates signal objects, if entity state uses hidden scoring, if validation relies on hidden judgment, if the engine calls external systems, if logic is hidden, or if it acts like a production graph engine.

## Future Considerations

Future PRs may add real deterministic behavior in small steps after review gates allow it.

The next likely PR is `Add top-10 account workflow`.

That future PR must remain local-only and deterministic. It must produce recommendations from generated entity states and local validation evidence without automatic outreach, CRM writes, UI, agents, integrations, or hidden ranking logic.

Later PRs may add:

- Top-10 recommendation output.
- Additional fixture cases.

Each future PR must preserve traceability, inspectability, and the gated Order Graph build sequence.
