"use strict";

/*
 * Independent JavaScript implementation for Lab 15: Minimax and Alpha-Beta.
 *
 * This file intentionally does not import, transpile, or generate code from the
 * Python reference. Both runtimes implement the same frozen data/trace contract
 * independently so cross-runtime parity can detect drift.
 */

const MAX_PLAYER = "MAX";
const MIN_PLAYER = "MIN";

class TreeValidationError extends Error {
  constructor(code, message) {
    super(message);
    this.name = "TreeValidationError";
    this.code = code;
  }
}

function playerForDepth(depth) {
  if (!Number.isInteger(depth) || depth < 0) {
    throw new Error("depth must be a non-negative integer");
  }
  return depth % 2 === 0 ? MAX_PLAYER : MIN_PLAYER;
}

function copyNode(node) {
  return {
    id: node.id,
    children: Array.isArray(node.children) ? [...node.children] : [],
    utility: node.utility === undefined ? null : node.utility,
    label: node.label === undefined ? null : node.label,
  };
}

function validateTree(tree) {
  if (!tree || typeof tree.root !== "string" || tree.root.length === 0) {
    throw new TreeValidationError("missing_root", "root id must be a non-empty string");
  }
  if (!Array.isArray(tree.nodes)) {
    throw new TreeValidationError("missing_root", "tree nodes must be an array");
  }

  const byId = new Map();
  for (const raw of tree.nodes) {
    const node = copyNode(raw);
    if (typeof node.id !== "string" || node.id.length === 0) {
      throw new TreeValidationError("invalid_id", "every node id must be a non-empty string");
    }
    if (byId.has(node.id)) {
      throw new TreeValidationError("duplicate_id", `duplicate node id: ${node.id}`);
    }
    byId.set(node.id, node);
  }

  if (!byId.has(tree.root)) {
    throw new TreeValidationError("missing_root", `root node does not exist: ${tree.root}`);
  }

  for (const node of byId.values()) {
    if (new Set(node.children).size !== node.children.length) {
      throw new TreeValidationError("duplicate_child", `node ${node.id} repeats a child`);
    }
    const terminal = node.children.length === 0;
    if (terminal) {
      if (node.utility === null) {
        throw new TreeValidationError("missing_utility", `terminal node ${node.id} lacks utility`);
      }
      if (typeof node.utility !== "number" || !Number.isFinite(node.utility)) {
        throw new TreeValidationError("invalid_utility", `terminal utility must be finite numeric: ${node.id}`);
      }
    } else if (node.utility !== null) {
      throw new TreeValidationError(
        "nonterminal_utility",
        `nonterminal node ${node.id} must not supply terminal utility`,
      );
    }
    for (const childId of node.children) {
      if (!byId.has(childId)) {
        throw new TreeValidationError(
          "missing_child",
          `node ${node.id} references missing child ${childId}`,
        );
      }
    }
  }

  const parentCount = new Map([...byId.keys()].map((id) => [id, 0]));
  for (const node of byId.values()) {
    for (const childId of node.children) {
      const count = parentCount.get(childId) + 1;
      parentCount.set(childId, count);
      if (count > 1) {
        throw new TreeValidationError("multiple_parents", `node ${childId} has more than one parent`);
      }
    }
  }

  if (parentCount.get(tree.root) !== 0) {
    throw new TreeValidationError("root_has_parent", "the configured root must not have a parent");
  }

  const color = new Map([...byId.keys()].map((id) => [id, 0]));
  function visitCycle(id) {
    if (color.get(id) === 1) {
      throw new TreeValidationError("cycle", `cycle detected at node ${id}`);
    }
    if (color.get(id) === 2) return;
    color.set(id, 1);
    for (const childId of byId.get(id).children) visitCycle(childId);
    color.set(id, 2);
  }
  for (const id of byId.keys()) {
    if (color.get(id) === 0) visitCycle(id);
  }

  const reachable = new Set();
  function mark(id) {
    if (reachable.has(id)) return;
    reachable.add(id);
    for (const childId of byId.get(id).children) mark(childId);
  }
  mark(tree.root);
  if (reachable.size !== byId.size) {
    const missing = [...byId.keys()].filter((id) => !reachable.has(id)).sort();
    throw new TreeValidationError("unreachable", `unreachable nodes: ${missing.join(", ")}`);
  }

  return byId;
}

