# AI Playgrounds Engagement and Immediate-Impact Acceptance Audit

Date: 2026-08-25

Status: candidate-design acceptance gate. Human engagement or learning gains are **not** claimed.

Baseline reviewed: released v1.4.0 commit `56ef84efa64de13a04d57d375f833d93d1cacf17`.

Accepted candidate head: `e3eaae0473142271682d8ea0a97192ca9984e1ea`.

Exact-head Verify evidence: run `32820222292`, job `97716565394`, PASS. The inherited suite, Lab 13 engagement candidate, Lab 14 engagement candidate, CNF/SAT DPLL-tree candidate, Bayesian posterior-delta candidate, v1.4 public integration regression, and final browser/responsive QA all passed on that exact head.

## 1. Decision rule

The audit applies the ten-dimension design rubric frozen in `docs/ENGAGEMENT_EXCELLENCE_FAS.md`:

1. first meaningful action;
2. agency;
3. causal continuity;
4. memorable transformation;
5. prediction coupling;
6. exploration depth;
7. replayability;
8. equivalent access;
9. responsive integrity;
10. mechanism-first visual impact.

An applet passes the internal design-excellence threshold when no dimension has a material unresolved weakness below the rubric's acceptable floor and when any proposed improvement survives the FAS semantic, accessibility, responsive, localization, and complexity gates.

This is deliberately different from claiming that engagement has been empirically measured as excellent. That requires human evidence.

## 2. External comparator conclusions

The web/product scan in the FAS found a consistent pattern across Transformer Explainer, CNN Explainer, GAN Lab, Diffusion Explainer, TensorFlow Playground, Teachable Machine, PhET, explorable-explanation systems, and modern agent debuggers:

- direct manipulation is valuable when it changes a real model variable;
- temporal animation is valuable when it preserves and reveals a genuine state transition;
- before/after comparison is valuable when it removes memory burden;
- learner-owned construction is valuable when the response space is meaningful;
- first contact should expose a substantive action with immediate feedback;
- visual spectacle that does not encode the mechanism is not a quality improvement.

The scan therefore does **not** support adding gamification, arbitrary animation, sound, badges, or additional controls to every applet.

## 3. Applet-by-applet decisions

| Applet | Decision | Why this is the highest-quality action |
|---|---|---|
| Pathfinding Visualizer | **NO CHANGE — design-excellence threshold already met** | The learner already manipulates the same grid and compares real frontier/expansion behavior with step/playback controls and a mechanism-specific featured race. More motion would duplicate the existing search animation rather than reveal a missing mechanism. |
| Hill Climbing and Simulated Annealing | **NO CHANGE — design-excellence threshold already met** | Same landscape/start-state comparison, temporal search paths, restart/temperature controls, and immediate local-versus-escaping behavior already provide agency and a memorable transformation. No mechanism-faithful missing view was found. |
| Wumpus World | **NO CHANGE — design-excellence threshold already met** | Hidden world versus agent knowledge, step/autoplay/scrub, reasoning log, per-cell explanation, scenarios, and teacher reveal/edit controls already make the key epistemic gap visible. Additional reveal effects would risk confusing ground truth with the simplified inference system, a v1.1 red-team boundary. |
| Bayes Rule Playground | **NO CHANGE — design-excellence threshold already met** | Direct base-rate/test sliders already update a population view, true/false-positive decomposition, probability tree, and repeated-update view immediately. The mechanism is already directly manipulable and visually consequential. |
| K-Nearest Neighbors | **NO CHANGE — design-excellence threshold already met** | The learner moves the query point, changes closeness/voting rules, sees exact selected neighbors, and predicts the set/class before reveal. A second animation layer would not expose a missing causal relation. |
| Overfitting Explorer | **NO CHANGE — design-excellence threshold already met** | Complexity, data/noise, fitted curve, and training-versus-validation behavior are already directly coupled. The visible turning point from better fit to worse validation performance is the mechanism-defining transformation. |
| Tiny Neural Network | **NO CHANGE — design-excellence threshold already met** | Training, representation controls, nonlinear activation, and the resulting prediction/representation change already expose the applet's central capacity-versus-optimization idea. No additional explanatory animation survived the complexity-benefit gate. |
| K-Means Clustering | **NO CHANGE — design-excellence threshold already met** | Initialization, assignment, centroid update, step/play controls, and alternate-start comparison already make the iterative mechanism visible. A second cluster-motion metaphor would duplicate the actual state evolution. |
| Convolution Playground | **NO CHANGE — design-excellence threshold already met** | Kernel manipulation, spatial sliding, literal multiply-and-sum inspection, and filter comparison already deliver immediate mechanism-first impact. It is one of the suite's natural visual ceiling cases. |
| Q-Learning Gridworld | **NO CHANGE — design-excellence threshold already met** | Trial-and-error episodes, value backups, policy evolution, exploration controls, and early-versus-trained comparison already create genuine temporal agency and visible learning. Decorative reward effects would add noise rather than explanation. |
| CNF and SAT Builder | **ACCEPT DPLL branch/prune tree** | The existing trace was correct but spatial search structure had to be reconstructed mentally. The new SVG tree is derived from the existing DPLL trace, so branch creation, propagation, contradiction, pruning, and sibling backtracking become one continuous visible object without adding a second solver. |
| Bayesian Network | **ACCEPT exact posterior before/after delta** | The graph and evidence controls were already strong, but learners had to remember the prior posterior while testing explaining away. The retained previous marker and exact percentage-point delta make the reversal visible. Generic probability-flow animation was rejected because it would imply an inference algorithm the applet is not running. |
| Transformer Language Modeling | **ACCEPT state continuity + deterministic continuation + comparison** | The frozen arithmetic was strong, but learners had to connect separate token/representation/attention/prediction panels mentally. The new state-derived journey, explicit argmax continuation, and exact baseline/current comparison add continuity and agency while remaining deterministic and offline. |
| Agent Tool Use and Context Protocols | **ACCEPT runtime packet + context delta + simulated-world sandbox** | The original runtime was technically strong but dashboard-like. A real recorded action packet now visibly stops or passes at actual gates; context deltas and isolated simulated side effects make execution consequences legible; learner-selected one-step calls add substantive agency without pretending to be model decisions. |

