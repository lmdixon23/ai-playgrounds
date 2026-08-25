# AI Playgrounds Engagement Excellence Full Assurance Stack

Date: 2026-08-25

Status: implementation-planning gate. This document does not authorize Lab 15, a public release, or claims of measured learning/engagement gains.

Baseline: released `main` / v1.4.0 commit `56ef84efa64de13a04d57d375f833d93d1cacf17`.

## 1. Objective

Raise the learner-facing engagement and immediate visual impact of any AI Playgrounds lab that still has a material, mechanism-faithful opportunity to improve, while preserving the suite's strongest properties: deterministic inspectability, precise pedagogy, multilingual state preservation, accessibility, offline operation, and bounded claims.

The target is **design-level excellence**, not a claim that user engagement or learning has already been empirically proven excellent. Empirical claims require human evidence.

The governing constraint is deliberately asymmetric: a lab may remain below the internal engagement/wow ceiling if every remaining intervention is decorative, misleading, disproportionately complex, or too weakly evidenced. Do not add spectacle merely to equalize scores.

## 2. External design evidence reviewed

The scan focused on products and research systems where interaction is part of the explanation rather than decoration.

### Transformer Explainer

Georgia Tech / Polo Club of Data Science's Transformer Explainer is the strongest direct comparator for Lab 13. Its CHI work emphasizes a token-centric overview, continuous data flow, smooth animated transitions that preserve context, custom input and parameter manipulation, and linked guided learning. A controlled study with 90 participants reported significant advantages in understanding and engagement relative to comparison conditions.

Sources:
- https://arxiv.org/abs/2408.04619
- https://poloclub.github.io/transformer-explainer/
- https://www.cc.gatech.edu/news/explaining-transformers-visually

Transferable principle: **show one object/state changing continuously through the mechanism instead of asking the learner to mentally connect independent panels**.

Non-transferable choice: loading a large live pretrained model would weaken AI Playgrounds' deterministic, compact, offline evidence boundary and is rejected.

### CNN Explainer

CNN Explainer connects overview and detail with interactive animation, image manipulation, and on-demand exact computation. Its evaluation reports particularly strong responses to animation, view transitions, and input customization.

Sources:
- https://arxiv.org/abs/2004.15004
- https://poloclub.github.io/cnn-explainer/

Transferable principle: **animated transitions should encode the computation or state relationship itself**. Learner-owned input is useful when it stays inside the model's defined domain.

### GAN Lab

GAN Lab exposes training as a visible temporal process, supports play/slow-motion/manual stepping, and lets users manipulate the data distribution. Published usage analysis found substantial use of alternate distributions, animation, user-drawn inputs, and slow motion.

Sources:
- https://arxiv.org/abs/1809.01587
- https://poloclub.github.io/ganlab/

Transferable principle: **one-step control, replay, and direct construction create useful agency when the process genuinely evolves over time**.

### Diffusion Explainer

Diffusion Explainer uses linked overview/detail views, animation, and prompt/parameter manipulation to make a temporal generative mechanism inspectable. Its user study reported substantial learning improvements.

Source:
- https://arxiv.org/abs/2305.03509

Transferable principle: **make intermediate states visibly continuous and allow controlled comparisons of one changed variable**.

### TensorFlow Playground and Teachable Machine

TensorFlow Playground uses low-risk direct manipulation with immediate model feedback. Teachable Machine creates a strong gather -> train -> test loop around learner-owned examples.

Sources:
- https://playground.tensorflow.org/
- https://teachablemachine.withgoogle.com/

Transferable principle: **the learner should be able to cause a meaningful result quickly, not merely inspect a prepared dashboard**.

Non-transferable choice: camera/microphone collection or backend/model-service dependencies are unnecessary for this suite and are rejected.

### PhET

PhET's interaction guidance emphasizes intuitive direct controls, immediate feedback, making invisible mechanisms visible, limited startup complexity, and purposeful challenge. Sliders and draggable objects are generally preferred over requiring numeric entry when direct manipulation better expresses the causal variable.

Sources:
- https://phet.colorado.edu/en/research
- https://phet.colorado.edu/en/teaching-resources/tipsForUsingPhet

Transferable principle: **first contact should expose a clear meaningful action and its consequence without requiring the learner to read a dashboard manual**.

### Explorable Explanations / Nicky Case

The explorable-explanations pattern argues for a hook first, then learning by doing, showing, and telling; animation should explain temporal relations and interaction should expose systems and models.

