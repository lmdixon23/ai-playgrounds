# Lab 15 Architecture: Game Trees, Minimax, and Alpha-Beta Pruning

Date: 2026-08-25

Status: R0 architecture freeze candidate. No public integration is authorized by this file alone.

Base release: AI Playgrounds v1.5.0 at `467a9dc3768eddffd6238674b9752eaea1917ce8`.

Target release line: v1.6.0.

## 1. Decision

Lab 15 should be **Game Trees: Minimax and Alpha-Beta Pruning** rather than Retrieval, Embeddings, and RAG.

The older v1.2 roadmap ranked RAG as the strong curricular follow-up after Labs 13 and 14. The later curriculum coverage matrix exposed a more urgent structural gap: adversarial search is absent despite being central to both AIMA and the current CS50 AI search sequence. The v1.4 and v1.5 product/engagement gates are now complete, so the provisional classical/contemporary balancing rule should take effect.

Lab 15 therefore closes the highest-priority classical search gap while preserving RAG as a high-value later modern extension.

## 2. Core learning mechanism

The applet must make this transition inspectable:

`terminal utilities -> recursive MIN/MAX backups -> root decision`

and then add alpha-beta as a semantics-preserving work reduction:

`same game tree + same child order -> bounds update -> provably irrelevant subtree -> prune -> same minimax value`

The learner should see two distinct claims:

1. **Minimax determines the backed-up value and optimal action set under the toy game's assumptions.**
2. **Alpha-beta can avoid evaluating nodes that cannot change that minimax result.**

Move ordering is then a third mechanism:

`same tree + different child order -> different search work -> same minimax result`

The applet must never imply that alpha-beta changes the game value, improves the decision quality on a fixed fully searched tree, or somehow knows the values of nodes it prunes.

## 3. Scope and exclusions

### In scope

- finite deterministic two-player zero-sum perfect-information game trees;
- alternating MAX and MIN turns;
- numeric terminal utilities from MAX's perspective;
- recursive minimax backup;
- deterministic child-order tie breaking;
- alpha and beta bounds;
- alpha-beta cutoffs;
- visited-node and pruned-node accounting;
- move ordering as an efficiency variable;
- exact comparison of Minimax and Alpha-Beta on the same tree;
- one optional depth-limited heuristic-evaluation scenario only if it can remain clearly separated from terminal-utility semantics.

### Out of scope for the core model

- stochastic games or chance nodes;
- simultaneous moves;
- imperfect information;
- non-zero-sum payoffs;
- multiagent equilibria;
- Monte Carlo Tree Search;
- reinforcement learning;
- chess-engine claims;
- frontier-model reasoning claims.

These exclusions are important because each introduces a distinct mechanism that would weaken causal clarity in this lab.

## 4. Canonical data model

A game tree is an immutable finite rooted tree. Each node has:

- `id`: stable string identifier;
- `children`: ordered list of child node ids;
- `utility`: numeric value only for terminal nodes;
- optional presentation label.

The active player is determined by depth from the root:

- even depth: MAX;
- odd depth: MIN.

The reference model must validate:

- exactly one root;
- every referenced child exists;
- no cycles;
- every nonterminal node has at least one child;
- every terminal node has a finite numeric utility;
- nonterminal nodes do not supply a terminal utility;
- ids are unique;
- the complete tree is reachable from the root.

Invalid trees fail closed before any search trace is generated.

## 5. Deterministic reference semantics

### 5.1 Minimax

For a terminal node `n`:

`V(n) = utility(n)`

For a MAX node:

`V(n) = max(V(c))` over its ordered children.

For a MIN node:

`V(n) = min(V(c))` over its ordered children.

The deterministic selected action is the first child in configured child order whose value equals the node's backed-up optimum. The model must separately expose the complete set of equally optimal children so deterministic tie breaking is not confused with mathematical uniqueness.

### 5.2 Alpha-beta

The reference implementation uses the conventional bounds:

