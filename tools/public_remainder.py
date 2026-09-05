#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import page_components

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "src" / "product" / "public-remainder.json"
ORACLE = ROOT / "src" / "product" / "public-artifact-sha256.json"
EXPECTED_PHASE = "v1.9-r5a-public-remainder-ownership"
EXPECTED_REMAINDER_COUNT = 43
EXPECTED_EXISTING = 29
EXPECTED_SNAPSHOTS = 14
EXPECTED_TOTAL_FILES = 58
EXPECTED_SNAPSHOT_PUBLIC_PATHS = {
    "404.html",
    "activities/cnn-1.html",
    "activities/index.html",
    "activities/nn-1.html",
    "assets/localization-r4.js",
    "curriculum.html",
    "index.html",
    "quality.html",
    "release-notes.html",
    "research-and-citation.html",
    "sitemap.xml",
    "student-lab.html",
    "teacher-pack.html",
    "tests/index.html",
}


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_and_validate() -> dict[str, object]:
    manifest = load_json(MANIFEST)
    oracle = load_json(ORACLE)
    pages = page_components.load_and_validate()
    page_paths = {row["public_path"] for row in pages["page_evidence"].values()}
    expected_public_paths = set(oracle) - page_paths

    require(manifest.get("schema_version") == 1, "R5a public-remainder schema drift")
    require(manifest.get("phase") == EXPECTED_PHASE, "R5a public-remainder phase drift")
    require(manifest.get("public_release_boundary") == "v1.8.1", "R5a release boundary drift")
    require(manifest.get("artifact_oracle") == "src/product/public-artifact-sha256.json", "R5a oracle ownership drift")
    require(manifest.get("canonical_applet_page_count") == 15, "R5a applet-page count drift")
    require(manifest.get("public_remainder_count") == EXPECTED_REMAINDER_COUNT, "R5a remainder count drift")
    require(manifest.get("total_public_file_count") == EXPECTED_TOTAL_FILES, "R5a total public-file count drift")
    require(manifest.get("source_kinds") == ["canonical-existing", "current-snapshot"], "R5a source-kind contract drift")

    rows = manifest.get("files")
    require(isinstance(rows, list), "R5a public-remainder files registry is not a list")
    require(len(rows) == EXPECTED_REMAINDER_COUNT, f"R5a public-remainder row count drift: {len(rows)}")

    public_paths: list[str] = []
    source_paths: list[str] = []
    existing = 0
    snapshots = 0
    existing_bytes = 0
    snapshot_bytes = 0
    snapshot_public_paths: set[str] = set()
    evidence: dict[str, dict[str, object]] = {}

    for row in rows:
        require(isinstance(row, dict), "R5a public-remainder row is not an object")
        public_path = row.get("public_path")
        source_kind = row.get("source_kind")
        source_path = row.get("source_path")
        sha256 = row.get("sha256")
        byte_count = row.get("bytes")

        require(isinstance(public_path, str) and public_path, "R5a public path missing")
        require(isinstance(source_path, str) and source_path, f"R5a source path missing for {public_path}")
        require(source_kind in {"canonical-existing", "current-snapshot"}, f"R5a source kind invalid for {public_path}")
        require(isinstance(sha256, str) and len(sha256) == 64, f"R5a SHA invalid for {public_path}")
        require(isinstance(byte_count, int) and byte_count >= 0, f"R5a byte count invalid for {public_path}")
        require(public_path not in page_paths, f"R5a remainder illegally owns canonical applet page: {public_path}")
        require(public_path in oracle, f"R5a remainder owns path outside public oracle: {public_path}")
        require(sha256 == oracle[public_path], f"R5a remainder hash does not match public oracle: {public_path}")

        source = ROOT / source_path
        require(source.is_file(), f"R5a canonical source missing: {source_path}")
        raw = source.read_bytes()
        require(digest_bytes(raw) == sha256, f"R5a canonical source hash drift: {public_path}")
        require(len(raw) == byte_count, f"R5a canonical source byte-count drift: {public_path}")

        if source_kind == "current-snapshot":
            require(source_path == f"src/site/current/{public_path}", f"R5a snapshot path is not canonical current path: {public_path}")
            snapshots += 1
            snapshot_bytes += len(raw)
            snapshot_public_paths.add(public_path)
        else:
            require(not source_path.startswith("src/site/current/"), f"R5a existing source incorrectly points at snapshot root: {public_path}")
            existing += 1
            existing_bytes += len(raw)

        public_paths.append(public_path)
        source_paths.append(source_path)
        evidence[public_path] = {
            "source_kind": source_kind,
            "source_path": source_path,
            "sha256": sha256,
            "bytes": byte_count,
        }

    require(len(public_paths) == len(set(public_paths)), "R5a public remainder has duplicate public paths")
    require(len(source_paths) == len(set(source_paths)), "R5a public remainder has duplicate canonical source paths")
    require(set(public_paths) == expected_public_paths, f"R5a public remainder coverage drift: missing={sorted(expected_public_paths-set(public_paths))}, extra={sorted(set(public_paths)-expected_public_paths)}")
    require(existing == EXPECTED_EXISTING, f"R5a existing-source count drift: {existing}")
    require(snapshots == EXPECTED_SNAPSHOTS, f"R5a snapshot count drift: {snapshots}")
    require(snapshot_public_paths == EXPECTED_SNAPSHOT_PUBLIC_PATHS, f"R5a snapshot ownership set drift: {sorted(snapshot_public_paths)}")

    declared_counts = manifest.get("counts")
    require(declared_counts == {"canonical_existing": existing, "current_snapshot": snapshots}, "R5a declared ownership counts drift")
    declared_bytes = manifest.get("bytes")
    require(isinstance(declared_bytes, dict), "R5a declared byte metrics missing")
    require(declared_bytes.get("canonical_existing") == existing_bytes, "R5a existing-source byte metric drift")
    require(declared_bytes.get("current_snapshot") == snapshot_bytes, "R5a snapshot byte metric drift")
    require(declared_bytes.get("total") == existing_bytes + snapshot_bytes, "R5a total remainder byte metric drift")

    return {
        "manifest": manifest,
        "files": rows,
        "public_paths": public_paths,
        "evidence": evidence,
        "counts": {"canonical_existing": existing, "current_snapshot": snapshots},
        "bytes": {"canonical_existing": existing_bytes, "current_snapshot": snapshot_bytes, "total": existing_bytes + snapshot_bytes},
        "snapshot_public_paths": sorted(snapshot_public_paths),
        "pass": True,
    }


if __name__ == "__main__":
    state = load_and_validate()
    print(
        "R5a public remainder: PASS — "
        f"43 files / {state['counts']['canonical_existing']} existing canonical / "
        f"{state['counts']['current_snapshot']} exact current snapshots"
    )
