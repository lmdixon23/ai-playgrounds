#!/usr/bin/env python3
"""Adversarial and bounded-exhaustive tests for Lab 15's game-tree reference."""

from __future__ import annotations

import itertools
import json
import math
import unittest

from minimax_alpha_beta_reference import (
    GameTree,
    SearchResult,
    TreeNode,
    TreeValidationError,
    alpha_beta,
    minimax,
    player_for_depth,
    result_to_dict,
    scenario,
    tree_to_dict,
)


def make_tree(root: str, *nodes: TreeNode) -> GameTree:
    return GameTree(root=root, nodes=tuple(nodes))


def complete_binary_tree(
    utilities: tuple[int, int, int, int],
    order_mask: int,
) -> GameTree:
    r_children = ("B", "A") if order_mask & 1 else ("A", "B")
    a_children = ("A2", "A1") if order_mask & 2 else ("A1", "A2")
    b_children = ("B2", "B1") if order_mask & 4 else ("B1", "B2")
    a1, a2, b1, b2 = utilities
    return make_tree(
        "R",
        TreeNode("R", r_children),
        TreeNode("A", a_children),
        TreeNode("B", b_children),
        TreeNode("A1", utility=a1),
        TreeNode("A2", utility=a2),
        TreeNode("B1", utility=b1),
        TreeNode("B2", utility=b2),
    )