- `alpha`: best value MAX can already force along the current ancestry;
- `beta`: best value MIN can already force along the current ancestry.

At a MAX node, update `alpha = max(alpha, child_value)`.

At a MIN node, update `beta = min(beta, child_value)`.

A cutoff occurs when `alpha >= beta` after a child has been evaluated. Remaining siblings under that node are not evaluated.

The alpha-beta result must expose:

- root minimax value;
- selected child under deterministic tie breaking;
- optimal child set when it is provable from evaluated information;
- visited nodes in exact order;
- terminal nodes actually evaluated;
- pruned node ids;
- prune-root events;
- exact alpha/beta values at each trace event;
- node count and leaf-evaluation count.

The implementation must not read terminal utilities inside a pruned subtree while constructing the algorithmic trace. Presentation code may know the immutable tree structure, but algorithmic evidence must distinguish **present in the problem definition** from **evaluated by the algorithm**.

## 6. Trace contract

The Python reference and independent JavaScript implementation should emit a recursively comparable trace using explicit event types:

- `enter`
- `leaf`
- `child_return`
- `best_update`
- `alpha_update`
- `beta_update`
- `prune`
- `return`

Each event should include only the fields relevant to that transition, drawn from:

- node id;
- depth;
- player;
- child id;
- child index;
- returned value;
- current best value;
- alpha;
- beta;
- pruned child ids;
- visited count;
- evaluated-leaf count.

The trace is the source of truth for playback. The browser must not implement a second search algorithm merely to animate the tree.

## 7. Frozen scenario families

At least eight deterministic scenario families should be frozen before browser work.

### Scenario 1: Simple backup

A small balanced tree where the root value can be computed by two MIN backups followed by one MAX backup.

Purpose: establish the recursive value rule without pruning.

### Scenario 2: Greedy trap

The locally largest immediate-looking branch is not the minimax-optimal branch after the opponent's response.

Purpose: distinguish adversarial reasoning from one-ply greedy choice.

### Scenario 3: First safe prune

A tree with an early alpha-beta cutoff that removes at least one complete sibling subtree.

Purpose: show exactly why a branch cannot alter an ancestor decision.

### Scenario 4: Good versus poor move ordering

The tree and utilities are identical, but child order changes.

Required invariant:

- same root value;
- same optimal action set;
- different visited-node or evaluated-leaf count.

Purpose: make move ordering visibly affect work, not correctness.

### Scenario 5: No pruning possible

A valid tree where alpha-beta visits the same nodes as minimax under the supplied order.

Purpose: block the misconception that alpha-beta always prunes substantially.

### Scenario 6: Tied optimal actions

Two root children share the same optimal backed-up value.

Purpose: separate the optimal action set from deterministic first-child tie breaking.

### Scenario 7: Deep cutoff after several updates

A deeper tree in which alpha and beta both change before a later cutoff.

Purpose: make the bound logic more than a one-step special case.

### Scenario 8: Boundary trees

Include:

- a single terminal root;
- a one-child chain;
- a highly unbalanced tree;
- negative, zero, and positive utilities.

Purpose: adversarially test recursion, display layout, and counting.

## 8. Learner-facing experiments

The main applet should support the following direct manipulations without requiring code entry:

1. Switch between Minimax and Alpha-Beta.
2. Step forward and backward through the frozen trace.
3. Restart the same tree without regenerating it.
4. Change move ordering using deterministic presets.
5. Select a node and inspect its backed-up value, player role, and current bounds.
6. Compare visited and pruned nodes between two saved runs.
7. Change selected terminal utilities in a bounded editable teaching tree, then recompute deterministically.
8. Load frozen scenarios that isolate one misconception at a time.

If utility editing is included, the tree topology remains fixed in the first release. Free-form topology editing adds validation and layout complexity without improving the core first-use mechanism.

## 9. Visual architecture

The primary visual should be a game tree, not a board game.

Each node should communicate:

