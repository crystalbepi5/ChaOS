# Account Plan Tracker Architecture Starter Package

## Why This File Exists

This file applies ChaOS v0.1 to Account Plan Tracker at MVP level.

The proof gate needs to determine whether ChaOS can turn a fuzzy build idea into an implementation-ready scope faster than starting from scratch.

## Purpose

The purpose of this starter package is to define the smallest useful Account Plan Tracker architecture without adding implementation code, integrations, agents, UI, or deployment work.

## MVP Scope

Account Plan Tracker should help a user create and review account plans that identify account context, planning gaps, current state, recommended next actions, owners, outcomes, and feedback.

The MVP should not become a CRM. It should not write to Salesforce, send outreach, run agents, or claim automated prioritization authority.

## Core Semantic Model

```text
Entity -> Signal -> State -> Decision -> Outcome -> Feedback
```

## Entities

| Entity | Meaning | MVP Notes |
| --- | --- | --- |
| Account | Company or organization being planned. | Primary entity. |
| Contact/persona | Person, role, or buying persona connected to an account. | May be lightweight in MVP. |
| Signal | Observed account activity, context, or gap. | Must remain separate from state. |
| Account plan | Structured plan for one account. | Main artifact. |
| Play | Recommended approach or GTM motion. | Must be human-reviewable. |
| Action item | Next step assigned to a person. | Must not execute automatically. |
| Owner | Human responsible for an action or account. | May be a text field in MVP. |
| Review | Human assessment of plan quality or next action. | Feeds feedback. |

## Signals

Possible MVP signals include:

- Intent signal.
- Recent activity.
- Persona gap.
- Stale account.
- Open opportunity.
- Executive change.
- Event attendance.
- Prior meeting.
- No recent touch.

Signals must be treated as evidence, not decisions.

## States

Possible MVP states include:

- `account_needs_research`
- `account_ready_for_outreach`
- `account_has_persona_gap`
- `account_has_stale_activity`
- `account_has_active_opportunity`
- `account_blocked_needs_review`
- `account_plan_ready`

State must describe the current interpreted condition of the account. State must not silently trigger action.

## Decisions

Possible MVP decisions include:

- Prioritize account.
- Assign next action.
- Request missing context.
- Suppress account.
- Route to human review.
- Recommend play.

Decisions must be traceable to account context, signals, and state.

## Outcomes

Possible MVP outcomes include:

- Meeting booked.
- Reply received.
- Account disqualified.
- Plan accepted.
- Plan revised.
- Action completed.

Outcomes must record what happened after review or action.

## Feedback

Possible MVP feedback includes:

- Rep accepted recommendation.
- Rep rejected recommendation.
- Meeting quality.
- Outcome after action.
- Stale signal ignored.
- Play worked or did not work.

Feedback must change future plan quality, recommendation confidence, or pattern judgment.

## Initial Workflow Model

```text
Trigger -> Input -> Processing -> Decision -> Action -> Feedback
```

| Stage | MVP Definition |
| --- | --- |
| Trigger | User starts or reviews an account plan. |
| Input | Account name, segment, target personas, known signals, open opportunities, recent activity, owner, and gaps. |
| Processing | Organize input into entities, signals, state, missing context, and possible plays. |
| Decision | Recommend account readiness, next action, or human review. |
| Action | Record a proposed next step or plan update. Do not send outreach or write to CRM. |
| Feedback | Capture whether the user accepted, revised, rejected, or completed the recommendation. |

## MVP Output Shape

A useful first Account Plan Tracker build prompt should be able to produce:

- Account summary.
- Known account context.
- Missing context.
- Signal list.
- Current account state.
- Recommended play or next action.
- Owner.
- Review status.
- Outcome and feedback fields.

## Guardrails

The MVP must not:

- Become a full CRM.
- Write to Salesforce, Outreach, or any external system.
- Use real customer data.
- Send outreach.
- Add autonomous agents.
- Use hidden scoring.
- Treat state as final decision.
- Treat recommendation as permission to act.

## Implementation-Ready Scope Candidate

A future implementation PR may build a small local artifact that lets a user create and review account plans with fake or manually entered data.

The first build should prioritize inspectability over automation. It should make account planning clearer before it tries to make account planning smarter.

## Open Questions For Build Prompt

- Should the first implementation be a static HTML prototype, local web app, or Markdown/spreadsheet-style artifact?
- Which five account fields are required for the first useful plan?
- Should next actions be selected from a fixed list or written manually?
- Should account state be manually selected, rule-assisted, or deferred?
- What does the first user need to export or share?
