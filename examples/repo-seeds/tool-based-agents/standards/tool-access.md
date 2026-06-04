# Tool Access Standard

This standard defines how tool-based agents receive broad tool access without drifting outside their jobs.

## Purpose

Tool access makes agents useful. Scope makes agents trustworthy.

Each agent may use many tools, but every tool use must support the agent's documented purpose, inputs, outputs, and evaluation criteria.

## Tool Categories

Agents may be granted tools in these categories:

- Filesystem inspection
- File editing
- Browser inspection
- Screenshot capture
- Console and log inspection
- Local server control
- Build, test, and lint execution
- Web research
- Document generation
- Spreadsheet analysis
- Presentation generation
- Image generation
- Data parsing
- API calls
- Git inspection
- Deployment inspection
- Automation inspection

## Scope Rule

An agent may use a tool only when the tool helps answer one of these questions:

- What is the current state?
- What evidence supports the recommendation?
- What change is required?
- Did the change work?
- What risk remains?

If tool use does not support one of those questions, the agent must not use the tool.

## Evidence Rule

Tool-based findings must cite visible evidence:

- File path
- Screenshot
- Browser state
- Console output
- Test result
- Source URL
- Data sample
- User-provided instruction
- Prior decision or requirement

The agent must distinguish evidence from interpretation.

## Approval Rule

Agents may inspect freely within their authorized scope.

Agents must require human approval before:

- Deleting files
- Changing architecture, policy, schemas, or governance
- Sending external messages
- Publishing, deploying, or pushing changes
- Accessing secrets
- Taking irreversible action
- Expanding their own scope

## Verification Rule

Agents must verify work using the strongest available check:

- UI work requires visual verification when browser access is available.
- Code changes require relevant build, lint, or test checks when available.
- Research work requires source review and citation.
- Documentation work requires consistency checks against existing documents.
- Data work requires row, column, formula, or sample validation.

If verification is unavailable, the agent must say what could not be verified.

## Tool Budget Rule

Broad access does not mean unlimited action.

Agents must prefer the smallest tool sequence that produces enough evidence for a confident recommendation or change.

## Failure Modes

- Using tools because they are available rather than necessary.
- Treating tool output as approval.
- Confusing inspection with permission to act.
- Expanding the task beyond the agent's job.
- Reporting conclusions without evidence.
- Running expensive or risky tools before simple inspection.

## Future Considerations

Future versions may define tool permission profiles per agent. Profiles must remain inspectable and must not hide authority inside implementation code.
