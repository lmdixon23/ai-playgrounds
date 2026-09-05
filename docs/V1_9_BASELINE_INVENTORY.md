# AI Playgrounds v1.9 baseline inventory

Status: baseline evidence for issue #56. This document records the product and repository state that the v1.9 architecture work must preserve before any intentional redesign.

## 1. Exact baseline identity

Canonical source baseline:

- branch: `main`
- commit: `d1c72e10e6c5bf64b9a4bbed578b2305d1c988d0`
- current software release: `v1.8.1`
- public boundary: 15 applets and 58 deployed files
- learner locales: EN, ZH, VI, ES
- Level 1 Quick Assigns: 15 active assignments
- Level 2 Activity Pack pilots: NN-1 and CNN-1

The v1.9 program treats this exact revision as immutable comparison evidence. Urgent correctness, security, or privacy fixes may advance `main`, but any such advance requires a newly recorded baseline before architecture work continues.

## 2. Exact verification receipt

The exact baseline SHA has a successful GitHub Actions Verify run:

- workflow: `Verify`
- run: `33334774958`
- source SHA: `d1c72e10e6c5bf64b9a4bbed578b2305d1c988d0`
- conclusion: PASS
- run attempt: 2

Both current jobs passed.

### Release and browser checks

Job `99319884021` passed the inherited stack, including:

- release checks;
- current-document consistency;
- portfolio-freshness checker regressions;
- pedagogical and Guided Challenge contracts;
- ZH, VI, and ES localization and browser state checks;
- algorithm regressions;
- Transformer, agent, and Minimax reference and cross-runtime tests;
- HCI and Activity Pack checks;
- Quick Assign and design-system checks;
- v1.6, v1.7, and modern-shell regressions;
- final browser and responsive QA.

### v1.8.1 final-artifact job

Job `99319884506` passed:

- v1.8.1 metadata;
- exact v1.7.2 modern parity regression;
- exact v1.8.0 public composition regression;
- v1.8.0 algorithm-mode contracts;
- four-locale responsive behavior;
- deterministic v1.8.1 learner-parity composition;
- v1.8.1 modern learner, responsive, and dark-theme browser QA.

### Retained evidence archives

The exact run retains these evidence artifacts:

- `ai-playgrounds-verification-33334774958`, artifact `9738771300`, SHA-256 `1a9c7b7623dce1236074dd7ab8fdbef57d2bc1037f25353dcf5abcca8427883c`;
- `ai-playgrounds-v1.8.1-verification-33334774958`, artifact `9738704090`, SHA-256 `92bab271c004091e8ad9c0be1454a4bdeaeaa56dd8c4af066b2094258ca98971`;
- retained secondary verification archive `9738697269`, SHA-256 `5516bbf15c1fdfc21837bc84f7a5057a54b243187ee864e6c4ab738352ab7c40`.

These receipts establish the pre-refactor software baseline. They do not establish learning gains, universal learner preference, translation naturalness, or accessibility conformance.

## 3. Deterministic-build baseline

`tools/test_v1_8_1_modern_learner_parity.py` is the canonical current repeatability gate.

It performs two complete executions of `tools/build_site_v1_8_1.py`, computes SHA-256 for every generated file after each build, and fails if any file is added, removed, or byte-different. It then validates the 58-file / 15-applet boundary and compiles final inline JavaScript and JSON metadata blocks.

Therefore the architecture refactor in #47 should target the following strongest acceptance condition:

`new canonical-source build output == baseline v1.8.1 build output byte for byte`

If exact byte identity is impossible for a justified structural reason, the refactor must provide an explicit per-file diff and demonstrate that every difference is non-semantic before #47 can close.

## 4. Current public product boundary

The generated public release contains 15 applets.

### Original source-backed applets

The repository currently has twelve committed source directories under `playgrounds/`:

1. `search-pathfinding`
2. `hill-climbing`
3. `wumpus-world`
4. `cnf-sat`
5. `bayes-classifier`
6. `bayes-network`
7. `knn-classifier`
8. `overfitting`
9. `neural-network`
10. `kmeans`
11. `convolution`
12. `q-learning-gridworld`

