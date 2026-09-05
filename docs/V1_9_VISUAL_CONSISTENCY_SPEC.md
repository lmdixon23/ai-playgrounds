# AI Playgrounds v1.9 Visual Consistency Specification

Status: planning baseline

Parent plan: `docs/V1_9_PRODUCT_COHERENCE_AND_HUMAN_VALIDATION_PLAN.md`

Owner workstream: #48

## 1. Governing rule

Treat all fifteen labs as one product.

Standardize everything a learner or educator should not have to relearn from lab to lab.

Preserve differences that are necessary to expose the actual AI mechanism.

Visual consistency is not pixel identity. A mechanism specific visualization may differ substantially from another lab while still using the same product shell, spacing system, typography roles, accessibility contract, action hierarchy, semantic state grammar, responsive rules, and provenance structure.

## 2. Universal primitives

Unless a documented mechanism or accessibility exception exists, all applicable labs should converge on:

- page width and horizontal gutters;
- header composition and height;
- theme control;
- locale control;
- Share, Embed, local export, and Reset order;
- typography roles;
- spacing scale;
- border radius families;
- ordinary control heights;
- focus indicator;
- semantic information, success, warning, error, selected, and disabled treatment;
- featured experiment structure;
- scenario card structure;
- Quick Assign placement and disclosure pattern;
- key term structure;
- explanation hierarchy and readable text width;
- accessibility/help disclosure;
- provenance/footer treatment;
- responsive collapse order;
- dark theme contract;
- locale state preservation;
- shareable state conventions;
- local response persistence;
- privacy bounded analytics.

## 3. Mechanism specific surfaces

The following are not forced into identical geometry:

- graph, grid, tree, network, matrix, chart, and canvas structures;
- algorithm specific controls;
- trace and timeline representations;
- concept specific metrics;
- state transition animations;
- visual encodings whose geometry is itself part of the explanation.

Mechanism specific does not exempt a surface from keyboard, focus, contrast, non color state cues, text equivalent state, responsive containment, locale, or theme requirements.

## 4. Lab by lab invariants

### Search and Pathfinding

Preserve:

- grid as the dominant mechanism surface;
- distinct start, goal, obstacle, frontier or explored, and final path states;
- stepwise search trace;
- algorithm or heuristic comparison where supported.

Standardize:

- controls surrounding the grid;
- run, step, and reset hierarchy;
- legend treatment;
- text state explanation;
- comparison metric cards;
- scenario and Quick Assign placement.

Do not replace the grid with a generic chart merely to match other labs.

### Hill Climbing and Simulated Annealing

Preserve:

- optimization landscape and current versus best state relation;
- local move trajectory;
- local optimum behavior;
- temperature or acceptance behavior;
- repeated restart benchmark and reproducibility information.

Standardize:

- algorithm selector and parameter grouping;
- run and benchmark actions;
- result metric cards;
- seed and state presentation;
- scenario and explanation treatment.

Single run and benchmark modes must remain visually distinguishable.

### Wumpus World

Preserve:

- spatial world structure;
- agent location and orientation where represented;
- percept and hazard distinctions;
- known information versus hidden world facts;
- action progression.

Standardize:

- action controls;
- percept and status panels;
- legend;
- state explanation;
- reset and scenario entry.

Do not reveal hidden facts by default in a way that invalidates the inference task.

### CNF and SAT

Preserve:

- formula and clause representation;
- DPLL branch and prune trace;
- CDCL decisions, propagations, conflicts, learned clauses, and backjump relation;
- distinction between original and learned clauses.

Standardize:

- mode selector;
- formula input treatment;
- trace card framing;
- decision, propagation, conflict, and learned state grammar;
- control/reset hierarchy;
- text equivalent trace.

DPLL and CDCL need not share identical internal geometry if doing so would blur their different mechanisms.

### Bayes Rule

Preserve:

- prior, likelihood/evidence, and posterior relationship;
- conditional probability comparison;
- numeric and visual probability representation;
- one input change producing a visible posterior change.

Standardize:

- probability controls;
- percentage and decimal formatting rules;
- result hierarchy;
- equation placement;
- scenario and Quick Assign structure.

Avoid animation that suggests probability physically flows through the interface.

### Bayesian Networks

Preserve:

- directed acyclic graph geometry;
- node evidence states;
- exact versus sampled inference distinction where applicable;
- previous/current posterior comparison;
- conditional dependence and explaining away relations.

Standardize:

- evidence controls;
- node status treatment;
- posterior cards;
- previous/current comparison styling;
- legend, scenario, and explanation hierarchy.

Arrows represent conditional structure, not physical movement of probability.

### K Nearest Neighbors

Preserve:

- feature space/scatter visualization;
- query point and selected neighbors;
- classification versus regression distinction;
- distance or weighting contributions;
- decision or prediction result;
- regression evaluation metrics where present.

Standardize:

- task mode selector;
- k control;
- distance/weight selectors;
- neighbor highlight grammar;
- result metric cards;
- keyboard/touch equivalent for hover information.

### Overfitting and Model Complexity

Preserve:

- training versus test/generalization comparison;
- model curve and data relationship;
- complexity and regularization manipulation;
- underfit, appropriate fit, and overfit states;
- baseline/current comparison where supported.

Standardize:

- parameter controls;
- train/test legend and metric cards;
- comparison panel;
- scenario and explanation layout.

Visual emphasis must not imply that the most complex model is inherently best.

### Tiny Neural Network

Preserve:

- network topology;
- activations, weights, or learning signal where inspectable;
- forward/training progression;
- loss/error relation;
- training versus generalization distinction when present.

Standardize:

