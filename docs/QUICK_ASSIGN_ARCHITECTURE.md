# Quick Assign architecture

Quick Assigns make existing applet machinery assignable without a second worksheet system, account, backend, or grading workflow. A teacher can ask learners to open a lab and complete a stable activity such as **QA-SEARCH-01**.

## Three assignment levels

- **Level 1 — Quick Assign:** a 10–15 minute activity inside an applet, focused on one mechanism and one controlled comparison. Learners use the applet's response surface and copy or print their work if submission is required.
- **Level 2 — Activity Pack:** a longer sequence of connected experiments. The current English-only pilots are [NN-1](https://lmdixon23.github.io/ai-playgrounds/activities/nn-1.html) and [CNN-1](https://lmdixon23.github.io/ai-playgrounds/activities/cnn-1.html).
- **Level 3 — Lesson / Unit Pack:** reserved for future resources; no released Level-3 package is implied.

## All fifteen active Quick Assigns

IDs are stable and are not silently reassigned. Each link below opens the corresponding classroom surface. The [Teacher Pack](https://lmdixon23.github.io/ai-playgrounds/teacher-pack.html) provides the same classroom entry points.

### [QA-SEARCH-01 · A* vs BFS: same goal, different work](https://lmdixon23.github.io/ai-playgrounds/playgrounds/search-pathfinding/index.html?mode=classroom#quick-assign-qa-search-01)

**Objective:** Compare frontier ordering, explored work, and shortest-path behavior for BFS and A* on the same maze.

**Teacher look-for:** A strong response distinguishes search work from path quality, connects the heuristic to frontier ordering, and avoids claiming that A* is always faster.

### [QA-LOCAL-01 · Why local search gets stuck or escapes](https://lmdixon23.github.io/ai-playgrounds/playgrounds/hill-climbing/index.html?mode=classroom#quick-assign-qa-local-01)

**Objective:** Compare one local-search trajectory or matched seeded restarts, separating reliability from final and best solution cost.

**Teacher look-for:** A strong response connects the acceptance rule to the trajectory, verifies equivalent starts and restart counts, and explains why success frequency and mean cost can rank algorithms differently.

### [QA-WUMPUS-01 · Safe, risky, or unknown?](https://lmdixon23.github.io/ai-playgrounds/playgrounds/wumpus-world/index.html?mode=classroom#quick-assign-qa-wumpus-01)

**Objective:** Use percept evidence to distinguish a square that is proven safe, possibly hazardous, or unresolved.

**Teacher look-for:** A strong response distinguishes unknown from dangerous, separates entailment from plausibility, and does not treat a probability estimate as proof of safety.

### [QA-SAT-01 · SAT, UNSAT, or entailed?](https://lmdixon23.github.io/ai-playgrounds/playgrounds/cnf-sat/index.html?mode=classroom#quick-assign-qa-sat-01)

**Objective:** Convert a knowledge base to CNF, inspect DPLL or CDCL evidence, and explain any learned clause and backjump without overclaiming solver fidelity.

**Teacher look-for:** A strong response distinguishes satisfiability from entailment, traces decisions and implication reasons, and justifies why a learned clause is valid and its non-chronological backjump level is safe.

### [QA-BAYES-01 · Base rates and false alarms](https://lmdixon23.github.io/ai-playgrounds/playgrounds/bayes-classifier/index.html?mode=classroom#quick-assign-qa-bayes-01)

**Objective:** Connect prior prevalence, true positives, false positives, and posterior probability.

**Teacher look-for:** A strong response explains why the posterior depends on both test quality and the prior/base rate, and does not equate accuracy or sensitivity with the probability of the condition after a positive result.

### [QA-BN-01 · Explaining away](https://lmdixon23.github.io/ai-playgrounds/playgrounds/bayes-network/index.html?mode=classroom#quick-assign-qa-bn-01)

**Objective:** Predict and explain how evidence for one cause can lower belief in another after conditioning on a common effect.

**Teacher look-for:** A strong response compares the before/after posterior and explains the common-effect dependence rather than saying one cause directly suppresses the other.

### [QA-KNN-01 · Which neighbors vote—or get averaged?](https://lmdixon23.github.io/ai-playgrounds/playgrounds/knn-classifier/index.html?mode=classroom#quick-assign-qa-knn-01)

**Objective:** Compare categorical voting with continuous-target averaging while holding neighbor selection and relevant controls constant.

**Teacher look-for:** A strong response identifies the actual nearest neighbors, separates selection from aggregation, and explains why classification votes over labels while regression computes a uniform or distance-weighted mean.

### [QA-OVERFIT-01 · Fit the training set, fail the future](https://lmdixon23.github.io/ai-playgrounds/playgrounds/overfitting/index.html?mode=classroom#quick-assign-qa-overfit-01)

**Objective:** Separate training error from validation/test behavior as model capacity changes.

**Teacher look-for:** A strong response identifies the point where additional capacity continues to improve training fit while held-out performance stops improving or worsens, and does not define overfitting as simply having a complex model.

### [QA-NN-01 · Why nonlinearity changes capacity](https://lmdixon23.github.io/ai-playgrounds/playgrounds/neural-network/index.html?mode=classroom#quick-assign-qa-nn-01)

**Objective:** Compare an affine-only network with a nonlinear representation and explain the decision-boundary change.

**Teacher look-for:** A strong response explains that stacking affine layers without a nonlinear activation remains affine, then connects nonlinearity to the network&#x27;s ability to represent a non-linear boundary.

### [QA-KMEANS-01 · Assign, move, repeat](https://lmdixon23.github.io/ai-playgrounds/playgrounds/kmeans/index.html?mode=classroom#quick-assign-qa-kmeans-01)

**Objective:** Predict one assignment and centroid update, then explain the alternating k-means cycle.

**Teacher look-for:** A strong response separates the assignment step from the centroid-update step, cites distances or membership evidence, and recognizes that initialization can change the final clustering.

### [QA-CNN-01 · One convolution cell](https://lmdixon23.github.io/ai-playgrounds/playgrounds/convolution/index.html?mode=classroom#quick-assign-qa-cnn-01)

**Objective:** Predict one output-cell multiply-and-sum before revealing the feature-map value.

**Teacher look-for:** A strong response matches kernel entries to the local image patch, performs or interprets the multiply-and-sum correctly, and distinguishes the filter response from a semantic object label.

### [QA-QL-01 · One Q-update](https://lmdixon23.github.io/ai-playgrounds/playgrounds/q-learning-gridworld/index.html?mode=classroom#quick-assign-qa-ql-01)

**Objective:** Predict an action, TD target, and update direction before stepping the learner.

**Teacher look-for:** A strong response connects reward, discounted next-state value, current Q-value, and learning rate to the update direction and distinguishes exploration from the learned policy.

### [QA-TRANSFORMER-01 · Attend, then predict](https://lmdixon23.github.io/ai-playgrounds/playgrounds/transformer-language-model/index.html?mode=classroom#quick-assign-qa-transformer-01)

**Objective:** Connect a controlled representation/attention change to the next-token probability distribution.

**Teacher look-for:** A strong response cites a specific attention/logit/probability change, distinguishes attention weights from a complete explanation of the prediction, and separates the probability distribution from the generation rule.

### [QA-AGENT-01 · A proposed call is not an executed action](https://lmdixon23.github.io/ai-playgrounds/playgrounds/agent-tool-context/index.html?mode=classroom#quick-assign-qa-agent-01)

**Objective:** Trace a proposed tool call through validation, authorization, execution, observation, and context update.

**Teacher look-for:** A strong response distinguishes model output, schema validity, authorization, execution, and observation, and identifies the exact gate where a denied or invalid action stops.

### [QA-MINIMAX-01 · Same answer, less search](https://lmdixon23.github.io/ai-playgrounds/playgrounds/minimax-alpha-beta/index.html?mode=classroom#quick-assign-qa-minimax-01)

**Objective:** Explain why a safe alpha-beta cutoff can reduce evaluated work without changing the minimax result.

**Teacher look-for:** A strong response uses the alpha/beta bound to justify why the skipped branch cannot improve the relevant decision and explicitly states that alpha-beta returns the same exact minimax value.

## Interaction contract

1. **Predict:** commit to a mechanism-specific expectation before the relevant result is revealed.
2. **Manipulate / run:** perform a bounded applet action or comparison using the same underlying mechanism.
3. **Observe:** record specific state evidence, not a generic impression.
4. **Explain:** connect the evidence to the target mechanism using course vocabulary.
5. **Transfer:** apply that explanation to a changed case or counterfactual.

Guided Challenge remains the stricter predict-before-reveal interaction where applicable; a Quick Assign can reuse it without replacing the experiment. Teacher look-for criteria describe evidence of reasoning, not a hidden answer key. Private keys or grading exemplars are not published on the student surface.

## State, language, and privacy

All fifteen Quick Assigns support English, Simplified Chinese, Vietnamese, and Spanish. Labels, prompts, packet headings, and required state must survive language changes without altering learner-authored responses. Fluent-reader naturalness remains a separate human-review question.

Responses remain in the learner's browser. Copying or printing a packet is controlled by the learner or teacher; the project does not receive it. Answers must not be put in analytics or share URLs. Copy or export work before clearing browser data or changing devices. See [Analytics and privacy](ANALYTICS_AND_PRIVACY.md).

Keyboard access, visible focus, clear reset/clear behavior, responsive containment, and text-equivalent results where practical are part of the [shared design contract](APPLET_DESIGN_SYSTEM_CONTRACT.md). These engineering requirements are not a claim of WCAG conformance.
