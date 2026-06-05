# Order Graph Local Engine

## Why This File Exists

This file documents the local-only implementation track for the Order Graph reference implementation.

The local engine exists because ChaOS has defined Order Graph contracts, fake GTM fixtures, validation checks, and a controlled implementation boundary. The engine must prove one small deterministic behavior at a time without introducing real integrations, databases, UI, autonomous agents, LLM validation, or hidden business logic.

This file explains what the local engine does, what it must not do, how to run it, and how it fits into the gated build path.

## Purpose

The purpose of the local engine is simple:

```text
Read fixtures. Resolve only strong evidence. Attach signals through links. Do not get fancy.
```

The current engine proves this spine:

```text
local fake GTM fixture files -> deterministic identity resolution -> deterministic signal attachment -> local output files
```

It now performs first-pass identity resolution for source records with strong keys and first-pass signal attachment from local signal evidence. It still does not perform entity state computation.

## How This Fits Into ChaOS

ChaOS must remain documentation-first and human-inspectable. This local engine is allowed only because prior Order Graph documents established a controlled implementation boundary.

This engine follows:

- `docs/decision-records/0001-order-graph-reference-implementation.md`
- `docs/order-graph/overview.md`
- `docs/order-graph/contracts.md`
- `docs/order-graph/testing-gates.md`
- `docs/order-graph/validation-checks.md`
- `docs/order-graph/technical-requirements-and-development-roadmap.md`

This signal-attachment step prepares and partially proves Gate 3. It does not attempt to pass Gate 4.

## What The Engine Does

The engine reads fake GTM fixture files from:

```text
examples/order-graph/gtm/
```

It reads:

- `source-records.json`
- `signals.json`
- `expected-entities.json`
- `expected-entity-states.json`

It must not read `expected-signal-links.json` to produce output links. That fixture may remain available as a human review reference, but `signal-links.json` must be generated from `signals.json`, resolved entities, and explicit local source-record evidence.

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

## What Still Uses Fixture Projection

Entity states still project from `expected-entity-states.json`.

That projection remains intentional until a later PR adds explainable entity state logic.

## What The Engine Must Not Do

The engine must not use fuzzy matching.

It must not infer identity from name similarity alone.

It must not enrich records from external sources.

It must not call external APIs.

It must not call an LLM.

It must not use a database.

It must not require credentials.

It must not mutate fixture input files.

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

This file contains generated signal links from `signals.json`, generated entities, and local source-record evidence.

It includes generated signal links, unlinked signal notes when applicable, storage model principles, and warnings.

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
- Generated signal link count.
- Expected entity state count.
- Input directory.
- Output directory.
- Output files.
- Warnings.

## Why This Exists Before More Logic

The Order Graph must prove identity and signal attachment behavior before it adds state computation, recommendations, agents, UI, or integrations.

A small deterministic local engine removes ambiguity about:

- Which source records can safely merge.
- Which records must remain separate.
- Which weak matches must remain unresolved.
- Which signals can attach to which generated entities.
- Which signals must remain single source objects.
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
- The build summary clearly states `builder_mode: signal_attachment`.

A reviewer must reject the change if the resolver guesses weak matches, if signal attachment duplicates signal objects, if the engine calls external systems, if logic is hidden, or if it acts like a production graph engine.

## Future Considerations

Future PRs may add real deterministic behavior in small steps after review gates allow it.

The next likely PR is `Add entity state computation`.

That future PR must remain local-only and deterministic. It must compute state from generated entities, generated signal links, and local fixture evidence without hidden scoring, external enrichment, LLM reasoning, UI, agents, or integrations.

Later PRs may add:

- Explainable entity state computation.
- Local validation reports.
- Additional fixture cases.

Each future PR must preserve traceability, inspectability, and the gated Order Graph build sequence.
