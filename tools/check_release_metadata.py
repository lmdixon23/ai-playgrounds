#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.0.0"
TAG = f"v{VERSION}"
RELEASE_DATE = "2026-07-25"
DISPLAY_DATE = "July 25, 2026"


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> int:
    codemeta = json.loads(read("codemeta.json"))
    cff = read("CITATION.cff")
    release_notes = read("RELEASE_NOTES.md")
    changelog = read("CHANGELOG.md")
    readme = read("README.md")
    release_html = read("release-notes.html")

    require(
        re.fullmatch(r"\d+\.\d+\.\d+", VERSION) is not None,
        f"Invalid configured semantic version: {VERSION}",
    )
    require(
        re.fullmatch(r"\d{4}-\d{2}-\d{2}", RELEASE_DATE) is not None,
        f"Invalid configured release date: {RELEASE_DATE}",
    )

    require(
        codemeta.get("softwareVersion") == VERSION,
        "codemeta.json softwareVersion does not match.",
    )
    require(
        codemeta.get("dateModified") == RELEASE_DATE,
        "codemeta.json dateModified does not match.",
    )
    require(
        f"version: {VERSION}" in cff,
        "CITATION.cff version does not match.",
    )
    require(
        f"date-released: {RELEASE_DATE}" in cff,
        "CITATION.cff date-released does not match.",
    )
    require(
        f"## {TAG}, {RELEASE_DATE}" in release_notes,
        "RELEASE_NOTES.md lacks the versioned release heading.",
    )
    require(
        f"## {VERSION} - {RELEASE_DATE}" in changelog,
        "CHANGELOG.md lacks the versioned entry.",
    )
    require(
        f"releases/tag/{TAG}" in readme,
        "README.md lacks the current-release link.",
    )
    require(
        f"AI Playgrounds {TAG}, released {DISPLAY_DATE}." in release_html,
        "release-notes.html lacks the visible version declaration.",
    )

    print(
        f"Release metadata: PASS "
        f"({TAG}, {RELEASE_DATE})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
