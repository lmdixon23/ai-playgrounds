#!/usr/bin/env python3
"""Deterministic reference model for Lab 15: Minimax and Alpha-Beta Pruning.

The model is deliberately small and game-agnostic. It evaluates finite,
deterministic, two-player, zero-sum, perfect-information game trees whose
terminal utilities are expressed from MAX's perspective.

The browser layer should replay the trace emitted here rather than implement a
second solver for animation.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Iterable, Mapping, Sequence

MAX_PLAYER = "MAX"
MIN_PLAYER = "MIN"


class TreeValidationError(ValueError):
    """Stable fail-closed validation error with a machine-readable category."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


@dataclass(frozen=True)
class TreeNode:
    id: str
    children: tuple[str, ...] = ()
    utility: float | int | None = None
    label: str | None = None


@dataclass(frozen=True)
class GameTree:
    root: str
    nodes: tuple[TreeNode, ...]


@dataclass(frozen=True)
class SearchEvent:
    event: str
    node_id: str
    depth: int
    player: str
    child_id: str | None = None
    child_index: int | None = None
    value: float | None = None
    best: float | None = None
    alpha: float | None = None
    beta: float | None = None
    pruned: tuple[str, ...] = ()
    visited_count: int = 0
    evaluated_leaf_count: int = 0


@dataclass(frozen=True)
class SearchResult:
    algorithm: str
    root_value: float
    selected_child: str | None
    # Minimax computes the complete exact root-optimal set. A pruned alpha-beta
    # trace need not establish every tied optimum, so it deliberately reports
    # None here rather than overclaiming completeness.
    optimal_children: tuple[str, ...] | None
    visited_nodes: tuple[str, ...]
    evaluated_leaves: tuple[str, ...]
    pruned_nodes: tuple[str, ...]
    # These are values returned by the traversal. In minimax they are exact for
    # every visited node; after an alpha-beta cutoff a non-root return may be a
    # sufficient bound rather than that node's independently completed minimax
    # value. The root return is exact.
    node_returns: tuple[tuple[str, float], ...]
    trace: tuple[SearchEvent, ...]


def player_for_depth(depth: int) -> str:
    if depth < 0:
        raise ValueError("depth must be non-negative")
    return MAX_PLAYER if depth % 2 == 0 else MIN_PLAYER


def validate_tree(tree: GameTree) -> dict[str, TreeNode]:
    if not isinstance(tree.root, str) or not tree.root:
        raise TreeValidationError("missing_root", "root id must be a non-empty string")

    by_id: dict[str, TreeNode] = {}
    for node in tree.nodes:
        if not isinstance(node.id, str) or not node.id:
            raise TreeValidationError("invalid_id", "every node id must be a non-empty string")
        if node.id in by_id:
            raise TreeValidationError("duplicate_id", f"duplicate node id: {node.id}")
        by_id[node.id] = node

    if tree.root not in by_id:
        raise TreeValidationError("missing_root", f"root node does not exist: {tree.root}")

    for node in tree.nodes:
        if len(set(node.children)) != len(node.children):
            raise TreeValidationError("duplicate_child", f"node {node.id} repeats a child")
        terminal = not node.children
        if terminal:
            if node.utility is None:
                raise TreeValidationError("missing_utility", f"terminal node {node.id} lacks utility")
            if isinstance(node.utility, bool) or not isinstance(node.utility, (int, float)):
                raise TreeValidationError("invalid_utility", f"terminal utility must be numeric: {node.id}")
            if not math.isfinite(float(node.utility)):
                raise TreeValidationError("invalid_utility", f"terminal utility must be finite: {node.id}")
        elif node.utility is not None:
            raise TreeValidationError(
                "nonterminal_utility",
                f"nonterminal node {node.id} must not supply terminal utility",
            )
        for child_id in node.children:
            if child_id not in by_id:
                raise TreeValidationError(
                    "missing_child",
                    f"node {node.id} references missing child {child_id}",
                )

    parent_count = {node_id: 0 for node_id in by_id}
    for node in tree.nodes:
        for child_id in node.children:
            parent_count[child_id] += 1
            if parent_count[child_id] > 1:
                raise TreeValidationError(
                    "multiple_parents",
                    f"node {child_id} has more than one parent",
                )

    if parent_count[tree.root]:
        raise TreeValidationError("root_has_parent", "the configured root must not have a parent")

    # Detect cycles in every connected component, including disconnected input.
    color = {node_id: 0 for node_id in by_id}

    def visit_cycle(node_id: str) -> None:
        if color[node_id] == 1:
            raise TreeValidationError("cycle", f"cycle detected at node {node_id}")
        if color[node_id] == 2:
            return
        color[node_id] = 1
        for child_id in by_id[node_id].children:
            visit_cycle(child_id)
        color[node_id] = 2

    for node_id in by_id:
        if color[node_id] == 0:
            visit_cycle(node_id)

    reachable: set[str] = set()

    def mark_reachable(node_id: str) -> None:
        if node_id in reachable:
            return
        reachable.add(node_id)
        for child_id in by_id[node_id].children:
            mark_reachable(child_id)

    mark_reachable(tree.root)
    if len(reachable) != len(by_id):
        missing = sorted(set(by_id) - reachable)
        raise TreeValidationError("unreachable", f"unreachable nodes: {', '.join(missing)}")

    return by_id


