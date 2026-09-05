#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "tools" / "design_tokens.py"

PREFIX = '''#!/usr/bin/env python3
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
CUSTOM_PROPERTY_RE = re.compile(r"(--[A-Za-z0-9_-]+)\\s*:\\s*([^;{}]+)")
STYLE_OPEN_RE = re.compile(r"<style\\b[^>]*>", re.IGNORECASE)


'''


def main() -> int:
    text = PATH.read_text(encoding="utf-8")
    marker = "def style_contents(html: str) -> list[str]:\n"
    if marker not in text:
        raise RuntimeError("design_tokens style_contents boundary missing")
    suffix = text[text.index(marker):]
    PATH.write_text(PREFIX + suffix, encoding="utf-8")
    print("Refactored design_tokens.py to consume token_values.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
