# AI Playgrounds v1.9 human validation protocol

Status: operational formative product-validation protocol for issue #50.

This protocol supersedes the planning-only v1.5 human-engagement protocol for current product decisions. It preserves the useful earlier measures while expanding the scope to the complete fifteen-lab, four-locale, all-Quick-Assign product.

## 1. Purpose

The deterministic assurance stack can establish bounded software properties such as exact algorithm output, state preservation, release reproducibility, responsive containment, localization parity, and browser behavior. It cannot establish that a first-time learner notices the intended interaction, forms the intended mental model, or that an educator can adopt the resource without developer assistance.

v1.9 therefore requires human evidence before consequential visible redesign decisions are accepted.

The protocol separates four questions:

1. learner first-use usability and mechanism comprehension;
2. educator adoption and classroom-flow usability;
3. human translation naturalness and technical-semantic fidelity;
4. accessibility usability under representative human interaction conditions.

These are product-validation questions. They are not an efficacy trial and do not support population-level learning-gain claims.

## 2. Version binding

Every observation cycle must record:

- exact Git commit;
- public release or candidate version;
- browser and operating system;
- viewport/device class;
- active locale;
- input method;
- theme when relevant;
- accessibility condition when relevant.

The initial pre-redesign cycle may use exact v1.8.1 baseline `d1c72e10e6c5bf64b9a4bbed578b2305d1c988d0` or a byte-identical canonical-source candidate produced under #47.

A post-redesign validation cycle must use the exact v1.9 release-candidate SHA.

## 3. Evidence cycles

### Cycle A — baseline diagnosis

Use the current product before visible v1.9 redesign.

Purpose:

- find actual first-use friction;
- find repeated false mental models;
- test the current homepage-to-lab and homepage-to-teaching flows;
- identify translation-naturalness defects;
- establish bounded descriptive baseline metrics.

### Cycle B — targeted correction checks

After an accepted defect is corrected:

- reproduce the original condition;
- rerun deterministic/browser verification;
- repeat the affected human task with at least two fresh users when the original trigger was repeated across users;
- do not close a P0/P1 human finding from implementation inspection alone.

### Cycle C — release-candidate validation

Use a fresh sample after the visible v1.9 redesign stabilizes.

Do not reuse Cycle A participants for primary first-use measures because prior exposure would contaminate discovery and first-action evidence.

Cycle C should repeat the same core task definitions so bounded before/after descriptive comparison remains possible.

## 4. Learner sample

Cycle A target: 12 first-time learners in the intended secondary-school to early-undergraduate range.

Cycle C target: 12 fresh first-time learners.

Each learner receives five lab tasks. The schedule below creates 60 learner-lab observations per cycle and gives every public lab exactly four independent observations.

No learner should receive an explanatory tour before the first-action measure begins.

## 5. Balanced learner allocation

The schedule is a balanced incomplete coverage design for product testing, not a randomized efficacy design.

| Participant | Task 1 | Task 2 | Task 3 | Task 4 | Task 5 |
| --- | --- | --- | --- | --- | --- |
| P01 | Bayes Rule | Tiny Neural Network | Transformer | Wumpus World | KNN |
| P02 | Tiny Neural Network | Transformer | Wumpus World | KNN | Convolution |
| P03 | Transformer | Wumpus World | KNN | Convolution | Agent Tool Use |
| P04 | Wumpus World | KNN | Convolution | Agent Tool Use | Hill Climbing |
| P05 | Convolution | Agent Tool Use | Hill Climbing | Bayesian Network | K-Means |
| P06 | Agent Tool Use | Hill Climbing | Bayesian Network | K-Means | Minimax |
| P07 | Hill Climbing | Bayesian Network | K-Means | Minimax | CNF/SAT |
| P08 | Bayesian Network | K-Means | Minimax | CNF/SAT | Overfitting |
| P09 | Minimax | CNF/SAT | Overfitting | Q-Learning | Pathfinding |
| P10 | CNF/SAT | Overfitting | Q-Learning | Pathfinding | Bayes Rule |
| P11 | Overfitting | Q-Learning | Pathfinding | Bayes Rule | Tiny Neural Network |
| P12 | Q-Learning | Pathfinding | Bayes Rule | Tiny Neural Network | Transformer |

Properties of this schedule:

- every lab appears exactly four times;
- no lab is systematically always first or last;
- Foundations and Modern AI mechanisms are mixed across participants;
- each participant sees multiple mechanism types rather than five near-identical tasks.

For Cycle C, keep the same incidence structure but rotate participant labels or task order within blocks so position effects are not duplicated mechanically.

## 6. Learner facilitator procedure

For each lab:

