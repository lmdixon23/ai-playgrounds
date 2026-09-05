# AI Playgrounds v1.9 accessibility audit protocol

Status: operational accessibility engineering protocol for issue #49.

Target: WCAG 2.2 Level AA for the supported public interaction surfaces, plus stronger AI Playgrounds house requirements where they materially improve learner usability.

This document defines an engineering target and audit method. AI Playgrounds must not claim formal WCAG 2.2 AA conformance until every applicable Level A and AA success criterion has been evaluated on the declared conformance scope and the evidence supports that claim.

## 1. Audit principles

Accessibility is evaluated as preservation of the instructional relation, not only technical operability.

For an AI Playground, a passing keyboard or screen-reader path must let the learner recover the concept-defining state relation that the visual learner can use.

Examples:

- Pathfinding must expose frontier/explored/path state rather than only a focusable Run button.
- Convolution must expose the active patch, kernel values, multiplication/sum relation, and output location.
- Q-Learning must expose state, action, reward/transition, update, and resulting values/policy.
- Transformer must expose the causal attention computation and probability output without requiring inspection of a color matrix.
- Minimax must expose evaluated/pruned state and backed-up values without requiring visual tree geometry.

## 2. Declared audit scope

Audit every current public learner lab:

1. Pathfinding Visualizer
2. Hill Climbing and Simulated Annealing
3. Wumpus World
4. CNF/SAT
5. Bayes Rule
6. Bayesian Network
7. KNN
8. Overfitting
9. Tiny Neural Network
10. K-Means
11. Convolution
12. Q-Learning
13. Transformer Language Modeling
14. Agent Tool Use and Context Protocols
15. Minimax and Alpha-Beta

Audit the primary public learner/teacher routes:

- homepage/catalogue;
- Teacher Pack;
- Curriculum;
- Student Lab Sheet;
- Activity Pack index;
- NN-1 Activity Pack;
- CNN-1 Activity Pack;
- quality/evidence page;
- research/citation page;
- release notes where it remains part of normal site navigation;
- 404 recovery route.

A future scope expansion requires another audit. A conformance statement cannot silently cover pages that were not tested.

## 3. Required states

For every lab, evaluate at minimum:

- initial state;
- featured experiment applied;
- one active scenario;
- Quick Assign closed;
- Quick Assign open with local response text;
- text-equivalent/accessibility state;
- light theme;
- dark theme;
- English;
- at least one long translated locale during layout audit;
- state after locale round trip;
- state after reset/recovery.

Mechanism-specific states must include the state most likely to stress accessibility, such as a dense KNN neighborhood, a long SAT trace, a large Minimax tree, a Transformer matrix, or a long Agent context/tool trace.

## 4. Test environments

### Browser automation environment

Use the same fixed Chromium environment as deterministic release and visual-regression testing where possible. Record exact browser version and runner image.

### Desktop human environments

Preferred human assistive-technology coverage:

- NVDA with current Firefox or Chrome on Windows;
- VoiceOver with Safari on macOS where available.

At least one experienced screen-reader user or reviewer should perform the core learner workflow on representative labs from every mechanism family.

### Mobile human environment

Preferred:

- TalkBack with Chrome on Android or VoiceOver with Safari on iOS;
- physical touch target and scrolling checks on an actual phone where feasible.

### Zoom and reflow

Test:

- 200 percent browser zoom;
- 400 percent zoom or equivalent 320 CSS px reflow condition for content that falls under WCAG reflow requirements;
- 390 px phone portrait;
- short phone landscape;
- split/narrow desktop condition.

### Motion

Test normal motion and `prefers-reduced-motion: reduce`.

## 5. Automation versus human judgment

Automated accessibility testing is a defect detector, not the conformance authority.

Each applicable criterion is classified as:

- automated primary;
- automated support plus human review;
- human primary;
- not applicable with rationale.

No criterion is marked PASS solely because an automated scanner reports no violations when the criterion requires interpretation.

## 6. WCAG 2.2 Level A and AA audit map

### 1.1.1 Non-text Content — A

Audit:

- SVG/canvas visualizations;
- icons with functional meaning;
- screenshots/thumbnails if introduced;
- graph/tree/matrix states.

Require text alternatives or equivalent programmatic state when the non-text content conveys instructional information.

Decorative graphics should not create redundant screen-reader noise.

