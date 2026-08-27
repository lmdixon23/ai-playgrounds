# AI Playgrounds Applet Design System and Minimum Feature Contract

**Status:** active v1.8.0 contract
**Scope:** every current and future public learner applet unless a documented concept-specific exception is approved.
**Purpose:** prevent visual, interaction, accessibility, localization, catalogue, and release drift as new labs are added.

The [v1.7.2 parity addendum](APPLET_DESIGN_SYSTEM_V1_7_2_ADDENDUM.md) is normative for mature header actions, Share/Embed, settings export, skip links, discovery metadata, shared theme migration, and the distinction between product-shell parity and concept-specific learning bodies.

## 1. Governing principle

AI Playgrounds is a family of concept-specific simulations, not fifteen unrelated microsites. A new lab may invent the visualization that its mechanism requires, but it must inherit the same outer product language and minimum learner-support contract.

The design system therefore standardizes the **shell, interaction promises, metadata, accessibility, localization, classroom surfaces, provenance, and QA**, while leaving the internal visualization concept-specific.

The default rule is:

> **Standardize what learners should not have to relearn; specialize what the AI mechanism genuinely requires.**

A new lab may diverge only when the shared pattern would misrepresent the concept, increase cognitive load, or materially harm usability. Every exception must be named in its integration audit and covered by tests.

---

# 2. Product invariants

Every public learner applet must satisfy all of the following.

1. **One primary mechanism.** The lab has one identifiable conceptual center rather than a survey of unrelated controls.
2. **Meaningful first state.** Opening the page shows a phenomenon worth inspecting without requiring setup.
3. **Direct manipulation.** At least one learner action changes a causally meaningful model parameter/state.
4. **Visible consequence.** The resulting state change is inspectable, not hidden behind prose alone.
5. **Explicit model boundary.** The applet states what is simplified, omitted, simulated, or toy-scale.
6. **Predict-before-reveal where useful.** If the mechanism supports a meaningful misconception check, the learner can commit a prediction before seeing the decisive state.
7. **Fast recovery.** Reset/retry paths are obvious and should not erase unrelated learner work unexpectedly.
8. **No account/backend dependency.** Core learning behavior works as a static browser artifact.
9. **Offline-ready applet artifact.** A downloaded learner applet remains usable without a network connection except for clearly optional external links.
10. **Evidence discipline.** Software checks establish implementation behavior only; they do not imply learning gains, adoption, preference, equity, or accessibility conformance.

---

# 3. Standard public applet shell

The *outer shell* is mandatory. Internal lab layouts may differ.

## 3.1 Header

Every public applet must expose the same conceptual header components in this order:

1. **Back to AI Playgrounds** link.
2. **Applet title** (`h1`).
3. Optional one-sentence subtitle/descriptor when it materially helps orientation.
4. **Language selector** using the shared native-select presentation.
5. **Theme control** when dark mode is supported by the suite release.
6. **Reset** action.
7. Any applet-specific high-level action only after these shared controls.

The header should use the suite shell classes/tokens (`page-header`, header utility/main/action group or the current successor tokens) rather than creating an unrelated hero/navigation system.

The public header must not expose internal development labels such as `R4`, `R6`, `candidate`, `prototype`, or old release badges.

## 3.2 TL;DR / orientation

A compact orientation block is expected when the mechanism is not self-evident. It should answer:

- what the learner can manipulate;
- what they should watch;
- what the visualization does **not** prove.

Do not repeat the entire essay or controls manual in the header.

## 3.3 Main interactive region

The interactive mechanism should appear before long explanatory prose.

Required properties:

- bounded width and responsive reflow;
- no page-level horizontal overflow at supported viewports;
- controls remain operable at 200% text enlargement;
- critical state is not encoded by color alone;
- every dynamic visual relation needed for the core learning task has a text-equivalent state or table/list alternative where practical.

## 3.4 Explanation / model-fidelity region

Every applet must provide enough prose to explain:

- the mechanism represented;
- the central mathematical/computational relation;
- at least one common misconception where relevant;
- what the simplified model leaves out.

The prose may be shorter for a very simple lab and longer for mechanisms such as Transformers or agent runtimes.

## 3.5 Footer / provenance

Every public applet must expose the same provenance family:

- `AI Playgrounds`;
- current release version;
- Home;
- Curriculum;
- Teacher Pack;
- Source;
- Citation / research context.

Applet-specific sources may also be linked, but the suite-level provenance must not disappear.