function safeBound(value) {
  return Number.isFinite(value) ? value : null;
}

function subtreeIds(rootId, byId) {
  const out = [];
  function walk(id) {
    out.push(id);
    for (const childId of byId.get(id).children) walk(childId);
  }
  walk(rootId);
  return out;
}

function eventRecord(event, nodeId, depth, fields = {}) {
  return {
    event,
    node_id: nodeId,
    depth,
    player: playerForDepth(depth),
    child_id: fields.child_id ?? null,
    child_index: fields.child_index ?? null,
    value: fields.value ?? null,
    best: fields.best ?? null,
    alpha: fields.alpha ?? null,
    beta: fields.beta ?? null,
    pruned: fields.pruned ? [...fields.pruned] : [],
    visited_count: fields.visited_count ?? 0,
    evaluated_leaf_count: fields.evaluated_leaf_count ?? 0,
  };
}

function minimax(tree) {
  const byId = validateTree(tree);
  const visited = [];
  const leaves = [];
  const nodeReturns = {};
  const trace = [];

  function emit(event, id, depth, fields = {}) {
    trace.push(eventRecord(event, id, depth, {
      ...fields,
      alpha: null,
      beta: null,
      visited_count: visited.length,
      evaluated_leaf_count: leaves.length,
    }));
  }

  function solve(id, depth) {
    const node = byId.get(id);
    visited.push(id);
    emit("enter", id, depth);

    if (node.children.length === 0) {
      const value = Number(node.utility);
      leaves.push(id);
      nodeReturns[id] = value;
      emit("leaf", id, depth, { value, best: value });
      emit("return", id, depth, { value, best: value });
      return value;
    }

    const maximizing = playerForDepth(depth) === MAX_PLAYER;
    let best = maximizing ? -Infinity : Infinity;
    node.children.forEach((childId, index) => {
      const childValue = solve(childId, depth + 1);
      emit("child_return", id, depth, {
        child_id: childId,
        child_index: index,
        value: childValue,
        best: Number.isFinite(best) ? best : null,
      });
      const better = maximizing ? childValue > best : childValue < best;
      if (better) {
        best = childValue;
        emit("best_update", id, depth, {
          child_id: childId,
          child_index: index,
          value: childValue,
          best,
        });
      }
    });

    nodeReturns[id] = best;
    emit("return", id, depth, { value: best, best });
    return best;
  }

  const rootValue = solve(tree.root, 0);
  const root = byId.get(tree.root);
  let optimalChildren = [];
  let selectedChild = null;
  if (root.children.length) {
    optimalChildren = root.children.filter(
      (childId) => Object.prototype.hasOwnProperty.call(nodeReturns, childId)
        && nodeReturns[childId] === rootValue,
    );
    selectedChild = optimalChildren[0];
  }

  return {
    algorithm: "minimax",
    root_value: rootValue,
    selected_child: selectedChild,
    optimal_children: optimalChildren,
    visited_nodes: visited,
    evaluated_leaves: leaves,
    pruned_nodes: [],
    node_returns: nodeReturns,
    trace,
  };
}

