# AI Playgrounds v1.1 Pedagogical Red Team

Status: implementation inventory for the v1.1 development line

Base audited commit: `19d9a22aef9f537c01866964afbf8d1755c8a3c0`

## Evidence boundary

The existing release checks establish bounded software behavior and deployment integrity. They do not establish that the learner-facing wording, visual encoding, or interaction sequence produces the intended mental model. This audit therefore treats conceptual precision and epistemic sequencing as separate release obligations.

The immediate trigger was external educator feedback on the KNN playground. The reviewer observed that a learner could manipulate `k`, see the result, and construct a convincing explanation afterward without having predicted the mechanism. The reviewer also noted that learners may read nearest as visually closest even though the selected neighbors depend on the distance metric and feature representation.

## Shared suite-level finding

All twelve playgrounds use a predict, run, explain sequence in their scenarios and student response packet. In the current release, prediction is normally an instruction or text field rather than an enforced software state. A learner can therefore reveal the outcome before committing a prediction.

The v1.1 line separates two modes:

1. Explore mode preserves immediate manipulation.
2. Guided Challenge mode will require a committed, mechanism-specific prediction before reveal.

Guided Challenge is a later implementation stage. This first hardening stage corrects mathematical claims, terminology, and contradictory short-form explanations before those strings are translated or embedded into a new interaction system.

## Severity scale

- P0: mathematically false, epistemically unsupported, or directly contradictory to another maintained explanation.
- P1: materially misleading simplification or terminology likely to create an incorrect learner model.
- P2: useful clarification that does not currently overturn the central lesson.

## Findings and required corrections

### K-nearest neighbors

Severity: P0 and P1

- Nearest is not intrinsic. It depends on the representation, feature scaling, and selected distance metric.
- Equal-distance contours are not the same object as a KNN class decision boundary.
- The Manhattan worksheet currently mixes diamond contours with axis-aligned class-boundary language.
- Distance metric and distance weighting are different operations: the metric selects neighbors; weighting changes the votes after selection.
- Guided Challenge must ask learners to predict selected neighbors before predicting the class.

### Search and pathfinding

Severity: P1

- Reaching a goal after fewer expansions on one neighbor ordering is not the same claim as being faster in general.
- BFS shortest-path guarantees require unweighted or uniform-cost edges when path quality is measured by edge count.
- A heuristic can reduce work on a particular instance; the wording must not guarantee fewer expansions in every visualization.

### Hill climbing and simulated annealing

Severity: P0

- A cost-minimizing implementation should not be presented as steepest ascent without defining a negated fitness objective.
- Finite random restarts do not certify a global optimum.
- Tabu memory is not the only mechanism that permits movement away from a local optimum; accepting a best available worsening move also matters.
- Stochastic hill climbing introduces randomized choice; it does not simply avoid ties.

### Wumpus World

Severity: P0

- Comparative expected-value claims require a specified world distribution, prior, utility model, and action policy.
- A wider score distribution does not establish higher expected value.
- The applet is AIMA-inspired and simplified; it should not imply exact textbook identity where behavior differs.
- Teacher view compares ground truth with conclusions produced by this inference engine, not everything a logically complete agent should know.

### CNF and SAT

Severity: P0 and P1

- XOR is not inherently contradictory. The maintained example is unsatisfiable because a particular collection of XOR-style and truth constraints conflicts.
- The applet should keep exhaustive model enumeration distinct from DPLL branch pruning.
- Direct equivalent CNF expansion and compact equisatisfiable encodings must remain conceptually distinct.

### Bayes rule

Severity: P0

- Sensitivity and specificity must not be collapsed into the word accuracy in the central base-rate example.
- A chained second test can be treated as new evidence only under an explicit conditional-independence assumption.
- The classroom example must not generalize the idealized repeated-test calculation into a blanket claim about medical retesting.

### Bayesian networks

Severity: P0 and P1