### Generated modern applets

Three additional public applets are generated during release composition rather than existing as peer source directories under `playgrounds/`:

13. `transformer-language-model`
14. `agent-tool-context`
15. `minimax-alpha-beta`

This two-class source architecture is a primary v1.9 refactor target. The public product already presents one fifteen-lab suite; the canonical source tree should eventually represent all fifteen labs as peers while retaining mechanism-specific implementations.

## 5. Current source versus generated artifact split

The repository presently mixes three roles:

### Direct public source

Examples:

- root `index.html`;
- the twelve committed `playgrounds/<slug>/index.html` files;
- support HTML pages;
- activities;
- root public metadata files.

Some of these direct sources intentionally contain older historical assumptions that are transformed by successor builders. For example, root `index.html` still contains twelve-app and bilingual metadata even though the current generated product is fifteen-lab and four-locale.

### Build-time canonical or semi-canonical data

Examples include:

- `tools/quick_assigns_v2.json`;
- `tools/home_locales_v1.json`;
- `tools/catalogue_locales_v1.json`;
- `tools/modern_parity_v1.json`;
- `tools/modern_learning_v1_8_1.py`;
- Transformer locale/reference files;
- agent locale/reference files;
- Minimax locale/reference files;
- root citation and CodeMeta metadata.

These inputs do not yet form one clearly declared current source-of-truth layer.

### Generated public artifact

`_site/` is generated and ignored. The current release validator requires:

- exactly 58 files;
- exactly 15 `playgrounds/*/index.html` applets;
- v1.8.1 release identity;
- current analytics provenance exactly once per public HTML page;
- complete release metadata and local references.

The v1.9 architecture must make this source-to-artifact relationship explicit and substantially simpler.

## 6. Current release-composition chain

The current build is not a single canonical composition. It is a stack of historical release layers.

The directly observed successor chain is:

`build_site_v1_8_1.py`

→ `build_site_v1_8.py`

→ `build_site_v1_7_2.py`

→ `build_site_v1_7_2_modern_parity_accessible.py`

→ `build_site_v1_7_2_modern_parity_complete.py`

→ `build_site_v1_7_2_modern_parity_final.py`

→ `build_site_v1_7_2_modern_parity.py`

→ isolated clean execution of `build_site_v1_7_1.py`

→ `build_site_v1_7.py`

→ additional inherited v1.7 and v1.6 release layers.

The repository also retains older builders and candidate builders including v1.3, v1.4, v1.5, v1.5.1, v1.6, v1.6.1, v1.6.2, multiple v1.7 parity variants, Transformer candidates, agent candidates, Minimax candidates, and engagement candidates.

Historical reproducibility is valuable. Requiring current development to compose the product through this historical ladder is not.

### Concrete debt demonstrated by the current chain

- v1.7.2 builds v1.7.1 in a temporary copied repository to isolate monkeypatched historical builder state;
- v1.7.2 validation reaches through nested modules such as predecessor `base` objects to re-run older validators;
- modern shell, Quick Assign, accessibility, toolbar, metadata, and learner-depth changes are applied by separate successor wrappers;
- v1.8 patches three original applets and release identity over the v1.7.2 artifact;
- v1.8.1 adds another large inline CSS/runtime layer for Labs 13–15;
- current release identity is repeatedly rewritten through generated HTML and metadata.

The architecture refactor should preserve old builders as historical evidence where useful, while establishing one independent current builder that no longer depends on the historical release ladder.

## 7. Current design-system state

The primary current contract is `docs/APPLET_DESIGN_SYSTEM_CONTRACT.md`, supplemented by the v1.7.2 and v1.8.1 addenda.

Current public architecture already requires:

- shared suite navigation and provenance;
- concise catalogue discovery metadata;
- featured experiment;
- approximately five predict–run–explain scenarios for complex labs;
- terminology primer;
- mechanism explanation;
- teacher prompts;
- four-language learner support;
- one stable Level 1 Quick Assign per lab;
- keyboard/text-equivalent support where applicable;
- responsive containment;
- reduced-motion handling;
- privacy-minimized analytics;
- exact release verification.

