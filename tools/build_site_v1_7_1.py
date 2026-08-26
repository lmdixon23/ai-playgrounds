#!/usr/bin/env python3
from __future__ import annotations

"""Deterministic v1.7.1 public composition.

v1.7.1 is a parity/accessibility patch over v1.7.0. It keeps the exact
15-applet curriculum and 15 Quick Assign registry, then applies the verified
modern-lab parity wrapper to Labs 13-15 and normalizes current-release
provenance to v1.7.1. No AI algorithm or assignment identity changes.
"""

import json
import re
from pathlib import Path

import build_site as core
import build_site_v1_7_1_modern_parity_stable as base

ROOT = Path(__file__).resolve().parents[1]
SITE = base.SITE
CURRENT = "v1.7.1"
VERSION = "1.7.1"
REGISTRY = ROOT / "tools" / "quick_assigns_v2.json"


def patch_current_provenance() -> None:
    for path in sorted(SITE.rglob("*.html")):
        html = path.read_text(encoding="utf-8")
        if path.name != "release-notes.html":
            html = re.sub(
                r'(<meta name="ai-playgrounds-version" content=")(?:1\.6\.2|1\.7\.0)(")',
                rf'\g<1>{VERSION}\2', html,
            )
            html = re.sub(
                r'data-ai-playgrounds-analytics="v(?:1\.6\.2|1\.7\.0)"',
                f'data-ai-playgrounds-analytics="{CURRENT}"', html,
            )
            html = html.replace('<span class="site-version">v1.6.2</span>', f'<span class="site-version">{CURRENT}</span>')
            html = html.replace('<span class="site-version">v1.7.0</span>', f'<span class="site-version">{CURRENT}</span>')
            html = html.replace('data-v14-support-version="true">AI Playgrounds · v1.6.2<', f'data-v14-support-version="true">AI Playgrounds · {CURRENT}<')
            html = html.replace('data-v14-support-version="true">AI Playgrounds · v1.7.0<', f'data-v14-support-version="true">AI Playgrounds · {CURRENT}<')
            html = html.replace('data-v14-version-provenance="true" role="contentinfo">AI Playgrounds · v1.6.2<', f'data-v14-version-provenance="true" role="contentinfo">AI Playgrounds · {CURRENT}<')
            html = html.replace('data-v14-version-provenance="true" role="contentinfo">AI Playgrounds · v1.7.0<', f'data-v14-version-provenance="true" role="contentinfo">AI Playgrounds · {CURRENT}<')
        path.write_text(html, encoding="utf-8")

    for slug in base.MODERN:
        path = SITE / "playgrounds" / slug / "index.html"
        html = path.read_text(encoding="utf-8")
        html = html.replace("v1.6.2", CURRENT).replace("v1.7.0", CURRENT)
        path.write_text(html, encoding="utf-8")

    notes = SITE / "release-notes.html"
    html = notes.read_text(encoding="utf-8")
    anchor = '<section id="release-v1-6-2"'
    if anchor not in html:
        raise RuntimeError("Release-notes v1.6.2 anchor changed")
    if 'id="release-v1-7-0"' not in html:
        history = (
            '<section id="release-v1-7-0" style="margin:1rem 0;padding:1rem 1.2rem;border:1px solid currentColor;border-radius:12px">'
            '<h2>AI Playgrounds v1.7.0: Quick Assigns for all fifteen labs.</h2>'
            '<p>Completed the Level 1 teacher-assignment layer with one stable 10-15 minute Quick Assign per applet, canonical classroom links, local-only responses, and four-locale presentation. No new algorithm or sixteenth lab was added.</p></section>'
        )
        html = html.replace(anchor, history + anchor, 1)
    if 'id="release-v1-7-1"' not in html:
        section = (
            '<section id="release-v1-7-1" style="margin:1rem 0;padding:1rem 1.2rem;border:1px solid currentColor;border-radius:12px">'
            '<h2>AI Playgrounds v1.7.1: modern-lab parity hardening.</h2>'
            '<p>Brings Labs 13-15 onto the mature suite shell and support contract: Share/More/Reset hierarchy, shared theme preference, embed/settings helpers, orientation and fidelity support, complete discovery metadata, state-aware Quick Assign packets, and an open keyboard/text-state/reduced-motion accessibility layer. Core Transformer, agent-runtime, and Minimax/Alpha-Beta mechanisms are unchanged.</p></section>'
        )
        insert = html.find('<section id="release-v1-7-0"')
        if insert < 0:
            raise RuntimeError("Release-notes v1.7.0 insertion point missing")
        html = html[:insert] + section + html[insert:]
    notes.write_text(html, encoding="utf-8")


def validate() -> None:
    files = sorted(p for p in SITE.rglob("*") if p.is_file())
    applets = sorted((SITE / "playgrounds").glob("*/index.html"))
    if len(files) != 58 or len(applets) != 15:
        raise RuntimeError(f"v1.7.1 boundary drift: {len(files)} files / {len(applets)} applets")

    for path in applets:
        html = path.read_text(encoding="utf-8")
        if f'<meta name="ai-playgrounds-version" content="{VERSION}">' not in html:
            raise RuntimeError(f"Applet version metadata not {VERSION}: {path}")
        if f'data-ai-playgrounds-analytics="{CURRENT}"' not in html:
            raise RuntimeError(f"Applet analytics provenance not {CURRENT}: {path}")

    home = (SITE / "index.html").read_text(encoding="utf-8")
    if f'<span class="site-version">{CURRENT}</span>' not in home:
        raise RuntimeError("Homepage visible release version is not v1.7.1")
    if "undefinedundefined" in home or re.search(r'>\s*undefined\s*<', home):
        raise RuntimeError("Homepage contains undefined catalogue output")

    rows = json.loads(REGISTRY.read_text(encoding="utf-8"))["activities"]
    if len(rows) != 15 or len({r["id"] for r in rows}) != 15 or any(r.get("status") != "active" for r in rows):
        raise RuntimeError("v1.7.1 must preserve the 15-active-Quick-Assign registry")

    for slug in base.MODERN:
        html = (SITE / "playgrounds" / slug / "index.html").read_text(encoding="utf-8")
        required = (
            'class="ap-standard-header page-header"', 'id="ap-modern-share"', 'id="ap-modern-more"',
            'id="ap-modern-settings-json"', 'id="ap-modern-a11y"', 'id="ap-modern-a11y-state"',
            'id="v171-modern-packet-label-runtime"', 'data-v171-stable-lifecycle="true"',
            'id="v171-modern-toolbar-runtime"', '<script type="application/ld+json">',
        )
        missing = [marker for marker in required if marker not in html]
        if missing:
            raise RuntimeError(f"v1.7.1 modern parity missing for {slug}: {missing}")
        panel = re.search(r'<details\s+id="ap-modern-a11y"([^>]*)>', html, flags=re.I)
        if not panel or "open" not in panel.group(1).lower():
            raise RuntimeError(f"v1.7.1 accessibility panel is not open by default: {slug}")

    notes = (SITE / "release-notes.html").read_text(encoding="utf-8")
    for rel in ("release-v1-7-1", "release-v1-7-0", "release-v1-6-2", "release-v1-6-1", "release-v1-6-0"):
        if f'id="{rel}"' not in notes:
            raise RuntimeError(f"Release-note history missing {rel}")

    core.validate_local_references()


def build_site() -> None:
    base.build_site()
    patch_current_provenance()
    validate()
    print("Built deterministic v1.7.1 public site: 15 applets / 58 files / modern-lab parity hardening")


if __name__ == "__main__":
    build_site()
