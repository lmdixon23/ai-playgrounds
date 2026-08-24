# AI Playgrounds Curriculum Coverage Matrix

Date: 2026-08-25

Status: planning document only. This document does not authorize implementation of Lab 15 or later labs.

Baseline: AI Playgrounds v1.3.0, fourteen public applets.

## Purpose

AI Playgrounds began with a broad AIMA-aligned introductory-AI sequence and now also contains modern extensions. The goal of this matrix is to prevent future expansion from drifting into only contemporary topics while important classical introductory-AI mechanisms remain uncovered.

This matrix compares the fourteen current applets against two reference curricula:

1. Stuart Russell and Peter Norvig, *Artificial Intelligence: A Modern Approach*, 4th edition (AIMA), using the official chapter-level table of contents: https://aima.cs.berkeley.edu/global-index.html
2. Harvard CSCI E-80 / CS50's *Introduction to Artificial Intelligence with Python*, Spring 2026, using the official lecture-topic list: https://cs50.harvard.edu/extension/ai/2026/spring/lectures/

The comparison is instructional rather than bibliographic. A lab counts as direct coverage only when a learner can inspect or manipulate the central mechanism, not merely when the page mentions the topic.

## Status legend

- **Direct** — one or more current applets directly teach and expose the central mechanism.
- **Partial** — current applets cover part of the topic or an adjacent mechanism, but a major instructional component is absent.
- **Gap** — no current applet meaningfully exposes the mechanism.
- **Context** — important curricular framing, but not necessarily a good standalone playground target.
- **Extension** — useful modern material outside the core AIMA/CS50 backbone.

## Current fourteen-app inventory

| # | Applet | Primary area |
|---:|---|---|
| 1 | Pathfinding Visualizer | graph and heuristic search |
| 2 | Hill Climbing and Simulated Annealing | local search and optimization |
| 3 | Wumpus World | logical agents and inference |
| 4 | CNF and SAT Builder | propositional logic and satisfiability |
| 5 | Bayes Rule Playground | probability and Bayesian updating |
| 6 | Bayesian Network | probabilistic graphical inference |
| 7 | K-Nearest Neighbors | supervised classification |
| 8 | Overfitting Explorer | regression-style fitting, validation, generalization |
| 9 | Tiny Neural Network | feed-forward neural networks and nonlinearity |
| 10 | K-Means Clustering | unsupervised clustering |
| 11 | Convolution Playground | convolutional vision mechanisms |
| 12 | Q-Learning Gridworld | model-free reinforcement learning |
| 13 | Transformer Language Modeling | causal self-attention and next-token prediction |
| 14 | Agent Tool Use and Context Protocols | modern agent runtime/tool-use extension |

---

# A. AIMA 4th-edition chapter coverage

