# Release notes

## Current release index

Dedicated versioned files are the source for detailed notes in the current release line. The older detailed entries below remain as historical material.

| Release | Summary | Detailed notes |
|---|---|---|
| v1.7.2, 2026-08-27 | Modern-lab product parity and exact final-artifact release assurance | [docs/RELEASE_V1_7_2.md](docs/RELEASE_V1_7_2.md) |
| v1.7.1, 2026-08-27 | Shared theme preference and one-time legacy migration | [docs/RELEASE_V1_7_1.md](docs/RELEASE_V1_7_1.md) |
| v1.7.0, 2026-08-26 | One active four-locale Quick Assign for every lab | [docs/RELEASE_V1_7_0.md](docs/RELEASE_V1_7_0.md) |
| v1.6.2, 2026-08-26 | Exact public-artifact provenance normalization | [docs/RELEASE_V1_6_2.md](docs/RELEASE_V1_6_2.md) |
| v1.6.1, 2026-08-26 | Shared applet contract and Quick Assign canaries | [docs/RELEASE_V1_6_1.md](docs/RELEASE_V1_6_1.md) |

## v1.6.0, 2026-08-25

### Lab 15: Game Trees, Minimax, and Alpha-Beta Pruning

- Adds the fifteenth public AI Playground and thirteenth Foundations/course-track lab.
- Models finite deterministic two-player, zero-sum, perfect-information game trees with alternating MAX and MIN decisions and numeric terminal utilities from MAX's perspective.
- Makes recursive minimax backup inspectable as `terminal utilities -> MIN/MAX backups -> exact root value and move`.
- Adds exact Alpha-Beta pruning over the same fixed tree and child order; a cutoff occurs only when the current bounds establish that remaining siblings cannot change the minimax result.
- Keeps pruned subtrees spatially visible and explicitly labels them **not evaluated**, rather than implying that pruning deletes part of the game or approximates minimax.
- Adds a move-order experiment in which the same tree and utilities produce different search work while preserving the same exact minimax result.
- Includes bounded terminal-utility editing, deterministic trace stepping/replay, saved-run comparison, node inspection, and five prediction-before-reveal Guided Challenges.

### Four-locale and learner-centered interaction

- Adds complete English, Simplified Chinese, Vietnamese, and Spanish presentation catalogs while protecting `MAX`, `MIN`, `alpha`, `beta`, node ids, scenario ids, numeric utilities, and machine-state keys.
- Locale switching is presentation-only and preserves the complete tree/search/trace/challenge state.
- Provides a synchronized text-equivalent search state, focus-visible native controls, reduced-motion behavior, and internally scrollable wide trees rather than page-wide overflow.
- Adds release-level checks for 390×844 portrait, 844×390 landscape, 640×720 split view, and 200% text enlargement.
- The engagement/HCI audit adopts the current mechanism-first interaction model and explicitly rejects decorative animation, disappearing pruned branches, badges, points, sound, or automatic jumping to a cutoff without evidence that such additions improve the learner model.

### Verification and release composition

- The independent Python reference passes 26 adversarial/unit tests and a 648-case bounded exhaustive census.
- The independent JavaScript implementation is recursively cross-checked against the Python reference across frozen scenario and invalid-input families, with a parity-harness self-test.
- Prototype and English single-file browser candidates each pass 22 mechanism/browser checks.
- The semantic localization gate contains 1,235 checks across 126 presentation keys per locale.
- The four-locale browser/state gate preserves algorithm/challenge state while testing dynamic cutoff text, deep links, reduced motion, and narrow mobile behavior.
- v1.6 expands the deterministic Pages boundary from fourteen to fifteen applets and from 57 to 58 files while retaining the Activity Pack index, NN-1, and CNN-1 exactly as the three Activity Pack pages.
- The course structure is now thirteen Foundations/course-track labs plus two Modern AI extensions: Transformer Language Modeling and Agent Tool Use and Context Protocols.
- The v1.5.1 HCI, responsive, Activity Pack, and privacy-minimized GoatCounter hardening remains in force; every public HTML page receives the v1.6 analytics wrapper exactly once.

### Evidence boundary

