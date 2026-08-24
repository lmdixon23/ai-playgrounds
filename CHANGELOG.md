# Changelog

## [1.3.0] - 2026-08-25

### Added
- Lab 14, Agent Tool Use and Context Protocols, as the fourteenth public AI Playground.
- Deterministic Python and JavaScript agent-runtime references with 20 reference tests and eight cross-runtime parity fixture families.
- Eight browser scenarios spanning observation-driven replanning, schema overlap, invalid arguments, text versus execution, permissions, adversarial tool output, MCP 2026-07-28, and stopping.
- Five prediction-before-reveal Guided Challenges for action selection, runtime gates, observation updates, trust classification, and termination.
- Complete EN/ZH/VI/ES semantic coverage for static and dynamic Lab 14 surfaces with protected tool, state, and protocol identifiers.
- Four-locale browser/state-preservation and public v1.3 integration gates.

### Changed
- Expanded the deterministic Pages deployment boundary from thirteen to fourteen applets and from 53 to 54 files.
- Updated the landing catalogue, curriculum sequence, release notes, sitemap, citation metadata, CodeMeta metadata, and README for v1.3.0.
- Rebound the public Lab 13 regression gate and badge to the fourteen-applet v1.3 artifact.
- Preserved the v1.2 manifest as an immutable thirteen-app release input and composed v1.3 from that inventory plus one explicit Lab 14 release record.

### Fixed
- Reopened the initial R5 localization freeze after a browser-surface audit identified dynamic strings outside the first 121-key catalog, then added a separately verified 42-key dynamic supplement.
- Repaired the first R6 localization runtime after CI exposed escaped-whitespace matching that prevented DOM translation.
- Replaced the failing generic runtime matcher with deterministic exact/template matching, JSON observation translation, state-preserving DOM localization, and post-render mutation handling.

## [1.2.0] - 2026-08-24

### Added
- Lab 13, Transformer Language Modeling, as the thirteenth public AI Playground.
- Deterministic Python and JavaScript reference implementations with 20 numeric/adversarial fixtures and recursive cross-runtime parity.
- A single-file Transformer applet covering token representation, position information, Q/K/V projections, causal self-attention, logits, next-token probabilities, temperature, and bounded attention perturbations.
- Four isolated prediction-before-reveal Guided Challenges and six mechanism scenarios, including causal-mask leakage and an attention-not-explanation counterexample.
- Simplified-Chinese, Vietnamese, and Spanish Lab 13 semantic catalogs with protected model tokens, placeholder parity, and adversarial terminology checks.
- Four-locale state-preserving browser parity and a dedicated public v1.2 integration gate.

### Changed
- Expanded the deterministic Pages deployment boundary from twelve to thirteen applets.
- Updated the landing catalogue and curriculum sequence to include Transformer Language Modeling.
- Updated release, citation, CodeMeta, and README metadata for v1.2.0 while retaining v1.0.1 as the immutable archived DOI-bearing release.

### Fixed
- Repaired a prototype text-equivalent-state regression exposed by the permanent browser gate.
- Corrected over-broad VI/ES semantic trap checks so negated misconception statements are accepted while unqualified causal claims still fail.
- Preserved literal `<BOS>` and `<UNK>` rendering after the initial English candidate exposed HTML-parsing loss of special-token labels.

## [1.0.1] - 2026-08-08

### Added
- A three-audience, five-minute onboarding path on the landing page.
- A documented, privacy-preserving aggregate analytics layer with DNT/GPC and local opt-out.
- Allow-listed campaign attribution and first-substantive-interaction events without experiment values or learner identifiers.
- Durable exact-tag evidence, uptake-reporting definitions, educator adoption guidance, classroom-pilot protocol, and launch materials.
- Educator classroom-feedback issue template and a reproducible public-metrics snapshot utility.

### Changed
- Standardized analytics coverage across the landing page, applets, and resource pages.
- Extended release-evidence retention and added a manual release-evidence publishing workflow.
- Synchronized Paper 7 with the final v1.0.0 verification record.

### Fixed
- Removed the stale pre-release 27-pass/2-fail/4-skip narrative from the research companion.
- Added a constrained-environment validation wrapper and clearer separation between software assurance and educational efficacy.


## 1.0.0 - 2026-07-25

### Verified public release

- Established a deterministic minimal GitHub Pages deployment boundary.
- Added standalone Verify and Deploy status badges.
- Required all 45 browser-based algorithm regression tests in continuous integration.
- Added fail-closed counting for passed, failed, and skipped algorithm cases.
- Added automated consistency checks for citation and release metadata.
- Published consistent citation and CodeMeta release metadata.

## 2026-07-24

### State reliability

- Made the current controls authoritative when copying an experiment link.
- Removed scenario and featured aliases from copied links so presets cannot overwrite later manual changes.
- Restored scenario presets before exact serialized controls so exact state wins.
- Added regression coverage for Overfitting degree, training-sample count, and regularization strength.

### Complete localization

- Extended English and Simplified Chinese coverage through every applet explanation, scenario, featured experiment, shared control, hint, footer, and educator-facing support page.
- Added immediate dynamic-hint translation for K-Means.
- Localized landing-page durations, developer-resource labels, and footer controls while preserving stable filenames, URLs, formulas, names, licenses, and code identifiers.
- Replaced the fixed glossary quota with concept-sized bilingual glossaries containing six to twelve matched terms.
- Added language preference persistence, language query propagation, and `hreflang` metadata on support pages.

### Teaching accuracy

- Introduced Ridge regression, coefficient vectors, the squared Euclidean norm, and lambda before using the regularization objective.
- Corrected the Bayes specificity example, polynomial coefficient count, full-batch gradient terminology, and several overbroad claims across the applet essays.
- Added complete English and Chinese explanations to all twelve applets.

### Resilience and verification

- Pre-rendered Explore scenarios so the panel remains useful before JavaScript enhancement.
- Expanded browser QA for Chinese content, dynamic translation, nonempty Explore panels, concept-sized glossaries, and authoritative copied state.
- Expanded release checks for localization surfaces, exact-state precedence, support-page language metadata, and the canonical social image.

## 2026-07-22

### Interface

- Rebuilt the landing page around a live search comparison and searchable applet catalogue.
- Organized every applet into Explore, Understand, Use in class, and Text and keyboard modes.
- Added shareable experiment states.
- Standardized Share, More, and Reset actions.
- Added twelve consistent applet color identities.
- Improved responsive layouts for mobile, tablet, and desktop use.

### Learning materials

- Added five learner scenarios to every applet.
- Added featured comparisons and visual explanations.
- Added bilingual key-term introductions.
- Added formatted student response packets.
- Added a Teacher Pack, Curriculum Map, and Student Lab Sheet.
- Added course-aligned and quick-entry sequences.

### Accessibility and portability

- Added keyboard guidance and text-state descriptions.
- Added reduced-motion support.
- Preserved single-file, offline-ready operation.
- Added portfolio, source, licensing, issue, and ORCID links.

### Software verification

- Added algorithmic tests for all twelve applets.
- Added automated source and browser checks.
- Added citation, architecture, contribution, security, and release metadata.

## Initial public release

- Twelve bilingual foundational-AI applets.
- Offline single-file operation.
- Open release under the MIT License.