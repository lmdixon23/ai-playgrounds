#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any

import page_components

ROOT = Path(__file__).resolve().parents[1]
TOKENS = ROOT / "src" / "design" / "ai-playgrounds.tokens.json"
BINDINGS = ROOT / "src" / "design" / "current-bindings.json"
CATALOGUE = ROOT / "src" / "product" / "catalogue.json"
EXPECTED_SCHEMA = "https://www.designtokens.org/schemas/2025.10/format.json"
EXPECTED_FORMAT = "DTCG 2025.10"
ALIAS_RE = re.compile(r"^\{([A-Za-z0-9_.-]+)\}$")
HEX_RE = re.compile(r"^#[0-9a-fA-F]{6}$")
CUSTOM_PROPERTY_RE = re.compile(r"(--[A-Za-z0-9_-]+)\s*:\s*([^;{}]+)")
STYLE_OPEN_RE = re.compile(r"<style\b[^>]*>", re.IGNORECASE)


class TokenContractError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise TokenContractError(message)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def collect_tokens(root: dict[str, Any]) -> dict[str, dict[str, Any]]:
    tokens: dict[str, dict[str, Any]] = {}

    def walk(node: Any, path: tuple[str, ...], inherited_type: str | None) -> None:
        if not isinstance(node, dict):
            return
        current_type = node.get("$type", inherited_type)
        if "$value" in node:
            require(path, "Token at document root is invalid")
            require(isinstance(current_type, str) and current_type, f"Token has no type: {'.'.join(path)}")
            name = ".".join(path)
            require(name not in tokens, f"Duplicate token path: {name}")
            tokens[name] = {
                "path": name,
                "type": current_type,
                "value": node["$value"],
                "description": node.get("$description"),
            }
            return
        for key, value in node.items():
            if key.startswith("$"):
                continue
            walk(value, path + (key,), current_type)

    walk(root, tuple(), None)
    require(tokens, "Design-token document contains no tokens")
    return tokens


