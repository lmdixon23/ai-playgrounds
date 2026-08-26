#!/usr/bin/env python3
from __future__ import annotations

"""Deterministic v1.7.0 public composition.

v1.7.0 keeps the fifteen-app / 58-file curriculum boundary and activates one
Level 1 Quick Assign for every applet. This wrapper runs the verified all-lab
Quick Assign composition and then normalizes only current-release provenance.
Historical release-note sections remain historical.
"""

from pathlib import Path
import re

import build_site_v1_7_final as base

SITE = base.SITE
CURRENT = "v1.7.0"


def patch_current_provenance() -> None:
    for path in sorted(SITE.rglob("*.html")):
        html = path.read_text(encoding="utf-8")
        html = re.sub(r'(<meta name="ai-playgrounds-version" content=")1\.6\.2(")', r'\g<1>1.7.0\2', html)
        html = re.sub(r'data-ai-playgrounds-analytics="v1\.6\.2"', 'data-ai-playgrounds-analytics="v1.7.0"', html)
        html = html.replace('<span class="site-version">v1.6.2</span>', '<span class="site-version">v1.7.0</span>')
        html = html.replace('data-v14-support-version="true">AI Playgrounds · v1.6.2<', 'data-v14-support-version="true">AI Playgrounds · v1.7.0<')
        html = html.replace('data-v14-version-provenance="true" role="contentinfo">AI Playgrounds · v1.6.2<', 'data-v14-version-provenance="true" role="contentinfo">AI Playgrounds · v1.7.0<')
        html = html.replace('<span>AI Playgrounds · v1.6.2</span> · <a href="../../index.html"', '<span>AI Playgrounds · v1.7.0</span> · <a href="../../index.html"')
        path.write_text(html, encoding="utf-8")

    # Labs 13-15 retain hidden historical chrome in their generated single-file
    # bodies. Current hidden chrome must match the current release too.
    for slug in ("transformer-language-model", "agent-tool-context", "minimax-alpha-beta"):
        path = SITE / "playgrounds" / slug / "index.html"
        html = path.read_text(encoding="utf-8")
        html = html.replace("v1.6.2", "v1.7.0")
        path.write_text(html, encoding="utf-8")

    notes = SITE / "release-notes.html"
    html = notes.read_text(encoding="utf-8")
    anchor = '<section id="release-v1-6-2"'
    if anchor not in html:
        raise RuntimeError("Release-notes v1.6.2 anchor changed")
    if 'id="release-v1-7-0"' not in html:
        section = (
            '<section id="release-v1-7-0" style="margin:1rem 0;padding:1rem 1.2rem;border:1px solid currentColor;border-radius:12px">'
            '<h2>AI Playgrounds v1.7.0: Quick Assigns for all fifteen labs.</h2>'
            '<p>Completes the Level 1 teacher-assignment layer with one stable 10-15 minute Quick Assign per applet, canonical classroom links, local-only responses, four-locale presentation, and preserved mechanism-first Guided Challenges. No new algorithm or sixteenth lab is added.</p></section>'
        )
        html = html.replace(anchor, section + anchor, 1)
    notes.write_text(html, encoding="utf-8")


def validate() -> None:
    files = sorted(p for p in SITE.rglob("*") if p.is_file())
    applets = sorted((SITE / "playgrounds").glob("*/index.html"))
    if len(files) != 58 or len(applets) != 15:
        raise RuntimeError(f"v1.7.0 boundary drift: {len(files)} files / {len(applets)} applets")

    for path in applets:
        html = path.read_text(encoding="utf-8")
        if '<meta name="ai-playgrounds-version" content="1.7.0">' not in html:
            raise RuntimeError(f"Applet version metadata not v1.7.0: {path}")
        if 'data-ai-playgrounds-analytics="v1.7.0"' not in html:
            raise RuntimeError(f"Applet analytics provenance not v1.7.0: {path}")

    home = (SITE / "index.html").read_text(encoding="utf-8")
    if '<span class="site-version">v1.7.0</span>' not in home:
        raise RuntimeError("Homepage visible release version is not v1.7.0")
    if "undefinedundefined" in home or re.search(r'>\s*undefined\s*<', home):
        raise RuntimeError("Homepage contains undefined catalogue output")

    teacher = (SITE / "teacher-pack.html").read_text(encoding="utf-8")
    curriculum = (SITE / "curriculum.html").read_text(encoding="utf-8")
    rows = base.quick.registry()
    if len(rows) != 15 or any(row.get("status") != "active" for row in rows):
        raise RuntimeError("v1.7 Quick Assign registry is not fully active")
    for row in rows:
        canonical = f'playgrounds/{row["slug"]}/index.html?mode=classroom#{row["anchor"]}'
        if row["id"] not in teacher or canonical not in teacher:
            raise RuntimeError(f"Teacher Pack missing {row['id']}")
        if row["id"] not in curriculum or canonical not in curriculum:
            raise RuntimeError(f"Curriculum missing {row['id']}")

    for path in sorted((SITE / "activities").glob("*.html")):
        if "current suite release v1.6." in path.read_text(encoding="utf-8"):
            raise RuntimeError(f"Activity Pack retains drifting current-release suffix: {path.name}")

    notes = (SITE / "release-notes.html").read_text(encoding="utf-8")
    for rel in ("release-v1-7-0", "release-v1-6-2", "release-v1-6-1", "release-v1-6-0"):
        if f'id="{rel}"' not in notes:
            raise RuntimeError(f"Release-note history missing {rel}")

    base.quick.base.base.impl.base.validate_local_references()


def build_site() -> None:
    base.build_site()
    patch_current_provenance()
    validate()
    print("Built deterministic v1.7.0 public site: 15 applets / 58 files / 15 active Quick Assigns")


if __name__ == "__main__":
    build_site()
