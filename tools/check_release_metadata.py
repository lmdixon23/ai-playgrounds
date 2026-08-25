#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.6.1"
TAG = f"v{VERSION}"
RELEASE_DATE = "2026-08-26"
R6_BROWSER_FREEZE = "07f89d13269041d9ed66de2362bf84c288bb86de"
COVERAGE_MATRIX = ROOT / "docs" / "AI_CURRICULUM_COVERAGE_MATRIX_2026-08-25.md"
ENGAGEMENT_FAS = ROOT / "docs" / "ENGAGEMENT_EXCELLENCE_FAS.md"
ENGAGEMENT_AUDIT = ROOT / "docs" / "ENGAGEMENT_FIRST_MOVE_AUDIT.md"
LAB15_ENGAGEMENT_AUDIT = ROOT / "docs" / "LAB15_ENGAGEMENT_HCI_AUDIT.md"
USABILITY_PROTOCOL = ROOT / "docs" / "ENGAGEMENT_USABILITY_PROTOCOL.md"
HCI_RECOVERY = ROOT / "docs" / "HCI_STATE_RECOVERY_CONTRACT.md"
ANALYTICS_SPEC = ROOT / "docs" / "ANALYTICS_AND_PRIVACY.md"
DESIGN_SYSTEM = ROOT / "docs" / "APPLET_DESIGN_SYSTEM_CONTRACT.md"
LOCALE_MATRIX = ROOT / "docs" / "PUBLIC_SURFACE_LOCALE_MATRIX.md"
QUICK_ASSIGN_ARCH = ROOT / "docs" / "QUICK_ASSIGN_ARCHITECTURE.md"
RELEASE_161 = ROOT / "docs" / "RELEASE_V1_6_1.md"
QUICK_ASSIGN_REGISTRY = ROOT / "tools" / "quick_assigns_v1.json"


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
    readme = read("README.md")
    sitemap = read("sitemap.xml")
    public_builder = read("tools/build_agent_tool_context_public.py")
    legacy_manifest = json.loads(read("applets.json"))
    inherited_manifest = json.loads(read("tools/applets_v1_2.json"))
    lab14 = json.loads(read("tools/applet_v1_3_lab14.json"))
    lab15 = json.loads(read("tools/applet_v1_6_lab15.json"))
    composed = inherited_manifest + [lab14, lab15]

    require(re.fullmatch(r"\d+\.\d+\.\d+", VERSION) is not None, f"Invalid configured semantic version: {VERSION}")
    require(re.fullmatch(r"\d{4}-\d{2}-\d{2}", RELEASE_DATE) is not None, f"Invalid configured release date: {RELEASE_DATE}")
    require(codemeta.get("softwareVersion") == VERSION, "codemeta.json softwareVersion does not match")
    require(codemeta.get("dateModified") == RELEASE_DATE, "codemeta.json dateModified does not match")
    require(codemeta.get("datePublished") == RELEASE_DATE, "codemeta.json datePublished does not match")
    require(codemeta.get("identifier", "").endswith(f"/releases/tag/{TAG}"), "codemeta.json identifier does not match v1.6.1")
    require(yaml_scalar(cff, "version", VERSION), "CITATION.cff version does not match")
    require(yaml_scalar(cff, "date-released", RELEASE_DATE), "CITATION.cff date-released does not match")
    require("10.5281/zenodo.21854217" not in cff, "CITATION.cff must not attach the archived v1.0.1 DOI to v1.6.1")
    require(f"releases/tag/{TAG}" in readme, "README.md lacks the v1.6.1 current-release link")
    require("AI Playgrounds v1.6.1 is the current software release" in readme, "README.md does not identify v1.6.1 as current")
    require("Archived v1.0.1 DOI" in readme and "10.5281/zenodo.21854217" in readme, "README.md must preserve the archived v1.0.1 DOI boundary")
    require(RELEASE_161.is_file() and "# AI Playgrounds v1.6.1" in RELEASE_161.read_text(encoding="utf-8"), "v1.6.1 dedicated release notes are missing")

    require(len(legacy_manifest) == 12, "Legacy source manifest must remain bound to the twelve inherited source applets")
    require(len(inherited_manifest) == 13 and inherited_manifest[-1].get("slug") == "transformer-language-model", "tools/applets_v1_2.json must remain the thirteen-app v1.2 inventory")
    slugs = [entry.get("slug") for entry in composed]
    require(len(composed) == 15 and len(set(slugs)) == 15 and slugs[-2:] == ["agent-tool-context", "minimax-alpha-beta"], "v1.6.1 composition must preserve fifteen unique applets with Labs 14 and 15 appended")
    require(lab14.get("course_order") == 14 and lab14.get("showcase_order") == 14, "Lab 14 release metadata order is incorrect")
    require(lab15.get("course_order") == 15 and lab15.get("showcase_order") == 15, "Lab 15 release metadata order is incorrect")
    require(lab15.get("course_phase") == "foundations", "Lab 15 must retain the Foundations/course-track release token")
    require("playgrounds/agent-tool-context/index.html" in sitemap, "sitemap.xml lacks the Lab 14 route")
    require("playgrounds/minimax-alpha-beta/" in sitemap, "sitemap.xml lacks the Lab 15 route")
    require(R6_BROWSER_FREEZE in public_builder, "Public Lab 14 builder is not bound to the frozen R6 head")

    # Historical release compositions remain independently reproducible. v1.6.1
    # composes a consistency/adoption layer over v1.6 rather than mutating old builders.
    for relative, label in (
        ("tools/build_site_v1_4.py", "v1.4 Pages builder"),
        ("tools/test_v1_4_public_integration.py", "v1.4 public integration gate"),
        ("tools/build_site_v1_5.py", "v1.5 Pages builder"),
        ("tools/test_v1_5_public_integration.py", "v1.5 public integration gate"),
        ("tools/build_site_v1_5_1.py", "v1.5.1 Pages builder"),
        ("tools/test_v1_5_1_hci_adoption.py", "v1.5.1 HCI/adoption gate"),
        ("tools/build_site_v1_6_public.py", "v1.6 Pages builder"),
        ("tools/test_v1_6_public_release.py", "v1.6 public integration/HCI gate"),
        ("tools/build_site_v1_6_1_candidate.py", "v1.6.1 Quick Assign builder"),
        ("tools/build_site_v1_6_1_public.py", "v1.6.1 classroom/support builder"),
        ("tools/build_site_v1_6_1_consistency.py", "v1.6.1 final Pages builder"),
        ("tools/test_v1_6_1_quick_assign_currency.py", "v1.6.1 Quick Assign/currency gate"),
        ("tools/test_v1_6_1_design_consistency.py", "v1.6.1 final-composition/design-system gate"),
    ):
        require((ROOT / relative).is_file(), f"{label} is missing")

    for path, label in (
        (ROOT / "tools" / "test_transformer_engagement_candidate.py", "Lab 13 engagement gate"),
        (ROOT / "tools" / "test_agent_tool_context_engagement_candidate.py", "Lab 14 engagement gate"),
        (ROOT / "tools" / "test_cnf_sat_engagement_candidate.py", "CNF/SAT engagement gate"),
        (ROOT / "tools" / "test_bayes_network_engagement_candidate.py", "Bayesian engagement gate"),
        (ROOT / "tools" / "test_minimax_alpha_beta.py", "Lab 15 reference/census gate"),
        (ROOT / "tools" / "test_minimax_alpha_beta_cross_runtime.py", "Lab 15 cross-runtime gate"),
        (ROOT / "tools" / "test_minimax_alpha_beta_multilingual_applet.py", "Lab 15 four-locale gate"),
    ):
        require(path.is_file(), f"{label} is missing")

    for path, label in (
        (ROOT / "docs" / "V1_4_PRODUCT_QUALITY_ARCHITECTURE.md", "v1.4 product-quality architecture"),
        (COVERAGE_MATRIX, "curriculum coverage matrix"),
        (ENGAGEMENT_FAS, "Engagement Full Assurance Stack"),
        (ENGAGEMENT_AUDIT, "Engagement applet acceptance audit"),
        (LAB15_ENGAGEMENT_AUDIT, "Lab 15 engagement/HCI audit"),
        (USABILITY_PROTOCOL, "Human engagement/usability protocol"),
        (HCI_RECOVERY, "Learner-centered HCI state/recovery contract"),
        (ANALYTICS_SPEC, "Analytics/privacy specification"),
        (DESIGN_SYSTEM, "Applet design-system contract"),
        (LOCALE_MATRIX, "Public-surface locale matrix"),
        (QUICK_ASSIGN_ARCH, "Quick Assign architecture"),
    ):
        require(path.is_file(), f"{label} is missing")

    require("ten" in ENGAGEMENT_AUDIT.read_text(encoding="utf-8").lower() and "no change" in ENGAGEMENT_AUDIT.read_text(encoding="utf-8").lower(), "Engagement audit must preserve the explicit no-forced-change decision")
    require("ADOPT current Lab 15 behavior" in LAB15_ENGAGEMENT_AUDIT.read_text(encoding="utf-8"), "Lab 15 engagement/HCI audit does not contain its adopt ruling")
    require("**Release:** v1.6.1" in ANALYTICS_SPEC.read_text(encoding="utf-8"), "Analytics/privacy specification is not rebound to v1.6.1")

    quick = json.loads(QUICK_ASSIGN_REGISTRY.read_text(encoding="utf-8"))["activities"]
    require(len(quick) == 15 and len({row["id"] for row in quick}) == 15, "Quick Assign registry must reserve exactly one unique ID for every applet")
    require([row["id"] for row in quick if row.get("status") == "active"] == ["QA-SEARCH-01", "QA-LOCAL-01", "QA-WUMPUS-01", "QA-SAT-01"], "v1.6.1 release must preserve the four active Quick Assign canaries")

    activities = ROOT / "activities"
    require((activities / "index.html").is_file(), "Activity Pack index source is missing")
    require((activities / "nn-1.html").is_file(), "NN-1 Activity Pack source is missing")
    require((activities / "cnn-1.html").is_file(), "CNN-1 Activity Pack source is missing")
    require("TEACHER_PRIVATE" not in read("activities/nn-1.html") and "Expected answers" not in read("activities/nn-1.html"), "NN-1 public activity must not contain a teacher answer key")
    require("TEACHER_PRIVATE" not in read("activities/cnn-1.html") and "Expected answers" not in read("activities/cnn-1.html"), "CNN-1 public activity must not contain a teacher answer key")

    print(f"Release metadata: PASS ({TAG}, {RELEASE_DATE}, {len(composed)} public applets + 4 Quick Assign canaries + 2 Activity Pack canaries)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
