#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

import build_site as base
import build_site_v1_6 as draft
import build_site_v1_5_1 as v151

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
EXPECTED_FILES = 58
EXPECTED_APPLETS = 15
EXPECTED_FOUNDATION_ROWS = 13
EXPECTED_APPLET_CARDS = 15
LAB15_SLUG = "minimax-alpha-beta"

TRANSFORMER_ROW = re.compile(
    r'<tr style="--applet-accent:#6d28d9"><td data-label="#"><span class="order-dot">13</span></td>'
    r'<td data-label="Applet"><a href="playgrounds/transformer-language-model/index\.html">[\s\S]*?</tr>'
)

# v1.5.1 deliberately adds a data attribute to the analytics script, while the
# older inherited removal regex expects a literal <script>. v1.6 therefore
# identifies the block by its stable privacy comment + data marker instead of
# depending on one historical serialization shape.
ANALYTICS_ANY_RE = re.compile(
    r"\s*<!-- AI Playgrounds aggregate analytics: canonical host only; no cookies; no third-party script; DNT/GPC and opt-out respected\. -->\s*"
    r"<script[^>]*data-ai-playgrounds-analytics=[\"'][^\"']+[\"'][^>]*>[\s\S]*?window\.aiPlaygroundsAnalytics[\s\S]*?</script>\s*",
    re.S,
)

LAB15_ROW = (
    '<tr style="--applet-accent:#0d9488"><td data-label="#"><span class="order-dot">13</span></td>'
    '<td data-label="Applet"><a href="playgrounds/minimax-alpha-beta/index.html">Game Trees: Minimax and Alpha-Beta Pruning</a></td>'
    '<td data-label="Concept area">Adversarial search</td>'
    '<td data-label="Why here">Extend search to an opponent: back terminal utilities through alternating MIN/MAX nodes, then prune branches that cannot change the exact minimax result.</td></tr>'
)

LAB15_CARD = (
    '<article class="applet-card" style="--applet-accent:#0d9488">'
    '<div class="card-head"><span class="card-icon">♟</span><span class="phase"><span class="v14-en">Foundations</span><span class="v14-zh">基础</span></span></div>'
    '<h3><a href="playgrounds/minimax-alpha-beta/index.html"><span class="v14-en">Game Trees: Minimax and Alpha-Beta Pruning</span><span class="v14-zh">博弈树：Minimax 与 Alpha-Beta 剪枝</span></a></h3>'
    '<p><span class="v14-en">Back terminal utilities through alternating MIN/MAX turns, then inspect exact alpha-beta cutoffs and move-order work.</span><span class="v14-zh">通过交替的 MIN/MAX 回传终局效用，再检查精确的 Alpha-Beta 截断以及行动顺序对工作量的影响。</span></p>'
    '<p class="tiny">30 min · Intermediate</p>'
    '</article>'
)


def corrected_patch_curriculum() -> None:
    path = SITE / "curriculum.html"
    html = path.read_text(encoding="utf-8")

    html, removed = TRANSFORMER_ROW.subn("", html, count=1)
    if removed != 1:
        raise RuntimeError("Could not remove Transformer course-boundary row for the v1.6 Foundations split")

    first_tbody = html.find("</tbody>")
    if first_tbody < 0:
        raise RuntimeError("Could not locate Foundations course table")
    html = html[:first_tbody] + LAB15_ROW + html[first_tbody:]

    map_anchor = "<section><h2>Applet map</h2>"
    map_start = html.find(map_anchor)
    if map_start < 0:
        raise RuntimeError("Could not locate curriculum applet map")
    section_end = html.find("</section>", map_start)
    if section_end < 0:
        raise RuntimeError("Could not locate end of curriculum applet map")
    grid_close = html.rfind("</div>", map_start, section_end)
    if grid_close < 0:
        raise RuntimeError("Could not locate end of curriculum applet grid")
    if f'playgrounds/{LAB15_SLUG}/index.html' not in html[map_start:section_end]:
        html = html[:grid_close] + LAB15_CARD + html[grid_close:]

    for old, new in {
        "Fourteen multilingual": "Fifteen multilingual",
        "fourteen multilingual": "fifteen multilingual",
        "fourteen public applets": "fifteen public applets",
        "fourteen applets": "fifteen applets",
    }.items():
        html = html.replace(old, new)

    if html.count('class="order-dot"') != EXPECTED_FOUNDATION_ROWS:
        raise RuntimeError(f"v1.6 Foundations table must contain exactly {EXPECTED_FOUNDATION_ROWS} rows")
    if html.count('class="applet-card"') != EXPECTED_APPLET_CARDS:
        raise RuntimeError(f"v1.6 applet map must contain exactly {EXPECTED_APPLET_CARDS} cards")
    if "modern-extensions" not in html:
        raise RuntimeError("v1.6 must preserve the Modern AI extensions section")
    modern = html[html.index('id="modern-extensions"'):map_start]
    if "Transformer Language Modeling" not in modern or "Agent Tool Use and Context Protocols" not in modern:
        raise RuntimeError("v1.6 Modern Extensions must preserve Transformer and Agent Tool Use")
    path.write_text(html, encoding="utf-8")


