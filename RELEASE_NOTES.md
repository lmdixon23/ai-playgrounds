# Release notes

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
- Includes five prediction-before-reveal Guided Challenges for next-action selection, validation gates, observation effects, trust classification, and stop decisions.

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
