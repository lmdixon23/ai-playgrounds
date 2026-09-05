#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import token_values

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "src" / "design" / "token-components.json"
EXPECTED_COMPONENTS = 6
EXPECTED_BINDINGS = 21
ALLOWED_PHASES = {
    "v1.9-r4b-token-owned-components-candidate",
    "v1.9-r4b-token-owned-components",
}
MARKER_PREFIX = "{{dt:"


class TokenComponentError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise TokenComponentError(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_manifest() -> dict[str, Any]:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    require(payload.get("schema_version") == 1, "Token-component schema version drift")
    require(payload.get("phase") in ALLOWED_PHASES, f"Token-component phase drift: {payload.get('phase')!r}")
    require(payload.get("token_contract") == "src/design/ai-playgrounds.tokens.json", "Token-component token contract path drift")
    require(payload.get("page_component_manifest") == "src/product/page-components.json", "Token-component page graph path drift")
    require(payload.get("marker_format") == "{{dt:<token.path>}}", "Token-component marker format drift")
    require(payload.get("component_count") == EXPECTED_COMPONENTS, "Token-component declared component count drift")
    require(payload.get("binding_count") == EXPECTED_BINDINGS, "Token-component declared binding count drift")
    components = payload.get("components")
    require(isinstance(components, dict) and len(components) == EXPECTED_COMPONENTS, "Token-component registry cardinality drift")
    return payload


def _render_component_record(
    key: str,
    row: dict[str, Any],
    tokens: dict[str, dict[str, Any]],
    *,
    require_raw_equivalence: bool,
) -> tuple[bytes, dict[str, Any]]:
    template_value = row.get("template")
    require(isinstance(template_value, str) and template_value, f"Token-component template missing: {key}")
    template_path = ROOT / template_value
    require(template_path.is_file(), f"Token-component template file missing: {template_value}")
    template_bytes = template_path.read_bytes()
    require(digest(template_bytes) == row.get("template_sha256"), f"Token-component template hash drift: {key}")
    require(len(template_bytes) == row.get("template_bytes"), f"Token-component template byte-count drift: {key}")

    try:
        template = template_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise TokenComponentError(f"Token-component template is not UTF-8: {key}") from exc

    bindings = row.get("bindings")
    require(isinstance(bindings, list) and bindings, f"Token-component bindings missing: {key}")
    seen_tokens: set[str] = set()
    rendered = template
    binding_evidence: list[dict[str, Any]] = []
    binding_count = 0

    for binding in bindings:
        require(isinstance(binding, dict), f"Token-component binding is invalid: {key}")
        token_path = binding.get("token")
        marker = binding.get("marker")
        rendered_needle = binding.get("rendered_needle")
        template_needle = binding.get("template_needle")
        count = binding.get("count")
        require(isinstance(token_path, str) and token_path, f"Token-component token path missing: {key}")
        require(isinstance(marker, str) and marker == "{{dt:" + token_path + "}}", f"Token-component marker/token mismatch: {key} / {token_path}")
        require(isinstance(rendered_needle, str) and rendered_needle, f"Rendered needle missing: {key} / {token_path}")
        require(isinstance(template_needle, str) and template_needle, f"Template needle missing: {key} / {token_path}")
        require(isinstance(count, int) and count >= 1, f"Token-component binding count invalid: {key} / {token_path}")
        require(token_path not in seen_tokens, f"Token path repeated within one component manifest record: {key} / {token_path}")
        seen_tokens.add(token_path)

        resolved = token_values.css_value(tokens, token_path)
        require(resolved in rendered_needle, f"Resolved token value is absent from rendered needle: {key} / {token_path}")
        expected_template_needle = rendered_needle.replace(resolved, marker, 1)
        require(template_needle == expected_template_needle, f"Token-component template needle drift: {key} / {token_path}")
        require(template.count(template_needle) == count, f"Token-component template needle count drift: {key} / {token_path}")
        require(rendered.count(marker) == count, f"Token-component marker count drift: {key} / {token_path}")
        rendered = rendered.replace(marker, resolved)
        binding_count += 1
        binding_evidence.append(
            {
                "token": token_path,
                "resolved": resolved,
                "count": count,
                "rendered_needle": rendered_needle,
                "template_needle": template_needle,
            }
        )

    require(MARKER_PREFIX not in rendered, f"Unresolved token-component marker after render: {key}")
    rendered_bytes = rendered.encode("utf-8")
    require(digest(rendered_bytes) == row.get("rendered_sha256"), f"Rendered token-component hash drift: {key}")
    require(len(rendered_bytes) == row.get("rendered_bytes"), f"Rendered token-component byte-count drift: {key}")
    for binding in bindings:
        needle = str(binding["rendered_needle"])
        count = int(binding["count"])
        require(rendered.count(needle) == count, f"Rendered token-component literal count drift: {key} / {needle}")

    raw_equivalence: dict[str, Any] | None = None
    raw_value = row.get("r4a_raw_source")
    if require_raw_equivalence:
        require(isinstance(raw_value, str) and raw_value, f"R4b candidate raw source pointer missing: {key}")
        raw_path = ROOT / raw_value
        require(raw_path.is_file(), f"R4b candidate raw source file missing: {key} / {raw_value}")
        raw = raw_path.read_bytes()
        require(raw == rendered_bytes, f"R4b candidate token template differs from R4a raw component bytes: {key}")
        raw_equivalence = {
            "path": raw_value,
            "sha256": digest(raw),
            "bytes": len(raw),
            "byte_identical": True,
        }

    return rendered_bytes, {
        "template": template_value,
        "template_sha256": digest(template_bytes),
        "template_bytes": len(template_bytes),
        "rendered_sha256": digest(rendered_bytes),
        "rendered_bytes": len(rendered_bytes),
        "binding_count": binding_count,
        "bindings": binding_evidence,
        "raw_equivalence": raw_equivalence,
    }


def load_and_render(*, require_raw_equivalence: bool | None = None) -> dict[str, Any]:
    manifest = load_manifest()
    phase = manifest["phase"]
    if require_raw_equivalence is None:
        require_raw_equivalence = phase.endswith("-candidate")

    token_document, tokens = token_values.load_validated_tokens()
    components: dict[str, bytes] = {}
    evidence: dict[str, Any] = {}
    binding_count = 0
    rendered_total = 0
    template_total = 0

    for key, row in sorted(manifest["components"].items()):
        require(isinstance(row, dict), f"Token-component metadata invalid: {key}")
        rendered, entry = _render_component_record(
            key,
            row,
            tokens,
            require_raw_equivalence=require_raw_equivalence,
        )
        components[key] = rendered
        evidence[key] = entry
        binding_count += int(entry["binding_count"])
        rendered_total += len(rendered)
        template_total += int(entry["template_bytes"])

    require(len(components) == EXPECTED_COMPONENTS, "Rendered token-component cardinality drift")
    require(binding_count == EXPECTED_BINDINGS, f"Rendered token-component binding count drift: {binding_count}")
    require(rendered_total == manifest.get("rendered_component_bytes"), "Rendered token-component aggregate byte metric drift")
    require(template_total == manifest.get("token_template_bytes"), "Token-template aggregate byte metric drift")

    return {
        "phase": phase,
        "schema": token_document.get("$schema"),
        "components": components,
        "evidence": evidence,
        "component_count": len(components),
        "binding_count": binding_count,
        "rendered_component_bytes": rendered_total,
        "token_template_bytes": template_total,
        "raw_equivalence_required": require_raw_equivalence,
        "pass": True,
    }


if __name__ == "__main__":
    result = load_and_render()
    print(
        "R4b token components: PASS — "
        f"{result['component_count']} components / {result['binding_count']} token bindings / "
        f"{result['rendered_component_bytes']} rendered bytes"
    )
