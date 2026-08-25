# Quick Assign Architecture

Date: 2026-08-25
Status: v1.6.1 candidate contract; no release is authorized by this file alone.

## Purpose

AI Playgrounds already contains the machinery needed for short assignable work: Guided Challenges, scenario galleries, three-question checks, and local-only Student response packets. Quick Assigns formalize that existing machinery instead of creating a second worksheet system.

The design goal is simple: a teacher should be able to say **“Open this lab and complete `QA-SEARCH-01`”** without creating a separate worksheet, account, backend, or grading workflow.

## Three assignment levels

### Level 1 — Quick Assign

- **Target time:** 10–15 minutes.
- **Location:** inside the applet.
- **Structure:** `predict -> manipulate/run -> observe -> explain -> transfer`.
- **Student product:** the existing local response packet, copied or printed if the teacher requires submission.
- **Scope:** one mechanism and one controlled comparison; not a miniature unit.
- **Answers:** no private answer key is required for ordinary use. Teacher-facing “look for” criteria describe the mechanism evidence expected in a strong response without turning the task into answer copying.

### Level 2 — Activity Pack

- **Target time:** roughly 30–50 minutes.
- **Location:** separate student-facing activity page.
- **Structure:** multiple connected experiments with prediction, evidence, explanation, and transfer.
- **Current public canaries:** `NN-1` and `CNN-1`.
- **Student product:** local browser autosave plus print/PDF.
- **Teacher-answer boundary:** private keys or grading exemplars remain outside the public student surface when secrecy is genuinely useful.

### Level 3 — Lesson / Unit Pack

Reserved for future use. A Level 3 resource may include a longer lesson sequence, prerequisite/warm-up material, extension tasks, rubric guidance, and teacher planning notes. No Level 3 package is implied to exist until one is explicitly released.

## Stable ID contract

Quick Assign IDs use:

`QA-<CONCEPT>-<two-digit sequence>`

Examples:

- `QA-SEARCH-01`
- `QA-LOCAL-01`
- `QA-WUMPUS-01`
- `QA-SAT-01`

Rules:

1. IDs are permanent once publicly released.
2. An ID is never reassigned to a different lab or learning objective.
3. Later revisions may improve wording or accessibility while preserving the activity's mechanism and expected evidence.
4. If an activity must be retired, retain an alias/retirement record rather than silently recycling its ID.
5. Reserved IDs may exist in the registry without being surfaced publicly.

## Level-1 interaction contract

Every Quick Assign must contain or directly reuse all five stages:

1. **Predict** — commit to a mechanism-specific expectation before the relevant result is revealed or run.
2. **Manipulate / run** — perform a bounded existing applet action or comparison; never invoke a second hidden algorithm.
3. **Observe** — record specific state evidence from the applet, not a generic impression.
4. **Explain** — connect the observed state change to the target mechanism using course vocabulary.
5. **Transfer** — answer a counterfactual or changed-case prompt requiring the same mechanism in a new state.

The existing Guided Challenge state machine remains the stricter prediction-before-reveal path. Quick Assigns may use it, the existing deterministic scenario, or a controlled applet comparison, but the student response packet remains the submission surface.

## Teacher “look for” contract

A public Quick Assign may expose a short teacher-facing criterion such as:

> Look for an explanation that A* can reduce search work by changing frontier ordering while an admissible heuristic preserves the shortest-path guarantee; avoid “A* is always faster.”

This is a grading criterion, not a hidden answer key. Exact numerical keys, if later needed, should live outside the public student page.

## Accessibility and recovery

Quick Assigns inherit the HCI state/recovery contract:

`initial state -> action -> expected state -> recovery -> focus/accessibility/state consistency`

Required properties:

- keyboard-accessible controls for the required task;
- visible focus;
- text-equivalent state for concept-defining results;
- reduced-motion support without removing the mechanism;
- local draft recovery where the response packet already supports it;
- clear reset/clear behavior;
- mobile and split-view containment at the supported release boundary.

## Localization

The core learner applets support EN/ZH/VI/ES. A Quick Assign is not allowed to claim four-language support merely because its host applet does.

For a Quick Assign to be marked `locales: [en, zh, vi, es]`, all learner-facing Quick Assign labels, prompts, placeholders, state labels, and packet output headings required by that activity must survive locale switching without changing the algorithm or answer state.

The first four active canaries are required to meet this four-locale Quick Assign contract before public release. Fluent-reader naturalness remains a separate human-evidence question.

## Privacy

Quick Assign responses are student-authored content and must not be sent to AI Playgrounds analytics.

- no response text in GoatCounter requests;
- no student names or IDs requested by the applet;
- no response text in share URLs;
- localStorage is limited to the existing local draft behavior;
- copied/printed packets are controlled by the learner/teacher, not transmitted to the project.

## Analytics

A coarse event may record that a Quick Assign was opened or a first substantive applet interaction occurred, but it may include only the stable activity ID or applet slug. It must never include response content, grades, identifiers, or experiment-state values.

## Initial rollout

The v1.6.1 candidate surfaces four early-course Quick Assigns because they are the most likely to be useful at the beginning of a school year:

- `QA-SEARCH-01` — Pathfinding
- `QA-LOCAL-01` — Hill Climbing / Simulated Annealing
- `QA-WUMPUS-01` — Wumpus World
- `QA-SAT-01` — CNF/SAT

The remaining eleven IDs are reserved in the registry so the naming system is stable, but they are not publicly advertised until their individual activity contracts are verified.

## Expansion gate

A reserved Quick Assign becomes active only when:

- its mechanism-specific task is defined;
- the task reuses the existing applet algorithm/state path;
- Predict / Observe / Explain / Transfer are coherent and non-redundant;
- locale and state preservation pass at the declared scope;
- keyboard/reduced-motion/responsive checks pass;
- no Critical or unresolved Serious finding exists;
- the task is materially better than telling the teacher to use an arbitrary scenario.

Do not create multiple Quick Assigns per lab merely to fill a quota.