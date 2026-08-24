#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import pathlib
import subprocess
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import agent_tool_context_reference as pyref

JS_CORE = ROOT / "tools" / "agent_tool_context_core.js"


def python_fixtures() -> dict[str, Any]:
    permission = pyref.new_state("Send a note", principal="assistant")
    permission = pyref.process_action(
        permission,
        pyref.tool_call(
            "mail.send",
            {"recipient": "teacher@example.edu", "body": "Hello"},
        ),
    )
    text = pyref.new_state("Check weather")
    text = pyref.process_action(
        text,
        pyref.text_action("I will call weather.current for Oslo."),
    )
    injection = pyref.new_state("Find the meeting note", principal="assistant")
    injection = pyref.process_action(
        injection,
        pyref.tool_call("notes.search", {"query": "meeting"}),
    )
    error = pyref.new_state(
        "Check current weather",
        context=[pyref.fact("city", "Atlantis", source="goal")],
    )
    error = pyref.process_action(
        error,
        pyref.tool_call("weather.current", {"city": "Atlantis"}),
    )
    initial = pyref.canonical_initial_state()
    pre_decision = pyref.choose_candidate(initial, pyref.canonical_candidates(initial))
    after_weather = pyref.process_action(initial, pre_decision["selected_action"])
    post_decision = pyref.choose_candidate(
        after_weather,
        pyref.canonical_candidates(after_weather),
    )
    return {
        "canonical": pyref.canonical_trace(),
        "missing_required": pyref.validate_tool_call(
            {"name": "calendar.create", "arguments": {"title": "Review"}}
        ),
        "permission": permission,
        "text_only": text,
        "injection": injection,
        "execution_error": error,
        "mcp": pyref.mcp_2026_07_28_envelope(
            {"name": "weather.current", "arguments": {"city": "Oslo"}}
        ),
        "candidate_transition": {
            "before": pre_decision,
            "after": post_decision,
        },
    }


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
        for index, (left, right) in enumerate(zip(expected, actual)):
            failures.extend(compare(left, right, f"{path}[{index}]"))
        return failures

    if expected != actual:
        failures.append(f"{path}: {expected!r} != {actual!r}")
    return failures


def main() -> int:
    harness_self_test = bool(compare({"x": 1.0}, {"x": 2.0}))
    print(f"{'PASS' if harness_self_test else 'FAIL'} parity_harness_self_test")
    if not harness_self_test:
        return 1

    expected = python_fixtures()
    actual = javascript_fixtures()
    all_failures: list[dict[str, Any]] = []

    for name in expected:
        failures = compare(expected[name], actual.get(name), f"$.{name}")
        print(f"{'PASS' if not failures else 'FAIL'} {name}")
        if failures:
            all_failures.append({"case": name, "failures": failures[:20]})

    payload = {
        "harness": "tools/test_agent_tool_context_cross_runtime.py",
        "harness_self_test": harness_self_test,
        "cases": len(expected),
        "passed": len(expected) - len(all_failures),
        "failed": len(all_failures),
        "pass": not all_failures,
        "failures": all_failures,
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
