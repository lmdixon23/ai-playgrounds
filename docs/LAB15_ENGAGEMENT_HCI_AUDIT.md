# Lab 15 Engagement and Learner-Centered HCI Audit

**Artifact:** Lab 15, Game Trees: Minimax and Alpha-Beta Pruning  
**Release target:** AI Playgrounds v1.6.0  
**Baseline:** v1.5.1 (`e548a9bcd9e06e2c780335ce4e4a065f7a72167c`)  
**Mode:** adversarial design audit plus HCI release gate  
**Human evidence:** none yet; design/browser conclusions must not be represented as measured learner preference or learning gain.

## Direct verdict

**Adopt the current interaction model without another spectacle layer.**

Lab 15 already has a mechanism-faithful memorable transformation: the learner can watch exact MIN/MAX values back up through a game tree and then watch Alpha-Beta mark a still-visible subtree as **not evaluated** once the current bounds prove that the subtree cannot change the exact minimax result. The same tree can then be searched in another child order to show **different work, same result**.

This is the appropriate “wow” for adversarial search. Additional generic animation, rewards, sound, particles, badges, or an automatic jump directly to the first prune would not improve the causal model and could weaken prediction and explanation.

## Evidence and learning objective

### Executed/measured software evidence

- Independent Python reference: 26/26 tests pass.
- Bounded exhaustive census: 648 cases.
- Independent JavaScript core: Python/JavaScript parity passes across all frozen scenario and validation families.
- Prototype browser QA: 22/22.
- English single-file candidate QA: 22/22.
- EN/ZH/VI/ES semantic localization: 1,235 checks, 0 failures, 126 presentation keys per locale.
- Four-locale browser/state-preservation QA: 39/39 with no page or console errors after the R6 localization-runtime correction.

### Intended learner model

1. Terminal utilities are given values at completed game states.
2. MAX backs up the largest child value; MIN backs up the smallest because the opponent also chooses optimally.
3. The root value and optimal move come from recursive adversarial backup, not from greedily choosing the largest visible terminal number.
4. Alpha-Beta is an exact optimization of minimax on the same fixed tree and child order.
5. A cutoff is safe when the current bounds prove that remaining siblings cannot alter the ancestor's rational choice.
6. Pruned nodes remain part of the game tree but are not evaluated by that search run.
7. Child order can change search work without changing the exact minimax result.

## First meaningful action and agency

**Observed in artifact:** the learner can change scenario, algorithm, child order, and terminal utilities; restart, step backward, step forward, reveal the complete trace, and save a run for comparison.

**Judgment:** excellent design-level agency. Every primary manipulation changes an actual part of the modeled search rather than a cosmetic state.

## Causal continuity

The tree remains spatially stable while the trace advances. Current, visited, returned, and pruned states are rendered on the same structure. The trace explanation and text-equivalent state update from the same deterministic result object.

**Judgment:** excellent. The learner does not have to mentally join unrelated panels to understand where a cutoff occurred.

## Immediate impact / mechanism-first wow

The strongest transformation is:

`same game tree -> accumulating alpha/beta evidence -> safe cutoff -> visible subtree remains present but explicitly unevaluated`

The second strongest is:

`same tree + different child order -> different evaluated-leaf count -> same root value and selected move`

**Judgment:** excellent for this mechanism once the learner selects/reaches the pruning scenario.

### Candidate intervention considered: auto-open or auto-jump to first prune

**Rejected.** Starting with a pre-revealed cutoff would increase spectacle but weaken the prerequisite idea that Alpha-Beta is justified by already-backed-up values and bounds. The existing `Simple backup` path provides the cognitive foundation; `First safe prune`, `Good move ordering`, and `Reveal complete trace` already make the high-impact state quickly reachable without falsifying the sequence.

### Candidate intervention considered: animate deleted/disappearing branches

**Rejected.** Pruned nodes are part of the problem definition. Making them disappear encourages the misconception that pruning changes the game tree rather than the amount of search work. The current faded/still-visible representation is more faithful.

### Candidate intervention considered: gamification, points, badges, sound

