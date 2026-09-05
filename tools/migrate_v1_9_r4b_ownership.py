#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import token_components

ROOT = Path(__file__).resolve().parents[1]
PAGE_GRAPH = ROOT / "src" / "product" / "page-components.json"
TOKEN_COMPONENTS = ROOT / "src" / "design" / "token-components.json"
BINDINGS = ROOT / "src" / "design" / "current-bindings.json"
RELEASE = ROOT / "src" / "product" / "release.json"
TOKEN_MANIFEST_PATH = "src/design/token-components.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    # The candidate renderer must prove equality to all six R4a raw sources
    # immediately before ownership transfer.
    candidate = token_components.load_and_render(require_raw_equivalence=True)
    require(candidate["phase"] == "v1.9-r4b-token-owned-components-candidate", "R4b migration requires candidate token-component phase")
    require(candidate["component_count"] == 6 and candidate["binding_count"] == 21, "R4b candidate cardinality drift")

    page_graph = json.loads(PAGE_GRAPH.read_text(encoding="utf-8"))
    token_manifest = json.loads(TOKEN_COMPONENTS.read_text(encoding="utf-8"))
    bindings = json.loads(BINDINGS.read_text(encoding="utf-8"))
    release = json.loads(RELEASE.read_text(encoding="utf-8"))

    require(page_graph.get("phase") == "v1.9-r3-shared-page-components", "R4b migration requires R3 page graph")
    require(token_manifest.get("phase") == "v1.9-r4b-token-owned-components-candidate", "R4b migration token manifest phase drift")
    require(bindings.get("phase") == "v1.9-r4a-design-token-contract", "R4b migration requires R4a bindings")
    require(release.get("architecture_phase") == "v1.9-r4a-design-token-contract", "R4b migration requires R4a release phase")

    selected = set(token_manifest["components"])
    require(len(selected) == 6, "R4b selected component count drift")
    raw_paths: list[str] = []

    page_graph["schema_version"] = 2
    page_graph["phase"] = "v1.9-r4b-token-owned-components"
    page_graph["token_component_manifest"] = TOKEN_MANIFEST_PATH
    page_graph["token_template_component_count"] = len(selected)
    for key, row in page_graph["components"].items():
        require(isinstance(row, dict), f"Invalid page component row: {key}")
        if key in selected:
            manifest_row = token_manifest["components"][key]
            raw_source = manifest_row.get("r4a_raw_source")
            require(row.get("path") == raw_source, f"R4b raw component path mismatch: {key}")
            require(row.get("sha256") == manifest_row.get("rendered_sha256"), f"R4b rendered hash mismatch: {key}")
            require(row.get("bytes") == manifest_row.get("rendered_bytes"), f"R4b rendered byte-count mismatch: {key}")
            require(isinstance(raw_source, str) and (ROOT / raw_source).is_file(), f"R4b raw source missing at migration: {key}")
            raw_paths.append(raw_source)
            row.pop("path", None)
            row["source_kind"] = "token-template"
            row["token_component_manifest"] = TOKEN_MANIFEST_PATH
        else:
            require(isinstance(row.get("path"), str) and (ROOT / row["path"]).is_file(), f"R4b remaining raw component missing: {key}")
            row["source_kind"] = "raw"

    token_manifest["phase"] = "v1.9-r4b-token-owned-components"
    for key, row in token_manifest["components"].items():
        raw_source = row.pop("r4a_raw_source", None)
        require(isinstance(raw_source, str) and raw_source in raw_paths, f"R4b superseded raw source mismatch: {key}")
        row["superseded_r4a_raw_source"] = raw_source

    old_literal_rows = bindings.pop("componentLiteralBindings", None)
    require(isinstance(old_literal_rows, list) and len(old_literal_rows) == 21, "R4b requires 21 R4a literal bindings")
    bindings["schema_version"] = 2
    bindings["phase"] = "v1.9-r4b-token-owned-components"
    bindings["tokenComponentManifest"] = TOKEN_MANIFEST_PATH
    rendered_rows: list[dict] = []
    template_rows: list[dict] = []
    for component, row in token_manifest["components"].items():
        template = row["template"]
        for binding in row["bindings"]:
            rendered_rows.append(
                {
                    "component": component,
                    "token": binding["token"],
                    "rendered_needle": binding["rendered_needle"],
                    "count": binding["count"],
                }
            )
            template_rows.append(
                {
                    "component": component,
                    "template": template,
                    "token": binding["token"],
                    "marker": binding["marker"],
                    "template_needle": binding["template_needle"],
                    "rendered_needle": binding["rendered_needle"],
                    "count": binding["count"],
                }
            )
    require(len(rendered_rows) == len(template_rows) == 21, "R4b derived binding cardinality drift")
    bindings["renderedComponentLiteralBindings"] = rendered_rows
    bindings["tokenTemplateBindings"] = template_rows
    notes = bindings.setdefault("notes", {})
    notes["sourceOwnership"] = (
        "Six high-confidence shared components are now rendered from DTCG token templates. "
        "The remaining eleven shared components remain raw canonical sources until later evidence supports tokenization."
    )
    notes["noVisualAuthority"] = (
        "R4b transfers source ownership only. Rendered shared-component and public applet bytes remain frozen v1.8.1; "
        "visible normalization remains owned by v1.9 visual/accessibility evidence work."
    )

    release["architecture_phase"] = "v1.9-r4b-token-owned-components"
    release["design_token_phase"] = "token-owned-shared-component-source"
    release["token_component_manifest"] = TOKEN_MANIFEST_PATH
    release["token_template_component_count"] = 6
    release["token_template_binding_count"] = 21
    release["token_template_rendered_component_bytes"] = token_manifest["rendered_component_bytes"]
    release["token_template_source_bytes"] = token_manifest["token_template_bytes"]
    release["historical_manifest_note"] = (
        "Historical applet sources, candidate builders, and release-layer transforms remain legacy equivalence/provenance inputs during R4b. "
        "Current applet-page authority is src/labs/*/index.template.html plus src/product/page-components.json; six shared components are rendered from "
        "src/design/token-components.json and the DTCG token contract; the remaining eleven shared components remain raw canonical component sources. "
        "Current public catalogue authority remains src/product/catalogue.json."
    )

    write_json(PAGE_GRAPH, page_graph)
    write_json(TOKEN_COMPONENTS, token_manifest)
    write_json(BINDINGS, bindings)
    write_json(RELEASE, release)

    for raw_source in raw_paths:
        path = ROOT / raw_source
        require(path.is_file(), f"R4b raw source vanished before retirement: {raw_source}")
        path.unlink()

    print(
        "R4b ownership migration staged: 6 token-template components / 21 bindings / "
        f"{len(raw_paths)} redundant raw component sources retired"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