### 1.2 media criteria

Current applets do not depend on prerecorded instructional audio/video for core operation. Mark individual media criteria N/A only after confirming that no current public media surface introduces an applicable requirement.

### 1.3.1 Info and Relationships — A

Check semantic grouping for:

- headings;
- labels and controls;
- fieldsets/groups where needed;
- tables/matrices when semantically tabular;
- scenario structure;
- Quick Assign prompts;
- teacher notes;
- status/state sections.

Visual proximity alone is insufficient.

### 1.3.2 Meaningful Sequence — A

DOM/read order must preserve instructional sequence when styling is removed.

Special attention:

- featured experiment → scenarios → Quick Assign → explanation;
- multi-column control/result layouts;
- Transformer computation sequence;
- Agent validation/authorization/execution sequence;
- Minimax tree explanation.

### 1.3.3 Sensory Characteristics — A

Instructions must not depend only on position, shape, color, or visual direction.

Avoid instructions such as use the green node or click the box on the right unless another programmatic/text identifier is provided.

### 1.3.4 Orientation — AA

Do not lock content to portrait or landscape unless the mechanism genuinely requires a specific orientation.

### 1.3.5 Identify Input Purpose — AA

Evaluate only forms that collect user information covered by the criterion. Ordinary algorithm parameters and anonymous lesson responses may be N/A; document the rationale rather than assuming.

### 1.4.1 Use of Color — A

No concept-defining distinction may use color alone.

Audit:

- visited/frontier/path states;
- class labels and neighbor sets;
- exact/sampled probability states;
- train/test lines;
- neural-network error/history;
- cluster assignment;
- convolution heat maps;
- Q-value/policy displays;
- SAT decision/conflict/learn states;
- Transformer mask/attention states;
- Agent gate states;
- Minimax evaluated/pruned/returned states.

### 1.4.2 Audio Control — A

Current product has no persistent autoplay audio. Confirm N/A per release.

### 1.4.3 Contrast Minimum — AA

Target:

- at least 4.5:1 for normal text;
- at least 3:1 for qualifying large text.

Measure both light and dark themes and translated states.

### 1.4.4 Resize Text — AA

At 200 percent text enlargement, require no loss of content or functionality and no need to reduce zoom to complete the learner task.

### 1.4.5 Images of Text — AA

Do not use images of text where actual text can present the same information except for legitimate exceptions.

### 1.4.10 Reflow — AA

At the applicable 320 CSS px width/equivalent zoom condition:

- no two-dimensional page scrolling for ordinary content;
- preserve function and meaning;
- allow necessary two-dimensional scrolling inside genuinely spatial mechanisms such as a wide game tree or matrix when that exception is justified and the text-equivalent state remains available.

A spatial visualization exception does not excuse the rest of the page from reflow.

### 1.4.11 Non-text Contrast — AA

Require at least 3:1 where applicable for visual information needed to identify controls, focus, selected state, graph/node boundaries, or instructional state.

### 1.4.12 Text Spacing — AA

Apply the standard text-spacing override and verify no clipping/loss of content or functionality.

### 1.4.13 Content on Hover or Focus — AA

Any additional content triggered by hover/focus must satisfy dismissible, hoverable, and persistent behavior where applicable.

KNN hover inspection is a high-priority case. An equivalent non-hover path must also exist when hover is not available.

### 2.1.1 Keyboard — A

Every functionality must be keyboard-operable unless an essential exception applies.

Audit all controls and all concept-defining interactions.

Canvas or drag interactions require an alternative keyboard route when the action is not essential as a path-dependent gesture.

### 2.1.2 No Keyboard Trap — A

Verify modals, disclosures, menus, sliders, canvas substitutes, and embedded/print surfaces do not trap keyboard focus.

### 2.1.4 Character Key Shortcuts — A

If any single-character shortcuts exist, verify the required disable/remap/focus behavior. Otherwise document N/A.

### 2.2.1 Timing Adjustable — A

Current core tasks should not expire. Audit any animation timers or transient challenge states to ensure they do not impose a user-completion time limit.

### 2.2.2 Pause, Stop, Hide — A

For moving/blinking/scrolling/auto-updating information that meets the criterion conditions, provide pause/stop/hide or ensure the motion is not presented in a way that invokes the criterion.

Reduced-motion support does not automatically satisfy this criterion.

