# Changelog

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