The v1.9 design-token work should consolidate implementation of this contract. It must not reinterpret the contract as pixel-identical mechanism bodies.

## 8. Current localization sources

Localization is functionally complete at the learner surface but structurally fragmented.

Observed current sources include:

- `tools/home_locales_v1.json`;
- `tools/catalogue_locales_v1.json`;
- per-applet original localization embedded in original source applets;
- `tools/transformer_language_model_locales.json`;
- `tools/transformer_language_model_locales_vi_es.json`;
- `tools/agent_tool_context_locales.json`;
- `tools/agent_tool_context_locales_dynamic.json`;
- separate Minimax EN/ZH/VI/ES locale files;
- `tools/modern_learning_v1_8_1.py` containing another four-locale learner-curriculum layer;
- several build-layer dictionaries for modern shell, accessibility, packet, and toolbar labels.

v1.9 should create a declared current locale registry or equivalent source architecture without rewriting translations merely for structural neatness. Human naturalness review belongs to #50.

## 9. Quick Assign source state

Current all-lab assignment behavior is primarily represented by `tools/quick_assigns_v2.json` plus build/runtime code.

Historical `tools/quick_assigns_v1.json` remains in the repository for prior-release reproducibility.

v1.9 should retain historical registries but clearly declare one current assignment registry. Every refactor must preserve:

- 15 stable IDs;
- current canonical classroom links;
- EN/ZH/VI/ES presentation;
- local-only learner responses;
- response preservation across locale switching;
- copy/print/export behavior;
- analytics exclusion of learner responses.

## 10. Current verification architecture

Current verification is very strong but difficult to reason about as one present-day system.

`.github/workflows/verify.yml` currently runs two main jobs:

### Inherited release and browser job

This sequentially invokes a large ladder of historical and current checks from base release checks through v1.7.1 plus browser/responsive QA.

### Current v1.8.1 job

This independently verifies the current release identity and preserves v1.7.2, v1.8.0, and v1.8.1 behavior.

This layered redundancy is useful during the v1.9 refactor because it gives strong regression evidence. After the architecture stabilizes, #52 should expose one current manifest-driven verification interface while preserving historical release tests as provenance rather than deleting them.

### Known generic-QA drift

`tools/browser_qa.py` still contains current-looking historical assumptions such as a twelve-applet-card check and EN/ZH-only homepage localization logic. Current version-specific gates compensate for these assumptions, but they demonstrate why current inventory and locale state should be derived from canonical manifests rather than hard-coded historical values.

## 11. Current workflow inventory

Active workflow files on current `main` include:

- `deploy-pages.yml`;
- `portfolio-freshness.yml`;
- `publish-release-evidence.yml`;
- `publish-v1.7.2.yml`;
- `publish-v1.8.0.yml`;
- `publish-v1.8.1.yml`;
- `verify.yml`.

Version-specific publication workflows are historical/release machinery and should be audited in #52/#53. They should not be removed solely to reduce file count; each must be classified as active current logic, immutable historical reproducibility, or safely retireable workflow code.

## 12. Branch inventory and disposition

Branches present during this baseline audit:

### `main`

Disposition: retain. Exact baseline SHA recorded above.

### `planning/v1.9-product-coherence`

Disposition: retain through the v1.9 planning merge. Contains the v1.9 quality program and visual consistency specification.

### `planning/v1.9-baseline-inventory`

Disposition: temporary bounded #56 branch. Delete after the baseline evidence is integrated.

### `planning/v1.5-human-usability-validation`

Disposition: migrate useful protocol and observation material into the current #50 workstream, then delete the branch. Do not discard the methodological content before migration.

### `automation/portfolio-freshness`

Disposition: delete after confirming no unique post-merge work. Its substantive work was merged through PR #45.

### `fix/publisher-idempotency`

Disposition: delete after confirming no unique post-merge work. Its substantive work was merged through PR #46 and the baseline main SHA includes that merge.

