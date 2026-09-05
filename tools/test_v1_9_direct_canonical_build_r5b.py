#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import build_current as current
import direct_current_site
import public_remainder
import test_v1_9_token_owned_components_r4b as r4b

ROOT = Path(__file__).resolve().parents[1]
BUILD_SOURCE = ROOT / "tools" / "build_current.py"
HISTORICAL_BUILDER = ROOT / "tools" / "build_site_v1_8_1.py"
EVIDENCE = {
    phase: ROOT / "release-evidence" / f"v1.9-canonical-source-{phase}.json"
    for phase in ("r0", "r1", "r2", "r3", "r4a", "r4b", "r5a", "r5b")
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def test_public_remainder() -> int:
    checks = 0
    state = public_remainder.load_and_validate()
    require(state["manifest"]["phase"] == "v1.9-r5a-public-remainder-ownership", "R5b must preserve accepted R5a remainder phase")
    require(len(state["public_paths"]) == 43, "R5b remainder file count drift")
    require(state["counts"] == {"canonical_existing": 29, "current_snapshot": 14}, "R5b remainder ownership split drift")
    require(state["bytes"] == {"canonical_existing": 3036276, "current_snapshot": 603323, "total": 3639599}, "R5b remainder byte metrics drift")
    require(set(state["snapshot_public_paths"]) == public_remainder.EXPECTED_SNAPSHOT_PUBLIC_PATHS, "R5b snapshot ownership set drift")
    checks += 5
    return checks


def test_current_facade_independence() -> int:
    checks = 0
    source = BUILD_SOURCE.read_text(encoding="utf-8")
    forbidden_executable = (
        "from build_site_v",
        "import build_site_v",
        "build_legacy_v",
        "def handoff_catalogue",
        "def handoff_canonical_pages",
    )
    for needle in forbidden_executable:
        require(needle not in source, f"R5b current facade retained historical executable coupling: {needle}")
        checks += 1
    require("import direct_current_site" in source, "R5b current facade does not import direct composer")
    require("direct_current_site.build_direct(SITE)" in source, "R5b current facade does not invoke direct composer")
    require(HISTORICAL_BUILDER.is_file(), "Historical builder should remain available as test/provenance input during R5b")
    checks += 3
    return checks


def test_product_model() -> int:
    checks = 0
    model = current.validate_product_model()
    release = model["release"]
    require(release["architecture_phase"] == "v1.9-r5b-direct-canonical-build", "R5b release phase mismatch")
    require(release["direct_current_build"] is True, "R5b direct-current-build flag missing")
    require(release["current_build_composer"] == "tools/direct_current_site.py", "R5b composer ownership drift")
    require(release["historical_builder_role"] == "test-only-regression-and-provenance", "R5b historical builder role drift")
    require(release["public_remainder_manifest"] == "src/product/public-remainder.json", "R5b remainder manifest drift")
    require(release["public_remainder_count"] == 43, "R5b remainder count drift")
    require(model["page_components"]["phase"] == "v1.9-r4b-token-owned-components", "R5b must preserve R4b page subgraph phase")
    require(model["design_tokens"]["binding_phase"] == "v1.9-r4b-token-owned-components", "R5b must preserve R4b design-binding subgraph phase")
    require(model["public_remainder"]["manifest"]["phase"] == "v1.9-r5a-public-remainder-ownership", "R5b must preserve R5a remainder subgraph phase")
    require(model["lab_count"] == 15 and model["quick_assign_count"] == 15, "R5b product count boundary changed")
    require(model["foundation_count"] == 13 and model["modern_extension_count"] == 2, "R5b curriculum track boundary changed")
    checks += 11
    return checks


def test_direct_composer() -> int:
    checks = 0
    first = direct_current_site.build_direct()
    first_hashes = first["hashes"]
    require(first["remainder"]["file_count"] == 43, "R5b direct composer remainder count drift")
    require(first["pages"]["file_count"] == 15, "R5b direct composer page count drift")
    require(first["artifact"]["actual_files"] == 58 and first["artifact"]["pass"], "R5b direct composer failed 58-file oracle")
    checks += 3

    second = direct_current_site.build_direct()
    second_hashes = second["hashes"]
    require(direct_current_site.compare_hash_maps(first_hashes, second_hashes)["pass"], "two R5b direct composer builds are not byte-identical")
    require(second["artifact"]["pass"], "second R5b direct composer build failed frozen oracle")
    checks += 2
    return checks


def test_current_build_and_evidence() -> int:
    checks = 0
    current.build_current()
    first_hashes = current.artifact_hashes()
    require(len(first_hashes) == 58, "first R5b current build does not contain 58 public files")
    require(current.compare_to_oracle(first_hashes)["pass"], "first R5b current build differs from frozen oracle")
    checks += 2

    current.build_current()
    second_hashes = current.artifact_hashes()
    require(current.compare_hash_maps(first_hashes, second_hashes)["pass"], "two R5b current builds from one SHA are not byte-identical")
    require(current.compare_to_oracle(second_hashes)["pass"], "second R5b current build differs from frozen oracle")
    checks += 2

    expected_phases = {
        "r0": "v1.9-r0-equivalence",
        "r1": "v1.9-r1-canonical-catalogue",
        "r2": "v1.9-r2-peer-current-pages",
        "r3": "v1.9-r3-shared-page-components",
        "r4a": "v1.9-r4a-design-token-contract",
        "r4b": "v1.9-r4b-token-owned-components",
        "r5a": "v1.9-r5a-public-remainder-ownership",
        "r5b": "v1.9-r5b-direct-canonical-build",
    }
    for key, path in EVIDENCE.items():
        require(path.is_file(), f"missing canonical-source evidence: {key}")
        payload = json.loads(path.read_text(encoding="utf-8"))
        require(payload.get("phase") == expected_phases[key], f"evidence phase mismatch: {key}")
        require(payload.get("artifact", {}).get("pass") is True, f"artifact oracle failed in evidence: {key}")
        checks += 3

    r4b_payload = json.loads(EVIDENCE["r4b"].read_text(encoding="utf-8"))
    require(r4b_payload["component_source_kinds"] == {"raw": 11, "token-template": 6}, "R4b component-source invariant regressed under R5b")
    require(r4b_payload["minimaxMismatchPreserved"] is True, "R4b Minimax safeguard regressed under R5b")
    checks += 2

    r5a_payload = json.loads(EVIDENCE["r5a"].read_text(encoding="utf-8"))
    require(r5a_payload["ownership_counts"] == {"canonical_existing": 29, "current_snapshot": 14}, "R5a ownership receipt regressed under R5b")
    require(set(r5a_payload["snapshot_public_paths"]) == public_remainder.EXPECTED_SNAPSHOT_PUBLIC_PATHS, "R5a snapshot receipt regressed under R5b")
    checks += 2

    r5b_payload = json.loads(EVIDENCE["r5b"].read_text(encoding="utf-8"))
    require(r5b_payload["direct_current_build"] is True, "R5b evidence direct-build flag missing")
    require(r5b_payload["current_build_composer"] == "tools/direct_current_site.py", "R5b evidence composer drift")
    require(r5b_payload["historical_builder_role"] == "test-only-regression-and-provenance", "R5b evidence historical role drift")
    require(r5b_payload["historical_builder_imported_by_current_facade"] is False, "R5b evidence reports historical import")
    require(r5b_payload["public_remainder_emission"]["file_count"] == 43, "R5b evidence remainder emission drift")
    require(r5b_payload["applet_page_emission"]["file_count"] == 15, "R5b evidence applet emission drift")
    require(r5b_payload["total_public_file_count"] == 58, "R5b evidence total public-file drift")
    checks += 7
    return checks


def main() -> int:
    checks = (
        r4b.test_hash_comparator()
        + r4b.test_token_resolver_fail_closed()
        + r4b.test_token_components()
        + r4b.test_page_graph()
        + r4b.test_design_contract()
        + test_public_remainder()
        + test_current_facade_independence()
        + test_product_model()
        + test_direct_composer()
        + test_current_build_and_evidence()
    )
    print(
        "V1.9 DIRECT CANONICAL BUILD R5B: PASS — "
        f"{checks} checks; no executable historical builder coupling; "
        "43 remainder + 15 applet pages / two direct builds / 58 public files byte-locked"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
