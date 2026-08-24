# AI Playgrounds v1.4 Product-Quality Architecture

Date: 2026-08-25

Status: implementation architecture for the v1.4 product-quality pass. Lab 15 implementation is explicitly out of scope until this pass is accepted.

Baseline: v1.3.0 merged `main` commit `31de867576769e843a373e6a767428fe71c954bc`, plus the planning-only curriculum coverage matrix carried into this feature branch.

## 1. Goals

v1.4 is a quality and navigation release before another applet is added. It must improve the learner-facing coherence of the fourteen-app suite without weakening the deterministic, semantic, localization, accessibility, or offline guarantees already frozen for Labs 1–14.

The release has five primary goals:

1. bring Labs 13 and 14 closer to the strongest original applets in immediate visual engagement and mechanism legibility;
2. normalize all four-language controls to a scalable dropdown pattern rather than four exposed language buttons;
3. keep the software version explicitly discoverable without presenting a prominent engineering-style version badge beside the applet title;
4. distinguish foundational/course-aligned material from modern extensions in curriculum navigation;
5. preserve all v1.3 mechanisms and regression guarantees while adding an independent v1.4 acceptance layer.

## 2. Non-goals

The following are prohibited in this release:

- no Lab 15 implementation;
- no change to the mathematical reference model for Lab 13;
- no change to the Lab 14 tool catalog, authorization semantics, deterministic policy, protocol semantics, or in-memory world;
- no replacement of prediction-before-reveal with post-hoc explanation;
- no external model API, account, backend, runtime network request, or telemetry dependency;
- no mutation of the immutable v1.0.1 DOI-bearing release;
- no claim that a UX pass establishes learning gains.

## 3. Preservation strategy

The v1.3 builders and their regression tests remain historical release evidence and should continue to build the accepted v1.3 artifact unchanged.

New v1.4 builders should wrap the accepted public Lab 13 and Lab 14 outputs rather than rewriting the frozen semantic cores. The v1.4 layer may add or alter presentation, navigation, focus, animation, explanatory framing, and locale controls, but it must not mutate machine state or model/runtime arithmetic.

This allows the permanent verification stack to prove both:

- the v1.3 reference/release contract still passes; and
- the v1.4 experience layer satisfies additional UX and state-preservation contracts.

## 4. Language-control contract

All public four-language surfaces should converge on an accessible native `<select>` language control.

Required labels/options:

- English
- 简体中文
- Tiếng Việt
- Español

The dropdown must:

- preserve existing `?lang=` deep links;
- preserve the learner's experiment and Guided Challenge state when switching locale;
- use the applet's existing localization runtime rather than duplicate translation logic;
- remain keyboard and touch operable;
- remain usable at 390 px mobile width;
- avoid a custom ARIA listbox unless a native select proves insufficient.

Existing hidden compatibility buttons may remain in generated DOM only when required as an internal bridge for legacy localization code. They must not remain visible as the primary public control.

## 5. Version-presentation contract

The version remains explicit but secondary.

For Labs 13 and 14, replace the prominent hero-area `AI Playgrounds v1.3` badge in the v1.4 public output with a neutral suite identity and a compact provenance line in a footer or equivalent secondary area:

`AI Playgrounds · v1.4.0 · Source · Citation`

The precise link treatment may vary by surface, but:

- `v1.4.0` must be visible to a learner who scrolls to the page provenance area;
- the version must remain machine-readable in release metadata;
- applet titles should emphasize the concept, not the software release;
- version information must not be confused with the mathematical/model version of an applet.

## 6. Lab 13 engagement contract

Lab 13 already exposes strong mechanism detail. The v1.4 pass should reduce cognitive overload by making the causal path easier to follow without hiding the underlying numbers.

The public v1.4 experience should add a visible mechanism journey:

`1 Tokenize -> 2 Represent -> 3 Attend -> 4 Predict`

Each stage should be focusable/activatable. Activating a stage should visually emphasize the relevant existing panel(s) and de-emphasize unrelated detail without deleting or recomputing any model state.

Required behavior:

- a learner can move through all four stages in order;
- the current stage is announced through accessible state, not color alone;
- changing stage never changes tokens, temperature, mask, position vectors, perturbation, attention values, logits, probabilities, or challenge state;
- Guided Challenges remain prediction-before-reveal;
- all four locales preserve the same machine state and stage behavior.

The desired memorable story is not an animation for its own sake. It is the visible chain from a token sequence to the next-token distribution.

## 7. Lab 14 engagement contract

Lab 14 already computes the correct gate semantics. The v1.4 pass should make those semantics feel like an action moving through a runtime rather than a static dashboard.

The public v1.4 experience should make the selected action path legible across:

`Propose -> Validate -> Authorize -> Execute -> Observe -> Update / choose next -> Stop`

Required behavior:

- the currently selected candidate action is visually identified as the object being evaluated;
- invalid calls visibly terminate at validation;
- unauthorized calls visibly terminate at authorization;
- execution errors are distinct from rejected/denied calls;
- successful observations visibly feed the context-update/next-action story;
- satisfied goals visibly terminate at `stop` rather than suggesting more execution;
- the injection scenario retains the instruction-like text as provenance-aware data and does not sanitize it;
- visual staging never changes the underlying deterministic policy or state.

The desired memorable story is: an action can be available, valid, authorized, executed, observed, and still require a new decision; those are not the same thing.

## 8. Curriculum/navigation contract

The public curriculum should expose three complementary ways into the same applet set:

1. **Foundations / course track** — broad AIMA/introductory-AI progression;
2. **Modern extensions** — currently Lab 14, with Lab 13 positioned at the boundary because Transformers are now part of advanced introductory NLP curricula;
3. **Quick-entry sampler** — optimized for first-visit impact rather than prerequisites.

This is navigation, not a claim that one curriculum is universally canonical.

The curriculum coverage matrix in `docs/AI_CURRICULUM_COVERAGE_MATRIX_2026-08-25.md` remains planning evidence for future Lab 15+ decisions.

## 9. Acceptance stages

### R0 — architecture and baseline

- freeze this document;
- confirm exact baseline SHA and current fourteen-app inventory;
- add no public behavior yet.

### R1 — v1.4 applet wrappers

- add v1.4 public wrappers for Labs 13 and 14;
- add native locale dropdowns;
- normalize version presentation;
- prove arithmetic/runtime state is unchanged.

### R2 — engagement parity

- add Lab 13 mechanism-focus journey;
- add Lab 14 action/gate journey;
- add browser tests for state invariance and four-locale behavior.

### R3 — suite-wide UX and curriculum navigation

- normalize public support-page language control to the dropdown pattern;
- verify legacy applets continue using the existing dropdown overlay;
- add Foundations / Modern Extensions navigation without duplicating applets;
- preserve mobile and keyboard behavior.

### R4 — release candidate

- build a deterministic fourteen-applet v1.4 Pages artifact;
- run all inherited v1.3 gates plus new v1.4 gates;
- perform adversarial browser checks at desktop and 390 px mobile widths;
- require zero page/console errors;
- update v1.4 release metadata only after the candidate behavior is frozen.

## 10. Release gate

Lab 15 remains blocked until the v1.4 product-quality candidate passes the complete inherited verification stack and the new v1.4 UX/state-preservation gates on one exact head.

A later Lab 15 planning decision should use the coverage matrix rather than treating the provisional lab numbering as frozen.