- MAX or MIN role;
- current backed-up value when known;
- active-search state;
- evaluated terminal state;
- returned state;
- pruned state;
- alpha/beta bounds when relevant.

Edges should communicate traversal order without suggesting simultaneous computation.

Pruned subtrees should remain spatially visible so the learner can see what was skipped, but they must be clearly labeled **not evaluated by the algorithm**. A pruned leaf's utility may remain visible as part of the problem definition only if the visual wording makes it explicit that the search never inspected that value. An alternative reveal mode may hide pruned leaf utilities until the teacher chooses to inspect them.

A compact comparison strip should show:

- root value;
- selected move;
- optimal move set;
- nodes visited;
- leaves evaluated;
- nodes pruned.

## 10. Guided Challenges

Five predict-before-reveal challenges are required.

### Challenge 1: Root choice

Predict which root child minimax will select and the root value.

### Challenge 2: MIN backup

Predict the value a specific MIN node returns after seeing its child utilities.

### Challenge 3: Will this branch prune?

Freeze the trace immediately before a decisive child return. Ask whether the remaining siblings will be evaluated and why.

### Challenge 4: Move ordering

Compare two orders of the same tree. Predict which order evaluates fewer leaves without changing the minimax result.

### Challenge 5: Greedy versus minimax

Predict whether the largest one-ply visible value is necessarily the correct root action. Reveal the opponent response and require a mechanism explanation.

Prediction inputs must lock before reveal. Locale switching must preserve the complete challenge state.

## 11. Misconceptions the design must explicitly block

- MAX does not simply choose the largest visible terminal leaf anywhere in the tree.
- MIN is not an error term; it represents the opponent choosing against MAX's interest.
- Alpha-beta does not approximate minimax on a finite fully searched tree.
- A pruned node is not evaluated and then hidden.
- Better move ordering can reduce work but does not improve the exact minimax value.
- A deterministic tie-break does not prove the optimal move is unique.
- The toy game-tree assumptions do not automatically apply to stochastic, hidden-information, or non-zero-sum games.

## 12. Independent reference and parity plan

### Python reference

Create a small standard-library-only module, tentatively:

`tools/minimax_alpha_beta_reference.py`

It should expose:

- tree validation;
- exact minimax evaluation;
- exact alpha-beta evaluation;
- deterministic trace generation;
- scenario fixtures;
- result serialization.

### Independent JavaScript core

Create a separate implementation, tentatively:

`tools/minimax_alpha_beta_core.js`

It must not be generated from the Python source. Cross-runtime fixtures compare recursively normalized outputs.

### Cross-runtime families

At minimum compare:

- canonical simple backup;
- greedy trap;
- first prune;
- good ordering;
- poor ordering;
- no-prune tree;
- tied optimum;
- boundary/unbalanced tree;
- invalid input families separately as matching rejection categories.

The parity harness must include a self-test proving it detects an intentionally perturbed result.

## 13. Numerical and structural invariants

Permanent tests should include:

- minimax root value equals alpha-beta root value for every valid fixture;
- deterministic selected child obeys the documented tie-break;
- optimal child set is correct;
- alpha never decreases along a MAX node's processed children;
- beta never increases along a MIN node's processed children;
- every prune event satisfies `alpha >= beta` at the cutoff point;
- no pruned node appears in the evaluated-node sequence;
- alpha-beta evaluates no more leaves than minimax on the same child order;
- changing only child order leaves the root value unchanged;
- invalid trees fail before trace generation;
- replay is exactly reproducible.

A small exhaustive census should generate many bounded trees and compare both algorithms. For example, enumerate complete alternating trees up to a tractable size over a small utility alphabet such as `{-1, 0, 1}` and several child orders. The census should verify value equality, cutoff validity, no-pruned-node evaluation, and deterministic replay.

## 14. Localization contract

Target locales remain:

- English;
- Simplified Chinese;
- Vietnamese;
- Spanish.

Protected identifiers include:

