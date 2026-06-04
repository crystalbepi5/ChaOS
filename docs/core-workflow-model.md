# Core Workflow Model

This document defines the workflow model used by ChaOS:

Trigger -> Input -> Processing -> Decision -> Action -> Feedback

It exists because every system needs a clear way to describe how work begins, what it consumes, how it is transformed, how choices are made, what happens, and how the system learns.

## Trigger

### Purpose

The trigger starts the workflow. It may be a user request, scheduled review, external event, threshold crossing, manual approval, or system observation.

### Responsibilities

- Declare why work is starting
- Identify the affected entity
- Capture the initiating condition
- Prevent duplicate or accidental starts

### Failure Modes

- Workflow starts too often
- Workflow starts without enough context
- Workflow fails to start when needed
- Trigger depends on hidden platform behavior

### Evaluation Methods

- Count false starts and missed starts
- Review whether triggered workflows had sufficient context
- Compare trigger criteria against outcomes

## Input

### Purpose

The input stage gathers the information needed to process the workflow.

### Responsibilities

- Collect required data
- Validate completeness
- Name assumptions
- Preserve source references

### Failure Modes

- Missing fields
- Conflicting sources
- Stale context
- Unclear ownership of source data

### Evaluation Methods

- Track input validation errors
- Review decisions that failed because of missing information
- Measure how often humans must clarify inputs

## Processing

### Purpose

Processing transforms input into structured understanding.

### Responsibilities

- Normalize information
- Apply rules or models
- Identify relevant signals
- Prepare decision options

### Failure Modes

- Hidden logic
- Over-processing simple inputs
- Losing source traceability
- Treating interpretation as fact

### Evaluation Methods

- Compare processed outputs against source inputs
- Review explainability
- Test known edge cases

## Decision

### Purpose

The decision stage chooses or recommends what happens next.

### Responsibilities

- State the decision
- Explain rationale
- Identify confidence and uncertainty
- Reference supporting signals

### Failure Modes

- Untraceable decisions
- Overconfident recommendations
- Decisions based on weak signals
- No path for human override

### Evaluation Methods

- Review acceptance and rejection rates
- Compare decisions against outcomes
- Audit rationale quality

## Action

### Purpose

The action stage executes, recommends, records, or routes the decision.

### Responsibilities

- Perform the approved next step
- Record what happened
- Respect approval boundaries
- Preserve reversibility where possible

### Failure Modes

- Acting without authorization
- Taking irreversible action too early
- Failing silently
- Updating the wrong entity

### Evaluation Methods

- Track action success and failure
- Review approval compliance
- Audit action logs

## Feedback

### Purpose

Feedback captures what was learned after action.

### Responsibilities

- Record outcomes
- Capture human judgment
- Identify recurring failures
- Recommend improvements

### Failure Modes

- No feedback captured
- Feedback too vague to use
- Feedback not connected to decisions
- Lessons never update the workflow

### Evaluation Methods

- Track feedback completeness
- Review whether feedback changed future behavior
- Compare repeated failures over time

## Example Workflow

An RFP research workflow may begin when a new RFP is found. The input stage gathers requirements, deadlines, source documents, and company fit criteria. Processing extracts requirements and mismatches. The decision stage recommends bid, no-bid, or human review. The action stage records the recommendation or sends it for approval. Feedback captures the final human decision and later win or loss data.

## Future Considerations

Future versions may define workflow maturity levels, event contracts, or adapters for automation tools. Version 0.1 defines the portable pattern first.
