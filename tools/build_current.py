#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from build_site_v1_8_1 import build_site as build_legacy_v181
import page_components

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
PRODUCT = ROOT / "src" / "product" / "release.json"
LABS = ROOT / "src" / "product" / "labs.json"
CATALOGUE = ROOT / "src" / "product" / "catalogue.json"
ORACLE = ROOT / "src" / "product" / "public-artifact-sha256.json"
QUICK_ASSIGNS = ROOT / "tools" / "quick_assigns_v2.json"
R0_EVIDENCE = ROOT / "release-evidence" / "v1.9-canonical-source-r0.json"
R1_EVIDENCE = ROOT / "release-evidence" / "v1.9-canonical-source-r1.json"
R2_EVIDENCE = ROOT / "release-evidence" / "v1.9-canonical-source-r2.json"
R3_EVIDENCE = ROOT / "release-evidence" / "v1.9-canonical-source-r3.json"
BASELINE_SHA = "d1c72e10e6c5bf64b9a4bbed578b2305d1c988d0"
CURRENT_PHASE = "v1.9-r3-shared-page-components"
R2_PEER_SLUGS = (
    "transformer-language-model",
    "agent-tool-context",
    "minimax-alpha-beta",
)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def artifact_hashes() -> dict[str, str]:
    return {
        str(path.relative_to(SITE)).replace("\\", "/"): digest(path)
        for path in sorted(SITE.rglob("*"))
        if path.is_file()
    }


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def compare_hash_maps(expected: dict[str, str], actual: dict[str, str]) -> dict[str, object]:
    expected_keys = set(expected)
    actual_keys = set(actual)
    added = sorted(actual_keys - expected_keys)
    removed = sorted(expected_keys - actual_keys)
    changed = sorted(
        path for path in expected_keys & actual_keys if expected[path] != actual[path]
    )
    return {
        "expected_files": len(expected),
        "actual_files": len(actual),
        "added": added,
        "removed": removed,
        "changed": changed,
        "pass": not (added or removed or changed),
    }


def compare_to_oracle(actual: dict[str, str]) -> dict[str, object]:
    return compare_hash_maps(load_json(ORACLE), actual)