- `MAX`
- `MIN`
- `alpha`
- `beta`
- node ids;
- scenario ids;
- event-type keys;
- numeric utilities;
- machine-state keys.

Learner-facing prose, action labels, explanations, challenge prompts, and accessibility text must localize semantically without changing the underlying tree, trace, current index, saved comparison, or challenge state.

## 15. Accessibility and responsive requirements

- Complete text equivalent of the current search state.
- Keyboard access to algorithm selector, scenario selector, transport, node inspection, utility editing, and challenge controls.
- Focus-visible styling.
- No information conveyed only by color.
- Reduced-motion path with the complete state still available.
- 390 px viewport containment.
- Tree may scroll horizontally inside its own bounded region rather than forcing page-level overflow.
- SVG nodes and important trace states require accessible labels or a synchronized text representation.

## 16. Offline and security boundary

The lab remains deterministic and offline-ready.

No runtime dependency on:

- network access;
- model APIs;
- external game engines;
- remote assets;
- analytics for core operation;
- user accounts;
- backend persistence.

Editable utility input is numeric and bounded. No user-provided HTML is executed or injected into markup.

## 17. Release sequence

Use the same fail-closed progression established by Labs 13 and 14.

### R0 - architecture

Freeze this mechanism, trace schema, scenario families, misconceptions, acceptance boundary, and release sequence.

### R1 - Python reference

Implement validation, minimax, alpha-beta, frozen scenarios, adversarial unit tests, and initial bounded exhaustive census.

### R2 - independent JavaScript parity

Implement the second core and cross-runtime recursive fixture comparison with a harness self-test.

### R3 - browser prototype

Build English-only browser experience over the frozen core. Do not add localization before the interaction model is stable.

### R4 - English source freeze

Run mechanism, accessibility-state, challenge, mobile, and reduced-motion browser gates. Freeze the exact English source candidate.

### R5 - semantic localization

Create complete ZH/VI/ES catalogs with protected identifiers and semantic trap checks.

### R6 - four-locale browser/state freeze

Verify that locale switching changes presentation only and preserves the complete algorithm/challenge state.

### R7 - public integration

Compose Lab 15 into a fifteen-applet deterministic Pages artifact, update curriculum/release metadata, add permanent regression gates, and require exact-head Verify before merge.

### Release

One squash merge into `main`, exact-sha push Verify, Pages deployment, then an immutable v1.6.0 tag and GitHub Release only after the publisher confirms the deployed SHA is still current `main`.

## 18. Kill conditions

Stop or redesign the lab before public integration if any of the following remains unresolved:

1. The browser requires a second implementation of minimax/alpha-beta to animate the reference trace.
2. The visual implies pruned nodes were evaluated.
3. Alpha-beta and minimax disagree on root value for any valid bounded fixture.
4. Move-order comparisons accidentally change the tree or utility data.
5. Tie handling is presented as uniqueness.
6. Locale switching mutates search or challenge state.
7. Mobile layout makes the search tree unusable without page-level overflow.
8. The lab needs a game-specific rule system to make the core mechanism understandable.
9. The exhaustive census exposes a trace or pruning invariant violation.
10. The applet cannot explain why a cutoff is safe in one compact learner-visible statement tied to the actual bounds.

## 19. Acceptance boundary

Lab 15 is publishable only when it can support all of the following bounded claims with executable evidence:

- it implements deterministic minimax and alpha-beta over the documented finite-tree model;
- both algorithms return the same exact root value on all tested valid fixtures;
- alpha-beta pruning is derived from actual bound conditions and pruned nodes are not algorithmically evaluated;
- move ordering can change search work without changing the exact minimax result;
- the browser is a presentation of the tested mechanism rather than a separate solver;
- all four locales preserve machine state;
- the public artifact remains deterministic, offline-ready, responsive, and regression-tested.

It must not claim measured learning gains, superiority over other instructional tools, general game-solving performance, or applicability beyond the documented game assumptions without separate evidence.