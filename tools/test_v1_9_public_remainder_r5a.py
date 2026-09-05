#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import build_current as current
import public_remainder
import test_v1_9_token_owned_components_r4b as r4b

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = {
    phase: ROOT / "release-evidence" / f"v1.9-canonical-source-{phase}.json"
    for phase in ("r0", "r1", "r2", "r3", "r4a", "r4b", "r5a")
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def test_public_remainder() -> int:
    checks = 0
    state = public_remainder.load_and_validate()
    require(state["manifest"]["phase"] == "v1.9-r5a-public-remainder-ownership", "R5a public-remainder phase drift")
    require(len(state["public_paths"]) == 43, "R5a public-remainder file count drift")
    require(state["counts"] == {"canonical_existing": 29, "current_snapshot": 14}, "R5a public-remainder ownership count drift")
    require(set(state["snapshot_public_paths"]) == public_remainder.EXPECTED_SNAPSHOT_PUBLIC_PATHS, "R5a snapshot ownership set drift")
    require(state["bytes"] == {"canonical_existing": 3036276, "current_snapshot": 603323, "total": 3639599}, "R5a public-remainder byte metrics drift")
    checks += 5

    oracle = current.load_json(current.ORACLE)
    page_paths = set(current.validate_product_model()["page_components"]["page_evidence"][slug]["public_path"] for slug in current.validate_product_model()["slugs"])
    require(set(state["public_paths"]) == set(oracle) - page_paths, "R5a remainder does not exactly complement canonical applet pages")
    require(len(set(state["public_paths"]) | page_paths) == 58, "R5a ownership map does not cover all 58 public files")
    checks += 2
    return checks


def test_product_model() -> int:
    checks = 0
    model = current.validate_product_model()
    release = model["release"]
    require(release["architecture_phase"] == "v1.9-r5a-public-remainder-ownership", "R5a release phase mismatch")
    require(release["public_remainder_manifest"] == "src/product/public-remainder.json", "R5a release remainder manifest drift")
    require(release["public_remainder_count"] == 43, "R5a release remainder count drift")
    require(release["canonical_existing_public_remainder_count"] == 29, "R5a release existing-owner count drift")
    require(release["current_snapshot_public_remainder_count"] == 14, "R5a release snapshot-owner count drift")
    require(release["legacy_equivalence_builder"] == "tools/build_site_v1_8_1.py", "R5a must retain historical builder only until R5b")
    require(model["public_remainder"]["counts"] == {"canonical_existing": 29, "current_snapshot": 14}, "R5a model ownership counts drift")
    require(model["page_components"]["phase"] == "v1.9-r4b-token-owned-components", "R5a must preserve R4b page subgraph phase")
    require(model["design_tokens"]["binding_phase"] == "v1.9-r4b-token-owned-components", "R5a must preserve R4b design-binding subgraph phase")
    require(model["lab_count"] == 15 and model["quick_assign_count"] == 15, "R5a product count boundary changed")
    require(model["foundation_count"] == 13 and model["modern_extension_count"] == 2, "R5a curriculum track boundary changed")
    checks += 11
    return checks


def test_current_build() -> int:
    checks = 0
    current.build_current()
    first_hashes = current.artifact_hashes()
    require(len(first_hashes) == 58, "first R5a build does not contain 58 public files")
    require(current.compare_to_oracle(first_hashes)["pass"], "first R5a build differs from frozen v1.8.1 oracle")
    checks += 2

    current.build_current()
    second_hashes = current.artifact_hashes()
    require(current.compare_hash_maps(first_hashes, second_hashes)["pass"], "two clean R5a builds from one SHA are not byte-identical")
    require(current.compare_to_oracle(second_hashes)["pass"], "second R5a build differs from frozen v1.8.1 oracle")
    checks += 2

    expected_phases = {
        "r0": "v1.9-r0-equivalence",
        "r1": "v1.9-r1-canonical-catalogue",
        "r2": "v1.9-r2-peer-current-pages",
        "r3": "v1.9-r3-shared-page-components",
        "r4a": "v1.9-r4a-design-token-contract",
        "r4b": "v1.9-r4b-token-owned-components",
        "r5a": "v1.9-r5a-public-remainder-ownership",
    }
    for key, path in EVIDENCE.items():
        require(path.is_file(), f"missing canonical-source evidence: {key}")
        payload = json.loads(path.read_text(encoding="utf-8"))
        require(payload.get("phase") == expected_phases[key], f"evidence phase mismatch: {key}")
        require(payload.get("artifact", {}).get("pass") is True, f"artifact oracle failed in evidence: {key}")
        checks += 3

    r4b_payload = json.loads(EVIDENCE["r4b"].read_text(encoding="utf-8"))
    require(r4b_payload["component_source_kinds"] == {"raw": 11, "token-template": 6}, "R4b component-source invariant regressed under R5a")
    require(r4b_payload["minimaxMismatchPreserved"] is True, "R4b Minimax safeguard regressed under R5a")
    checks += 2

    r5a_payload = json.loads(EVIDENCE["r5a"].read_text(encoding="utf-8"))
    require(r5a_payload["public_remainder_count"] == 43, "R5a evidence remainder count drift")
    require(r5a_payload["ownership_counts"] == {"canonical_existing": 29, "current_snapshot": 14}, "R5a evidence ownership count drift")
    require(set(r5a_payload["snapshot_public_paths"]) == public_remainder.EXPECTED_SNAPSHOT_PUBLIC_PATHS, "R5a evidence snapshot set drift")
    require(r5a_payload["historical_builder_role"] == "independent-current-build-equivalence-witness-until-r5b", "R5a evidence historical-builder role drift")
    checks += 4
    return checks


def main() -> int:
    checks = (
        r4b.test_hash_comparator()
        + r4b.test_token_resolver_fail_closed()
        + r4b.test_token_components()
        + r4b.test_page_graph()
        + r4b.test_design_contract()
        + test_public_remainder()
        + test_product_model()
        + test_current_build()
    )
    print(
        "V1.9 PUBLIC REMAINDER R5A: PASS — "
        f"{checks} checks; 43 non-applet files = 29 existing canonical + 14 exact current snapshots; "
        "15 canonical applet pages / two-build determinism / 58 public files byte-locked"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