def alias_target(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    match = ALIAS_RE.fullmatch(value.strip())
    return match.group(1) if match else None


def validate_dimension(value: Any, path: str) -> None:
    require(isinstance(value, dict), f"Dimension must be an object: {path}")
    require(set(value) == {"value", "unit"}, f"Dimension fields drift: {path}")
    number = value.get("value")
    unit = value.get("unit")
    require(isinstance(number, (int, float)) and not isinstance(number, bool), f"Dimension value is not numeric: {path}")
    require(math.isfinite(float(number)), f"Dimension value is not finite: {path}")
    require(unit in {"px", "rem"}, f"Unsupported R4a dimension unit for {path}: {unit!r}")


def validate_color(value: Any, path: str) -> None:
    require(isinstance(value, dict), f"Color must be an object: {path}")
    require(value.get("colorSpace") == "srgb", f"R4a color space must be sRGB: {path}")
    components = value.get("components")
    require(isinstance(components, list) and len(components) == 3, f"sRGB color requires 3 components: {path}")
    for component in components:
        require(isinstance(component, (int, float)) and not isinstance(component, bool), f"Color component is not numeric: {path}")
        require(0 <= float(component) <= 1, f"Color component outside 0..1: {path}")
    alpha = value.get("alpha", 1)
    require(isinstance(alpha, (int, float)) and not isinstance(alpha, bool) and 0 <= float(alpha) <= 1, f"Color alpha invalid: {path}")
    hex_value = value.get("hex")
    require(isinstance(hex_value, str) and HEX_RE.fullmatch(hex_value), f"Color hex invalid: {path}")
    raw = hex_value[1:]
    expected = [int(raw[index:index + 2], 16) / 255 for index in (0, 2, 4)]
    for actual, target in zip(components, expected):
        require(abs(float(actual) - target) <= 0.0000015, f"Color components/hex disagree: {path}")


def validate_shadow(value: Any, path: str) -> None:
    require(isinstance(value, dict), f"Shadow must be an object: {path}")
    require(set(value) == {"color", "offsetX", "offsetY", "blur", "spread"}, f"Shadow fields drift: {path}")
    validate_color(value["color"], f"{path}.color")
    for field in ("offsetX", "offsetY", "blur", "spread"):
        validate_dimension(value[field], f"{path}.{field}")


def validate_literal(value: Any, token_type: str, path: str) -> None:
    if token_type == "dimension":
        validate_dimension(value, path)
    elif token_type == "number":
        require(isinstance(value, (int, float)) and not isinstance(value, bool), f"Number token invalid: {path}")
        require(math.isfinite(float(value)), f"Number token is not finite: {path}")
    elif token_type == "fontFamily":
        if isinstance(value, str):
            require(bool(value), f"Font family token is empty: {path}")
        else:
            require(isinstance(value, list) and value and all(isinstance(item, str) and item for item in value), f"Font family token invalid: {path}")
    elif token_type == "color":
        validate_color(value, path)
    elif token_type == "shadow":
        if isinstance(value, list):
            require(value, f"Shadow token list is empty: {path}")
            for index, item in enumerate(value):
                validate_shadow(item, f"{path}[{index}]")
        else:
            validate_shadow(value, path)
    else:
        raise TokenContractError(f"Unsupported R4a token type {token_type!r}: {path}")


def resolve_token(tokens: dict[str, dict[str, Any]], path: str, stack: tuple[str, ...] = tuple()) -> tuple[str, Any]:
    require(path in tokens, f"Unknown token reference: {path}")
    require(path not in stack, f"Token alias cycle: {' -> '.join(stack + (path,))}")
    token = tokens[path]
    target = alias_target(token["value"])
    if target is None:
        validate_literal(token["value"], token["type"], path)
        return token["type"], token["value"]
    target_type, target_value = resolve_token(tokens, target, stack + (path,))
    require(target_type == token["type"], f"Alias type mismatch: {path} ({token['type']}) -> {target} ({target_type})")
    return target_type, target_value


def css_number(value: int | float) -> str:
    number = float(value)
    if number.is_integer():
        return str(int(number))
    return format(number, ".12g")


def css_value(tokens: dict[str, dict[str, Any]], path: str) -> str:
    token_type, value = resolve_token(tokens, path)
    if token_type == "dimension":
        return f"{css_number(value['value'])}{value['unit']}"
    if token_type == "number":
        return css_number(value)
    if token_type == "fontFamily":
        return ",".join(value) if isinstance(value, list) else value
    if token_type == "color":
        return str(value["hex"]).lower()
    raise TokenContractError(f"No CSS scalar representation for token type {token_type!r}: {path}")


def style_contents(html: str) -> list[str]:
    styles: list[str] = []
    cursor = 0
    while True:
        match = STYLE_OPEN_RE.search(html, cursor)
        if not match:
            break
        close = html.lower().find("</style>", match.end())
        require(close >= 0, "Unterminated style element while validating token bindings")
        styles.append(html[match.end():close])
        cursor = close + len("</style>")
    return styles


def selector_blocks(css: str, selector: str) -> list[str]:
    blocks: list[str] = []
    cursor = 0
    while True:
        start = css.find(selector, cursor)
        if start < 0:
            break
        before = css[start - 1] if start else ""
        after_index = start + len(selector)
        after = css[after_index] if after_index < len(css) else ""
        if before and before not in "}\n\r\t ,":
            cursor = after_index
            continue
        if after and after not in "{\n\r\t , ":
            cursor = after_index
            continue
        brace = after_index
        while brace < len(css) and css[brace].isspace():
            brace += 1
        if brace >= len(css) or css[brace] != "{":
            cursor = after_index
            continue
        depth = 1
        index = brace + 1
        while index < len(css) and depth:
            if css[index] == "{":
                depth += 1
            elif css[index] == "}":
                depth -= 1
            index += 1
        require(depth == 0, f"Unbalanced CSS braces after selector {selector!r}")
        blocks.append(css[brace + 1:index - 1])
        cursor = index
    return blocks


def custom_properties(html: str, selector: str) -> dict[str, str]:
    properties: dict[str, str] = {}
    for css in style_contents(html):
        for block in selector_blocks(css, selector):
            for name, value in CUSTOM_PROPERTY_RE.findall(block):
                properties[name] = value.strip().lower()
    return properties


def validate_theme_profiles(tokens: dict[str, dict[str, Any]], bindings: dict[str, Any], pages: dict[str, bytes]) -> dict[str, Any]:
    profiles = bindings.get("themeProfiles")
    require(isinstance(profiles, dict) and profiles, "Theme profiles missing")
    covered: list[str] = []
    checks = 0
    evidence: dict[str, Any] = {}
    for profile_name, profile in profiles.items():
        require(isinstance(profile, dict), f"Theme profile invalid: {profile_name}")
        slugs = profile.get("slugs")
        require(isinstance(slugs, list) and slugs, f"Theme profile has no slugs: {profile_name}")
        covered.extend(slugs)
        profile_evidence: dict[str, Any] = {}
        for slug in slugs:
            require(slug in pages, f"Theme profile references unknown page: {slug}")
            html = pages[slug].decode("utf-8")
            entry: dict[str, Any] = {}
            for mode in ("light", "dark"):
                selector = profile.get(f"{mode}Selector")
                mapping = profile.get(mode)
                require(isinstance(selector, str) and selector, f"Theme selector missing: {profile_name}.{mode}")
                require(isinstance(mapping, dict) and mapping, f"Theme token map missing: {profile_name}.{mode}")
                observed = custom_properties(html, selector)
                require(observed, f"Theme selector not found in {slug}: {selector}")
                mode_evidence: dict[str, Any] = {}
                for variable, token_path in mapping.items():
                    require(variable in observed, f"Theme variable {variable} missing in {slug} / {selector}")
                    expected = css_value(tokens, token_path)
                    actual = observed[variable]
                    require(actual == expected, f"Theme token mismatch {slug} {selector} {variable}: {actual} != {expected}")
                    mode_evidence[variable] = {"token": token_path, "value": actual}
                    checks += 1
                entry[mode] = {"selector": selector, "variables": mode_evidence}
            profile_evidence[slug] = entry
        evidence[profile_name] = profile_evidence
    require(len(covered) == len(set(covered)), "Theme profiles overlap in lab membership")
    require(set(covered) == set(pages), f"Theme profile lab coverage drift: missing={sorted(set(pages)-set(covered))}, extra={sorted(set(covered)-set(pages))}")
    return {"profiles": len(profiles), "slugs": len(covered), "checks": checks, "evidence": evidence, "pass": True}


def validate_accents(tokens: dict[str, dict[str, Any]], bindings: dict[str, Any], pages: dict[str, bytes]) -> dict[str, Any]:
    catalogue = {row["slug"]: row for row in load_json(CATALOGUE)}
    accent_bindings = bindings.get("accentBindings")
    require(isinstance(accent_bindings, dict), "Accent bindings missing")
    require(set(accent_bindings) == set(pages) == set(catalogue), "Accent binding membership drift")
    checks = 0
    evidence: dict[str, Any] = {}
    newer = {"transformer-language-model", "agent-tool-context", "minimax-alpha-beta"}
    for slug, paths in accent_bindings.items():
        require(isinstance(paths, dict), f"Accent binding invalid: {slug}")
        catalogue_value = css_value(tokens, paths["catalogue"])
        require(catalogue_value == str(catalogue[slug]["accent"]).lower(), f"Catalogue accent token drift: {slug}")
        html = pages[slug].decode("utf-8")
        root = custom_properties(html, ":root")
        require("--accent" in root, f"Page root accent missing: {slug}")
        light_value = css_value(tokens, paths["uiLight"])
        require(root["--accent"] == light_value, f"Light page accent token drift: {slug}: {root['--accent']} != {light_value}")
        entry: dict[str, Any] = {"catalogue": catalogue_value, "uiLight": light_value}
        if slug in newer:
            selector = f'body.ap-standard-dark[data-ap-modern-parity="{slug}"]'
            dark = custom_properties(html, selector)
            require("--accent" in dark and "--accent-strong" in dark, f"Dark accent overrides missing: {slug}")
            dark_value = css_value(tokens, paths["uiDark"])
            strong_value = css_value(tokens, paths["uiDarkStrong"])
            require(dark["--accent"] == dark_value, f"Dark page accent token drift: {slug}")
            require(dark["--accent-strong"] == strong_value, f"Dark strong accent token drift: {slug}")
            entry["uiDark"] = dark_value
            entry["uiDarkStrong"] = strong_value
            checks += 4
        else:
            dark_value = css_value(tokens, paths["uiDark"])
            require(dark_value == light_value, f"Legacy accent unexpectedly changes in dark mode token contract: {slug}")
            entry["uiDark"] = dark_value
            checks += 3
        evidence[slug] = entry
    require(evidence["minimax-alpha-beta"]["catalogue"] != evidence["minimax-alpha-beta"]["uiLight"], "Minimax frozen catalogue/page accent discrepancy was accidentally erased")
    return {"slugs": len(evidence), "checks": checks, "evidence": evidence, "minimaxMismatchPreserved": True, "pass": True}


def validate_component_literal_bindings(tokens: dict[str, dict[str, Any]], bindings: dict[str, Any]) -> dict[str, Any]:
    rows = bindings.get("componentLiteralBindings")
    require(isinstance(rows, list) and rows, "Component literal bindings missing")
    evidence: list[dict[str, Any]] = []
    for row in rows:
        require(isinstance(row, dict), "Component literal binding is not an object")
        resource = row.get("resource")
        token_path = row.get("token")
        needle = row.get("needle")
        expected_count = row.get("count")
        require(isinstance(resource, str) and resource, "Component binding resource missing")
        require(isinstance(token_path, str) and token_path, "Component binding token missing")
        require(isinstance(needle, str) and needle, "Component binding needle missing")
        require(isinstance(expected_count, int) and expected_count >= 1, "Component binding count invalid")
        path = ROOT / resource
        require(path.is_file(), f"Component binding resource missing: {resource}")
        text = path.read_text(encoding="utf-8")
        actual_count = text.count(needle)
        require(actual_count == expected_count, f"Component literal count drift {resource} / {needle}: {actual_count} != {expected_count}")
        css = css_value(tokens, token_path)
        require(css in needle, f"Component binding does not contain resolved token value: {token_path}={css!r} not in {needle!r}")
        evidence.append({"resource": resource, "token": token_path, "value": css, "needle": needle, "count": actual_count})
    return {"bindings": len(rows), "evidence": evidence, "pass": True}


def validate_contract() -> dict[str, Any]:
    document = load_json(TOKENS)
    bindings = load_json(BINDINGS)
    require(isinstance(document, dict), "Design-token document must be an object")
    require(document.get("$schema") == EXPECTED_SCHEMA, f"Design-token schema must be {EXPECTED_SCHEMA}")
    require(bindings.get("schema_version") == 1, "R4a binding schema version drift")
    require(bindings.get("phase") == "v1.9-r4a-design-token-contract", "R4a binding phase drift")
    require(bindings.get("token_file") == "src/design/ai-playgrounds.tokens.json", "R4a token-file ownership drift")
    require(bindings.get("format") == EXPECTED_FORMAT, "R4a token format drift")
    require(bindings.get("public_release_boundary") == "v1.8.1", "R4a release boundary drift")

    tokens = collect_tokens(document)
    aliases = 0
    type_counts: dict[str, int] = {}
    for path, token in tokens.items():
        if alias_target(token["value"]):
            aliases += 1
        resolve_token(tokens, path)
        type_counts[token["type"]] = type_counts.get(token["type"], 0) + 1
    require(set(type_counts) == {"dimension", "number", "fontFamily", "color", "shadow"}, f"R4a token type-family drift: {sorted(type_counts)}")

    page_state = page_components.load_and_validate()
    pages = page_state["reconstructed"]
    themes = validate_theme_profiles(tokens, bindings, pages)
    accents = validate_accents(tokens, bindings, pages)
    literals = validate_component_literal_bindings(tokens, bindings)

    required_paths = {
        "dimension.control.compact", "dimension.control.standard", "dimension.control.touch",
        "dimension.radius.control", "dimension.radius.panel", "dimension.focus.ringWidth",
        "dimension.layout.reading", "dimension.layout.learning", "dimension.layout.wide",
        "dimension.breakpoint.phoneLegacy", "dimension.breakpoint.phoneNewer",
        "dimension.breakpoint.shellCompact", "dimension.breakpoint.learningCompact",
        "color.theme.semantic.success", "color.theme.semantic.warning", "color.theme.semantic.error",
        "font.family.ui", "number.lineHeight.body", "number.fontWeight.action", "shadow.popover",
    }
    missing = sorted(required_paths - set(tokens))
    require(not missing, f"Required semantic token paths missing: {missing}")

    return {
        "schema": document["$schema"],
        "format": EXPECTED_FORMAT,
        "token_count": len(tokens),
        "alias_count": aliases,
        "type_counts": type_counts,
        "theme_profiles": themes,
        "accents": accents,
        "component_literal_bindings": literals,
        "page_graph": {
            "pages": len(page_state["slugs"]),
            "components": len(page_state["components"]),
            "deduplicated_bytes": page_state["metrics"]["deduplicated_bytes"],
        },
        "pass": True,
    }


if __name__ == "__main__":
    result = validate_contract()
    print(
        "R4a design tokens: PASS — "
        f"{result['token_count']} typed tokens / {result['alias_count']} aliases / "
        f"{result['theme_profiles']['checks']} theme bindings / "
        f"{result['component_literal_bindings']['bindings']} component literal bindings"
    )
