#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.8.1"
TAG = f"v{VERSION}"
RELEASE_DATE = "2026-08-27"
R6_BROWSER_FREEZE = "07f89d13269041d9ed66de2362bf84c288bb86de"
ANALYTICS_SPEC = ROOT / "docs" / "ANALYTICS_AND_PRIVACY.md"
DESIGN_SYSTEM = ROOT / "docs" / "APPLET_DESIGN_SYSTEM_CONTRACT.md"
LOCALE_MATRIX = ROOT / "docs" / "PUBLIC_SURFACE_LOCALE_MATRIX.md"
QUICK_ASSIGN_ARCH = ROOT / "docs" / "QUICK_ASSIGN_ARCHITECTURE.md"
RELEASE_170 = ROOT / "docs" / "RELEASE_V1_7_0.md"
RELEASE_171 = ROOT / "docs" / "RELEASE_V1_7_1.md"
RELEASE_172 = ROOT / "docs" / "RELEASE_V1_7_2.md"
RELEASE_180 = ROOT / "docs" / "RELEASE_V1_8_0.md"
RELEASE_181 = ROOT / "docs" / "RELEASE_V1_8_1.md"
QUICK_V1 = ROOT / "tools" / "quick_assigns_v1.json"
QUICK_V2 = ROOT / "tools" / "quick_assigns_v2.json"


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def yaml_scalar(text: str, key: str, expected: str) -> bool:
    return re.search(rf"(?m)^{re.escape(key)}:\s*['\"]?{re.escape(expected)}['\"]?\s*$", text) is not None


