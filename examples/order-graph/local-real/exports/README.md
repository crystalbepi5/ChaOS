# Local Real Export Files

## Why This Folder Exists

This folder is the future committed location for fake-but-real-shaped export files used by local import adapter tests.

It is intentionally empty in this PR. The folder shape is being established before any sample exports are added.

## Allowed Future Files

Future PRs may add small sanitized examples such as:

```text
accounts.example.csv
contacts.example.csv
activities.example.csv
opportunities.example.csv
```

File names should describe source object type, not a real customer, company, or private system.

## Required Boundary

Files in this folder must be fake or safely sanitized.

This folder must not contain real customer exports, credentials, private notes, sensitive free text, raw production downloads, or generated outputs from unreviewed real data.

## Future Adapter Boundary

Future import adapters may read from this folder only after mapping and field classification contracts are reviewed.

Adding this folder does not approve import scripts, live integrations, CRM writes, outreach actions, UI, agents, LLM calls, or deployment work.
