# AI Playgrounds v1.9 Product Coherence and Human Validation Plan

Status: planning baseline

Planning branch: `planning/v1.9-product-coherence`

Baseline: current `main` after v1.8.1 publication and release automation hardening

## 1. Release thesis

v1.9 is a quality release, not a feature release.

The suite already demonstrates broad mechanism coverage, deterministic algorithm verification, four learner locales, offline single file operation, Level 1 Quick Assign coverage for every lab, responsive/browser testing, privacy bounded analytics, release provenance, and a mature evidence boundary.

The highest remaining product risk is no longer insufficient feature coverage. It is accidental source and visual drift, first use friction, incomplete human validation, maintenance complexity, accessibility evidence depth, and insufficient external adoption evidence.

Therefore v1.9 freezes new labs and optimizes the complete existing product.

No Lab 16 is promoted while the v1.9 quality gates are open. The RAG candidate remains an intentionally unscheduled future extension.

## 2. Objective function

Optimize, in order:

1. mechanism correctness and epistemic fidelity;
2. learner comprehension and recoverability;
3. cross lab product coherence;
4. accessibility and input modality robustness;
5. educator preparation and assignment usability;
6. deterministic release integrity;
7. maintainability and contributor clarity;
8. performance and responsive quality;
9. discoverability and uptake;
10. feature expansion.

A change that improves visual uniformity while weakening mechanism understanding is rejected.

A change that increases engagement while introducing an unsupported mental model is rejected.

A change that improves developer convenience while weakening deterministic release evidence is rejected.

## 3. Governing product rule

Standardize everything a learner or educator should not have to relearn from lab to lab.

Preserve differences that are necessary to expose the actual mechanism.

This produces two classes of design decisions.

### 3.1 Universal product primitives

These should converge across all relevant labs unless a documented accessibility or mechanism exception exists:

- page width and horizontal gutters;
- header composition;
- theme and language controls;
- Share, Embed, export, and Reset hierarchy;
- typography roles;
- spacing scale;
- border radius families;
- ordinary control heights;
- focus treatment;
- semantic state colors and non color cues;
- scenario card structure;
- featured experiment structure;
- Quick Assign placement and disclosure pattern;
- key term structure;
- explanation section hierarchy;
- accessibility/help disclosure;
- provenance/footer treatment;
- responsive breakpoint behavior;
- dark theme contract;
- locale switching behavior;
- shareable state conventions;
- local response persistence;
- analytics privacy boundary.

### 3.2 Mechanism specific surfaces

These may remain structurally and visually different when the difference carries conceptual meaning:

- graph, grid, tree, network, matrix, chart, and canvas geometry;
- animation or trace semantics;
- algorithm specific controls;
- state quantities and comparison panels;
- sequence or timeline representation;
- interaction gestures required to expose the mechanism;
- domain specific warnings and model fidelity notes;
- number and arrangement of concept specific data panels.

Mechanism specific does not mean exemption from accessibility, spacing, focus, responsive, localization, theme, or evidence requirements.

## 4. Workstream sequence

The order is deliberate. Later phases may depend on evidence produced earlier.

### Phase 0: freeze and baseline

1. Freeze new lab implementation.
2. Record exact current main SHA and current release artifact.
3. Preserve immutable release tags and historical builders.
4. Capture current structural/browser evidence.
5. Inventory all current source of truth files, generated artifacts, and version layered transforms.
6. Inventory open and stale branches.
7. Record current homepage, catalogue, support page, and lab screenshots as diagnostic evidence only, not final baselines.

Exit gate: current behavior and release boundary are reproducible before refactoring begins.

### Phase 1: canonical source architecture

Owner issue: #47

Goal: remove architectural drift without visible redesign.

Create canonical build time sources for design tokens, product shell primitives, support page primitives, lab metadata, locales, Quick Assigns, and release metadata.

The public output remains self contained offline HTML. v1.9 does not introduce a runtime framework, package dependency in the learner artifact, account system, backend, or external API requirement.

Behavior preserving refactor requirements:

- algorithms unchanged;
- learner state unchanged;
- locale round trips unchanged;
- Quick Assign response semantics unchanged;
- Share, Embed, export, theme, and Reset behavior unchanged;
- analytics payload boundary unchanged;
- final artifact reproducible;
- every shared primitive has one canonical source;
- every deliberate exception is named and documented.

Exit gate: exact functional parity plus deterministic builds.

### Phase 2: design token and component contract

