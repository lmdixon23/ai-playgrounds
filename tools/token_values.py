#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TOKENS = ROOT / "src" / "design" / "ai-playgrounds.tokens.json"
EXPECTED_SCHEMA = "https://www.designtokens.org/schemas/2025.10/format.json"
EXPECTED_FORMAT = "DTCG 2025.10"
ALIAS_RE = re.compile(r"^\{([A-Za-z0-9_.-]+)\}$")
HEX_RE = re.compile(r"^#[0-9a-fA-F]{6}$")


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
    require(unit in {"px", "rem"}, f"Unsupported design-token dimension unit for {path}: {unit!r}")


def validate_color(value: Any, path: str) -> None:
    require(isinstance(value, dict), f"Color must be an object: {path}")
    require(value.get("colorSpace") == "srgb", f"Design-token color space must be sRGB: {path}")
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
        raise TokenContractError(f"Unsupported design-token type {token_type!r}: {path}")


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


def normalize_css_atom(value: str) -> str:
    normalized = value.strip().lower()
    match = re.fullmatch(r"#([0-9a-f]{3})", normalized)
    if match:
        digits = match.group(1)
        return "#" + "".join(char * 2 for char in digits)
    return normalized


def load_validated_tokens() -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    document = load_json(TOKENS)
    require(isinstance(document, dict), "Design-token document must be an object")
    require(document.get("$schema") == EXPECTED_SCHEMA, f"Design-token schema must be {EXPECTED_SCHEMA}")
    tokens = collect_tokens(document)
    for path in tokens:
        resolve_token(tokens, path)
    return document, tokens
