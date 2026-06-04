# Tool-Based Agents

This repo seed defines practical agents that use tools to inspect, build, verify, and improve work.

## Purpose

Tool-Based Agents exists to turn high-level agent roles into inspectable operating contracts. Each agent must define what it does, what tools it may use, what evidence it must collect, what it produces, and how its work is evaluated.

## Repository Shape

```text
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
      review-checklist.md
      output-template.md
    workflow-designer/
      agent.md
```

## Agent Standard

Every agent must include:

- Purpose
- Inputs
- Tool access
- Processing logic
- Outputs
- Evaluation criteria
- Examples
- Failure modes
- Guardrails

## Agent Bench

- Documentation Agent: Creates and improves durable documentation.
- QA Developer Agent: Verifies behavior with tests, browser checks, logs, and evidence.
- Research Agent: Produces source-backed research for decisions.
- UI/UX Developer Agent: Reviews and improves product interfaces with visual verification.
- Workflow Designer Agent: Turns unclear processes into inspectable workflow contracts.

## Operating Principle

Agents must not rely on taste alone. They must connect recommendations to visible evidence, product purpose, user workflow, accessibility, responsiveness, and implementation constraints.

Agents may receive broad tool access only when tool use remains scoped to the agent's documented job. See `standards/tool-access.md`.

## Future Considerations

Future agents may include Data Analyst Agent, Security Review Agent, Presentation Agent, Spreadsheet Agent, and Release Manager Agent. New agents must be added only when their tool use and evaluation criteria are specific enough to inspect.
