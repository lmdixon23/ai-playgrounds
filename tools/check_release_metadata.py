#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.5.0"
TAG = f"v{VERSION}"
RELEASE_DATE = "2026-08-25"
R6_BROWSER_FREEZE = "07f89d13269041d9ed66de2362bf84c288bb86de"
COVERAGE_MATRIX = ROOT / "docs" / "AI_CURRICULUM_COVERAGE_MATRIX_2026-08-25.md"
ENGAGEMENT_FAS = ROOT / "docs" / "ENGAGEMENT_EXCELLENCE_FAS.md"
ENGAGEMENT_AUDIT = ROOT / "docs" / "ENGAGEMENT_FIRST_MOVE_AUDIT.md"
USABILITY_PROTOCOL = ROOT / "docs" / "ENGAGEMENT_USABILITY_PROTOCOL.md"


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
    sitemap = read("sitemap.xml")
    public_builder = read("tools/build_agent_tool_context_public.py")
    legacy_manifest = json.loads(read("applets.json"))
    inherited_manifest = json.loads(read("tools/applets_v1_2.json"))
    lab14 = json.loads(read("tools/applet_v1_3_lab14.json"))
    composed = inherited_manifest + [lab14]

    require(re.fullmatch(r"\d+\.\d+\.\d+", VERSION) is not None, f"Invalid configured semantic version: {VERSION}")
    require(re.fullmatch(r"\d{4}-\d{2}-\d{2}", RELEASE_DATE) is not None, f"Invalid configured release date: {RELEASE_DATE}")
    require(codemeta.get("softwareVersion") == VERSION, "codemeta.json softwareVersion does not match")
    require(codemeta.get("dateModified") == RELEASE_DATE, "codemeta.json dateModified does not match")
    require(codemeta.get("datePublished") == RELEASE_DATE, "codemeta.json datePublished does not match")
    require(codemeta.get("identifier", "").endswith(f"/releases/tag/{TAG}"), "codemeta.json identifier does not match v1.5.0")
    require(yaml_scalar(cff, "version", VERSION), "CITATION.cff version does not match")
    require(yaml_scalar(cff, "date-released", RELEASE_DATE), "CITATION.cff date-released does not match")
    require("10.5281/zenodo.21854217" not in cff, "CITATION.cff must not attach the archived v1.0.1 DOI to v1.5.0")
    require(f"## {TAG}, {RELEASE_DATE}" in release_notes, "RELEASE_NOTES.md lacks the v1.5.0 release heading")
    require(re.search(rf"(?m)^## \[{re.escape(VERSION)}\] - {re.escape(RELEASE_DATE)}$|^## {re.escape(VERSION)} - {re.escape(RELEASE_DATE)}$", changelog) is not None, "CHANGELOG.md lacks the v1.5.0 entry")
    require(f"releases/tag/{TAG}" in readme, "README.md lacks the v1.5.0 current-release link")
    require("Archived v1.0.1 DOI" in readme and "10.5281/zenodo.21854217" in readme, "README.md must preserve the archived v1.0.1 DOI boundary")
    require(len(legacy_manifest) == 12, "Legacy source manifest must remain bound to the twelve inherited source applets")
    require(len(inherited_manifest) == 13 and inherited_manifest[-1].get("slug") == "transformer-language-model", "tools/applets_v1_2.json must remain the thirteen-app v1.2 inventory")
    slugs = [entry.get("slug") for entry in composed]
    require(len(composed) == 14 and len(set(slugs)) == 14 and slugs[-1] == "agent-tool-context", "v1.5 composition must preserve fourteen unique applets with Lab 14 appended")
    require(lab14.get("course_order") == 14 and lab14.get("showcase_order") == 14, "Lab 14 release metadata order is incorrect")
    require("playgrounds/agent-tool-context/index.html" in sitemap, "sitemap.xml lacks the Lab 14 route")
    require(R6_BROWSER_FREEZE in public_builder, "Public Lab 14 builder is not bound to the frozen R6 head")

    # Preserve v1.4 as an inherited, reproducible historical composition and add
    # a separately bounded v1.5 engagement composition rather than mutating it.
    require((ROOT / "tools" / "build_site_v1_4.py").is_file(), "v1.4 Pages builder is missing")
    require((ROOT / "tools" / "test_v1_4_public_integration.py").is_file(), "v1.4 public integration gate is missing")
    require((ROOT / "tools" / "build_site_v1_5.py").is_file(), "v1.5 Pages builder is missing")
    require((ROOT / "tools" / "test_v1_5_public_integration.py").is_file(), "v1.5 public integration gate is missing")

    for path, label in (
        (ROOT / "tools" / "test_transformer_engagement_candidate.py", "Lab 13 engagement gate"),
        (ROOT / "tools" / "test_agent_tool_context_engagement_candidate.py", "Lab 14 engagement gate"),
        (ROOT / "tools" / "test_cnf_sat_engagement_candidate.py", "CNF/SAT engagement gate"),
        (ROOT / "tools" / "test_bayes_network_engagement_candidate.py", "Bayesian engagement gate"),
    ):
        require(path.is_file(), f"{label} is missing")

    require((ROOT / "docs" / "V1_4_PRODUCT_QUALITY_ARCHITECTURE.md").is_file(), "v1.4 product-quality architecture is missing")
    require(COVERAGE_MATRIX.is_file(), f"curriculum coverage matrix is missing: {COVERAGE_MATRIX.relative_to(ROOT)}")
    require(ENGAGEMENT_FAS.is_file(), "Engagement Full Assurance Stack is missing")
    require(ENGAGEMENT_AUDIT.is_file(), "Engagement applet acceptance audit is missing")
    require(USABILITY_PROTOCOL.is_file(), "Human engagement/usability protocol is missing")
    require("ten" in ENGAGEMENT_AUDIT.read_text(encoding="utf-8").lower() and "no change" in ENGAGEMENT_AUDIT.read_text(encoding="utf-8").lower(), "Engagement audit must preserve the explicit no-forced-change decision")

    print(f"Release metadata: PASS ({TAG}, {RELEASE_DATE}, {len(composed)} public applets)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())