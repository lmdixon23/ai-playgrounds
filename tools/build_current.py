#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from build_site_v1_8_1 import build_site as build_legacy_v181


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
PRODUCT = ROOT / "src" / "product" / "release.json"
LABS = ROOT / "src" / "product" / "labs.json"
CATALOGUE = ROOT / "src" / "product" / "catalogue.json"
ORACLE = ROOT / "src" / "product" / "public-artifact-sha256.json"
QUICK_ASSIGNS = ROOT / "tools" / "quick_assigns_v2.json"
R0_EVIDENCE = ROOT / "release-evidence" / "v1.9-canonical-source-r0.json"
R1_EVIDENCE = ROOT / "release-evidence" / "v1.9-canonical-source-r1.json"
BASELINE_SHA = "d1c72e10e6c5bf64b9a4bbed578b2305d1c988d0"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


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

    # R1 owns not only the semantic rows but the exact stable serialization.
    serialized = (json.dumps(rows, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if serialized != raw:
        raise RuntimeError(
            "Canonical catalogue is not in deterministic public serialization form "
            "(UTF-8, ensure_ascii=False, indent=2, trailing newline)"
        )

    oracle = load_json(ORACLE)
    expected_digest = oracle.get("applets.json")
    actual_digest = hashlib.sha256(raw).hexdigest()
    if actual_digest != expected_digest:
        raise RuntimeError(
            f"Canonical catalogue digest drift: {actual_digest} != frozen applets.json {expected_digest}"
        )

    slugs = [row.get("slug") for row in rows]
    if len(set(slugs)) != 15:
        raise RuntimeError("Canonical catalogue slugs are not unique")
    showcase_orders = [row.get("showcase_order") for row in rows]
    if sorted(showcase_orders) != list(range(1, 16)):
        raise RuntimeError(
            f"Canonical catalogue showcase order is not exactly 1..15: {showcase_orders}"
        )

    required = {
        "slug",
        "icon",
        "category",
        "category_en",
        "category_zh",
        "category_es",
        "category_vi",
        "title",
        "title_zh",
        "title_es",
        "title_vi",
        "desc",
        "desc_zh",
        "desc_es",
        "desc_vi",
        "time",
        "level",
        "featured",
        "featured_zh",
        "featured_es",
        "featured_vi",
        "accent",
        "course_order",
        "showcase_order",
        "course_phase",
        "accent_name",
        "keywords",
    }
    for row in rows:
        slug = row.get("slug")
        missing = sorted(required - set(row))
        # Minimax retains one additional concept field; extra fields are allowed.
        if missing:
            raise RuntimeError(f"Canonical catalogue fields missing for {slug}: {missing}")
        keywords = row.get("keywords")
        if not isinstance(keywords, list) or not keywords or any(not isinstance(x, str) or not x for x in keywords):
            raise RuntimeError(f"Canonical catalogue keywords invalid for {slug}")

    return {
        "rows": rows,
        "raw": raw,
        "sha256": actual_digest,
        "slugs": slugs,
        "showcase_orders": showcase_orders,
        "serializer_roundtrip": True,
    }


def validate_product_model() -> dict[str, object]:
    release = load_json(PRODUCT)
    lab_payload = load_json(LABS)
    labs = lab_payload.get("labs", [])
    quick = load_json(QUICK_ASSIGNS)
    activities = quick.get("activities", [])
    catalogue = load_canonical_catalogue()
    catalogue_rows = catalogue["rows"]

    if release.get("architecture_phase") != "v1.9-r1-canonical-catalogue":
        raise RuntimeError("Current architecture phase must be v1.9-r1-canonical-catalogue")
    if release.get("public_release") != "v1.8.1" or release.get("software_version") != "1.8.1":
        raise RuntimeError("R1 release manifest must remain bound to exact public v1.8.1")
    if release.get("baseline_source_sha") != BASELINE_SHA:
        raise RuntimeError("R1 baseline source SHA changed")
    if release.get("public_file_count") != 58 or release.get("applet_count") != 15:
        raise RuntimeError("R1 public boundary must remain 58 files / 15 applets")
    if release.get("foundations_count") != 13 or release.get("modern_extension_count") != 2:
        raise RuntimeError("R1 track-count boundary changed")
    if release.get("learner_locales") != ["en", "zh", "vi", "es"]:
        raise RuntimeError("R1 learner locale order changed")
    if release.get("quick_assign_count") != 15:
        raise RuntimeError("R1 Quick Assign count changed")
    if release.get("canonical_catalogue") != "src/product/catalogue.json":
        raise RuntimeError("R1 canonical catalogue ownership path changed")

    if len(labs) != 15:
        raise RuntimeError(f"Canonical lab manifest has {len(labs)} entries, expected 15")
    slugs = [row.get("slug") for row in labs]
    if len(set(slugs)) != 15:
        raise RuntimeError("Canonical lab slugs are not unique")
    orders = [row.get("course_order") for row in labs]
    if sorted(orders) != list(range(1, 16)):
        raise RuntimeError(f"Canonical course order is not exactly 1..15: {orders}")

    foundations = [row for row in labs if row.get("track") == "foundations"]
    modern = [row for row in labs if row.get("track") == "modern-extension"]
    if len(foundations) != 13 or len(modern) != 2:
        raise RuntimeError(
            f"Canonical track boundary changed: foundations={len(foundations)}, modern={len(modern)}"
        )
    if {row.get("slug") for row in modern} != {"transformer-language-model", "agent-tool-context"}:
        raise RuntimeError("Modern-extension membership changed")

    catalogue_by_slug = {row.get("slug"): row for row in catalogue_rows}
    lab_by_slug = {row.get("slug"): row for row in labs}
    if set(catalogue_by_slug) != set(lab_by_slug):
        raise RuntimeError(
            "Canonical lab/catalogue membership differs: "
            f"labs_only={sorted(set(lab_by_slug) - set(catalogue_by_slug))}, "
            f"catalogue_only={sorted(set(catalogue_by_slug) - set(lab_by_slug))}"
        )
    for slug, lab in lab_by_slug.items():
        public = catalogue_by_slug[slug]
        for field in ("title", "course_order", "accent"):
            if lab.get(field) != public.get(field):
                raise RuntimeError(
                    f"Canonical lab/catalogue drift for {slug}.{field}: "
                    f"{lab.get(field)!r} != {public.get(field)!r}"
                )

    qa_by_slug = {row.get("slug"): row for row in activities if row.get("status") == "active"}
    if len(qa_by_slug) != 15:
        raise RuntimeError(f"Expected 15 active Quick Assigns, found {len(qa_by_slug)}")

    for row in labs:
        slug = str(row["slug"])
        if slug not in qa_by_slug:
            raise RuntimeError(f"Canonical lab has no active Quick Assign: {slug}")
        if row.get("quick_assign_id") != qa_by_slug[slug].get("id"):
            raise RuntimeError(
                f"Quick Assign ID drift for {slug}: {row.get('quick_assign_id')} != {qa_by_slug[slug].get('id')}"
            )
        if qa_by_slug[slug].get("locales") != ["en", "zh", "vi", "es"]:
            raise RuntimeError(f"Quick Assign locale boundary changed for {slug}")

        implementation = row.get("implementation", {})
        if not isinstance(implementation, dict):
            raise RuntimeError(f"Implementation ownership missing for {slug}")
        source_paths = [
            value
            for key, value in implementation.items()
            if key != "kind" and isinstance(value, str) and value
        ]
        if not source_paths:
            raise RuntimeError(f"No current source ownership paths declared for {slug}")
        missing = [path for path in source_paths if not (ROOT / path).is_file()]
        if missing:
            raise RuntimeError(f"Declared source ownership path missing for {slug}: {missing}")

    return {
        "release": release,
        "labs": labs,
        "catalogue": catalogue,
        "lab_count": len(labs),
        "foundation_count": len(foundations),
        "modern_count": len(modern),
        "quick_assign_count": len(qa_by_slug),
        "slugs": slugs,
    }


def validate_emitted_catalogue(model: dict[str, object]) -> dict[str, object]:
    path = SITE / "applets.json"
    if not path.is_file():
        raise RuntimeError("Generated public applet catalogue is missing")
    emitted = load_json(path)
    canonical_rows = model["catalogue"]["rows"]
    if emitted != canonical_rows:
        raise RuntimeError("Generated public catalogue semantics differ from canonical catalogue source")

    mismatches: list[dict[str, object]] = []
    canonical_by_slug = {row.get("slug"): row for row in model["labs"]}
    emitted_by_slug = {row.get("slug"): row for row in emitted}
    for slug in sorted(canonical_by_slug):
        canonical = canonical_by_slug[slug]
        public = emitted_by_slug[slug]
        for field in ("title", "course_order", "accent"):
            if canonical.get(field) != public.get(field):
                mismatches.append(
                    {
                        "slug": slug,
                        "field": field,
                        "canonical": canonical.get(field),
                        "emitted": public.get(field),
                    }
                )
        applet_path = SITE / "playgrounds" / str(slug) / "index.html"
        if not applet_path.is_file():
            mismatches.append(
                {
                    "slug": slug,
                    "field": "public_path",
                    "canonical": f"playgrounds/{slug}/index.html",
                    "emitted": None,
                }
            )

    if mismatches:
        raise RuntimeError(f"Canonical lab manifest does not describe emitted public product: {mismatches}")

    return {
        "rows": len(emitted),
        "canonical_sha256": model["catalogue"]["sha256"],
        "fields_compared": ["title", "course_order", "accent"],
        "mismatches": [],
        "pass": True,
    }


def write_evidence(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_current() -> None:
    model = validate_product_model()
    canonical_catalogue = model["catalogue"]

    # R1 still delegates non-catalogue composition to the frozen v1.8.1 builder.
    # Catalogue ownership changes only after exact legacy/canonical equivalence is proven.
    build_legacy_v181()

    public_catalogue = SITE / "applets.json"
    legacy_bytes = public_catalogue.read_bytes()
    canonical_bytes = canonical_catalogue["raw"]
    legacy_sha = hashlib.sha256(legacy_bytes).hexdigest()
    canonical_sha = canonical_catalogue["sha256"]
    if legacy_bytes != canonical_bytes:
        raise RuntimeError(
            "R1 legacy/canonical catalogue handoff differs: "
            f"legacy_sha256={legacy_sha}, canonical_sha256={canonical_sha}"
        )

    # From this point onward, src/product/catalogue.json is the final public owner.
    public_catalogue.write_bytes(canonical_bytes)
    catalogue_check = validate_emitted_catalogue(model)
    actual = artifact_hashes()
    comparison = compare_to_oracle(actual)

    # Preserve the R0 invariant receipt so the historical R0 gate remains a
    # regression check while R1 adds a stronger ownership receipt.
    r0_payload = {
        "phase": "v1.9-r0-equivalence",
        "baseline_source_sha": BASELINE_SHA,
        "legacy_builder": "tools/build_site_v1_8_1.py",
        "canonical_facade": "tools/build_current.py",
        "model": {
            key: value for key, value in model.items() if key not in {"labs", "catalogue"}
        },
        "catalogue": catalogue_check,
        "artifact": comparison,
    }
    write_evidence(R0_EVIDENCE, r0_payload)

    r1_payload = {
        "phase": "v1.9-r1-canonical-catalogue",
        "baseline_source_sha": BASELINE_SHA,
        "canonical_catalogue": "src/product/catalogue.json",
        "canonical_catalogue_sha256": canonical_sha,
        "serializer_roundtrip": canonical_catalogue["serializer_roundtrip"],
        "legacy_handoff": {
            "legacy_sha256": legacy_sha,
            "canonical_sha256": canonical_sha,
            "byte_identical": legacy_bytes == canonical_bytes,
        },
        "model": {
            "lab_count": model["lab_count"],
            "foundation_count": model["foundation_count"],
            "modern_count": model["modern_count"],
            "quick_assign_count": model["quick_assign_count"],
            "slugs": model["slugs"],
        },
        "catalogue": catalogue_check,
        "artifact": comparison,
    }
    write_evidence(R1_EVIDENCE, r1_payload)

    if not comparison["pass"]:
        raise RuntimeError(
            "R1 current build differs from frozen v1.8.1 byte oracle: "
            f"added={comparison['added']}, removed={comparison['removed']}, changed={comparison['changed']}"
        )

    print(
        "v1.9 R1 current build: PASS — "
        f"canonical catalogue {canonical_sha[:12]}… owns applets.json; "
        f"{comparison['actual_files']} public files remain byte-identical to frozen v1.8.1"
    )


if __name__ == "__main__":
    build_current()
