#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import token_components

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "src" / "product" / "page-components.json"
ORACLE = ROOT / "src" / "product" / "public-artifact-sha256.json"
EXPECTED_PHASES = {
    "v1.9-r3-shared-page-components",
    "v1.9-r4b-token-owned-components",
}
EXPECTED_PAGE_COUNT = 15
EXPECTED_COMPONENT_COUNT = 17
EXPECTED_DEDUPLICATED_BYTES = 247_281
MARKER_PREFIX = b"<!-- AI_PLAYGROUNDS_COMPONENT:"
TOKEN_COMPONENT_MANIFEST = "src/design/token-components.json"


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

    _require(graph.get("schema_version") in {1, 2}, "Page-component schema version drift")
    phase = graph.get("phase")
    _require(phase in EXPECTED_PHASES, f"Page-component phase drift: {phase!r}")
    _require(graph.get("marker_format") == "<!-- AI_PLAYGROUNDS_COMPONENT:<key> -->", "Page-component marker contract drift")

    pages = graph.get("pages")
    components = graph.get("components")
    _require(isinstance(pages, list), "Page registry is not a list")
    _require(isinstance(components, dict), "Component registry is not an object")
    _require(len(pages) == EXPECTED_PAGE_COUNT, f"Page count drift: {len(pages)}")
    _require(len(components) == EXPECTED_COMPONENT_COUNT, f"Component count drift: {len(components)}")
    _require(graph.get("page_count") == EXPECTED_PAGE_COUNT, "Declared page count drift")
    _require(graph.get("component_count") == EXPECTED_COMPONENT_COUNT, "Declared component count drift")

    source_kinds: dict[str, str] = {}
    for key, row in components.items():
        _require(isinstance(row, dict), f"Component metadata is invalid: {key}")
        source_kind = row.get("source_kind", "raw")
        _require(source_kind in {"raw", "token-template"}, f"Unsupported component source kind {source_kind!r}: {key}")
        source_kinds[key] = source_kind

    token_keys = {key for key, kind in source_kinds.items() if kind == "token-template"}
    if phase == "v1.9-r3-shared-page-components":
        _require(not token_keys, "R3 page graph cannot claim token-template component ownership")
    if phase == "v1.9-r4b-token-owned-components":
        _require(graph.get("token_component_manifest") == TOKEN_COMPONENT_MANIFEST, "R4b token-component manifest ownership drift")
        _require(graph.get("token_template_component_count") == len(token_keys), "R4b declared token-template component count drift")
        _require(len(token_keys) == token_components.EXPECTED_COMPONENTS, "R4b token-template component cardinality drift")

    token_state = None
    if token_keys:
        token_state = token_components.load_and_render(require_raw_equivalence=False)
        _require(token_state["phase"] == "v1.9-r4b-token-owned-components", "Final page graph requires final token-component manifest phase")
        _require(set(token_state["components"]) == token_keys, "Page graph/token-component manifest membership drift")

    component_payloads: dict[str, bytes] = {}
    declared_users: dict[str, set[str]] = {}
    component_evidence: dict[str, dict[str, object]] = {}
    for key, row in components.items():
        source_kind = source_kinds[key]
        if source_kind == "raw":
            path_value = row.get("path")
            _require(isinstance(path_value, str) and path_value, f"Raw component path missing: {key}")
            path = ROOT / path_value
            _require(path.is_file(), f"Raw component file missing: {path_value}")
            raw = path.read_bytes()
            source_evidence = {"source_kind": "raw", "path": path_value}
        else:
            _require(row.get("token_component_manifest") == TOKEN_COMPONENT_MANIFEST, f"Token-template manifest pointer drift: {key}")
            _require("path" not in row, f"Token-template component still exposes raw path ownership: {key}")
            assert token_state is not None
            raw = token_state["components"][key]
            source_evidence = {
                "source_kind": "token-template",
                "token_component_manifest": TOKEN_COMPONENT_MANIFEST,
                "template": token_state["evidence"][key]["template"],
                "binding_count": token_state["evidence"][key]["binding_count"],
            }

        actual_sha = digest_bytes(raw)
        _require(actual_sha == row.get("sha256"), f"Component rendered hash drift: {key}")
        _require(len(raw) == row.get("bytes"), f"Component rendered byte-count drift: {key}")
        users = row.get("users")
        _require(isinstance(users, list) and users, f"Component has no declared users: {key}")
        _require(len(users) == len(set(users)), f"Component has duplicate users: {key}")
        component_payloads[key] = raw
        declared_users[key] = set(users)
        component_evidence[key] = {
            **source_evidence,
            "sha256": actual_sha,
            "bytes": len(raw),
            "users": list(users),
        }

    slugs: list[str] = []
    public_paths: list[str] = []
    templates: list[str] = []
    actual_users: dict[str, set[str]] = {key: set() for key in components}
    reconstructed: dict[str, bytes] = {}
    page_evidence: dict[str, dict[str, object]] = {}

    for row in pages:
        _require(isinstance(row, dict), "Page metadata row is invalid")
        slug = row.get("slug")
        template_value = row.get("template")
        public_path = row.get("public_path")
        refs = row.get("components")
        _require(isinstance(slug, str) and slug, "Page slug missing")
        _require(isinstance(template_value, str) and template_value, f"Template path missing: {slug}")
        _require(isinstance(public_path, str) and public_path, f"Public path missing: {slug}")
        _require(isinstance(refs, list), f"Component reference list missing: {slug}")
        _require(len(refs) == len(set(refs)), f"Page repeats a component reference: {slug}")
        _require(public_path == f"playgrounds/{slug}/index.html", f"Public path/slug mismatch: {slug}")
        _require(set(refs) <= set(components), f"Page references unknown component: {slug}")

        template_path = ROOT / template_value
        _require(template_path.is_file(), f"Template file missing: {template_value}")
        template = template_path.read_bytes()
        page = template
        for key in refs:
            component_marker = marker(key)
            _require(page.count(component_marker) == 1, f"Page template marker count drift: {slug} / {key}")
            page = page.replace(component_marker, component_payloads[key], 1)
            actual_users[key].add(slug)
        _require(MARKER_PREFIX not in page, f"Unresolved page-component marker after reconstruction: {slug}")

        actual_sha = digest_bytes(page)
        expected_sha = row.get("sha256")
        oracle_sha = oracle.get(public_path)
        _require(actual_sha == expected_sha, f"Reconstructed page hash drift: {slug}")
        _require(actual_sha == oracle_sha, f"Reconstructed page no longer matches frozen oracle: {slug}")
        _require(len(page) == row.get("bytes"), f"Reconstructed page byte-count drift: {slug}")

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

    _require(len(slugs) == len(set(slugs)), "Page slugs are not unique")
    _require(len(public_paths) == len(set(public_paths)), "Public page paths are not unique")
    _require(len(templates) == len(set(templates)), "Template paths are not unique")

    for key in components:
        _require(
            actual_users[key] == declared_users[key],
            f"Component user-set drift for {key}: actual={sorted(actual_users[key])}, declared={sorted(declared_users[key])}",
        )

    full_page_bytes = sum(len(data) for data in reconstructed.values())
    template_bytes = sum((ROOT / value).stat().st_size for value in templates)
    component_bytes = sum(len(data) for data in component_payloads.values())
    deduplicated_bytes = full_page_bytes - (template_bytes + component_bytes)

    _require(full_page_bytes == graph.get("full_page_bytes"), "Full-page byte metric drift")
    _require(template_bytes == graph.get("template_bytes"), "Page-template byte metric drift")
    _require(component_bytes == graph.get("component_bytes"), "Rendered component byte metric drift")
    _require(deduplicated_bytes == graph.get("deduplicated_bytes"), "Page-component deduplication metric drift")
    _require(deduplicated_bytes == EXPECTED_DEDUPLICATED_BYTES, "Accepted page-component deduplication boundary drift")

    return {
        "graph": graph,
        "phase": phase,
        "pages": pages,
        "components": components,
        "slugs": slugs,
        "reconstructed": reconstructed,
        "page_evidence": page_evidence,
        "component_payloads": component_payloads,
        "component_evidence": component_evidence,
        "component_source_kinds": source_kinds,
        "token_template_components": sorted(token_keys),
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
        "Page components: PASS — "
        f"{len(state['slugs'])} pages / {len(state['components'])} components / "
        f"{len(state['token_template_components'])} token-template components / "
        f"{state['metrics']['deduplicated_bytes']} duplicate source bytes removed"
    )
