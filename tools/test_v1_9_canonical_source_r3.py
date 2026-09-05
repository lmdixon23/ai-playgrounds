#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import build_current as current
import page_components

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = {
    phase: ROOT / "release-evidence" / f"v1.9-canonical-source-{phase}.json"
    for phase in ("r0", "r1", "r2", "r3")
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


def test_component_graph() -> int:
    checks = 0
    state = page_components.load_and_validate()
    require(len(state["slugs"]) == 15, "R3 source graph must contain 15 pages")
    require(len(state["components"]) == 17, "R3 source graph must contain 17 components")
    require(state["metrics"]["deduplicated_bytes"] == 247_281, "R3 deduplication metric drift")
    checks += 3

    graph_components = state["graph"]["components"]
    require(
        set(graph_components["original/learning-modes-style-common"]["users"])
        == set(state["slugs"][:12]) - {"hill-climbing", "knn-classifier"},
        "original common learning-mode style user set drift",
    )
    require(
        graph_components["original/learning-modes-style-hill-climbing"]["users"] == ["hill-climbing"],
        "Hill Climbing style exception drift",
    )
    require(
        graph_components["original/learning-modes-style-knn-classifier"]["users"] == ["knn-classifier"],
        "KNN style exception drift",
    )
    newer = {"transformer-language-model", "agent-tool-context", "minimax-alpha-beta"}
    require(
        set(graph_components["newer/v181-modern-learner-parity-style"]["users"]) == newer,
        "newer-lineage shared learner-parity style user set drift",
    )
    packet_users = {"transformer-language-model", "agent-tool-context"}
    require(
        set(graph_components["newer/transformer-agent/v172-modern-packet-runtime"]["users"]) == packet_users,
        "Transformer/Agent packet runtime exception drift",
    )
    require(
        set(graph_components["newer/transformer-agent/v172-modern-packet-label-runtime"]["users"]) == packet_users,
        "Transformer/Agent packet-label runtime exception drift",
    )
    checks += 6

    for slug in state["slugs"]:
        template = ROOT / state["page_evidence"][slug]["template"]
        require(template.is_file(), f"canonical template missing: {slug}")
        require(not (ROOT / "src" / "labs" / slug / "index.html").exists(), f"superseded full current-page source still exists: {slug}")
        checks += 2

    return checks


def test_product_model() -> int:
    checks = 0
    model = current.validate_product_model()
    require(model["release"]["architecture_phase"] == current.CURRENT_PHASE, "R3 release phase mismatch")
    require(model["lab_count"] == 15, "canonical lab count is not 15")
    require(model["foundation_count"] == 13, "foundation count is not 13")
    require(model["modern_extension_count"] == 2, "modern-extension count is not 2")
    require(model["quick_assign_count"] == 15, "active Quick Assign count is not 15")
    checks += 5

    by_slug = {row["slug"]: row for row in model["labs"]}
    pages = {row["slug"]: row for row in model["page_components"]["pages"]}
    for slug, lab in by_slug.items():
        impl = lab["implementation"]
        require(impl["kind"] == "canonical-template-with-shared-components-and-legacy-equivalence", f"R3 implementation kind drift: {slug}")
        require(impl["primary"] == pages[slug]["template"], f"R3 primary template drift: {slug}")
        require(impl["component_manifest"] == "src/product/page-components.json", f"R3 component manifest drift: {slug}")
        require(isinstance(impl.get("legacy_equivalence"), dict) and impl["legacy_equivalence"], f"legacy provenance missing: {slug}")
        checks += 4
    return checks


def test_current_build() -> int:
    checks = 0
    current.build_current()
    first_hashes = current.artifact_hashes()
    require(len(first_hashes) == 58, "first R3 build does not contain 58 public files")
    require(current.compare_to_oracle(first_hashes)["pass"], "first R3 build differs from frozen oracle")
    checks += 2

    graph = page_components.load_and_validate()
    for slug, canonical in graph["reconstructed"].items():
        public = ROOT / "_site" / "playgrounds" / slug / "index.html"
        require(public.read_bytes() == canonical, f"public page is not canonical R3 reconstruction: {slug}")
        checks += 1

    current.build_current()
    second_hashes = current.artifact_hashes()
    require(current.compare_hash_maps(first_hashes, second_hashes)["pass"], "two clean R3 builds from one SHA are not byte-identical")
    require(current.compare_to_oracle(second_hashes)["pass"], "second R3 build differs from frozen oracle")
    checks += 2

    expected_phases = {
        "r0": "v1.9-r0-equivalence",
        "r1": "v1.9-r1-canonical-catalogue",
        "r2": "v1.9-r2-peer-current-pages",
        "r3": "v1.9-r3-shared-page-components",
    }
    for key, path in EVIDENCE.items():
        require(path.is_file(), f"missing canonical-source evidence: {key}")
        payload = json.loads(path.read_text(encoding="utf-8"))
        require(payload.get("phase") == expected_phases[key], f"evidence phase mismatch: {key}")
        require(payload.get("artifact", {}).get("pass") is True, f"artifact oracle failed in evidence: {key}")
        checks += 3

    r2 = json.loads(EVIDENCE["r2"].read_text(encoding="utf-8"))
    require(r2.get("representation") == "superseded-by-r3-template-component-composition", "R2 supersession evidence missing")
    require(set(r2.get("peer_page_handoff", {}).get("pages", {})) == set(current.R2_PEER_SLUGS), "R2 peer invariant was not preserved")
    checks += 2

    r3 = json.loads(EVIDENCE["r3"].read_text(encoding="utf-8"))
    require(r3.get("component_count") == 17, "R3 evidence component count drift")
    require(r3.get("page_handoff", {}).get("page_count") == 15, "R3 evidence page handoff count drift")
    require(r3.get("page_component_metrics", {}).get("deduplicated_bytes") == 247_281, "R3 evidence deduplication metric drift")
    checks += 3
    return checks


def main() -> int:
    checks = test_hash_comparator() + test_component_graph() + test_product_model() + test_current_build()
    print(
        "V1.9 CANONICAL SOURCE R3: PASS — "
        f"{checks} checks; 15 canonical templates / 17 shared components / "
        "247281 duplicate source bytes removed / 58 public files byte-locked"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
