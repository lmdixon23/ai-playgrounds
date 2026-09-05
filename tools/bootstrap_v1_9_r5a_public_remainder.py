#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import build_current
import page_components

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
ORACLE = ROOT / "src" / "product" / "public-artifact-sha256.json"
MANIFEST = ROOT / "src" / "product" / "public-remainder.json"
SNAPSHOT_ROOT = ROOT / "src" / "site" / "current"

PREFERRED_EXISTING = {
    "applets.json": "src/product/catalogue.json",
}


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    # Produce the exact accepted R4b product first. R5a only classifies ownership;
    # it does not change the current build path.
    build_current.build_current()

    oracle = load_json(ORACLE)
    pages = page_components.load_and_validate()
    page_paths = {row["public_path"] for row in pages["page_evidence"].values()}
    if len(page_paths) != 15:
        raise RuntimeError(f"Expected 15 canonical applet pages, found {len(page_paths)}")

    actual_paths = {
        str(path.relative_to(SITE)).replace("\\", "/")
        for path in SITE.rglob("*")
        if path.is_file()
    }
    if actual_paths != set(oracle):
        raise RuntimeError(
            "Current product inventory differs from frozen oracle: "
            f"added={sorted(actual_paths-set(oracle))}, removed={sorted(set(oracle)-actual_paths)}"
        )

    remainder = sorted(set(oracle) - page_paths)
    if len(remainder) != 43:
        raise RuntimeError(f"Expected 43 non-applet public files, found {len(remainder)}")

    if SNAPSHOT_ROOT.exists():
        shutil.rmtree(SNAPSHOT_ROOT)

    rows: list[dict[str, object]] = []
    existing_count = 0
    snapshot_count = 0
    existing_bytes = 0
    snapshot_bytes = 0

    for public_path in remainder:
        public = SITE / public_path
        data = public.read_bytes()
        actual_sha = digest_bytes(data)
        expected_sha = oracle[public_path]
        if actual_sha != expected_sha:
            raise RuntimeError(f"Built public remainder differs from frozen oracle: {public_path}")

        candidate_value = PREFERRED_EXISTING.get(public_path, public_path)
        candidate = ROOT / candidate_value
        if candidate.is_file() and candidate.read_bytes() == data:
            source_kind = "canonical-existing"
            source_path = candidate_value
            existing_count += 1
            existing_bytes += len(data)
        else:
            source_kind = "current-snapshot"
            source_path = f"src/site/current/{public_path}"
            target = ROOT / source_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            snapshot_count += 1
            snapshot_bytes += len(data)

        rows.append({
            "public_path": public_path,
            "source_kind": source_kind,
            "source_path": source_path,
            "sha256": actual_sha,
            "bytes": len(data),
        })

    payload = {
        "schema_version": 1,
        "phase": "v1.9-r5a-public-remainder-ownership",
        "public_release_boundary": "v1.8.1",
        "artifact_oracle": "src/product/public-artifact-sha256.json",
        "canonical_applet_page_count": 15,
        "public_remainder_count": 43,
        "total_public_file_count": 58,
        "source_kinds": ["canonical-existing", "current-snapshot"],
        "counts": {
            "canonical_existing": existing_count,
            "current_snapshot": snapshot_count,
        },
        "bytes": {
            "canonical_existing": existing_bytes,
            "current_snapshot": snapshot_bytes,
            "total": existing_bytes + snapshot_bytes,
        },
        "files": rows,
        "notes": {
            "snapshotMeaning": "current-snapshot is exact accepted current output materialized only where no byte-identical canonical repository source already exists; it is an ownership bridge, not a claim that support-page architecture is fully decomposed.",
            "next": "R5b makes the current builder emit all 58 files directly from this remainder map plus the canonical applet page graph, then removes the historical release ladder from the current build path."
        },
    }
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Re-read every declared source after writing to make the materialization fail closed.
    for row in rows:
        source = ROOT / str(row["source_path"])
        if not source.is_file():
            raise RuntimeError(f"Canonical remainder source missing after materialization: {row['source_path']}")
        data = source.read_bytes()
        if digest_bytes(data) != row["sha256"] or len(data) != row["bytes"]:
            raise RuntimeError(f"Canonical remainder source drift after materialization: {row['public_path']}")

    print(
        "R5a public remainder materialized: PASS — "
        f"43 files = {existing_count} existing canonical + {snapshot_count} exact current snapshots"
    )


if __name__ == "__main__":
    main()