## 4. Accepted candidate evidence

### Transformer Language Modeling

The candidate gate verifies:

- unchanged frozen Transformer arithmetic;
- four-stage state-derived continuity;
- deterministic argmax continuation;
- presentation-only baseline saving;
- exact model-control comparison;
- model and comparison-state preservation across locale changes;
- EN/ZH/VI/ES presentation;
- reduced-motion equivalence;
- 390 px containment;
- no runtime network dependency.

### Agent Tool Use and Context Protocols

The candidate gate verifies:

- seven runtime gates derived from actual event records;
- successful execution reaches observation/context update;
- denied calls stop at authorization and remain side-effect free;
- isolated learner sandbox side effects cannot mutate the canonical scenario world;
- schema rejection and authorization rejection remain side-effect free;
- explicit simulated-world boundary;
- locale-state preservation;
- reduced-motion equivalence;
- 390 px containment;
- no runtime network dependency.

### CNF and SAT Builder

The candidate gate verifies:

- exactly one DPLL solver remains;
- the tree is a read-only presentation of the existing trace;
- a parser-valid adversarial UNSAT formula contains genuine branching, conflict, sibling backtracking, and terminal contradiction;
- stepping the existing DPLL transport grows the same visible tree;
- conflict appears as a pruned leaf;
- locale switching preserves trace/index state;
- reduced-motion and 390 px paths remain usable.

### Bayesian Network

The candidate gate verifies:

- exactly one exact-inference implementation remains;
- no fabricated initial baseline;
- both-call evidence raises the burglary posterior from the prior;
- adding earthquake evidence then produces the exact visible downward explaining-away delta;
- sampling modes suppress exact before/after comparison so Monte Carlo noise is not misrepresented as a model-state change;
- locale changes preserve probability/evidence/method state;
- reduced-motion and 390 px paths retain the numeric comparison.

## 5. FAS kill decisions

The following proposals were explicitly killed rather than forced into the suite:

- points, streaks, badges, leaderboards, confetti, or sound;
- decorative autoplay;
- generic probability animation along Bayesian-network arrows;
- invented model thoughts or hidden reasoning for the agent lab;
- live frontier-model/API dependencies solely to create spectacle;
- camera/microphone collection;
- a social/backend layer for engagement;
- redundant animation on already temporal applets;
- modifications to the ten no-change applets merely to make every row look equally changed.

These rejections are part of the quality result, not unfinished work.

## 6. Internal post-pass assessment

Under the explicit FAS rubric, all fourteen applets now meet the **design-level engagement/immediate-impact excellence threshold**: ten because their existing v1.4 mechanism interaction already had no material missing design dimension, and four because a specific mechanism-faithful deficiency now has a tested candidate remedy.

This statement is bounded to the design and deterministic/browser evidence. It does not establish that every student will find every topic equally engaging, nor does it establish a measured learning effect.

## 7. Release implication

The accepted set is minor-release scope rather than a patch:

- Lab 13 gains a new continuation/comparison interaction layer;
- Lab 14 gains a new isolated runtime sandbox and visible execution-state layer;
- CNF/SAT gains a new DPLL search-tree representation;
- Bayesian Network gains a new exact before/after posterior comparison.

The next public composition should therefore target **v1.5.0**, subject to a new integrated build, integrated browser gate, exact-head Verify PASS, squash merge, deployed-main verification, and immutable tag/release sequencing.