- Software/browser assurance establishes behavior under tested conditions; it does not establish accessibility conformance, measured learning gains, classroom adoption, or universal learner preference.
- Human screen-reader/assistive-technology usability and fluent-learner translation naturalness remain separate evidence questions.
- v1.6.0 does not modify or reassign the immutable v1.0.1 DOI `10.5281/zenodo.21854217`.

## v1.5.1, 2026-08-25

### Learner-centered HCI hardening

- Keeps all fourteen applet algorithms unchanged while applying a second Educational-HCI assurance pass over the released v1.5.0 product.
- Adds KNN Guided Challenge near-miss recovery so a slightly imprecise mobile tap near a training point selects the nearby point instead of unexpectedly moving the query and clearing prediction progress.
- Reflows Bayesian Network inference-method choices into a two-row narrow-mobile layout so all four methods remain visible with EN/ZH/VI/ES labels.
- Reflows Tiny Neural Network history/scrub controls for short mobile-landscape layouts.
- Adds a PWP-inspired learner-state/recovery contract covering initial state, action, expected state, recovery path, focus/accessibility state, state preservation, and failure-path behavior.

### Ready-to-assign Activity Pack pilot

- Adds **NN-1 · Make it fail, then make it learn**, adapted from prior classroom use and structured around nonlinear capacity, training dynamics, and train/test generalization.
- Adds **CNN-1 · Be the filter**, adapted from prior classroom use and structured around one hand-calculated convolution, directional edge detection, learned filters, and pooling.
- Both activities use the same inquiry spine: predict -> run -> observe -> explain -> transfer.
- Student text autosaves only in the local browser, supports guarded clearing and print/PDF use, and is never submitted to AI Playgrounds.
- Teacher answer keys and grading exemplars are intentionally excluded from the public student site.

### Analytics repair and adoption measurement

- Applies the privacy-minimized analytics wrapper exactly once to every public HTML page in the deterministic artifact, including generated Labs 13/14 and the Activity Pack pages.
- Normalizes canonical page paths so `/index.html` aliases do not fragment the same page, and sends the human-readable document title.
- Sends synthetic applet/resource/outbound/engaged interactions as GoatCounter events with `e=1` instead of counting them as ordinary page paths.
- Converts allow-listed `ap_src` values into GoatCounter campaign query data while retaining the project's no-general-referrer policy.
- Preserves Global Privacy Control, Do Not Track, `?analytics=off`, local opt-out, canonical-host-only operation, no third-party analytics JavaScript, and no transmission of learner answers or experiment state.

### Verification and evidence boundary

- Expands the deterministic Pages boundary from 54 to 57 files while preserving exactly fourteen applets; the three additional files are the Activity Pack index plus NN-1 and CNN-1.
- Adds a dedicated v1.5.1 browser gate covering analytics coverage and payload semantics, KNN touch recovery, four-locale Bayesian method containment, Neural Network 844×390 landscape containment, 200% text-enlargement stress across all fourteen applets, Activity Pack autosave/clear/focus recovery, and analytics opt-out behavior.
- Retains the complete inherited v1.5 pedagogical, localization, algorithm, Transformer, agent, engagement, public-integration, and browser/responsive verification stack.
- Software/browser assurance establishes behavior under tested conditions; it does not establish accessibility conformance, measured learning gains, classroom adoption, or universal learner preference.
- v1.5.1 does not modify or reassign the immutable v1.0.1 DOI `10.5281/zenodo.21854217`.

## v1.5.0, 2026-08-25

### Engagement excellence without decorative inflation

- Keeps the public suite at fourteen applets and the deterministic Pages boundary at 54 files.
- Applies the Full Assurance Stack to learner engagement and immediate visual impact, including Red Team, Blue Team, Arbiter, FMEA, fault-tree analysis, STPA, Bowtie, negative/boundary tests, and explicit kill conditions.
- Researches strong interaction patterns from educational and model-explainer products and transfers only mechanism-faithful ideas: direct manipulation, state continuity, before/after comparison, one-step replay, and learner construction.
- Deliberately leaves ten already-strong applets unchanged rather than adding arbitrary animation, gamification, sound, badges, points, or other spectacle.

### Lab 13: Transformer state continuity and controlled continuation

