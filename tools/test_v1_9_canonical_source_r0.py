#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import build_current as current


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "release-evidence" / "v1.9-canonical-source-r0.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def test_hash_comparator() -> int:
    checks = 0

    exact = current.compare_hash_maps({"a": "1", "b": "2"}, {"a": "1", "b": "2"})
    require(exact["pass"], "exact hash maps should pass")
    require(exact["added"] == [] and exact["removed"] == [] and exact["changed"] == [], "exact comparison diagnostics wrong")
    checks += 1

    changed = current.compare_hash_maps({"a": "1"}, {"a": "9"})
    require(not changed["pass"] and changed["changed"] == ["a"], "changed byte must fail")
    checks += 1

    added = current.compare_hash_maps({"a": "1"}, {"a": "1", "b": "2"})
    require(not added["pass"] and added["added"] == ["b"], "added artifact must fail")
    checks += 1

    removed = current.compare_hash_maps({"a": "1", "b": "2"}, {"a": "1"})
    require(not removed["pass"] and removed["removed"] == ["b"], "removed artifact must fail")
    checks += 1

    return checks


def test_current_product() -> int:
    checks = 0
    model = current.validate_product_model()
    require(model["lab_count"] == 15, "canonical lab count is not 15")
    require(model["foundation_count"] == 13, "foundation count is not 13")
    require(model["modern_count"] == 2, "modern-extension count is not 2")
    require(model["quick_assign_count"] == 15, "active Quick Assign count is not 15")
    require(model["slugs"] == [row["slug"] for row in model["labs"]], "canonical slug ordering drift")
    checks += 5

    current.build_current()
    require(EVIDENCE.is_file(), "R0 evidence file was not generated")
    payload = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    require(payload.get("phase") == "v1.9-r0-equivalence", "R0 evidence phase mismatch")
    require(payload.get("baseline_source_sha") == current.BASELINE_SHA, "R0 evidence baseline SHA mismatch")
    require(payload.get("artifact", {}).get("pass") is True, "byte-equivalence oracle did not pass")
    require(payload.get("artifact", {}).get("actual_files") == 58, "R0 generated file count is not 58")
    require(payload.get("catalogue", {}).get("pass") is True, "canonical/emitted catalogue parity did not pass")
    require(payload.get("catalogue", {}).get("rows") == 15, "emitted catalogue row count is not 15")
    checks += 6

    actual = current.artifact_hashes()
    oracle = current.load_json(current.ORACLE)
    final_compare = current.compare_hash_maps(oracle, actual)
    require(final_compare["pass"], f"post-build oracle mismatch: {final_compare}")
    checks += 1

    return checks


def main() -> int:
    checks = test_hash_comparator() + test_current_product()
    print(f"V1.9 CANONICAL SOURCE R0: PASS ({checks} checks; 58 public files byte-locked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