Part of #47, consumed by #48 and #49.

Define canonical roles rather than arbitrary local values.

#### Spacing

Use a small explicit scale for micro, compact, standard, section, and major section spacing. Existing values should migrate by semantic role, not by mechanically replacing every number.

#### Typography

Define roles for caption, metadata, small body, body, emphasized body, panel heading, section heading, page heading, and display heading.

#### Controls

Define ordinary, compact, primary, secondary, destructive/reset, disclosure, selected, disabled, and touch target behavior.

House preference: ordinary interactive controls should target at least 44 CSS px in coarse pointer contexts when the layout permits, even though the WCAG 2.2 AA minimum target criterion may also be satisfied through a smaller target with permitted spacing conditions.

#### Focus

Use a clearly visible focus indicator across the suite. The preferred house standard is at least a 2 CSS px perimeter equivalent with sufficient visual contrast.

#### Semantic states

Create consistent information, success, warning, error, selected, visited, pruned, masked, disabled, and unavailable roles where they are semantically applicable. Color must not be the only carrier of concept defining state.

#### Layout

Define canonical page width, readable text width, visualization width behavior, gutters, section boundaries, and breakpoint responsibilities.

Exit gate: no new arbitrary product shell styling without a named token or documented mechanism exception.

### Phase 3: whole suite visual census and regression

Owner issue: #48

The old twelve versus modern three comparison is retired as the primary mental model. v1.9 evaluates all fifteen labs simultaneously.

#### Required census states

For each lab capture at least:

- desktop light fresh;
- desktop dark fresh;
- phone portrait light fresh;
- phone portrait dark fresh;
- one translated locale with long labels;
- one active mechanism state;
- Quick Assign open where applicable.

Add tablet/split view and enlarged text captures where they expose a real layout boundary.

#### Compare

- header geometry;
- preference/action order;
- title and introductory spacing;
- featured experiment treatment;
- scenario card dimensions;
- control grouping;
- panel padding;
- button hierarchy;
- field labels;
- text wrapping;
- mechanism canvas containment;
- Quick Assign placement;
- explanation reading width;
- term cards;
- accessibility section;
- footer;
- semantic state styling;
- dark theme;
- focus visibility;
- responsive collapse order.

#### Regression strategy

Use visual baselines in a fixed browser, operating system, viewport, font, theme, locale, and seed/state environment.

Baseline stable structural regions. Mask or normalize volatile mechanism areas when state variation is expected.

Disable animations, transitions, and caret noise during capture.

A baseline update is a reviewed product change. CI never rewrites baselines automatically to obtain a pass.

Exit gate: every unexplained cross lab discrepancy is fixed or documented as a mechanism required exception.

### Phase 4: accessibility engineering audit

Owner issue: #49

Target WCAG 2.2 AA for supported public interactions while retaining stronger house requirements where useful.

Audit all 15 labs and the principal learner/teacher routes.

Required evidence includes:

- keyboard only operation;
- logical focus order;
- focus visible;
- focus not obscured;
- target sizing and spacing;
- headings and labels;
- name, role, value;
- status messages;
- text enlargement to at least 200 percent;
- narrow reflow;
- reduced motion;
- non color state distinction;
- text equivalent mechanism state;
- alternatives for hover or pointer only relations;
- error identification and recovery;
- locale and document language correctness.

Human accessibility passes must include keyboard, phone, 200 percent zoom, reduced motion, and at least one representative desktop screen reader workflow.

Do not claim formal conformance merely because engineering tests pass. Claims follow evidence.

Exit gate: no P0 or P1 accessibility defect remains.

### Phase 5: human learner and educator validation

Owner issue: #50

The existing v1.5 planning protocol is useful provenance but is obsolete as a product baseline. Port it to the current release and expand it for the complete Quick Assign and modern lab experience.

#### Learner formative cycle

Recommended first cycle: 8 to 12 first time learners.

Measure:

- time to first meaningful action;
- mechanism relevant versus administrative first action;
- prompting;
- prediction before reveal;
- mechanism explanation;
- cause attribution;
- transfer to a changed case;
- voluntary exploration;
- false mental model severity;
- navigation/control friction;
- accessibility and locale condition.

#### Educator formative cycle

Recommended first cycle: 4 to 6 educators not involved in development.

Measure:

- time from homepage to selecting a usable activity;
- preparation time;
- learning objective clarity;
- prerequisite clarity;
- Quick Assign discoverability and usability;
- Share, print/export, Reset, and offline friction;
- understanding of model limitations;
- willingness to reuse;
- classroom needs that are not already solved.

