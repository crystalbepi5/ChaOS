# Assumptions

This document exists to make implicit choices explicit. ChaOS treats context as a dependency, so assumptions should be visible.

## Version 0.1 Assumptions

1. ChaOS is documentation-first. Implementation will come later.
2. Markdown, JSON Schema, YAML, and CSV are sufficient for the first version because they are portable and inspectable.
3. Future projects will vary by industry, but they can inherit common architecture patterns.
4. Human approval is required for constitutional changes.
5. Agents should be designed as bounded system components, not open-ended personalities.
6. Evaluation is part of architecture, not a final testing step.
7. Simplicity is a feature when it improves reuse and comprehension.
8. The repository should support both human builders and coding agents.
9. The Meta-Agent should begin as an advisory reviewer before it can generate patches.
10. ChaOS must remain useful even if its creator is unavailable.

## Open Questions

These are not TODOs. They are known areas for future decision records.

- Should ChaOS use formal semantic versioning for constitutional documents?
- How should project-specific forks report improvements back to ChaOS?
- What level of evaluation evidence is required before an advisory agent can propose patches?
- Should future versions include domain packs, or would that make ChaOS too product-specific?

## Future Considerations

Assumptions should be reviewed when a future project inherits ChaOS and finds a gap. Repeated project-level gaps may indicate a ChaOS-level improvement.