| AIMA chapter | Current coverage | Status | Main missing mechanism / note | Standalone-lab priority |
|---|---|---|---|---|
| 1. Introduction | Suite-wide | Context | Historical/field framing is better handled by curriculum materials than a mechanism lab. | Low |
| 2. Intelligent Agents | Wumpus World; Agent Tool Use | Partial | Wumpus covers percept/inference/action; Lab 14 covers a modern tool-using runtime. A general PEAS/rational-agent lab is not essential. | Low |
| 3. Solving Problems by Searching | Pathfinding Visualizer | **Direct** | BFS/DFS/Dijkstra/A* already provide a strong state-space and heuristic-search foundation. | Covered |
| 4. Search in Complex Environments | Hill Climbing and Simulated Annealing | **Direct/Partial** | Local search is strong; broader complex-environment search is not exhaustive. | Covered enough |
| 5. Constraint Satisfaction Problems | — | **Gap** | Variables, domains, constraints, backtracking, MRV, degree heuristic, LCV, forward checking/arc consistency. | **Must-have** |
| 6. Adversarial Search and Games | — | **Gap** | Minimax, evaluation functions, game trees, alpha-beta pruning, move ordering. | **Must-have** |
| 7. Logical Agents | Wumpus World; CNF and SAT Builder | **Direct** | Strong propositional/logical-agent coverage. | Covered |
| 8. First-Order Logic | — | **Gap** | Predicates, quantifiers, relations, substitution/unification. | High-value classical |
| 9. Inference in First-Order Logic | — | **Gap** | Unification, forward/backward chaining in FOL, generalized resolution. | High-value classical |
| 10. Knowledge Representation | Wumpus World; CNF/SAT | Partial | Existing labs focus mostly on propositional facts/clauses, not richer ontology/relations/events/defaults. | Medium |
| 11. Automated Planning | — | **Gap** | States, actions, preconditions/effects, planning graphs or forward search; Blocks World is a strong visual candidate. | **High** |
| 12. Quantifying Uncertainty | Bayes Rule | **Direct** | Base rates and conditional probability are explicit. | Covered |
| 13. Probabilistic Reasoning | Bayesian Network; Bayes Rule | **Direct** | Exact/sampling inference and explaining away are already central. | Covered |
| 14. Probabilistic Reasoning over Time | — | **Gap** | Markov models, HMM filtering/prediction/smoothing, Viterbi/state estimation. | **Must-have / High** |
| 15. Making Simple Decisions | Bayes Rule; Bayesian Network; Q-Learning | Partial | Probabilities are present, but utility, expected utility, decision networks, and value of information are not directly taught. | Medium-high |
| 16. Making Complex Decisions | Q-Learning Gridworld | Partial | Q-learning gives model-free control, but explicit MDPs, Bellman expectation/value iteration, policy iteration, and POMDP ideas are absent. | **High** |
| 17. Multiagent Decision Making | — | **Gap** | Lab 14 is not multiagent game/decision theory. Strategic interaction and equilibria remain absent. | Medium |
| 18. Probabilistic Programming | — | **Gap** | Important advanced AIMA topic, but lower introductory/high-school priority. | Low-medium |
| 19. Learning from Examples | KNN; Overfitting; Tiny Neural Network | **Direct/Partial** | Classification/generalization are strong; explicit regression mechanics and margin-based SVM classification are not dedicated. | Medium-high |
| 20. Knowledge in Learning | — | **Gap** | Prior knowledge/inductive bias/knowledge-guided learning are not directly represented. | Low-medium |
| 21. Learning Probabilistic Models | Bayesian Network | Partial | The current Bayesian Network lab performs inference; it does not primarily teach parameter/structure learning. | Medium |
| 22. Deep Learning | Tiny Neural Network; Convolution; Transformer | **Direct** | Feed-forward, CNN-like, and Transformer mechanisms give unusually broad coverage. | Covered |
| 23. Reinforcement Learning | Q-Learning Gridworld | **Direct/Partial** | Model-free Q-learning is strong; model-based RL/value iteration is still a useful complement. | Covered core; extend later |
| 24. Natural Language Processing | Transformer Language Modeling | Partial | Modern language modeling is strong, but CFG parsing, n-grams, text classification, and embeddings are absent. | **High** |
| 25. Deep Learning for Natural Language Processing | Transformer Language Modeling | **Direct** | Lab 13 directly exposes causal self-attention and next-token probabilities. | Covered core |
| 26. Robotics | — | **Gap** | Localization, sensing, motion/planning, particle filters, mapping. | High visual potential; medium curricular priority |
| 27. Computer Vision | Convolution Playground | **Direct/Partial** | Convolution/filtering is strong; detection/recognition and broader vision pipelines are not represented. | Covered foundation |
| 28. Philosophy, Ethics, and Safety of AI | Lab 14 evidence/security boundaries; suite misconception work | Partial | No dedicated ethics/safety decision lab. A mechanism-oriented suite may handle much of this through cross-lab framing rather than a single simulation. | Medium |
| 29. The Future of AI | — | Context | Better treated as discussion/reading than deterministic playground mechanism. | Low |

## AIMA interpretation

The largest classical gaps are not peripheral. They occur in the center of the standard AIMA progression: **adversarial search/games, constraint satisfaction, first-order logic, automated planning, temporal probabilistic reasoning, and explicit decision-process methods**.

The current suite is comparatively strong in ordinary search, local search, propositional logic, Bayesian reasoning, introductory machine learning, deep learning, convolution, reinforcement learning, and Transformer mechanisms.

---

# B. CS50 AI / CSCI E-80 Spring 2026 coverage

The current 2026 Harvard lecture sequence remains Search, Knowledge, Uncertainty, Optimization, Learning, Neural Networks, and Language. The matrix below scores the named subtopics in that official lecture list.

