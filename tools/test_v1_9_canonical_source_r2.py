#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import build_current as current


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_CATALOGUE = ROOT / "_site" / "applets.json"
R0_EVIDENCE = ROOT / "release-evidence" / "v1.9-canonical-source-r0.json"
R1_EVIDENCE = ROOT / "release-evidence" / "v1.9-canonical-source-r1.json"
R2_EVIDENCE = ROOT / "release-evidence" / "v1.9-canonical-source-r2.json"
EXPECTED_PEER_SLUGS = [
    "transformer-language-model",
    "agent-tool-context",
    "minimax-alpha-beta",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def comparator_regressions() -> int:
    checks = 0
    exact = current.compare_hash_maps({"a": "1", "b": "2"}, {"a": "1", "b": "2"})
    require(exact["pass"], "exact hash maps should pass")
    require(exact["added"] == [] and exact["removed"] == [] and exact["changed"] == [], "exact diagnostics wrong")
    checks += 1

    changed = current.compare_hash_maps({"a": "1"}, {"a": "9"})
    require(not changed["pass"] and changed["changed"] == ["a"], "changed artifact must fail")
    checks += 1

    added = current.compare_hash_maps({"a": "1"}, {"a": "1", "b": "2"})
    require(not added["pass"] and added["added"] == ["b"], "added artifact must fail")
    checks += 1

    removed = current.compare_hash_maps({"a": "1", "b": "2"}, {"a": "1"})
    require(not removed["pass"] and removed["removed"] == ["b"], "removed artifact must fail")
    checks += 1
    return checks


def main() -> int:
    checks = comparator_regressions()

    catalogue = current.load_canonical_catalogue()
    require(catalogue["serializer_roundtrip"] is True, "canonical catalogue serializer roundtrip failed")
    require(len(catalogue["rows"]) == 15, "canonical catalogue row count is not 15")
    require(sorted(catalogue["showcase_orders"]) == list(range(1, 16)), "showcase order is not 1..15")
    require(catalogue["sha256"] == current.load_json(current.ORACLE)["applets.json"], "canonical catalogue is not bound to frozen applets.json digest")
    checks += 4

    peer = current.validate_peer_current_pages()
    require(peer["pass"] is True, "peer current-page source gate did not pass")
    require(list(peer["pages"]) == EXPECTED_PEER_SLUGS, "peer current-page order/membership drift")
    oracle = current.load_json(current.ORACLE)
    for slug in EXPECTED_PEER_SLUGS:
        record = peer["pages"][slug]
        public_path = f"playgrounds/{slug}/index.html"
        require(record["matches_oracle"] is True, f"peer source does not match oracle: {slug}")
        require(record["sha256"] == oracle[public_path], f"peer source digest mismatch: {slug}")
        require(record["bytes"] > 100_000, f"peer source unexpectedly small: {slug}")
    checks += 2 + 3 * 3

    model = current.validate_product_model()
    require(model["release"]["architecture_phase"] == current.CURRENT_PHASE, "release phase is not R2")
    require(model["lab_count"] == 15, "canonical lab count is not 15")
    require(model["foundation_count"] == 13, "foundation count is not 13")
    require(model["modern_extension_count"] == 2, "modern-extension count is not 2")
    require(model["quick_assign_count"] == 15, "Quick Assign count is not 15")
    require(model["release"]["canonical_peer_page_slugs"] == EXPECTED_PEER_SLUGS, "release peer-page registry drift")
    checks += 6

    labs = {row["slug"]: row for row in model["labs"]}
    require(labs["minimax-alpha-beta"]["track"] == "foundations", "Minimax curriculum track changed")
    require(labs["transformer-language-model"]["track"] == "modern-extension", "Transformer curriculum track changed")
    require(labs["agent-tool-context"]["track"] == "modern-extension", "Agent curriculum track changed")
    for slug in EXPECTED_PEER_SLUGS:
        implementation = labs[slug]["implementation"]
        require(implementation["kind"] == "canonical-current-page-with-legacy-equivalence", f"peer ownership kind drift: {slug}")
        require(implementation["primary"] == f"src/labs/{slug}/index.html", f"peer primary owner drift: {slug}")
    checks += 3 + 3 * 2

    current.build_current()

    for path in (R0_EVIDENCE, R1_EVIDENCE, R2_EVIDENCE):
        require(path.is_file(), f"missing architecture evidence: {path.name}")
    r2 = json.loads(R2_EVIDENCE.read_text(encoding="utf-8"))
    require(r2["phase"] == current.CURRENT_PHASE, "R2 evidence phase mismatch")
    require(r2["baseline_source_sha"] == current.BASELINE_SHA, "R2 baseline SHA mismatch")
    require(r2["catalogue_handoff"]["byte_identical"] is True, "catalogue handoff is not byte-identical")
    require(r2["peer_page_handoff"]["pass"] is True, "peer page handoff did not pass")
    require(r2["artifact"]["pass"] is True, "58-file byte oracle did not pass")
    require(r2["artifact"]["actual_files"] == 58, "R2 generated file count is not 58")
    checks += 3 + 6

    canonical_catalogue = current.CATALOGUE.read_bytes()
    require(PUBLIC_CATALOGUE.read_bytes() == canonical_catalogue, "public applets.json is not canonical catalogue bytes")
    require(hashlib.sha256(canonical_catalogue).hexdigest() == catalogue["sha256"], "public catalogue digest drift")
    checks += 2

    handoff_pages = r2["peer_page_handoff"]["pages"]
    require(list(handoff_pages) == EXPECTED_PEER_SLUGS, "peer handoff membership/order drift")
    checks += 1
    for slug in EXPECTED_PEER_SLUGS:
        source = current.PEER_CURRENT_PAGES[slug]
        public = ROOT / "_site" / "playgrounds" / slug / "index.html"
        require(public.read_bytes() == source.read_bytes(), f"public peer page is not canonical source bytes: {slug}")
        require(handoff_pages[slug]["byte_identical"] is True, f"legacy/canonical peer handoff failed: {slug}")
        require(handoff_pages[slug]["legacy_sha256"] == handoff_pages[slug]["canonical_sha256"], f"peer handoff digest mismatch: {slug}")
    checks += 3 * 3

    final_compare = current.compare_hash_maps(oracle, current.artifact_hashes())
    require(final_compare["pass"], f"post-R2 public artifact oracle mismatch: {final_compare}")
    checks += 1

    print(
        "V1.9 CANONICAL SOURCE R2: PASS — "
        f"{checks} checks; 3 peer current pages canonically owned; 58 public files byte-locked"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
