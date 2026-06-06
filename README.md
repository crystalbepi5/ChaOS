# ChaOS

ChaOS stands for Chase Architecture Operating System.

ChaOS is a reusable operating system for turning ideas into systems. Its purpose is to eliminate the cost of starting over. Each future project must inherit stable architecture, agent patterns, workflow patterns, decision patterns, evaluation patterns, documentation patterns, and learning patterns before adding project-specific structure. Only the business context is expected to change.

## Current v0.1 Positioning

ChaOS v0.1 is a personal architecture operating system, a local proof harness, and a reusable pattern library under pressure test.

ChaOS v0.1 is allowed to help one maintainer think, build, and audit more clearly before it claims to be portable for other maintainers.

ChaOS v0.1 is not yet a universal framework, portable constitution for other humans, production application framework, deployed system, agent platform, or replacement for domain-specific judgment.

ChaOS must pay for itself. If applying ChaOS to a project creates more translation cost than delivery leverage, the project may adapt, bypass, or fork the pattern, but the reason must be recorded.

## What ChaOS Is

ChaOS is a foundational architecture repository. It defines reusable ways to reason about entities, signals, state, decisions, outcomes, feedback, workflows, agents, evaluations, and change management.

The documentation is the product. The repository is the container.

ChaOS helps future projects begin with a clear operating model instead of a blank page. Examples include Sales OS, Synapse, Velocity Bot, MedSpa CRM, RFP research systems, AI agents, and future businesses that do not exist yet.

## What ChaOS Is Not

ChaOS is not a product, startup, CRM, workflow engine, AI agent platform, or coding framework. It does not assume a specific industry, vendor, model provider, programming language, database, or deployment target.

ChaOS must not become an implementation too early. Implementation belongs downstream, after the architecture has clarified what the system is, how it behaves, and how its decisions are evaluated.

## Who It Is For

ChaOS is for founders, builders, operators, architects, and coding agents who need to turn unclear ideas into durable systems. In v0.1, that claim is still under proof. ChaOS must demonstrate that it accelerates real builds before it claims broad portability.

The repository is also for future maintainers who were not present when the original decisions were made. ChaOS must be understandable without private context.

## How To Use ChaOS

For a new project, start with the Project Intake Packet:

`templates/project-intake-packet.md`

Start with the architectural laws, then model the domain through the core system model:

Entity -> Signal -> State -> Decision -> Outcome -> Feedback

If the business context is incomplete, ambiguous, conflicting, or inherited from private memory, run Context Sufficiency Assessment before Architecture Generation:

Known / Inferred / Unknown -> Readiness Decision -> Clarifying Questions or Architecture Generation

When context is sufficient, generate a reviewable Architecture Starter Package:

Business Context -> Architecture Generation -> Architecture Starter Package -> Human Review -> Implementation Decision

Use the starter package template for the generated output:

`templates/architecture-starter-package.md`

Next, model work through the core workflow model:

Trigger -> Input -> Processing -> Decision -> Action -> Feedback

Then define any agents using the core agent model:

Purpose, Inputs, Processing Logic, Outputs, Evaluation, Examples

Only after those documents are clear may a project choose tools, code structure, vendors, automations, or user interfaces.

## How Future Projects Inherit From ChaOS

A future project must copy or reference the stable ChaOS patterns, then replace only the business context:

- Domain entities
- Signals worth observing
- States worth interpreting
- Decisions worth supporting
- Outcomes worth measuring
- Feedback loops worth preserving
- Workflows to operate
- Agents to assist
- Evaluation criteria

If a future project needs to modify a ChaOS pattern, it must document why the inherited pattern was insufficient and whether the improvement belongs back in ChaOS.

A project using ChaOS must declare the ChaOS pattern version inherited, patterns used, patterns adapted, patterns bypassed, and the reason for each adaptation or bypass.

If a project modifies a ChaOS pattern, the change must be classified as `project_specific_exception`, `candidate_upstream_improvement`, `breaking_abstraction`, or `rejected_pattern`.

## Proof Gate

ChaOS must be used to accelerate a real build within two weeks of major framework expansion. If it cannot demonstrate practical leverage, expansion pauses.

The proof gate measures whether ChaOS reduced decision or design time, clarified requirements, prevented rework, improved Codex prompts, improved PR audit quality, or produced a working artifact faster.

## Long-Term Vision

ChaOS is intended to become a portable architecture constitution for new systems. It must make good system design repeatable without making it rigid. It must help humans and agents collaborate with shared language, visible assumptions, traceable decisions, and inspectable feedback.

The long-term measure of success is simple: a new project can begin from ChaOS and feel like it inherited a seasoned architecture team.

## First Milestone

Version 0.1 defines the constitution and proof harness:

- Architectural laws
- Core system model
- Core workflow model
- Core agent model
- Meta-Agent specification
- Documentation standards
- Evaluation standards
- Change management standards
- Abstraction tax, inheritance, upstreaming, and proof-gate rules
- Portable schemas, workflows, templates, and examples

Version 0.1 intentionally avoids production application code. The first milestone is conceptual clarity under real-build pressure.

## Meta-Agent CLI

ChaOS includes a simple first working version of the Meta-Agent review process.

The Meta-Agent CLI reads selected repository files, combines them into a review context, sends that context to an LLM, and saves a Markdown report at:

```text
docs/journal/0001-meta-agent-review.md
```

The CLI follows this process:

```text
Observe -> Diagnose -> Recommend -> Human Approval
```

It does not apply recommended changes automatically. It does not use a database, frontend, Docker, or infrastructure.

### Setup

1. Copy `.env.example` to `.env`.
2. Add your OpenAI API key:

```text
OPENAI_API_KEY=your_api_key_here
```

3. Optionally change the model:

```text
OPENAI_MODEL=gpt-5.2
```

### Run

Use the bundled runner from the repository root:

```powershell
scripts\run_meta_agent.cmd
```

The runner uses PowerShell and has no package dependencies to install.

If Python is available in your environment, this alternate command is also provided:

```bash
python scripts/run_meta_agent.py
```

## Recommended Review Order

1. Read `AGENTS.md`.
2. Read `docs/architectural-laws.md`.
3. Read `docs/chaos-v0.1-scope.md`.
4. Read `docs/core-system-model.md`.
5. Read `docs/core-workflow-model.md`.
6. Read `docs/core-agent-model.md`.
7. Read `docs/meta-agent.md`.
8. Review schemas, workflows, and examples.
9. Read `docs/assumptions.md`.
