# Source Field Classification Model

## Why This File Exists

This file defines how ChaOS classifies fields from local real-shaped exports before any import adapter may ingest them.

Real business exports contain a mix of stable identifiers, useful context, source-system interpretations, sensitive fields, irrelevant fields, and fields whose meaning is unclear. If those fields are not classified before ingestion, ChaOS may treat context as truth, preserve data it should exclude, or make recommendations from unsafe evidence.

This document turns the field classes introduced in `docs/order-graph/local-real-export-inputs.md` into a reviewable contract.

## Purpose

The purpose of the source field classification model is to decide what each source field is allowed to do.

Every source field must have exactly one primary classification before it is ingested.

Classification must answer:

- Can this field support identity resolution?
- Can this field support relationship linking?
- Can this field become or support a Signal?
- Can this field explain state or recommendations as context?
- Must this field be excluded from ingestion?
- Does this field require human review before use?

## How This Fits Into ChaOS

Source field classification protects the boundary between source exports and ChaOS SourceRecords.

It supports these ChaOS laws:

- Context is a dependency. Minimize it.
- Systems must be understandable by humans first.
- Prefer inspectable systems over intelligent systems.
- Every decision must be traceable.
- Recommend before automating.

This document does not approve import scripts, live integrations, CRM writes, outreach actions, UI, agents, LLM calls, deployment, or production ingestion.

## Classification Requirements

Every local export field must include:

- Field name.
- Source system.
- Source object type.
- Primary classification.
- Allowed use.
- Prohibited use.
- Sanitization requirement.
- Review status.
- Rationale.

Field classification must happen before mapping fields into SourceRecords.

Unknown fields must remain blocked until reviewed.

Restricted and excluded fields must not be copied into generated SourceRecords.

## Field Classes

### `structured_truth`

#### Definition

`structured_truth` fields are stable, explicit fields that may be used as hard local evidence.

These fields may support identity resolution, relationship linking, signal attachment, traceability, and deterministic validation.

#### Common Examples

- Source record identifier.
- Source system name.
- Source object type.
- Domain.
- Website.
- Email address.
- Created date.
- Updated date.
- Event timestamp.
- Owner identifier.
- Account identifier.
- Contact identifier.
- Opportunity identifier.
- Sequence or workflow identifier.

#### Allowed Uses

`structured_truth` fields may:

- Identify a SourceRecord.
- Link records through explicit source identifiers.
- Support canonical entity resolution when the matching rule is approved.
- Support SignalEntityLink generation.
- Support traceability.
- Support deterministic validation checks.

#### Prohibited Uses

`structured_truth` fields must not:

- Override a human review decision.
- Trigger production actions.
- Become a recommendation by themselves.
- Hide the source system that provided the value.

### `contextual_evidence`

#### Definition

`contextual_evidence` fields are human-readable or source-provided context that may explain a state or recommendation but must not be treated as hard truth.

These fields are useful for review, but they are not identity keys.

#### Common Examples

- Notes.
- Descriptions.
- Call summaries.
- Email snippets.
- Free-text next steps.
- Human-entered status comments.
- Meeting summaries.

#### Allowed Uses

`contextual_evidence` fields may:

- Explain why a recommendation deserves human review.
- Preserve uncertainty.
- Support reviewer understanding.
- Appear in sanitized summaries if approved.

#### Prohibited Uses

`contextual_evidence` fields must not:

- Create identity matches.
- Merge entities.
- Establish source relationships by themselves.
- Drive high-priority state without structured supporting evidence.
- Be ingested when sensitive or unreviewed.

### `derived_signal`

#### Definition

`derived_signal` fields are source-system interpretations, classifications, scores, labels, or inferred statuses.

They may be useful, but they are not neutral truth. Their source and derivation risk must remain visible.

#### Common Examples

- Intent score band.
- Engagement score band.
- Health label.
- Risk label.
- Forecast category.
- Lead score.
- Fit score.
- Buying stage label.

#### Allowed Uses

`derived_signal` fields may:

- Become a Signal or support a Signal when source and time are available.
- Explain source-system interpretation.
- Support state when paired with visible source and confidence metadata.
- Remain traceable as source-derived evidence.

#### Prohibited Uses

`derived_signal` fields must not:

- Be treated as hidden authority.
- Replace ChaOS validation.
- Create autonomous actions.
- Hide source-system uncertainty.
- Produce numeric ranking without an approved explainable rule.

### `restricted`

#### Definition

`restricted` fields are fields that may exist in exports but must not be ingested into early local Order Graph outputs.

Restricted fields may sometimes be safe in a future design, but only after a reviewed handling rule exists.

#### Common Examples

- Sensitive free text.
- Private customer notes.
- Legal notes.
- HR-like fields.
- Unredacted phone numbers.
- Personal addresses.
- Internal-only commentary.
- Sensitive support descriptions.

#### Allowed Uses

`restricted` fields may:

- Be listed by field name in warnings.
- Be counted for review.
- Be routed to human classification before ingestion.

#### Prohibited Uses

`restricted` fields must not:

- Be copied into SourceRecords.
- Be copied into generated outputs.
- Be summarized by an LLM.
- Support identity resolution.
- Support entity state.
- Support recommendations.

### `excluded`

#### Definition

`excluded` fields must not be copied, transformed, summarized, preserved, or ingested.