### 2.3.1 Three Flashes or Below Threshold — A

No applet may create flashing content beyond the threshold.

### 2.4.1 Bypass Blocks — A

Provide effective skip/bypass behavior for repeated navigation/chrome.

### 2.4.2 Page Titled — A

Every public route has a descriptive title reflecting the actual lab/resource.

### 2.4.3 Focus Order — A

Keyboard focus order must follow the meaningful task sequence and must remain logical after disclosures open, locale changes, scenario application, and Quick Assign expansion.

### 2.4.4 Link Purpose in Context — A

Link purpose must be understandable from link text plus programmatic context.

### 2.4.5 Multiple Ways — AA

For pages in the site collection, provide appropriate multiple navigation methods such as catalogue/search, curriculum navigation, and direct route links. Single-step process pages may be evaluated under applicable exceptions.

### 2.4.6 Headings and Labels — AA

Headings and labels must describe topic or purpose, including technical controls whose abbreviations may otherwise be ambiguous.

### 2.4.7 Focus Visible — AA

Every keyboard-operable control must have an unambiguous visible focus indicator.

### 2.4.11 Focus Not Obscured Minimum — AA

When a component receives keyboard focus, it must not be entirely hidden by author-created content.

Explicitly test:

- sticky/expanded headers;
- open More menus;
- Quick Assign disclosures;
- long mobile pages;
- internal scroll containers;
- tree/matrix scrollers.

### 2.5.1 Pointer Gestures — A

Multipoint/path-based gestures require a single-pointer alternative unless the gesture is essential.

### 2.5.2 Pointer Cancellation — A

Avoid triggering irreversible actions on pointer-down where cancellation/undo requirements apply.

Reset/clear actions require particular scrutiny.

### 2.5.3 Label in Name — A

Visible control labels must be contained in the accessible name where applicable.

Test all four locales.

### 2.5.4 Motion Actuation — A

If device motion is ever used, provide an interface alternative and disable option. Current release is expected to be N/A; verify.

### 2.5.7 Dragging Movements — AA

Any functionality using drag must also be achievable with a single pointer without dragging unless dragging is essential.

Audit:

- point placement/movement;
- graph manipulation;
- sliders where browser-native keyboard/single-pointer behavior applies;
- any future draggable thumbnail/card behavior.

### 2.5.8 Target Size Minimum — AA

A pointer target must be at least 24 by 24 CSS px or satisfy a permitted spacing/equivalent/inline/user-agent/essential exception.

AI Playgrounds house standard:

- ordinary buttons, toggles, disclosure summaries, and primary form controls should target at least 44 CSS px in coarse-pointer contexts where feasible;
- any smaller target must be explicitly reviewed rather than silently relying on an exception.

### 3.1.1 Language of Page — A

The document language must match the active locale after initial load and every locale change.

Expected mappings include English, Simplified Chinese, Vietnamese, and Spanish.

### 3.1.2 Language of Parts — AA

Mark substantial text in another natural language where required. Machine identifiers, formulas, code, and standard acronyms should not be mislabeled as natural-language changes.

### 3.2.1 On Focus — A

Receiving focus must not unexpectedly change context.

### 3.2.2 On Input — A

Changing a form value must not unexpectedly navigate/change context without prior explanation where the criterion applies.

Algorithm-state updates are expected task behavior; unexpected page/context changes are not.

### 3.2.3 Consistent Navigation — AA

Repeated navigation appears in a consistent relative order unless the user initiates a change.

### 3.2.4 Consistent Identification — AA

Components with the same functionality across labs should be identified consistently.

This is directly coupled to #48 visual/product consistency.

### 3.2.6 Consistent Help — A

If a repeated help mechanism is present across multiple pages, keep it in a consistent relative location unless an exception applies.

### 3.3.1 Error Identification — A

Input errors must be identified in text where errors can occur.

### 3.3.2 Labels or Instructions — A

Provide necessary labels/instructions for algorithm parameters, response prompts, and state-editing controls.

### 3.3.3 Error Suggestion — AA

Where an input error is detected and a correction is known, offer a useful suggestion unless doing so would compromise the purpose/security.

### 3.3.4 Error Prevention Legal Financial Data — AA

Expected N/A for the current public product because it does not execute legal/financial transactions or persist user-controlled submissions of that class. Verify current scope.

