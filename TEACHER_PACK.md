# AI Playgrounds Teacher Pack

**Purpose.** This pack turns AI Playgrounds into ready-to-run classroom activities. The public suite contains **14 multilingual applets**: twelve Foundations/course-track labs plus two Modern AI extensions. It is designed for introductory AI, high school computer science, early undergraduate survey courses, teacher training, and self-study.

**Core claim.** Each applet is an offline-ready learning tool with no backend, no account system, no student-data storage, multilingual learner-facing support, scenario or prediction workflows, visual and text explanations, and keyboard support. Labs 13 and 14 are generated as self-contained public HTML artifacts from frozen deterministic sources. Two v1.5.1 Activity Pack canaries add ready-to-assign student worksheets without publishing teacher answer keys.

## Quick start

1. Choose one applet from the map below.
2. For a short lesson, use the applet's built-in Guided Challenge or student response packet.
3. For a full inquiry lesson, use an Activity Pack when one is available.
4. Ask students to predict before revealing the result.
5. Have students run one controlled comparison and record what changed.
6. Require an explanation using course vocabulary and one transfer/counterfactual response.
7. Students copy, print, or submit their work through your normal classroom system.

## Ready-to-assign Activity Packs

The v1.5.1 pilot includes two public **student-facing** activities. Responses autosave locally in the learner's browser and can be printed or saved as PDF. AI Playgrounds does not receive worksheet answers.

| ID | Applet | Time | Core inquiry | Student link |
|---|---|---:|---|---|
| **NN-1** | Tiny Neural Network | 35–45 min | Make a network fail, then add the mechanism/capacity needed to succeed; connect loss and train/test behavior to what changed. | [Open NN-1](activities/nn-1.html) |
| **CNN-1** | Convolution Playground | 40–50 min | Compute one convolution by hand, connect it to the visual scan, then investigate directional edges, learned filters, and pooling. | [Open CNN-1](activities/cnn-1.html) |

The activity architecture is **predict → run → observe → explain → transfer**. It deliberately treats a well-reasoned wrong prediction as useful evidence rather than rewarding answer guessing.

**Teacher-answer boundary:** public Activity Pack pages do not contain answer keys or grading exemplars. Keep private teacher solutions outside the deployed student site if students should not be able to inspect them.

## Fast classroom routes

### 20-minute route

Use one flagship applet. Keep the task narrow.

1. 2 minutes: teacher frames the misconception.
2. 3 minutes: students predict.
3. 7 minutes: students apply one scenario or controlled comparison.
4. 5 minutes: students complete Observe and Explain.
5. 3 minutes: exit ticket.

Recommended applets: Pathfinding, Bayes Rule, Overfitting, or K-Means.

### 45-minute route

Use the applet as a structured inquiry lab.

1. 5 minutes: warm-up prediction.
2. 8 minutes: lesson tour or first guided task.
3. 15 minutes: controlled exploration or Activity Pack experiments.
4. 10 minutes: student explanation/reflection.
5. 7 minutes: pair discussion or written transfer.

Recommended applets: Bayesian Network, Hill Climbing and Simulated Annealing, Tiny Neural Network, Q-Learning Gridworld, Wumpus World, or one of the Activity Pack canaries.

### Homework route

1. Students open the assigned applet or Activity Pack.
2. Students run one named scenario or activity experiment.
3. Students complete Predict, Observe, Explain, and Transfer.
4. Students copy/print their local work if required.
5. Students submit through the class learning-management system.

## Foundations / course-track applet map

These twelve labs form the primary introductory course path.

