#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import page_components
import token_values
from token_values import (
    ALIAS_RE,
    EXPECTED_FORMAT,
    EXPECTED_SCHEMA,
    HEX_RE,
    TOKENS,
    TokenContractError,
    alias_target,
    collect_tokens,
    css_number,
    css_value,
    load_json,
    normalize_css_atom,
    require,
    resolve_token,
    validate_color,
    validate_dimension,
    validate_literal,
    validate_shadow,
)

ROOT = token_values.ROOT
BINDINGS = ROOT / "src" / "design" / "current-bindings.json"
CATALOGUE = ROOT / "src" / "product" / "catalogue.json"
CUSTOM_PROPERTY_RE = re.compile(r"(--[A-Za-z0-9_-]+)\s*:\s*([^;{}]+)")
STYLE_OPEN_RE = re.compile(r"<style\b[^>]*>", re.IGNORECASE)


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
                    require(normalize_css_atom(actual) == normalize_css_atom(expected), f"Theme token mismatch {slug} {selector} {variable}: {actual} != {expected}")
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
        require(normalize_css_atom(root["--accent"]) == normalize_css_atom(light_value), f"Light page accent token drift: {slug}: {root['--accent']} != {light_value}")
        entry: dict[str, Any] = {"catalogue": catalogue_value, "uiLight": light_value}
        if slug in newer:
            selector = f'body.ap-standard-dark[data-ap-modern-parity="{slug}"]'
            dark = custom_properties(html, selector)
            require("--accent" in dark and "--accent-strong" in dark, f"Dark accent overrides missing: {slug}")
            dark_value = css_value(tokens, paths["uiDark"])
            strong_value = css_value(tokens, paths["uiDarkStrong"])
            require(normalize_css_atom(dark["--accent"]) == normalize_css_atom(dark_value), f"Dark page accent token drift: {slug}")
            require(normalize_css_atom(dark["--accent-strong"]) == normalize_css_atom(strong_value), f"Dark strong accent token drift: {slug}")
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
