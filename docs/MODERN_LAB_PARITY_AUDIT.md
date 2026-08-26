# Modern Lab Parity Audit

**Baseline:** AI Playgrounds v1.7.0  
**Scope:** compare Labs 13–15 against the mature product-level affordances present in all original twelve applets.

## Finding

The original twelve applets have converged on a consistent outer learning/product shell. Labs 13–15 have strong concept-specific mechanisms and now share a common header/footer, but they still omit several mature suite affordances.

This audit distinguishes **shared-shell deficits** from **legitimate concept-specific equivalents**. The goal is not to make every learning body identical.

## Affordance matrix

| Affordance present in original 12 | Original 12 | Labs 13–15 v1.7.0 | v1.7.1 ruling |
|---|---:|---:|---|
| Skip-to-controls link | 12/12 | 0/3 | Add |
| Share current state/link | 12/12 | 0/3 | Add generic share/copy |
| Embed helper / `?embed=1` | 12/12 | 0/3 | Add generic embed mode |
| TL;DR / Big idea orientation | 12/12 | 0/3 shared | Add concise concept-specific orientation |
| Accessibility/text-state guidance layer | 12/12 | 0/3 shared | Add shared guidance, point to each lab's existing text state |
| Key terms panel | 12/12 | 0/3 shared | Add compact concept-specific terms |
| Essay/primer + misconception/fidelity framing | 12/12 | partial/ad hoc | Add compact shared primer/fidelity block |
| Learning-mode shell | 12/12 | 0/3 | Do **not** duplicate; Guided Challenge + Quick Assign are the modern equivalent |
| Scenario gallery | 12/12 | concept-specific selectors already exist | Do **not** duplicate |
| Worksheet/response system | 12/12 | Quick Assign response layer exists | Do **not** duplicate |
| Rich site footer | 12/12 | thinner standardized footer | Enrich while retaining current-release provenance |
| Compact header More treatment | 12/12 | absent | Add only if useful for Share/Embed/Key terms on narrow screens |

## Rationale

The missing items chosen for v1.7.1 reduce product-learning friction without changing any AI algorithm:

- a learner can skip directly to the interactive mechanism;
- a teacher can share or embed a modern lab in the same way as an older lab;
- the first screen exposes the same orientation vocabulary (`The big idea`);
- keyboard/text-state support is explicitly discoverable rather than merely implemented;
- terminology and misconception/fidelity boundaries are visible in the same conceptual location;
- suite provenance and classroom links are consistent.

The following are intentionally **not** standardized into duplicate UI:

- Explore/Guided/Classroom tabs, because Labs 13–15 already have explicit Guided Challenges and local Quick Assign surfaces;
- scenario galleries, because the Transformer, agent-runtime, and game-tree bodies already expose concept-specific scenario/challenge selectors;
- a second response packet, because v1.7.0 already gives every lab exactly one assignment surface.

## Evidence boundary

This audit concerns product consistency and implementation behavior. It does not establish learner preference, learning gains, adoption, or accessibility conformance.