def load_canonical_catalogue() -> dict[str, object]:
    if not CATALOGUE.is_file():
        raise RuntimeError("Canonical catalogue source is missing")
    raw = CATALOGUE.read_bytes()
    rows = json.loads(raw.decode("utf-8"))
    if not isinstance(rows, list) or len(rows) != 15:
        raise RuntimeError("Canonical catalogue must contain exactly 15 rows")
    serialized = (json.dumps(rows, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if serialized != raw:
        raise RuntimeError("Canonical catalogue serialization drift")
    oracle = load_json(ORACLE)
    actual_digest = digest_bytes(raw)
    if actual_digest != oracle.get("applets.json"):
        raise RuntimeError("Canonical catalogue no longer matches frozen public applets.json")
    slugs = [row.get("slug") for row in rows]
    if len(set(slugs)) != 15:
        raise RuntimeError("Canonical catalogue slugs are not unique")
    if sorted(row.get("showcase_order") for row in rows) != list(range(1, 16)):
        raise RuntimeError("Canonical catalogue showcase order is not exactly 1..15")
    required = {
        "slug", "icon", "category", "category_en", "category_zh", "category_es", "category_vi",
        "title", "title_zh", "title_es", "title_vi", "desc", "desc_zh", "desc_es", "desc_vi",
        "time", "level", "featured", "featured_zh", "featured_es", "featured_vi", "accent",
        "course_order", "showcase_order", "course_phase", "accent_name", "keywords",
    }
    for row in rows:
        missing = sorted(required - set(row))
        if missing:
            raise RuntimeError(f"Canonical catalogue fields missing for {row.get('slug')}: {missing}")
        keywords = row.get("keywords")
        if not isinstance(keywords, list) or not keywords or any(not isinstance(v, str) or not v for v in keywords):
            raise RuntimeError(f"Canonical catalogue keywords invalid for {row.get('slug')}")
    return {
        "rows": rows,
        "raw": raw,
        "sha256": actual_digest,
        "slugs": slugs,
        "serializer_roundtrip": True,
    }


def _legacy_paths(value: object) -> list[str]:
    result: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "kind":
                continue
            if isinstance(child, str):
                result.append(child)
            else:
                result.extend(_legacy_paths(child))
    elif isinstance(value, list):
        for child in value:
            result.extend(_legacy_paths(child))
    return result


def validate_product_model() -> dict[str, object]:
    release = load_json(PRODUCT)
    lab_payload = load_json(LABS)
    labs = lab_payload.get("labs", [])
    quick = load_json(QUICK_ASSIGNS)
    catalogue = load_canonical_catalogue()
    pages = page_components.load_and_validate()

    if release.get("architecture_phase") != CURRENT_PHASE:
        raise RuntimeError(f"Current architecture phase must be {CURRENT_PHASE}")
    if release.get("public_release") != "v1.8.1" or release.get("software_version") != "1.8.1":
        raise RuntimeError("R3 must remain bound to exact public v1.8.1")
    if release.get("baseline_source_sha") != BASELINE_SHA:
        raise RuntimeError("R3 baseline source SHA changed")
    if release.get("public_file_count") != 58 or release.get("applet_count") != 15:
        raise RuntimeError("R3 public boundary must remain 58 files / 15 applets")
    if release.get("foundations_count") != 13 or release.get("modern_extension_count") != 2:
        raise RuntimeError("R3 curriculum track-count boundary changed")
    if release.get("learner_locales") != ["en", "zh", "vi", "es"]:
        raise RuntimeError("R3 learner locale order changed")
    if release.get("quick_assign_count") != 15:
        raise RuntimeError("R3 Quick Assign count changed")
    expected_release_fields = {
        "canonical_catalogue": "src/product/catalogue.json",
        "canonical_page_component_manifest": "src/product/page-components.json",
        "canonical_page_template_root": "src/labs",
        "canonical_component_root": "src/ui/components",
        "canonical_page_count": 15,
        "canonical_component_count": 17,
        "canonical_deduplicated_bytes": page_components.EXPECTED_DEDUPLICATED_BYTES,
    }
    for key, expected in expected_release_fields.items():
        if release.get(key) != expected:
            raise RuntimeError(f"R3 release source boundary drift for {key}: {release.get(key)!r} != {expected!r}")

    if not isinstance(labs, list) or len(labs) != 15:
        raise RuntimeError("Canonical lab manifest must contain exactly 15 labs")
    slugs = [row.get("slug") for row in labs]
    if len(set(slugs)) != 15:
        raise RuntimeError("Canonical lab slugs are not unique")
    if sorted(row.get("course_order") for row in labs) != list(range(1, 16)):
        raise RuntimeError("Canonical course order is not exactly 1..15")
    foundations = [row for row in labs if row.get("track") == "foundations"]
    modern_extensions = [row for row in labs if row.get("track") == "modern-extension"]
    if len(foundations) != 13 or len(modern_extensions) != 2:
        raise RuntimeError("Canonical curriculum track boundary changed")
    if {row.get("slug") for row in modern_extensions} != {"transformer-language-model", "agent-tool-context"}:
        raise RuntimeError("Modern-extension curriculum membership changed")

    page_by_slug = {row["slug"]: row for row in pages["pages"]}
    lab_by_slug = {row.get("slug"): row for row in labs}
    catalogue_by_slug = {row.get("slug"): row for row in catalogue["rows"]}
    if set(page_by_slug) != set(lab_by_slug) or set(catalogue_by_slug) != set(lab_by_slug):
        raise RuntimeError("Canonical page/lab/catalogue membership differs")

    active = [row for row in quick.get("activities", []) if row.get("status") == "active"]
    qa_by_slug = {row.get("slug"): row for row in active}
    if len(qa_by_slug) != 15:
        raise RuntimeError(f"Expected 15 active Quick Assigns, found {len(qa_by_slug)}")

    for slug, lab in lab_by_slug.items():
        public = catalogue_by_slug[slug]
        for field in ("title", "course_order", "accent"):
            if lab.get(field) != public.get(field):
                raise RuntimeError(f"Canonical lab/catalogue drift for {slug}.{field}")

        qa = qa_by_slug.get(slug)
        if qa is None or lab.get("quick_assign_id") != qa.get("id"):
            raise RuntimeError(f"Quick Assign ownership drift for {slug}")
        if qa.get("locales") != ["en", "zh", "vi", "es"]:
            raise RuntimeError(f"Quick Assign locale boundary changed for {slug}")

        implementation = lab.get("implementation")
        if not isinstance(implementation, dict):
            raise RuntimeError(f"Implementation ownership missing for {slug}")
        if implementation.get("kind") != "canonical-template-with-shared-components-and-legacy-equivalence":
            raise RuntimeError(f"R3 canonical implementation kind drift for {slug}")
        if implementation.get("primary") != page_by_slug[slug].get("template"):
            raise RuntimeError(f"R3 canonical template owner drift for {slug}")
        if implementation.get("component_manifest") != "src/product/page-components.json":
            raise RuntimeError(f"R3 component manifest owner drift for {slug}")
        legacy = implementation.get("legacy_equivalence")
        if not isinstance(legacy, dict) or not legacy:
            raise RuntimeError(f"R3 legacy-equivalence provenance missing for {slug}")
        missing_legacy = [path for path in _legacy_paths(legacy) if not (ROOT / path).is_file()]
        if missing_legacy:
            raise RuntimeError(f"R3 legacy-equivalence path missing for {slug}: {missing_legacy}")

    return {
        "release": release,
        "labs": labs,
        "catalogue": catalogue,
        "page_components": pages,
        "lab_count": len(labs),
        "foundation_count": len(foundations),
        "modern_extension_count": len(modern_extensions),
        "quick_assign_count": len(qa_by_slug),
        "slugs": slugs,
    }


def validate_emitted_catalogue(model: dict[str, object]) -> dict[str, object]:
    path = SITE / "applets.json"
    if not path.is_file():
        raise RuntimeError("Generated public applet catalogue is missing")
    emitted = load_json(path)
    if emitted != model["catalogue"]["rows"]:
        raise RuntimeError("Generated public catalogue semantics differ from canonical catalogue source")
    for slug in model["slugs"]:
        if not (SITE / "playgrounds" / slug / "index.html").is_file():
            raise RuntimeError(f"Generated public applet path missing: {slug}")
    return {
        "rows": len(emitted),
        "canonical_sha256": model["catalogue"]["sha256"],
        "pass": True,
    }


def handoff_catalogue(model: dict[str, object]) -> dict[str, object]:
    public = SITE / "applets.json"
    legacy = public.read_bytes()
    canonical = model["catalogue"]["raw"]
    if legacy != canonical:
        raise RuntimeError(
            "R3 legacy/canonical catalogue handoff differs: "
            f"legacy_sha256={digest_bytes(legacy)}, canonical_sha256={digest_bytes(canonical)}"
        )
    public.write_bytes(canonical)
    return {
        "legacy_sha256": digest_bytes(legacy),
        "canonical_sha256": digest_bytes(canonical),
        "byte_identical": True,
    }


def handoff_canonical_pages(model: dict[str, object]) -> dict[str, object]:
    result: dict[str, object] = {"pages": {}, "page_count": 0, "pass": True}
    reconstructed = model["page_components"]["reconstructed"]
    evidence = model["page_components"]["page_evidence"]
    for slug in model["slugs"]:
        page_info = evidence[slug]
        public = SITE / str(page_info["public_path"])
        if not public.is_file():
            raise RuntimeError(f"Legacy equivalence build did not emit page: {slug}")
        legacy = public.read_bytes()
        canonical = reconstructed[slug]
        if legacy != canonical:
            raise RuntimeError(
                f"R3 legacy/canonical page handoff differs for {slug}: "
                f"legacy_sha256={digest_bytes(legacy)}, canonical_sha256={digest_bytes(canonical)}"
            )
        public.write_bytes(canonical)
        result["pages"][slug] = {
            "template": page_info["template"],
            "component_manifest": "src/product/page-components.json",
            "public_path": page_info["public_path"],
            "legacy_sha256": digest_bytes(legacy),
            "canonical_sha256": digest_bytes(canonical),
            "byte_identical": True,
        }
    result["page_count"] = len(result["pages"])
    return result


def write_evidence(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_current() -> None:
    model = validate_product_model()

    # R3 still invokes the historical ladder strictly as an independent
    # equivalence witness. Current catalogue and all 15 page bytes are owned by
    # canonical sources only after byte-for-byte equality has been proven.
    build_legacy_v181()

    catalogue_handoff = handoff_catalogue(model)
    page_handoff = handoff_canonical_pages(model)
    catalogue_check = validate_emitted_catalogue(model)
    comparison = compare_to_oracle(artifact_hashes())

    common_model = {
        "lab_count": model["lab_count"],
        "foundation_count": model["foundation_count"],
        "modern_extension_count": model["modern_extension_count"],
        "quick_assign_count": model["quick_assign_count"],
        "slugs": model["slugs"],
    }

    write_evidence(R0_EVIDENCE, {
        "phase": "v1.9-r0-equivalence",
        "baseline_source_sha": BASELINE_SHA,
        "legacy_builder": "tools/build_site_v1_8_1.py",
        "canonical_facade": "tools/build_current.py",
        "model": common_model,
        "catalogue": catalogue_check,
        "artifact": comparison,
    })
    write_evidence(R1_EVIDENCE, {
        "phase": "v1.9-r1-canonical-catalogue",
        "baseline_source_sha": BASELINE_SHA,
        "canonical_catalogue": "src/product/catalogue.json",
        "canonical_catalogue_sha256": model["catalogue"]["sha256"],
        "serializer_roundtrip": model["catalogue"]["serializer_roundtrip"],
        "legacy_handoff": catalogue_handoff,
        "model": common_model,
        "catalogue": catalogue_check,
        "artifact": comparison,
    })

    peer_pages = {
        slug: model["page_components"]["page_evidence"][slug]
        for slug in R2_PEER_SLUGS
    }
    peer_handoff = {
        slug: page_handoff["pages"][slug]
        for slug in R2_PEER_SLUGS
    }
    write_evidence(R2_EVIDENCE, {
        "phase": "v1.9-r2-peer-current-pages",
        "baseline_source_sha": BASELINE_SHA,
        "representation": "superseded-by-r3-template-component-composition",
        "canonical_catalogue": "src/product/catalogue.json",
        "catalogue_handoff": catalogue_handoff,
        "peer_current_pages": {"pages": peer_pages, "pass": True},
        "peer_page_handoff": {"pages": peer_handoff, "pass": True},
        "model": common_model,
        "catalogue": catalogue_check,
        "artifact": comparison,
    })
    write_evidence(R3_EVIDENCE, {
        "phase": CURRENT_PHASE,
        "baseline_source_sha": BASELINE_SHA,
        "canonical_catalogue": "src/product/catalogue.json",
        "canonical_page_component_manifest": "src/product/page-components.json",
        "catalogue_handoff": catalogue_handoff,
        "page_component_metrics": model["page_components"]["metrics"],
        "component_count": len(model["page_components"]["components"]),
        "canonical_pages": model["page_components"]["page_evidence"],
        "page_handoff": page_handoff,
        "model": common_model,
        "catalogue": catalogue_check,
        "artifact": comparison,
    })

    if not comparison["pass"]:
        raise RuntimeError(
            "R3 current build differs from frozen v1.8.1 byte oracle: "
            f"added={comparison['added']}, removed={comparison['removed']}, changed={comparison['changed']}"
        )

    print(
        "v1.9 R3 current build: PASS — canonical catalogue plus 15 template/component pages own final public bytes; "
        f"{comparison['actual_files']} files remain byte-identical to frozen v1.8.1"
    )


if __name__ == "__main__":
    build_current()
