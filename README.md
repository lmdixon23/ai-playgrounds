# AI Playgrounds — Interactive Visualizations for Intro-to-AI

Twelve single-file HTML+JavaScript applets that let students *drag a slider and
watch a core AI idea play out*. No build step, no install, no backend — each
applet is one HTML file you can open locally or host on GitHub Pages.

The applets were authored as a companion to the
**Introduction to Artificial Intelligence** course (Mixed High School, 2025–2026,
Haidian Kaiwen Academy) and map 1-to-1 to the curriculum's most
visually-rich units, with extra depth on the under-served Russell & Norvig topics
(logical agents, knowledge bases, Bayesian networks, local search). They're free for any classroom to use.

> **Live demo:** https://lmdixon23.github.io/ai-playgrounds/

## The twelve applets

| Concept | Applet | "Aha" moment |
|---|---|---|
| Search & problem representation | [Pathfinding](playgrounds/search-pathfinding/) | Why A* explores fewer nodes than BFS |
| Logical agent (AIMA Ch 7) | [Wumpus World](playgrounds/wumpus-world/) | The difference between "I haven't seen it" and "I've proved it's not there" |
| Logic & knowledge bases | [CNF & SAT Builder](playgrounds/cnf-sat/) | Why every SAT solver in the world wants CNF as input |
| Probability & Naïve Bayes | [Bayes classifier](playgrounds/bayes-classifier/) | Why a 99%-accurate test for a rare disease still misleads |
| Bayesian networks (AIMA Ch 14) | [Bayes network](playgrounds/bayes-network/) | Why learning of an earthquake LOWERS your belief in a burglary |
| Supervised learning (KNN) | [K-Nearest Neighbors](playgrounds/knn-classifier/) | What `k` does to a decision boundary |
| Evaluation, leakage, regularization | [Overfitting](playgrounds/overfitting/) | Why a perfect training fit can fail on test data |
| Local search (AIMA Ch 4) | [Hill climbing & SA](playgrounds/hill-climbing/) | Why sometimes you have to take a worse step |
| Neural network fundamentals | [Tiny neural net](playgrounds/neural-network/) | How layers + non-linearity carve up space |
| Unsupervised learning | [K-means clustering](playgrounds/kmeans/) | What "iterating to convergence" looks like |
| Vision with CNNs | [Convolution playground](playgrounds/convolution/) | Why a 3×3 matrix can detect edges — and how a CNN *learns* one |
| Reinforcement learning | [Q-learning gridworld](playgrounds/q-learning-gridworld/) | How a value function emerges from random walking |

## Design principles

Every applet follows the same template so students who use one know how to use them all:

1. **One screen, no menus.** Sliders / buttons on one side, live visualization on the other.
2. **Default state already shows the punchline.** Open the page → the visualization is already mid-demo. No setup before learning begins.
3. **Tooltips on every control.** Hovering a slider explains what it does and which units cover it.
4. **Reset is one click.** Students can experiment without fear.
5. **No build step.** Every applet is a single `index.html` with inline `<script>` and `<style>`. Open in a browser, done.
6. **Self-contained, minimal dependencies.** Every applet is a single file with no build step. The only outbound calls are a privacy-friendly, cookieless pageview ping (GoatCounter) and — for the Bayesian-network applet only — D3 from cdnjs; if D3 is blocked, that applet now degrades to a short fallback message and its inference and probabilities keep working (`typeof d3` guard in `bayes-network/index.html`).

## Deploying

### Option A — GitHub Pages (how the live demo runs)

This repository is published directly to GitHub Pages. In **Settings → Pages**, the source is the `main` branch at the root (`/`); because `index.html` sits at the repo root, the site serves at the live-demo URL above, and the `.nojekyll` file tells Pages to serve the folders as-is.

To host your own copy, fork this repo and enable Pages the same way (Settings → Pages → deploy from `main`, root), or drop these files onto any static host.

### Option B — open locally

Double-click `index.html`. Everything works from a `file://` URL.

