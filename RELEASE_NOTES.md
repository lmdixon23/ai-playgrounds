# Release notes

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

The legacy applets require no account, backend, database, package manager, or build step. Student responses remain local unless the learner copies or prints them. Lab 13 is generated deterministically into the Pages artifact from its frozen source and catalogs and remains one self-contained offline HTML file after generation.

## Release integrity

- GitHub Pages deploys a deterministic public artifact containing only intentionally published files.
- GitHub Actions requires static release checks, algorithm regression tests, release-metadata checks, Lab 13-specific gates, and browser/responsive QA.
- The release tag identifies the exact verified source revision.

## Scope

The project provides interactive teaching tools. Claims about learning gains, classroom adoption, or accessibility conformance require separate classroom and user studies.
