# AI Playgrounds Curriculum Map

The current public suite contains **15 learner applets: 13 Foundations/course-track labs plus 2 Modern AI extensions**.

The suite supports two orders:

1. **Foundations / course sequence:** preserves conceptual dependencies and follows the broad progression from search to logic, probability, machine learning, reinforcement learning, and adversarial search.
2. **Quick-entry sampler:** optimized for a first visit or short four-lesson introduction. It is not the full course order.

The learner applets support English, Simplified Chinese, Vietnamese, and Spanish. The current curriculum/navigation support page has a narrower EN/ZH boundary; do not infer four-language support for every support page from the applet localization boundary.

## Beginning-of-course Quick Assigns

These Level-1 activities take about 10-15 minutes and reuse each applet's existing Guided Challenge and local response packet.

| Stable ID | Applet | Focus |
|---|---|---|
| `QA-SEARCH-01` | [Pathfinding](playgrounds/search-pathfinding/index.html?mode=classroom#quick-assign-qa-search-01) | A* vs BFS: distinguish path quality from search work |
| `QA-LOCAL-01` | [Hill Climbing / Simulated Annealing](playgrounds/hill-climbing/index.html?mode=classroom#quick-assign-qa-local-01) | Explain how local-search acceptance shapes the cost trajectory and when escape mechanisms can help |
| `QA-WUMPUS-01` | [Wumpus World](playgrounds/wumpus-world/index.html?mode=classroom#quick-assign-qa-wumpus-01) | Distinguish safe, hazardous, and unresolved states from percept evidence |
| `QA-SAT-01` | [CNF/SAT](playgrounds/cnf-sat/index.html?mode=classroom#quick-assign-qa-sat-01) | Distinguish SAT/UNSAT/entailment and explain concrete CNF/DPLL or resolution evidence |

The remaining eleven Level-1 IDs are reserved in `tools/quick_assigns_v1.json` but are not advertised until their individual activity contracts pass.

## Quick-entry sampler

1. Pathfinding
2. Bayes Rule
3. Overfitting
4. Q-Learning

## Foundations / course-track sequence

| # | Applet | Concept area | Why here |
|---:|---|---|---|
| 1 | [Pathfinding Visualizer](playgrounds/search-pathfinding/index.html) | Search and problem solving | Introduce controlled exploration, optimality, and heuristic focus. |
| 2 | [Hill Climbing and Simulated Annealing](playgrounds/hill-climbing/index.html) | Search and optimization | Show why local improvement can stall and why escape strategies matter. |
| 3 | [Wumpus World](playgrounds/wumpus-world/index.html) | Logic and knowledge | Bridge perception, inference, uncertainty, and safe action. |
| 4 | [CNF and SAT Builder](playgrounds/cnf-sat/index.html) | Logic and knowledge | Formalize propositional reasoning and search over assignments. |
| 5 | [Bayes Rule Playground](playgrounds/bayes-classifier/index.html) | Probability | Surface base-rate neglect before moving to graphical models. |
| 6 | [Bayesian Network](playgrounds/bayes-network/index.html) | Probabilistic reasoning | Extend conditional probability into dependence and explaining away. |
| 7 | [K-Nearest Neighbors](playgrounds/knn-classifier/index.html) | Machine learning | Introduce supervised classification through visible neighborhood votes. |
| 8 | [Overfitting Explorer](playgrounds/overfitting/index.html) | Machine learning and evaluation | Separate training performance from generalization on new data. |
| 9 | [Tiny Neural Network](playgrounds/neural-network/index.html) | Neural networks | Build intuition for hidden representations and nonlinearity. |
| 10 | [K-Means Clustering](playgrounds/kmeans/index.html) | Unsupervised learning | Introduce iterative unsupervised clustering and initialization sensitivity. |
| 11 | [Convolution Playground](playgrounds/convolution/index.html) | Computer vision | Connect local filters to feature maps and learned visual representations. |
| 12 | [Q-Learning Gridworld](playgrounds/q-learning-gridworld/index.html) | Reinforcement learning | Develop trial-and-error learning, delayed reward, and policy emergence. |
| 13 | [Game Trees: Minimax and Alpha-Beta Pruning](playgrounds/minimax-alpha-beta/index.html) | Adversarial search | Extend search to an optimal opponent and separate exact minimax result from search work. |

## Modern AI extensions

These are optional modern/boundary extensions rather than prerequisites for the Foundations sequence.

| Applet | Concept area | Why here |
|---|---|---|
| [Transformer Language Modeling](playgrounds/transformer-language-model/index.html) | Generative language models | Connect token representation, causal self-attention, logits, temperature, and next-token probabilities after earlier neural-network foundations. |
| [Agent Tool Use and Context Protocols](playgrounds/agent-tool-context/index.html) | Modern AI systems | Separate model text, structured tool calls, validation, authorization, execution, observations, context updates, and stopping. |

## Assignment levels

- **Level 1 - Quick Assign:** 10-15 minutes, inside the applet, one controlled mechanism task.
- **Level 2 - Activity Pack:** roughly 30-50 minutes, separate student activity page; current canaries are `NN-1` and `CNN-1`.
- **Level 3 - Lesson / Unit Pack:** reserved for future longer teacher packages; none is implied to exist yet.

All levels use the same inquiry spine where appropriate: **predict -> run -> observe -> explain -> transfer**.

## Why the orders differ

The quick-entry sampler maximizes contrast and first-visit impact. The Foundations sequence preserves prerequisite development and should be used for sustained instruction. Modern extensions are intentionally separated so contemporary systems do not displace the classical introductory-AI spine.

## Visual identity

Each applet keeps the same accent color across the landing page, curriculum map, and Teacher Pack.
