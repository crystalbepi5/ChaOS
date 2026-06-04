# Tool-Based Agents

This repo seed defines practical agents that use tools to inspect, build, verify, and improve work.

## Purpose

Tool-Based Agents exists to turn high-level agent roles into inspectable operating contracts. Each agent must define what it does, what tools it may use, what evidence it must collect, what it produces, and how its work is evaluated.

## Repository Shape

```text
tool-based-agents/
  README.md
  agents/
    ui-ux-developer/
      agent.md
      operating-prompt.md
      review-checklist.md
      output-template.md
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

## First Agent

The first agent is the UI/UX Developer Agent. It reviews and improves product interfaces using source files, screenshots, browser inspection, and implementation tools.

## Operating Principle

Agents must not rely on taste alone. They must connect recommendations to visible evidence, product purpose, user workflow, accessibility, responsiveness, and implementation constraints.

## Future Considerations

Future agents may include Research Agent, QA Agent, Documentation Agent, Data Analyst Agent, and Workflow Designer Agent. New agents must be added only when their tool use and evaluation criteria are specific enough to inspect.
