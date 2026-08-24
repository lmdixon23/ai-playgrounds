#!/usr/bin/env python3
"""Cross-runtime parity gate for Lab 13's Python and JavaScript models."""

from __future__ import annotations

import json
import math
import pathlib
import subprocess
import sys

from transformer_language_model_reference import forward_tokens

ROOT = pathlib.Path(__file__).resolve().parents[1]
JS_CORE = ROOT / "tools" / "transformer_language_model_core.js"


def js_forward(tokens, *, use_positions=True, causal_mask=True, temperature=1.0):
    payload = json.dumps(
        {
            "tokens": list(tokens),
            "options": {
                "usePositions": use_positions,
                "causalMask": causal_mask,
                "temperature": temperature,
            },
        }
    )
    code = f"""
const core=require({json.dumps(str(JS_CORE))});
const payload={payload};
process.stdout.write(JSON.stringify(core.forwardTokens(payload.tokens,payload.options)));
"""
    proc = subprocess.run(
        ["node", "-e", code],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
    )
    if proc.returncode:
        raise RuntimeError(proc.stderr or proc.stdout)
    return json.loads(proc.stdout)


def assert_close(actual, expected, path="root", tol=1e-12):
    if expected is None or actual is None:
        if actual != expected:
            raise AssertionError(f"{path}: {actual!r} != {expected!r}")
        return
    if isinstance(expected, bool):
        if actual is not expected:
            raise AssertionError(f"{path}: {actual!r} != {expected!r}")
        return
    if isinstance(expected, (int, float)) and not isinstance(expected, bool):
        if not isinstance(actual, (int, float)):
            raise AssertionError(f"{path}: expected numeric, got {type(actual).__name__}")
        if not math.isclose(float(actual), float(expected), rel_tol=tol, abs_tol=tol):
            raise AssertionError(f"{path}: {actual!r} != {expected!r}")
        return
    if isinstance(expected, (list, tuple)):
        if len(actual) != len(expected):
            raise AssertionError(f"{path}: length {len(actual)} != {len(expected)}")
        for index, (a, e) in enumerate(zip(actual, expected, strict=True)):
            assert_close(a, e, f"{path}[{index}]", tol=tol)
        return
    if actual != expected:
        raise AssertionError(f"{path}: {actual!r} != {expected!r}")


def python_payload(tokens, *, use_positions=True, causal_mask=True, temperature=1.0):
    result = forward_tokens(
        tokens,
        use_positions=use_positions,
        causal_mask=causal_mask,
        temperature=temperature,
    )
    return {
        "tokens": list(result.tokens),
        "tokenIds": list(result.token_ids),
        "inputs": result.inputs,
        "queries": result.queries,
        "keys": result.keys,
        "values": result.values,
        "rawScores": result.raw_scores,
        "maskedScores": result.masked_scores,
        "attention": result.attention,
        "attentionOutputs": result.attention_outputs,
        "residual1": result.residual1,
        "feedForward": result.feed_forward,
        "finalStates": result.final_states,
        "logits": result.logits,
        "probabilities": result.probabilities,
        "temperature": result.temperature,
        "causalMask": result.causal_mask,
        "usePositions": result.use_positions,
    }


def run_case(name, tokens, **options):
    py = python_payload(tokens, **options)
    js = js_forward(tokens, **options)
    assert_close(js, py, path=name, tol=1e-11)


def main() -> int:
    cases = [
        ("canonical", ("<BOS>", "i", "like", "cats"), {}),
        ("substitution", ("<BOS>", "i", "like", "dogs"), {}),
        ("no_positions", ("<BOS>", "like", "i", "cats"), {"use_positions": False}),
        ("no_mask", ("<BOS>", "i", "like", "cats"), {"causal_mask": False}),
        ("cold_temperature", ("<BOS>", "i", "like", "cats"), {"temperature": 0.5}),
        ("hot_temperature", ("<BOS>", "i", "like", "cats"), {"temperature": 2.0}),
        ("single_token", ("<BOS>",), {}),
        ("unknown_token", ("<BOS>", "not-in-vocab", "cats"), {}),
    ]

    failures = []
    for name, tokens, options in cases:
        try:
            run_case(name, tokens, **options)
            print(f"PASS {name}")
        except Exception as exc:
            failures.append(f"{name}: {type(exc).__name__}: {exc}")
            print(f"FAIL {name}: {exc}", file=sys.stderr)

    payload = {
        "harness": "tools/test_transformer_cross_runtime.py",
        "cases": len(cases),
        "passed": len(cases) - len(failures),
        "failed": len(failures),
        "pass": not failures,
        "failures": failures,
    }
    print(json.dumps(payload, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
