# Modern Lab Parity Audit

**Baseline:** AI Playgrounds v1.7.1; corrected at v1.8.1
**Scope:** compare Labs 13–15 against the mature product-level affordances present in all original twelve applets.

## Finding

The original twelve applets have converged on a consistent outer learning/product shell. Labs 13–15 have strong concept-specific mechanisms and, since v1.6.1, share a common basic header/footer. v1.7.1 also aligned theme persistence, but several mature suite affordances remained absent or divergent.

This audit distinguishes **shared-shell deficits** from **legitimate concept-specific equivalents**. The goal is not to make every learning body identical.

## Affordance matrix

| Affordance present in original 12 | Original 12 | Labs 13–15 v1.7.1 | v1.7.2 ruling |
|---|---:|---:|---|
| Skip-to-controls link | 12/12 | 0/3 | Add |
| Share current link/state affordance | 12/12 | 0/3 | Add generic share/copy; do not pretend every modern state is URL-serialized |
| Embed helper / `?embed=1` | 12/12 | 0/3 | Add generic embed mode |
| Mature header hierarchy | visible Share · Embed · local export(s) · Reset | flatter modern action row | **Corrected in v1.8.1:** v1.7.2 wrongly hid shared actions under More; expose Share · Embed · JSON · Reset |
| Generic current-settings JSON | shared mature toolbar | 0/3 | Add local-only settings export; exclude learner responses |
| TL;DR / Big idea orientation | 12/12 | 0/3 shared | Add concise concept-specific orientation |
| Accessibility/text-state guidance layer | 12/12 | 0/3 shared | Add shared guidance, point to each lab's existing text/numeric state |
| Key terms panel | 12/12 | 0/3 shared | Add compact concept-specific terms |
| Essay/primer + misconception/fidelity framing | 12/12 | partial/ad hoc | Add compact shared fidelity/model-boundary block |
| Shared theme preference namespace | 12/12 use `theme` | 3/3 use `theme` with one-time legacy migration | Preserve v1.7.1 behavior and add final-artifact regression coverage |
| Theme placement in preference row | 12/12 | action-row placement | Move theme beside language preference |
| Quick Assign state snapshot | original packet includes current-state evidence | 0/3 | Add from each modern lab's existing text-equivalent state |
| Quick Assign Refresh state | original packet | 0/3 | Add |
| Quick Assign copy includes state + answers | original packet | answers only | Align |
| Quick Assign packet-only print | original packet | whole-page `window.print()` | Align |
| Quick Assign localized action labels / textarea names | mature original packet localizes interface | action buttons / `aria-label`s English-only | Align EN/ZH/VI/ES |
| Canonical suite portfolio + ORCID provenance | 12/12 | thinner footer | Enrich footer using the already-established repository values only |
| Favicon | 12/12 | 0/3 | Add shared favicon |
| JSON-LD WebApplication/LearningResource metadata | 12/12 | 0/3 | Add |
| OpenGraph title/description/url/image | 12/12 | Labs 13–14 yes; Lab 15 incomplete | Normalize all three |
| Twitter card/title/description/image | 12/12 | Labs 13–14 partial; Lab 15 absent | Normalize all three |
| `hreflang` EN/ZH/VI/ES/x-default | 12/12 | Labs 13–14 yes; Lab 15 absent | Normalize all three |
| Learning-mode shell | 12/12 | 0/3 | Keep concept-specific interactive bodies; add the shared learner sequence without duplicating a tab system |
| Scenario gallery | 12/12 | concept-specific selectors already exist | **Corrected in v1.8.1:** selectors are controls, not curriculum; add five plain-language predict–run–explain cases |
| Worksheet/response system | 12/12 | Quick Assign response layer exists | Do **not** duplicate |
| Applet-specific CSV/PNG export | mixed, not universal | mixed/absent | Do **not** force; concept-specific |

## Rationale

The missing items chosen for v1.7.2 reduce product-learning friction without changing any AI algorithm:

