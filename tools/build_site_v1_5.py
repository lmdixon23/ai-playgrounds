#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import build_site as base
import build_site_v1_4 as v14
from build_agent_tool_context_engagement_candidate import build_candidate as build_agent_engagement
from build_bayes_network_engagement_candidate import ADAPTER as BAYES_ADAPTER, CSS as BAYES_CSS, SCRIPT as BAYES_SCRIPT
from build_cnf_sat_engagement_candidate import CSS as CNF_CSS, SCRIPT as CNF_SCRIPT, TRACE_EXPOSURE as CNF_TRACE_EXPOSURE
from build_transformer_engagement_candidate import build_candidate as build_transformer_engagement

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
RELEASE_VERSION = "1.5.0"
PREVIOUS_VERSION = "1.4.0"
EXPECTED_FILES = 54
EXPECTED_APPLETS = 14


def insert_before_last(html: str, marker: str, fragment: str) -> str:
    index = html.rfind(marker)
    if index < 0:
        raise RuntimeError(f"Could not locate final {marker} marker")
    return html[:index] + fragment + html[index:]


def transform_cnf_sat() -> None:
    path = SITE / "playgrounds" / "cnf-sat" / "index.html"
    source = path.read_text(encoding="utf-8")
    marker = "    () => dpllSteps.length, renderDpllStep);\n\n  // Console acceptance test"
    if marker not in source:
        raise RuntimeError("Could not locate frozen DPLL stepper boundary in v1.5 composition")
    if "window.__cnfDpllPresentationState" in source:
        raise RuntimeError("CNF/SAT engagement transform would be applied twice")
    source = source.replace(
        marker,
        "    () => dpllSteps.length, renderDpllStep);" + CNF_TRACE_EXPOSURE + "\n  // Console acceptance test",
        1,
    )
    source = source.replace("</head>", CNF_CSS + "\n</head>", 1)
    source = insert_before_last(source, "</body>", CNF_SCRIPT + "\n")
    path.write_text(source, encoding="utf-8")


def transform_bayes_network() -> None:
    path = SITE / "playgrounds" / "bayes-network" / "index.html"
    source = path.read_text(encoding="utf-8")
    marker = "  function renderPosteriors(post, meta) {\n    const row = $('postRow');"
    if marker not in source:
        raise RuntimeError("Could not locate frozen Bayesian posterior renderer in v1.5 composition")
    if "__bayesPosteriorPresentationSnapshot" in source:
        raise RuntimeError("Bayesian engagement transform would be applied twice")
    source = source.replace(
        marker,
        "  function renderPosteriors(post, meta) {\n" + BAYES_ADAPTER + "    const row = $('postRow');",
        1,
    )
    source = source.replace("</head>", BAYES_CSS + "\n</head>", 1)
    source = insert_before_last(source, "</body>", BAYES_SCRIPT + "\n")
    path.write_text(source, encoding="utf-8")


def update_applet_release_provenance() -> None:
    for path in sorted((SITE / "playgrounds").glob("*/index.html")):
        html = path.read_text(encoding="utf-8")
        old_meta = f'name="ai-playgrounds-version" content="{PREVIOUS_VERSION}"'
        new_meta = f'name="ai-playgrounds-version" content="{RELEASE_VERSION}"'
        if old_meta not in html:
            raise RuntimeError(f"Missing inherited v1.4 version metadata before v1.5 upgrade: {path.parent.name}")
        html = html.replace(old_meta, new_meta, 1)
        slug = path.parent.name
        if slug in {"transformer-language-model", "agent-tool-context"}:
            old_visible = f"v{PREVIOUS_VERSION}"
            if old_visible not in html:
                raise RuntimeError(f"Missing inherited visible version provenance: {slug}")
            html = html.replace(old_visible, f"v{RELEASE_VERSION}", 1)
        else:
            old_visible = f"AI Playgrounds · v{PREVIOUS_VERSION}"
            if old_visible not in html:
                raise RuntimeError(f"Missing inherited applet provenance: {slug}")
            html = html.replace(old_visible, f"AI Playgrounds · v{RELEASE_VERSION}")
        path.write_text(html, encoding="utf-8")


def update_landing_release_provenance() -> None:
    path = SITE / "index.html"
    html = path.read_text(encoding="utf-8")
    html = html.replace(f'"version": "{PREVIOUS_VERSION}"', f'"version": "{RELEASE_VERSION}"', 1)
    html = html.replace(
        f'<meta name="ai-playgrounds-version" content="{PREVIOUS_VERSION}">',
        f'<meta name="ai-playgrounds-version" content="{RELEASE_VERSION}">',
        1,
    )
    html = html.replace(
        f'<span class="site-version">v{PREVIOUS_VERSION}</span>',
        f'<span class="site-version">v{RELEASE_VERSION}</span>',
        1,
    )
    if f"v{RELEASE_VERSION}" not in html:
        raise RuntimeError("Landing page did not receive v1.5 release provenance")
    path.write_text(html, encoding="utf-8")


def update_support_release_provenance() -> None:
    old = f'data-v14-support-version="true">AI Playgrounds · v{PREVIOUS_VERSION}'
    new = f'data-v14-support-version="true">AI Playgrounds · v{RELEASE_VERSION}'
    for path in sorted(SITE.glob("*.html")):
        if path.name == "index.html":
            continue
        html = path.read_text(encoding="utf-8")
        if old in html:
            html = html.replace(old, new)
            path.write_text(html, encoding="utf-8")


