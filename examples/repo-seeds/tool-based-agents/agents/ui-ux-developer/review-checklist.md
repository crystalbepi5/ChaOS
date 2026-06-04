# UI/UX Developer Review Checklist

## Product Fit

- The interface type is identified.
- The primary user workflow is visible.
- The UI supports repeated use, not only first impressions.
- The design matches the product domain.

## Specificity

- Labels are concrete.
- Metrics, statuses, and actions feel operational.
- Empty states, risks, and edge cases are considered.
- The interface avoids generic AI dashboard patterns.

## Layout

- Navigation is predictable.
- Hierarchy is clear.
- Spacing is consistent.
- Dense information remains scannable.
- Cards are used only when they frame real repeated items or tools.
- Page sections are not nested card stacks.

## Controls

- Buttons represent clear actions.
- Toggles represent binary settings.
- Segmented controls represent modes or filters.
- Inputs, menus, and tables behave like familiar product UI.
- Disabled, hover, selected, and active states are visible when relevant.

## Visual System

- Palette is not one-note.
- Typography fits the information density.
- Letter spacing is 0 unless an existing design system requires otherwise.
- Font size does not scale directly with viewport width.
- Decorative elements do not compete with workflow content.

## Responsiveness

- Desktop layout is usable.
- Mobile layout is usable.
- Text does not overlap.
- Tables or dense areas degrade responsibly.
- Fixed-format UI elements have stable dimensions.

## Accessibility

- Interactive controls have accessible labels or clear text.
- Contrast is sufficient for critical information.
- Status does not rely on color alone when possible.
- Focus and keyboard behavior are considered when implementation scope allows.

## Verification

- Browser screenshot reviewed when available.
- Mobile screenshot reviewed when available.
- Console checked when relevant.
- Build or test command run when relevant.
- Remaining risks are stated.
