#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import design_tokens
import page_components
import public_remainder

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
ORACLE = ROOT / "src" / "product" / "public-artifact-sha256.json"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def artifact_hashes(site: Path = SITE) -> dict[str, str]:
    return {
        str(path.relative_to(site)).replace("\\", "/"): digest(path)
        for path in sorted(site.rglob("*"))
        if path.is_file()
    }


def compare_hash_maps(expected: dict[str, str], actual: dict[str, str]) -> dict[str, object]:
    expected_keys = set(expected)
    actual_keys = set(actual)
    added = sorted(actual_keys - expected_keys)
    removed = sorted(expected_keys - actual_keys)
    changed = sorted(path for path in expected_keys & actual_keys if expected[path] != actual[path])
    return {
        "expected_files": len(expected),
        "actual_files": len(actual),
        "added": added,
        "removed": removed,
        "changed": changed,
        "pass": not (added or removed or changed),
    }


def build_direct(site: Path = SITE) -> dict[str, object]:
    pages = page_components.load_and_validate()
    token_contract = design_tokens.validate_contract()
    remainder = public_remainder.load_and_validate()
    oracle = json.loads(ORACLE.read_text(encoding="utf-8"))

    if site.exists():
        shutil.rmtree(site)
    site.mkdir(parents=True, exist_ok=True)

    remainder_emit = public_remainder.emit(site, remainder)
    page_emit: dict[str, dict[str, object]] = {}
    reconstructed = pages["reconstructed"]
    evidence = pages["page_evidence"]
    for slug in pages["slugs"]:
        info = evidence[slug]
        public_path = str(info["public_path"])
        raw = reconstructed[slug]
        target = site / public_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        actual = target.read_bytes()
        actual_sha = hashlib.sha256(actual).hexdigest()
        if actual_sha != info["sha256"] or len(actual) != info["bytes"]:
            raise RuntimeError(f"R5b direct applet-page emission drift: {slug}")
        page_emit[slug] = {
            "public_path": public_path,
            "sha256": actual_sha,
            "bytes": len(actual),
        }

    hashes = artifact_hashes(site)
    comparison = compare_hash_maps(oracle, hashes)
    if remainder_emit["file_count"] != 43 or len(page_emit) != 15:
        raise RuntimeError("R5b direct emission must be exactly 43 remainder + 15 applet pages")
    if len(hashes) != 58:
        raise RuntimeError(f"R5b direct emission produced {len(hashes)} files instead of 58")
    if not comparison["pass"]:
        raise RuntimeError(
            "R5b direct site differs from frozen v1.8.1 oracle: "
            f"added={comparison['added']}, removed={comparison['removed']}, changed={comparison['changed']}"
        )

    return {
        "remainder": remainder_emit,
        "pages": {"file_count": len(page_emit), "files": page_emit, "pass": True},
        "design_tokens": {
            "token_count": token_contract["token_count"],
            "alias_count": token_contract["alias_count"],
            "binding_phase": token_contract["binding_phase"],
            "pass": token_contract["pass"],
        },
        "artifact": comparison,
        "hashes": hashes,
        "pass": True,
    }


if __name__ == "__main__":
    result = build_direct()
    print(
        "R5b direct current site: PASS — "
        f"{result['remainder']['file_count']} remainder + {result['pages']['file_count']} applet pages = "
        f"{result['artifact']['actual_files']} frozen public files"
    )
