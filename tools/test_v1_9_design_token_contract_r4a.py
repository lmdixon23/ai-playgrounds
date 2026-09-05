#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path

import build_current as current
import design_tokens
import page_components

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = {
    phase: ROOT / "release-evidence" / f"v1.9-canonical-source-{phase}.json"
    for phase in ("r0", "r1", "r2", "r3", "r4a")
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
    document = design_tokens.load_json(design_tokens.TOKENS)
    tokens = design_tokens.collect_tokens(document)

    broken = copy.deepcopy(tokens)
    broken["dimension.layout.gutterStandard"]["value"] = "{dimension.space.missing}"
    try:
        design_tokens.resolve_token(broken, "dimension.layout.gutterStandard")
    except design_tokens.TokenContractError:
        pass
    else:
        raise AssertionError("unresolved design-token alias did not fail closed")
    checks += 1

    cyclic = copy.deepcopy(tokens)
    cyclic["dimension.layout.gutterStandard"]["value"] = "{dimension.layout.gutterCompact}"
    cyclic["dimension.layout.gutterCompact"]["value"] = "{dimension.layout.gutterStandard}"
    try:
        design_tokens.resolve_token(cyclic, "dimension.layout.gutterStandard")
    except design_tokens.TokenContractError:
        pass
    else:
        raise AssertionError("design-token alias cycle did not fail closed")
    checks += 1

    return checks


def test_contract() -> int:
    checks = 0
    contract = design_tokens.validate_contract()
    require(contract["schema"] == design_tokens.EXPECTED_SCHEMA, "DTCG schema boundary drift")
    require(contract["format"] == "DTCG 2025.10", "DTCG format label drift")
    require(contract["token_count"] == 181, f"typed token count drift: {contract['token_count']}")
    require(contract["alias_count"] == 66, f"token alias count drift: {contract['alias_count']}")
    require(contract["theme_profiles"]["profiles"] == 3, "theme profile count drift")
    require(contract["theme_profiles"]["slugs"] == 15, "theme profile lab coverage drift")
    require(contract["theme_profiles"]["checks"] == 180, "theme binding count drift")
    require(contract["component_literal_bindings"]["bindings"] == 21, "component literal binding count drift")
    require(contract["accents"]["slugs"] == 15, "accent binding coverage drift")
    require(contract["accents"]["minimaxMismatchPreserved"] is True, "Minimax frozen accent mismatch was erased")
    require(contract["page_graph"] == {"pages": 15, "components": 17, "deduplicated_bytes": 247281}, "R3 page graph changed under R4a")
    checks += 11

    tokens = design_tokens.collect_tokens(design_tokens.load_json(design_tokens.TOKENS))
    require(design_tokens.css_value(tokens, "dimension.control.compact") == "38px", "compact control token drift")
    require(design_tokens.css_value(tokens, "dimension.control.touch") == "44px", "touch control token drift")
    require(design_tokens.css_value(tokens, "dimension.layout.gutterStandard") == "20px", "dimension alias resolution drift")
    require(design_tokens.css_value(tokens, "color.theme.legacyLight.card") == "#ffffff", "color alias resolution drift")
    require(design_tokens.css_value(tokens, "color.lab.minimax_alpha_beta.catalogue") == "#0d9488", "Minimax catalogue accent token drift")
    require(design_tokens.css_value(tokens, "color.lab.minimax_alpha_beta.uiLight") == "#3157c8", "Minimax frozen UI accent token drift")
    checks += 6

    bindings = design_tokens.load_json(design_tokens.BINDINGS)
    require(bindings["notes"]["lineageNotTaxonomy"].endswith("Minimax remains Foundations."), "lineage/taxonomy safeguard missing")
    require("does not authorize visible consolidation" in bindings["notes"]["noVisualAuthority"], "no-visual-authority safeguard missing")
    checks += 2
    return checks


def test_product_model() -> int:
    checks = 0
    model = current.validate_product_model()
    release = model["release"]
    require(release["architecture_phase"] == "v1.9-r4a-design-token-contract", "R4a release phase mismatch")
    require(release["design_token_contract"] == "src/design/ai-playgrounds.tokens.json", "release token contract path drift")
    require(release["design_token_bindings"] == "src/design/current-bindings.json", "release token bindings path drift")
    require(release["design_token_format"] == "DTCG 2025.10", "release token format drift")
    require(release["design_token_phase"] == "contract-first-frozen-output-binding", "R4a contract-first safeguard drift")
    require(model["design_tokens"]["pass"] is True, "design-token contract is not mandatory in current model")
    require(model["lab_count"] == 15 and model["quick_assign_count"] == 15, "R4a product count boundary changed")
    require(model["foundation_count"] == 13 and model["modern_extension_count"] == 2, "R4a curriculum track boundary changed")
    checks += 8

    graph = page_components.load_and_validate()
    require(len(graph["slugs"]) == 15 and len(graph["components"]) == 17, "R3 page-component ownership regressed")
    require(graph["metrics"]["deduplicated_bytes"] == 247281, "R3 source deduplication boundary regressed")
    checks += 2
    return checks


def test_current_build() -> int:
    checks = 0
    current.build_current()
    first_hashes = current.artifact_hashes()
    require(len(first_hashes) == 58, "first R4a build does not contain 58 public files")
    require(current.compare_to_oracle(first_hashes)["pass"], "first R4a build differs from frozen v1.8.1 oracle")
    checks += 2

    current.build_current()
    second_hashes = current.artifact_hashes()
    require(current.compare_hash_maps(first_hashes, second_hashes)["pass"], "two clean R4a builds from one SHA are not byte-identical")
    require(current.compare_to_oracle(second_hashes)["pass"], "second R4a build differs from frozen v1.8.1 oracle")
    checks += 2

    expected_phases = {
        "r0": "v1.9-r0-equivalence",
        "r1": "v1.9-r1-canonical-catalogue",
        "r2": "v1.9-r2-peer-current-pages",
        "r3": "v1.9-r3-shared-page-components",
        "r4a": "v1.9-r4a-design-token-contract",
    }
    for key, path in EVIDENCE.items():
        require(path.is_file(), f"missing canonical-source evidence: {key}")
        payload = json.loads(path.read_text(encoding="utf-8"))
        require(payload.get("phase") == expected_phases[key], f"evidence phase mismatch: {key}")
        require(payload.get("artifact", {}).get("pass") is True, f"artifact oracle failed in evidence: {key}")
        checks += 3

    r4a = json.loads(EVIDENCE["r4a"].read_text(encoding="utf-8"))
    require(r4a["design_token_schema"] == design_tokens.EXPECTED_SCHEMA, "R4a evidence schema drift")
    require(r4a["design_token_format"] == "DTCG 2025.10", "R4a evidence format drift")
    require(r4a["token_count"] == 181 and r4a["alias_count"] == 66, "R4a evidence token cardinality drift")
    require(r4a["theme_profiles"]["checks"] == 180 and r4a["theme_profiles"]["pass"] is True, "R4a evidence theme binding drift")
    require(r4a["accent_bindings"]["minimaxMismatchPreserved"] is True, "R4a evidence lost Minimax mismatch safeguard")
    require(r4a["component_literal_bindings"] == {"bindings": 21, "pass": True}, "R4a evidence component binding drift")
    checks += 6
    return checks


def main() -> int:
    checks = (
        test_hash_comparator()
        + test_token_resolver_fail_closed()
        + test_contract()
        + test_product_model()
        + test_current_build()
    )
    print(
        "V1.9 DESIGN TOKEN CONTRACT R4A: PASS — "
        f"{checks} checks; 181 typed tokens / 66 aliases / 180 theme bindings / "
        "21 component bindings / two-build determinism / 58 public files byte-locked"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
