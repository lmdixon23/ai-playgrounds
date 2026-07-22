# AI Playgrounds Teacher Pack

**Purpose.** This pack turns the 12 AI Playgrounds applets into ready-to-run classroom activities. It is designed for introductory AI, high school computer science, early undergraduate survey courses, teacher training, and self-study.

**Core claim.** Each applet is a single-file HTML learning tool with no backend, no account system, no student-data storage, bilingual interface support, scenario gallery, visual explanation, text and keyboard support, and student response packet.

## Quick start

1. Choose one applet from the table below.
2. Give students the student lab packet template or use the built-in student response packet.
3. Ask students to predict before changing the applet.
4. Have students run one scenario from the scenario gallery.
5. Have students write one observation, one explanation, and one transfer answer.
6. Students copy or print their local packet and submit it through your normal classroom system.

## Fast classroom routes

### 20-minute route

Use one flagship applet. Keep the task narrow.

1. 2 minutes: teacher frames the misconception.
2. 3 minutes: students predict.
3. 7 minutes: students apply one scenario gallery case.
4. 5 minutes: students complete Observe and Explain.
5. 3 minutes: exit ticket.

Recommended applets: Pathfinding, Bayes Rule, Overfitting, or K-Means.

### 45-minute route

Use the applet as a structured inquiry lab.

1. 5 minutes: warm-up prediction.
2. 8 minutes: lesson tour.
3. 15 minutes: scenario gallery exploration.
4. 10 minutes: student response packet response.
5. 7 minutes: pair discussion or written transfer.

Recommended applets: Bayesian Network, Hill Climbing and Simulated Annealing, Tiny Neural Network, Q-Learning Gridworld, or Wumpus World.

### Homework route

Use the built-in local lab packet.

1. Students open the assigned applet.
2. Students run one named scenario gallery case.
3. Students complete Predict, Observe, Explain, and Transfer.
4. Students copy or print their packet.
5. Students submit through the class learning-management system.

## Applet map

| Applet | Concept | Time | Learning objective | Core question |
| --- | --- | --- | --- | --- |
| [Pathfinding Visualizer](playgrounds/search-pathfinding/index.html) | Search | 20 min | Compare uninformed and informed search while watching the frontier, explored set, and final path change. | Why does A* usually expand fewer nodes than BFS when the heuristic is useful? |
| [Bayes Rule Playground](playgrounds/bayes-classifier/index.html) | Probability | 20 min | Connect prior probability, sensitivity, specificity, and posterior probability. | Why can a highly accurate test still produce many false alarms when the event is rare? |
| [Overfitting Explorer](playgrounds/overfitting/index.html) | Evaluation | 25 min | Separate training error from test error and explain why model capacity changes generalization. | Why does a model that fits the training data perfectly sometimes fail on new data? |
| [Q-Learning Gridworld](playgrounds/q-learning-gridworld/index.html) | Reinforcement learning | 30 min | Trace how rewards, exploration, and Bellman-style updates shape a value function and policy. | How does useful behavior emerge from repeated trial and error? |
| [Wumpus World](playgrounds/wumpus-world/index.html) | Logical agent | 25 min | Distinguish perception, inference, belief, and safe action in a logical-agent environment. | What is the difference between an unknown square and a square proven safe? |
| [CNF and SAT Builder](playgrounds/cnf-sat/index.html) | Logic and knowledge bases | 25 min | Rewrite propositional formulas into CNF and inspect why satisfiability solving prefers that form. | Why do solvers prefer a standardized clause structure before search begins? |
| [Bayesian Network](playgrounds/bayes-network/index.html) | Bayesian networks | 30 min | Read conditional dependence, enter evidence, and observe explaining-away behavior. | Why can one possible cause lower belief in another possible cause? |
| [K-Nearest Neighbors](playgrounds/knn-classifier/index.html) | Supervised learning | 20 min | Show how k, distance, and neighborhood voting shape a decision boundary. | What does k control, and why can both small and large k fail? |
| [Hill Climbing and Simulated Annealing](playgrounds/hill-climbing/index.html) | Local search | 30 min | Compare greedy improvement with search strategies that sometimes accept worse moves. | When can a worse local step produce a better final result? |
| [Tiny Neural Network](playgrounds/neural-network/index.html) | Neural networks | 30 min | Connect features, hidden units, activation functions, and decision regions. | How do layers and nonlinearity change what a classifier can separate? |
| [K-Means Clustering](playgrounds/kmeans/index.html) | Unsupervised learning | 20 min | Step through assignment and centroid update cycles until clusters stabilize. | What changes during each iteration, and when should the algorithm stop? |
| [Convolution Playground](playgrounds/convolution/index.html) | Vision | 25 min | Apply a 3 by 3 filter, interpret feature maps, and connect hand-built kernels to learned filters. | Why can a small matrix reveal edges, blur, or sharpen an image? |

## Suggested 4-lesson mini-unit

| Lesson | Applet | Focus | Student product |
|---|---|---|---|
| 1 | Pathfinding | Search as controlled exploration | Compare two algorithms and explain the frontier |
| 2 | Bayes Rule | Evidence, base rates, and posterior belief | Explain one base-rate trap |
| 3 | Overfitting | Model capacity and generalization | Identify underfit, reasonable fit, and overfit |
| 4 | Q-Learning | Reward, exploration, and value propagation | Explain how policy emerges from repeated updates |

## Suggested 8-lesson sequence

| Lesson | Applet | Role in sequence |
|---|---|---|
| 1 | Pathfinding | Introduces search and state spaces |
| 2 | Wumpus World | Adds perception and logical inference |
| 3 | CNF and SAT Builder | Formalizes logic into solver-friendly structure |
| 4 | Bayes Rule | Introduces uncertainty and evidence |
| 5 | Bayesian Network | Extends probability to structured dependence |
| 6 | KNN and Overfitting | Introduces supervised learning and model evaluation |
| 7 | K-Means Clustering and Tiny Neural Network | Contrasts unsupervised structure with learned decision surfaces |
| 8 | Convolution and Q-Learning | Connects perception and action-oriented learning |

## Student submission expectations

A complete student response should include:

1. the applet name,
2. the scenario used,
3. a prediction made before running,
4. one observation from the applet state,
5. one explanation using course vocabulary,
6. one transfer answer that applies the idea to a new case.

## Assessment options

| Level | Evidence |
|---|---|
| Complete | Student predicts, observes, explains, and transfers with applet-specific evidence |
| Developing | Student completes the fields but gives mostly description rather than explanation |
| Incomplete | Student omits prediction, explanation, transfer, or applet evidence |

## Classroom privacy and data handling

AI Playgrounds has no backend and no student account system. student response packet stores draft text only in the local browser. Students decide whether to copy or print their own response. The site does not collect student names, student IDs, grades, submissions, or classroom rosters.

The public GitHub Pages site may load privacy-light analytics on the canonical host to estimate uptake. Classroom users can add `?noanalytics=1` to the URL to disable analytics for that session.

## Accessibility and inclusion notes

Each applet includes a skip link, visible focus states, reduced-motion CSS, an text and keyboard support, and ARIA live status. This supports keyboard and screen-reader pathways, but it does not replace a full human accessibility audit. For assessment, give students a non-visual written explanation option whenever the visual layer is not the best fit.

## Reuse and licensing

The suite is MIT licensed. Teachers may link, fork, embed, print, adapt, and remix the materials for classroom use. Each applet is a standalone HTML file, so a teacher can copy one applet into a learning-management system or static site without running a build process.


## Launch safety note

No backend. Student work remains local unless the teacher asks students to submit it through a separate classroom system.
