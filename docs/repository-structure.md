# Repository Structure

This document exists to explain the structure of the ChaOS repository and why each major area exists.

## Structure

```text
ChaOS/
  README.md
  AGENTS.md
  .env.example
  agents/
    meta-agent/
      prompt.md
  docs/
    architectural-laws.md
    architecture.md
    assumptions.md
    chaos-v0.1-scope.md
    core-agent-model.md
    core-system-model.md
    core-workflow-model.md
    decision-records/
      0001-order-graph-reference-implementation.md
      0002-chaos-v0.1-scope-and-proof-gate.md
    decisions/
      0003-repository-alignment.md
      0004-authority-and-implementation-boundary.md
      0005-candidate-constitutional-concepts.md
      0006-architecture-generation-workflow.md
      0007-modal-language-authority.md
      0008-context-sufficiency-assessment.md
      0009-project-intake-packet.md
    decision-records.md
    evaluations.md
    glossary.md
    journal/
      0001-meta-agent-review.md
      0003-synapse-inheritance-review.md
      0004-cross-project-pattern-analysis.md
      0005-architecture-generation-test-rfp-discovery.md
      0006-context-sufficiency-test-community-garden.md
      README.md
    meta-agent.md
    order-graph/
      overview.md
      build-roadmap.md
      testing-gates.md
    repository-structure.md
  schemas/
    agent.schema.json
    decision-record.schema.json
    system-model.schema.json
    workflow.schema.json
  workflows/
    architecture-generation.yaml
    context-sufficiency-assessment.yaml
    meta-agent-review.yaml
    system-design-review.yaml
    workflow-template.yaml
  templates/
    README.md
    architecture-starter-package.md
    project-intake-packet.md
  examples/
    decisions.csv
    feedback.csv
    repo-seeds/
      README.md
      tool-based-agents/
        README.md
        standards/
          tool-access.md
        agents/
          documentation/
            agent.md
          qa-developer/
            agent.md
          research/
            agent.md
          ui-ux-developer/
            agent.md
            operating-prompt.md
            output-template.md
            review-checklist.md
          workflow-designer/
            agent.md
    signals.csv
    ui-mockups/
      README.md
      rootline-command/
        README.md
        index.html
    workflow-runs.csv
  scripts/
    run_meta_agent.cmd
    run_meta_agent.ps1
    run_meta_agent.py
```

## Root Files

### README.md

The README is the public orientation layer. It explains what ChaOS is, what it is not, who it is for, how it is used, how future projects inherit from it, the long-term vision, and the first milestone.

Future consideration: The README may later include version history and project inheritance instructions.

### AGENTS.md

AGENTS.md is the operational handbook for future coding agents. It defines the repository purpose, architectural laws, design philosophy, documentation standards, agent standards, workflow standards, evaluation standards, and change management standards.

Future consideration: This file may later include stricter agent permissions or maturity levels.

### .env.example

`.env.example` documents the environment variables needed to run local support tooling such as the Meta-Agent CLI.

Future consideration: This file must remain minimal and must not become a general configuration system.

## agents/

The agents directory contains agent-specific definitions and prompts. These files describe agent behavior without granting agents authority to change the repository automatically.

Examples:

- `agents/meta-agent/prompt.md` defines the prompt contract for Meta-Agent review output.

Future consideration: Additional agents must be added only when they remove more complexity than they add.

## docs/

The docs directory contains the constitutional layer of ChaOS. These documents define the thinking patterns future projects inherit.

Examples:

- A future CRM inherits the workflow model before selecting CRM software.
- A research system inherits the decision record pattern before building ranking tools.
- A new agent inherits the agent model before choosing a model provider.

Future consideration: The docs directory may later be split into constitution, patterns, and governance if the repository grows.

### docs/chaos-v0.1-scope.md

This document defines the honest v0.1 scope, abstraction tax rule, pattern inheritance rule, upstreaming classifications, proof gate, and success/failure criteria.

Examples:

- A project declares that it inherits ChaOS v0.1 but bypasses the full workflow model.
- A pattern adaptation is classified as `candidate_upstream_improvement`.
- Major framework expansion pauses until a real build proves practical leverage.

Future consideration: If these rules grow, ChaOS may split them into separate governance documents only after repeated use proves that one scope document is not enough.

### docs/decision-records/

The decision-records directory contains approved decision records for implementation-track boundaries that must remain separate from exploratory journal entries.

