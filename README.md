# AI Playgrounds

> **Start in five minutes:** open the live site, choose one applet, make a prediction, change one variable, and explain the trace. The suite contains 15 multilingual, offline-ready applets with deterministic algorithm and browser verification. [Live suite](https://lmdixon23.github.io/ai-playgrounds/) · [Teacher Pack](teacher-pack.html) · [Activity Packs](activities/) · [Analytics and privacy](docs/ANALYTICS_AND_PRIVACY.md)

**Evidence boundary:** release checks establish bounded software behaviour and deployment integrity; they do not establish learning gains, classroom adoption, universal learner preference, or accessibility conformance.

[![Verify](https://github.com/lmdixon23/ai-playgrounds/actions/workflows/verify.yml/badge.svg?branch=main&event=push)](https://github.com/lmdixon23/ai-playgrounds/actions/workflows/verify.yml)
[![Deploy](https://github.com/lmdixon23/ai-playgrounds/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/lmdixon23/ai-playgrounds/actions/workflows/deploy-pages.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Archived v1.0.1 DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21854217.svg)](https://doi.org/10.5281/zenodo.21854217)

Fifteen multilingual, offline-ready interactive AI labs spanning thirteen Foundations/course-track mechanisms and two Modern AI extensions. The suite covers uninformed and informed search, local search, adversarial search, logic, probability, machine learning, neural networks, computer vision, reinforcement learning, Transformer language modeling, and agent tool use/runtime protocols.

**Live site:** https://lmdixon23.github.io/ai-playgrounds/

**Current release:** [v1.8.1](https://github.com/lmdixon23/ai-playgrounds/releases/tag/v1.8.1)

**Archived v1.0.1 DOI:** [10.5281/zenodo.21854217](https://doi.org/10.5281/zenodo.21854217) · **All-versions DOI:** [10.5281/zenodo.21854216](https://doi.org/10.5281/zenodo.21854216)

### 15-second demo

[![AI Playgrounds demo showing the interactive suite in use](media/AI_Playgrounds_Demo_15s.gif)](https://lmdixon23.github.io/ai-playgrounds/media/AI_Playgrounds_Demo_15s.mp4)

**[▶ Open the full-resolution demo](https://lmdixon23.github.io/ai-playgrounds/media/AI_Playgrounds_Demo_15s.mp4)**

## Why this project exists

Foundational AI concepts are dynamic. A search frontier expands, evidence changes a posterior probability, a model begins to overfit, a game-tree value backs up through an opponent's move, value propagates through reinforcement learning, causal self-attention changes a next-token distribution, or a tool observation changes the next justified agent action.

AI Playgrounds turns those mechanisms into direct experiments that learners can manipulate before implementing them in code.

Each applet includes:

- one focused AI concept,
- multilingual learner-facing support across English, Simplified Chinese, Vietnamese, and Spanish,
- a featured experiment and scenario-led prediction workflow,
- visual and text-based explanations,
- teacher notes and model limitations where appropriate,
- keyboard guidance,
- shareable/reproducible experiment state where appropriate,
- offline-ready operation without an account or backend.

## Course structure

The public catalogue has **13 Foundations/course-track labs** plus **2 Modern AI extensions**.

The Foundations track covers pathfinding, local search, Wumpus World, CNF/SAT, Bayes Rule, Bayesian Networks, KNN, overfitting, a tiny neural network, K-Means, convolution, Q-Learning, and Game Trees with Minimax/Alpha-Beta. The modern extensions are Transformer Language Modeling and Agent Tool Use and Context Protocols.

The planning matrix in [docs/AI_CURRICULUM_COVERAGE_MATRIX_2026-08-25.md](docs/AI_CURRICULUM_COVERAGE_MATRIX_2026-08-25.md) compares coverage against AIMA and the Spring 2026 CS50/CSCI E-80 AI curriculum.

## v1.8.1: modern-lab learner parity

v1.8.1 corrects an overly narrow earlier parity claim. Transformer Language Modeling, Agent Tool Use, and Minimax/Alpha-Beta already shared the release shell, but their learner-facing sequence was materially thinner than the first twelve applets.

Each now has one featured experiment, five plain-language predict–run–explain scenarios, a terminology primer, a step-by-step mechanism explanation, and teacher prompts in EN/ZH/VI/ES. Scenario buttons apply the existing native controls; no second algorithm or simulation state was added.

The patch also shortens their catalogue descriptions, exposes Share / Embed / JSON / Reset in the established action-row style, removes the always-open duplicate state mirror, makes Quick Assign state capture learner-triggered, and fixes dark-theme legibility for headings, actions, Transformer mask/warning surfaces, agent semantic states, and Minimax controls/cards/SVG nodes. See [the detailed v1.8.1 release notes](docs/RELEASE_V1_8_1.md).

## v1.8.0: algorithm modes and reproducible comparison

v1.8.0 adds three opt-in mechanism modes while preserving the original behavior and the fifteen-lab curriculum boundary:

- **Hill Climbing / Simulated Annealing** adds seeded repeated-restart benchmarking. Selected algorithms receive the same generated problem and starting state on each restart, and the lab reports success frequency separately from final and best cost.
- **K-Nearest Neighbors** adds continuous-target regression. It reuses the same neighbor selection, distance metrics, feature scaling, and uniform/distance weights, then predicts with the corresponding mean instead of a class vote.
- **CNF/SAT** adds a bounded educational CDCL trace with implication reasons, first-UIP clause learning, and non-chronological backjumping. The original DPLL trace remains the default.

All three modes preserve shareable state, local-only Quick Assign responses, hard-reset recovery, and EN/ZH/VI/ES presentation. Their fidelity disclosures distinguish the inspectable teaching implementations from production solvers or hardware-performance benchmarks. See [the detailed v1.8.0 release notes](docs/RELEASE_V1_8_0.md).

## v1.7.2: modern-lab shell parity and release assurance

v1.7.2 completed mature product-shell and assignment-support parity for Transformer Language Modeling, Agent Tool Use, and Minimax/Alpha-Beta while preserving their concept-specific mechanism bodies. v1.8.1 later corrected the remaining learner-curriculum depth gap.

Labs 13-15 now share the established Share / More / Reset hierarchy, skip link, Big idea / What to watch orientation, local settings export, key terms, text-and-keyboard support, model-fidelity disclosure, suite provenance, and complete discovery metadata. Their existing Quick Assigns now refresh from the real text-equivalent mechanism state, copy state plus responses, print only the packet, and localize action/accessibility labels across EN/ZH/VI/ES without erasing learner text.

The release also makes final composition repeatable, syntax-validates every final inline script, directly exercises packet/share/embed/export/theme behavior, and prevents Pages deployment from preceding a successful exact-sha Verify result. See [the detailed v1.7.2 release notes](docs/RELEASE_V1_7_2.md).

## v1.7.1: shared theme behavior across all labs

v1.7.1 is a compatibility/consistency patch. It does not add or change an AI mechanism, lab, language, Quick Assign, or curriculum unit.

The original applets and the standardized Labs 13–15 shell now share the same persisted `theme` preference. A theme choice made in an original lab therefore carries into Transformer Language Modeling, Agent Tool Use, and Minimax/Alpha-Beta. Existing users of the temporary modern-shell `ai-playgrounds-theme` key are migrated once to the canonical `theme` key, and modern labs follow the system dark preference when no stored preference exists.

The patch preserves the v1.7.0 public boundary: 15 applets, 58 deployed files, all 15 Level-1 Quick Assigns, four learner-facing languages, two Level-2 Activity Pack canaries, and unchanged algorithm/curriculum semantics.

## v1.7.0: Quick Assigns for every lab

v1.7.0 completed the Level 1 teacher-assignment layer without adding another algorithm or a sixteenth lab.

Every public applet has one stable **Quick Assign** ID and a canonical classroom link. The activities are designed for about 10–15 minutes and use the shared inquiry spine:

**predict -> run/manipulate -> observe -> explain -> transfer**

The fifteen IDs are:

- `QA-SEARCH-01`
- `QA-LOCAL-01`
- `QA-WUMPUS-01`
- `QA-SAT-01`
- `QA-BAYES-01`
- `QA-BN-01`
- `QA-KNN-01`
- `QA-OVERFIT-01`
- `QA-NN-01`
- `QA-KMEANS-01`
- `QA-CNN-01`
- `QA-QL-01`
- `QA-MINIMAX-01`
- `QA-TRANSFORMER-01`
- `QA-AGENT-01`

The original twelve applets reuse their existing classroom response-packet machinery. Labs 13–15 use a local-only Quick Assign response surface aligned to their existing Guided Challenges. Responses remain in the learner's browser unless deliberately copied or printed. No response or answer text is sent to AI Playgrounds analytics.

Teacher Pack and Curriculum routes list all fifteen canonical activity links. EN/ZH/VI/ES presentation and response preservation are tested under the supported paths. v1.7.0 also removed the Activity Pack footer's drifting current-release suffix and constrained the Lab 15 challenge selector on narrow mobile layouts.

## Lab 15: Game Trees, Minimax, and Alpha-Beta Pruning

v1.6.0 added a deterministic adversarial-search playground for finite, two-player, zero-sum, perfect-information game trees. Learners back terminal utilities through alternating MAX and MIN nodes, then compare full minimax with Alpha-Beta on the same tree and child order.

The core relation is:

`terminal utilities -> recursive MIN/MAX backups -> root value and move`

The Alpha-Beta experiment keeps the exact minimax result while exposing safe cutoffs. Pruned nodes remain visible and are explicitly marked **not evaluated**, so pruning is not misrepresented as deleting part of the game or as an approximation. A move-order comparison demonstrates:

`same tree + different child order -> different search work -> same exact minimax result`

The lab includes editable terminal utilities, deterministic trace playback, saved-run comparison, five prediction-before-reveal Guided Challenges, EN/ZH/VI/ES state-preserving localization, reduced-motion support, text-equivalent state, mobile/split-screen containment, and 200% text-enlargement regression coverage.

## Labs 13 and 14

**Transformer Language Modeling** connects token/position representation, causal self-attention, logits, temperature, and next-token probabilities in a deterministic toy decoder-like model. It explicitly separates attention from a general explanation of reasoning and distinguishes argmax from sampling.

**Agent Tool Use and Context Protocols** separates model text, structured tool calls, validation, authorization, execution, observations, provenance-aware context updates, and stopping in a deterministic simulated tool world. Text is not execution, schema validity is not authorization, and no real external action occurs.

## Product hardening inherited from v1.5 through v1.8

v1.5 applied mechanism-first engagement improvements only where the Full Assurance Stack found a real missing relation. v1.5.1 added learner-centered HCI/adoption hardening, corrected privacy-minimized GoatCounter semantics, and the NN-1/CNN-1 Activity Pack canaries. v1.6.0 added Minimax/Alpha-Beta. v1.6.1 standardized cross-suite product contracts and introduced the first four Quick Assign canaries. v1.6.2 normalized current-version provenance in the exact deployed artifact. v1.7.0 promoted the Quick Assign layer to all fifteen labs. v1.7.1 aligned modern-shell theme persistence. v1.7.2 completed bounded product-shell parity and final-artifact assurance. v1.8.0 added three opt-in deterministic mechanism modes. v1.8.1 completes the previously missing modern-lab learner sequence and dark-theme parity without changing the applet, assignment, locale, or privacy boundaries.

## Quick Assigns and Activity Packs

**Level 1 Quick Assigns** are approximately 10–15 minutes and are available for all fifteen labs through stable IDs and classroom-mode links.

**Level 2 Activity Packs** remain the longer pilot resources:

- [NN-1 · Make it fail, then make it learn](activities/nn-1.html): non-linearity, hidden-layer capacity, training dynamics, and train/test generalization.
- [CNN-1 · Be the filter](activities/cnn-1.html): hand-calculated convolution, directional edges, learned filters, and pooling.

Both layers use the inquiry spine:

**predict -> run/manipulate -> observe -> explain -> transfer**

Responses remain local to the learner's browser unless the learner or teacher deliberately copies, exports, or prints them. AI Playgrounds has no assignment-submission backend. Teacher answer keys are intentionally not published on the student site.

## Explore

Build the deterministic v1.8.1 Pages artifact with:

```bash
python tools/build_site_v1_8_1.py
```

The deployed applets require no server, account, package manager, or backend. Labs 13, 14, and 15 are generated deterministically into the public artifact and remain self-contained offline HTML files after generation.

## Verification

The release workflow retains the complete inherited suite and adds exact v1.8.1 learner-parity, deterministic composition, localization/state, contrast, and browser-behavior gates:

```bash
python tools/release_check.py
python tools/test_current_docs_consistency.py
python tools/check_release_metadata.py
python tools/run_algorithm_tests.py
python tools/test_minimax_alpha_beta.py
python tools/test_minimax_alpha_beta_cross_runtime.py
python tools/test_minimax_alpha_beta_multilingual_applet.py
python tools/test_v1_6_public_integration.py
python tools/test_v1_5_1_hci_adoption.py
python tools/test_v1_5_1_hci_extended.py
python tools/test_v1_6_1_quick_assign_currency.py
python tools/test_v1_6_1_design_consistency.py
python tools/test_v1_6_2_public_provenance.py
python tools/test_v1_7_all_quick_assigns.py
python tools/test_v1_7_public_release.py
python tools/test_v1_7_1_modern_shell.py
python tools/test_v1_7_1_public_release.py
python tools/test_v1_7_2_modern_parity.py
python tools/test_v1_8_public_release.py
python tools/test_v1_8_algorithm_modes.py
python tools/test_v1_8_algorithm_modes_browser.py
python tools/test_v1_8_1_modern_learner_parity.py
python tools/test_v1_8_1_modern_learner_parity_browser.py
python tools/browser_qa.py --no-screenshots
```

The v1.8.1 public boundary remains 15 applets and 58 deployed files. The three Activity Pack pages remain the index, NN-1, and CNN-1. Every public HTML page receives the privacy-minimized analytics wrapper exactly once, while applet state, worksheet answers, Quick Assign responses, free text, and experiment values remain excluded from analytics requests.

## Teaching materials

- [Teacher Pack](teacher-pack.html)
- [Activity Packs](activities/)
- [Curriculum Map](curriculum.html)
- [Student Lab Sheet](student-lab.html)
- [How the project works](quality.html)
- [Research and citation](research-and-citation.html)

## Research status

AI Playgrounds v1.8.1 is the current software release. The earlier v1.0.1 artifact remains immutable and archived at its version DOI. Its DOI should not be interpreted as a DOI for v1.8.1.

The deterministic/browser evidence supports implementation integrity and bounded design/interaction claims. It does not establish measured learning gains, universal learner preference, classroom adoption, or accessibility conformance. The human-usability protocol defines the evidence required for stronger claims.

A separate design-and-tools research manuscript about the suite remains in preparation. Publication of the software is not publication of that manuscript.

## Reuse and citation

The project is released under the MIT License.

- [Architecture](ARCHITECTURE.md)
- [Applet design-system contract](docs/APPLET_DESIGN_SYSTEM_CONTRACT.md)
- [Quick Assign architecture](docs/QUICK_ASSIGN_ARCHITECTURE.md)
- [Public surface locale matrix](docs/PUBLIC_SURFACE_LOCALE_MATRIX.md)
- [Contributing](CONTRIBUTING.md)
- [Citation metadata](CITATION.cff)
- [Release notes](docs/RELEASE_V1_8_1.md)
- [Localization standard](docs/LOCALIZATION.md)
- [Analytics and privacy](docs/ANALYTICS_AND_PRIVACY.md)

Built by Logan M. Dixon

- [Portfolio](https://lmdixon23.github.io/)
- [ORCID](https://orcid.org/0009-0001-0592-462X)
- [GitHub repository](https://github.com/lmdixon23/ai-playgrounds)
- [Releases](https://github.com/lmdixon23/ai-playgrounds/releases)