- JohnCalls and MaryCalls are not simply independent. In the standard alarm network they are conditionally independent given Alarm.
- Conditional independence must always name or represent the conditioning set.
- The implementation comment must not conflate active-trail or Bayes-ball traversal on a DAG with moralization.

### Overfitting

Severity: P0 and P1

- A repeatedly inspected holdout used to select degree or regularization functions as validation data, not as a final untouched test set.
- The applet must reserve test-set terminology for a final evaluation after choices are fixed.
- Fixed statements about a useful degree, regularization effect, or additional data are properties of the current generated setting rather than universal laws.

### Neural networks

Severity: P1

- With biases, stacked linear-activation layers compose to one affine transformation, not one linear map.
- XOR requires a nonlinear representation in the original feature space; engineered nonlinear features can also make it linearly separable.
- The applet uses full-batch gradients. The optimizer label and primer must not teach that the data path is stochastic gradient descent.
- Representational capacity and optimization success must remain separate claims.

### K-means

Severity: P0

- Silhouette is diagnostic evidence, not a proof of a true or correct `k`.
- Synthetic Gaussian components are generating groups, not an ontologically unique clustering.
- K-means uses point centroids and squared Euclidean distance; centroid is not synonymous with Gaussian-shaped cluster.
- K-means++ improves initialization probabilities but does not guarantee the final optimum.

### Convolution

Severity: P1

- The implemented CNN-style operation is cross-correlation because the kernel is not flipped.
- Max pooling retains the numerically largest activation, not the largest magnitude unless the preceding representation makes those equivalent.
- A larger theoretical receptive field means one output can depend on a larger input region; it does not alone establish detection of a larger object or pattern.
- The output is one feature-map response, not everything the CNN sees.

### Q-learning

Severity: P0

- With `gamma < 1`, a delayed terminal reward is discounted even when the ordinary step reward is zero. Zero step penalty therefore does not remove all time preference.
- With `gamma = 0`, updates retain immediate rewards. Ordinary step penalties can affect many state-action pairs, not only actions next to terminal states.
- With deterministic tie-breaking and zero-initialized values, `epsilon = 0` can leave actions untried; the wording should not present a universal theorem about all exploration mechanisms.

## R1 implementation scope

This hardening stage:

1. Corrects the P0 and P1 learner-facing claims above in English and Simplified Chinese.
2. Aligns short-form scenario, worksheet, tour, tooltip, and profile language with the more careful long-form explanations.
3. Adds a deterministic pedagogical-claim checker so known prohibited formulations cannot silently return.
4. Records the Guided Challenge prediction targets for the next stage.
5. Does not alter the immutable v1.0.1 tag or archived release.
6. Does not yet add Vietnamese or Spanish. Localization begins only after the English and Chinese conceptual source strings are frozen.

## R2 Guided Challenge targets

- Search: predict the next frontier expansion.
- Hill climbing: predict the accepted neighboring state and acceptance reason.
- Wumpus: classify squares as proven safe, proven dangerous, or unresolved.
- SAT: predict unit propagation, branch survival, or contradiction.
- Bayes: predict true-positive and false-positive counts before posterior reveal.
- Bayesian network: predict update direction and active dependence paths.
- Overfitting: predict training and validation error movement.
- Neural network: predict representational or decision-boundary change.
- KNN: predict selected neighbors, then predicted class.
- K-means: predict assignments, then centroid movement.
- Convolution: predict one output-cell value before revealing the sum.
- Q-learning: predict action, TD target, and update direction.

## R3 localization gate

After R1 and R2 pass:

- Replace the two-button language switch with a native select control.
- Support `en`, `zh-Hans`, `vi`, and `es`.
- Translate controls, scenarios, state descriptions, teacher guidance, student packets, errors, and dynamic messages.
- Require terminology review by a Vietnamese ICT educator and a Spanish-language CS or AI educator.
- Expand browser and state-transition QA across all four language states.
