# AI Playgrounds Human Engagement and Usability Validation Protocol

Date: 2026-08-25

Status: future evidence protocol. No participant results have been collected under this protocol yet.

## 1. Purpose

The deterministic/browser assurance stack can prove that an interaction exists, uses the intended state, preserves invariants, fits supported viewports, and behaves consistently across tested locales. It cannot prove that a first-time learner notices the intended relation, understands it, enjoys the interaction, or prefers it to the previous design.

This protocol defines the smallest credible human-evidence layer for those questions without turning product iteration into an oversized research study.

## 2. Primary questions

For each applet tested:

1. Can a first-time learner identify a meaningful first action without being told where to click?
2. Does the learner predict an outcome before revealing it when the task asks for a prediction?
3. After one meaningful state change, can the learner describe the mechanism that caused the visible result?
4. Does the visual create a false mental model that is not present in the applet's formal explanation?
5. Does the learner voluntarily replay, alter, or compare another case after the first result?
6. Can the same essential relation be recovered with keyboard-only operation, reduced motion, and a narrow viewport?
7. Does switching language preserve task state and comprehension of the active mechanism for fluent speakers of that locale?

## 3. Suggested pilot structure

### Round A — think-aloud usability

Target: 5–8 first-time participants spanning the intended secondary-school / early-undergraduate range.

Per participant:

- test 3–5 applets, rotated so no applet is systematically disadvantaged by fatigue;
- begin on the applet without an explanatory walkthrough;
- ask the participant to say what they think the page is for and what they would try first;
- do not point to a control unless the participant is genuinely stuck;
- after the first result, ask what changed and why;
- use one prediction-before-reveal prompt;
- ask the participant to create or test one altered case;
- record misconceptions verbatim before correcting them.

### Round B — classroom observation

Target: one normal class use of the relevant topic rather than a special demo session.

Record only aggregate/non-identifying observations needed for product design unless a separate approved research protocol says otherwise.

Observe:

- how many learners begin the intended interaction without teacher intervention;
- common points of hesitation;
- whether learners manipulate variables beyond the teacher's first example;
- whether prediction is made before reveal;
- recurring wrong explanations;
- whether the instructor has to translate interface structure into instructions that should have been obvious from the page.

## 4. Core measures

### Time to first meaningful action

Start: applet interactive area is usable.

Stop: participant performs an action that changes a substantive model/runtime variable or executes a legitimate step.

Record seconds plus whether prompting was required.

This is not a race metric. It is a diagnostic for startup friction.

### First-action correctness

Classify the first action as:

- mechanism-relevant;
- harmless but administrative;
- unrelated/exploratory;
- blocked by interface confusion.

### Prediction integrity

Record whether the participant:

- commits before reveal;
- edits only before locking;
- attempts to inspect/reveal the result first;
- can explain the discrepancy after compare.

### Mechanism explanation

After one state change, ask a neutral question such as:

`What changed, and what in the applet caused it?`

Score only against applet-specific mechanism anchors, not writing quality.

Recommended coding:

- 0 — explanation contradicts the mechanism;
- 1 — describes the visible result but not the mechanism;
- 2 — identifies the relevant mechanism with a material omission;
- 3 — correctly connects the action, intermediate relation, and result.

### False-mental-model log

For every repeated misconception, record:

- exact learner interpretation;
- interface surface that plausibly suggested it;
- severity under the v1.1 P0/P1/P2 pedagogical scheme;
- whether the problem is copy, visualization, control ordering, or task design;
- proposed minimal correction;
- regression test that would prevent recurrence where automation is possible.

### Voluntary exploration

After the first required result, record whether the learner voluntarily:

- replays;
- changes one variable;
- tries another scenario;
- creates a custom input;
- stops immediately.

Treat this as behavioral product evidence, not a universal measure of motivation.

## 5. Accessibility and responsive checks with people

Automated QA remains necessary but is insufficient.

At least one human pass should cover each of:

- keyboard only;
- `prefers-reduced-motion` enabled;
- 390 px-class viewport;
- 200% browser zoom;
- screen reader on a representative desktop/browser combination when feasible.

Record whether the learner can recover the same *instructional relation*, not merely whether every control is technically reachable.

For example, the reduced-motion path for a temporal mechanism must still make event order inferable; a text label that says animation disabled is not equivalent evidence.

## 6. Locale validation

For ZH, VI, and ES, use fluent readers rather than machine back-translation as the acceptance authority for learner-facing naturalness.

Check:

- task intent;
- technical term accuracy;
- label brevity;
- dynamic-state grammar;
- whether the active prediction/result remains understandable after a locale switch;
- whether a translated phrase accidentally strengthens a bounded claim.

Do not require sentence-by-sentence literal equivalence when a more natural translation preserves the same pedagogical contract.

## 7. Applet-specific observation anchors

### Transformer Language Modeling

Watch whether learners understand that the four-stage pulse is a replay of state relations, not a measured wall-clock pipeline. Check whether `Append argmax token` is understood as a deterministic rule rather than stochastic model generation.

### Agent Tool Use and Context Protocols

Watch whether learners distinguish:

- available from authorized;
- authorized from executed;
- learner-selected sandbox action from model-selected action;
- simulated side effect from a real external action;
- tool observation data from an instruction that should be followed.

### CNF and SAT Builder

Watch whether the branch/prune tree clarifies that DPLL searches selectively rather than enumerating every assignment, and whether a conflict leaf is understood as pruning one branch rather than proving every sibling branch impossible.

### Bayesian Network

Watch whether the previous-posterior marker reduces memory burden and makes explaining away visible. Explicitly probe whether anyone interprets the marker or graph as showing probability physically flowing along arrows; that interpretation is a kill-condition defect.

## 8. Stopping rules for a design

Reopen an accepted design if:

- 2 or more independent participants form the same P0/P1 false model from the same visual/control;
- a majority cannot identify the first meaningful action without prompting;
- prediction-before-reveal is routinely bypassed because the result is visible elsewhere;
- reduced-motion or keyboard use removes the concept-defining relation;
- locale wording changes the mathematical or epistemic claim;
- the new interaction attracts attention but learners cannot connect it to the mechanism.

Do not redesign merely because every learner does not prefer every topic.

## 9. Evidence needed for stronger claims

After a pilot, it is reasonable to report bounded findings such as:

- median time to first meaningful action in the observed sample;
- proportion of observed tasks completed without facilitator prompting;
- recurring misconception categories;
- proportion of mechanism explanations at each rubric level;
- qualitative preference or replay behavior in that sample.

Do not generalize to population-level learning gains from a convenience usability pilot.

A claim that a feature *improves learning* relative to the previous interface requires a comparison design with an appropriate outcome measure and enough participants to support the intended inference.

## 10. Product workflow

For any human finding that triggers a change:

1. reproduce the interface condition;
2. classify the failure using the FAS and v1.1 pedagogical severity system;
3. make the smallest mechanism-faithful correction;
4. add deterministic/browser regression where possible;
5. rerun the entire exact-head Verify gate;
6. repeat the affected human task before claiming the issue is resolved.

This keeps human evidence and deterministic assurance complementary rather than substituting one for the other.