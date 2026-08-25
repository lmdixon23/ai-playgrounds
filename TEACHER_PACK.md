# AI Playgrounds Teacher Pack

**Purpose.** This pack turns AI Playgrounds into ready-to-run classroom activities. The current suite contains **15 learner applets: 13 Foundations/course-track labs plus 2 Modern AI extensions**. It is designed for introductory AI, high-school computer science, early undergraduate survey courses, teacher training, and self-study.

**Language scope.** All 15 learner applets support English, Simplified Chinese, Vietnamese, and Spanish. This Teacher Pack and the current curriculum/navigation support pages use English and Simplified Chinese; the NN-1/CNN-1 Activity Pack pilot is English-only. Do not infer site-wide four-language coverage from the applet boundary.

**Core claim.** Each applet is an offline-ready learning tool with no backend, no account system, no student-data storage, scenario/prediction workflows, visual and text explanations, and keyboard-oriented support. The current software-verification stack establishes tested implementation behavior, not learning gains or accessibility conformance.

## Assignment levels

### Level 1 - Quick Assign · 10-15 min

Quick Assigns reuse the applet's existing Guided Challenge and local Student response packet. Students complete one bounded mechanism task using:

**predict -> run/manipulate -> observe -> explain -> transfer**

Use the stable ID when assigning work. Student writing stays local unless the student copies, prints, or submits it through the teacher's normal classroom system.

