# Account Plan Tracker ChaOS Inheritance

## Why This File Exists

This file records how Account Plan Tracker inherits ChaOS v0.1 patterns for the proof gate.

ChaOS v0.1 requires projects to declare inherited patterns, adapted patterns, bypassed patterns, and reasons for adaptation or bypass. This prevents silent framework fragmentation and makes abstraction tax visible.

## Purpose

The purpose of this document is to show which ChaOS patterns are useful for Account Plan Tracker and which patterns may need adaptation before implementation.

## Inheritance Declaration

Project: Account Plan Tracker

ChaOS pattern version inherited: v0.1

Proof status: proof_started_not_concluded

## Pattern Use Table

| Pattern | Status | Reason | Upstreaming classification |
| --- | --- | --- | --- |
| Context Sufficiency Assessment | used | The project has enough likely context to define limited MVP scope, but open questions must be named before build. | `project_specific_exception` |
| Entity/Signal/State/Decision/Outcome/Feedback | used | The model maps cleanly to account planning and next-action recommendation. | `project_specific_exception` |
| Core Workflow Model | adapted | The MVP needs one lightweight account-plan review workflow, not a full operating workflow library. | `project_specific_exception` |
| Core Agent Model | bypassed | The first proof does not require agents or autonomous assistant behavior. | `project_specific_exception` |
| Full Order Graph implementation path | bypassed | Account Plan Tracker may learn from Order Graph patterns, but this proof must not add graph implementation work. | `project_specific_exception` |
| Production integration model | bypassed | Salesforce, Outreach, and 6sense may matter later, but this proof must not assume live integrations. | `project_specific_exception` |

## Required Upstreaming Classifications

Future Account Plan Tracker pattern changes must use one of these classifications:

| Classification | Meaning |
| --- | --- |
| `project_specific_exception` | Useful only for Account Plan Tracker. |
| `candidate_upstream_improvement` | May improve ChaOS core. |
| `breaking_abstraction` | Reveals the current ChaOS pattern does not generalize. |
| `rejected_pattern` | Pattern created friction and must not be reused here. |

## Current Adaptations

Current adaptation: Core Workflow Model narrowed to one MVP workflow.

Reason: A narrow proof project needs enough workflow structure to produce a build prompt, but not enough ceremony to become framework work.

Upstreaming classification: `project_specific_exception`

## Current Bypasses

Current bypass: Core Agent Model.

Reason: The proof target is account-plan architecture clarity, not agent behavior.

Upstreaming classification: `project_specific_exception`

Current bypass: Production integrations.

Reason: This proof must not assume live Salesforce, Outreach, 6sense, CRM writes, or external data.

Upstreaming classification: `project_specific_exception`

## Watch Items

The proof should watch for:

- Whether Entity/Signal/State/Decision/Outcome/Feedback clarifies account planning.
- Whether the workflow model creates useful build structure or unnecessary ceremony.
- Whether account planning needs domain vocabulary that does not fit ChaOS cleanly.
- Whether any adaptation should become `candidate_upstream_improvement`, `breaking_abstraction`, or `rejected_pattern` after the proof run.