---

# 4. Catalogue metadata contract

Every applet record included in the public catalogue must supply the complete schema below. Missing fields are a release-blocking error; UI code must also fall back safely rather than rendering literal `undefined`.

Required fields:

- `slug`
- `icon`
- `category`
- `category_en`
- `category_zh`
- `category_vi`
- `category_es`
- `title`
- `title_zh`
- `title_vi`
- `title_es`
- `desc`
- `desc_zh`
- `desc_vi`
- `desc_es`
- `time`
- `level`
- `featured`
- `featured_zh`
- `featured_vi`
- `featured_es`
- `accent`
- `accent_name`
- `course_order`
- `showcase_order`
- `course_phase`
- `keywords` (array)

Optional fields may extend the record but cannot replace required fields under alternate names such as `description` instead of `desc`.

## 4.1 Search vocabulary

`keywords` should contain likely teacher/learner search terms that may not occur in the card prose:

- algorithm names and acronyms;
- common alternate spellings;
- mathematical terms;
- textbook vocabulary;
- misconception vocabulary when useful.

Search should index all four locale fields plus English keywords.

---

# 5. Localization contract

## 5.1 Learner applets

At the current product boundary, all learner applets must support:

- English (`en`)
- Simplified Chinese (`zh` / `zh-Hans`)
- Vietnamese (`vi`)
- Spanish (`es`)

Support-page language claims are controlled separately by `PUBLIC_SURFACE_LOCALE_MATRIX.md`.

## 5.2 Language selector

- Use one native `<select>` presentation, not four persistent language buttons.
- Display self-names: `English`, `简体中文`, `Tiếng Việt`, `Español`.
- Minimum touch height: 44 CSS px on coarse-pointer layouts.
- Do not nest a second bordered square control inside a bordered language-switch shell.
- The current locale must be encoded in `document.documentElement.lang` and the shareable URL (`?lang=`) where the surface supports it.

## 5.3 Reversibility

Every applet must pass round trips, not merely one-way translation:

- EN → ZH → EN
- EN → VI → EN
- EN → ES → EN
- ZH → VI → ZH where the implementation architecture makes this meaningful

Round-trip checks cover at minimum:

- visible `h1` title;
- page `<title>`;
- principal control labels;
- dynamic state labels involved in the core task;
- Guided Challenge text/state;
- learner response packet headings;
- ARIA labels and placeholders that are localized.

A locale overlay must retain an immutable/current English source representation rather than learning its source text from already translated DOM content.

## 5.4 State preservation

Changing language must not silently:

- restart an experiment;
- change random seed;
- change active challenge;
- clear a committed prediction;
- alter numerical model state;
- erase response-packet text.

If a legacy language handler rebuilds state, the localization bridge must suppress or safely reconstruct that mutation and prove equivalence with tests.

---

# 6. Theme and visual tokens

Applets should inherit the current suite visual primitives rather than inventing unrelated chrome.

Minimum token families:

- background;
- foreground;
- muted text;
- card/surface;
- border;
- soft/subtle surface;
- applet accent;
- focus indicator;
- semantic success/warning/error if needed.

Concept-specific colors are permitted inside a visualization. Shared controls/header/footer should retain the suite’s typography, radii, spacing rhythm, focus treatment, and surface hierarchy.

Dark mode, when present, must preserve semantic distinctions and not rely on naïve inversion of canvas/SVG content.

---

# 7. Required learning components

A lab does not need to display every component simultaneously, but the current suite contract expects these capabilities unless a concept-specific exception is recorded.

## 7.1 Explore mode

Learner can directly manipulate the mechanism without being forced through a worksheet.

## 7.2 Guided Challenge

When a concept has a meaningful predictable state:

1. prepare/choose a case;
2. hide the decisive result;
3. commit prediction;
4. reveal mechanism;
5. compare prediction with state/evidence;
6. reset/retry or transfer.

A Guided Challenge should not merely be a multiple-choice quiz disconnected from the visual mechanism.

## 7.3 Scenario / example gallery

Provide a small set of cases when contrasting scenarios meaningfully reveal the concept. Do not add a gallery solely for consistency if one carefully chosen initial state is better.

## 7.4 Visual explanation

Hidden structure should become inspectable through stepping, tracing, comparison, annotation, or direct manipulation. Decorative animation alone does not satisfy this component.

## 7.5 Key terms / misconception support

