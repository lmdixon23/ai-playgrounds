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
ORACLE = ROOT / "src" / "product" / "public-artifact-sha256.json"
QUICK_ASSIGNS = ROOT / "tools" / "quick_assigns_v2.json"
EVIDENCE = ROOT / "release-evidence" / "v1.9-canonical-source-r0.json"
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


def validate_product_model() -> dict[str, object]:
    release = load_json(PRODUCT)
    lab_payload = load_json(LABS)
    labs = lab_payload.get("labs", [])
    quick = load_json(QUICK_ASSIGNS)
    activities = quick.get("activities", [])

    if release.get("public_release") != "v1.8.1" or release.get("software_version") != "1.8.1":
        raise RuntimeError("R0 release manifest must remain bound to exact public v1.8.1")
    if release.get("baseline_source_sha") != BASELINE_SHA:
        raise RuntimeError("R0 baseline source SHA changed")
    if release.get("public_file_count") != 58 or release.get("applet_count") != 15:
        raise RuntimeError("R0 public boundary must remain 58 files / 15 applets")
    if release.get("foundations_count") != 13 or release.get("modern_extension_count") != 2:
        raise RuntimeError("R0 track-count boundary changed")
    if release.get("learner_locales") != ["en", "zh", "vi", "es"]:
        raise RuntimeError("R0 learner locale order changed")
    if release.get("quick_assign_count") != 15:
        raise RuntimeError("R0 Quick Assign count changed")

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
        "lab_count": len(labs),
        "foundation_count": len(foundations),
        "modern_count": len(modern),
        "quick_assign_count": len(qa_by_slug),
        "slugs": slugs,
    }


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
    expected = load_json(ORACLE)
    return compare_hash_maps(expected, actual)


def validate_emitted_catalogue(model: dict[str, object]) -> dict[str, object]:
    path = SITE / "applets.json"
    if not path.is_file():
        raise RuntimeError("Generated public applet catalogue is missing")
    emitted = load_json(path)
    if not isinstance(emitted, list) or len(emitted) != 15:
        raise RuntimeError(f"Generated public catalogue must contain 15 rows, got {len(emitted) if isinstance(emitted, list) else type(emitted).__name__}")

    emitted_by_slug = {row.get("slug"): row for row in emitted}
    canonical_rows = model["labs"]
    canonical_by_slug = {row.get("slug"): row for row in canonical_rows}
    if set(emitted_by_slug) != set(canonical_by_slug):
        raise RuntimeError(
            "Canonical/emitted lab membership differs: "
            f"canonical_only={sorted(set(canonical_by_slug) - set(emitted_by_slug))}, "
            f"emitted_only={sorted(set(emitted_by_slug) - set(canonical_by_slug))}"
        )

    mismatches: list[dict[str, object]] = []
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
        "fields_compared": ["title", "course_order", "accent"],
        "mismatches": [],
        "pass": True,
    }


def build_current() -> None:
    model = validate_product_model()

    # R0 intentionally delegates to the frozen current builder. The purpose of
    # this facade is to make current ownership explicit and establish an exact
    # byte oracle before any historical build layer is replaced.
    build_legacy_v181()

    catalogue = validate_emitted_catalogue(model)
    actual = artifact_hashes()
    comparison = compare_to_oracle(actual)
    payload = {
        "phase": "v1.9-r0-equivalence",
        "baseline_source_sha": BASELINE_SHA,
        "legacy_builder": "tools/build_site_v1_8_1.py",
        "canonical_facade": "tools/build_current.py",
        "model": {
            key: value for key, value in model.items() if key != "labs"
        },
        "catalogue": catalogue,
        "artifact": comparison,
    }
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if not comparison["pass"]:
        raise RuntimeError(
            "R0 current build differs from frozen v1.8.1 byte oracle: "
            f"added={comparison['added']}, removed={comparison['removed']}, changed={comparison['changed']}"
        )

    print(
        "v1.9 R0 current build: PASS — "
        f"{comparison['actual_files']} files byte-identical to frozen v1.8.1; "
        f"{model['lab_count']} canonical lab owners; {model['quick_assign_count']} Quick Assigns"
    )


if __name__ == "__main__":
    build_current()
