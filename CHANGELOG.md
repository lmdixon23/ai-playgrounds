# Changelog

## [1.6.0] - 2026-08-25

### Added
- Lab 15, **Game Trees: Minimax and Alpha-Beta Pruning**, as the fifteenth public applet and thirteenth Foundations/course-track lab.
- An independent Python minimax/alpha-beta reference with fail-closed tree validation, deterministic traces, adversarial fixtures, and a 648-case bounded exhaustive census.
- An independently implemented JavaScript core with recursive Python/JavaScript parity, including a parity-harness self-test and matching validation categories.
- Five prediction-before-reveal Guided Challenges covering root choice, MIN backup, safe pruning, move ordering, and greedy-versus-minimax reasoning.
- Complete EN/ZH/VI/ES semantic localization with protected algorithm/state identifiers and state-preserving locale switching.
- A Lab 15 engagement and learner-centered HCI audit plus a permanent v1.6 public/HCI browser gate.

### Changed
- Expanded the deterministic Pages boundary from fourteen applets / 57 files to fifteen applets / 58 files while retaining exactly the three Activity Pack pages introduced in v1.5.1.
- Expanded the Foundations/course track from twelve to thirteen labs; Transformer Language Modeling and Agent Tool Use remain the two Modern AI extensions.
- Updated landing, curriculum, Teacher Pack, sitemap, README, citation metadata, CodeMeta, analytics coverage, deployment composition, and release automation for v1.6.0.
- Preserved the v1.5.1 HCI, responsive, Activity Pack, and privacy-minimized GoatCounter hardening while adding Lab 15 to the same release-quality boundary.

### Verification and evidence boundary
- Lab 15 pre-integration evidence includes 26 Python reference tests, a 648-case exhaustive census, independent cross-runtime parity, 22 prototype browser checks, 22 English-candidate browser checks, 1,235 semantic-localization checks, and a four-locale state-preservation gate.
- The release-level v1.6 gate additionally checks exact safe cutoffs, move-order work invariance, prediction locking, locale-state invariance, reduced motion, 390×844 portrait, 844×390 landscape, 640×720 split view, and 200% text enlargement.
- Software/browser assurance establishes behavior under tested conditions; it does not establish accessibility conformance, measured learning gains, classroom adoption, or universal learner preference.
- The immutable v1.0.1 DOI remains historical provenance and is not reassigned to v1.6.0.

## [1.5.1] - 2026-08-25

### Added
- Two ready-to-assign public student Activity Pack canaries: **NN-1 Make it fail, then make it learn** and **CNN-1 Be the filter**, both structured around predict -> run -> observe -> explain -> transfer and local-only response autosave.
- A learner-centered state/recovery QA contract adapted from the audited PWP Notebook interaction model: initial state -> learner action -> expected state -> recovery path -> focus/accessibility/state consistency.
- Dedicated v1.5.1 browser checks for KNN touch recovery, four-locale Bayesian method containment, Tiny Neural Network mobile-landscape transport, 200% text enlargement, Activity Pack autosave/clear/focus recovery, and GoatCounter payload semantics.

### Changed
- Rebound the deterministic public composition to v1.5.1 while preserving all fourteen applet algorithms and the complete v1.5 engagement layer.
- Expanded the Pages artifact from 54 to 57 files by adding the Activity Pack index plus two student activity pages; the applet count remains fourteen.
- Reworked the privacy-minimized GoatCounter wrapper so every public HTML page, including Labs 13/14 and Activity Packs, receives exactly one wrapper; page views now send canonical paths and titles, synthetic interactions use true GoatCounter events (`e=1`), and allow-listed `ap_src` values populate GoatCounter campaign query data.
- Updated Teacher Pack, quality, README, analytics/privacy, citation, and CodeMeta metadata for the fourteen-lab Foundations + Modern Extensions model and the Activity Pack pilot.

### Fixed
- Added KNN Guided Challenge near-miss recovery so an imprecise mobile tap near a training point selects the intended nearby point instead of unexpectedly relocating the query and clearing prediction progress.
- Reflowed Bayesian Network inference-method controls into a two-row mobile layout so longer EN/VI/ES labels remain visible at 390 px.
- Reflowed Tiny Neural Network history/scrub controls for short mobile-landscape layouts.
- Eliminated analytics blind spots for Transformer Language Modeling and Agent Tool Use, normalized `/index.html` aliases, supplied page titles, and separated events from page-visit totals.