### 3.3.7 Redundant Entry — A

If the same information is required again within the same process, auto-populate or make the prior value selectable unless an exception applies.

Review Quick Assign/local response flows rather than declaring N/A globally.

### 3.3.8 Accessible Authentication Minimum — AA

Current product requires no authentication. Mark N/A while that boundary remains true.

### 4.1.2 Name, Role, Value — A

All custom controls expose correct accessible name, role, current value/state, and changes.

Audit:

- custom tabs;
- disclosure menus;
- toggles;
- scenario selectors;
- custom visualization controls;
- generated modern-lab controls.

### 4.1.3 Status Messages — AA

Important non-focus status changes must be programmatically determinable through appropriate live/status semantics when the message meets the criterion.

Audit:

- copied/exported status;
- errors;
- simulation completion;
- prediction compare/reveal;
- Quick Assign state refresh;
- Agent gate outcomes;
- SAT result/conflict state;
- model-training completion where relevant.

## 7. Removed criterion note

WCAG 2.2 removes the obsolete WCAG 2.0/2.1 Parsing success criterion 4.1.1. Do not create a false current failure solely from a legacy 4.1.1 checklist.

HTML validity remains valuable as engineering QA and is already part of the release-integrity model.

## 8. AI Playgrounds stronger house requirements

These are product-quality requirements, not claims that WCAG AA itself requires the stronger threshold.

### 8.1 Coarse-pointer target size

Target at least 44 CSS px for ordinary interactive controls where feasible.

### 8.2 Focus appearance

Prefer a clearly visible focus indicator with at least a 2 CSS px perimeter-equivalent and strong contrast change. Where the implementation can meet the WCAG 2.2 AAA Focus Appearance geometry/contrast model without harming the design, treat that as the preferred house target.

### 8.3 Text-equivalent mechanism state

Every visual mechanism whose instructional information cannot be fully inferred from standard control labels must expose one canonical current text-equivalent state.

Do not create a stale duplicate state solely for accessibility.

### 8.4 No hover-only learning relation

Hover may enrich inspection but may not be the only way to obtain a concept-defining value or relation.

### 8.5 Reduced-motion semantic equivalence

Reduced motion must preserve event order and state transitions needed to understand temporal mechanisms.

### 8.6 Error recovery

Reset, clear, delete, or destructive local-draft actions must provide proportional recovery/guard behavior and must not be easy accidental adjacent targets.

## 9. Lab-specific accessibility invariants

### Pathfinding

Text state identifies start, goal, obstacles where relevant, explored/frontier/path state, algorithm, path/cost result, and completion status.

### Hill Climbing

Text state identifies current/best solution, cost, algorithm, step/restart context, and benchmark aggregates without relying on chart color.

### Wumpus World

Text state distinguishes actual learner-visible percepts from inferred/hidden world information.

### CNF/SAT

Trace text distinguishes decision, propagation, conflict, learned clause, backjump, branch result, and final SAT/UNSAT state.

### Bayes Rule

Prior, likelihood/evidence terms, normalization, and posterior remain readable as structured text.

### Bayesian Network

Graph structure/evidence/posterior and previous/current comparisons are available without graph position or color alone.

### KNN

Query point, selected neighbors, distances/weights, classification vote or regression calculation, and final prediction are available without hover/color alone.

### Overfitting

Model degree/regularization/sample settings and train/test metrics are available without requiring visual curve comparison alone.

### Tiny Neural Network

Inputs, activations/state, output, loss/error, and training/history summary are available without interpreting animated edges alone.

### K-Means

Point assignment, centroid coordinates/movement, iteration state, and convergence are available without cluster color alone.

### Convolution

Input patch coordinates/values, kernel, elementwise products or equivalent calculation, sum, and output location/value are available as text.

### Q-Learning

Current state/action/reward/next state/update and relevant Q/policy values are available without grid color/arrows alone.

### Transformer

Tokens/positions, attention score/mask/weight relation, output/logits/probabilities, and decoding choice are available without matrix color alone.

### Agent Tool Use

Proposed call, validation, authorization, execution, observation, context update, and stop/error state are distinguishable programmatically.

### Minimax

Node role/value, evaluation order, returned value, pruned/not-evaluated state, root action/value, and move-order comparison remain accessible without visual tree geometry.

## 10. Automated evidence

