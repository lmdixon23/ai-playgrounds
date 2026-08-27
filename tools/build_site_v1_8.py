#!/usr/bin/env python3
from __future__ import annotations

"""Compose the deterministic v1.8.0 algorithm-modes release.

v1.7.2 remains the immutable public baseline. This successor layer advances
only the release identity and the three source applets changed for issues
#2, #3, and #4; the inherited builder already copies those current sources and
then applies every prior shell, localization, Quick Assign, and accessibility
contract.
"""

import json
import re
import shutil

import build_site as core
import build_site_v1_7_2 as base

ROOT = base.SITE.parent
SITE = base.SITE
CURRENT = "v1.8.0"
VERSION = "1.8.0"
FEATURES = {
    "hill-climbing": ("restartBenchmark", "__hillBenchmarkTest", "benchAlgos"),
    "knn-classifier": ("taskMode", "aggregateRegressionTargets", "__knnModeTest"),
    "cnf-sat": ("solverMode", "cdclTrace", "__cdclModeTest"),
}


def patch_release_identity() -> None:
    for path in sorted(SITE.rglob("*.html")):
        page = path.read_text(encoding="utf-8")
        if path.name != "release-notes.html":
            page = page.replace("v1.7.2", CURRENT)
            page = page.replace('content="1.7.2"', 'content="1.8.0"')
        page = re.sub(
            r'data-ai-playgrounds-analytics="v\d+\.\d+\.\d+"',
            'data-ai-playgrounds-analytics="v1.8.0"',
            page,
        )
        page = re.sub(
            r'(<p data-v14-support-version="true">AI Playgrounds · )v\d+\.\d+\.\d+(</p>)',
            rf"\g<1>{CURRENT}\g<2>",
            page,
        )
        path.write_text(page, encoding="utf-8")

    notes_path = SITE / "release-notes.html"
    notes = notes_path.read_text(encoding="utf-8")
    anchor = '<section id="release-v1-7-2"'
    if anchor not in notes:
        raise RuntimeError("Release-notes v1.7.2 anchor changed")
    if 'id="release-v1-8-0"' not in notes:
        section = (
            '<section id="release-v1-8-0" style="margin:1rem 0;padding:1rem 1.2rem;'
            'border:1px solid currentColor;border-radius:12px">'
            '<h2>AI Playgrounds v1.8.0: algorithm modes and reproducible comparison.</h2>'
            '<p>Hill climbing adds seeded repeated-restart benchmarking, K-nearest '
            'neighbors adds continuous-target regression, and CNF/SAT adds a bounded '
            'first-UIP CDCL learning trace. Existing single-run, classification, and '
            'DPLL behavior remains available, with EN/ZH/VI/ES state-preserving controls '
            'and deterministic mechanism tests.</p></section>'
        )
        notes = notes.replace(anchor, section + anchor, 1)
    notes_path.write_text(notes, encoding="utf-8")

    # Keep this historical composition reproducible after repository-level
    # citation metadata advances to a successor release.
    shutil.copy2(ROOT / "codemeta.json", SITE / "codemeta.json")
    codemeta_path = SITE / "codemeta.json"
    codemeta = json.loads(codemeta_path.read_text(encoding="utf-8"))
    codemeta["softwareVersion"] = VERSION
    codemeta["identifier"] = "https://github.com/lmdixon23/ai-playgrounds/releases/tag/v1.8.0"
    codemeta["description"] = (
        "Fifteen multilingual, offline-ready interactive AI labs spanning thirteen "
        "Foundations/course-track mechanisms and two Modern AI extensions. v1.8.0 "
        "adds seeded repeated-restart benchmarking to Hill Climbing, continuous-target "
        "regression to K-Nearest Neighbors, and a bounded first-UIP CDCL trace to "
        "CNF/SAT while preserving all fifteen applets, assignments, languages, privacy "
        "boundaries, and the original modes."
    )
    codemeta_path.write_text(json.dumps(codemeta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    shutil.copy2(ROOT / "CITATION.cff", SITE / "CITATION.cff")
    citation_path = SITE / "CITATION.cff"
    citation = citation_path.read_text(encoding="utf-8")
    citation = re.sub(r"(?m)^version:\s*.*$", "version: '1.8.0'", citation, count=1)
    citation = re.sub(
        r"(?m)^abstract:\s*.*$",
        "abstract: Fifteen multilingual, offline-ready interactive AI labs spanning "
        "thirteen Foundations/course-track mechanisms and two Modern AI extensions. "
        "v1.8.0 adds seeded repeated-restart benchmarking to Hill Climbing, "
        "continuous-target regression to K-Nearest Neighbors, and a bounded first-UIP "
        "CDCL trace to CNF/SAT while preserving all fifteen applets, assignments, "
        "languages, privacy boundaries, and the original modes.",
        citation,
        count=1,
    )
    citation_path.write_text(citation, encoding="utf-8")


def validate() -> None:
    files = sorted(path for path in SITE.rglob("*") if path.is_file())
    applets = sorted((SITE / "playgrounds").glob("*/index.html"))
    if len(files) != 58 or len(applets) != 15:
        raise RuntimeError(f"v1.8.0 boundary drift: {len(files)} files / {len(applets)} applets")
    for path in sorted(SITE.rglob("*.html")):
        page = path.read_text(encoding="utf-8")
        if page.count('data-ai-playgrounds-analytics="v1.8.0"') != 1:
            raise RuntimeError(f"HTML analytics provenance not exactly once at v1.8.0: {path.relative_to(SITE)}")
        if 'data-v14-support-version="true"' in page and f"AI Playgrounds · {CURRENT}</p>" not in page:
            raise RuntimeError(f"Support-page visible version not v1.8.0: {path.relative_to(SITE)}")
    for path in applets:
        page = path.read_text(encoding="utf-8")
        if '<meta name="ai-playgrounds-version" content="1.8.0">' not in page:
            raise RuntimeError(f"Applet version metadata not v1.8.0: {path.parent.name}")
        if 'data-ai-playgrounds-analytics="v1.8.0"' not in page:
            raise RuntimeError(f"Applet analytics provenance not v1.8.0: {path.parent.name}")
    for slug, markers in FEATURES.items():
        page = (SITE / "playgrounds" / slug / "index.html").read_text(encoding="utf-8")
        missing = [marker for marker in markers if marker not in page]
        if missing:
            raise RuntimeError(f"v1.8.0 feature composition incomplete for {slug}: {missing}")
    home = (SITE / "index.html").read_text(encoding="utf-8")
    if '<span class="site-version">v1.8.0</span>' not in home:
        raise RuntimeError("Homepage visible release version is not v1.8.0")
    notes = (SITE / "release-notes.html").read_text(encoding="utf-8")
    for release in ("release-v1-8-0", "release-v1-7-2", "release-v1-7-1", "release-v1-7-0"):
        if f'id="{release}"' not in notes:
            raise RuntimeError(f"Release-note history missing {release}")
    codemeta = json.loads((SITE / "codemeta.json").read_text(encoding="utf-8"))
    if codemeta.get("softwareVersion") != VERSION or not str(codemeta.get("identifier", "")).endswith("/releases/tag/v1.8.0"):
        raise RuntimeError("Deployed CodeMeta is not bound to v1.8.0")
    citation = (SITE / "CITATION.cff").read_text(encoding="utf-8")
    if re.search(r"(?m)^version:\s*['\"]?1\.8\.0['\"]?\s*$", citation) is None:
        raise RuntimeError("Deployed citation metadata is not bound to v1.8.0")
    core.validate_local_references()


def build_site() -> None:
    base.build_site()
    patch_release_identity()
    validate()
    print("Built deterministic v1.8.0 algorithm-modes release: 15 applets / 58 files")


if __name__ == "__main__":
    build_site()
