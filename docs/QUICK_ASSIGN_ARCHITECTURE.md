# Quick Assign Architecture

Date: 2026-08-27
Status: **active v1.7.1 contract**.

## Purpose

AI Playgrounds contains the machinery needed for short assignable work: Guided Challenges, scenarios or bounded comparisons, and local-only response surfaces. Quick Assigns formalize that machinery instead of creating a second worksheet system.

The design goal is simple: a teacher should be able to say **Open this lab and complete `QA-SEARCH-01`** without creating a separate worksheet, account, backend, or grading workflow.

## Three assignment levels

### Level 1 — Quick Assign

- **Target time:** 10–15 minutes.
- **Location:** inside the applet.
- **Structure:** `predict -> manipulate/run -> observe -> explain -> transfer`.
- **Student product:** the applet's local response surface, copied or printed if the teacher requires submission.
- **Scope:** one mechanism and one controlled comparison; not a miniature unit.
- **Answers:** no private answer key is required for ordinary use. Teacher-facing look-for criteria describe the mechanism evidence expected in a strong response without turning the task into answer copying.

### Level 2 — Activity Pack

- **Target time:** roughly 30–50 minutes.
- **Location:** separate student-facing activity page.
- **Structure:** multiple connected experiments with prediction, evidence, explanation, and transfer.
- **Current public canaries:** `NN-1` and `CNN-1`.
- **Student product:** local browser autosave plus print/PDF.
- **Current locale boundary:** English-only until separately translated and verified.
- **Teacher-answer boundary:** private keys or grading exemplars remain outside the public student surface when secrecy is genuinely useful.

### Level 3 — Lesson / Unit Pack

Reserved for future use. A Level 3 resource may include a longer lesson sequence, prerequisite/warm-up material, extension tasks, rubric guidance, and teacher planning notes. No Level 3 package is implied to exist until one is explicitly released.

## Stable ID contract

Quick Assign IDs use:

`QA-<CONCEPT>-<two-digit sequence>`

IDs are permanent once publicly released and are never silently reassigned.

## Current active Level-1 registry

All fifteen public applets have one active v1.7.1 Quick Assign:

- `QA-SEARCH-01` — Pathfinding
- `QA-LOCAL-01` — Hill Climbing / Simulated Annealing
- `QA-WUMPUS-01` — Wumpus World
- `QA-SAT-01` — CNF/SAT
- `QA-BAYES-01` — Bayes Rule / Naïve Bayes
- `QA-BN-01` — Bayesian Networks
- `QA-KNN-01` — K-Nearest Neighbors
- `QA-OVERFIT-01` — Overfitting
- `QA-NN-01` — Tiny Neural Network
- `QA-KMEANS-01` — K-Means
- `QA-CNN-01` — Convolution
- `QA-QL-01` — Q-Learning
- `QA-MINIMAX-01` — Minimax / Alpha-Beta
- `QA-TRANSFORMER-01` — Transformer Language Modeling
- `QA-AGENT-01` — Agent Tool Use and Context Protocols

The first four were the v1.6.1 rollout canaries. The remaining eleven were promoted in v1.7.0 after the all-lab assignment, localization/state, responsive, and release gates passed. v1.7.1 preserves that complete assignment layer unchanged.

## Level-1 interaction contract

Every Quick Assign must contain or directly reuse all five stages:

1. **Predict** — commit to a mechanism-specific expectation before the relevant result is revealed or run.
2. **Manipulate / run** — perform a bounded existing applet action or comparison; never invoke a second hidden algorithm.
3. **Observe** — record specific state evidence from the applet, not a generic impression.
4. **Explain** — connect the observed state change to the target mechanism using course vocabulary.
5. **Transfer** — answer a counterfactual or changed-case prompt requiring the same mechanism in a new state.

The Guided Challenge state machine remains the stricter prediction-before-reveal path where one exists. Quick Assigns may use it, an existing deterministic scenario, or a controlled applet comparison, but they must reuse the applet's real mechanism/state path.

## Teacher look-for contract

A public Quick Assign may expose a short teacher-facing criterion such as:

> Look for an explanation that A* can reduce search work by changing frontier ordering while an admissible heuristic preserves the shortest-path guarantee; avoid the claim that A* is always faster.

This is a grading criterion, not a hidden answer key. Exact numerical keys, if later needed, should live outside the public student page when secrecy is useful.

## Accessibility and recovery

Quick Assigns inherit the HCI state/recovery contract:

`initial state -> action -> expected state -> recovery -> focus/accessibility/state consistency`

Required properties:

- keyboard-accessible controls for the required task;
- visible focus;
- text-equivalent state for concept-defining results where feasible;
- reduced-motion support without removing the mechanism;
- local draft recovery where the response surface supports it;
- clear reset/clear behavior;
- mobile and split-view containment at the supported release boundary.

## Localization

All fifteen current Level-1 Quick Assigns are verified for the learner-locale set:

`[en, zh, vi, es]`

For that claim to remain true, all learner-facing Quick Assign labels, prompts, placeholders, state labels, and packet/output headings required by the activity must survive locale switching without changing the algorithm state or learner response text.

Fluent-reader naturalness remains a separate human-evidence question; automated semantic/state parity does not establish translation quality by itself.

## Privacy

Quick Assign responses are student-authored content and must not be sent to AI Playgrounds analytics.

- no response text in GoatCounter requests;
- no student names or IDs requested by the applet;
- no response text in share URLs;
- localStorage is limited to local draft behavior;
- copied/printed packets are controlled by the learner/teacher, not transmitted to the project.

## Analytics

A coarse event may record that a Quick Assign was opened or that a first substantive applet interaction occurred, but it may include only the stable activity ID or applet slug. It must never include response content, grades, identifiers, or experiment-state values.

## Expansion gate

A future additional Quick Assign becomes active only when:

- its mechanism-specific task is defined;
- it reuses the existing applet algorithm/state path;
- Predict / Observe / Explain / Transfer are coherent and non-redundant;
- locale and state preservation pass at the declared scope;
- keyboard/reduced-motion/responsive checks pass;
- no Critical or unresolved Serious finding exists;
- it is materially better than telling the teacher to use an arbitrary scenario.

Do not create multiple Quick Assigns per lab merely to fill a quota.