The current verification system should eventually include a dedicated accessibility stage under #52.

Automatable checks should include at minimum:

- document language;
- unique IDs and valid control associations;
- accessible names for interactive elements;
- keyboard reachability for custom controls;
- focus-visible computed styles;
- focus not fully obscured in tested states;
- target bounding boxes and spacing diagnostics;
- light/dark text contrast for stable representative surfaces;
- non-text control/state contrast where computable;
- 200 percent and 320 CSS px reflow overflow diagnostics;
- reduced-motion state equivalence markers;
- pointer/hover alternatives;
- text-equivalent state presence and update;
- status-message semantics;
- locale round-trip language/state preservation.

Automated scanners may be added as a supporting layer, but a scanner PASS never substitutes for manual criterion review.

## 11. Human keyboard audit

For every lab:

1. start at browser chrome then enter the page by keyboard;
2. use bypass/skip navigation;
3. reach theme, language, share/embed/export/reset controls;
4. operate featured experiment/scenario controls;
5. operate the core mechanism without a mouse where non-essential gestures are involved;
6. open and complete the Quick Assign path;
7. reach text-equivalent state;
8. recover/reset;
9. confirm focus remains visible and logical throughout.

Record any focus jump, hidden focus, keyboard trap, unavailable mechanism action, or mismatch between visible and accessible names.

## 12. Human screen-reader audit

For representative AT/browser combinations:

- navigate by headings/landmarks;
- identify the lab and primary mechanism;
- discover and operate controls;
- understand current values/states;
- execute one featured/scenario task;
- inspect the resulting text-equivalent state;
- complete one Quick Assign response path;
- hear important status changes without destructive focus movement;
- verify visual-only information has an equivalent relation.

Do not mark the lab accessible because a screen reader can enumerate buttons if the learner cannot understand the algorithmic relation.

## 13. Human touch audit

On physical touch hardware where feasible:

- use every primary action row control;
- use dense algorithm controls;
- test near-point selection in KNN and other coordinate surfaces;
- test internal horizontal scrollers;
- test disclosure menus and reset/clear controls;
- check accidental adjacent activation;
- verify any drag interaction has a non-drag path where required.

## 14. Localization accessibility

For EN/ZH/VI/ES:

- document `lang` must update correctly;
- accessible names must match visible labels;
- translated labels must not truncate into ambiguous controls;
- live/status messages must use the active language;
- state text must preserve mechanism meaning;
- response text must survive locale switching;
- switching back to English restores canonical English control/state labels without resetting mechanism state.

## 15. Severity

### A0 release blocker

Examples:

- core mechanism cannot be operated by keyboard when no essential exception applies;
- screen-reader/text path omits the concept-defining relation;
- focus trap blocks escape;
- required state conveyed only by color;
- translated accessible name changes function;
- major text/controls become unavailable at supported zoom/reflow.

### A1 major

Material difficulty completing the core task, repeated focus obscuration, undersized critical targets, status changes unavailable to AT, or other WCAG A/AA failure with substantial user impact.

### A2 moderate

Applicable conformance defect with bounded impact or a stronger house-standard failure that materially reduces usability.

### A3 minor

Polish or preferred-house-standard issue without loss of core accessibility.

Any confirmed applicable WCAG Level A or AA failure must be resolved before a formal AA conformance claim, regardless of internal severity label.

## 16. Evidence record

Each audit row records:

- exact SHA;
- route/lab;
- state;
- locale;
- theme;
- viewport/zoom;
- input/AT environment;
- success criterion or house rule;
- applicability;
- method;
- result;
- severity;
- evidence reference;
- finding owner;
- regression-test candidate;
- resolution SHA when fixed.

Use `docs/V1_9_ACCESSIBILITY_AUDIT.csv` as the canonical row schema.

## 17. Release gate

v1.9 release is blocked while any of the following remains:

- unresolved A0;
- unresolved A1;
- confirmed applicable WCAG A/AA failure intended to be inside the declared release conformance scope;
- concept-defining information unavailable without color, hover, pointer drag, or animation when an alternative is required;
- locale-specific accessibility semantics changing function or mechanism meaning;
- a supported viewport/zoom condition making the core learner task unusable.

A formal WCAG 2.2 AA public claim is a separate gate after the full criterion matrix is complete. The product may be engineered toward AA without prematurely publishing a conformance claim.