#### Locale validation

Use fluent ZH, VI, and ES readers for active tasks. Machine parity is not evidence of naturalness.

Escalate repeated technical term errors, ambiguous dynamic text, altered epistemic meaning, and control labels that create action errors.

#### Stop rules

Reopen a design when:

- two or more independent users form the same severe false model from the same surface;
- most users cannot identify a meaningful first action without prompting;
- prediction before reveal is routinely bypassed because the result is already visible;
- the core relation disappears under a supported accessibility condition;
- translation changes the mechanism claim;
- educators cannot reach a teachable activity without developer intervention;
- attention is captured by a feature users cannot connect to the mechanism.

Do not redesign based on isolated aesthetic preference.

Exit gate: accepted visible redesigns are traceable to repeated human or structural evidence.

### Phase 6: homepage, catalogue, and teacher conversion

Owner issue: #51

Only after canonical architecture is stable should the public entry experience change substantially.

Optimize three user intents.

#### Learn

Provide a fast path into a curated first experiment.

Do not require a new learner to understand all fifteen choices before experiencing the product.

#### Teach

Provide a fast path into a canonical 10 to 15 minute Quick Assign with learning objective and teacher context.

#### Explore

Retain full catalogue, curriculum, evidence, offline/reuse, research, and GitHub access for users seeking depth.

Candidate improvements must be tested rather than assumed:

- direct Explore and Teach actions on catalogue cards;
- deterministic concept thumbnails based on actual lab states;
- concept family and level filters;
- activity length and coding prerequisite filters;
- curated first lab recommendations;
- clearer teacher preparation cues.

Exit gate: human task measures improve or remain non worse without creating new conceptual errors.

### Phase 7: current verification and performance

Owner issue: #52

Create one manifest driven current verification command while preserving historical evidence.

Suggested stages:

1. build;
2. structure;
3. algorithms;
4. localization;
5. accessibility;
6. browser/responsive;
7. visual regression;
8. privacy/analytics;
9. metadata/provenance;
10. performance;
11. release boundary.

Generic current tests must derive app count, locale set, and release state from canonical manifests. Historical tests may retain historical expectations.

#### Performance targets

Use current Core Web Vitals good thresholds for field interpretation when enough field data exist:

- LCP at or below 2.5 seconds at the 75th percentile;
- INP at or below 200 ms at the 75th percentile;
- CLS at or below 0.1 at the 75th percentile.

Also create deterministic repository budgets for generated page size, media weight, startup work, representative interaction latency, and unexpected external runtime dependencies.

Exit gate: one current command and one CI release gate represent the current product contract clearly.

### Phase 8: repository governance and contributor quality

Owner issue: #53

Align repository settings with the release assurance model.

Recommended main protection:

- pull request required;
- canonical Verify gate required;
- force pushes blocked;
- deletion blocked;
- conversation resolution required;
- strict up to date requirement when appropriate for exact release verification;
- administrator bypass minimized where feasible.

Do not require fake independent approval while the repository has one practical maintainer. Add genuine review requirements when additional maintainers exist.

Prefer one documented merge strategy, normally squash for bounded product work.

Enable merged branch cleanup when safe.

Migrate useful material from the obsolete usability planning branch and then remove the obsolete branch if no unique evidence remains.

Create bounded contributor issues across localization, accessibility, curriculum, browser QA, visual regression, documentation, and small code improvements.

Exit gate: repository governance prevents concrete release failure modes and contributor entry points are credible.

### Phase 9: evidence led Activity Pack expansion

Owner issue: #54

Do not create thirteen additional Level 2 packs for symmetry.

Pilot a bounded set after educator feedback. Initial candidates are Pathfinding, Bayesian Networks, KNN, and Minimax, subject to replacement by stronger evidence.

Measure preparation time, classroom friction, reuse intent, mechanism explanation quality, and incremental value beyond Quick Assign.

Exit gate: suite wide expansion occurs only if pilot evidence demonstrates value and maintainability.

### Phase 10: adoption and external evidence

After the product coherence gates pass, run the existing distribution strategy as an experiment with explicit attribution boundaries.

Measure aggregate routes such as:

- landing page to applet launch;
- landing page to first substantive interaction;
- teacher resource opens;
- Quick Assign entry;
- resource downloads;
- repository outbound;
- campaign source where allowed.