Source:
- https://explorabl.es/

Transferable principle: **the first move should be the mechanism's hook, not administrative UI**.

### Desmos and Brilliant

Desmos' activity patterns and Brilliant's interactive lessons emphasize direct manipulation, challenge, prediction, immediate feedback, and learner construction. Creation is valuable when the space of responses has meaningful variation; shallow gamification is not a substitute.

Sources:
- https://www.desmos.com/
- https://teacher.desmos.com/
- https://brilliant.org/

Transferable principle: **prediction should be connected to the same active visual state that resolves it**.

### LangSmith Studio / modern agent debuggers

Modern agent-development interfaces expose step-by-step tool calls, results, intermediate state, graph structure, checkpoints, and replay/fork workflows.

Sources:
- https://docs.langchain.com/langsmith/studio
- https://docs.langchain.com/langgraph-platform/langgraph-studio

Transferable principle for Lab 14: **agent execution becomes legible when action, gate, result, state delta, and next action are visibly connected**.

## 3. Internal excellence rubric

Each candidate experience is scored from 1 to 5 on the dimensions below. A design may be called **internally excellent** only when no dimension is below 4 and the pedagogical/integrity gates remain excellent.

1. **First meaningful action** — a first-time learner can identify a useful action quickly, with a target of about 10 seconds or less and little prerequisite reading.
2. **Agency** — the learner directly manipulates a real model variable, chooses a real step, or constructs a legitimate input.
3. **Causal continuity** — the visual consequence is immediate and spatially/temporally connected to the action that caused it.
4. **Memorable transformation** — at least one concept-defining change or comparison is visible without hunting through secondary panels.
5. **Prediction coupling** — prediction-before-reveal resolves in the same active visual state rather than only in prose feedback.
6. **Exploration depth** — free exploration and guided use coexist without either becoming clutter.
7. **Replayability** — reset/replay/share behavior is unambiguous and deterministic where the mechanism permits it.
8. **Equivalent access** — reduced-motion and text/keyboard paths preserve the essential instructional relation.
9. **Responsive integrity** — the essential interaction survives keyboard-only operation and a 390 px viewport.
10. **Mechanism-first wow** — visual impact comes from seeing the mechanism work, not confetti, sound, arbitrary motion, badges, or points.

## 4. Current suite assessment

The original twelve applets already received a substantial product/red-team pass. Several already contain the interaction patterns the external scan recommends: direct manipulation, transport controls, one-step playback, scenario galleries, signature comparisons, responsive layouts, and accessible text state.

### No forced intervention group

The current evidence does not justify adding new mechanics solely for spectacle to:

- Pathfinding Visualizer
- Hill Climbing and Simulated Annealing
- Wumpus World
- Bayes Rule Playground
- K-Nearest Neighbors
- Overfitting Explorer
- Tiny Neural Network
- K-Means Clustering
- Convolution Playground
- Q-Learning Gridworld

These remain subject to a first-10-second audit, but a failed audit is required before adding another layer. Their existing interactions are already close to the appropriate ceiling for their mechanisms.

### Material intervention candidates

**CNF and SAT Builder.** DPLL is currently a high-quality stepped trace with assignments, actions, and working clauses. A spatial branch/prune tree is absent. A tree can make the core search insight visible without changing solver semantics: branching creates alternatives, propagation collapses them, and contradiction prunes a branch.

**Bayesian Network.** The existing draggable graph, evidence controls, multiple inference methods, and explaining-away scenarios are strong. The only intervention with a plausible net gain is a **posterior delta comparison**: preserve the previous posterior as a ghost/baseline and show the exact increase/decrease after new evidence. Do not animate probability as though it literally flows along graph arrows unless the applet is actually executing such a message-passing algorithm.

**Transformer Language Modeling.** v1.4 improved navigation through the existing panels, but the learner still has to connect token, representation, attention, and prediction mentally. The evidence supports three mechanism-faithful additions: a state-derived flow pulse, deterministic one-token continuation, and a baseline-versus-current comparison.

**Agent Tool Use and Context Protocols.** v1.4 made gate stages legible, but the experience remains dashboard-like. The strongest improvements are a visible action packet moving through actual runtime gates, an observation/context delta, an explicitly simulated in-memory world, and a learner-controlled one-step runtime sandbox.

## 5. Full Assurance Stack

### 5.1 Red Team

