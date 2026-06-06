# Local Real Export Config Examples

## Why This Folder Exists

This folder contains non-executable example configuration artifacts for local real-shaped export work.

The configs define shape and review expectations before any import adapter is allowed to read exported data.

## Files

```text
field-classification.example.json
field-mapping.example.json
```

`field-classification.example.json` shows how source fields are classified before ingestion.

`field-mapping.example.json` shows how classified source fields may be mapped into future ChaOS SourceRecord shape.

## Boundary

These files are examples only. They must not be treated as executable import configuration.

They do not approve CSV import adapters, live source connections, production data ingestion, CRM writes, outreach actions, UI, agents, LLM calls, integrations, or deployment work.

## Review Requirements

Any future executable mapping must be reviewed separately and must prove that:

- Every source field has a classification.
- Restricted values are not ingested.
- Excluded values are not copied, transformed, summarized, logged, or preserved.
- Safe excluded field names may appear in warnings only when needed.
- SourceRecords do not include excluded field values.
- Unknown fields remain blocked pending review.