function alphaBeta(tree) {
  const byId = validateTree(tree);
  const visited = [];
  const leaves = [];
  const pruned = [];
  const nodeReturns = {};
  const trace = [];

  function emit(event, id, depth, alpha, beta, fields = {}) {
    trace.push(eventRecord(event, id, depth, {
      ...fields,
      alpha: safeBound(alpha),
      beta: safeBound(beta),
      visited_count: visited.length,
      evaluated_leaf_count: leaves.length,
    }));
  }

  function solve(id, depth, alphaIn, betaIn) {
    let alpha = alphaIn;
    let beta = betaIn;
    const node = byId.get(id);
    visited.push(id);
    emit("enter", id, depth, alpha, beta);

    if (node.children.length === 0) {
      const value = Number(node.utility);
      leaves.push(id);
      nodeReturns[id] = value;
      emit("leaf", id, depth, alpha, beta, { value, best: value });
      emit("return", id, depth, alpha, beta, { value, best: value });
      return value;
    }

    const maximizing = playerForDepth(depth) === MAX_PLAYER;
    let best = maximizing ? -Infinity : Infinity;

    for (let index = 0; index < node.children.length; index += 1) {
      const childId = node.children[index];
      const childValue = solve(childId, depth + 1, alpha, beta);
      emit("child_return", id, depth, alpha, beta, {
        child_id: childId,
        child_index: index,
        value: childValue,
        best: Number.isFinite(best) ? best : null,
      });

      const better = maximizing ? childValue > best : childValue < best;
      if (better) {
        best = childValue;
        emit("best_update", id, depth, alpha, beta, {
          child_id: childId,
          child_index: index,
          value: childValue,
          best,
        });
      }

      if (maximizing) {
        const updated = Math.max(alpha, best);
        if (updated !== alpha) {
          alpha = updated;
          emit("alpha_update", id, depth, alpha, beta, {
            child_id: childId,
            child_index: index,
            value: childValue,
            best,
          });
        }
      } else {
        const updated = Math.min(beta, best);
        if (updated !== beta) {
          beta = updated;
          emit("beta_update", id, depth, alpha, beta, {
            child_id: childId,
            child_index: index,
            value: childValue,
            best,
          });
        }
      }

      if (alpha >= beta && index + 1 < node.children.length) {
        const skipped = [];
        for (const siblingId of node.children.slice(index + 1)) {
          skipped.push(...subtreeIds(siblingId, byId));
        }
        pruned.push(...skipped);
        emit("prune", id, depth, alpha, beta, {
          child_id: childId,
          child_index: index,
          value: childValue,
          best,
          pruned: skipped,
        });
        break;
      }
    }

    nodeReturns[id] = best;
    emit("return", id, depth, alpha, beta, { value: best, best });
    return best;
  }

  const rootValue = solve(tree.root, 0, -Infinity, Infinity);
  const root = byId.get(tree.root);
  let selectedChild = null;
  if (root.children.length) {
    const updates = trace.filter(
      (entry) => entry.event === "best_update" && entry.node_id === tree.root,
    );
    selectedChild = updates.length ? updates[updates.length - 1].child_id : root.children[0];
  }

  return {
    algorithm: "alpha_beta",
    root_value: rootValue,
    selected_child: selectedChild,
    optimal_children: null,
    visited_nodes: visited,
    evaluated_leaves: leaves,
    pruned_nodes: pruned,
    node_returns: nodeReturns,
    trace,
  };
}

function node(id, children = [], utility = null, label = null) {
  return { id, children: [...children], utility, label };
}

function tree(root, rows) {
  return {
    root,
    nodes: rows.map(([id, children, utility]) => node(id, children, utility)),
  };
}

