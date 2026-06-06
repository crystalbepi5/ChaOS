# Account Plan Tracker Static Prototype

## Why This Exists

This static prototype is the first implementation proof artifact for the ChaOS v0.1 Account Plan Tracker proof gate.

It tests whether the proof-gate architecture can become a working, reviewable artifact without adding frameworks, integrations, agents, or production machinery.

## How To Open Locally

Open this file in a browser:

```text
examples/proof-gates/account-plan-tracker/static-prototype/index.html
```

No install step is required. No package manager is required. No local server is required.

## What This Prototype Is Testing

This prototype tests whether Account Plan Tracker becomes easier to understand when mapped through the ChaOS semantic model:

```text
Entity -> Signal -> State -> Decision -> Outcome -> Feedback
```

The prototype lets a reviewer:

- Select a fake account.
- Review known context and missing context.
- Inspect fake signals.
- See interpreted account state.
- Review a human-reviewable recommendation.
- Track local account-plan actions after review.
- Change action status locally in the browser.
- Add a local action with owner, timing, status, and note.
- Change review status locally in the browser.
- Add or edit outcome and feedback text locally in the browser.
- See summary counts by state, review status, and action status.

## Action Tracking Loop

The action tracking loop exists to test account-plan execution without turning the prototype into an automation system.

The loop is:

```text
Reviewed recommendation -> Human-owned action -> Local status update -> Outcome/feedback note
```

Actions may be marked:

- `planned`
- `in_progress`
- `blocked`
- `completed`
- `deferred`

Actions are execution records, not automated tasks. They must not send outreach, write to CRM, trigger integrations, or claim that the system performed the work.

## How It Maps To The Proof Gate

This prototype starts the practical part of the two-week proof gate. It turns the Account Plan Tracker starter package into a local artifact that can be evaluated by a human.

The goal is not to prove the product is complete. The goal is to learn whether ChaOS helped produce a clearer first artifact faster than starting from scratch.

## Data Boundary

All sample accounts and actions are fake. The prototype uses manual sample data only.

The prototype does not use real customer data, Salesforce, Outreach, 6sense, CRM data, email data, or external APIs.

## State Boundary

The prototype uses in-memory browser state only. Local edits disappear on refresh.

The prototype does not use browser storage, files, databases, APIs, or persistence.

## Intentionally Out Of Scope

This prototype does not include:

- App code beyond static HTML, CSS, and vanilla JavaScript.
- `package.json`.
- Build tools.
- Frameworks.
- React or Next.js.
- Backend services.
- Database.
- API calls.
- Integrations.
- Agents.
- LLM calls.
- CRM writes.
- Salesforce, Outreach, or 6sense access.
- Real customer data.
- Persistence.
- Deployment configuration.

## Guardrails

The prototype must not execute outreach. It must not write to CRM. It must not claim automated prioritization authority.

Recommendations are framed as human-reviewable. State must not silently become action. Actions must remain human-owned local tracking records.

## Proof Gate Questions

During review, answer:

- Did this make Account Plan Tracker easier to understand?
- Did ChaOS help structure the build?
- Did the Entity/Signal/State/Decision/Outcome/Feedback model help or add friction?
- Did action tracking make the prototype feel closer to real account-plan execution?
- Did the local action loop preserve the boundary between recommendation and action?
- Is the prototype useful enough to iterate?
- What felt like abstraction tax?
- What should be simplified before the next PR?

## What Should Be Evaluated

Reviewers should evaluate:

- Whether the prototype makes account planning clearer.
- Whether the account states are useful or too abstract.
- Whether signals, state, recommendation, action tracking, outcome, and feedback are clearly separated.
- Whether action statuses are enough for a first execution loop.
- Whether the first implementation should remain static, become a local app, or become a simpler document/spreadsheet artifact.
- Whether the prototype is useful enough to become the next Codex build prompt.

## Current Status

Status: `implementation_proof_started_not_concluded`

This prototype starts implementation proof. It does not conclude the ChaOS proof gate.
