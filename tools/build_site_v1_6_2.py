#!/usr/bin/env python3
from __future__ import annotations

"""v1.6.2 public-provenance hotfix over the verified v1.6.1 composition.

No applet algorithm, curriculum item, Quick Assign, or learner mechanism changes here.
The wrapper normalizes current-release provenance only after the complete v1.6.1
composition has been generated, while preserving historical release-note text.
"""

from pathlib import Path
import re

import build_site_v1_6_1_consistency as base

SITE = base.SITE
CURRENT = "v1.6.2"


def patch_current_provenance() -> None:
    for path in sorted(SITE.rglob("*.html")):
        html = path.read_text(encoding="utf-8")

        # Machine/current-release markers. These are not historical prose.
        html = re.sub(
            r'(<meta name="ai-playgrounds-version" content=")1\.6\.1(")',
            r'\g<1>1.6.2\2',
            html,
        )
        html = re.sub(
            r'data-ai-playgrounds-analytics="v1\.6\.[01]"',
            'data-ai-playgrounds-analytics="v1.6.2"',
            html,
        )
        html = html.replace('<span class="site-version">v1.6.0</span>', '<span class="site-version">v1.6.2</span>')
        html = html.replace('data-v14-support-version="true">AI Playgrounds · v1.6.1<', 'data-v14-support-version="true">AI Playgrounds · v1.6.2<')
        html = html.replace('data-v14-version-provenance="true" role="contentinfo">AI Playgrounds · v1.6.1<', 'data-v14-version-provenance="true" role="contentinfo">AI Playgrounds · v1.6.2<')
        html = html.replace('<span>AI Playgrounds · v1.6.1</span> · <a href="../../index.html"', '<span>AI Playgrounds · v1.6.2</span> · <a href="../../index.html"')

        path.write_text(html, encoding="utf-8")

    # Modern applet legacy chrome is hidden by the shared shell, but it remains
    # part of the shipped HTML and should not carry stale current-version tokens.
    for slug in ("transformer-language-model", "agent-tool-context", "minimax-alpha-beta"):
        path = SITE / "playgrounds" / slug / "index.html"
        html = path.read_text(encoding="utf-8")
        html = html.replace("v1.6.0", "v1.6.2")
        html = html.replace("AI Playgrounds · v1.6.1", "AI Playgrounds · v1.6.2")
        path.write_text(html, encoding="utf-8")

    # Preserve v1.6.0/v1.6.1 as historical sections, while making the current
    # public release-notes page explicitly lead with the hotfix and prior patch.
    notes = SITE / "release-notes.html"
    html = notes.read_text(encoding="utf-8")
    anchor = '<section id="release-v1-6-0"'
    if anchor not in html:
        raise RuntimeError("Release-notes v1.6.0 anchor changed")
    if 'id="release-v1-6-2"' not in html:
        current_sections = (
            '<section id="release-v1-6-2" style="margin:1rem 0;padding:1rem 1.2rem;border:1px solid currentColor;border-radius:12px">'
            '<h2>AI Playgrounds v1.6.2: public provenance hotfix.</h2>'
            '<p>Normalizes current-version labels and analytics provenance across the exact generated Pages artifact after the v1.6.1 post-deployment audit found legacy v1.6.0 markers. No algorithm, curriculum, or assignment behavior changes.</p></section>'
            '<section id="release-v1-6-1" style="margin:1rem 0;padding:1rem 1.2rem;border:1px solid currentColor;border-radius:12px">'
            '<h2>AI Playgrounds v1.6.1: Quick Assign and cross-suite consistency hardening.</h2>'
            '<p>Formalized four early-course Quick Assign canaries, repaired landing/search/localization drift, standardized the outer shell of Labs 13–15, and added permanent design-system and final-composition QA contracts.</p></section>'
        )
        html = html.replace(anchor, current_sections + anchor, 1)
    notes.write_text(html, encoding="utf-8")


def validate() -> None:
    html_files = sorted(SITE.rglob("*.html"))
    if not html_files:
        raise RuntimeError("No generated HTML files")

    applets = sorted((SITE / "playgrounds").glob("*/index.html"))
    if len(applets) != 15:
        raise RuntimeError(f"Expected 15 applets, found {len(applets)}")

    for path in applets:
        html = path.read_text(encoding="utf-8")
        if '<meta name="ai-playgrounds-version" content="1.6.2">' not in html:
            raise RuntimeError(f"Applet current-version metadata not v1.6.2: {path}")
        if 'data-ai-playgrounds-analytics="v1.6.2"' not in html:
            raise RuntimeError(f"Applet analytics provenance not v1.6.2: {path}")

    home = (SITE / "index.html").read_text(encoding="utf-8")
    if '<span class="site-version">v1.6.2</span>' not in home:
        raise RuntimeError("Homepage visible release version is not v1.6.2")

    for slug in ("transformer-language-model", "agent-tool-context", "minimax-alpha-beta"):
        html = (SITE / "playgrounds" / slug / "index.html").read_text(encoding="utf-8")
        if "v1.6.0" in html:
            raise RuntimeError(f"Modern applet retains stale v1.6.0 token: {slug}")

    notes = (SITE / "release-notes.html").read_text(encoding="utf-8")
    if 'id="release-v1-6-2"' not in notes or 'id="release-v1-6-1"' not in notes or 'id="release-v1-6-0"' not in notes:
        raise RuntimeError("Release notes do not preserve 1.6.2 -> 1.6.1 -> 1.6.0 history")

    base.impl.base.validate_local_references()


def build_site() -> None:
    base.build_site()
    patch_current_provenance()
    validate()
    print("Built v1.6.2 public provenance hotfix: 15 applets; no algorithm/curriculum changes")


if __name__ == "__main__":
    build_site()