1. Navigate directly to the assigned lab in the intended default learner state.
2. Do not point out controls or explain page organization.
3. Start the first-action timer when the interactive surface is usable.
4. Ask the learner to describe what the page appears to let them investigate and show what they would try first.
5. Stop the first-action timer at the first substantive mechanism-relevant action.
6. If the learner is blocked, wait for the predeclared recovery threshold before giving a neutral prompt.
7. After the first substantive state change, ask what changed and what in the applet caused it.
8. Run one prediction-before-reveal scenario or Quick Assign prediction step.
9. Ask the learner to test one changed case that they expect to behave differently.
10. Ask what they would try next with two additional minutes.
11. Record false mental models before correction.
12. Record interface hesitation separately from conceptual difficulty.

Facilitators should use neutral acknowledgements and avoid praising or steering a particular answer while the task is active.

## 7. Learner measures

### 7.1 Time to first meaningful action

Start: interactive area is usable.

Stop: learner changes a substantive variable, selects a meaningful scenario, or executes a legitimate mechanism step.

Record seconds and whether facilitator prompting was required.

This is a friction diagnostic rather than a speed contest.

### 7.2 First-action class

Code as one of:

- mechanism-relevant;
- administrative but harmless;
- unrelated exploration;
- blocked by interface confusion.

### 7.3 Prediction integrity

Record whether the learner:

- commits a prediction before reveal;
- attempts to inspect the answer/result first;
- changes a prediction only before commitment;
- can explain the discrepancy after reveal.

### 7.4 Mechanism explanation score

Use a 0–3 scale against applet-specific mechanism anchors.

- 0: explanation contradicts the mechanism or asserts a severe false model;
- 1: describes the visible result without the mechanism;
- 2: identifies the relevant mechanism with a material omission;
- 3: correctly connects learner action, intermediate relation, and result.

Do not score writing style, vocabulary sophistication, or prior subject knowledge beyond what the task requires.

### 7.5 Transfer task

Record whether the learner can choose or create a changed case and state a mechanism-relevant reason for expecting different behavior.

Code:

- independent successful transfer;
- successful after neutral prompt;
- changed case selected without mechanism rationale;
- blocked.

### 7.6 Voluntary exploration

After required work, record whether the learner voluntarily:

- replays;
- changes a variable;
- opens another scenario;
- creates custom input;
- inspects explanation/state text;
- stops immediately.

Treat this as bounded behavioral evidence, not a universal motivation measure.

### 7.7 False-mental-model log

For every material misconception record:

- exact interpretation;
- likely interface surface;
- mechanism involved;
- severity;
- whether the cause appears to be copy, visualization, control ordering, task design, translation, or prior conceptual knowledge;
- whether the same pattern has appeared independently before.

## 8. Learner internal product targets

These are release-quality targets, not research claims.

For each lab with four baseline observations, review rather than automatically fail on a small sample when uncertainty is high. Across the suite, the desired pattern is:

- at least 80 percent mechanism-relevant first actions without facilitator prompting;
- suite median first meaningful action at or below 20 seconds;
- at least 75 percent mechanism-explanation scores of 2 or 3 after one guided state change;
- no repeated P0/P1 false mental model attributable to the same product surface;
- prediction-before-reveal not routinely bypassed by visible answers or UI ordering;
- transfer task possible without the facilitator teaching the mechanism.

A lab can still be reopened when a severe repeated defect is clear even if aggregate suite metrics remain strong.

## 9. Applet-specific mechanism anchors

### Pathfinding

Learner should connect algorithm choice and heuristic information to frontier expansion, explored states, path discovery, and path cost rather than equating fewer explored cells with guaranteed better path cost.

### Hill Climbing and Simulated Annealing

Learner should distinguish local move choice, local optimum, randomness/temperature, restart reliability, and solution cost. Repeated-restart success frequency must not be interpreted as a universal algorithm ranking independent of problem distribution.

### Wumpus World

Learner should distinguish percept from inferred world state and understand that local sensory evidence constrains rather than reveals the complete hidden world.

### CNF/SAT

Learner should distinguish decisions, propagation, conflicts, branch pruning, and, in CDCL mode, learned-clause validity and non-chronological backjumping. A conflict leaf must not be read as proving unrelated sibling branches impossible.

### Bayes Rule

Learner should identify prior, likelihood/evidence relation, and posterior update without treating posterior probability as a simple renamed likelihood.

### Bayesian Network

Learner should understand conditional dependence/evidence update without treating probability as physically flowing along graph arrows. Previous/current markers must not be interpreted as two different inference algorithms.

### KNN

Learner should identify neighbor selection and distinguish classification voting from regression averaging. Distance weighting and feature scaling should be understood as changing influence or geometry rather than changing the identity of the underlying method.

### Overfitting

Learner should connect model complexity and regularization to train/test behavior rather than treating training fit alone as model quality.

### Tiny Neural Network