const SCENARIOS = {
  simple_backup: () => tree("R", [
    ["R", ["A", "B"], null],
    ["A", ["A1", "A2"], null],
    ["B", ["B1", "B2"], null],
    ["A1", [], 3], ["A2", [], 5], ["B1", [], 4], ["B2", [], 6],
  ]),
  greedy_trap: () => tree("R", [
    ["R", ["A", "B"], null],
    ["A", ["A1", "A2"], null],
    ["B", ["B1", "B2"], null],
    ["A1", [], 9], ["A2", [], -4], ["B1", [], 2], ["B2", [], 3],
  ]),
  first_prune: () => tree("R", [
    ["R", ["A", "B"], null],
    ["A", ["A1", "A2"], null],
    ["B", ["B1", "B2"], null],
    ["A1", [], 5], ["A2", [], 6], ["B1", [], 4], ["B2", [], 9],
  ]),
  good_ordering: () => tree("R", [
    ["R", ["A", "B", "C"], null],
    ["A", ["A1", "A2"], null],
    ["B", ["B1", "B2"], null],
    ["C", ["C1", "C2"], null],
    ["A1", [], 8], ["A2", [], 9],
    ["B1", [], 7], ["B2", [], 10],
    ["C1", [], 6], ["C2", [], 11],
  ]),
  poor_ordering: () => tree("R", [
    ["R", ["C", "B", "A"], null],
    ["A", ["A2", "A1"], null],
    ["B", ["B2", "B1"], null],
    ["C", ["C2", "C1"], null],
    ["A1", [], 8], ["A2", [], 9],
    ["B1", [], 7], ["B2", [], 10],
    ["C1", [], 6], ["C2", [], 11],
  ]),
  no_prune: () => tree("R", [
    ["R", ["A", "B"], null],
    ["A", ["A1", "A2"], null],
    ["B", ["B1", "B2"], null],
    ["A1", [], 1], ["A2", [], 2], ["B1", [], 3], ["B2", [], 4],
  ]),
  tied_optimum: () => tree("R", [
    ["R", ["A", "B", "C"], null],
    ["A", ["A1", "A2"], null],
    ["B", ["B1", "B2"], null],
    ["C", ["C1", "C2"], null],
    ["A1", [], 5], ["A2", [], 7],
    ["B1", [], 5], ["B2", [], 8],
    ["C1", [], 4], ["C2", [], 9],
  ]),
  deep_cutoff: () => tree("R", [
    ["R", ["A", "B"], null],
    ["A", ["A1", "A2"], null],
    ["B", ["B1", "B2"], null],
    ["A1", ["A11", "A12"], null],
    ["A2", ["A21", "A22"], null],
    ["B1", ["B11", "B12"], null],
    ["B2", ["B21", "B22"], null],
    ["A11", [], 5], ["A12", [], 6],
    ["A21", [], 7], ["A22", [], 4],
    ["B11", [], 3], ["B12", [], 2],
    ["B21", [], 9], ["B22", [], 8],
  ]),
  boundary_terminal: () => tree("R", [["R", [], -2]]),
  boundary_chain: () => tree("R", [
    ["R", ["A"], null],
    ["A", ["B"], null],
    ["B", ["C"], null],
    ["C", [], 7],
  ]),
  boundary_unbalanced: () => tree("R", [
    ["R", ["A", "B"], null],
    ["A", [], 1],
    ["B", ["C", "D"], null],
    ["C", ["E"], null],
    ["D", ["F", "G"], null],
    ["E", [], -2],
    ["F", [], 0],
    ["G", [], 3],
  ]),
};

function scenario(name) {
  if (!Object.prototype.hasOwnProperty.call(SCENARIOS, name)) {
    throw new Error(`unknown Lab 15 scenario: ${name}`);
  }
  return SCENARIOS[name]();
}

function invalidFixtures() {
  return {
    missing_root: { root: "missing", nodes: [node("R", [], 0)] },
    duplicate_id: { root: "R", nodes: [node("R", [], 0), node("R", [], 1)] },
    missing_child: { root: "R", nodes: [node("R", ["X"], null)] },
    duplicate_child: { root: "R", nodes: [node("R", ["A", "A"], null), node("A", [], 1)] },
    root_has_parent: { root: "R", nodes: [node("R", ["A"], null), node("A", ["R"], null)] },
    multiple_parents: {
      root: "R",
      nodes: [
        node("R", ["A", "B"], null),
        node("A", ["C"], null),
        node("B", ["C"], null),
        node("C", [], 0),
      ],
    },
    cycle: {
      root: "R",
      nodes: [node("R", [], 0), node("X", ["Y"], null), node("Y", ["X"], null)],
    },
    unreachable: { root: "R", nodes: [node("R", [], 0), node("X", [], 1)] },
    missing_utility: { root: "R", nodes: [node("R", [], null)] },
    invalid_utility: { root: "R", nodes: [node("R", [], Number.POSITIVE_INFINITY)] },
    nonterminal_utility: {
      root: "R",
      nodes: [node("R", ["A"], 5), node("A", [], 1)],
    },
  };
}

function validationCode(input) {
  try {
    validateTree(input);
    return null;
  } catch (error) {
    if (error instanceof TreeValidationError) return error.code;
    throw error;
  }
}

function parityFixtures() {
  const scenarios = {};
  for (const name of Object.keys(SCENARIOS)) {
    const input = scenario(name);
    scenarios[name] = {
      tree: input,
      minimax: minimax(input),
      alpha_beta: alphaBeta(input),
    };
  }

  const invalid = {};
  for (const [name, input] of Object.entries(invalidFixtures())) {
    invalid[name] = validationCode(input);
  }

  return { scenarios, invalid };
}

module.exports = {
  MAX_PLAYER,
  MIN_PLAYER,
  TreeValidationError,
  playerForDepth,
  validateTree,
  minimax,
  alphaBeta,
  scenario,
  parityFixtures,
};
