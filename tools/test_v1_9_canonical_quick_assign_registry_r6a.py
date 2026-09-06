#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import build_current as current
import quick_assigns
import test_v1_9_direct_canonical_build_r5b as r5b

ROOT = Path(__file__).resolve().parents[1]
BUILD_SOURCE = ROOT / "tools" / "build_current.py"
EVIDENCE = {
    phase: ROOT / "release-evidence" / f"v1.9-canonical-source-{phase}.json"
    for phase in ("r0", "r1", "r2", "r3", "r4a", "r4b", "r5a", "r5b", "r6a")
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def test_registry_handoff() -> int:
    checks = 0
    state = quick_assigns.load_and_validate(require_historical_equivalence=True)
    manifest = state["manifest"]
    require(manifest["phase"] == quick_assigns.PHASE, "R6a canonical registry phase drift")
    require(manifest["schema_version"] == 1, "R6a canonical registry schema drift")
    require(len(state["activities"]) == 15, "R6a activity count drift")
    require(len(set(state["ids"])) == 15, "R6a stable ID uniqueness drift")
    require(len(set(state["slugs"])) == 15, "R6a slug uniqueness drift")
    require(len(set(state["anchors"])) == 15, "R6a anchor uniqueness drift")
    require(manifest["sequence"] == quick_assigns.EXPECTED_SEQUENCE, "R6a inquiry sequence drift")
    require(all(row["locales"] == quick_assigns.EXPECTED_LOCALES for row in state["activities"]), "R6a locale boundary drift")
    require(state["historical_equivalent"] is True, "R6a historical handoff is not equivalent")
    require(state["historical_sha256"] == quick_assigns.EXPECTED_HISTORICAL_SHA256, "R6a historical registry digest drift")
    checks += 10
    return checks


def _expect_registry_failure(payload: dict[str, object], message: str) -> None:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "quick-assigns.json"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        with patch.object(quick_assigns, "REGISTRY", path):
            try:
                quick_assigns.load_and_validate()
            except RuntimeError:
                return
    raise AssertionError(message)


def test_registry_fail_closed() -> int:
    checks = 0
    original = quick_assigns.load_json(quick_assigns.REGISTRY)

    payload = copy.deepcopy(original)
    payload["sequence"] = ["run", "observe", "explain"]
    _expect_registry_failure(payload, "R6a accepted inquiry-sequence drift")
    checks += 1

    payload = copy.deepcopy(original)
    payload["activities"][0]["locales"] = ["en"]
    _expect_registry_failure(payload, "R6a accepted locale-boundary drift")
    checks += 1

    payload = copy.deepcopy(original)
    payload["activities"][1]["id"] = payload["activities"][0]["id"]
    _expect_registry_failure(payload, "R6a accepted duplicate stable IDs")
    checks += 1

    payload = copy.deepcopy(original)
    payload["activities"][0]["unexpected"] = True
    _expect_registry_failure(payload, "R6a accepted an undeclared activity field")
    checks += 1

    return checks


def test_current_source_ownership() -> int:
    checks = 0
    source = BUILD_SOURCE.read_text(encoding="utf-8")
    require("import quick_assigns" in source, "Current build does not import the canonical Quick Assign validator")
    require("quick_assigns.load_and_validate()" in source, "Current build does not load the canonical Quick Assign registry")
    checks += 2

    missing_historical = ROOT / "tools" / "missing-historical-quick-assign-registry.json"
    with patch.object(quick_assigns, "HISTORICAL_REGISTRY", missing_historical):
        model = current.validate_product_model()
    release = model["release"]
    require(release["architecture_phase"] == quick_assigns.PHASE, "R6a release phase mismatch")
    require(release["direct_current_build_phase"] == "v1.9-r5b-direct-canonical-build", "R6a lost the accepted R5b build phase")
    require(release["current_quick_assign_registry"] == "src/product/quick-assigns.json", "R6a current registry pointer drift")
    require(release["historical_quick_assign_registry"] == "tools/quick_assigns_v2.json", "R6a historical registry provenance drift")
    require(release["historical_quick_assign_registry_role"] == "test-only-regression-and-provenance", "R6a historical registry role drift")
    require(model["quick_assign_count"] == 15, "R6a product Quick Assign count drift")
    require(set(model["quick_assigns"]["slugs"]) == set(model["slugs"]), "R6a registry/lab membership drift")
    require(model["quick_assigns"]["historical_sha256"] is None, "Current product validation read the historical registry")
    checks += 8
    return checks


def test_current_build_and_evidence() -> int:
    checks = 0
    current.build_current()
    first_hashes = current.artifact_hashes()
    require(len(first_hashes) == 58, "first R6a current build does not contain 58 public files")
    require(current.compare_to_oracle(first_hashes)["pass"], "first R6a current build differs from frozen v1.8.1 oracle")
    checks += 2

    state = quick_assigns.load_and_validate()
    emitted = quick_assigns.validate_emitted(current.SITE, state)
    require(emitted == {"activity_count": 15, "surface_checks": 30, "support_checks": 120, "pass": True}, "R6a emitted Quick Assign bindings drift")
    checks += 1

    current.build_current()
    second_hashes = current.artifact_hashes()
    require(current.compare_hash_maps(first_hashes, second_hashes)["pass"], "two R6a current builds from one SHA are not byte-identical")
    require(current.compare_to_oracle(second_hashes)["pass"], "second R6a current build differs from frozen v1.8.1 oracle")
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
        "r6a": quick_assigns.PHASE,
    }
    for key, path in EVIDENCE.items():
        require(path.is_file(), f"missing canonical-source evidence: {key}")
        payload = json.loads(path.read_text(encoding="utf-8"))
        require(payload.get("phase") == expected_phases[key], f"evidence phase mismatch: {key}")
        require(payload.get("artifact", {}).get("pass") is True, f"artifact oracle failed in evidence: {key}")
        checks += 3

    r5b_payload = json.loads(EVIDENCE["r5b"].read_text(encoding="utf-8"))
    require(r5b_payload["direct_current_build"] is True, "R5b direct-build invariant regressed under R6a")
    require(r5b_payload["representation"] == "preserved-under-r6a-canonical-quick-assign-registry", "R5b preservation evidence missing under R6a")
    checks += 2

    r6a_payload = json.loads(EVIDENCE["r6a"].read_text(encoding="utf-8"))
    require(r6a_payload["canonical_quick_assign_sha256"] == state["sha256"], "R6a evidence canonical digest drift")
    require(r6a_payload["historical_quick_assign_sha256"] == quick_assigns.EXPECTED_HISTORICAL_SHA256, "R6a evidence historical digest drift")
    require(r6a_payload["historical_quick_assign_registry_role"] == "test-only-regression-and-provenance", "R6a evidence historical role drift")
    require(r6a_payload["current_build_reads_historical_quick_assign_registry"] is False, "R6a evidence reports current historical-registry coupling")
    require(r6a_payload["activity_count"] == 15, "R6a evidence activity count drift")
    require(r6a_payload["inquiry_sequence"] == quick_assigns.EXPECTED_SEQUENCE, "R6a evidence inquiry sequence drift")
    require(r6a_payload["learner_locales"] == quick_assigns.EXPECTED_LOCALES, "R6a evidence locale boundary drift")
    require(r6a_payload["emitted_bindings"] == emitted, "R6a evidence emitted binding drift")
    checks += 8
    return checks


def main() -> int:
    checks = (
        r5b.r4b.test_hash_comparator()
        + r5b.r4b.test_token_resolver_fail_closed()
        + r5b.r4b.test_token_components()
        + r5b.r4b.test_page_graph()
        + r5b.r4b.test_design_contract()
        + r5b.test_public_remainder()
        + r5b.test_current_facade_independence()
        + test_registry_handoff()
        + test_registry_fail_closed()
        + test_current_source_ownership()
        + test_current_build_and_evidence()
    )
    print(
        "V1.9 CANONICAL QUICK ASSIGN REGISTRY R6A: PASS — "
        f"{checks} checks; 15 canonical activities / historical handoff verified / "
        "current build independent / 150 emitted bindings / two builds / 58 public files byte-locked"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