def _bound(value: float) -> float | None:
    """Serialize +/- infinity as None so traces remain JSON-safe."""
    return value if math.isfinite(value) else None


def _subtree_ids(root_id: str, by_id: Mapping[str, TreeNode]) -> tuple[str, ...]:
    out: list[str] = []

    def walk(node_id: str) -> None:
        out.append(node_id)
        for child_id in by_id[node_id].children:
            walk(child_id)

    walk(root_id)
    return tuple(out)


def _optimal_root_children(
    root: TreeNode,
    node_returns: Mapping[str, float],
    root_value: float,
) -> tuple[str, ...]:
    return tuple(
        child_id
        for child_id in root.children
        if child_id in node_returns and node_returns[child_id] == root_value
    )


def minimax(tree: GameTree) -> SearchResult:
    by_id = validate_tree(tree)
    visited: list[str] = []
    leaves: list[str] = []
    returns: dict[str, float] = {}
    trace: list[SearchEvent] = []

    def emit(
        event: str,
        node_id: str,
        depth: int,
        *,
        child_id: str | None = None,
        child_index: int | None = None,
        value: float | None = None,
        best: float | None = None,
    ) -> None:
        trace.append(
            SearchEvent(
                event=event,
                node_id=node_id,
                depth=depth,
                player=player_for_depth(depth),
                child_id=child_id,
                child_index=child_index,
                value=value,
                best=best,
                alpha=None,
                beta=None,
                visited_count=len(visited),
                evaluated_leaf_count=len(leaves),
            )
        )

    def solve(node_id: str, depth: int) -> float:
        node = by_id[node_id]
        visited.append(node_id)
        emit("enter", node_id, depth)

        if not node.children:
            value = float(node.utility)
            leaves.append(node_id)
            returns[node_id] = value
            emit("leaf", node_id, depth, value=value, best=value)
            emit("return", node_id, depth, value=value, best=value)
            return value

        maximizing = player_for_depth(depth) == MAX_PLAYER
        best = -math.inf if maximizing else math.inf

        for index, child_id in enumerate(node.children):
            child_value = solve(child_id, depth + 1)
            emit(
                "child_return",
                node_id,
                depth,
                child_id=child_id,
                child_index=index,
                value=child_value,
                best=None if not math.isfinite(best) else best,
            )
            better = child_value > best if maximizing else child_value < best
            if better:
                best = child_value
                emit(
                    "best_update",
                    node_id,
                    depth,
                    child_id=child_id,
                    child_index=index,
                    value=child_value,
                    best=best,
                )

        returns[node_id] = float(best)
        emit("return", node_id, depth, value=float(best), best=float(best))
        return float(best)

    root_value = solve(tree.root, 0)
    root = by_id[tree.root]
    if root.children:
        optimal = _optimal_root_children(root, returns, root_value)
        selected = optimal[0]
    else:
        optimal = ()
        selected = None

    return SearchResult(
        algorithm="minimax",
        root_value=root_value,
        selected_child=selected,
        optimal_children=optimal,
        visited_nodes=tuple(visited),
        evaluated_leaves=tuple(leaves),
        pruned_nodes=(),
        node_returns=tuple(returns.items()),
        trace=tuple(trace),
    )


