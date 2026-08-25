# AI Playgrounds

> **Start in five minutes:** open the live site, choose one applet, make a prediction, change one variable, and explain the trace. The suite contains 14 multilingual, offline-ready applets with deterministic algorithm and browser verification. [Live suite](https://lmdixon23.github.io/ai-playgrounds/) · [Teacher Pack](teacher-pack.html) · [Activity Packs](activities/) · [Analytics and privacy](docs/ANALYTICS_AND_PRIVACY.md)

**Evidence boundary:** release checks establish bounded software behaviour and deployment integrity; they do not establish learning gains, classroom adoption, universal learner preference, or accessibility conformance.

[![Verify](https://github.com/lmdixon23/ai-playgrounds/actions/workflows/verify.yml/badge.svg?branch=main&event=push)](https://github.com/lmdixon23/ai-playgrounds/actions/workflows/verify.yml)
[![Deploy](https://github.com/lmdixon23/ai-playgrounds/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/lmdixon23/ai-playgrounds/actions/workflows/deploy-pages.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Archived v1.0.1 DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21854217.svg)](https://doi.org/10.5281/zenodo.21854217)

Fourteen multilingual, offline-ready interactive AI labs spanning foundational mechanisms and modern extensions. The suite covers search, logic, probability, machine learning, neural networks, computer vision, reinforcement learning, Transformer language modeling, and agent tool use/runtime protocols.

**Live site:** https://lmdixon23.github.io/ai-playgrounds/

**Current release:** [v1.5.1](https://github.com/lmdixon23/ai-playgrounds/releases/tag/v1.5.1)

**Archived v1.0.1 DOI:** [10.5281/zenodo.21854217](https://doi.org/10.5281/zenodo.21854217) · **All-versions DOI:** [10.5281/zenodo.21854216](https://doi.org/10.5281/zenodo.21854216)

### 15-second demo

[![AI Playgrounds demo showing the interactive suite in use](media/AI_Playgrounds_Demo_15s.gif)](https://lmdixon23.github.io/ai-playgrounds/media/AI_Playgrounds_Demo_15s.mp4)

**[▶ Open the full-resolution demo](https://lmdixon23.github.io/ai-playgrounds/media/AI_Playgrounds_Demo_15s.mp4)**

## Why this project exists

Foundational AI concepts are dynamic. A search frontier expands, evidence changes a posterior probability, a model begins to overfit, value propagates through repeated experience, causal self-attention changes a next-token distribution, or a tool observation changes the next justified agent action.

AI Playgrounds turns those mechanisms into direct experiments that learners can manipulate before implementing them in code.

Each applet includes:

- one focused AI concept,
- multilingual learner-facing support across English, Simplified Chinese, Vietnamese, and Spanish,
- a featured experiment and scenario gallery or equivalent prediction workflow,
- visual and text-based explanations,
- teacher notes and model limitations where appropriate,
- keyboard guidance,
- shareable/reproducible experiment state where appropriate,
- offline-ready operation without an account or backend.

## Course structure

The public catalogue has **12 Foundations/course-track labs** plus **2 Modern AI extensions**.

The Foundations track covers pathfinding, local search, Wumpus World, CNF/SAT, Bayes Rule, Bayesian Networks, KNN, overfitting, a tiny neural network, K-Means, convolution, and Q-Learning. The modern extensions are Transformer Language Modeling and Agent Tool Use and Context Protocols.

The planning matrix in [docs/AI_CURRICULUM_COVERAGE_MATRIX_2026-08-25.md](docs/AI_CURRICULUM_COVERAGE_MATRIX_2026-08-25.md) compares current coverage against AIMA and the Spring 2026 CS50/CSCI E-80 AI curriculum so future labs can balance classical gaps with contemporary extensions.

## Lab 13: Transformer Language Modeling

v1.2.0 added a deterministic decoder-like teaching model connecting token IDs, token/position vectors, Q/K/V projections, causal masking, self-attention, logits, temperature, and next-token probabilities. Its browser arithmetic is cross-checked against an independent Python reference.

The applet explicitly distinguishes attention weights from a general explanation of model reasoning, separates argmax probability from sampling, and treats its tokenizer/weights as small teaching fixtures rather than a reproduction of a frontier LLM.

v1.4.0 added a progressive Tokenize -> Represent -> Attend -> Predict journey. v1.5.0 added state-derived continuity, deterministic `Append argmax token`, and a saved baseline/current comparison while preserving frozen arithmetic.

## Lab 14: Agent Tool Use and Context Protocols

v1.3.0 added a deterministic agent-runtime lab separating model output, structured tool calls, schema validation, authorization, execution, observations, provenance-aware context updates, and stopping. Eight scenarios cover observation-driven replanning, overlapping schemas, invalid arguments, text versus execution, permission denial, instruction-like tool content, MCP 2026-07-28 serialization, and termination.

v1.4.0 made the runtime story explicitly visible as Propose -> Validate -> Authorize -> Execute -> Observe -> Update / choose next -> Stop. v1.5.0 added a state-derived action packet, explicit context delta, and learner-selected one-step sandbox. The sandbox uses a fresh in-memory simulated world and cannot perform a real external action.

## v1.5.0 engagement-excellence pass

v1.5.0 kept the suite at fourteen applets and applied an evidence-led engagement/immediate-impact pass rather than adding Lab 15. Four applets had a credible missing mechanism relation and received targeted additions:

- **Transformer Language Modeling:** continuous state journey, deterministic continuation, and baseline/current comparison.
- **Agent Tool Use and Context Protocols:** visible runtime packet, context delta, and isolated simulated-world sandbox.
- **CNF and SAT Builder:** a DPLL branch/prune tree derived from the existing solver trace.
- **Bayesian Network:** exact before/after posterior markers and percentage-point deltas.

The remaining ten applets were deliberately left unchanged at the behavior layer because the audit found no credible mechanism-level deficit justifying additional UI or animation. The acceptance record is in [docs/ENGAGEMENT_FIRST_MOVE_AUDIT.md](docs/ENGAGEMENT_FIRST_MOVE_AUDIT.md), the assurance model is in [docs/ENGAGEMENT_EXCELLENCE_FAS.md](docs/ENGAGEMENT_EXCELLENCE_FAS.md), and the human-evidence layer is defined in [docs/ENGAGEMENT_USABILITY_PROTOCOL.md](docs/ENGAGEMENT_USABILITY_PROTOCOL.md).

## v1.5.1 HCI and adoption hardening

v1.5.1 changes **no applet algorithm**. It adds the highest-value improvements identified by a second learner-centered Educational-HCI assurance pass:

- KNN Guided Challenge near-miss recovery so an imprecise mobile tap near a training point does not unexpectedly relocate the query and erase prediction progress;
- two-row Bayesian inference-method controls on narrow mobile layouts, including longer localized labels;
- Tiny Neural Network history-transport reflow for short mobile-landscape layouts;
- a PWP-inspired [learner-centered state/recovery contract](docs/HCI_STATE_RECOVERY_CONTRACT.md) covering initial state, learner action, expected state, recovery, focus, accessibility/state consistency, and failure paths;
- targeted 844×390 landscape, 390px touch, 200% text-enlargement, localized-component, autosave/recovery, and analytics browser checks;
- complete GoatCounter instrumentation across the built public HTML surface, including Labs 13/14 and Activity Packs;
- canonical page paths and titles, true GoatCounter events (`e=1`), and allow-listed campaign attribution while preserving the no-general-referrer and no-learner-content privacy boundary;
- two ready-to-assign **student Activity Pack canaries**, NN-1 and CNN-1.

## Activity Packs

The first Activity Packs are adapted from classroom worksheets and use a consistent inquiry structure:

**predict -> run -> observe -> explain -> transfer**

- [NN-1 · Make it fail, then make it learn](activities/nn-1.html) — non-linearity, hidden-layer capacity, training dynamics, and train/test generalization.
- [CNN-1 · Be the filter](activities/cnn-1.html) — hand-calculated convolution, directional edges, learned filters, and pooling.

Responses autosave **locally in the learner's browser** and can be printed or saved as PDF. AI Playgrounds has no assignment-submission backend. Teacher answer keys are intentionally not published on the student site.

## Explore

Build the deterministic v1.5.1 Pages artifact with:

```bash
python tools/build_site_v1_5_1.py
```

The deployed applets require no server, account, package manager, or backend. Labs 13 and 14 are generated into the public artifact from frozen source/localization inputs and remain self-contained. v1.5.1 composes its HCI/adoption layer over the immutable historical v1.5 builder rather than rewriting the previous release composition.

## Verification

The repository uses complementary verification layers. The release workflow includes the inherited pedagogical, localization, algorithm, Transformer, agent, engagement, public-integration, and broad browser gates plus the v1.5.1 HCI/adoption gate:

```bash
python tools/release_check.py
python tools/check_release_metadata.py
python tools/run_algorithm_tests.py
python tools/test_transformer_engagement_candidate.py
python tools/test_agent_tool_context_engagement_candidate.py
python tools/test_cnf_sat_engagement_candidate.py
python tools/test_bayes_network_engagement_candidate.py
python tools/test_v1_5_public_integration.py
python tools/test_v1_5_1_hci_adoption.py
python tools/browser_qa.py --no-screenshots
```

The v1.5.1 gate additionally verifies the 14-applet composition plus two Activity Pack canaries, analytics-wrapper coverage on every public HTML page, KNN touch recovery, four-locale Bayesian method containment, Neural Network landscape containment, 200% text-enlargement stress across all applets, Activity Pack autosave/guarded clear/focus recovery, canonical GoatCounter page/campaign data, true event semantics, and analytics opt-out behavior.

## Teaching materials

- [Teacher Pack](teacher-pack.html)
- [Activity Packs](activities/)
- [Curriculum Map](curriculum.html)
- [Student Lab Sheet](student-lab.html)
- [How the project works](quality.html)
- [Research and citation](research-and-citation.html)

## Research status

AI Playgrounds v1.5.1 is the current software release. The earlier v1.0.1 artifact remains immutable and archived at its version DOI. Its DOI should not be interpreted as a DOI for v1.5.1.

The deterministic/browser evidence supports implementation integrity and bounded design/interaction claims. It does not establish measured learning gains, universal learner preference, classroom adoption, or accessibility conformance. A separate human-usability protocol defines the evidence required for stronger claims.

A separate design-and-tools research manuscript about the suite remains in preparation. Publication of the software is not publication of that manuscript.

## Reuse and citation

The project is released under the MIT License.

- [Architecture](ARCHITECTURE.md)
- [Contributing](CONTRIBUTING.md)
- [Citation metadata](CITATION.cff)
- [Release notes](RELEASE_NOTES.md)
- [Localization standard](docs/LOCALIZATION.md)
- [Analytics and privacy](docs/ANALYTICS_AND_PRIVACY.md)

Built by Logan M. Dixon

- [Portfolio](https://lmdixon23.github.io/)
- [ORCID](https://orcid.org/0009-0001-0592-462X)
- [GitHub repository](https://github.com/lmdixon23/ai-playgrounds)
- [Releases](https://github.com/lmdixon23/ai-playgrounds/releases)
