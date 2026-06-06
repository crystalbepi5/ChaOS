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
- Change review status locally in the browser.
- Add or edit outcome and feedback text locally in the browser.
- See summary counts by state and review status.

## How It Maps To The Proof Gate

This prototype starts the practical part of the two-week proof gate. It turns the Account Plan Tracker starter package into a local artifact that can be evaluated by a human.

The goal is not to prove the product is complete. The goal is to learn whether ChaOS helped produce a clearer first artifact faster than starting from scratch.

## Data Boundary

All sample accounts are fake. The prototype uses manual sample data only.

The prototype does not use real customer data, Salesforce, Outreach, 6sense, CRM data, email data, or external APIs.

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
- Deployment configuration.

## Guardrails

The prototype must not execute outreach. It must not write to CRM. It must not claim automated prioritization authority.

Recommendations are framed as human-reviewable. State must not silently become action.

## Proof Gate Questions

During review, answer:

- Did this make Account Plan Tracker easier to understand?
- Did ChaOS help structure the build?
- Did the Entity/Signal/State/Decision/Outcome/Feedback model help or add friction?
- Is the prototype useful enough to iterate?
- What felt like abstraction tax?
- What should be simplified before the next PR?

## What Should Be Evaluated

Reviewers should evaluate:

- Whether the prototype makes account planning clearer.
- Whether the account states are useful or too abstract.
- Whether signals, state, recommendation, outcome, and feedback are clearly separated.
- Whether the first implementation should remain static, become a local app, or become a simpler document/spreadsheet artifact.
- Whether the prototype is useful enough to become the next Codex build prompt.

## Current Status

Status: `implementation_proof_started_not_concluded`

This prototype starts implementation proof. It does not conclude the ChaOS proof gate.