Examples:

- `0001-order-graph-reference-implementation.md` approves the controlled Order Graph reference implementation track while prohibiting production integrations, real customer data ingestion, databases, frontends, autonomous actions, and vendor lock-in at this stage.
- `0002-chaos-v0.1-scope-and-proof-gate.md` records the decision to scope ChaOS v0.1 as a personal architecture operating system and local proof harness with a State primitive, abstraction tax rule, inheritance rules, upstreaming classifications, and a two-week proof gate.

Current boundary: ChaOS currently contains both `docs/decision-records/` and `docs/decisions/`. Until a future cleanup decision is made, new formal architecture decision records must use `docs/decision-records/`. The `docs/decisions/` folder must not be expanded without a decision record clarifying its purpose.

Future consideration: If decision records remain split between `docs/decisions/` and `docs/decision-records/`, ChaOS must clarify whether the distinction is historical, structural, or temporary.

### docs/decisions/

The decisions directory contains earlier decision records. These records explain accepted changes, rationale, alternatives, consequences, and feedback plans.

Examples:

- A decision record accepting repository alignment after a Meta-Agent review.

Current boundary: This folder must not receive new formal architecture decision records until ChaOS clarifies the relationship between `docs/decisions/` and `docs/decision-records/` through an explicit decision record.

Future consideration: Decision records may later receive an index if the directory becomes difficult to scan.

### docs/journal/

The journal directory contains review artifacts. Journal entries may include observations, diagnoses, recommendations, and questions, but they are not approved architecture changes by themselves.

Examples:

- A Meta-Agent review report.

Future consideration: Journal entries may later use review-type prefixes if numbered files become too vague.

### docs/order-graph/

The order-graph directory contains documentation rails for the Order Graph reference implementation track.

Examples:

- `overview.md` defines the Order Graph and its relationship to ChaOS.
- `build-roadmap.md` defines the controlled phase sequence.
- `testing-gates.md` defines the strict gates that must stop implementation from outrunning understanding.

Future consideration: This directory may later include contracts, fixtures, or schema documentation only after the relevant testing gates allow that work.

## schemas/

The schemas directory contains portable JSON Schemas for core ChaOS objects. Schemas make the architecture inspectable and easier to implement later without choosing a software stack now.

Examples:

- Validate an agent specification.
- Validate a workflow definition.
- Validate a decision record.
- Validate an entity-signal-decision-outcome-feedback model.

Future consideration: Schemas may later gain versioning, examples, and compatibility notes.

## workflows/

The workflows directory contains YAML workflow definitions. These are not automation scripts. They are inspectable workflow contracts that explain stages, responsibilities, inputs, outputs, failure modes, and evaluation methods.

Examples:

- A Meta-Agent review workflow.
- A system design review workflow.
- A context sufficiency assessment workflow.
- An architecture generation workflow.
- A reusable workflow template.

Future consideration: Workflow definitions may later map to automation platforms, but the YAML must remain understandable without those platforms.

## templates/

The templates directory contains directly usable Markdown artifacts. Templates help humans and agents capture project context before applying ChaOS workflows.

Examples:

- `project-intake-packet.md` captures raw business context and routes the project to Context Sufficiency Assessment, Architecture Generation, or no generation yet.
- `architecture-starter-package.md` captures the standard Architecture Generation output for human review.

Future consideration: Additional templates must be added only when repeated use proves that one reusable intake packet is not enough.

## examples/

The examples directory contains CSV examples that make the architecture concrete. CSV is intentionally simple, portable, and inspectable.

Examples:

- Signals collected about entities.
- Decisions made from signals.
- Feedback captured after outcomes.
- Workflow run history.
- Repo seeds for future standalone projects.
- Static UI mockups that explore possible product experience without defining implementation requirements.

Future consideration: Examples may later expand by domain, but Version 0.1 keeps them cross-domain.

## scripts/

The scripts directory contains small support tooling for repository review. Scripts must serve the documentation-first architecture and must not become product code.

Examples:

- `run_meta_agent.cmd` starts the Meta-Agent review on Windows.
- `run_meta_agent.ps1` reads selected files, calls the LLM, and writes the review report.
- `run_meta_agent.py` provides an alternate runner for environments with Python.

Future consideration: If support tooling grows, ChaOS must decide which runner is primary and avoid duplicating logic unnecessarily.