Expose the vocabulary learners need for the mechanism, and name high-value misconceptions where appropriate.

## 7.6 Student response packet

For classroom-capable labs, the local response surface should support the inquiry spine:

`Predict → Observe → Explain → Transfer`

Responses remain on the learner device until the learner/teacher deliberately exports or submits them through another system.

## 7.7 Quick Assign

Level 1 activities are approximately 10–15 minutes and reuse native applet machinery rather than duplicating a second worksheet system.

A Quick Assign must have:

- stable ID;
- explicit objective;
- canonical deep link;
- predictable classroom mode;
- teacher look-for;
- bounded completion time;
- locale boundary recorded in the registry.

## 7.8 Activity Packs

Level 2 activities are 30–45 minute ready-to-assign resources. They may exist only for selected labs; absence is not a lab defect.

---

# 8. Interaction and recovery contract

Every shared interaction must be tested as a state transition rather than only for control presence.

Minimum pattern:

`initial state → learner action → expected state → recovery/undo/reset path → focus/state consistency`

Examples:

- opening/closing a disclosure returns focus sensibly;
- reset does not leave stale visual/state text;
- a missed touch on a dense visualization does not trigger a destructive unrelated action when a tolerant selection rule is feasible;
- changing modes does not silently erase learner responses;
- share/copy feedback returns to its normal state.

This contract is derived from the PWP Notebook interaction architecture and is now part of AI Playgrounds’ release assurance.

---

# 9. Accessibility-oriented minimums

These are engineering requirements under tested conditions, not a claim of WCAG conformance.

## 9.1 Keyboard

- all essential controls keyboard-operable;
- logical focus order;
- no positive `tabindex` unless an audited exception exists;
- visible focus indication;
- modal/dialog/disclosure focus returns appropriately.

## 9.2 Non-color information

Color can reinforce state but cannot be the sole representation of:

- selected/active state;
- sign;
- pass/fail;
- class;
- pruning/visited status when that status is required for the task.

Use labels, values, patterns, text, icons, or structural differences as redundant channels.

## 9.3 Motion

`prefers-reduced-motion: reduce` must remove nonessential transitions/animation while preserving the complete mechanism and controls.

## 9.4 Text-equivalent state

Where a visual encodes essential numerical or logical state, provide an inspectable text/table/summary representation sufficient to understand the current result.

## 9.5 Touch

- shared controls target approximately 44 px on coarse pointer where feasible;
- custom visualization targets must have an equivalent/tolerant selection strategy when the drawn mark itself is too small;
- a near miss should not unexpectedly perform a destructive secondary action.

## 9.6 Text enlargement

At 200% text enlargement, the core task remains operable without loss of required controls/content.

---

# 10. Responsive contract

Every final public applet must be checked at least at:

- desktop: ~1366×900;
- classroom/projector: 1280×720;
- tablet portrait: 768×1024;
- split/narrow desktop: ~640×900;
- phone portrait: 360–390×740–844;
- phone landscape: ~844×390.

Required results:

- no page-level horizontal overflow;
- no clipped essential control;
- no fixed-width sub-control defeating outer wrapping;
- tables/trees/matrices use intentional local scrolling where necessary;
- language expansion does not push the active control outside the viewport.

Final-composition QA must inspect `_site`, not only source applet files, because generated wrappers are part of the released product.

---

# 11. Offline and dependency contract

Core learner interactions should not require:

- a server round trip;
- authentication;
- CDN availability;
- third-party model/API calls;
- analytics availability.

Optional external Source/Citation links may require a network.

If an applet intentionally uses an external dependency in the future, that is a design-system exception requiring:

- documented pedagogical necessity;
- blocked-network failure behavior;
- privacy/security review;
- a fallback or explicit online-only label.

---

# 12. Analytics and privacy contract

The public GitHub Pages build may collect only the coarse events defined in `ANALYTICS_AND_PRIVACY.md`.

Prohibited analytics payloads include:

- learner answers;
- experiment parameter values;
- names/emails;
- exact location;
- persistent cross-site IDs;
- student-specific campaign codes.

Offline/local copies send no analytics.

New labs must be automatically included in the analytics-coverage gate rather than manually remembered.

---

# 13. Search/discovery contract

The public catalogue must never display literal `undefined`, `null`, or missing-card artifacts.

Card rendering must:

1. validate the complete manifest schema at build time;
2. use safe English fallback at runtime as defense in depth;
3. index all locale fields and the keyword list;
4. include common textbook acronyms/aliases;
5. preserve deep links with locale/mode parameters.

