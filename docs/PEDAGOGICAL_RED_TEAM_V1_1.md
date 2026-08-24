# AI Playgrounds v1.1 Pedagogical Red-Team Inventory

## Purpose

This record distinguishes software correctness from instructional correctness. The existing deterministic and browser tests establish bounded software behavior. They do not establish that a learner will form the intended concept from the interface.

The red-team question used here is:

> What false mental model could a reasonable learner construct from the wording, visualization, control sequence, or feedback?

The inventory began with external educator feedback on the K-nearest-neighbors applet. That feedback identified a suite-wide problem: a written prediction prompt does not prevent a learner from seeing the result first and producing a plausible explanation afterward.

## Release boundary

- v1.0.1 remains immutable.
- This work belongs to v1.1 development.
- Paper 7 is not changed by this patch.
- English and existing Chinese wording are corrected together where the same conceptual defect appears.
- Vietnamese and Spanish localization is deferred until the corrected source concepts are stable.

## Severity classes

- P0: mathematically false, epistemically misleading, or internally contradictory.
- P1: technically imprecise wording likely to create a wrong novice model.
- P2: useful refinement that improves explanation but does not change the core claim.

## Findings and R1 resolution

### K-nearest neighbors

Risk: nearest may be interpreted as visually closest. Distance metric and distance weighting may be conflated. Metric-ball shapes may be confused with the classifier decision boundary. Cross-validation may be treated as producing the uniquely correct k.

R1:

- renames the control concepts to closeness rule and voting rule;
- states that the closeness rule and scaling determine which points count as nearest;
- distinguishes equal-distance contours from the full class decision boundary;
- corrects Manhattan geometry wording;
- weakens cross-validation from a universal selector to evidence for a sample and fold scheme;
- adds a guided prediction-before-reveal challenge that asks for the query point, predicted neighbor set, and predicted class before showing the actual mechanism.

### Search and pathfinding

Risk: reaching the goal first in one animation may be interpreted as generally faster. BFS edge-count optimality may be confused with weighted least-cost optimality.

R1:

- uses expansion counts for fixed-instance comparisons;
- states that one trace is not a general runtime ranking;
- defines BFS layers by number of edges from the start;
- qualifies weighted A-star behavior as a possible focus gain with lost optimality guarantee.

### Hill climbing and simulated annealing

Risk: steepest-ascent is confusing in a cost-minimization display. Random restart may be read as guaranteeing a global optimum after enough finite attempts.

R1:

- uses best-improvement for the cost-minimization rule;
- explains the naming choice;
- states that more restarts sample more basins but a finite run can still miss the global optimum;
- changes deterministic claims about different starts to possibility claims.

### Wumpus World

Risk: expected-value rankings are asserted without a distribution over worlds and utility model. The teacher view may imply that the simplified inference engine derives everything a complete agent should know. A probabilistic estimate may appear assumption-free.

R1:

- renames the hybrid strategy as AIMA-inspired;
- removes the unrelated Sutton attribution;
- removes unsupported expected-value ranking;
- states the explicit per-cell prior used by the frontier calculation;
- distinguishes hidden ground truth from conclusions produced by this simplified inference system.

### CNF and SAT

Risk: XOR itself may be learned as contradictory. Direct distribution may be mistaken for the only practical conversion route. Exhaustive enumeration and DPLL may be conflated.

R1:

- names the example as conflicting XOR constraints;
- labels exhaustive enumeration as a reference check and DPLL as a separate pruning trace;
- explains logically equivalent direct rewrites versus compact equisatisfiable encodings with auxiliary variables.

### Bayes rule

Risk: 99 percent sensitivity and specificity are collapsed into 99 percent accuracy. A repeated-test example is generalized into a medical-practice claim and hides the conditional-independence assumption.

R1:

- names sensitivity and specificity directly;
- makes conditional independence explicit for repeated updates;
- states that repeated tests can share systematic errors;
- removes generalized claims about why doctors retest.

### Bayesian networks

Risk: sibling reports may be called independent without naming the conditioning variable. Code comments conflate active-trail rules on a DAG with moralization.

