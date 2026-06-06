# Local Import Adapter Skeleton

## Why This File Exists

This file documents the first local CSV-to-SourceRecord adapter skeleton.

The adapter exists only to prove that local fake or sanitized CSV exports can be transformed into adapter-shaped JSON outputs under visible mapping and classification rules.

It does not approve real customer data ingestion, live integrations, production exports, CRM writes, outreach actions, UI, agents, LLM classification, or deployment work.

## Purpose

The purpose of the adapter skeleton is:

```text
Read local CSV. Read mapping and classification files. Write SourceRecord-shaped output, import summary, and mapping warnings.
```

The adapter must remain deterministic and inspectable.

## Inputs

The adapter requires:

- A local fake or sanitized CSV export.
- A local field mapping JSON file.
- A local field classification JSON file.
- A local output directory.

The adapter must not read from live APIs, databases, SaaS tools, credentials, or production systems.

## Outputs

The adapter writes:

```text
source-records.json
import-summary.json
mapping-warnings.json
```

`source-records.json` contains SourceRecord-shaped objects.

`import-summary.json` contains deterministic counts, input paths, output paths, warning types, and boundaries.

`mapping-warnings.json` contains safe warning records.

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

The command uses only the Python standard library.

## What This Does Not Approve

This adapter skeleton does not approve:

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
- Deployment.

## Future Considerations

The next likely PR is `Add local real-export smoke fixture`.

That PR may add fake-but-real-shaped CSV fixtures and expected SourceRecord output. It must not add real customer data or live integrations.