Learner should connect inputs, hidden representation/nonlinearity, outputs, parameter updates, and error behavior without inferring that node animation is an explanation of human-like reasoning.

### K-Means

Learner should distinguish assignment and centroid-update steps and understand convergence as stable assignments/centers under the algorithm rather than proof of the uniquely correct clustering.

### Convolution

Learner should connect local input patch, kernel weights, multiply-and-sum operation, output location, and feature response. Highlighted cells must preserve spatial correspondence.

### Q-Learning

Learner should connect state, action, reward/transition, temporal-difference update, Q-values, and policy behavior without reading the current learned policy as guaranteed optimal before sufficient learning.

### Transformer Language Modeling

Learner should connect token/position representation, Q/K/V attention computation, causal masking, logits/probabilities, and decoding. Attention must not be interpreted as a general explanation of reasoning. Deterministic argmax continuation must not be mistaken for ordinary stochastic generation.

### Agent Tool Use and Context Protocols

Learner should distinguish available, schema-valid, authorized, executed, observed, context-updated, and stopped states. Simulated actions must not be mistaken for real side effects, and learner-selected sandbox actions must remain distinct from model-selected actions.

### Minimax and Alpha-Beta

Learner should distinguish alternating MAX/MIN backups, terminal utilities, root decision, evaluated versus pruned nodes, and the fact that alpha-beta preserves the exact minimax result for a fixed tree while changing search work with move order.

## 10. Educator sample

Cycle A target: 6 educators who did not participate in product development.

Cycle C target: 6 fresh educators when feasible.

Prefer a mix of secondary CS/AI teachers, mathematically adjacent STEM teachers, and introductory higher-education instructors. Prior AI-specialist expertise is not required for every participant because the product must communicate its teaching boundary to ordinary instructors as well as specialists.

## 11. Educator task sequence

Each educator completes the following without a developer walkthrough.

### Task E1 — identify a usable lesson

From the public homepage, select a lab appropriate to a supplied teaching need.

Record:

- time to first credible choice;
- whether the educator uses Learn, Teach, search/filter, or catalogue scanning;
- uncertainty about level, prerequisite, duration, or objective;
- whether they choose an inappropriate lab because discovery copy is ambiguous.

### Task E2 — locate and understand the Quick Assign

Ask the educator to prepare a 10–15 minute use of the selected lab.

Record:

- time to find the canonical Quick Assign;
- whether the learning objective is inferable;
- whether predict → manipulate → observe → explain → transfer is understood;
- whether the educator can distinguish student-facing from teacher-facing material;
- any need for developer explanation.

### Task E3 — classroom sharing

Ask the educator to create the form they would actually give students.

Exercise:

- canonical classroom/deep link;
- share behavior;
- print/copy packet;
- reset/recovery;
- locale choice where relevant.

### Task E4 — offline use

Ask the educator to identify how they would use the lab in a restricted-network classroom.

Record whether the offline/self-contained model is discoverable and understandable.

### Task E5 — fidelity boundary

Ask what the visualization demonstrates and what it simplifies.

This checks whether teacher notes and fidelity disclosures prevent overclaiming the pedagogical model.

### Task E6 — reuse judgment

Ask:

- whether they would use the resource;
- in what lesson context;
- what preparation they still need;
- which missing affordance would materially block classroom use;
- which requested feature would merely be convenient rather than necessary.

## 12. Educator measures

Record:

- homepage-to-credible-lesson seconds;
- homepage-to-Quick-Assign seconds;
- preparation minutes before educator states they could teach the activity;
- developer intervention required yes/no;
- objective clarity 0–3;
- prerequisite clarity 0–3;
- fidelity-boundary understanding 0–3;
- successful canonical link/share task yes/no;
- successful print/copy task yes/no;
- successful reset/recovery task yes/no;
- offline-use understanding yes/no;
- intended reuse yes/no/uncertain;
- blocker severity;
- missing-affordance category;
- verbatim rationale.

## 13. Educator internal product targets

Desired release pattern:

- at least 80 percent reach a credible teachable activity without developer guidance;
- at least 80 percent find the Quick Assign and understand its sequence without developer guidance;
- median preparation time for a Level 1 activity at or below five minutes after opening the selected lab;
- at least 80 percent complete canonical sharing and packet print/copy tasks;
- no repeated P0/P1 misunderstanding of what the model demonstrates or where learner responses are stored;
- no repeated classroom blocker caused by navigation, reset, sharing, or offline-use ambiguity.

These targets guide product iteration and do not imply external adoption rates.

## 14. Human locale validation

Machine parity remains necessary but is not the acceptance authority for natural language.

For each of ZH, VI, and ES:

