# Local Real Export Examples

## Why This Folder Exists

This folder defines the approved committed example location for fake-but-real-shaped local export fixtures.

It exists so future import adapter work has a concrete folder shape to obey before any adapter reads CSV or JSON export files.

## Purpose

The purpose of this folder is to separate safe committed examples from uncommitted local real exports.

Committed files in this folder must be fake or safely sanitized. Real customer exports must not be committed here.

## Approved Shape

Future fake-but-real-shaped examples may use:

```text
examples/order-graph/local-real/
  README.md
  exports/
    README.md
  expected-source-records.json
```

The `exports/` folder is reserved for future sanitized sample CSV or JSON exports. It is intentionally empty except for its README in this PR.

## What May Be Added Later

Future PRs may add small fake-but-real-shaped export fixtures such as:

- Account or company exports.
- Person or contact exports.
- Activity or signal exports.
- Opportunity or commercial object exports.
- Expected SourceRecord output for adapter tests.

Those future fixtures must preserve messy data shape without preserving private content.

## What Must Not Be Added

This folder must not contain:

- Real customer data.
- Production exports.
- Credentials.
- Tokens.
- API keys.
- Private notes.
- Sensitive free text.
- Import scripts.
- Live integration configuration.
- Generated outputs from unreviewed real exports.

## Relationship To Configs

Mapping and classification examples belong under:

```text
configs/order-graph/local-real/
```

The example configs define how future adapters should interpret local export shape. They do not execute imports.

## Review Checklist

Before adding any future fixture file here, a reviewer must confirm:

- The data is fake or safely sanitized.
- Required fields are present or missing fields are intentional test cases.
- Restricted values are absent.
- Excluded values are absent.
- Unknown fields are safe by name and do not include sensitive values.
- The fixture remains small enough for human review.
- The fixture does not imply live ingestion or production readiness.