- Adds a state-derived Tokens -> Represent -> Attend -> Predict replay over the already-computed toy Transformer; it is explicitly not a wall-clock execution trace.
- Adds `Append argmax token`, an explicit deterministic continuation rule rather than stochastic sampling.
- Adds a saved baseline/current comparison for top-token probability, maximum probability delta, final-attention L1 delta, and the largest token-probability changes.
- Preserves the frozen Transformer arithmetic, one-file/offline operation, four-locale state invariance, reduced-motion behavior, and 390 px containment.

### Lab 14: runtime packet and isolated learner sandbox

- Adds a visible action packet whose path is derived from the actual runtime event across Propose -> Validate -> Authorize -> Execute -> Observe -> Update -> Stop.
- Makes rejection and authorization denial visibly stop at the correct runtime gate.
- Adds an explicit context delta and `SIMULATED WORLD - no real external action` surface.
- Adds a learner-selected one-step sandbox for principal, tool, and JSON arguments using a fresh isolated in-memory world. Learner-selected calls are explicitly distinguished from model-selected actions.
- Preserves side-effect-free rejection/denial, frozen runtime semantics, four-locale state invariance, reduced motion, offline operation, and narrow-viewport containment.

### CNF/SAT: DPLL branch-and-prune tree

- Adds an SVG search tree derived read-only from the existing DPLL trace; there remains exactly one DPLL solver.
- Makes real branching, unit/pure propagation, contradiction, pruning, sibling backtracking, and terminal SAT/UNSAT states spatially visible.
- Adversarial browser QA uses a parser-valid two-variable UNSAT formula with no initial unit or pure literal so the test must exercise actual branch/conflict/backtrack behavior.
- Preserves the existing DPLL transport, locale state, reduced-motion path, and mobile containment.

### Bayesian Network: exact before/after posterior delta

- Preserves the previous exact posterior as a marker and shows the current posterior plus exact percentage-point delta.
- Makes explaining away visible without requiring the learner to remember the previous number.
- Explicitly rejects generic probability-flow animation because the applet is not running a literal message-flow algorithm along its arrows.
- Suppresses the exact before/after comparison for sampling methods so Monte Carlo noise is not misrepresented as a model-state change.

### Verification and evidence boundary

- Adds dedicated candidate gates for Lab 13, Lab 14, CNF/SAT, and Bayesian Network, plus a composed v1.5 public integration gate.
- The accepted pre-integration behavior candidate at `e3eaae0473142271682d8ea0a97192ca9984e1ea` passed Verify run `32820222292`, job `97716565394`, including all inherited gates and final browser/responsive QA.
- Adds a human usability protocol for time to first meaningful action, prediction integrity, mechanism explanation, recurring false mental models, voluntary exploration, accessibility paths, and fluent-reader locale review.
- Design and browser evidence support an internal design-level engagement/immediate-impact assessment; they do not establish measured learning gains, universal learner preference, classroom adoption, or accessibility conformance.
- v1.5.0 does not modify or reassign the immutable v1.0.1 DOI `10.5281/zenodo.21854217`.

## v1.4.0, 2026-08-25

### Product-quality pass before Lab 15

- Keeps the public suite at fourteen applets and treats v1.4 as an experience, navigation, and provenance release rather than adding another lab.
- Adds a curriculum coverage matrix against AIMA 4th edition and the Spring 2026 CS50/CSCI E-80 AI curriculum so future labs can balance classical introductory-AI gaps with contemporary extensions.
- Explicitly blocks Lab 15 implementation until the v1.4 quality and release boundary is complete.

### Lab 13: clearer Transformer mechanism journey

- Adds a visible Tokenize -> Represent -> Attend -> Predict journey over the existing deterministic Transformer lab.
- Lets learners focus the relevant existing mechanism panels without changing prompt state, temperature, masking, position information, perturbations, challenge state, or numeric model outputs.
- Replaces the prominent four-language button group with a native English / 简体中文 / Tiếng Việt / Español selector while retaining state preservation and `?lang=` deep links.
- Moves software-version provenance out of the hero treatment and into a secondary provenance area.

### Lab 14: clearer agent-runtime journey

- Extends the learner-visible runtime story to Propose -> Validate -> Authorize -> Execute -> Observe -> Update / choose next -> Stop.
- Makes schema rejection, authorization denial, execution error, successful observation, context update, next-action selection, and correct stopping visually distinct without changing the frozen deterministic policy or tool world.
- Preserves the canonical `weather.current -> 8 C -> unit.convert_temperature -> 46.4 F -> STOP` trace and side-effect-free behavior for invalid or unauthorized calls.
- Replaces the prominent four-language button group with the same native four-language selector pattern used by the rest of the multilingual applet experience.

