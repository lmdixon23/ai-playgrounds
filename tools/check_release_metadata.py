#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.2.0"
TAG = f"v{VERSION}"
RELEASE_DATE = "2026-08-24"


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def yaml_scalar(text: str, key: str, expected: str) -> bool:
    pattern = rf"(?m)^{re.escape(key)}:\s*['\"]?{re.escape(expected)}['\"]?\s*$"
    return re.search(pattern, text) is not None


def main() -> int:
    codemeta = json.loads(read("codemeta.json"))
    cff = read("CITATION.cff")
    release_notes = read("RELEASE_NOTES.md")
    changelog = read("CHANGELOG.md")
    readme = read("README.md")
    manifest = json.loads(read("applets.json"))

    require(re.fullmatch(r"\d+\.\d+\.\d+", VERSION) is not None, f"Invalid configured semantic version: {VERSION}")
    require(re.fullmatch(r"\d{4}-\d{2}-\d{2}", RELEASE_DATE) is not None, f"Invalid configured release date: {RELEASE_DATE}")
    require(codemeta.get("softwareVersion") == VERSION, "codemeta.json softwareVersion does not match.")
    require(codemeta.get("dateModified") == RELEASE_DATE, "codemeta.json dateModified does not match.")
    require(codemeta.get("datePublished") == RELEASE_DATE, "codemeta.json datePublished does not match.")
    require(yaml_scalar(cff, "version", VERSION), "CITATION.cff version does not match.")
    require(yaml_scalar(cff, "date-released", RELEASE_DATE), "CITATION.cff date-released does not match.")
    require("10.5281/zenodo.21854217" not in cff, "CITATION.cff must not attach the archived v1.0.1 DOI to v1.2.0.")
    require(f"## {TAG}, {RELEASE_DATE}" in release_notes, "RELEASE_NOTES.md lacks the versioned release heading.")
    require(re.search(rf"(?m)^## \[{re.escape(VERSION)}\] - {re.escape(RELEASE_DATE)}$|^## {re.escape(VERSION)} - {re.escape(RELEASE_DATE)}$", changelog) is not None, "CHANGELOG.md lacks the versioned entry.")
    require(f"releases/tag/{TAG}" in readme, "README.md lacks the current-release link.")
    require("Archived v1.0.1 DOI" in readme and "10.5281/zenodo.21854217" in readme, "README.md must preserve the archived v1.0.1 DOI boundary.")
    slugs = {entry.get("slug") for entry in manifest}
    require(len(manifest) == 13 and "transformer-language-model" in slugs, "applets.json must contain the thirteen-app v1.2 inventory.")
    print(f"Release metadata: PASS ({TAG}, {RELEASE_DATE}, {len(manifest)} applets)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
