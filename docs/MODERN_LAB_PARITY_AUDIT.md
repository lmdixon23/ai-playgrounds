# Modern Lab Parity Audit

**Baseline:** AI Playgrounds v1.7.0  
**Scope:** compare Labs 13–15 against the mature product-level affordances present in all original twelve applets.

## Finding

The original twelve applets have converged on a consistent outer learning/product shell. Labs 13–15 have strong concept-specific mechanisms and, since v1.6.1, share a common basic header/footer, but they still omit or diverge from several mature suite affordances.

This audit distinguishes **shared-shell deficits** from **legitimate concept-specific equivalents**. The goal is not to make every learning body identical.

## Affordance matrix

| Affordance present in original 12 | Original 12 | Labs 13–15 v1.7.0 | v1.7.1 ruling |
|---|---:|---:|---|
| Skip-to-controls link | 12/12 | 0/3 | Add |
| Share current link/state affordance | 12/12 | 0/3 | Add generic share/copy; do not pretend every modern state is URL-serialized |
| Embed helper / `?embed=1` | 12/12 | 0/3 | Add generic embed mode |
| TL;DR / Big idea orientation | 12/12 | 0/3 shared | Add concise concept-specific orientation |
| Accessibility/text-state guidance layer | 12/12 | 0/3 shared | Add shared guidance, point to each lab's existing text/numeric state |
| Key terms panel | 12/12 | 0/3 shared | Add compact concept-specific terms |
| Essay/primer + misconception/fidelity framing | 12/12 | partial/ad hoc | Add compact shared fidelity/model-boundary block |
| Shared theme preference namespace | 12/12 use `theme` | 0/3 (`ai-playgrounds-theme`) | Rejoin canonical `theme` key |
| Theme placement in preference row | 12/12 | action-row placement | Move theme beside language preference |
| Canonical suite portfolio + ORCID provenance | 12/12 | thinner footer | Enrich footer using the already-established repository values only |
| Favicon | 12/12 | 0/3 | Add shared favicon |
| JSON-LD WebApplication/LearningResource metadata | 12/12 | 0/3 | Add |
| OpenGraph title/description/url/image | 12/12 | Labs 13–14 yes; Lab 15 incomplete | Normalize all three |
| Twitter card/title/description/image | 12/12 | Labs 13–14 partial; Lab 15 absent | Normalize all three |
| `hreflang` EN/ZH/VI/ES/x-default | 12/12 | Labs 13–14 yes; Lab 15 absent | Normalize all three |
| Learning-mode shell | 12/12 | 0/3 | Do **not** duplicate; Guided Challenge + Quick Assign are the modern equivalent |
| Scenario gallery | 12/12 | concept-specific selectors already exist | Do **not** duplicate |
| Worksheet/response system | 12/12 | Quick Assign response layer exists | Do **not** duplicate |
| Applet-specific CSV/PNG export | mixed, not universal | mixed/absent | Do **not** force; concept-specific |
| Compact header More treatment | 12/12 has established narrow-header treatment | absent | Use responsive action wrapping; do not add a menu unless measured clutter warrants it |

## Rationale

The missing items chosen for v1.7.1 reduce product-learning friction without changing any AI algorithm:

- a learner can skip directly to the interactive mechanism;
- a teacher can share or embed a modern lab in the same way as an older lab;
- the first screen exposes the same orientation vocabulary (`The big idea`);
- keyboard/text-state support is explicitly discoverable rather than merely implemented;
- terminology and misconception/fidelity boundaries are visible in the same conceptual location;
- theme choice carries between old and new labs instead of splitting into two preference namespaces;
- suite provenance uses the same already-established portfolio/ORCID values everywhere;
- social/search metadata has the same completeness regardless of which generation produced the applet.

The following are intentionally **not** standardized into duplicate UI:

- Explore/Guided/Classroom tabs, because Labs 13–15 already have explicit Guided Challenges and local Quick Assign surfaces;
- scenario galleries, because the Transformer, agent-runtime, and game-tree bodies already expose concept-specific scenario/challenge selectors;
- a second response packet, because v1.7.0 already gives every lab exactly one assignment surface;
- CSV/PNG exports, because those are not universal even among the original twelve and should exist only where they support the mechanism.

## Additional defects caught during the parity implementation

The parity process itself caught two control-induced errors before release:

1. an early static validator counted JavaScript references to `data-quick-assign-id` as if they were extra assignment surfaces; the final gate counts actual HTML start tags/DOM surfaces instead;
2. an early rich-footer draft introduced alternate portfolio/ORCID values instead of inheriting the existing suite provenance. The final composition now normalizes to the established repository identity and rejects alternate values.

These are retained as evidence that consistency work must itself be tested at final composition rather than accepted because controls merely look similar.

## Evidence boundary

This audit concerns product consistency, discoverability metadata, and implementation behavior. It does not establish learner preference, learning gains, classroom adoption, or accessibility conformance.