- a learner can skip directly to the interactive mechanism;
- a teacher can share or embed a modern lab in the same way as an older lab;
- the first screen exposes the same orientation vocabulary (`The big idea`);
- keyboard/text-state support is explicitly discoverable rather than merely implemented;
- terminology and misconception/fidelity boundaries are visible in the same conceptual location;
- theme choice carries between old and new labs instead of splitting into two preference namespaces;
- suite provenance uses the same already-established portfolio/ORCID values everywhere;
- social/search metadata has the same completeness regardless of which generation produced the applet;
- a modern Quick Assign captures the same type of inspectable state evidence as an original packet rather than asking the learner to reconstruct the run from memory;
- Copy/Print packet behavior operates on the assignment packet rather than the whole applet;
- the packet's action labels and accessible field names follow the same locale as its prompts.

The following are intentionally **not** standardized into duplicate UI:

- Explore/Guided/Classroom tabs, because Labs 13–15 already have explicit Guided Challenges and local Quick Assign surfaces;
- a second response packet, because v1.7.0 already gives every lab exactly one assignment surface;
- CSV/PNG exports, because those are not universal even among the original twelve and should exist only where they support the mechanism.

## Approved concept-specific equivalents and exceptions

- The modern labs' Guided Challenge plus Quick Assign path is the approved equivalent of adding another Explore / Guided / Classroom mode shell.
- Existing scenario and challenge selectors remain the mechanism controls. They are no longer treated as an approved substitute for learner-facing scenario explanations.
- Reset reloads the current modern mechanism while the separate local Quick Assign draft remains recoverable. The control is therefore labeled **Reset lab**, not **Reset all**.
- The generic settings JSON is shared product chrome. Applet-specific CSV/PNG export remains optional and must be justified by the mechanism.

No exception permits a second algorithm, simulation state, response packet, or assignment ID.

## v1.8.1 correction

The v1.7.2 ruling was too narrow. It established shell and release parity but overstated learner-facing parity by accepting a selector, compact key terms, and a fidelity note as equivalents for the original twelve applets' scenario-led curriculum. That decision produced three observable gaps:

- the modern labs had no featured experiment or five-case predict–run–explain sequence;
- their explanations and teacher prompts were materially thinner;
- repeated generated state and dense catalogue copy made them harder, not easier, to enter.

v1.8.1 corrects the boundary without forcing identical mechanism layouts. Labs 13–15 retain their native Transformer, agent-runtime, and game-tree controls, but now add the same learner sequence and depth in EN/ZH/VI/ES. The correction also exposes Share, Embed, JSON, and Reset as one visible action row, removes the always-open duplicate state mirror, leaves Quick Assign state empty until explicitly refreshed, and adds final dark-theme contrast checks for hard-coded light surfaces and accent text.

## Additional defects caught during the parity implementation

The parity process itself caught four control-induced errors before release:

1. an early static validator counted JavaScript references to `data-quick-assign-id` as if they were extra assignment surfaces; the final gate counts actual HTML start tags/DOM surfaces instead;
2. an early rich-footer draft introduced alternate portfolio/ORCID values instead of inheriting the existing suite provenance. The final composition now normalizes to the established repository identity and rejects alternate values.
3. an accessibility wrapper searched backward for `</head>` and matched that text inside packet-printing JavaScript, inserting CSS into an executable string. The corrected builder locates the structural head boundary, and final QA compiles every inline script.
4. the inherited builder chain reused ignored release-evidence and generated state, so a second invocation could fail after a successful first build. v1.7.2 composes the v1.7.1 baseline in a clean isolated workspace and compares all final file hashes across two builds.

These are retained as evidence that consistency work must itself be tested at final composition rather than accepted because controls merely look similar.

## Evidence boundary

This audit concerns product consistency, discoverability metadata, assignment-surface parity, and implementation behavior. It does not establish learner preference, learning gains, classroom adoption, or accessibility conformance.
