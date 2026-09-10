# AI Playgrounds Teacher Pack

**Purpose.** This pack turns AI Playgrounds into ready-to-run classroom activities. The current suite contains **15 learner applets: 13 Foundations/course-track labs plus 2 Modern AI extensions**. It is designed for introductory AI, high-school computer science, early undergraduate survey courses, teacher training, and self-study.

**Language scope.** All 15 learner applets and Quick Assigns support English, Simplified Chinese, Vietnamese, and Spanish. The website Teacher Pack and Curriculum Map use English and Simplified Chinese; this text guide and the NN-1/CNN-1 Activity Pack pilot are English-only. Do not infer site-wide four-language coverage from the applet boundary.

**Core claim.** Each applet is an offline-ready learning tool with no backend, no account system, and no project-hosted student-response storage. It includes scenario/prediction workflows, visual and text explanations, and keyboard-oriented support. Drafts can remain in the learner's browser. Software verification establishes tested implementation behavior, not learning gains or accessibility conformance.

## Assignment levels

### Level 1 - Quick Assign · 10-15 min

Quick Assigns reuse the applet's existing Guided Challenge and local Student response packet. Students complete one bounded mechanism task using:

**predict -> run/manipulate -> observe -> explain -> transfer**

Use the stable ID when assigning work. Student writing stays local unless the student copies, prints, or submits it through the teacher's normal classroom system.

All fifteen Level-1 activities are active. Use the classroom link for the chosen lab:

| # | Applet | Track | Quick Assign |
|---:|---|---|---|
| 1 | [Pathfinding Visualizer](https://lmdixon23.github.io/ai-playgrounds/playgrounds/search-pathfinding/index.html) | Foundations | [QA-SEARCH-01](https://lmdixon23.github.io/ai-playgrounds/playgrounds/search-pathfinding/index.html?mode=classroom#quick-assign-qa-search-01) |
| 2 | [Hill Climbing and Simulated Annealing](https://lmdixon23.github.io/ai-playgrounds/playgrounds/hill-climbing/index.html) | Foundations | [QA-LOCAL-01](https://lmdixon23.github.io/ai-playgrounds/playgrounds/hill-climbing/index.html?mode=classroom#quick-assign-qa-local-01) |
| 3 | [Wumpus World](https://lmdixon23.github.io/ai-playgrounds/playgrounds/wumpus-world/index.html) | Foundations | [QA-WUMPUS-01](https://lmdixon23.github.io/ai-playgrounds/playgrounds/wumpus-world/index.html?mode=classroom#quick-assign-qa-wumpus-01) |
| 4 | [CNF and SAT Builder](https://lmdixon23.github.io/ai-playgrounds/playgrounds/cnf-sat/index.html) | Foundations | [QA-SAT-01](https://lmdixon23.github.io/ai-playgrounds/playgrounds/cnf-sat/index.html?mode=classroom#quick-assign-qa-sat-01) |
| 5 | [Bayes Rule Playground](https://lmdixon23.github.io/ai-playgrounds/playgrounds/bayes-classifier/index.html) | Foundations | [QA-BAYES-01](https://lmdixon23.github.io/ai-playgrounds/playgrounds/bayes-classifier/index.html?mode=classroom#quick-assign-qa-bayes-01) |
| 6 | [Bayesian Network](https://lmdixon23.github.io/ai-playgrounds/playgrounds/bayes-network/index.html) | Foundations | [QA-BN-01](https://lmdixon23.github.io/ai-playgrounds/playgrounds/bayes-network/index.html?mode=classroom#quick-assign-qa-bn-01) |
| 7 | [K-Nearest Neighbors](https://lmdixon23.github.io/ai-playgrounds/playgrounds/knn-classifier/index.html) | Foundations | [QA-KNN-01](https://lmdixon23.github.io/ai-playgrounds/playgrounds/knn-classifier/index.html?mode=classroom#quick-assign-qa-knn-01) |
| 8 | [Overfitting Explorer](https://lmdixon23.github.io/ai-playgrounds/playgrounds/overfitting/index.html) | Foundations | [QA-OVERFIT-01](https://lmdixon23.github.io/ai-playgrounds/playgrounds/overfitting/index.html?mode=classroom#quick-assign-qa-overfit-01) |
| 9 | [Tiny Neural Network](https://lmdixon23.github.io/ai-playgrounds/playgrounds/neural-network/index.html) | Foundations | [QA-NN-01](https://lmdixon23.github.io/ai-playgrounds/playgrounds/neural-network/index.html?mode=classroom#quick-assign-qa-nn-01) |
| 10 | [K-Means Clustering](https://lmdixon23.github.io/ai-playgrounds/playgrounds/kmeans/index.html) | Foundations | [QA-KMEANS-01](https://lmdixon23.github.io/ai-playgrounds/playgrounds/kmeans/index.html?mode=classroom#quick-assign-qa-kmeans-01) |
| 11 | [Convolution Playground](https://lmdixon23.github.io/ai-playgrounds/playgrounds/convolution/index.html) | Foundations | [QA-CNN-01](https://lmdixon23.github.io/ai-playgrounds/playgrounds/convolution/index.html?mode=classroom#quick-assign-qa-cnn-01) |
| 12 | [Q-Learning Gridworld](https://lmdixon23.github.io/ai-playgrounds/playgrounds/q-learning-gridworld/index.html) | Foundations | [QA-QL-01](https://lmdixon23.github.io/ai-playgrounds/playgrounds/q-learning-gridworld/index.html?mode=classroom#quick-assign-qa-ql-01) |
| 13 | [Transformer Language Modeling](https://lmdixon23.github.io/ai-playgrounds/playgrounds/transformer-language-model/index.html) | Modern AI extension | [QA-TRANSFORMER-01](https://lmdixon23.github.io/ai-playgrounds/playgrounds/transformer-language-model/index.html?mode=classroom#quick-assign-qa-transformer-01) |
| 14 | [Agent Tool Use and Context Protocols](https://lmdixon23.github.io/ai-playgrounds/playgrounds/agent-tool-context/index.html) | Modern AI extension | [QA-AGENT-01](https://lmdixon23.github.io/ai-playgrounds/playgrounds/agent-tool-context/index.html?mode=classroom#quick-assign-qa-agent-01) |
| 15 | [Game Trees: Minimax and Alpha-Beta Pruning](https://lmdixon23.github.io/ai-playgrounds/playgrounds/minimax-alpha-beta/index.html) | Foundations | [QA-MINIMAX-01](https://lmdixon23.github.io/ai-playgrounds/playgrounds/minimax-alpha-beta/index.html?mode=classroom#quick-assign-qa-minimax-01) |

The [Quick Assign guide](docs/QUICK_ASSIGN_ARCHITECTURE.md) provides every activity's objective and teacher look-for criteria.

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

Use one of the first four Quick Assigns for early-course topics, or another of the fifteen active activities when its topic fits the class. No separate worksheet is required.

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

The suite is MIT licensed. Teachers may link, fork, embed, print, adapt, and remix the materials for classroom use. For single-file offline delivery, use the [standalone classroom downloads](https://lmdixon23.github.io/ai-playgrounds/downloads.html), not a website page that may need neighbouring assets. Extract the ZIP, then copy or rename any individual HTML. No build or installation is needed. Activity Packs are printable HTML pages with local-only response storage.

Copying an HTML file does not copy saved answers. Copy, export, or print work before clearing browser data or changing devices. Human learner/educator usability studies and human screen-reader testing remain deferred; automated checks do not establish those outcomes.