| CS50 lecture | Topic | Current applet(s) | Status | Gap significance |
|---|---|---|---|---|
| Search | graph search | Pathfinding | **Direct** | covered |
| Search | heuristic search | Pathfinding | **Direct** | covered |
| Search | adversarial search | — | **Gap** | **critical** |
| Search | alpha-beta pruning | — | **Gap** | **critical** |
| Knowledge | knowledge representation | Wumpus; CNF/SAT | Partial | moderate |
| Knowledge | propositional logic | Wumpus; CNF/SAT | **Direct** | covered |
| Knowledge | inference | Wumpus; CNF/SAT | **Direct/Partial** | mostly covered for propositional systems |
| Knowledge | resolution | CNF/SAT adjacent | Partial | explicit resolution is not the main current mechanism |
| Knowledge | first-order logic | — | **Gap** | high |
| Uncertainty | probability | Bayes Rule | **Direct** | covered |
| Uncertainty | random variables | Bayes Rule; Bayesian Network | **Direct/Partial** | covered enough for introductory use |
| Uncertainty | probabilistic inference | Bayes Rule; Bayesian Network | **Direct** | covered |
| Uncertainty | Bayesian Networks | Bayesian Network | **Direct** | covered |
| Uncertainty | Markov Models | — | **Gap** | **critical/high** |
| Optimization | local search | Hill Climbing / Simulated Annealing | **Direct** | covered |
| Optimization | hill climbing | Hill Climbing / Simulated Annealing | **Direct** | covered |
| Optimization | constraint satisfaction | — | **Gap** | **critical** |
| Optimization | backtracking search | — | **Gap** | **critical** |
| Learning | classification | KNN | **Direct** | covered |
| Learning | regression | Overfitting Explorer | Partial | polynomial fitting/generalization is present, but regression itself is not the dedicated instructional target |
| Learning | support vector machines | — | **Gap** | medium-high |
| Learning | reinforcement learning | Q-Learning | **Direct** | covered |
| Learning | clustering | K-Means | **Direct** | covered |
| Neural Networks | feed-forward networks | Tiny Neural Network | **Direct** | covered |
| Neural Networks | backpropagation | Tiny Neural Network | **Direct/Partial** | mechanism is present; could be checked in a later parity audit |
| Neural Networks | convolutional networks | Convolution | **Direct** | covered |
| Neural Networks | recurrent networks | — | **Gap** | medium; historically/core sequence material but less urgent than CSP/games/HMM |
| Language | context-free grammar | — | **Gap** | high for CS50 alignment |
| Language | n-gram models | — | **Gap** | high |
| Language | Naive Bayes | Bayes Rule only adjacent | **Gap/Partial** | text-classification mechanism is absent |
| Language | word2vec | — | **Gap** | **high and highly visualizable** |
| Language | transformers | Transformer Language Modeling | **Direct** | covered |

## CS50 interpretation

For a teacher following a CS50-AI-like high-school sequence, the most conspicuous missing experiences are:

1. **Minimax and alpha-beta pruning**
2. **Constraint satisfaction and backtracking**
3. **Markov / hidden-state temporal reasoning**
4. **First-order logic**
5. **Pre-Transformer language mechanisms**: CFG parsing, n-grams, Naive Bayes text classification, and word embeddings
6. **SVM / explicit regression mechanics**
7. **Recurrent neural networks**

This means Lab 13 fits the end of the current CS50 language sequence much more naturally than Lab 14. Lab 14 should remain a clearly labeled modern extension rather than redefining the core curriculum order.

---

# C. Recommended gap taxonomy

## Tier A — core gaps worth adding before the suite is considered broadly complete

| Candidate | Why Tier A | Visual mechanism / memorable moment |
|---|---|---|
| **Game Trees: Minimax & Alpha-Beta Pruning** | AIMA core + CS50 Search; completely absent | utilities propagate up the tree; alpha-beta visibly cuts branches; move ordering changes work without changing the correct move |
| **Constraint Satisfaction: Map Coloring / Sudoku** | AIMA core + CS50 Optimization; completely absent | domains shrink under propagation; contradictions trigger backtracking; MRV/LCV/arc consistency alter the search |
| **Markov Models / Hidden Markov Models & Viterbi** | AIMA temporal probability + CS50 Uncertainty; completely absent | hidden-state beliefs move over time as evidence arrives; Viterbi path diverges from per-step local guesses |
| **Classical Planning / Blocks World** | central AIMA planning topic; distinct from pathfinding and agent tool use | preconditions/effects animate state changes; a plan is built or fails because an action is not applicable |
| **MDP / Value Iteration** | closes the conceptual gap behind Q-learning | Bellman backups sweep the grid; values converge; policy changes; compare known-model planning to learned Q-values |

## Tier B — high-value curriculum completion

| Candidate | Why | Visual opportunity |
|---|---|---|
| **Word Embeddings / word2vec** | direct CS50 Language gap; bridge from classical NLP to Transformer and future RAG | words occupy an embedding space; cosine neighbors and vector relations update visibly |
| **Grammar & Parsing** | direct CS50 Language gap | parse tree grows step by step; ambiguous sentences produce competing trees |
| **N-grams & Naive Bayes Text Classification** | fills classical language-model/text-classification gap | counts become probabilities; smoothing changes zero-probability behavior; evidence contributions accumulate |
| **First-Order Logic & Unification** | AIMA + CS50 Knowledge gap | substitutions make predicates match; quantified rules fire only when unification succeeds |
| **Regression / Margins / SVM** | fills a CS50 Learning gap and strengthens traditional ML | fit line/curve and margin move as points are dragged; support vectors become geometrically obvious |
| **Robotics Localization / Particle Filter** | major AIMA domain with exceptional visual potential | noisy particles collapse toward the robot's position as sensor evidence arrives |