def alpha_beta(tree: GameTree) -> SearchResult:
    by_id = validate_tree(tree)
    visited: list[str] = []
    leaves: list[str] = []
    pruned: list[str] = []
    returns: dict[str, float] = {}
    trace: list[SearchEvent] = []

    def emit(
        event: str,
        node_id: str,
        depth: int,
        alpha: float,
        beta: float,
        *,
        child_id: str | None = None,
        child_index: int | None = None,
        value: float | None = None,
        best: float | None = None,
        pruned_ids: Sequence[str] = (),
    ) -> None:
        trace.append(
            SearchEvent(
                event=event,
                node_id=node_id,
                depth=depth,
                player=player_for_depth(depth),
                child_id=child_id,
                child_index=child_index,
                value=value,
                best=best,
                alpha=_bound(alpha),
                beta=_bound(beta),
                pruned=tuple(pruned_ids),
                visited_count=len(visited),
                evaluated_leaf_count=len(leaves),
            )
        )

    def solve(node_id: str, depth: int, alpha: float, beta: float) -> float:
        node = by_id[node_id]
        visited.append(node_id)
        emit("enter", node_id, depth, alpha, beta)

        if not node.children:
            value = float(node.utility)
            leaves.append(node_id)
            returns[node_id] = value
            emit("leaf", node_id, depth, alpha, beta, value=value, best=value)
            emit("return", node_id, depth, alpha, beta, value=value, best=value)
            return value

        maximizing = player_for_depth(depth) == MAX_PLAYER
        best = -math.inf if maximizing else math.inf

        for index, child_id in enumerate(node.children):
            child_value = solve(child_id, depth + 1, alpha, beta)
            emit(
                "child_return",
                node_id,
                depth,
                alpha,
                beta,
                child_id=child_id,
                child_index=index,
                value=child_value,
                best=None if not math.isfinite(best) else best,
            )

            better = child_value > best if maximizing else child_value < best
            if better:
                best = child_value
                emit(
                    "best_update",
                    node_id,
                    depth,
                    alpha,
                    beta,
                    child_id=child_id,
                    child_index=index,
                    value=child_value,
                    best=best,
                )

            if maximizing:
                updated_alpha = max(alpha, best)
                if updated_alpha != alpha:
                    alpha = updated_alpha
                    emit(
                        "alpha_update",
                        node_id,
                        depth,
                        alpha,
                        beta,
                        child_id=child_id,
                        child_index=index,
                        value=child_value,
                        best=best,
                    )
            else:
                updated_beta = min(beta, best)
                if updated_beta != beta:
                    beta = updated_beta
                    emit(
                        "beta_update",
                        node_id,
                        depth,
                        alpha,
                        beta,
                        child_id=child_id,
                        child_index=index,
                        value=child_value,
                        best=best,
                    )

            if alpha >= beta and index + 1 < len(node.children):
                skipped: list[str] = []
                for sibling_id in node.children[index + 1 :]:
                    skipped.extend(_subtree_ids(sibling_id, by_id))
                pruned.extend(skipped)
                emit(
                    "prune",
                    node_id,
                    depth,
                    alpha,
                    beta,
                    child_id=child_id,
                    child_index=index,
                    value=child_value,
                    best=best,
                    pruned_ids=skipped,
                )
                break

        returns[node_id] = float(best)
        emit("return", node_id, depth, alpha, beta, value=float(best), best=float(best))
        return float(best)

    root_value = solve(tree.root, 0, -math.inf, math.inf)
    root = by_id[tree.root]

    if not root.children:
        selected = None
    else:
        # At the root, strict best updates plus stable child order provide the
        # deterministic optimal action even if later tied children are pruned
        # before their exact internal minimax values are established.
        root_best_events = [
            event for event in trace if event.event == "best_update" and event.node_id == tree.root
        ]
        selected = root_best_events[-1].child_id if root_best_events else root.children[0]

    return SearchResult(
        algorithm="alpha_beta",
        root_value=root_value,
        selected_child=selected,
        optimal_children=None,
        visited_nodes=tuple(visited),
        evaluated_leaves=tuple(leaves),
        pruned_nodes=tuple(pruned),
        node_returns=tuple(returns.items()),
        trace=tuple(trace),
    )


def tree_to_dict(tree: GameTree) -> dict[str, object]:
    return {
        "root": tree.root,
        "nodes": [
            {
                "id": node.id,
                "children": list(node.children),
                "utility": node.utility,
                "label": node.label,
            }
            for node in tree.nodes
        ],
    }


def result_to_dict(result: SearchResult) -> dict[str, object]:
    return {
        "algorithm": result.algorithm,
        "root_value": result.root_value,
        "selected_child": result.selected_child,
        "optimal_children": None
        if result.optimal_children is None
        else list(result.optimal_children),
        "visited_nodes": list(result.visited_nodes),
        "evaluated_leaves": list(result.evaluated_leaves),
        "pruned_nodes": list(result.pruned_nodes),
        "node_returns": {node_id: value for node_id, value in result.node_returns},
        "trace": [asdict(event) for event in result.trace],
    }


def _tree(root: str, rows: Iterable[tuple[str, Sequence[str], float | int | None]]) -> GameTree:
    return GameTree(
        root=root,
        nodes=tuple(
            TreeNode(node_id, tuple(children), utility)
            for node_id, children, utility in rows
        ),
    )


def scenario_simple_backup() -> GameTree:
    return _tree(
        "R",
        (
            ("R", ("A", "B"), None),
            ("A", ("A1", "A2"), None),
            ("B", ("B1", "B2"), None),
            ("A1", (), 3),
            ("A2", (), 5),
            ("B1", (), 4),
            ("B2", (), 6),
        ),
    )


