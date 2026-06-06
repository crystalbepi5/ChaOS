# Local Import Adapter Skeleton

## Why This File Exists

This file documents the first local CSV-to-SourceRecord adapter skeleton and the first local builder handoff for imported SourceRecords.

The adapter exists only to prove that local fake or sanitized CSV exports can be transformed into adapter-shaped JSON outputs under visible mapping and classification rules.

The builder handoff exists only to prove that adapter-shaped SourceRecords can be consumed by the existing local builder entry point without pretending they are a complete graph fixture.

It does not approve real customer data ingestion, live integrations, production exports, CRM writes, outreach actions, UI, agents, LLM classification, graph expansion from imported records, or deployment work.

## Purpose

The purpose of the adapter skeleton is:

```text
Read local CSV. Read mapping and classification files. Write SourceRecord-shaped output, import summary, and mapping warnings.
```

The purpose of the imported SourceRecord build handoff is:

```text
Read local adapter-shaped SourceRecords. Write a deterministic SourceRecord handoff output and build summary.
```

Both paths must remain deterministic and inspectable.

## Inputs

The adapter requires:

- A local fake or sanitized CSV export.
- A local field mapping JSON file.
- A local field classification JSON file.
- A local output directory.

The imported SourceRecord build handoff requires:

- A local fake or sanitized adapter output file named `expected-source-records.json`.
- A local output directory.

Neither path must read from live APIs, databases, SaaS tools, credentials, or production systems.

## Outputs

The adapter writes:

```text
source-records.json
import-summary.json
mapping-warnings.json
```

The imported SourceRecord build handoff writes:

```text
source-records.json
build-summary.json
```

`source-records.json` contains SourceRecord-shaped objects.

`import-summary.json` contains deterministic counts, input paths, output paths, warning types, and boundaries.

`mapping-warnings.json` contains safe warning records.

`build-summary.json` names the local handoff mode, counts the imported SourceRecords, and states that graph expansion has not run.

Warnings may include safe field names. Warnings must not include restricted, excluded, or unknown field values.

## Field Handling Rules

The adapter may ingest a field value only when:

- The field has a classification.
- The classification is not `restricted`, `excluded`, or `unknown_needs_review`.
- The review status is `approved_for_local_ingestion`.
- The field has a mapping target.

The adapter must not ingest:

- Restricted field values.
- Excluded field values.
- Unknown field values.
- Unclassified field values.
- Fields blocked pending review.

Excluded field names may appear in warnings only when safe. Excluded field values must never appear in SourceRecords or warning output.

## How To Run

Future reviewers may run the adapter with a fake or sanitized local CSV:

```powershell
python -m src.order_graph.import_exports --csv <local-csv> --mapping <mapping-json> --classification <classification-json> --output <output-dir>
```

Future reviewers may run the imported SourceRecord build handoff against the local-real fixture:

```powershell
python -m src.order_graph.build_graph --input examples/order-graph/local-real --output outputs/order-graph/local-real --mode imported-source-records
```

The command writes only imported SourceRecord handoff output and a build summary. It must not generate entities, signal links, entity states, validation reports, recommendations, human review records, or feedback validation records for the local-real fixture.

The command uses only the Python standard library.

## What This Does Not Approve

This adapter skeleton and build handoff do not approve:

- Real customer data committed to the repository.
- Salesforce API access.
- Live integrations.
- Production exports.
- Credential handling.
- LLM field classification.
- Agent review.
- UI.
- CRM writes.
- Outreach actions.
- Graph expansion from imported SourceRecords.
- Deployment.

## Future Considerations

The next likely PR is `Add local-real identity normalization fixture`.

That PR may decide how imported domain values such as `acme.example` and `https://www.acme.example` are normalized before identity resolution. It must preserve the current adapter boundary: mapping may preserve imported values exactly, and identity normalization must be a separate visible decision.