| Applet | Concept | Time | Learning objective | Core question |
| --- | --- | --- | --- | --- |
| [Pathfinding Visualizer](playgrounds/search-pathfinding/index.html) | Search | 20 min | Compare uninformed and informed search while watching the frontier, explored set, and final path change. | Why does A* usually expand fewer nodes than BFS when the heuristic is useful? |
| [Hill Climbing and Simulated Annealing](playgrounds/hill-climbing/index.html) | Local search | 30 min | Compare greedy improvement with search strategies that sometimes accept worse moves. | When can a worse local step produce a better final result? |
| [Wumpus World](playgrounds/wumpus-world/index.html) | Logical agent | 25 min | Distinguish perception, inference, belief, and safe action in a logical-agent environment. | What is the difference between an unknown square and a square proven safe? |
| [CNF and SAT Builder](playgrounds/cnf-sat/index.html) | Logic and knowledge bases | 25 min | Rewrite propositional formulas into CNF and inspect DPLL branch/prune structure. | Why does DPLL avoid exploring every complete assignment? |
| [Bayes Rule Playground](playgrounds/bayes-classifier/index.html) | Probability | 20 min | Connect prior probability, sensitivity, specificity, and posterior probability. | Why can a highly accurate test still produce many false alarms when the event is rare? |
| [Bayesian Network](playgrounds/bayes-network/index.html) | Bayesian networks | 30 min | Read conditional dependence, enter evidence, and observe explaining-away behavior. | Why can evidence for one possible cause lower belief in another? |
| [K-Nearest Neighbors](playgrounds/knn-classifier/index.html) | Supervised learning | 20 min | Show how k, distance, and neighborhood voting shape a decision boundary. | What does k control, and why can both small and large k fail? |
| [Overfitting Explorer](playgrounds/overfitting/index.html) | Evaluation | 25 min | Separate training error from test error and explain why model capacity changes generalization. | Why does a model that fits the training data perfectly sometimes fail on new data? |
| [Tiny Neural Network](playgrounds/neural-network/index.html) | Neural networks | 30 min | Connect features, hidden units, activation functions, training, and decision regions. | How do layers and nonlinearity change what a classifier can separate? |
| [K-Means Clustering](playgrounds/kmeans/index.html) | Unsupervised learning | 20 min | Step through assignment and centroid update cycles until clusters stabilize. | What changes during each iteration, and when should the algorithm stop? |
| [Convolution Playground](playgrounds/convolution/index.html) | Vision | 25 min | Apply a 3×3 filter, interpret feature maps, and connect hand-built kernels to learned filters. | Why can a small matrix reveal edges, blur, or sharpen an image? |
| [Q-Learning Gridworld](playgrounds/q-learning-gridworld/index.html) | Reinforcement learning | 30 min | Trace how rewards, exploration, and Bellman-style updates shape values and policy. | How does useful behavior emerge from repeated trial and error? |

## Modern AI extensions

These two labs are optional extensions rather than prerequisites for the Foundations sequence.

| Applet | Concept | Time | Learning objective | Core question |
|---|---|---:|---|---|
| [Transformer Language Modeling](playgrounds/transformer-language-model/index.html) | Modern NLP / Transformers | 30–40 min | Connect token/position representation, causal self-attention, logits, temperature, and next-token probabilities without treating attention as general reasoning explanation. | How can changing representation or attention state change the next-token distribution? |
| [Agent Tool Use and Context Protocols](playgrounds/agent-tool-context/index.html) | Agent systems | 30–40 min | Distinguish model text, structured calls, validation, authorization, execution, observations, provenance-aware context updates, and stopping. | What has to happen between a proposed tool call and a legitimate external action? |

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
| 3 | CNF and SAT Builder | Formalizes logic and solver search |
| 4 | Bayes Rule | Introduces uncertainty and evidence |
| 5 | Bayesian Network | Extends probability to structured dependence |
| 6 | KNN and Overfitting | Introduces supervised learning and model evaluation |
| 7 | K-Means Clustering and Tiny Neural Network | Contrasts unsupervised structure with learned decision surfaces |
| 8 | Convolution and Q-Learning | Connects perception and action-oriented learning |

After this sequence, Transformer Language Modeling can be used as an advanced NLP extension and Agent Tool Use as a modern systems extension.

## Student submission expectations

A complete student response should include:

1. the applet/activity name,
2. the scenario or experiment used,
3. a prediction made before running/revealing,
4. one specific observation from the applet state,
5. one explanation using course vocabulary,
6. one transfer or counterfactual answer.

## Assessment options

| Level | Evidence |
|---|---|
| Complete | Student predicts, observes, explains, and transfers with applet-specific evidence |
| Developing | Student completes the fields but gives mostly description rather than explanation |
| Incomplete | Student omits prediction, explanation, transfer, or applet evidence |

## Classroom privacy and data handling

AI Playgrounds has no backend and no student account system. Built-in response packets and Activity Pack draft responses stay in the local browser. Students decide whether to copy, print, or submit their own response through a separate classroom system. The site does not collect student names, IDs, grades, submissions, or classroom rosters.

The canonical GitHub Pages site may send privacy-minimized aggregate requests to estimate public interest. The wrapper honors Global Privacy Control and Do Not Track; classroom users can add `?analytics=off` or use the persistent opt-out control. Downloaded/offline copies send no project analytics. Worksheet answers and experiment state are not included in analytics requests.

## Accessibility and inclusion notes

The applets include visible focus treatment, reduced-motion support, keyboard guidance, text-state descriptions, and ARIA/live-state patterns where appropriate. v1.5.1 also adds a targeted state/recovery QA contract plus mobile-landscape, text-enlargement, dense-touch, and localized-component checks. These automated safeguards do not constitute accessibility conformance or replace testing with assistive-technology users. For assessment, provide a non-visual written explanation route whenever the visual layer is not the best fit.

## Reuse and licensing

The suite is MIT licensed. Teachers may link, fork, embed, print, adapt, and remix the materials for classroom use. Each public applet is deployable as an offline-ready HTML artifact; Activity Packs are ordinary printable HTML pages with local-only response storage.

## Launch safety note

No backend. Student work remains local unless the teacher asks students to submit it through a separate classroom system.