def corrected_upgrade_analytics() -> None:
    pages = sorted(path for path in SITE.rglob("*.html") if path.is_file())
    for path in pages:
        html = path.read_text(encoding="utf-8")
        html, removed = ANALYTICS_ANY_RE.subn("\n", html, count=1)
        # Lab 15 is newly generated and has no inherited project analytics block;
        # all inherited public pages must have exactly one removable block.
        if path.parent.name == LAB15_SLUG and path.parent.parent.name == "playgrounds":
            if removed not in (0, 1):
                raise RuntimeError("Unexpected Lab 15 analytics block count")
        elif removed != 1:
            raise RuntimeError(f"Could not remove exactly one inherited analytics block: {path.relative_to(SITE)}")
        if "data-ai-playgrounds-analytics=" in html:
            raise RuntimeError(f"Stale analytics marker remains before v1.6 insertion: {path.relative_to(SITE)}")
        kind, slug = v151.page_identity(path)
        block = v151.analytics_block(kind, slug).replace(
            'data-ai-playgrounds-analytics="v1.5.1"',
            'data-ai-playgrounds-analytics="v1.6.0"',
            1,
        )
        html = v151.insert_before_last(html, "</body>", block)
        path.write_text(html, encoding="utf-8")


def validate_boundary() -> None:
    base.validate_local_references()
    files = sorted(path for path in SITE.rglob("*") if path.is_file())
    if len(files) != EXPECTED_FILES:
        raise RuntimeError(f"Expected {EXPECTED_FILES} v1.6 files, found {len(files)}")

    applets = sorted((SITE / "playgrounds").glob("*/index.html"))
    if len(applets) != EXPECTED_APPLETS:
        raise RuntimeError(f"Expected {EXPECTED_APPLETS} v1.6 applets, found {len(applets)}")
    manifest_slugs = {str(entry["slug"]) for entry in draft.release_manifest()}
    if {path.parent.name for path in applets} != manifest_slugs:
        raise RuntimeError("v1.6 deployed applet set does not match the release manifest")

    activities = {path.name for path in (SITE / "activities").glob("*.html")}
    if activities != draft.EXPECTED_ACTIVITIES:
        raise RuntimeError(f"v1.6 Activity Pack boundary changed: {sorted(activities)}")

    for path in sorted(SITE.rglob("*.html")):
        source = path.read_text(encoding="utf-8")
        if source.count('data-ai-playgrounds-analytics="v1.6.0"') != 1:
            raise RuntimeError(f"v1.6 analytics coverage mismatch: {path.relative_to(SITE)}")
        if v151.ANALYTICS_COMMENT not in source:
            raise RuntimeError(f"Analytics privacy marker missing: {path.relative_to(SITE)}")

    lab15 = SITE / "playgrounds" / LAB15_SLUG / "index.html"
    source = lab15.read_text(encoding="utf-8")
    if source.count("function minimax(") != 1 or source.count("function alphaBeta(") != 1:
        raise RuntimeError("Public Lab 15 must preserve one minimax and one alpha-beta implementation")
    if any(token in source for token in ("fetch(", "XMLHttpRequest", "WebSocket", "EventSource", "<script src=")):
        raise RuntimeError("Public Lab 15 must remain self-contained and offline")

    curriculum = (SITE / "curriculum.html").read_text(encoding="utf-8")
    if curriculum.count('class="order-dot"') != EXPECTED_FOUNDATION_ROWS:
        raise RuntimeError("v1.6 curriculum Foundations row count is incorrect")
    if curriculum.count('class="applet-card"') != EXPECTED_APPLET_CARDS:
        raise RuntimeError("v1.6 curriculum applet map count is incorrect")
    foundation_table = curriculum[:curriculum.find("</tbody>")]
    if "transformer-language-model" in foundation_table or "agent-tool-context" in foundation_table:
        raise RuntimeError("Modern/boundary labs leaked into the v1.6 Foundations table")
    if LAB15_SLUG not in foundation_table:
        raise RuntimeError("Lab 15 is missing from the v1.6 Foundations table")

    landing = (SITE / "index.html").read_text(encoding="utf-8")
    teacher = (SITE / "teacher-pack.html").read_text(encoding="utf-8")
    if "15 interactive labs" not in landing or LAB15_SLUG not in landing:
        raise RuntimeError("v1.6 landing integration is incomplete")
    if "thirteen Foundations/course-track labs" not in teacher or LAB15_SLUG not in teacher:
        raise RuntimeError("v1.6 Teacher Pack integration is incomplete")
    if "release-v1-6-0" not in (SITE / "release-notes.html").read_text(encoding="utf-8"):
        raise RuntimeError("v1.6 public release banner is missing")


def build_site() -> None:
    original_curriculum = draft.patch_curriculum
    original_analytics = draft.upgrade_analytics
    try:
        draft.patch_curriculum = corrected_patch_curriculum
        draft.upgrade_analytics = corrected_upgrade_analytics
        draft.build_site()
    finally:
        draft.patch_curriculum = original_curriculum
        draft.upgrade_analytics = original_analytics
    validate_boundary()


def main() -> None:
    build_site()
    print(
        f"Built v1.6 public candidate: {EXPECTED_FILES} files / {EXPECTED_APPLETS} applets / "
        f"{EXPECTED_FOUNDATION_ROWS} Foundations + 2 Modern extensions"
    )
    print("v1.6 public deployment boundary: PASS")


if __name__ == "__main__":
    main()