R1:

- states that the two reports are conditionally independent given the alarm;
- defines conditional independence relative to a conditioning set;
- corrects the implementation comment to active-trail, Bayes-ball-style rules on the DAG.

### Overfitting

Risk: repeatedly inspected comparison data are called a held-out test set even while used to choose degree and regularization. The interface directly claims that zero noise makes overfitting impossible and that more data fixes it.

R1:

- calls the repeatedly viewed set validation data;
- retains the separate need for a final untouched test set;
- removes the false zero-noise claim;
- qualifies more-data and degree-five outcomes as setting-dependent rather than universal.

### Neural networks

Risk: layers with biases are described as linear maps rather than affine maps. XOR is described as requiring a nonlinear model without restricting the claim to the original features. Capacity and successful optimization may be conflated.

R1:

- uses affine map when biases are included;
- scopes XOR nonseparability to the original x-y representation;
- notes that engineered nonlinear features can also change separability;
- separates representational capacity from whether optimization finds suitable parameters.

### K-means

Risk: the nuanced essay says there is no universally correct k, but short-form UI says the highest silhouette identifies the true or right k. A centroid is described as Gaussian-shaped.

R1:

- treats silhouette as one piece of evidence;
- describes k=3 as matching three generating groups in one synthetic sample;
- removes true-k and right-k language;
- states that a centroid is a point and that Euclidean Voronoi partitions cannot preserve a curved arc as one cluster.

### Convolution

Risk: CNN-style cross-correlation is introduced as mathematical convolution without early qualification. Max pooling may be read as maximum magnitude. A larger receptive field may be equated with detecting a larger object.

R1:

- states that the unflipped operation is mathematically cross-correlation;
- defines max pooling as retaining the numerically largest value;
- distinguishes receptive-field dependence from feature detection;
- replaces the phrase What the CNN sees with one feature-map response.

### Q-learning

Risk: the app claims that zero step reward removes time pressure while gamma remains below one. This is mathematically false because later terminal reward is discounted more strongly. The gamma-zero explanation is also too narrow when immediate nonterminal rewards exist.

R1:

- allows gamma equal to one for the bounded episodic comparison;
- states that step costs and discounting are separate sources of time preference;
- rewrites the scenario to compare gamma 0.9 and gamma 1;
- states that gamma zero blocks delayed value propagation while direct transition rewards can still change Q-values.

## R1 limits

R1 corrects the major semantics and implements one guided challenge in KNN. It does not yet implement mechanism-specific guided challenges in all twelve applets. That is the next architectural stage after the R1 corrections pass software, browser, and pedagogical-contract regression.


## R1.1 remote-diff audit follow-up

The first R1 automated contract gate passed 145 checks, but an independent review of the actual draft-PR diff found residual duplicate claims in secondary tours, worksheets, Chinese strings, accessibility summaries, and optimizer/tooltips. R1.1 therefore treats duplicate learner-facing surfaces as part of the same conceptual contract rather than accepting a corrected headline while contradictory fallback copy remains.

The follow-up specifically closes: KNN universal sweet-spot wording; finite-run hill-climbing guarantees; simplified Wumpus strategy identity; repeated-test Bayes assumptions; Bayesian-network conditioning wording; validation-vs-test terminology in all overfitting surfaces; full-batch gradient-descent naming; Chinese K-means true-k claims; Chinese convolution/cross-correlation parity; and setup-specific exploration/time-preference wording in Q-learning.

## R1.2 exact-head remote content audit

After the 76a5aad exact-head CI passed, an independent review of the rendered duplicate surfaces found additional English/Chinese drift that phrase-level CI had not yet covered. The final R1 audit therefore closes residual claims around KNN weighted ties and scaling, search speed wording, low-temperature simulated annealing, Wumpus expected-value assumptions, repeated-test Bayes assumptions, validation-versus-test terminology, affine neural-network composition, k-means objective/initialization nuance, convolution/pooling scope, and setup-dependent Q-learning exploration. The pedagogical verifier now includes a second independent contract layer for these exact-head findings.
