# Architectural Laws

This document exists to define the non-negotiable design laws of ChaOS. It is the first reference point for any architectural decision, agent behavior, workflow design, or future implementation.

The laws are intentionally plain. Their job is to keep systems understandable, portable, and maintainable even as projects become more complex.

## Law 1: Do Not Optimize Chaos Into More Chaos

### Meaning

Improving a messy system without first understanding it often produces a faster, larger, or more automated mess. Optimization must follow comprehension.

### Rationale

Many systems fail because they improve surface speed while preserving underlying confusion. ChaOS must identify the shape of the problem before proposing tools or automations.

### Examples

- Before automating lead routing, define what a lead is, which signals matter, and how routing quality will be evaluated.
- Before building an agent, document the decision it supports and the feedback it will receive.
- Before adding dashboards, decide which outcomes deserve attention.

### Anti-Patterns

- Automating a workflow no one can explain.
- Adding AI to compensate for unclear process ownership.
- Building integrations before defining the source of truth.

## Law 2: Every Component Must Remove More Complexity Than It Adds

### Meaning

A component earns its place only if the system becomes easier to understand, operate, or evolve because it exists.

### Rationale

Every document, schema, workflow, agent, and integration creates maintenance cost. Complexity is acceptable only when it buys back more clarity or capability than it consumes.

### Examples

- A decision record adds value when it prevents the same debate from recurring.
- A schema adds value when it makes data exchange safer across projects.
- An agent adds value when it makes a repeated judgment more consistent.

### Anti-Patterns

- Creating categories that no one uses.
- Adding a tool because it is fashionable.
- Splitting one simple workflow into many abstractions without operational need.

## Law 3: Context Is A Dependency. Minimize It.

### Meaning

If a system requires private memory, tribal knowledge, or a single person's explanation to function, that context is a hidden dependency.

### Rationale

Hidden context makes systems fragile. ChaOS must make assumptions, definitions, decisions, and evaluation criteria visible.

### Examples

- Document why a project defines an entity as an account instead of a company.
- Capture the rationale behind evaluation thresholds.
- Write examples that show how a pattern changes across industries.

### Anti-Patterns

- Naming concepts after inside jokes or personal shorthand.
- Relying on "everyone knows" logic.
- Leaving edge cases in chat history instead of repository documents.

## Law 4: Systems Must Be Understandable By Humans First

### Meaning

A system that only machines can operate is not yet architecture. Humans must be able to inspect its logic, purpose, inputs, outputs, and tradeoffs.

### Rationale

Human comprehension is the foundation of trust, maintenance, and responsible automation.

### Examples

- Use readable workflow definitions before implementation code.
- Explain agent behavior in plain language before prompt or model selection.
- Keep evaluation rubrics visible.

### Anti-Patterns

- Treating a model response as an explanation.
- Hiding business logic inside prompts, scripts, or vendor configuration.
- Using complex terminology to disguise unclear thinking.

## Law 5: The System Must Survive The Loss Of Its Creator

### Meaning

ChaOS must remain understandable and useful if its original creator is unavailable.

### Rationale

Durable systems cannot depend on one person's memory. The repository must teach future maintainers how to reason with it.

### Examples

- Record assumptions explicitly.
- Keep decision records for major architectural choices.
- Use examples from multiple domains to prove portability.

### Anti-Patterns

- Requiring the creator to explain why a pattern exists.
- Leaving important standards in private notes.
- Designing around personal habits that future teams cannot inherit.

## Law 6: Recommend Before Automating

### Meaning

A system must first prove that it can make useful recommendations before it is allowed to act automatically.

### Rationale

Recommendation creates a learning loop with lower risk. Automation must be earned through repeated, evaluated recommendations.

### Examples

- A Meta-Agent first recommends improvements to ChaOS before generating patches.
- A sales assistant first suggests next actions before sending messages.
- A research system first ranks sources before automatically writing reports.

### Anti-Patterns

- Letting an agent modify architecture without approval.
- Automating actions before failure modes are known.
- Confusing confidence with permission.

## Law 7: Prefer Inspectable Systems Over Intelligent Systems

### Meaning

A less sophisticated system that can be inspected is often better than a more intelligent system that cannot be explained.

### Rationale

Inspection enables trust, debugging, evaluation, and transfer across domains.

### Examples

- A transparent scoring rubric may be better than a black-box classifier.
- A workflow YAML file may be better than hidden platform configuration.
- A documented decision tree may be better than an opaque model chain.

### Anti-Patterns

- Choosing tools that cannot expose reasoning or logs.
- Treating "AI-powered" as an architecture.
- Depending on outputs that cannot be traced to inputs.

## Law 8: Every Decision Must Be Traceable

### Meaning

Important decisions must connect back to context, rationale, alternatives, expected consequences, and feedback.

### Rationale

Traceability prevents repeated debates and helps future maintainers understand why the system is shaped the way it is.

### Examples

- Record why ChaOS uses a five-layer system model.
- Track why an agent may recommend but not self-modify.
- Link evaluation changes to observed failures.

### Anti-Patterns

- Making architectural changes in passing.
- Replacing rationale with authority.
- Keeping decisions only in meeting notes or chat threads.

## Law 9: Feedback Is More Valuable Than Prediction

### Meaning

Predictions are useful, but feedback is what lets systems learn.

### Rationale

ChaOS must prefer loops that observe outcomes over claims that a design will work forever.

### Examples

- Evaluate agent recommendations after humans accept or reject them.
- Review workflow failures and update assumptions.
- Track whether a copied pattern helped a future project start faster.

### Anti-Patterns

- Treating projections as proof.
- Ignoring rejected recommendations.
- Failing to capture lessons from implementation.

## Law 10: The Simplest Architecture That Works Is The Correct Architecture

### Meaning

Architecture must be as simple as the problem allows, but no simpler than the system requires.

### Rationale

Simple systems are easier to teach, test, migrate, and repair. ChaOS must add structure only where it improves reuse and comprehension.

### Examples

- Start with Markdown before building a documentation platform.
- Use CSV examples before inventing a database.
- Define YAML workflow patterns before adopting workflow software.

### Anti-Patterns

- Designing for imaginary scale.
- Creating frameworks before patterns are proven.
- Adding layers because architecture feels more serious with more boxes.