def main() -> int:
    codemeta = json.loads(read("codemeta.json"))
    cff = read("CITATION.cff")
    readme = read("README.md")
    sitemap = read("sitemap.xml")
    public_builder = read("tools/build_agent_tool_context_public.py")
    legacy_manifest = json.loads(read("applets.json"))
    inherited_manifest = json.loads(read("tools/applets_v1_2.json"))
    lab14 = json.loads(read("tools/applet_v1_3_lab14.json"))
    lab15 = json.loads(read("tools/applet_v1_6_lab15.json"))
    composed = inherited_manifest + [lab14, lab15]

    require(re.fullmatch(r"\d+\.\d+\.\d+", VERSION) is not None, f"Invalid semantic version: {VERSION}")
    require(codemeta.get("softwareVersion") == VERSION, "CodeMeta version mismatch")
    require(codemeta.get("dateModified") == RELEASE_DATE and codemeta.get("datePublished") == RELEASE_DATE, "CodeMeta date mismatch")
    require(codemeta.get("identifier", "").endswith(f"/releases/tag/{TAG}"), "CodeMeta release identifier mismatch")
    require(yaml_scalar(cff, "version", VERSION) and yaml_scalar(cff, "date-released", RELEASE_DATE), "CITATION.cff version/date mismatch")
    require("10.5281/zenodo.21854217" not in cff, f"Archived v1.0.1 DOI must not be attached to {TAG}")
    require(f"releases/tag/{TAG}" in readme and "AI Playgrounds v1.8.1 is the current software release" in readme, "README current-release boundary mismatch")
    require("Archived v1.0.1 DOI" in readme and "10.5281/zenodo.21854217" in readme, "README historical DOI boundary missing")
    require(RELEASE_170.is_file() and "# AI Playgrounds v1.7.0" in RELEASE_170.read_text(encoding="utf-8"), "historical v1.7.0 release notes missing")
    require(RELEASE_171.is_file() and "# AI Playgrounds v1.7.1" in RELEASE_171.read_text(encoding="utf-8"), "v1.7.1 release notes missing")
    require(RELEASE_172.is_file() and "# AI Playgrounds v1.7.2" in RELEASE_172.read_text(encoding="utf-8"), "v1.7.2 release notes missing")
    require(RELEASE_180.is_file() and "# AI Playgrounds v1.8.0" in RELEASE_180.read_text(encoding="utf-8"), "v1.8.0 release notes missing")
    require(RELEASE_181.is_file() and "# AI Playgrounds v1.8.1" in RELEASE_181.read_text(encoding="utf-8"), "v1.8.1 release notes missing")

    for index_name in ("CHANGELOG.md", "RELEASE_NOTES.md"):
        release_index = read(index_name)
        for version in ("1.6.1", "1.6.2", "1.7.0", "1.7.1", "1.7.2", "1.8.0", "1.8.1"):
            target = f"docs/RELEASE_V{version.replace('.', '_')}.md"
            require(target in release_index, f"{index_name} missing dedicated-note link for v{version}")

    require(len(legacy_manifest) == 12, "Legacy twelve-app source manifest changed")
    require(len(inherited_manifest) == 13 and inherited_manifest[-1].get("slug") == "transformer-language-model", "v1.2 inventory changed")
    slugs = [x.get("slug") for x in composed]
    require(len(composed) == 15 and len(set(slugs)) == 15 and slugs[-2:] == ["agent-tool-context", "minimax-alpha-beta"], "Current fifteen-app composition changed")
    require(lab14.get("course_order") == 14 and lab15.get("course_order") == 15 and lab15.get("course_phase") == "foundations", "Lab 14/15 ordering or phase changed")
    require("playgrounds/agent-tool-context/index.html" in sitemap and "playgrounds/minimax-alpha-beta/" in sitemap, "Sitemap current routes missing")
    require(R6_BROWSER_FREEZE in public_builder, "Lab 14 public builder freeze changed")

    required_files = (
        "tools/build_site_v1_4.py", "tools/build_site_v1_5.py", "tools/build_site_v1_5_1.py", "tools/build_site_v1_6_public.py",
        "tools/build_site_v1_6_1_consistency.py", "tools/build_site_v1_6_2.py", "tools/build_site_v1_7_quick_assigns.py",
        "tools/build_site_v1_7_final.py", "tools/build_site_v1_7.py", "tools/build_site_v1_7_1.py",
        "tools/build_site_v1_7_2.py", "tools/build_site_v1_7_2_modern_parity.py",
        "tools/build_site_v1_7_2_modern_parity_final.py", "tools/build_site_v1_7_2_modern_parity_complete.py",
        "tools/build_site_v1_7_2_modern_parity_accessible.py", "tools/modern_parity_v1.json",
        "tools/test_v1_6_1_quick_assign_currency.py", "tools/test_v1_6_1_design_consistency.py", "tools/test_v1_6_2_public_provenance.py",
        "tools/test_v1_7_all_quick_assigns.py", "tools/test_v1_7_public_release.py", "tools/test_v1_7_1_modern_shell.py",
        "tools/test_v1_7_1_public_release.py", "tools/test_minimax_alpha_beta.py", "tools/test_transformer_language_model.py",
        "tools/test_agent_tool_context.py", "tools/test_v1_7_2_modern_parity.py", "tools/test_v1_7_2_public_release.py",
        "tools/build_site_v1_8.py", "tools/test_v1_8_public_release.py", "tools/test_v1_8_algorithm_modes.py",
        "tools/test_v1_8_algorithm_modes_browser.py", "tools/build_site_v1_8_1.py",
        "tools/modern_learning_v1_8_1.py", "tools/test_v1_8_1_modern_learner_parity.py",
        "tools/test_v1_8_1_modern_learner_parity_browser.py", "tools/check_portfolio_freshness.py",
        "tools/test_portfolio_freshness.py", ".github/workflows/portfolio-freshness.yml",
        "docs/APPLET_DESIGN_SYSTEM_V1_7_2_ADDENDUM.md", "docs/APPLET_DESIGN_SYSTEM_V1_8_1_ADDENDUM.md",
        "docs/MODERN_LAB_PARITY_AUDIT.md",
        ".github/workflows/publish-v1.7.2.yml", ".github/workflows/publish-v1.8.0.yml",
        ".github/workflows/publish-v1.8.1.yml",
    )
    for relative in required_files:
        require((ROOT / relative).is_file(), f"Required release artifact missing: {relative}")
    require(not (ROOT / ".github/workflows/publish-v1.7.1.yml").exists(), "Obsolete v1.7.1 publisher was not retired")
    deploy_workflow = read(".github/workflows/deploy-pages.yml")
    publisher_workflow = read(".github/workflows/publish-v1.8.1.yml")
    require('workflows: ["Verify"]' in deploy_workflow and "build_site_v1_8_1.py" in deploy_workflow, "Pages deployment is not chained to Verify and v1.8.1 composition")
    require(
        "TAG: v1.8.1" in publisher_workflow
        and "test_v1_8_1_modern_learner_parity.py" in publisher_workflow
        and "check_portfolio_freshness.py" in publisher_workflow,
        "v1.8.1 publisher boundary is incomplete",
    )
    release_probe = publisher_workflow.find('if gh release view "$TAG"')
    unpublished_tag_probe = publisher_workflow.find('elif git ls-remote --exit-code --tags origin')
    require(
        0 <= release_probe < unpublished_tag_probe
        and "--json targetCommitish" in publisher_workflow,
        "v1.8.1 publisher must short-circuit an existing release before comparing an unpublished tag to current main",
    )

    for path in (ANALYTICS_SPEC, DESIGN_SYSTEM, LOCALE_MATRIX, QUICK_ASSIGN_ARCH):
        require(path.is_file(), f"Required documentation missing: {path.name}")
    require("**Release:** v1.8.1" in ANALYTICS_SPEC.read_text(encoding="utf-8"), "Analytics specification is not rebound to v1.8.1")
    require("**Status:** active v1.8.1 contract" in DESIGN_SYSTEM.read_text(encoding="utf-8"), "Design-system contract is not rebound to v1.8.1")

    v1 = json.loads(QUICK_V1.read_text(encoding="utf-8"))["activities"]
    v2 = json.loads(QUICK_V2.read_text(encoding="utf-8"))["activities"]
    require(len(v1) == 15 and len({r["id"] for r in v1}) == 15, "Historical v1 Quick Assign registry changed shape")
    require([r["id"] for r in v1 if r.get("status") == "active"] == ["QA-SEARCH-01", "QA-LOCAL-01", "QA-WUMPUS-01", "QA-SAT-01"], "Historical v1 Quick Assign active set changed")
    require(len(v2) == 15 and len({r["id"] for r in v2}) == 15, "v2 Quick Assign registry must have 15 unique IDs")
    require(all(r.get("status") == "active" for r in v2), "v1.8.1 requires all 15 Quick Assigns active")
    require(all(r.get("locales") == ["en", "zh", "vi", "es"] for r in v2), "v1.8.1 Quick Assign locale contract changed")

    for relative in ("activities/index.html", "activities/nn-1.html", "activities/cnn-1.html"):
        require((ROOT / relative).is_file(), f"Activity Pack source missing: {relative}")
    require("TEACHER_PRIVATE" not in read("activities/nn-1.html") and "Expected answers" not in read("activities/nn-1.html"), "NN-1 public answer key leak")
    require("TEACHER_PRIVATE" not in read("activities/cnn-1.html") and "Expected answers" not in read("activities/cnn-1.html"), "CNN-1 public answer key leak")

    print(f"Release metadata: PASS ({TAG}, {RELEASE_DATE}, {len(composed)} applets + 15 active Quick Assigns + 2 Activity Pack canaries)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