### Suite navigation and language UX

- Adapts the landing and support-page language controls to native selectors using only the translations actually available on those surfaces.
- Retains the existing native four-language selector overlay for the original twelve applets.
- Reframes curriculum navigation into Foundations / course track, Modern AI extensions, and the existing quick-entry sampler.
- Keeps Transformer Language Modeling at the advanced introductory/modern boundary and identifies Agent Tool Use and Context Protocols as a modern extension rather than a classical-course prerequisite.
- Regenerates the curriculum applet map from the full fourteen-entry release inventory so generated Labs 13 and 14 remain discoverable.

### Verification and provenance

- Preserves the fourteen-applet, 54-file deterministic Pages boundary.
- Adds dedicated Lab 13 v1.4, Lab 14 v1.4, and full-site v1.4 product-quality browser gates while retaining all inherited v1.3 verification.
- The accepted behavior candidate at `1a30893ce0341e3063bb969921cd8b66d1243915` passed permanent Verify run `32780480520`, job `97601258430`.
- Candidate evidence artifact `9539645266` has SHA-256 `4e7e5ec532076e19967252a7805825651dd200d4002449071c47bb3f1bbd8cbf`.
- v1.4.0 does not modify or reassign the immutable v1.0.1 DOI `10.5281/zenodo.21854217`.

### Verification boundary

Software checks establish implementation and release integrity only. They do not establish learning gains, classroom adoption, or accessibility conformance.

## v1.3.0, 2026-08-25

### Lab 14: Agent Tool Use and Context Protocols

- Added the fourteenth public applet, a deterministic agent-runtime lab for structured tool use and context updates.
- Separates model text, structured tool calls, schema validation, authorization, execution, returned observations, provenance-aware context updates, and stopping into explicit runtime stages.
- Includes eight deterministic scenarios covering observation-driven replanning, overlapping tool schemas, invalid arguments, text versus execution, permission denial, instruction-like tool output, MCP 2026-07-28 serialization, and correct termination.
- Includes five prediction-before-reveal Guided Challenges for next-action selection, validation gates, observation effects, trust classification, and termination.

### Four-locale parity

- Added English, Simplified Chinese, Vietnamese, and Spanish semantic coverage for both static and dynamically generated Lab 14 surfaces.
- Preserves tool names, state keys, argument keys, protocol identifiers, frozen numeric data, permission state, provenance, and complete deterministic machine state across locale switches.
- Keeps the adversarial note fixture visibly instruction-like in every locale without allowing translated content to rewrite the goal, principal, or authorization state.
- Keeps the public Lab 14 applet as one self-contained, offline-ready HTML file with no runtime API, fetch, XHR, WebSocket, EventSource, or external script dependency.

### Verification and deployment

- Added independent Python and JavaScript Lab 14 references with 20 reference tests and eight cross-runtime parity fixture families.
- Added prototype, English-source, primary localization, dynamic localization, four-locale browser/state-preservation, and public v1.3 integration gates.
- Expanded the deterministic Pages boundary from thirteen to fourteen applets and from 53 to 54 files while retaining every inherited v1.2, Lab 13, algorithm, localization, and browser gate.
- Rebound the public Lab 13 regression gate to the fourteen-applet v1.3 artifact so the Transformer applet remains verified after Lab 14 integration.

### Release provenance

- v1.3.0 does not modify the immutable v1.0.1 tag, release, or version DOI.
- The archived v1.0.1 DOI remains `10.5281/zenodo.21854217`; it is not represented as a DOI for v1.3.0.
- The separate design-and-tools research manuscript remains in preparation and is not part of this software release.

### Verification boundary

Software checks establish implementation and release integrity only. They do not establish learning gains, classroom adoption, or accessibility conformance.

## v1.2.0, 2026-08-24

### Lab 13: Transformer Language Modeling

- Added the thirteenth public applet, a deterministic decoder-like Transformer language-model lab.
- Connects toy tokenization, token and position vectors, Q/K/V projections, scaled dot-product self-attention, causal masking, residual and feed-forward state, logits, temperature, and next-token probabilities.
- Adds six mechanism scenarios and four prediction-before-reveal Guided Challenges, including mask leakage, token substitution, temperature transfer, and an executable attention-not-explanation counterexample.
- Keeps the model deliberately small and inspectable; the applet does not claim to reproduce a frontier LLM or use attention weights as a general explanation of reasoning.

