# AI Playgrounds Engagement Usability Pilot 01

Date: 2026-08-25

Status: planning-only operational kit. This does not authorize a product change or support population-level claims about learning or engagement.

Baseline under test: released v1.5.0, commit `467a9dc3768eddffd6238674b9752eaea1917ce8`.

## Purpose

The v1.5 Full Assurance Stack establishes design-level engagement/immediate-impact excellence under deterministic, semantic, browser, responsive, localization, and negative-test evidence. The remaining uncertainty is human: whether first-time learners actually notice the intended interaction, form the intended mental model, and voluntarily explore it.

Pilot 01 operationalizes `docs/ENGAGEMENT_USABILITY_PROTOCOL.md` without changing the released product.

## Scope

Primary applets under test:

- Transformer Language Modeling — v1.5 state journey, deterministic argmax continuation, and baseline/current comparison.
- Agent Tool Use and Context Protocols — runtime packet, gate stopping, context delta, and isolated learner sandbox.
- CNF and SAT Builder — DPLL branch/prune tree.
- Bayesian Network — exact previous/current posterior comparison.

Control applets for calibration rather than redesign pressure:

- Convolution Playground — natural high-visual-impact ceiling case.
- Q-Learning Gridworld — natural temporal/learning ceiling case.
- Pathfinding Visualizer — natural search-animation ceiling case.

No redesign is triggered merely because a control applet receives stronger subjective preference than a more abstract topic.

## Participants

Recommended formative sample: 8 first-time users in the intended secondary-school / early-undergraduate range.

Each participant tests four applets: two of the four v1.5-modified applets, one high-visual control applet, and one additional applet assigned to balance exposure. Rotate order so no applet is systematically advantaged by being first.

Target at least four independent observations for each v1.5-modified applet. This is a formative usability sample, not an effectiveness study.

Do not collect names, email addresses, account identifiers, exact location, or other unnecessary personal data. Use anonymous participant IDs such as P01–P08.

## Facilitator protocol

For each applet:

1. Open directly to the applet. Do not give a tour.
2. Say: `Tell me what you think this page lets you investigate, and show me what you would try first.`
3. Start the first-action timer when the interactive area is usable.
4. Do not point at controls unless the participant is genuinely stuck.
5. After the first substantive state change, ask: `What changed, and what in the applet caused it?`
6. Use one prediction-before-reveal challenge and record whether the prediction is committed before reveal.
7. Ask: `Try one different case that you think might behave differently.` Do not prescribe the variable unless needed to recover from confusion.
8. Record any false mental model verbatim before correcting it.
9. At the end, ask: `What would you try next if I gave you two more minutes?`

Do not praise a specific answer while the task is active. Neutral acknowledgements are acceptable.

## Applet-specific tasks and kill-condition probes

### Transformer Language Modeling

Required observations:

- Can the learner identify a meaningful first action without reading every panel?
- Does the Tokens → Represent → Attend → Predict journey help them connect the panels as one state relation?
- Do they understand `Append argmax token` as an explicit deterministic rule rather than stochastic generation?
- Can they save a baseline, change one model/input control, and correctly describe at least one before/after difference?

Kill-condition probes:

- learner interprets the replay pulse as measured wall-clock timing;
- learner believes argmax continuation represents ordinary stochastic text generation;
- comparison values are read as causal importance claims unsupported by the toy model.

### Agent Tool Use and Context Protocols

Required observations:

- Can the learner distinguish available, valid, authorized, executed, and observed?
- Does an invalid/unauthorized action visibly stop at the expected gate?
- Is the context delta understood as a state update caused by the observation?
- Can the learner use the one-step sandbox and recognize it as learner-selected rather than model-selected?

Kill-condition probes:

- simulated mail/calendar/tool action is mistaken for a real external action;
- learner-selected sandbox action is mistaken for the model's decision;
- tool-returned instruction-like text is treated as trusted control instruction;
- authorization is conflated with execution.

### CNF and SAT Builder

Required observations:

- Can the learner connect DPLL stepping to growth of the same branch/prune tree?
- Is a conflict leaf understood as pruning one branch rather than proving all sibling branches impossible?
- Can the learner identify where sibling backtracking occurs?

Kill-condition probe:

- repeated interpretation that the tree enumerates every possible assignment regardless of DPLL propagation/pruning.

### Bayesian Network

Required observations:

- Can the learner use the retained previous-posterior marker without memorizing the earlier value?
- In the explaining-away scenario, can the learner describe the direction of the posterior change after adding evidence?

Kill-condition probe:

- repeated interpretation that probability physically flows along graph arrows or that the ghost marker represents a second inference algorithm.

## Core measures

Record one row per participant × applet in `docs/ENGAGEMENT_USABILITY_OBSERVATIONS.csv`.

Primary fields:

- seconds to first meaningful action;
- first action class: mechanism-relevant / administrative / unrelated / blocked;
- whether prompting was required;
- prediction committed before reveal;
- mechanism explanation score 0–3 using the existing protocol;
- voluntary replay/change/scenario/custom-input behavior;
- false-model severity and verbatim description;
- accessibility/locale condition where applicable.

The 10-second first-action target is diagnostic, not a hard pass/fail threshold.

## Accessibility sub-round

Across the eight participants, ensure human coverage of:

- keyboard-only operation;
- reduced-motion preference;
- 390 px-class viewport;
- 200% browser zoom.

If feasible, add one representative desktop screen-reader pass. The acceptance question is whether the same instructional relation can be recovered, not merely whether controls receive focus.

## Locale sub-round

Machine parity is already covered. Human naturalness requires fluent readers.

For ZH, VI, and ES, ask fluent readers to perform one active state-change task in at least the four v1.5-modified applets. Record technical-term errors, awkward dynamic grammar, ambiguous labels, or altered epistemic claims.

Do not require literal translation when a more natural phrase preserves the same contract.

## Escalation and stopping rules

Reopen a design when any of the following occurs:

- two or more independent participants form the same P0/P1 false model from the same surface;
- a majority cannot identify a meaningful first action without prompting;
- prediction-before-reveal is routinely bypassed because the result is visible elsewhere;
- keyboard/reduced-motion/mobile/zoom use removes the concept-defining relation;
- locale wording changes the mathematical, causal, or epistemic claim;
- the new interaction attracts attention but learners cannot connect it to the mechanism.

Do not redesign because one participant dislikes a topic, prefers another visual style, or asks for decorative effects unsupported by the mechanism.

## Decision procedure after Pilot 01

For each finding:

1. classify it under the engagement FAS and v1.1 pedagogical severity system;
2. reproduce the exact interface condition;
3. decide whether the defect is copy, visualization, control ordering, task design, or no defect;
4. make the smallest mechanism-faithful correction only if a stop rule is met or repeated evidence supports it;
5. add deterministic/browser regression where feasible;
6. rerun the full exact-head Verify stack;
7. repeat the affected human task before considering the issue closed.

If no stop rule is triggered, freeze v1.5 engagement design and do not add further spectacle.