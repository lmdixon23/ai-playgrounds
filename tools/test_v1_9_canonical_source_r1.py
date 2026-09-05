#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import build_current as current


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "release-evidence" / "v1.9-canonical-source-r1.json"
PUBLIC_CATALOGUE = ROOT / "_site" / "applets.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    checks = 0

    catalogue = current.load_canonical_catalogue()
    require(catalogue["serializer_roundtrip"] is True, "canonical catalogue serializer roundtrip failed")
    require(len(catalogue["rows"]) == 15, "canonical catalogue row count is not 15")
    require(sorted(catalogue["showcase_orders"]) == list(range(1, 16)), "showcase order is not 1..15")
    require(catalogue["sha256"] == current.load_json(current.ORACLE)["applets.json"], "canonical catalogue is not bound to frozen public applets.json digest")
    checks += 4

    rows = catalogue["rows"]
    require({row["slug"] for row in rows} == set(catalogue["slugs"]), "catalogue slug set drift")
    for row in rows:
        for suffix in ("zh", "vi", "es"):
            require(bool(row.get(f"title_{suffix}")), f"{row['slug']} missing title_{suffix}")
            require(bool(row.get(f"desc_{suffix}")), f"{row['slug']} missing desc_{suffix}")
            require(bool(row.get(f"featured_{suffix}")), f"{row['slug']} missing featured_{suffix}")
            require(bool(row.get(f"category_{suffix}")), f"{row['slug']} missing category_{suffix}")
        require(isinstance(row.get("keywords"), list) and len(row["keywords"]) > 0, f"{row['slug']} missing keywords")
    checks += 15 * 13

    model = current.validate_product_model()
    require(model["lab_count"] == 15, "canonical lab count is not 15")
    require(model["foundation_count"] == 13, "foundation count is not 13")
    require(model["modern_count"] == 2, "modern-extension count is not 2")
    require(model["quick_assign_count"] == 15, "Quick Assign count is not 15")
    require(model["release"].get("architecture_phase") == "v1.9-r1-canonical-catalogue", "release phase is not R1")
    checks += 5

    current.build_current()
    require(EVIDENCE.is_file(), "R1 evidence file was not generated")
    payload = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    require(payload.get("phase") == "v1.9-r1-canonical-catalogue", "R1 evidence phase mismatch")
    require(payload.get("baseline_source_sha") == current.BASELINE_SHA, "R1 baseline SHA mismatch")
    require(payload.get("serializer_roundtrip") is True, "R1 serializer evidence is not true")
    require(payload.get("legacy_handoff", {}).get("byte_identical") is True, "legacy/canonical catalogue handoff is not byte-identical")
    require(payload.get("artifact", {}).get("pass") is True, "58-file byte oracle did not pass")
    require(payload.get("artifact", {}).get("actual_files") == 58, "R1 generated file count is not 58")
    require(payload.get("catalogue", {}).get("pass") is True, "R1 catalogue gate did not pass")
    require(payload.get("catalogue", {}).get("rows") == 15, "R1 catalogue row count is not 15")
    checks += 8

    canonical_bytes = current.CATALOGUE.read_bytes()
    public_bytes = PUBLIC_CATALOGUE.read_bytes()
    require(public_bytes == canonical_bytes, "public applets.json is not exactly canonical catalogue bytes")
    require(hashlib.sha256(public_bytes).hexdigest() == catalogue["sha256"], "public catalogue digest differs from canonical source")
    checks += 2

    final_compare = current.compare_hash_maps(current.load_json(current.ORACLE), current.artifact_hashes())
    require(final_compare["pass"], f"post-R1 public artifact oracle mismatch: {final_compare}")
    checks += 1

    print(
        "V1.9 CANONICAL SOURCE R1: PASS — "
        f"{checks} checks; 15-row multilingual catalogue canonically owned; 58 public files byte-locked"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