def add_v15_release_banner() -> None:
    path = SITE / "release-notes.html"
    html = path.read_text(encoding="utf-8")
    if "release-v1-5-0" in html:
        return
    marker = '<section id="release-v1-4-0"'
    if marker not in html:
        raise RuntimeError("Could not locate v1.4 public release banner for v1.5 insertion")
    banner = (
        '<section id="release-v1-5-0" style="margin:1rem 0;padding:1rem 1.2rem;border:1px solid currentColor;border-radius:12px">'
        '<h2><span class="v14-release-en">AI Playgrounds v1.5.0, released August 25, 2026.</span><span class="v14-release-zh">AI Playgrounds v1.5.0，发布于 2026 年 8 月 25 日。</span></h2>'
        '<p><span class="v14-release-en">v1.5 is the engagement-excellence pass: Transformer state continuity and deterministic continuation, a visible and isolated agent runtime sandbox, a DPLL branch/prune tree, and exact Bayesian before/after posterior deltas. Ten already-strong applets are deliberately unchanged rather than decorated.</span><span class="v14-release-zh">v1.5 是互动体验优化版本：加入 Transformer 状态连续视图与确定性续写、可视且隔离的智能体运行时沙盒、DPLL 分支/剪枝树，以及贝叶斯后验概率的精确前后差异。其余十个已经成熟的 applet 刻意保持不变，而不是添加装饰性效果。</span></p>'
        '</section>'
    )
    html = html.replace(marker, banner + marker, 1)
    path.write_text(html, encoding="utf-8")


def build_site() -> None:
    # Start from the exact v1.4 public composition and validate that inherited
    # release boundary before changing any version provenance or applet surface.
    v14.build_site()
    v14.validate_boundary()
    build_transformer_engagement(SITE / "playgrounds" / "transformer-language-model" / "index.html")
    build_agent_engagement(SITE / "playgrounds" / "agent-tool-context" / "index.html")
    transform_cnf_sat()
    transform_bayes_network()
    update_applet_release_provenance()
    update_landing_release_provenance()
    update_support_release_provenance()
    add_v15_release_banner()


def validate_boundary() -> None:
    # v1.4 was already validated before the v1.5 transformations. At this stage
    # its version assertions would correctly fail, so validate local references
    # plus the stricter v1.5 composition contract instead.
    base.validate_local_references()

    deployed_paths = sorted((SITE / "playgrounds").glob("*/index.html"))
    if len(deployed_paths) != EXPECTED_APPLETS:
        raise RuntimeError(f"v1.5 must preserve exactly {EXPECTED_APPLETS} applets")

    required_by_slug = {
        "transformer-language-model": ("Lab13EngagementExperience", "lab13-eq-flowline", "lab13-eq-compare-body"),
        "agent-tool-context": ("Lab14EngagementExperience", "lab14-eq-gates", "lab14-eq-sandbox"),
        "cnf-sat": ("__cnfDpllPresentationState", "__cnfDpllTreeExperience", "cnf-eq-svg"),
        "bayes-network": ("__bayesPosteriorPresentationSnapshot", "__bayesPosteriorDeltaExperience", "bayes-eq-strip"),
    }
    for path in deployed_paths:
        source = path.read_text(encoding="utf-8")
        slug = path.parent.name
        if f'name="ai-playgrounds-version" content="{RELEASE_VERSION}"' not in source:
            raise RuntimeError(f"Missing v1.5 version metadata: {slug}")
        if f"v{PREVIOUS_VERSION}" in source and slug in {"transformer-language-model", "agent-tool-context"}:
            raise RuntimeError(f"Modern applet still exposes v1.4 as current provenance: {slug}")
        for marker in required_by_slug.get(slug, ()):
            if marker not in source:
                raise RuntimeError(f"Missing v1.5 engagement marker {marker!r}: {slug}")

    # The FAS explicitly accepted only four applet behavior changes. Prevent
    # accidental widening of the public delta to the remaining ten applets.
    allowed = set(required_by_slug)
    for path in deployed_paths:
        slug = path.parent.name
        if slug in allowed:
            continue
        source = path.read_text(encoding="utf-8")
        for marker in (
            "lab13-engagement-excellence-runtime",
            "lab14-engagement-excellence-runtime",
            "cnf-engagement-excellence-runtime",
            "bayes-engagement-excellence-runtime",
        ):
            if marker in source:
                raise RuntimeError(f"Engagement candidate leaked into no-change applet {slug}")

    landing = (SITE / "index.html").read_text(encoding="utf-8")
    if f"v{RELEASE_VERSION}" not in landing:
        raise RuntimeError("Landing page lacks v1.5 provenance")
    if "release-v1-5-0" not in (SITE / "release-notes.html").read_text(encoding="utf-8"):
        raise RuntimeError("Public release notes lack the v1.5 engagement-excellence banner")


def main() -> None:
    build_site()
    validate_boundary()
    files = sorted(path for path in SITE.rglob("*") if path.is_file())
    if len(files) != EXPECTED_FILES:
        raise RuntimeError(f"Expected a {EXPECTED_FILES}-file minimal v1.5 Pages artifact, found {len(files)}")
    print(f"Built minimal v1.5 Pages candidate: {len(files)} files / {EXPECTED_APPLETS} applets")
    print("v1.5 engagement-excellence deployment boundary: PASS")


if __name__ == "__main__":
    main()