### Option C — embed individual applets

Each applet is fully self-contained. Paste any `playgrounds/*/index.html` into a
school LMS as an HTML widget and it runs in isolation, with no dependency on the
landing page or sibling applets.

## Educational notes

Each applet has a **For teachers** section at the bottom of its page covering:

- Curriculum unit number and learning objectives addressed
- A 3-question pre-discussion prompt to use before students touch the applet
- A 3-question post-exploration prompt to use after
- Common misconceptions the applet was designed to defeat

## Pedagogy: why these twelve?

The IAI curriculum has units that are inherently visual (search trees,
decision boundaries, clusters, value functions) and units that are
discussion-driven (ethics, society). Interactive applets pay off most where:

1. The concept involves **continuous parameters** a slider can sweep (k in KNN, polynomial degree, learning rate).
2. The concept involves a **dynamic process** a play button can animate (search expansion, k-means iterations, Q-learning convergence).
3. The concept produces an **immediate visual contradiction** to a naive expectation (overfitting curve looking great in-sample, terrible out-of-sample).

The remaining units are discussion-driven (ethics, society, and the like), so they get
discussion guides instead of applets (those guides live in the IAI course repo,
not here). Search gets **three applets**, and a couple of other topics get **two each**, because
Russell & Norvig–style content (logical agents, knowledge bases, Bayesian
networks, local search) is under-served by existing interactive tools on the web.

## License

MIT — see `LICENSE`. Free to use, fork, modify, deploy, and remix for any classroom.

## Contact

Built by Logan Dixon for the 2025–2026 Intro to AI course at Haidian Kaiwen Academy.
File issues at <https://github.com/lmdixon23/ai-playgrounds/issues>.

## Scope

- **Educational accuracy ≠ research accuracy.** These are intuition-builders, not
  reference implementations. For example, the convolution applet defaults to hand-picked filters to show what a convolution *does* — and its optional Learn-the-filter mode runs gradient descent on one 3×3 kernel toward a target, so students can also watch a filter being *learned*. Each
  applet has a "What this simplifies" note at the bottom.
- **Browser-only compute.** All applets run in pure JavaScript with no GPU
  acceleration. Anything heavier than ~10⁴ operations per frame will stutter on
  Chromebooks.
- **Bilingual UI is complete.** All twelve applets ship a full English/中文 `STRINGS` table and a language toggle. (An earlier draft of this section wrongly called this partial; every applet has a parallel `zh:` block.)

## Future Enhancements

Framed as teaching extensions: each item exposes a variable the current applet holds fixed. These are deliberately scoped to gaps that are *not* already built — the applets already ship rich control sets (e.g. the search demo covers BFS / DFS / A\* / Dijkstra / bidirectional / IDA\* with four heuristics, weighted terrain, selectable wall / maze layouts (a recursive-division maze generator plus a random-walls generator), and a side-by-side two-algorithm race with live node-expansion counters; the neural-net already has activation/optimizer selectors, per-neuron activation heatmaps, input-feature toggles, **and** a weights-as-edges network graph; k-means already has k-means++/inertia/silhouette).

- **CNF & SAT — CDCL trace mode.** The applet already animates DPLL with unit propagation; the page text notes real solvers add conflict-driven clause learning and watched literals. A CDCL view would show *why* modern solvers outrun plain DPLL. (Verified absent from the code.)
- **k-Nearest Neighbors — regression mode.** A toggle to predict a continuous value (mean of the k neighbors) alongside classification, so students see kNN is not inherently a classifier. (Verified absent.)
- **Hill climbing & SA — success-rate benchmark.** Run N random restarts per algorithm on the same problem and tabulate success rate and mean cost, turning the eight-algorithm menu into a comparison rather than a sequence of anecdotes. (Verified absent.)
- **Bayes-network — inline D3.** A `typeof d3` guard now shows a fallback message if the CDN is blocked (inference and probabilities still work); fully inlining D3 would remove the last CDN dependency.
