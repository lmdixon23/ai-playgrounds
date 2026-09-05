#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path

import build_current as current
import design_tokens
import page_components
import token_components
import token_values

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = {
    phase: ROOT / "release-evidence" / f"v1.9-canonical-source-{phase}.json"
    for phase in ("r0", "r1", "r2", "r3", "r4a", "r4b")
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def test_hash_comparator() -> int:
    checks = 0
    exact = current.compare_hash_maps({"a": "1", "b": "2"}, {"a": "1", "b": "2"})
    require(exact["pass"], "exact hash maps should pass")
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


def test_token_resolver_fail_closed() -> int:
    checks = 0
    _, tokens = token_values.load_validated_tokens()

    broken = copy.deepcopy(tokens)
    broken["dimension.layout.gutterStandard"]["value"] = "{dimension.space.missing}"
    try:
        token_values.resolve_token(broken, "dimension.layout.gutterStandard")
    except token_values.TokenContractError:
        pass
    else:
        raise AssertionError("unresolved design-token alias did not fail closed")
    checks += 1

    cyclic = copy.deepcopy(tokens)
    cyclic["dimension.layout.gutterStandard"]["value"] = "{dimension.layout.gutterCompact}"
    cyclic["dimension.layout.gutterCompact"]["value"] = "{dimension.layout.gutterStandard}"
    try:
        token_values.resolve_token(cyclic, "dimension.layout.gutterStandard")
    except token_values.TokenContractError:
        pass
    else:
        raise AssertionError("design-token alias cycle did not fail closed")
    checks += 1
    return checks


def test_token_components() -> int:
    checks = 0
    state = token_components.load_and_render(require_raw_equivalence=False)
    require(state["phase"] == "v1.9-r4b-token-owned-components", "token-component manifest is not final R4b")
    require(state["component_count"] == 6, "R4b token-template component count drift")
    require(state["binding_count"] == 21, "R4b token-template binding count drift")
    require(state["rendered_component_bytes"] == 19050, "R4b rendered token-component byte metric drift")
    require(state["token_template_bytes"] == 19724, "R4b token-template source byte metric drift")
    require(state["raw_equivalence_required"] is False, "R4b final token components must not depend on raw-source equivalence")
    checks += 6

    manifest = token_components.load_manifest()
    for key, row in manifest["components"].items():
        template = ROOT / row["template"]
        require(template.is_file(), f"R4b token template missing: {key}")
        require(row.get("superseded_r4a_raw_source"), f"R4b historical raw-source provenance missing: {key}")
        require(not (ROOT / row["superseded_r4a_raw_source"]).exists(), f"R4b superseded raw source still exists: {key}")
        require(row.get("r4a_raw_source") is None, f"R4b manifest still exposes live R4a raw-source key: {key}")
        require(state["evidence"][key]["raw_equivalence"] is None, f"R4b final renderer still reports raw equivalence: {key}")
        checks += 5
    return checks


def test_page_graph() -> int:
    checks = 0
    graph = page_components.load_and_validate()
    require(graph["phase"] == "v1.9-r4b-token-owned-components", "R4b page graph phase drift")
    require(graph["graph"].get("schema_version") == 2, "R4b page graph schema version drift")
    require(graph["graph"].get("token_component_manifest") == "src/design/token-components.json", "R4b page graph token manifest pointer drift")
    require(graph["graph"].get("token_template_component_count") == 6, "R4b page graph declared token component count drift")
    require(len(graph["slugs"]) == 15 and len(graph["components"]) == 17, "R4b page/component cardinality drift")
    require(len(graph["token_template_components"]) == 6, "R4b token-template component membership drift")
    require(sum(1 for value in graph["component_source_kinds"].values() if value == "raw") == 11, "R4b raw component count drift")
    require(sum(1 for value in graph["component_source_kinds"].values() if value == "token-template") == 6, "R4b token-template source-kind count drift")
    require(graph["metrics"]["deduplicated_bytes"] == 247281, "R3 page-source deduplication invariant regressed")
    checks += 9

    for slug, page in graph["reconstructed"].items():
        public_path = graph["page_evidence"][slug]["public_path"]
        oracle = current.load_json(current.ORACLE)[public_path]
        require(page_components.digest_bytes(page) == oracle, f"R4b canonical page differs from frozen oracle: {slug}")
        checks += 1
    return checks


def test_design_contract() -> int:
    checks = 0
    contract = design_tokens.validate_contract()
    require(contract["schema"] == token_values.EXPECTED_SCHEMA, "DTCG schema boundary drift")
    require(contract["format"] == "DTCG 2025.10", "DTCG format label drift")
    require(contract["binding_phase"] == "v1.9-r4b-token-owned-components", "R4b design binding phase drift")
    require(contract["token_count"] == 181, "typed token count drift")
    require(contract["alias_count"] == 66, "token alias count drift")
    require(contract["theme_profiles"]["profiles"] == 3 and contract["theme_profiles"]["slugs"] == 15, "theme profile coverage drift")
    require(contract["theme_profiles"]["checks"] == 180, "theme binding count drift")
    require(contract["component_literal_bindings"]["bindings"] == 21, "rendered component binding count drift")
    require(contract["component_literal_bindings"]["source_model"] == "r4b-rendered-token-components", "rendered component binding source-model drift")
    require(contract["token_template_bindings"]["active"] is True, "R4b token-template binding contract not active")
    require(contract["token_template_bindings"]["components"] == 6, "R4b token-template binding component coverage drift")
    require(contract["token_template_bindings"]["bindings"] == 21, "R4b token-template binding cardinality drift")
    require(contract["token_template_bindings"]["rendered_component_bytes"] == 19050, "R4b rendered component metric drift")
    require(contract["token_template_bindings"]["token_template_bytes"] == 19724, "R4b token-template metric drift")
    require(contract["accents"]["slugs"] == 15 and contract["accents"]["minimaxMismatchPreserved"] is True, "accent binding safeguard drift")
    require(contract["page_graph"] == {"pages": 15, "components": 17, "token_template_components": 6, "deduplicated_bytes": 247281}, "R4b design/page graph summary drift")
    checks += 16
    return checks


def test_product_model() -> int:
    checks = 0
    model = current.validate_product_model()
    release = model["release"]
    require(release["architecture_phase"] == "v1.9-r4b-token-owned-components", "R4b release phase mismatch")
    require(release["design_token_phase"] == "token-owned-shared-component-source", "R4b design-token source-ownership phase drift")
    require(release["token_component_manifest"] == "src/design/token-components.json", "R4b release token-component manifest drift")
    require(release["token_template_component_count"] == 6, "R4b release token component count drift")
    require(release["token_template_binding_count"] == 21, "R4b release token binding count drift")
    require(release["token_template_rendered_component_bytes"] == 19050, "R4b release rendered token-component bytes drift")
    require(release["token_template_source_bytes"] == 19724, "R4b release token-template bytes drift")
    require(model["lab_count"] == 15 and model["quick_assign_count"] == 15, "R4b product count boundary changed")
    require(model["foundation_count"] == 13 and model["modern_extension_count"] == 2, "R4b curriculum track boundary changed")
    checks += 9
    return checks


def test_current_build() -> int:
    checks = 0
    current.build_current()
    first_hashes = current.artifact_hashes()
    require(len(first_hashes) == 58, "first R4b build does not contain 58 public files")
    require(current.compare_to_oracle(first_hashes)["pass"], "first R4b build differs from frozen v1.8.1 oracle")
    checks += 2

    current.build_current()
    second_hashes = current.artifact_hashes()
    require(current.compare_hash_maps(first_hashes, second_hashes)["pass"], "two clean R4b builds from one SHA are not byte-identical")
    require(current.compare_to_oracle(second_hashes)["pass"], "second R4b build differs from frozen v1.8.1 oracle")
    checks += 2

    expected_phases = {
        "r0": "v1.9-r0-equivalence",
        "r1": "v1.9-r1-canonical-catalogue",
        "r2": "v1.9-r2-peer-current-pages",
        "r3": "v1.9-r3-shared-page-components",
        "r4a": "v1.9-r4a-design-token-contract",
        "r4b": "v1.9-r4b-token-owned-components",
    }
    for key, path in EVIDENCE.items():
        require(path.is_file(), f"missing canonical-source evidence: {key}")
        payload = json.loads(path.read_text(encoding="utf-8"))
        require(payload.get("phase") == expected_phases[key], f"evidence phase mismatch: {key}")
        require(payload.get("artifact", {}).get("pass") is True, f"artifact oracle failed in evidence: {key}")
        checks += 3

    r3 = json.loads(EVIDENCE["r3"].read_text(encoding="utf-8"))
    require(r3.get("representation") == "superseded-by-r4b-token-template-component-source", "R3 supersession evidence missing")
    checks += 1

    r4a = json.loads(EVIDENCE["r4a"].read_text(encoding="utf-8"))
    require(r4a.get("representation") == "preserved-through-r4b-rendered-component-bindings", "R4a preservation evidence missing")
    require(r4a["component_literal_bindings"] == {"bindings": 21, "source_model": "r4b-rendered-token-components", "pass": True}, "R4a rendered-literal invariant drift under R4b")
    require(r4a["accent_bindings"]["minimaxMismatchPreserved"] is True, "R4a Minimax evidence safeguard regressed under R4b")
    checks += 3

    r4b = json.loads(EVIDENCE["r4b"].read_text(encoding="utf-8"))
    require(r4b["token_template_component_count"] == 6, "R4b evidence component count drift")
    require(r4b["token_template_binding_count"] == 21, "R4b evidence binding count drift")
    require(r4b["rendered_component_bytes"] == 19050, "R4b evidence rendered component bytes drift")
    require(r4b["token_template_bytes"] == 19724, "R4b evidence template bytes drift")
    require(r4b["component_source_kinds"] == {"raw": 11, "token-template": 6}, "R4b evidence source-kind counts drift")
    require(r4b["minimaxMismatchPreserved"] is True, "R4b evidence Minimax safeguard drift")
    checks += 6
    return checks


def main() -> int:
    checks = (
        test_hash_comparator()
        + test_token_resolver_fail_closed()
        + test_token_components()
        + test_page_graph()
        + test_design_contract()
        + test_product_model()
        + test_current_build()
    )
    print(
        "V1.9 TOKEN-OWNED COMPONENTS R4B: PASS — "
        f"{checks} checks; 6 token-template components / 21 bindings / 15 canonical pages / "
        "two-build determinism / 58 public files byte-locked"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
