# AI Playgrounds — Curriculum Map

Twelve interactive applets, mapped to the standard *Artificial Intelligence: A Modern Approach* (Russell & Norvig) syllabus. Free, open-source (MIT), no install, bilingual EN/中文.

**Live:** https://lmdixon23.github.io/ai-playgrounds/

*Chapter numbers follow AIMA 4th edition; a 3rd-edition course will find the same topics under nearby chapters. Each applet's own "For teachers" panel carries that unit's pre- and post-discussion prompts and the misconceptions it targets.*

| Applet | AIMA topic (chapter) | Learning objective | The "aha" / misconception it defeats |
|---|---|---|---|
| [Pathfinding](playgrounds/search-pathfinding/) | Solving Problems by Searching (Ch 3) | Compare uninformed and informed search; see how a heuristic steers A\* | Why A\* expands far fewer nodes than BFS for the same optimal path |
| [Wumpus World](playgrounds/wumpus-world/) | Logical Agents (Ch 7) | Separate "not yet observed" from "logically entailed" | The gap between "I haven't seen it" and "I've *proved* it isn't there" |
| [CNF & SAT Builder](playgrounds/cnf-sat/) | Logical Agents; propositional inference (Ch 7) | Convert formulas to CNF; trace DPLL with unit propagation | Why every SAT solver wants CNF as its input |
| [Bayes classifier](playgrounds/bayes-classifier/) | Quantifying Uncertainty; Naïve Bayes (Ch 12–13) | Apply Bayes' rule; reason about base rates | Why a 99%-accurate test for a rare disease still misleads |
| [Bayes network](playgrounds/bayes-network/) | Probabilistic Reasoning; Bayesian networks (Ch 13–14) | Read conditional independence; update beliefs | Why learning of an earthquake *lowers* your belief in a burglary (explaining away) |
| [K-Nearest Neighbors](playgrounds/knn-classifier/) | Learning from Examples; instance-based learning (Ch 19) | See how *k* shapes a decision boundary | What *k* trades off — a jagged overfit vs. an over-smoothed boundary |
| [Overfitting](playgrounds/overfitting/) | Learning from Examples; model selection & regularization (Ch 19) | Separate training from test error; motivate regularization | Why a perfect training fit can fail on held-out data |
| [Hill climbing & SA](playgrounds/hill-climbing/) | Search in Complex Environments; local search (Ch 4) | Contrast greedy ascent with simulated annealing | Why you sometimes must take a *worse* step to escape a local optimum |
| [Tiny neural net](playgrounds/neural-network/) | Deep Learning (Ch 21) | Connect layers and non-linearity to decision regions | How depth and non-linearity carve up the input space |
| [K-means clustering](playgrounds/kmeans/) | Learning Probabilistic Models; unsupervised learning (Ch 20) | Run assign/update to convergence; judge the choice of *k* | What "iterating to convergence" actually looks like |
| [Convolution playground](playgrounds/convolution/) | Deep Learning; computer vision (Ch 21, 25) | Apply a kernel by hand; watch a filter be *learned* | Why a 3×3 matrix can detect edges — and how a CNN learns one |
| [Q-learning gridworld](playgrounds/q-learning-gridworld/) | Reinforcement Learning (Ch 22) | Watch a value function form from experience | How a value function emerges from random walking |

**Why these twelve.** Search gets three applets and a few topics get two, by design: the Russell & Norvig topics under-served by existing interactive tools — logical agents, knowledge bases, Bayesian networks, local search — get the most depth here.

**Use it freely.** MIT-licensed: fork it, embed any applet in an LMS as an HTML widget, or link directly. Every applet is a single HTML file with no build step and runs offline from `file://`.
