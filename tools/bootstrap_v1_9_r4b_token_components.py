#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path

import design_tokens

ROOT = Path(__file__).resolve().parents[1]
BINDINGS = ROOT / "src" / "design" / "current-bindings.json"
PAGE_COMPONENTS = ROOT / "src" / "product" / "page-components.json"
OUTPUT_MANIFEST = ROOT / "src" / "design" / "token-components.json"

EXPECTED_BINDINGS = 21
EXPECTED_COMPONENTS = 6
MARKER_PREFIX = "{{dt:"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def marker(token_path: str) -> str:
    return "{{dt:" + token_path + "}}"


def main() -> int:
    binding_payload = json.loads(BINDINGS.read_text(encoding="utf-8"))
    page_graph = json.loads(PAGE_COMPONENTS.read_text(encoding="utf-8"))
    rows = binding_payload.get("componentLiteralBindings")
    require(isinstance(rows, list) and len(rows) == EXPECTED_BINDINGS, "R4b requires the accepted 21 R4a component literal bindings")

    path_to_component = {
        str(meta.get("path")): key
        for key, meta in page_graph.get("components", {}).items()
        if isinstance(meta, dict) and isinstance(meta.get("path"), str)
    }
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        require(isinstance(row, dict), "R4a component literal binding is not an object")
        resource = row.get("resource")
        token_path = row.get("token")
        needle = row.get("needle")
        count = row.get("count")
        require(resource in path_to_component, f"R4a binding resource is not a page component: {resource}")
        require(isinstance(token_path, str) and token_path, f"R4a binding token missing: {resource}")
        require(isinstance(needle, str) and needle, f"R4a binding needle missing: {resource}")
        require(isinstance(count, int) and count >= 1, f"R4a binding count invalid: {resource}")
        grouped[resource].append(row)

    require(len(grouped) == EXPECTED_COMPONENTS, f"R4b expected {EXPECTED_COMPONENTS} token-owned components, found {len(grouped)}")

    token_document = design_tokens.load_json(design_tokens.TOKENS)
    tokens = design_tokens.collect_tokens(token_document)
    components: dict[str, dict] = {}
    total_template_bytes = 0
    total_rendered_bytes = 0
    binding_count = 0

    for resource in sorted(grouped):
        component_key = path_to_component[resource]
        source_path = ROOT / resource
        require(source_path.is_file(), f"R4b source component missing: {resource}")
        original = source_path.read_text(encoding="utf-8")
        template = original
        binding_records: list[dict] = []

        # Longer needles first avoids any future partial-overlap ambiguity.
        for row in sorted(grouped[resource], key=lambda item: len(str(item["needle"])), reverse=True):
            token_path = str(row["token"])
            needle = str(row["needle"])
            count = int(row["count"])
            resolved = design_tokens.css_value(tokens, token_path)
            require(resolved in needle, f"Resolved token value {resolved!r} is not represented in R4a needle {needle!r}")
            actual = template.count(needle)
            require(actual == count, f"R4b literal count drift before templating {component_key} / {needle}: {actual} != {count}")
            token_marker = marker(token_path)
            require(token_marker not in template, f"R4b token marker already exists before insertion: {component_key} / {token_path}")
            templated_needle = needle.replace(resolved, token_marker, 1)
            template = template.replace(needle, templated_needle)
            binding_records.append(
                {
                    "token": token_path,
                    "marker": token_marker,
                    "rendered_needle": needle,
                    "template_needle": templated_needle,
                    "count": count,
                }
            )
            binding_count += 1

        template_path = source_path.with_name(source_path.stem + ".template.html")
        template_path.write_text(template, encoding="utf-8")

        rendered = template
        for record in binding_records:
            token_path = record["token"]
            token_marker = record["marker"]
            count = int(record["count"])
            require(rendered.count(token_marker) == count, f"R4b marker count drift: {component_key} / {token_path}")
            rendered = rendered.replace(token_marker, design_tokens.css_value(tokens, token_path))
        require(MARKER_PREFIX not in rendered, f"R4b unresolved token marker after candidate render: {component_key}")
        require(rendered == original, f"R4b token template does not reconstruct exact component bytes: {component_key}")

        original_bytes = original.encode("utf-8")
        template_bytes = template.encode("utf-8")
        graph_row = page_graph["components"][component_key]
        require(sha256(original_bytes) == graph_row.get("sha256"), f"R4b component source is not bound to R3 hash: {component_key}")
        require(len(original_bytes) == graph_row.get("bytes"), f"R4b component source byte count drift: {component_key}")

        components[component_key] = {
            "template": template_path.relative_to(ROOT).as_posix(),
            "rendered_sha256": sha256(original_bytes),
            "rendered_bytes": len(original_bytes),
            "template_sha256": sha256(template_bytes),
            "template_bytes": len(template_bytes),
            "r4a_raw_source": resource,
            "bindings": binding_records,
        }
        total_template_bytes += len(template_bytes)
        total_rendered_bytes += len(original_bytes)

    require(binding_count == EXPECTED_BINDINGS, f"R4b token-template binding count drift: {binding_count}")
    require(len(components) == EXPECTED_COMPONENTS, f"R4b token-template component count drift: {len(components)}")

    payload = {
        "schema_version": 1,
        "phase": "v1.9-r4b-token-owned-components-candidate",
        "token_contract": "src/design/ai-playgrounds.tokens.json",
        "page_component_manifest": "src/product/page-components.json",
        "marker_format": "{{dt:<token.path>}}",
        "component_count": len(components),
        "binding_count": binding_count,
        "rendered_component_bytes": total_rendered_bytes,
        "token_template_bytes": total_template_bytes,
        "components": components,
    }
    OUTPUT_MANIFEST.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        "R4b token-component candidate: PASS — "
        f"{len(components)} components / {binding_count} bindings / "
        "all candidate templates reconstruct R3 component bytes exactly"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