Do not interpret visits or engaged tab sessions as unique people, classrooms, learning outcomes, or adoption by themselves.

Pair aggregate analytics with separately collected educator feedback.

The main adoption question is whether a visitor successfully reaches a meaningful use case, not whether traffic increases.

## 5. PR architecture

Avoid one giant v1.9 PR. Use a gated sequence.

### PR A: planning and baseline

Documentation only. Freeze scope, record architecture map, migrate human protocol planning, define quality metrics.

### PR B: canonical source architecture

Behavior preserving only. No intentional visual redesign.

### PR C: design tokens and shared primitives

Still behavior preserving in meaning and interaction. Small visual normalization is allowed only when it removes accidental drift and is separately enumerated.

### PR D: visual census and regression infrastructure

Add baselines and evidence generation. Avoid broad redesign in the same PR.

### PR E: accessibility corrections

Fix findings through shared primitives first. Lab local patches require a documented reason.

### PR F: human evidence driven product corrections

Only findings meeting the evidence threshold enter this PR. Include finding to change traceability.

### PR G: homepage, catalogue, and teacher flow

Use validated task measures and preserve performance/accessibility gates.

### PR H: verification and performance consolidation

One current verification entry point plus budgets. Historical evidence retained.

### PR I: repository/documentation/contributor cleanup

README, contribution surface, current docs, branch hygiene related source changes. Repository settings may require separate administrative action.

### PR J: v1.9 release candidate

No new features. Exact final artifact audit, all P0/P1 issues closed, reproducible build, final human regression spot checks, metadata, publication, and portfolio freshness.

Activity Packs may ship later as v1.9.x or a separate content release if they are not mature when the product coherence release is ready.

## 6. Release gates

v1.9 cannot publish until all of the following are true.

### Correctness

- all algorithm reference tests pass;
- all cross runtime parity tests pass where maintained;
- no mechanism semantics changed without explicit new evidence and tests.

### Determinism

- two clean builds are byte identical;
- generated inventory matches the declared manifest;
- final inline executable scripts and structured data parse/compile.

### Visual coherence

- all fifteen labs appear in the visual census;
- unexplained shell differences are zero;
- visual baselines pass in the canonical CI environment.

### Accessibility

- WCAG 2.2 AA engineering audit complete for supported primary surfaces;
- no P0/P1 accessibility defect remains;
- human keyboard, zoom, mobile, reduced motion, and representative screen reader passes complete.

### Localization

- EN/ZH/VI/ES semantic and state parity pass;
- human naturalness review covers high risk changed surfaces;
- no locale changes the mathematical, causal, or epistemic claim.

### Human usability

- no repeated severe false mental model remains unresolved;
- first action failures are below the defined escalation threshold on tested routes;
- educator Quick Assign flow can be completed without developer guidance by the tested educators;
- every accepted finding has a disposition.

### Privacy

- learner text, answers, experiment state, and identifying data remain excluded from analytics;
- canonical hosted analytics payload remains allow listed and bounded;
- offline/local copies remain analytics silent.

### Performance

- deterministic page and media budgets pass;
- no major responsive regression;
- field Core Web Vitals are interpreted against the current good thresholds when sufficient data exist, without overstating sparse data.

### Repository and release integrity

- current Verify gate passes on the exact candidate SHA;
- Pages artifact corresponds to the exact verified SHA;
- release metadata is current;
- portfolio freshness checks pass;
- branch/release rules prevent accidental bypass.

## 7. Deferred work

The following are not v1.9 objectives unless evidence changes the priority:

- RAG / Lab 16;
- accounts;
- cloud synchronization;
- grading backend;
- learner profile tracking;
- broad Activity Pack completion;
- decorative animation expansion;
- framework migration for its own sake;
- redesign toward pixel identity across mechanism bodies.

## 8. Decision standard after v1.9

Only resume major feature expansion after answering these questions with evidence:

1. Can first time learners identify the intended mechanism action and explain the resulting state change?
2. Can educators reach and run a useful activity without developer intervention?
3. Are the fifteen labs perceived and operated as one coherent product?
4. Are supported input, zoom, motion, viewport, theme, and locale states robust?
5. Is current development maintainable through canonical sources rather than release layering?
6. Does the public entry experience convert discovery into meaningful interaction?
7. Are remaining feature requests stronger than the value of further quality refinement?

If the answer to these is yes, RAG and other future labs can be evaluated from a substantially stronger product foundation.