Primary failure modes:

- decorative animation that does not encode a real state relation;
- motion that implies a false mechanism, especially fake probability flow in Bayesian networks;
- engagement features that displace prediction-before-reveal;
- a simulated Lab 14 side effect being mistaken for a real mail/calendar/network action;
- learner-selected sandbox actions being mistaken for model-selected actions;
- animation lagging behind or diverging from deterministic state;
- reduced-motion users losing essential causal information;
- localization overflow or state loss;
- mobile controls obscuring the result;
- rapid click/reset/locale-switch races;
- importing large pretrained models, external APIs, or telemetry solely to create spectacle.

### 5.2 Blue Team

Strongest opportunities:

- preserve a visible object or state across stages;
- give the learner a meaningful first move;
- connect action and consequence spatially;
- show before/after deltas instead of requiring memory;
- expose one-step/replay controls for temporal mechanisms;
- let the learner construct valid inputs where the deterministic model supports them;
- keep challenge predictions tied to the exact state that resolves the prediction.

### 5.3 Arbiter

Accepted for prototyping:

1. Lab 13 state-derived flow animation/highlight.
2. Lab 13 deterministic `Append argmax token`; seeded sampling only if exact replay obtains an independent fixture and parity test.
3. Lab 13 baseline/current comparison.
4. Lab 14 state-derived action packet.
5. Lab 14 context before/after delta.
6. Lab 14 explicit `SIMULATED WORLD — no real external action` surface.
7. Lab 14 learner runtime sandbox, clearly separated from the deterministic policy.
8. CNF/SAT DPLL branch/prune tree derived from the existing trace.
9. Bayesian Network posterior delta visualization, retained only if it improves explaining-away legibility without suggesting a false inference algorithm.
10. First-move refinements only where audit evidence shows genuine startup friction.

Rejected:

- points, streaks, leaderboards, confetti, sound, or badges for spectacle;
- autoplay that makes substantive choices before the learner acts;
- live frontier-model APIs or a large pretrained model download;
- camera/microphone input;
- generic animated probability flow on Bayesian-network arrows;
- a social/backend layer solely for engagement;
- visualization of invented agent thoughts or hidden reasoning;
- changes to Labs 1–12 where the only argument is score equalization.

### 5.4 FMEA

| Failure mode | Severity | Prevention | Required evidence |
|---|---|---|---|
| Visual implies a false mechanism | Critical | Render only documented state transitions; reject metaphor if ambiguous | semantic assertions + adversarial review |
| Engagement layer mutates frozen model/runtime state | Critical | presentation wrapper over existing state; snapshot invariants | before/after state equality tests |
| Rejected/denied tool appears to cause a side effect | Critical | simulated-world mutation only from executed successful event | invalid/permission negative tests |
| Animation continues after reset/state replacement | High | state/run IDs and cancellable renderer | rapid reset/double-action browser tests |
| Reduced-motion mode loses information | High | replace motion with ordered visible state changes and text | reduced-motion browser test |
| Locale switch loses state or desynchronizes animation | High | presentation-only locale change; re-render from canonical state | all four locale invariants |
| 390 px view hides the active causal relation | High | responsive stacking with current action/result kept adjacent | 390 px browser audit |
| Added code breaks offline/single-file boundary | High | no runtime network/dependency | static network-token checks + offline load |
| Seeded generation is not exactly replayable | High | frozen PRNG, seed in state, independent parity fixture | Python/JS/browser replay tests |

### 5.5 Fault Tree Analysis

Top event: **the engagement pass makes AI Playgrounds less trustworthy**.

Major branches:

- false visual metaphor;
- hidden state mutation;
- accessibility/state-equivalence regression;
- real-world side-effect confusion;
- nondeterministic replay;
- complexity that obscures the original mechanism.

The release gate fails if any branch remains plausible without a tested control.

### 5.6 STPA

Unsafe control actions to prohibit:

- advancing the Lab 14 visual packet beyond a gate without the corresponding runtime event;
- showing context update before an observation exists;
- mutating simulated world after a rejected or denied action;
- appending a Lab 13 token without an explicit selection rule;
- replaying or forking from a stale snapshot;
- allowing locale/UI state to become a second source of truth for machine state.

Controls:

- derive presentation from canonical event/state IDs;
- cancel/rebuild transient presentation on reset or state replacement;
- keep simulation/provenance labels persistent;
- expose deterministic selection rule and seed where applicable;
- retain complete text state.