| ID | Applet | Core task | Teacher look-for | Student link |
|---|---|---|---|---|
| **QA-SEARCH-01** | Pathfinding | Compare A* and BFS on the same maze | Distinguishes search work from path quality; connects the heuristic to frontier ordering; avoids “A* is always faster.” | [Open QA-SEARCH-01](playgrounds/search-pathfinding/index.html?mode=classroom#quick-assign-qa-search-01) |
| **QA-LOCAL-01** | Hill Climbing / Simulated Annealing | Explain how a local-search acceptance rule shapes the cost trajectory and when escape mechanisms can help | Connects accepted or rejected neighboring moves to the trajectory; distinguishes local from global optimality; explains when restart or annealing can change the outcome. | [Open QA-LOCAL-01](playgrounds/hill-climbing/index.html?mode=classroom#quick-assign-qa-local-01) |
| **QA-WUMPUS-01** | Wumpus World | Classify a state/action as safe, risky, or unresolved from percept evidence | Distinguishes unknown from dangerous and entailment from plausibility; probability does not prove safety. | [Open QA-WUMPUS-01](playgrounds/wumpus-world/index.html?mode=classroom#quick-assign-qa-wumpus-01) |
| **QA-SAT-01** | CNF/SAT | Classify SAT/UNSAT/entailment, inspect CNF/DPLL or resolution evidence, and explain what it establishes | Distinguishes satisfiability from entailment; cites a concrete CNF/DPLL or resolution result; explains what the evidence establishes without overclaiming. | [Open QA-SAT-01](playgrounds/cnf-sat/index.html?mode=classroom#quick-assign-qa-sat-01) |

The remaining eleven Level-1 IDs are reserved in `tools/quick_assigns_v1.json` so the naming system stays stable, but they are not advertised until their individual activity contracts pass.

### Level 2 - Activity Pack · roughly 30-50 min

The current pilot includes two public student-facing Activity Packs. Responses autosave locally and can be printed or saved as PDF.

| ID | Applet | Time | Core inquiry | Student link |
|---|---|---:|---|---|
| **NN-1** | Tiny Neural Network | 35-45 min | Make a network fail, then add the mechanism/capacity needed to succeed; connect loss and train/test behavior to what changed. | [Open NN-1](activities/nn-1.html) |
| **CNN-1** | Convolution Playground | 40-50 min | Compute one convolution by hand, connect it to the visual scan, then investigate directional edges, learned filters, and pooling. | [Open CNN-1](activities/cnn-1.html) |

**Teacher-answer boundary:** public Activity Packs do not contain private answer keys or grading exemplars. Keep genuinely secret teacher solutions outside the deployed student site.

### Level 3 - Lesson / Unit Pack

Reserved for future longer teacher packages. A Level 3 package may include prerequisites, warm-up, a longer sequence, rubric guidance, extension work, and private teacher materials. No Level 3 package is implied to exist yet.

## Quick start

1. Choose one applet from the map below.
2. For a 10-15 minute assignment, give students one stable Quick Assign ID.
3. For a full inquiry lesson, use an Activity Pack when available.
4. Require a prediction before the relevant reveal/run where the task supports it.
5. Require one specific observation from applet state, not a generic impression.
6. Require an explanation using course vocabulary and one transfer/counterfactual response.
7. Students copy, print, or submit their work through the classroom's normal system.

## Fast classroom routes

### 15-minute beginning-of-course route

Use one of the first four Quick Assigns. No separate worksheet is required.

1. 2 minutes: frame the question.
2. 2 minutes: student prediction.
3. 5 minutes: bounded run/comparison.
4. 4 minutes: Observe + Explain.
5. 2 minutes: Transfer/exit response.

### 45-minute route

Use the applet as a structured inquiry lab or use a Level-2 Activity Pack.

1. 5 minutes: warm-up prediction.
2. 8 minutes: lesson tour or first Guided Challenge.
3. 15 minutes: controlled exploration / Activity Pack experiments.
4. 10 minutes: explanation/reflection.
5. 7 minutes: pair discussion or written transfer.

### Homework route

1. Students open the assigned stable Quick Assign link or Activity Pack.
2. Students run the named mechanism task.
3. Students complete Predict, Observe, Explain, and Transfer.
4. Students copy/print their local work if required.
5. Students submit through the class LMS or other teacher-controlled system.

## Foundations / course-track applet map

These thirteen labs form the primary introductory course path.

| # | Applet | Concept | Typical time | Core question |
|---:|---|---|---:|---|
| 1 | [Pathfinding Visualizer](playgrounds/search-pathfinding/index.html) | Search | 20 min | Why can A* do less search work than BFS while preserving the shortest-path result under the right heuristic assumptions? |
| 2 | [Hill Climbing and Simulated Annealing](playgrounds/hill-climbing/index.html) | Local search | 30 min | Why can greedy improvement stall, and what changes when the search can escape? |
| 3 | [Wumpus World](playgrounds/wumpus-world/index.html) | Logical agents | 25 min | What is the difference between unknown, plausible, and proven safe? |
| 4 | [CNF and SAT Builder](playgrounds/cnf-sat/index.html) | Logic / SAT | 25 min | How do propagation, branching, conflict, and pruning reduce solver search? |
| 5 | [Bayes Rule Playground](playgrounds/bayes-classifier/index.html) | Probability | 20 min | Why can a high-quality test still generate many false alarms when the event is rare? |
| 6 | [Bayesian Network](playgrounds/bayes-network/index.html) | Bayesian networks | 30 min | Why can evidence for one cause lower belief in another? |
| 7 | [K-Nearest Neighbors](playgrounds/knn-classifier/index.html) | Supervised learning | 20 min | What does k control, and why can both small and large k fail? |
| 8 | [Overfitting Explorer](playgrounds/overfitting/index.html) | Evaluation | 25 min | Why can perfect training performance fail on new data? |
| 9 | [Tiny Neural Network](playgrounds/neural-network/index.html) | Neural networks | 30 min | How do layers and nonlinearity change what a classifier can represent? |
| 10 | [K-Means Clustering](playgrounds/kmeans/index.html) | Unsupervised learning | 20 min | What changes during assignment and centroid-update cycles? |
| 11 | [Convolution Playground](playgrounds/convolution/index.html) | Vision | 25 min | Why can a small kernel expose edges, blur, or sharpen an image? |
| 12 | [Q-Learning Gridworld](playgrounds/q-learning-gridworld/index.html) | Reinforcement learning | 30 min | How does useful behavior emerge from repeated reward-driven updates? |
| 13 | [Game Trees: Minimax and Alpha-Beta Pruning](playgrounds/minimax-alpha-beta/index.html) | Adversarial search | 30 min | How can Alpha-Beta skip search work without changing the exact minimax answer? |

## Modern AI extensions

These two labs remain optional extensions rather than prerequisites for the Foundations sequence.

| Applet | Concept | Time | Core question |
|---|---|---:|---|
| [Transformer Language Modeling](playgrounds/transformer-language-model/index.html) | Transformers / modern NLP | 30-40 min | How can changing representation or attention state change the next-token distribution? |
| [Agent Tool Use and Context Protocols](playgrounds/agent-tool-context/index.html) | Agent systems | 30-40 min | What has to happen between a proposed tool call and a legitimate action? |

## Suggested 4-lesson mini-unit

| Lesson | Applet | Focus | Student product |
|---|---|---|---|
| 1 | Pathfinding | Search as controlled exploration | `QA-SEARCH-01` |
| 2 | Bayes Rule | Evidence, base rates, posterior belief | Explain one base-rate trap |
| 3 | Overfitting | Capacity and generalization | Identify underfit / reasonable fit / overfit |
| 4 | Q-Learning | Reward, exploration, value propagation | Explain one update and resulting policy change |

## Suggested 8-lesson sequence

| Lesson | Applet | Role in sequence |
|---|---|---|
| 1 | Pathfinding | State spaces and informed/uninformed search |
| 2 | Wumpus World | Perception and logical inference |
| 3 | CNF/SAT | Formal logic and solver search |
| 4 | Bayes Rule | Uncertainty and evidence |
| 5 | Bayesian Network | Structured dependence |
| 6 | KNN + Overfitting | Supervised learning and evaluation |
| 7 | K-Means + Tiny Neural Network | Unsupervised structure and learned representation |
| 8 | Convolution + Q-Learning | Perception and action-oriented learning |

Minimax/Alpha-Beta can extend the search unit when adversarial search is reached. Transformer and Agent Tool Use remain modern extensions.

## Student submission expectations

A complete response should include:

1. applet / stable activity ID,
2. prediction made before the relevant run or reveal,
3. one specific observation from applet state,
4. one mechanism-level explanation using course vocabulary,
5. one transfer or counterfactual response.

## Lightweight assessment rubric

| Level | Evidence |
|---|---|
| Complete | Predicts, observes, explains, and transfers with applet-specific evidence |
| Developing | Completes the fields but mostly describes rather than explains |
| Incomplete | Omits prediction, explanation, transfer, or applet evidence |

## Classroom privacy and data handling

AI Playgrounds has no backend and no student account system. Built-in response packets and Activity Pack drafts stay in the local browser. Students decide whether to copy, print, or submit their own response through a separate classroom system. The site does not collect student names, IDs, grades, submissions, or rosters.

The canonical site may send privacy-minimized aggregate requests to estimate public interest. DNT/GPC and explicit opt-out remain supported. Worksheet answers, Quick Assign response text, and experiment state are excluded from analytics requests.

## Accessibility and inclusion notes

The applets include visible focus treatment, reduced-motion support, keyboard guidance, text-state descriptions, and ARIA/live-state patterns where appropriate. The state/recovery QA contract also covers mobile/landscape/text-enlargement and selected localized-component behavior. These automated safeguards do not constitute accessibility conformance or replace assistive-technology user testing.

## Reuse and licensing

The suite is MIT licensed. Teachers may link, fork, embed, print, adapt, and remix the materials for classroom use. Applets remain offline-ready HTML artifacts; Activity Packs are printable HTML pages with local-only response storage.
