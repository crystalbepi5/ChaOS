# Account Plan Tracker Static Prototype

## Why This Exists

This static prototype is an implementation proof artifact for the ChaOS v0.1 Account Plan Tracker proof gate.

It tests whether the proof-gate architecture can become a working, reviewable product artifact without adding frameworks, integrations, agents, persistence, or production machinery.

## How To Open Locally

Open this file in a browser:

```text
examples/proof-gates/account-plan-tracker/static-prototype/index.html
```

No install step is required. No package manager is required. No local server is required.

## Product Language Decision

ChaOS structures the prototype internally, but the user interface uses account-planning language. A BDR or manager should not need to understand ChaOS primitives to use the tool.

The visible UI intentionally uses labels such as:

- Account Snapshot
- Why This Account
- Plan Status
- Buying Signals
- Gaps / Blockers
- Recommended Next Step
- Action Plan
- Progress
- Review Notes
- Results / Learning

The UI intentionally avoids framework-facing labels such as Entity, Signal, State, Decision, Outcome, and Feedback.

This tests whether ChaOS can improve product structure without leaking abstraction tax into the product experience.

## What This Prototype Is Testing

This prototype tests whether Account Plan Tracker becomes easier to understand when the app experience is organized around account planning while the underlying proof remains structured by the ChaOS semantic model:

```text
Entity -> Signal -> State -> Decision -> Outcome -> Feedback
```

The prototype lets a reviewer:

- Select a fake account.
- Review account snapshot details.
- Inspect buying signals.
- See plan status.
- Review gaps and blockers.
- Review a human-reviewable recommended next step.
- Track local account-plan actions after review.
- Change action progress locally in the browser.
- Add a local action with owner, timing, progress, and note.
- Change review status locally in the browser.
- Add or edit results and review notes locally in the browser.
- See summary counts and selected-account progress update in memory.

## Action Tracking Loop

The action tracking loop exists to test account-plan execution without turning the prototype into an automation system.

The loop is:

```text
Reviewed recommendation -> Human-owned action -> Local progress update -> Results/review note
```

Actions may be marked:

- `planned`
- `in_progress`
- `blocked`
- `completed`
- `deferred`

Actions are execution records, not automated tasks. They must not send outreach, write to CRM, trigger integrations, or claim that the system performed the work.

## How It Maps To The Proof Gate

This prototype is part of the practical two-week proof gate. It turns the Account Plan Tracker starter package into a local artifact that can be evaluated by a human.

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

Recommended next steps are framed as human-reviewable. Plan status must not silently become action. Actions must remain human-owned local tracking records.

## Proof Gate Questions

During review, answer:

- Did this make Account Plan Tracker easier to understand?
- Did ChaOS help structure the build without appearing in the product language?
- Did the account-planning labels reduce friction compared with framework labels?
- Did action tracking make the prototype feel closer to real account-plan execution?
- Did the local action loop preserve the boundary between recommendation and action?
- Is the prototype useful enough to iterate?
- What felt like abstraction tax?
- What should be simplified before the next PR?

## What Should Be Evaluated

Reviewers should evaluate:

- Whether the prototype makes account planning clearer.
- Whether plan statuses are useful or too abstract.
- Whether buying signals, gaps, recommendation, action tracking, results, and review notes are clearly separated.
- Whether action progress is enough for a first execution loop.
- Whether the first implementation should remain static, become a local app, or become a simpler document/spreadsheet artifact.
- Whether the prototype is useful enough to become the next Codex build prompt.

## Current Status

Status: `implementation_proof_started_not_concluded`

This prototype continues implementation proof. It does not conclude the ChaOS proof gate.