## Tier C — useful but lower priority or more specialized

- Recurrent neural networks / sequence memory
- multiagent decision making and game theory beyond minimax
- probabilistic programming
- learning Bayesian-network parameters/structure
- richer knowledge representation / ontologies
- dedicated AI ethics/safety simulation

---

# D. Contemporary-extension track

The modern-extension roadmap remains valuable, but it should advance alongside the classical/core backlog instead of replacing it.

High-value contemporary candidates:

1. **Generative Images: Diffusion / Denoising / Guidance** — strongest immediate visual wow factor.
2. **Retrieval, Embeddings & RAG** — strongest practical connection to current LLM systems.
3. **Multimodal Image-Text Embeddings** — strong visual and conceptual bridge across vision and language.
4. Mixture-of-Experts routing — technically strong but narrower teaching audience.
5. Preference learning / DPO — valuable but easier to oversimplify.

Recommended expansion principle:

> Alternate or otherwise balance **classical curriculum completion** with **contemporary AI extensions**. Do not let all post-14 labs become frontier-system topics.

A provisional sequence, not yet frozen:

- Lab 15: Minimax & Alpha-Beta Game Trees
- Lab 16: Generative Images / Diffusion
- Lab 17: Constraint Satisfaction Problems
- Lab 18: Retrieval, Embeddings & RAG
- Lab 19: Markov / Hidden Markov Models & Viterbi
- Lab 20: Multimodal Image-Text Embeddings
- Lab 21: Classical Planning / Blocks World
- Lab 22: later candidate selected from the updated matrix

This ordering should be reconsidered after the v1.4 product-quality pass below; no Lab 15 implementation should begin merely because this provisional ordering exists.

---

# E. Required work before Lab 15 implementation

The next release should first strengthen the existing product and especially Labs 13 and 14. Treat this as a gate before opening implementation of another applet.

## 1. Lab 13 engagement-parity pass

Preserve the frozen Transformer arithmetic and semantic boundaries, but evaluate whether the learner experiences a sufficiently strong visual story compared with the best original applets. Candidate improvements include progressive token-to-representation-to-attention-to-logit highlighting, better focus management, and a more explicit visual causal journey rather than presenting many dense panels at once.

## 2. Lab 14 engagement-parity pass

Preserve its deterministic runtime, validation/authorization semantics, provenance, and security boundaries. Improve the visual story so a proposed action visibly moves through validation, authorization, execution, observation, context update, and stop/next-action selection. Rejection/denial should be visually obvious at the exact gate that blocks execution.

## 3. Suite-wide language-selector redesign

The current four-language button pattern is reaching its scaling limit. Evaluate and, if accepted, replace it consistently with an accessible native language `<select>` while preserving:

- EN / Simplified Chinese / Vietnamese / Spanish;
- `?lang=` deep links;
- keyboard and screen-reader behavior;
- locale switching without mutation of applet mathematical/mechanistic state;
- all current localization parity guarantees.

## 4. Version-visibility decision

Normalize how version provenance is exposed. The design question is not whether version information exists; it should remain available for citation, bug reporting, reproducibility, and release provenance. The UX question is **where** it appears.

Candidate default: remove/promote down hero-level version badges and retain a consistent, discoverable version in a footer/About/Info surface plus metadata. The final choice should be made during the v1.4 UX pass and then applied suite-wide rather than only to Labs 13 and 14.

## 5. Curriculum navigation redesign

Extend the existing AIMA-aligned curriculum concept into two complementary paths over one shared applet library:

- **Foundations / Course Track** — classical introductory AI sequence.
- **Modern AI Extensions** — Transformer, agent systems, future diffusion/RAG/multimodal labs.

The quick-entry showcase can remain a third navigation purpose optimized for demonstrations rather than course order.

## 6. Release boundary

Do not implement Lab 15 until the v1.4 product-quality scope is explicitly frozen. The coverage matrix is intended to improve future selection, not to create pressure to add applet count before the current suite is coherent.

---

# F. Current strategic conclusion

AI Playgrounds is already unusually strong across search, logic, Bayesian reasoning, introductory machine learning, deep learning, vision, reinforcement learning, Transformer mechanisms, and modern agent systems. Its largest weakness is now **coverage shape**, not applet count: several canonical classical-AI mechanisms remain absent while the newest additions have moved rapidly toward contemporary systems.

The strongest next curriculum targets are therefore **adversarial game search, constraint satisfaction, temporal probabilistic reasoning, planning, and MDP/value-iteration reasoning**. Contemporary work such as diffusion, RAG, and multimodal models should continue, but in deliberate balance with those classical gaps.

Before any new lab, v1.4 should prioritize product consistency and engagement parity for Labs 13 and 14, suite-wide language UX, normalized version provenance, and clearer separation between foundational course order and modern extensions.