def scenario_greedy_trap() -> GameTree:
    return _tree(
        "R",
        (
            ("R", ("A", "B"), None),
            ("A", ("A1", "A2"), None),
            ("B", ("B1", "B2"), None),
            ("A1", (), 9),
            ("A2", (), -4),
            ("B1", (), 2),
            ("B2", (), 3),
        ),
    )


def scenario_first_prune() -> GameTree:
    return _tree(
        "R",
        (
            ("R", ("A", "B"), None),
            ("A", ("A1", "A2"), None),
            ("B", ("B1", "B2"), None),
            ("A1", (), 5),
            ("A2", (), 6),
            ("B1", (), 4),
            ("B2", (), 9),
        ),
    )


def scenario_good_ordering() -> GameTree:
    return _tree(
        "R",
        (
            ("R", ("A", "B", "C"), None),
            ("A", ("A1", "A2"), None),
            ("B", ("B1", "B2"), None),
            ("C", ("C1", "C2"), None),
            ("A1", (), 8),
            ("A2", (), 9),
            ("B1", (), 7),
            ("B2", (), 10),
            ("C1", (), 6),
            ("C2", (), 11),
        ),
    )


def scenario_poor_ordering() -> GameTree:
    return _tree(
        "R",
        (
            ("R", ("C", "B", "A"), None),
            ("A", ("A2", "A1"), None),
            ("B", ("B2", "B1"), None),
            ("C", ("C2", "C1"), None),
            ("A1", (), 8),
            ("A2", (), 9),
            ("B1", (), 7),
            ("B2", (), 10),
            ("C1", (), 6),
            ("C2", (), 11),
        ),
    )


def scenario_no_prune() -> GameTree:
    return _tree(
        "R",
        (
            ("R", ("A", "B"), None),
            ("A", ("A1", "A2"), None),
            ("B", ("B1", "B2"), None),
            ("A1", (), 1),
            ("A2", (), 2),
            ("B1", (), 3),
            ("B2", (), 4),
        ),
    )


def scenario_tied_optimum() -> GameTree:
    return _tree(
        "R",
        (
            ("R", ("A", "B", "C"), None),
            ("A", ("A1", "A2"), None),
            ("B", ("B1", "B2"), None),
            ("C", ("C1", "C2"), None),
            ("A1", (), 5),
            ("A2", (), 7),
            ("B1", (), 5),
            ("B2", (), 8),
            ("C1", (), 4),
            ("C2", (), 9),
        ),
    )


def scenario_deep_cutoff() -> GameTree:
    return _tree(
        "R",
        (
            ("R", ("A", "B"), None),
            ("A", ("A1", "A2"), None),
            ("B", ("B1", "B2"), None),
            ("A1", ("A11", "A12"), None),
            ("A2", ("A21", "A22"), None),
            ("B1", ("B11", "B12"), None),
            ("B2", ("B21", "B22"), None),
            ("A11", (), 5),
            ("A12", (), 6),
            ("A21", (), 7),
            ("A22", (), 4),
            ("B11", (), 3),
            ("B12", (), 2),
            ("B21", (), 9),
            ("B22", (), 8),
        ),
    )


def scenario_boundary_terminal() -> GameTree:
    return _tree("R", (("R", (), -2),))


def scenario_boundary_chain() -> GameTree:
    return _tree(
        "R",
        (
            ("R", ("A",), None),
            ("A", ("B",), None),
            ("B", ("C",), None),
            ("C", (), 7),
        ),
    )


def scenario_boundary_unbalanced() -> GameTree:
    return _tree(
        "R",
        (
            ("R", ("A", "B"), None),
            ("A", (), 1),
            ("B", ("C", "D"), None),
            ("C", ("E",), None),
            ("D", ("F", "G"), None),
            ("E", (), -2),
            ("F", (), 0),
            ("G", (), 3),
        ),
    )


SCENARIOS = {
    "simple_backup": scenario_simple_backup,
    "greedy_trap": scenario_greedy_trap,
    "first_prune": scenario_first_prune,
    "good_ordering": scenario_good_ordering,
    "poor_ordering": scenario_poor_ordering,
    "no_prune": scenario_no_prune,
    "tied_optimum": scenario_tied_optimum,
    "deep_cutoff": scenario_deep_cutoff,
    "boundary_terminal": scenario_boundary_terminal,
    "boundary_chain": scenario_boundary_chain,
    "boundary_unbalanced": scenario_boundary_unbalanced,
}


def scenario(name: str) -> GameTree:
    try:
        factory = SCENARIOS[name]
    except KeyError as exc:
        raise KeyError(f"unknown Lab 15 scenario: {name}") from exc
    return factory()