These fields fail review if they appear in committed test data.

#### Common Examples

- Credentials.
- Tokens.
- API keys.
- Session identifiers.
- Passwords.
- Payment information.
- Social security numbers or government identifiers.
- Raw files containing unreviewed sensitive data.

#### Allowed Uses

`excluded` fields may:

- Be identified by field name in a warning.
- Cause import rejection.
- Cause fixture review failure.

#### Prohibited Uses

`excluded` fields must not:

- Be copied into any generated output.
- Be stored in SourceRecords.
- Be logged with values.
- Be summarized.
- Be transformed.
- Be used as evidence.

### `unknown_needs_review`

#### Definition

`unknown_needs_review` fields are fields whose meaning, sensitivity, or allowed use is not yet clear.

Unknown fields must stay blocked until a human reviewer classifies them.

#### Common Examples

- Vendor-specific fields with unclear names.
- Custom fields without owner explanation.
- Abbreviated fields.
- Legacy fields.
- Fields whose values look inconsistent.
- Fields added by a tool export that were not expected by the mapping.

#### Allowed Uses

`unknown_needs_review` fields may:

- Be listed by field name in mapping warnings.
- Be counted.
- Be routed to a future classification review.

#### Prohibited Uses

`unknown_needs_review` fields must not:

- Be ingested into SourceRecords.
- Be used for identity resolution.
- Be used for signal attachment.
- Be used for entity state.
- Be used for recommendations.
- Be silently ignored without a warning.

## Classification Decision Rules

A field must be classified as `structured_truth` only when:

- The field meaning is explicit.
- The field value is stable enough for deterministic use.
- The source system can be named.
- The allowed use is clear.
- The field does not contain sensitive free text.

A field must be classified as `contextual_evidence` when:

- The field is descriptive or interpretive.
- The field is useful for human understanding.
- The field is not safe as identity or relationship truth.
- The field can be sanitized without losing the test purpose.

A field must be classified as `derived_signal` when:

- The field is a source-system score, category, label, or interpretation.
- The source system is doing some inference or aggregation.
- The value may support review but must not become hidden authority.

A field must be classified as `restricted` when:

- The field may contain sensitive content.
- The field may be useful later but has no approved handling rule now.
- The field should be blocked from generated outputs while the field name remains visible for review.

A field must be classified as `excluded` when:

- The field contains or may contain secrets, credentials, payment data, government identifiers, or unreviewed highly sensitive content.
- The field should fail committed fixture review.
- The field must not be copied or transformed.

A field must be classified as `unknown_needs_review` when:

- The field cannot be confidently classified.
- The field appears unexpectedly.
- The field name is too vague to determine safe use.
- The field owner or meaning is unknown.

## Review Status Values

Every field classification must include a review status.

Allowed review statuses:

- `approved_for_local_ingestion`
- `blocked_pending_review`
- `excluded_from_ingestion`
- `approved_for_warning_only`

`structured_truth`, `contextual_evidence`, and `derived_signal` fields may be `approved_for_local_ingestion` only when their sanitization and allowed use are clear.

`restricted` fields must be `approved_for_warning_only` or `blocked_pending_review`.

`excluded` fields must be `excluded_from_ingestion`.

`unknown_needs_review` fields must be `blocked_pending_review`.

## SourceRecord Mapping Boundary

The future import adapter may map fields into SourceRecords only after classification.

SourceRecords may preserve:

- Approved `structured_truth` fields.
- Approved `contextual_evidence` fields when sanitized.
- Approved `derived_signal` fields with source and interpretation context.

SourceRecords must not preserve:

- `restricted` field values.
- `excluded` field names or values except field names in warnings when safe.
- `unknown_needs_review` field values.

## Examples Of Use

A reviewer may inspect a field classification file and ask:

- Are identity fields classified as `structured_truth`?
- Are notes and descriptions classified as `contextual_evidence` or blocked?
- Are source scores classified as `derived_signal` instead of hard truth?
- Are sensitive fields classified as `restricted` or `excluded`?
- Are unknown fields blocked until review?
- Does every field have an allowed use and prohibited use?
- Does every field name its sanitization requirement?

## Validation Expectations

A valid field classification set must:

- Classify every field exactly once.
- Use only approved field classes.
- Include review status for every field.
- Preserve rationale for every classification.
- Prohibit ingestion for restricted, excluded, and unknown fields.
- Preserve source system and object type.
- Keep structured truth separate from contextual evidence.

## Failure Modes

The field classification model fails if:

- A field has no classification.
- A field has multiple conflicting classifications.
- Free text is classified as structured truth.
- Source-system scores are treated as hidden authority.
- Restricted values are copied into outputs.
- Excluded fields are logged with values.
- Unknown fields are silently ingested.
- Review status is missing.
- The classification depends on private memory instead of visible rationale.

## What This Document Does Not Approve

This document does not approve:

- CSV import adapters.
- Mapping execution.
- Live source connections.
- Production data ingestion.
- Credential handling.
- CRM writes.
- Outreach automation.
- UI.
- Agents.
- LLM classification.
- Deployment.

## Future Considerations

The next likely PR is `Add local export folder structure and sample mapping config`.

That PR may add example configuration files and local-real folders, but it must not add real customer data, import scripts, live integrations, agents, UI, or deployment work.