### 5.7 Bowtie

Threats: fast repeated input, reset mid-transition, locale change mid-transition, malformed custom input, denied tool call, execution error, untrusted tool content, reduced-motion preference, narrow viewport.

Preventive barriers: schema/state checks, event IDs, render-only wrappers, explicit action types, immutable snapshots, reduced-motion branch, responsive layout constraints.

Recovery barriers: deterministic reset/replay, complete text state, visible provenance, animation cancellation, invariant assertions, and zero real backend side effects.

## 6. Boundary and negative tests

Any accepted implementation must exercise at least:

- reduced-motion rendering;
- keyboard-only operation;
- 390 px mobile width;
- locale switch before/after/in the middle of a transient visual transition;
- reset during a transient transition;
- rapid repeated clicks;
- Lab 13 unknown token and maximum context cases;
- Lab 13 deterministic argmax tie behavior;
- seeded sampling replay if sampling is added;
- Lab 14 invalid arguments, unavailable tool, unauthorized tool, execution error, instruction-like untrusted observation, and correct termination;
- Lab 14 sandbox action/principal changes;
- simulated world unchanged after rejection/denial;
- one-file/offline operation and no runtime network request.

## 7. Claim-to-evidence boundary

Allowed after deterministic/browser verification:

- the feature visually links specific existing model/runtime states;
- the feature preserves frozen arithmetic/runtime semantics;
- the interaction is deterministic/replayable under its documented rule;
- all required responsive, localization, reduced-motion, and negative tests pass.

Not allowed without human evidence:

- learners understand better;
- engagement is objectively excellent;
- the feature improves retention;
- the feature is more accessible in practice;
- teachers or students prefer the new design.

A later small usability/think-aloud or classroom pilot can test those claims.

## 8. Phased implementation gate

### R0 — assurance and architecture freeze

- freeze this FAS;
- preserve exact v1.4.0 baseline;
- no public behavior yet.

### R1 — Lab 13 flow prototype

- add state-derived token -> representation -> attention -> prediction continuity;
- add reduced-motion equivalent;
- prove model state is unchanged.

### R2 — Lab 13 agency/compare

- add deterministic one-token `argmax` continuation;
- add baseline/current comparison;
- add seeded sampling only if an independent deterministic parity contract is first frozen.

### R3 — Lab 14 runtime-object prototype

- add action packet derived from the real selected action/event;
- add context delta;
- add explicit simulated-world state and negative side-effect checks.

### R4 — Lab 14 learner sandbox

- allow learner-selected principal/tool/valid argument combinations for one deterministic runtime step;
- visually distinguish learner choice from deterministic policy choice;
- preserve all original eight scenarios and five Guided Challenges.

### R5 — targeted original-lab prototypes

- add CNF/SAT DPLL branch/prune tree;
- prototype Bayesian posterior delta comparison;
- kill the Bayesian prototype if it creates misleading flow semantics or weakens clarity.

### R6 — suite first-move audit

- score all fourteen applets against the excellence rubric;
- modify no lab without an identified weak dimension and a mechanism-faithful remedy;
- keep already-strong labs unchanged when marginal gain is not credible.

### R7 — exact-head candidate

- run inherited v1.4 gates plus new engagement/state/negative tests;
- require zero page/console errors;
- require desktop, keyboard, reduced-motion, and 390 px evidence;
- do not call the release empirically more engaging without human evidence.

## 9. Expansion and kill conditions

Expand an intervention only when:

- it makes a real model/runtime relation easier to perceive;
- the learner can manipulate or predict something substantive;
- state semantics remain exact;
- the new code remains proportionate to the learning gain.

Kill or revert it when:

- a reviewer can reasonably infer the wrong mechanism from the visual;
- the same learning goal is already achieved more clearly by the existing applet;
- reduced-motion/text equivalence becomes materially weaker;
- it adds state or race complexity without a correspondingly strong learning interaction;
- it is primarily aesthetic rather than explanatory.

## 10. Release-number decision

Do not freeze the next release number at R0. If the accepted work ultimately includes the Lab 13 generation/compare layer, Lab 14 sandbox/simulated-world layer, and one or more substantive original-lab visual mechanisms, it is minor-release scope. If most prototypes are killed and only small presentation fixes survive, use a patch release instead.

Lab 15 remains blocked until this pass is either completed or explicitly terminated.