class MinimaxAlphaBetaTests(unittest.TestCase):
    def assertValidationCode(self, tree: GameTree, code: str) -> None:
        with self.assertRaises(TreeValidationError) as caught:
            minimax(tree)
        self.assertEqual(caught.exception.code, code)

    def assertSameRootDecision(self, tree: GameTree) -> tuple[SearchResult, SearchResult]:
        mm = minimax(tree)
        ab = alpha_beta(tree)
        self.assertEqual(ab.root_value, mm.root_value)
        self.assertEqual(ab.selected_child, mm.selected_child)
        return mm, ab

    def test_01_player_roles_alternate_from_max_root(self):
        self.assertEqual(player_for_depth(0), "MAX")
        self.assertEqual(player_for_depth(1), "MIN")
        self.assertEqual(player_for_depth(2), "MAX")
        with self.assertRaises(ValueError):
            player_for_depth(-1)

    def test_02_missing_root_fails_closed(self):
        self.assertValidationCode(
            make_tree("missing", TreeNode("R", utility=0)),
            "missing_root",
        )

    def test_03_duplicate_id_fails_closed(self):
        self.assertValidationCode(
            make_tree("R", TreeNode("R", utility=0), TreeNode("R", utility=1)),
            "duplicate_id",
        )

    def test_04_missing_child_fails_closed(self):
        self.assertValidationCode(
            make_tree("R", TreeNode("R", ("X",))),
            "missing_child",
        )

    def test_05_duplicate_child_fails_closed(self):
        self.assertValidationCode(
            make_tree("R", TreeNode("R", ("A", "A")), TreeNode("A", utility=1)),
            "duplicate_child",
        )

    def test_06_root_with_parent_fails_closed(self):
        self.assertValidationCode(
            make_tree(
                "R",
                TreeNode("R", ("A",)),
                TreeNode("A", ("R",)),
            ),
            "root_has_parent",
        )

    def test_07_multiple_parents_fail_closed(self):
        self.assertValidationCode(
            make_tree(
                "R",
                TreeNode("R", ("A", "B")),
                TreeNode("A", ("C",)),
                TreeNode("B", ("C",)),
                TreeNode("C", utility=0),
            ),
            "multiple_parents",
        )

    def test_08_disconnected_cycle_is_detected(self):
        self.assertValidationCode(
            make_tree(
                "R",
                TreeNode("R", utility=0),
                TreeNode("X", ("Y",)),
                TreeNode("Y", ("X",)),
            ),
            "cycle",
        )

    def test_09_unreachable_node_fails_closed(self):
        self.assertValidationCode(
            make_tree(
                "R",
                TreeNode("R", utility=0),
                TreeNode("X", utility=1),
            ),
            "unreachable",
        )

    def test_10_terminal_requires_finite_numeric_utility(self):
        self.assertValidationCode(make_tree("R", TreeNode("R")), "missing_utility")
        for bad in (True, math.inf, -math.inf, math.nan, "3"):
            with self.subTest(utility=bad):
                self.assertValidationCode(
                    make_tree("R", TreeNode("R", utility=bad)),  # type: ignore[arg-type]
                    "invalid_utility",
                )

    def test_11_nonterminal_cannot_supply_terminal_utility(self):
        self.assertValidationCode(
            make_tree(
                "R",
                TreeNode("R", ("A",), utility=5),
                TreeNode("A", utility=1),
            ),
            "nonterminal_utility",
        )

    def test_12_simple_backup_has_known_exact_result(self):
        mm = minimax(scenario("simple_backup"))
        self.assertEqual(mm.root_value, 4.0)
        self.assertEqual(mm.selected_child, "B")
        self.assertEqual(mm.optimal_children, ("B",))
        self.assertEqual(mm.evaluated_leaves, ("A1", "A2", "B1", "B2"))
        self.assertEqual(mm.pruned_nodes, ())

    def test_13_greedy_trap_requires_opponent_backup(self):
        mm = minimax(scenario("greedy_trap"))
        self.assertEqual(mm.root_value, 2.0)
        self.assertEqual(mm.selected_child, "B")
        returns = dict(mm.node_returns)
        self.assertEqual(returns["A"], -4.0)
        self.assertEqual(returns["B"], 2.0)

    def test_14_alpha_beta_matches_minimax_on_every_frozen_scenario(self):
        for name in (
            "simple_backup",
            "greedy_trap",
            "first_prune",
            "good_ordering",
            "poor_ordering",
            "no_prune",
            "tied_optimum",
            "deep_cutoff",
            "boundary_terminal",
            "boundary_chain",
            "boundary_unbalanced",
        ):
            with self.subTest(scenario=name):
                mm, ab = self.assertSameRootDecision(scenario(name))
                self.assertLessEqual(len(ab.evaluated_leaves), len(mm.evaluated_leaves))

    def test_15_first_prune_skips_the_actual_subtree(self):
        mm, ab = self.assertSameRootDecision(scenario("first_prune"))
        self.assertEqual(mm.evaluated_leaves, ("A1", "A2", "B1", "B2"))
        self.assertEqual(ab.evaluated_leaves, ("A1", "A2", "B1"))
        self.assertEqual(ab.pruned_nodes, ("B2",))
        self.assertNotIn("B2", ab.visited_nodes)

    def test_16_every_prune_event_has_a_valid_cutoff(self):
        for name in ("first_prune", "good_ordering", "tied_optimum", "deep_cutoff"):
            with self.subTest(scenario=name):
                ab = alpha_beta(scenario(name))
                prune_events = [event for event in ab.trace if event.event == "prune"]
                self.assertTrue(prune_events)
                for event in prune_events:
                    self.assertIsNotNone(event.alpha)
                    self.assertIsNotNone(event.beta)
                    self.assertGreaterEqual(event.alpha, event.beta)
                    self.assertTrue(event.pruned)

    def test_17_good_move_order_reduces_work_without_changing_value(self):
        good_mm, good_ab = self.assertSameRootDecision(scenario("good_ordering"))
        poor_mm, poor_ab = self.assertSameRootDecision(scenario("poor_ordering"))
        self.assertEqual(good_mm.root_value, poor_mm.root_value)
        self.assertEqual(set(good_mm.optimal_children or ()), set(poor_mm.optimal_children or ()))
        self.assertLess(len(good_ab.evaluated_leaves), len(poor_ab.evaluated_leaves))
        self.assertEqual(len(good_ab.evaluated_leaves), 4)
        self.assertEqual(len(poor_ab.evaluated_leaves), 6)

    def test_18_valid_tree_can_offer_no_pruning_opportunity(self):
        mm, ab = self.assertSameRootDecision(scenario("no_prune"))
        self.assertEqual(len(ab.evaluated_leaves), len(mm.evaluated_leaves))
        self.assertEqual(ab.pruned_nodes, ())

    def test_19_tie_break_is_not_misreported_as_unique_optimum(self):
        mm, ab = self.assertSameRootDecision(scenario("tied_optimum"))
        self.assertEqual(mm.optimal_children, ("A", "B"))
        self.assertEqual(mm.selected_child, "A")
        self.assertEqual(ab.selected_child, "A")
        self.assertIsNone(ab.optimal_children)

    def test_20_terminal_root_and_chain_boundaries(self):
        terminal_mm, terminal_ab = self.assertSameRootDecision(scenario("boundary_terminal"))
        self.assertEqual(terminal_mm.root_value, -2.0)
        self.assertIsNone(terminal_mm.selected_child)
        self.assertEqual(terminal_mm.optimal_children, ())
        self.assertIsNone(terminal_ab.optimal_children)

        chain_mm, chain_ab = self.assertSameRootDecision(scenario("boundary_chain"))
        self.assertEqual(chain_mm.root_value, 7.0)
        self.assertEqual(chain_ab.root_value, 7.0)
        self.assertEqual(chain_mm.evaluated_leaves, ("C",))

    def test_21_unbalanced_negative_zero_positive_tree(self):
        mm, ab = self.assertSameRootDecision(scenario("boundary_unbalanced"))
        self.assertEqual(mm.root_value, 1.0)
        self.assertEqual(mm.selected_child, "A")
        self.assertIn("D", ab.pruned_nodes)
        self.assertTrue({"D", "F", "G"}.issubset(set(ab.pruned_nodes)))

    def test_22_alpha_updates_are_monotone_per_node(self):
        for name in ("first_prune", "good_ordering", "deep_cutoff"):
            with self.subTest(scenario=name):
                ab = alpha_beta(scenario(name))
                per_node: dict[str, list[float]] = {}
                for event in ab.trace:
                    if event.event == "alpha_update":
                        self.assertIsNotNone(event.alpha)
                        per_node.setdefault(event.node_id, []).append(event.alpha)
                for values in per_node.values():
                    self.assertEqual(values, sorted(values))

    def test_23_beta_updates_are_monotone_per_node(self):
        for name in ("first_prune", "good_ordering", "deep_cutoff"):
            with self.subTest(scenario=name):
                ab = alpha_beta(scenario(name))
                per_node: dict[str, list[float]] = {}
                for event in ab.trace:
                    if event.event == "beta_update":
                        self.assertIsNotNone(event.beta)
                        per_node.setdefault(event.node_id, []).append(event.beta)
                for values in per_node.values():
                    self.assertEqual(values, sorted(values, reverse=True))

    def test_24_pruned_nodes_are_never_visited(self):
        for name in ("first_prune", "good_ordering", "tied_optimum", "deep_cutoff", "boundary_unbalanced"):
            with self.subTest(scenario=name):
                ab = alpha_beta(scenario(name))
                self.assertTrue(set(ab.pruned_nodes).isdisjoint(ab.visited_nodes))

    def test_25_serialization_and_replay_are_exactly_deterministic(self):
        tree = scenario("deep_cutoff")
        first = alpha_beta(tree)
        second = alpha_beta(tree)
        self.assertEqual(first, second)
        self.assertEqual(result_to_dict(first), result_to_dict(second))
        self.assertEqual(tree_to_dict(tree), tree_to_dict(scenario("deep_cutoff")))
        self.assertNotIn(math.inf, result_to_dict(first)["trace"])

    def test_26_bounded_exhaustive_census(self):
        utility_alphabet = (-1, 0, 1)
        cases = 0
        value_mismatches = 0
        selection_mismatches = 0
        alpha_more_leaves = 0
        cutoff_violations = 0
        pruned_visited_overlap = 0
        replay_mismatches = 0

        for utilities in itertools.product(utility_alphabet, repeat=4):
            for order_mask in range(8):
                tree = complete_binary_tree(utilities, order_mask)
                mm = minimax(tree)
                ab = alpha_beta(tree)
                cases += 1
                if mm.root_value != ab.root_value:
                    value_mismatches += 1
                if mm.selected_child != ab.selected_child:
                    selection_mismatches += 1
                if len(ab.evaluated_leaves) > len(mm.evaluated_leaves):
                    alpha_more_leaves += 1
                if set(ab.pruned_nodes) & set(ab.visited_nodes):
                    pruned_visited_overlap += 1
                for event in ab.trace:
                    if event.event == "prune" and (
                        event.alpha is None
                        or event.beta is None
                        or event.alpha < event.beta
                    ):
                        cutoff_violations += 1
                if ab != alpha_beta(tree):
                    replay_mismatches += 1

        self.assertEqual(cases, 648)
        self.assertEqual(value_mismatches, 0)
        self.assertEqual(selection_mismatches, 0)
        self.assertEqual(alpha_more_leaves, 0)
        self.assertEqual(cutoff_violations, 0)
        self.assertEqual(pruned_visited_overlap, 0)
        self.assertEqual(replay_mismatches, 0)


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(MinimaxAlphaBetaTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    payload = {
        "harness": "tools/test_minimax_alpha_beta.py",
        "testsRun": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "censusCases": 648,
        "pass": result.wasSuccessful(),
    }
    print(json.dumps(payload, indent=2))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