**Rejected.** No learning or recovery problem is established that these controls would solve.

## Prediction coupling

Five Guided Challenges require an explicit prediction to be locked before deterministic reveal. The challenges target root choice, MIN backup, pruning, move ordering, and greedy-versus-minimax reasoning.

**Judgment:** excellent design-level prediction coupling. Release tests must preserve the lock-before-reveal invariant.

## Misconception handling

The artifact explicitly protects against:

- “MAX picks the largest leaf anywhere in the tree.”
- “MIN is an error or loss state rather than the opponent's optimal choice.”
- “Alpha-Beta is approximate.”
- “Pruned nodes were evaluated and then hidden.”
- “A better child order changes the minimax answer.”
- “The deterministic tie-break means the optimum is unique.”

**Judgment:** strong. No additional warning layer is justified before human testing.

## Accessibility and equivalent access

### Implemented/verified paths

- keyboard-focus visibility;
- native form controls for scenario, algorithm, child order, utilities, and challenges;
- a complete textual state representation alongside the SVG tree;
- `aria-live` trace/challenge feedback;
- reduced-motion behavior;
- internal tree scrolling rather than forced page-wide overflow;
- EN/ZH/VI/ES presentation-only locale switching;
- v1.6 HCI gate covering 390x844 portrait, 844x390 landscape, 640x720 split view, and 200% text enlargement.

### Unknown

No claim of WCAG conformance, screen-reader usability, or classroom accessibility outcome is made without human assistive-technology testing.

## Responsive integrity

R6 exposed and corrected a real narrow-mobile containment problem rather than weakening the assertion. The public R7 gate additionally tests portrait, short landscape, split view, reduced motion, and 200% text enlargement.

**Judgment:** release-worthy if the permanent R7 gate passes on the exact release head.

## Cognitive load

The current default preserves the pedagogically simpler backup mechanism before requiring the learner to interpret a cutoff. The trace, stable tree, summary metrics, and textual state provide multiple representations, but they all derive from the same computation.

**Judgment:** acceptable-to-strong. Automatically starting at the most dramatic cutoff state is rejected because it would increase extraneous search for meaning.

## FMEA summary

| Failure mode | Severity | Existing/proposed control | Ruling |
| --- | --- | --- | --- |
| Learner treats pruning as approximation | Serious | exact minimax/alpha-beta parity, same-result move-order experiment, explanatory copy | controlled |
| Learner thinks pruned nodes were evaluated | Serious | nodes remain visible and explicitly labeled not evaluated; trace/text state exposes pruned set | controlled |
| Learner chooses greedy visible leaf | Serious | greedy-trap scenario and locked prediction challenge | controlled |
| Locale switch mutates search state | Serious | 39-check R6 state-preservation gate | controlled |
| Localization observer loops or stalls page | Serious | R6 observer disconnect/mutation guard; permanent browser gate | corrected |
| Narrow viewport loses controls/content | Moderate | mobile containment CSS plus portrait/landscape/split/text-enlargement checks | release-gated |
| Visual tree unavailable to a learner | Serious | text-equivalent state and native control path | partially controlled; human AT testing remains |

Ratings are expert judgments unless explicitly described as executed checks.

## Arbiter ruling

**ADOPT current Lab 15 behavior for v1.6 public integration if the exact-head R7 and inherited suite gates pass.**

Do not add a new engagement feature merely to make the lab appear more animated. The existing prune transformation, exact move-order comparison, direct manipulation, replay, and prediction coupling satisfy the suite's mechanism-first engagement standard at the design level.

## Human-evidence boundary

The following remain unknown until first-time learners are observed:

- time to first meaningful action;
- whether learners spontaneously distinguish “not evaluated” from “removed from the game”;
- whether the simple-backup-first sequence makes the later cutoff easier to explain;
- voluntary exploration depth;
- screen-reader and assistive-technology usability;
- whether translations are pedagogically natural to fluent learners.

Any repeated serious false mental model in the human usability pilot reopens this audit. Otherwise, freeze the design rather than continuing to decorate it.
