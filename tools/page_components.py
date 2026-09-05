#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "src" / "product" / "page-components.json"
ORACLE = ROOT / "src" / "product" / "public-artifact-sha256.json"
EXPECTED_PHASE = "v1.9-r3-shared-page-components"
EXPECTED_PAGE_COUNT = 15
EXPECTED_COMPONENT_COUNT = 17
EXPECTED_DEDUPLICATED_BYTES = 247_281
MARKER_PREFIX = b"<!-- AI_PLAYGROUNDS_COMPONENT:"


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def marker(key: str) -> bytes:
    return f"<!-- AI_PLAYGROUNDS_COMPONENT:{key} -->".encode("ascii")


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_and_validate() -> dict[str, object]:
    graph = load_json(MANIFEST)
    oracle = load_json(ORACLE)

    _require(graph.get("schema_version") == 1, "R3 page-component schema version drift")
    _require(graph.get("phase") == EXPECTED_PHASE, "R3 page-component phase drift")
    _require(graph.get("marker_format") == "<!-- AI_PLAYGROUNDS_COMPONENT:<key> -->", "R3 marker contract drift")

    pages = graph.get("pages")
    components = graph.get("components")
    _require(isinstance(pages, list), "R3 pages registry is not a list")
    _require(isinstance(components, dict), "R3 component registry is not an object")
    _require(len(pages) == EXPECTED_PAGE_COUNT, f"R3 page count drift: {len(pages)}")
    _require(len(components) == EXPECTED_COMPONENT_COUNT, f"R3 component count drift: {len(components)}")
    _require(graph.get("page_count") == EXPECTED_PAGE_COUNT, "R3 declared page count drift")
    _require(graph.get("component_count") == EXPECTED_COMPONENT_COUNT, "R3 declared component count drift")

    component_payloads: dict[str, bytes] = {}
    declared_users: dict[str, set[str]] = {}
    for key, row in components.items():
        _require(isinstance(key, str) and key, "R3 component key is invalid")
        _require(isinstance(row, dict), f"R3 component metadata is invalid: {key}")
        path_value = row.get("path")
        _require(isinstance(path_value, str) and path_value, f"R3 component path missing: {key}")
        path = ROOT / path_value
        _require(path.is_file(), f"R3 component file missing: {path_value}")
        raw = path.read_bytes()
        actual_sha = digest_bytes(raw)
        _require(actual_sha == row.get("sha256"), f"R3 component hash drift: {key}")
        _require(len(raw) == row.get("bytes"), f"R3 component byte-count drift: {key}")
        users = row.get("users")
        _require(isinstance(users, list) and users, f"R3 component has no declared users: {key}")
        _require(len(users) == len(set(users)), f"R3 component has duplicate users: {key}")
        component_payloads[key] = raw
        declared_users[key] = set(users)

    slugs: list[str] = []
    public_paths: list[str] = []
    templates: list[str] = []
    actual_users: dict[str, set[str]] = {key: set() for key in components}
    reconstructed: dict[str, bytes] = {}
    page_evidence: dict[str, dict[str, object]] = {}

    for row in pages:
        _require(isinstance(row, dict), "R3 page metadata row is invalid")
        slug = row.get("slug")
        template_value = row.get("template")
        public_path = row.get("public_path")
        refs = row.get("components")
        _require(isinstance(slug, str) and slug, "R3 page slug missing")
        _require(isinstance(template_value, str) and template_value, f"R3 template path missing: {slug}")
        _require(isinstance(public_path, str) and public_path, f"R3 public path missing: {slug}")
        _require(isinstance(refs, list), f"R3 component reference list missing: {slug}")
        _require(len(refs) == len(set(refs)), f"R3 page repeats a component reference: {slug}")
        _require(public_path == f"playgrounds/{slug}/index.html", f"R3 public path/slug mismatch: {slug}")
        _require(set(refs) <= set(components), f"R3 page references unknown component: {slug}")

        template_path = ROOT / template_value
        _require(template_path.is_file(), f"R3 template file missing: {template_value}")
        template = template_path.read_bytes()
        page = template
        for key in refs:
            token = marker(key)
            _require(page.count(token) == 1, f"R3 template marker count drift: {slug} / {key}")
            page = page.replace(token, component_payloads[key], 1)
            actual_users[key].add(slug)
        _require(MARKER_PREFIX not in page, f"R3 unresolved component marker after reconstruction: {slug}")

        actual_sha = digest_bytes(page)
        expected_sha = row.get("sha256")
        oracle_sha = oracle.get(public_path)
        _require(actual_sha == expected_sha, f"R3 reconstructed page hash drift: {slug}")
        _require(actual_sha == oracle_sha, f"R3 reconstructed page no longer matches frozen oracle: {slug}")
        _require(len(page) == row.get("bytes"), f"R3 reconstructed page byte-count drift: {slug}")

        slugs.append(slug)
        public_paths.append(public_path)
        templates.append(template_value)
        reconstructed[slug] = page
        page_evidence[slug] = {
            "template": template_value,
            "public_path": public_path,
            "sha256": actual_sha,
            "bytes": len(page),
            "components": list(refs),
        }

    _require(len(slugs) == len(set(slugs)), "R3 page slugs are not unique")
    _require(len(public_paths) == len(set(public_paths)), "R3 public page paths are not unique")
    _require(len(templates) == len(set(templates)), "R3 template paths are not unique")

    for key in components:
        _require(
            actual_users[key] == declared_users[key],
            f"R3 component user-set drift for {key}: actual={sorted(actual_users[key])}, declared={sorted(declared_users[key])}",
        )

    full_page_bytes = sum(len(data) for data in reconstructed.values())
    template_bytes = sum((ROOT / value).stat().st_size for value in templates)
    component_bytes = sum(len(data) for data in component_payloads.values())
    deduplicated_bytes = full_page_bytes - (template_bytes + component_bytes)

    _require(full_page_bytes == graph.get("full_page_bytes"), "R3 full-page byte metric drift")
    _require(template_bytes == graph.get("template_bytes"), "R3 template byte metric drift")
    _require(component_bytes == graph.get("component_bytes"), "R3 component byte metric drift")
    _require(deduplicated_bytes == graph.get("deduplicated_bytes"), "R3 deduplication metric drift")
    _require(deduplicated_bytes == EXPECTED_DEDUPLICATED_BYTES, "R3 accepted deduplication boundary drift")

    return {
        "graph": graph,
        "pages": pages,
        "components": components,
        "slugs": slugs,
        "reconstructed": reconstructed,
        "page_evidence": page_evidence,
        "component_payloads": component_payloads,
        "metrics": {
            "full_page_bytes": full_page_bytes,
            "template_bytes": template_bytes,
            "component_bytes": component_bytes,
            "deduplicated_bytes": deduplicated_bytes,
        },
        "pass": True,
    }


if __name__ == "__main__":
    state = load_and_validate()
    print(
        "R3 page components: PASS — "
        f"{len(state['slugs'])} pages / {len(state['components'])} components / "
        f"{state['metrics']['deduplicated_bytes']} duplicate source bytes removed"
    )
