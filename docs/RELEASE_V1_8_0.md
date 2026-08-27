# AI Playgrounds v1.8.0

Release date: 2026-08-27

v1.8.0 completes GitHub issues #2, #3, and #4 by adding three opt-in algorithm modes to existing learner applets. It does not add a sixteenth applet, a new assignment surface, a learner account, or a backend. Previously released modes remain available and are still the defaults.

## Hill Climbing: repeated-restart benchmark

- Runs 2–100 seeded restarts with a bounded 10–500-step budget.
- Compares any subset of simple, steepest-ascent, stochastic, first-choice, simulated annealing, and tabu search.
- Gives every selected algorithm the same generated problem and the same starting state on restart `r`; each stochastic algorithm receives its own reproducible random stream.
- Reports completed trials, success frequency, mean final cost, mean best cost, and best observed cost instead of collapsing unlike outcomes into one ranking.
- Defines success explicitly for each teaching problem: zero attacking queen pairs, a stated landscape threshold, or a TSP result within 2% of the best result observed in that bounded comparison.
- Keeps benchmark state separate from the existing animated single-run experiment.

The benchmark compares these bounded teaching implementations. It is not a hardware benchmark and does not prove asymptotic superiority or general performance outside the selected seeds, instances, and budgets.

## K-Nearest Neighbors: regression mode

- Switches between classification and continuous-target regression without reloading the page.
- Uses the same selected `k`, distance metric, feature scaling, nearest-neighbor set, and uniform/distance weighting as the classification path.
- Predicts a continuous value with an arithmetic mean for uniform weights or a normalized weighted mean for distance weights.
- Shows each selected neighbor's distance, target, and contribution in a text-equivalent inspector and continuous prediction field.
- Uses RMSE rather than accuracy for regression cross-validation and exports `x,y,class,target` CSV data.

The original classification mode, class labels, voting behavior, and guided challenge remain the default path.

## CNF/SAT: bounded CDCL trace

- Keeps the original DPLL branch-and-backtrack trace as the default.
- Adds decisions, decision levels, implication reasons, conflicts, learned clauses, and non-chronological backjumps to an opt-in trace.
- Uses a deterministic first-UIP resolution analysis and retains learned clauses in the visible working clause set.
- Includes a fixed example that learns `(¬A ∨ ¬C)` and backjumps from decision level 3 to level 1, skipping an irrelevant level-2 decision.
- Preserves exhaustive SAT enumeration as the small-formula reference check.

This is a bounded educational CDCL implementation. Production optimizations including watched literals, restart policies, activity heuristics, and learned-clause deletion are intentionally outside the fidelity boundary.

## Localization, state, and classroom boundaries

- New static and dynamic presentation is available in English, Simplified Chinese, Vietnamese, and Spanish.
- Locale changes preserve mechanism controls, generated results/traces, and learner-authored Quick Assign responses.
- Share links preserve the new mode and bounded controls without including learner response text.
- Hard reset restores the historical default mode and the new controls' documented defaults.
- Quick Assign packet snapshots can name the new mode/result while responses remain local unless deliberately copied or printed.

## Release assurance

The v1.8.0 gate verifies:

- two byte-for-byte identical clean final builds;
- 15 applets and 58 deployed files;
- syntax-valid executable inline scripts and parseable inline JSON in every final HTML file;
- exact current CodeMeta, citation, analytics, and visible-release provenance;
- deterministic CDCL learning/backjump behavior, matched-start restart fairness, and KNN mean/weighted-mean calculations;
- responsive browser behavior, all four locales, share state, hard reset, result preservation, and the original DPLL/classification/single-run modes;
- the full inherited algorithm, localization, Quick Assign, HCI, privacy, responsive, and modern-lab parity suite.

These checks establish bounded software behavior under the tested conditions. They do not establish measured learning gains, universal learner preference, classroom adoption, hardware performance, production-solver equivalence, or accessibility conformance.

The archived v1.0.1 DOI remains historical provenance and is not reassigned to v1.8.0.