Actual branch deletion belongs to #53 so governance changes and cleanup occur under one audited repository-hygiene workstream.

## 13. Freeze boundary before #47

Until the canonical-source architecture passes its behavior-preserving gate:

- no Lab 16 implementation;
- no RAG implementation;
- no broad homepage redesign;
- no cross-suite cosmetic normalization mixed into architecture changes;
- no algorithm/mechanism change bundled with source consolidation;
- no translation rewrite bundled with source movement;
- no change to analytics payload semantics;
- no change to Quick Assign IDs or response storage;
- no change to the offline/single-file public contract.

Urgent correctness, security, or privacy defects may be fixed in isolated patches. If `main` advances for such a patch, the exact baseline SHA and receipts must be refreshed before continuing #47.

## 14. Baseline risk register

### P0: current output depends on historical composition layers

Risk: a refactor can accidentally omit behavior that exists only in a late wrapper.

Control: byte-identical output target plus full exact-SHA verification.

### P0: two source classes for the fifteen public labs

Risk: future work can reproduce the original-twelve versus modern-three drift that v1.7.2 and v1.8.1 had to repair.

Control: canonical peer representation for all fifteen labs, with mechanism-specific modules rather than separate product families.

### P1: localization has multiple overlapping source locations

Risk: a shared label or curriculum phrase can diverge across shell/runtime layers.

Control: declared current locale ownership and regression tests after consolidation.

### P1: current QA contains historical assumptions

Risk: a green generic test may describe an old product boundary while stronger successor tests hide the drift.

Control: #52 manifest-driven current verification.

### P1: large inline style/runtime patches are release-layer owned

Risk: visual fixes can be duplicated or overridden by later wrappers.

Control: #47 canonical design primitives and #48 visual regression.

### P1: current source HTML can be stale while generated artifact is correct

Risk: contributors edit the wrong layer or infer current behavior from stale source metadata.

Control: explicit canonical-input/generated-output map and current-source normalization after byte-equivalent architecture is established.

## 15. Baseline completion status

Completed evidence:

- exact baseline SHA recorded;
- exact successful Verify run recorded;
- retained evidence artifact digests recorded;
- deterministic two-build byte-comparison mechanism confirmed;
- public 15-app / 58-file boundary confirmed by current builder/test contracts;
- source/public 12-plus-3 split identified;
- current release-composition chain identified;
- major current manifests/registries identified;
- workflow inventory recorded;
- branch disposition recorded;
- freeze rules recorded.

Still required before #56 closes:

1. Produce a fresh diagnostic screenshot census of all 15 baseline applets at representative desktop and phone states. Existing `browser_qa.py` supports screenshot capture, but the accepted baseline Verify run deliberately used `--no-screenshots`.
2. Retain the screenshot evidence with the exact baseline SHA and viewport/browser metadata.
3. If feasible, retain a machine-readable final 58-file hash manifest from the exact baseline build as a direct input to #47 byte-equivalence checks.
4. Migrate the reusable v1.5 human-usability protocol into the current #50 workstream before deleting its old branch.

The screenshot census is diagnostic evidence for the pre-refactor state. Permanent visual-regression goldens are established later under #48 after canonical architecture exists and reviewed visual inconsistencies have been resolved.

## 16. Handoff to #47

#47 may begin only after the remaining #56 evidence is captured or an explicit recorded reason demonstrates why a missing baseline item cannot affect refactor attribution.

The first architecture PR should add canonical source structures beside the existing build path and prove equivalence before replacing anything. A safe migration sequence is:

1. declare current product manifest and current release metadata;
2. declare current shared design tokens/primitives without changing emitted bytes;
3. create peer source ownership for Labs 13–15;
4. consolidate shared locale and Quick Assign ownership;
5. implement one current builder that reproduces the baseline artifact;
6. compare every output hash;
7. run the entire inherited Verify stack;
8. switch current CI/deployment to the new builder only after equivalence passes;
9. retain historical builders under a clearly historical boundary rather than letting them remain current dependencies.

No visible redesign belongs in those steps. Visual normalization starts only after the new current builder is proven.