### Evidence boundary
- The v1.5.1 software/browser assurance establishes behavior under the tested conditions; it does not establish accessibility conformance, measured learning gains, classroom adoption, or universal learner preference.
- Teacher answer keys remain outside the public student site.
- The immutable v1.0.1 DOI remains historical provenance and is not reassigned to v1.5.1.

## [1.5.0] - 2026-08-25

### Added
- A state-derived Lab 13 continuity layer that keeps Tokens, Represent, Attend, and Predict visually connected, plus deterministic argmax continuation and exact baseline-versus-current comparison.
- A Lab 14 runtime packet that visibly traverses actual validation, authorization, execution, observation, context-update, and stopping gates, together with an explicitly isolated learner-selected simulated-world sandbox.
- A CNF/SAT DPLL branch-and-prune tree derived read-only from the existing DPLL trace; no second solver is introduced.
- An exact Bayesian-network before/after posterior comparison that preserves the previous exact belief as a marker and highlights the largest percentage-point change.
- Full Assurance Stack, applet-by-applet engagement acceptance audit, human usability protocol, and dedicated v1.5 public integration QA.

### Changed
- Promoted the four mechanism-faithful engagement candidates into the fourteen-applet v1.5 public composition while preserving the deterministic 54-file Pages boundary.
- Deliberately left Pathfinding, Hill Climbing/Simulated Annealing, Wumpus World, Bayes Rule, KNN, Overfitting, Tiny Neural Network, K-Means, Convolution, and Q-Learning behavior unchanged because the audit found no credible mechanism-level deficit that justified additional UI or animation.
- Updated release provenance and deployment/release automation for v1.5.0 while preserving historical v1.0.1 DOI ownership.

### Fixed
- Hardened Guided Challenge browser timing against shared-runner startup variance without weakening assertions.
- Isolated candidate localization surfaces so locale switching cannot rewrite machine state or create translation feedback loops.
- Constrained the Lab 14 runtime lane at 390 px and repaired the CNF/Bayesian candidate mounting order discovered by adversarial browser QA.
- Replaced invalid or timing-sensitive adversarial test fixtures with parser-valid, state-stable fixtures that exercise the same intended mechanisms.

## [1.4.0] - 2026-08-25

### Added
- A mechanism-journey layer for Lab 13 that lets learners move through Tokenize, Represent, Attend, and Predict without changing the frozen Transformer arithmetic or learner state.
- A seven-stage runtime journey for Lab 14 that makes Propose, Validate, Authorize, Execute, Observe, Update/choose next, and Stop visually distinct while preserving the frozen deterministic runtime.
- A curriculum coverage matrix comparing the fourteen-app suite with AIMA 4th edition and the Spring 2026 CS50/CSCI E-80 AI curriculum, including prioritized classical and contemporary gaps for future labs.
- Dedicated v1.4 browser and integration gates covering engagement-state invariance, language-selection state preservation, curriculum completeness, and 390 px containment.

### Changed
- Replaced the remaining prominent Lab 13 and Lab 14 four-button locale controls with native EN/ZH/VI/ES selectors while retaining `?lang=` deep links and existing localization runtimes.
- Adapted landing and support-page language controls to native selectors using only the translations actually available on those surfaces.
- Moved Lab 13 and Lab 14 software-version provenance out of the hero treatment and into secondary page provenance while retaining explicit release metadata.
- Reframed the curriculum around Foundations / course track, Modern AI extensions, and the existing quick-entry sampler; Lab 14 is now explicitly a modern extension while Lab 13 remains at the advanced introductory/modern boundary.
- Regenerated the curriculum applet map from the complete fourteen-entry release inventory so generated Labs 13 and 14 remain present in navigation.
- Preserved the fourteen-applet, 54-file deterministic Pages boundary; v1.4 adds no Lab 15.

### Fixed
- Removed a mutation-observer feedback loop discovered by the first Lab 14 v1.4 browser gate and replaced it with event-driven presentation updates.
- Corrected the first full-site v1.4 acceptance pass after it exposed an incomplete generated curriculum applet map and an over-specific Simplified-Chinese `lang` assertion.

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
- A single-file Transformer applet covering token representation, position information, Q/K/V projections, causal masking, self-attention, logits, next-token probabilities, temperature, and bounded attention perturbations.
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
