# AI Playgrounds Learner-Centered State and Recovery Contract

Date: 2026-08-25

Status: v1.5.1 HCI hardening contract.

## Purpose

A shared control is not adequately tested merely because it exists and performs its primary action once. For learner-facing software, verification must also establish the state reached after the action, the route back from that state, and whether focus, accessible naming, and instructional meaning survive the transition.

This contract adapts the strongest reusable interaction-assurance pattern found in the audited PWP Notebooks: **initial state -> learner action -> expected state -> recovery/close path -> focus/ARIA/state consistency**. AI Playgrounds keeps concept-specific interactions rather than forcing every applet into the same surface design.

## Required transition record

For every materially shared or high-risk learner interaction, record:

1. **Initial state** — visible controls, enabled/disabled state, model state, focus location when relevant.
2. **Learner action** — click, tap, key press, input change, locale switch, reset, replay, disclosure open/close, or similar action.
3. **Expected state** — visible consequence and machine-state consequence.
4. **Recovery path** — how the learner undoes, closes, resets, repositions, or returns to the prior task.
5. **Focus contract** — where keyboard focus remains or returns after a modal/disclosure/reset when relevant.
6. **Accessible-state contract** — `aria-*`, text equivalent, non-color cue, and reduced-motion relation when relevant.
7. **State preservation** — what must remain unchanged, including locale-independent model state and isolated sandbox state.
8. **Failure-path behavior** — invalid, denied, rapid-repeat, near-miss, and interrupted actions where applicable.

## Required examples

### Guided Challenge prediction

- Initial: challenge active; prediction not locked.
- Action: learner selects/enters a prediction.
- Expected: prediction state updates without revealing the actual result.
- Recovery: learner may change prediction until locking; reset returns to the documented challenge baseline.
- Safety: no result becomes visible before reveal through another surface.

### Reset

- Initial: non-default learner state exists.
- Action: learner invokes reset.
- Expected: documented default state is restored.
- Recovery: where reset can destroy substantial learner work, confirmation or an equivalent guard is required.
- Focus: focus returns to a meaningful control rather than disappearing to the document body.

### Disclosure or modal

- Initial: control closed.
- Action: open by pointer or keyboard.
- Expected: content becomes visible and programmatically related to the trigger.
- Recovery: Escape/close path works where the pattern supports it.
- Focus: focus is not trapped or lost; modal focus returns to the invoking control when closed.

### Dense visualization selection

- Initial: learner has a partially completed selection.
- Action: pointer tap/click near an intended target.
- Expected: selection changes only when the input is plausibly directed at a target.
- Recovery: an imprecise touch must not silently destroy unrelated progress.
- Equivalent access: keyboard selection exposes the same instructional relation.

### Locally autosaved Activity Pack

- Initial: empty or restored response fields.
- Action: learner enters text.
- Expected: response is saved locally without network transmission.
- Recovery: refresh restores the local response; guarded clear removes it intentionally and returns focus to the first response field.

## Viewport and input matrix

The general suite regression remains desktop/tablet/mobile. A lightweight HCI hardening gate adds targeted conditions that are disproportionately likely to expose learner-facing failures:

- 390 x 844 phone portrait;
- 844 x 390 phone landscape;
- approximately 640 px split-screen/narrow desktop;
- 200% text enlargement stress;
- coarse-pointer/touch behavior for custom graphics;
- keyboard-only recovery for custom selection and reset paths.

Projector-specific visual legibility remains a human/classroom validation question unless a measurable layout contract is defined.

## Scope rule

Do not add controls or animation merely to make applets uniform. Apply this contract to the interaction that already expresses the concept, and add a new shared pattern only when it reduces learner friction, prevents an error, improves accessibility, or creates useful transfer between applets.

## Evidence boundary

Passing this contract establishes deterministic interaction behavior under the tested conditions. It does not establish accessibility conformance, learner comprehension, preference, or learning gains. Those remain human-evidence questions under `docs/ENGAGEMENT_USABILITY_PROTOCOL.md`.