Filters and search results must continue to work when a new category is introduced; a new applet category cannot be absent from the filter registry.

---

# 14. Release provenance contract

Every release must bind:

- source commit;
- deterministic public composition;
- current version metadata;
- exact tag;
- release object;
- Pages deployment;
- final verification receipt.

A public page must not present stale current-release counts or language claims. Historical release notes may preserve old counts and are excluded from currency rewrites when clearly scoped to their historical version.

---

# 15. Final-composition QA contract

A release is not complete until QA has built the exact `_site` artifact and checked the generated pages.

Minimum suite-level checks:

1. **Manifest schema:** every public applet has every required catalogue field.
2. **No undefined UI:** no public page/card includes `undefinedundefined`, visible `undefined`, or unresolved template placeholders.
3. **Applet count:** manifest, landing copy, JSON-LD, curriculum, release metadata, and public inventory agree.
4. **Language controls:** learner applets expose four languages; support-page controls match their declared locale matrix.
5. **Locale reversibility:** at minimum h1/title round trips VI→EN and ES→EN for every learner applet.
6. **Shared shell:** every public applet has the standard outer header/footer components or a documented exception.
7. **Responsive:** required viewport matrix over the final composition.
8. **Focus/reduced motion/text enlargement:** required HCI matrix.
9. **Search vocabulary:** representative aliases/acronyms return the correct applet.
10. **Quick Assign registry:** active IDs resolve to canonical classroom surfaces.
11. **Local references:** all generated relative links/assets resolve.
12. **Analytics coverage:** every public HTML surface expected to be measured has the privacy wrapper exactly once.
13. **Version provenance:** current public surfaces expose the release version, not a prior current version.

---

# 16. Concept-specific exception process

A new lab may diverge from a shared component when the shared component would harm the lesson.

The integration audit must record:

- component being omitted/changed;
- pedagogical or technical reason;
- alternative affordance;
- accessibility/recovery implications;
- QA required for the exception.

Examples of legitimate exceptions:

- a matrix-heavy Transformer view may use locally scrollable tables rather than the spatial diagram pattern of Pathfinding;
- an agent runtime may need an ordered pipeline instead of animation controls;
- Minimax may keep a tree locally scrollable rather than compress labels below legibility.

An exception is not:

> “the new lab was built later and happened to use a different header/footer.”

---

# 17. Future-lab implementation checklist

Before a new lab can enter public integration:

- [ ] Learning objective and misconception are explicit.
- [ ] Mechanism is formally/numerically verified against an independent reference where feasible.
- [ ] Complete catalogue metadata schema exists.
- [ ] Search keywords include acronyms and textbook terms.
- [ ] EN source is frozen before secondary locale work.
- [ ] ZH/VI/ES semantics pass protected-term/placeholder checks.
- [ ] EN↔ZH/VI/ES round trips preserve title and model state.
- [ ] Standard public header is present.
- [ ] Standard public provenance footer is present.
- [ ] Shared language selector is present.
- [ ] Theme/reset behavior is consistent.
- [ ] Evidence/model boundary is visible.
- [ ] Explore mode is usable immediately.
- [ ] Guided Challenge exists when mechanism-appropriate.
- [ ] Text-equivalent state exists for essential dynamic content.
- [ ] Keyboard/focus/reduced-motion behavior is tested.
- [ ] Mobile portrait and landscape are tested.
- [ ] 640px split view and 1280×720 classroom view are tested.
- [ ] 200% text enlargement is tested.
- [ ] Final `_site` composition is tested, not only source/candidate HTML.
- [ ] Analytics/privacy coverage is automatic.
- [ ] Release metadata/counts/curriculum are updated from one source of truth.
- [ ] A no-change/adversarial review confirms that extra visuals/features are mechanism-justified.

---

# 18. Governance

This file is a **minimum contract**, not a visual-design prison.

When future evidence shows that a shared pattern is harmful, update the contract intentionally and migrate the relevant labs through a canary process. Do not let the contract drift implicitly through one-off fixes.

The release arbiter should prefer, in order:

1. conceptual correctness;
2. learner clarity/recovery;
3. accessibility-oriented operability;
4. cross-lab transfer/consistency;
5. responsive/offline reliability;
6. visual polish;
7. implementation convenience.

If a proposed standardization damages a mechanism’s correctness or clarity, the mechanism wins and the exception is documented.