- use two independent fluent reviewers;
- where feasible, use one reviewer comfortable with technical/educational terminology and one reviewer closer to the intended learner audience;
- each reviewer performs an active state-change task in all fifteen labs;
- each reviewer inspects scenario instructions, controls, dynamic state text, key terms, Quick Assign prompts, mechanism explanation headings, and fidelity wording.

This yields two human naturalness observations per lab per non-English locale.

Record:

- technical-term accuracy;
- naturalness;
- label brevity and scanability;
- dynamic grammar;
- ambiguity;
- altered mathematical/causal/epistemic strength;
- truncation or wrapping that changes usability;
- preferred replacement wording when a defect exists.

Do not reward literal translation when a more natural phrase preserves the same contract.

Any wording that changes a mechanism claim is a correctness defect, not a style preference.

## 15. Accessibility human subround

Coordinate with #49 rather than duplicating the formal accessibility audit.

Human product validation should include at minimum:

- keyboard-only task completion on representative labs from each major mechanism family;
- 200 percent browser zoom;
- 390 px-class phone viewport;
- reduced-motion preference;
- one representative desktop screen-reader workflow with an experienced screen-reader user when feasible.

The acceptance question is whether the concept-defining instructional relation remains recoverable, not merely whether every control receives focus.

## 16. Finding taxonomy

Every finding receives exactly one primary class:

- mechanism correctness;
- false mental model;
- discovery/navigation;
- control affordance;
- visual hierarchy;
- state interpretation;
- assignment/teacher flow;
- recovery/reset;
- localization semantics;
- localization naturalness;
- accessibility;
- responsive layout;
- performance/responsiveness;
- documentation/fidelity;
- preference/no product defect.

Secondary tags may be added, but one primary owner prevents findings from disappearing between workstreams.

## 17. Severity

### P0

The product gives materially wrong mechanism feedback, transmits prohibited learner data, loses required learner work without recovery, changes mathematical/causal meaning by locale, or creates another release-blocking correctness/privacy defect.

### P1

The same product surface causes a severe false mental model, blocks core task completion for multiple independent users, makes the concept-defining relation unavailable under a supported interaction mode, or prevents educators from using the canonical classroom flow.

### P2

Material friction or ambiguity that does not block the core relation but reasonably reduces successful first use.

### P3

Cosmetic preference, isolated wording polish, or convenience improvement without demonstrated task impact.

## 18. Automatic reopen rules

Reopen the relevant design when any of the following occurs:

- any P0 finding;
- two or more independent users form the same P1 false mental model from the same surface;
- a majority of observations for a lab cannot identify a meaningful first action without prompting;
- prediction-before-reveal is routinely bypassed because the answer is visible elsewhere;
- keyboard, reduced motion, zoom, phone, or screen-reader use removes the concept-defining relation;
- locale wording changes a mathematical, causal, or epistemic claim;
- two or more educators cannot find or understand the canonical Quick Assign flow for the same reason;
- an interaction attracts attention but users cannot connect it to the mechanism.

Do not redesign solely because one participant dislikes a topic, prefers a different aesthetic, or requests decorative spectacle unsupported by the mechanism.

## 19. Change procedure

For each accepted human finding:

1. bind it to exact product SHA and condition;
2. classify primary owner and severity;
3. reproduce the interface condition;
4. distinguish interface defect from conceptual difficulty and prior knowledge;
5. identify the smallest mechanism-faithful correction;
6. add deterministic/browser regression where automation can represent the invariant;
7. run the complete current Verify gate;
8. rerun the affected human task with fresh users;
9. update the finding status with evidence rather than implementation intent.

## 20. Release decision

v1.9 should not ship with:

- any unresolved P0 human finding;
- any unresolved repeated P1 false mental model attributable to the product;
- an unresolved core educator-flow blocker repeated across participants;
- a non-English locale defect that changes the mechanism claim;
- a supported accessibility condition that removes the concept-defining relation.

P2/P3 findings may remain only when explicitly triaged with rationale and no interaction with a release-critical invariant.

## 21. Reporting boundary

Permissible bounded reporting includes:

- observed median time to first meaningful action;
- task completion without facilitator prompting;
- mechanism-explanation score distribution in the observed sample;
- recurring false-model categories;
- educator preparation time in the observed sample;
- human locale defects found and corrected;
- accessibility barriers found under tested conditions;
- descriptive before/after changes between Cycle A and fresh Cycle C samples.

Do not describe these formative product observations as proof of learning effectiveness. A claim of improved learning requires a separate comparison design with an appropriate outcome measure and inference plan.

## 22. Data minimization

The product itself must not collect participant responses for this study.

Use anonymous IDs such as P01–P12 and E01–E06. Store only the context required to interpret the product finding. Do not place student names, email addresses, school identifiers, grades, or private screenshots into public GitHub evidence.

If the observations are later used for formal publication rather than internal product improvement, review the applicable institutional research and consent requirements before extending the claim boundary.
