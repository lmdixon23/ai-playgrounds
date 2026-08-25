#!/usr/bin/env python3
"""Cross-runtime parity gate for Lab 15 minimax and alpha-beta implementations."""

from __future__ import annotations

import json
import math
import pathlib
import subprocess
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import minimax_alpha_beta_reference as pyref

JS_CORE = ROOT / "tools" / "minimax_alpha_beta_core.js"


def python_invalid_fixtures() -> dict[str, pyref.GameTree]:
    T = pyref.TreeNode
    G = pyref.GameTree
    return {
        "missing_root": G("missing", (T("R", utility=0),)),
        "duplicate_id": G("R", (T("R", utility=0), T("R", utility=1))),
        "missing_child": G("R", (T("R", ("X",)),)),
        "duplicate_child": G("R", (T("R", ("A", "A")), T("A", utility=1))),
        "root_has_parent": G("R", (T("R", ("A",)), T("A", ("R",)))),
        "multiple_parents": G(
            "R",
            (
                T("R", ("A", "B")),
                T("A", ("C",)),
                T("B", ("C",)),
                T("C", utility=0),
            ),
        ),
        "cycle": G(
            "R",
            (
                T("R", utility=0),
                T("X", ("Y",)),
                T("Y", ("X",)),
            ),
        ),
        "unreachable": G("R", (T("R", utility=0), T("X", utility=1))),
        "missing_utility": G("R", (T("R"),)),
        "invalid_utility": G("R", (T("R", utility=math.inf),)),
        "nonterminal_utility": G(
            "R",
            (T("R", ("A",), utility=5), T("A", utility=1)),
        ),
    }


def validation_code(tree: pyref.GameTree) -> str | None:
    try:
        pyref.validate_tree(tree)
    except pyref.TreeValidationError as exc:
        return exc.code
    return None


def python_fixtures() -> dict[str, Any]:
    scenarios: dict[str, Any] = {}
    for name in pyref.SCENARIOS:
        tree = pyref.scenario(name)
        scenarios[name] = {
            "tree": pyref.tree_to_dict(tree),
            "minimax": pyref.result_to_dict(pyref.minimax(tree)),
            "alpha_beta": pyref.result_to_dict(pyref.alpha_beta(tree)),
        }

    invalid = {
        name: validation_code(tree)
        for name, tree in python_invalid_fixtures().items()
    }
    # Normalize tuples in dataclass-derived trace fields to JSON arrays before
    # comparing them with the independent JavaScript runtime.
    return json.loads(json.dumps({"scenarios": scenarios, "invalid": invalid}))


def javascript_fixtures() -> dict[str, Any]:
    script = (
        "const C=require(" + json.dumps(str(JS_CORE)) + ");"
        "process.stdout.write(JSON.stringify(C.parityFixtures()));"
    )
    proc = subprocess.run(
        ["node", "-e", script],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode:
        raise RuntimeError(proc.stderr or proc.stdout)
    return json.loads(proc.stdout)


def compare(expected: Any, actual: Any, path: str = "$") -> list[str]:
    failures: list[str] = []

    if isinstance(expected, bool) or isinstance(actual, bool):
        if expected is not actual:
            failures.append(f"{path}: {expected!r} != {actual!r}")
        return failures

    if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
        if not math.isclose(float(expected), float(actual), rel_tol=0.0, abs_tol=1e-12):
            failures.append(f"{path}: {expected!r} != {actual!r}")
        return failures

    if type(expected) is not type(actual):
        failures.append(
            f"{path}: type {type(expected).__name__} != {type(actual).__name__}"
        )
        return failures

    if isinstance(expected, dict):
        if set(expected) != set(actual):
            failures.append(
                f"{path}: key sets differ: {sorted(expected)} != {sorted(actual)}"
            )
            return failures
        for key in sorted(expected):
            failures.extend(compare(expected[key], actual[key], f"{path}.{key}"))
        return failures

    if isinstance(expected, list):
        if len(expected) != len(actual):
            failures.append(f"{path}: lengths differ: {len(expected)} != {len(actual)}")
            return failures
        for index, (left, right) in enumerate(zip(expected, actual, strict=True)):
            failures.extend(compare(left, right, f"{path}[{index}]"))
        return failures

    if expected != actual:
        failures.append(f"{path}: {expected!r} != {actual!r}")
    return failures


def main() -> int:
    harness_self_test = bool(
        compare(
            {"root_value": 1.0, "trace": [{"event": "return"}]},
            {"root_value": 2.0, "trace": [{"event": "return"}]},
        )
    )
    print(f"{'PASS' if harness_self_test else 'FAIL'} parity_harness_self_test")
    if not harness_self_test:
        return 1

    expected = python_fixtures()
    actual = javascript_fixtures()
    failures: list[dict[str, Any]] = []

    scenario_names = list(expected["scenarios"])
    for name in scenario_names:
        case_failures = compare(
            expected["scenarios"][name],
            actual.get("scenarios", {}).get(name),
            f"$.scenarios.{name}",
        )
        print(f"{'PASS' if not case_failures else 'FAIL'} scenario_{name}")
        if case_failures:
            failures.append({"case": name, "failures": case_failures[:30]})

    invalid_failures = compare(expected["invalid"], actual.get("invalid"), "$.invalid")
    print(f"{'PASS' if not invalid_failures else 'FAIL'} validation_categories")
    if invalid_failures:
        failures.append({"case": "validation_categories", "failures": invalid_failures[:30]})

    payload = {
        "harness": "tools/test_minimax_alpha_beta_cross_runtime.py",
        "harness_self_test": harness_self_test,
        "scenario_cases": len(scenario_names),
        "validation_cases": len(expected["invalid"]),
        "passed": len(scenario_names) + 1 - len(failures),
        "failed": len(failures),
        "pass": not failures,
        "failures": failures,
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