### Four-locale parity

- Added English, Simplified Chinese, Vietnamese, and Spanish semantic catalogs for Lab 13.
- Preserves model-data tokens and mathematical identifiers across locale changes so translation cannot mutate the frozen arithmetic.
- Adds state-preserving browser locale switching and exact arithmetic-invariance checks.
- Keeps the public Lab 13 applet as one self-contained, offline-ready HTML artifact with no runtime API, fetch, XHR, or external script dependency.

### Verification and deployment

- Added 20 independent numeric/adversarial Transformer fixtures.
- Added recursive Python-to-JavaScript numeric parity across the complete model state.
- Added prototype, English-source, ZH semantic, VI/ES semantic, four-locale browser, and public v1.2 integration gates.
- Expands the deterministic Pages boundary from twelve to thirteen applets while retaining the existing v1.1 hardening, localization, algorithm, and browser gates.

### Release provenance

- v1.2.0 does not modify the immutable v1.0.1 tag, release, or version DOI.
- The archived v1.0.1 DOI remains `10.5281/zenodo.21854217`; it is not represented as a DOI for v1.2.0.
- The separate design-and-tools research manuscript remains in preparation and is not part of this software release.

### Verification boundary

Software checks establish implementation and release integrity only. They do not establish learning gains, classroom adoption, or accessibility conformance.

## v1.0.1, 2026-08-08

### Launch hardening

- Added a bilingual five-minute start path and dedicated educator/reviewer routes.
- Standardized privacy-minimized aggregate analytics across public pages without loading third-party JavaScript.
- Analytics run only on the canonical GitHub Pages host, honor GPC/DNT and explicit opt-out, exclude URL query strings from page paths, and send no experiment values or learner responses.
- Added durable release-evidence tooling, educator adoption guidance, classroom-pilot guidance, contribution templates, and launch materials.
- Synchronized the active Paper 7 source with the final v1.0.0 verification record while retaining historical pre-release records as provenance.
- Fixed the print-packet JavaScript regression introduced during the initial launch-hardening pass.

### Verification boundary

Software checks establish implementation and release integrity only. They do not establish learning gains, classroom adoption, or accessibility conformance.

## v1.0.0, 2026-07-25

AI Playgrounds includes twelve bilingual, offline-ready interactive demonstrations covering:

- search,
- local optimization,
- logical agents,
- satisfiability,
- Bayesian reasoning,
- supervised learning,
- model evaluation,
- neural networks,
- clustering,
- convolution,
- reinforcement learning.

## Included with every applet

- a focused interactive model,
- five learner scenarios,
- a featured experiment,
- complete English and Chinese visual and text-based explanations,
- teacher notes,
- model limitations,
- keyboard guidance,
- a printable student response packet,
- shareable experiment settings that preserve the exact current controls.

## Teaching materials

The release includes complete English and Simplified Chinese public teaching surfaces:

- a printable Teacher Pack,
- a responsive Curriculum Map,
- a one-page Student Lab Sheet,
- course-aligned and quick-entry sequences,
- citation and reuse information.

## Reliability and instructional accuracy

Explore panels include pre-rendered scenarios, dynamic text changes language immediately, and copied experiment links preserve later manual changes after a scenario is applied. The explanatory essays introduce notation and prerequisite terms before use and narrow technical claims to their valid assumptions.

## Privacy and portability

The legacy applets require no account, backend, database, package manager, or build step. Student responses remain local unless the learner copies or prints them. Lab 13 and Lab 14 are generated deterministically into the Pages artifact from frozen source and localization inputs and remain self-contained offline HTML files after generation.

## Release integrity

- GitHub Pages deploys a deterministic public artifact containing only intentionally published files.
- GitHub Actions requires static release checks, algorithm regression tests, release-metadata checks, Lab 13 and Lab 14 specific gates, and browser/responsive QA.
- The release tag identifies the exact verified source revision.

## Scope

The project provides interactive teaching tools. Claims about learning gains, classroom adoption, or accessibility conformance require separate classroom and user studies.