- training controls;
- epoch/step actions;
- metric cards;
- topology legend;
- history chart framing;
- reset/recovery pattern.

Animation speed must not be presented as hardware or runtime performance evidence.

### K Means Clustering

Preserve:

- point cloud and centroid geometry;
- assignment versus update iteration;
- cluster membership and center movement;
- convergence state;
- inertia/silhouette comparison where supported;
- initialization sensitivity.

Standardize:

- k selector;
- initialization controls;
- assignment, update, and automatic run hierarchy;
- centroid/cluster legend;
- comparison metric cards.

Cluster identity must not depend on color alone.

### Convolution

Preserve:

- input grid or image;
- kernel/filter;
- local receptive field;
- multiply accumulate relation;
- output feature map;
- pooling relation where present.

Standardize:

- kernel controls;
- step/run actions;
- input, kernel, and output panel framing;
- active cell highlight semantics;
- numeric equation and explanation treatment.

Spatial correspondence among input patch, kernel, and output cell is concept defining and may require a unique multi panel layout.

### Q Learning Gridworld

Preserve:

- environment grid;
- current state/action/reward transition;
- Q value or policy representation;
- episode progression;
- exploration versus exploitation relation;
- value propagation through learning.

Standardize:

- episode and step controls;
- epsilon and learning controls;
- reward/state legend;
- metric/history cards;
- scenario and Quick Assign placement.

Rapid animation cannot substitute for inspectable update steps.

### Game Trees, Minimax, and Alpha Beta

Preserve:

- tree geometry;
- MAX versus MIN levels;
- terminal utilities;
- backed up values;
- evaluated versus pruned nodes;
- exact minimax result despite pruning;
- move order comparison.

Standardize:

- algorithm/mode controls;
- terminal value editing;
- run, step, and reset hierarchy;
- visited, returned, and pruned state grammar;
- comparison metric cards;
- responsive tree containment.

Pruned nodes remain visible as not evaluated rather than disappearing from the conceptual tree.

### Transformer Language Modeling

Preserve:

- token sequence;
- representation and position relation;
- Q, K, V and attention computation;
- causal mask;
- weighted value relation;
- logits and next token probabilities;
- temperature, top k, and deterministic/stochastic decoding distinctions;
- baseline/current comparison where supported.

Standardize:

- control grouping;
- staged mechanism navigation;
- matrix/table framing;
- warning and fidelity panels;
- scenario actions;
- probability result cards;
- text equivalent numeric state.

Attention is not presented as a general explanation of reasoning. Brighter attention must not imply causal importance beyond the model relation being displayed.

### Agent Tool Use and Context Protocols

Preserve:

- separation among model text, structured call, validation, authorization, execution, observation, context update, and stop;
- gate failure states;
- structured action packet;
- provenance aware context delta;
- learner selected sandbox action versus model selected action;
- simulated world boundary.

Standardize:

- stage card geometry;
- valid, authorized, executed, and observed state grammar;
- action controls;
- error/recovery surfaces;
- scenario and Quick Assign structure;
- fidelity/provenance disclosure.

Validation must not look equivalent to authorization, and authorization must not look equivalent to execution. Simulated actions remain visibly simulated.

## 5. Cross lab disposition matrix

Every lab receives one of four values for each dimension: canonical, mechanism exception, not applicable, or defect.

| Dimension | Default |
| --- | --- |
| Header height and order | canonical |
| Theme control | canonical |
| Locale control | canonical |
| Share action | canonical |
| Embed action | canonical |
| Local export | canonical |
| Reset action | canonical |
| Page gutter | canonical |
| Body typography | canonical |
| Section heading typography | canonical |
| Control height | canonical |
| Focus indicator | canonical |
| Scenario card structure | canonical |
| Featured experiment structure | canonical |
| Quick Assign placement | canonical |
| Key term structure | canonical |
| Explanation reading width | canonical |
| Accessibility disclosure | canonical |
| Footer and provenance | canonical |
| Dark theme semantics | canonical |
| Semantic state grammar | canonical when meanings overlap |
| Main visualization geometry | mechanism exception |
| Algorithm specific controls | mechanism exception |
| Trace or timeline geometry | mechanism exception |
| Concept specific metrics | mechanism exception |
| State transition animation | mechanism exception |

A mechanism exception requires a short documented reason. Not applicable is allowed only when the underlying learner function genuinely does not exist.

## 6. Screenshot census

For every lab capture at minimum:

1. desktop light fresh state;
2. desktop dark fresh state;
3. phone portrait light fresh state;
4. phone portrait dark fresh state;
5. one long translated locale;
6. one active mechanism state;
7. Quick Assign open where applicable.

Add tablet, split view, and enlarged text captures where they expose a real boundary.

The census should produce both individual images and a generated contact sheet for direct whole suite comparison.

## 7. Visual regression rules

Use a fixed browser, operating system, font environment, viewport, theme, locale, and deterministic state.

Baseline stable structural surfaces and mask or normalize expected volatile mechanism areas.

Disable animations, transitions, and caret noise during capture.

Every failed visual comparison should retain expected, actual, and diff artifacts.

Baseline changes require review. CI must never update snapshots automatically to obtain a pass.

Visual comparisons supplement semantic and browser assertions; they never replace them.

## 8. Acceptance condition

The visual consistency workstream closes only when:

- all fifteen labs are represented in the census;
- every universal primitive either matches the canonical contract or has a defect recorded;
- every mechanism exception has an explicit reason;
- no unexplained shell discrepancy remains;
- dark theme and translated states are represented;
- visual baselines are deterministic in the canonical CI environment;
- visual uniformity has not changed algorithm meaning or hidden mechanism specific information.