#!/usr/bin/env python3
from __future__ import annotations

"""Deterministic v1.7.1 consistency patch composition.

v1.7.1 keeps the v1.7.0 curriculum, Quick Assign, and algorithm boundaries.
It changes only shared-shell behavior for Labs 13-15 so theme preference follows
the same persisted `theme` contract used by the original applets. The temporary
`ai-playgrounds-theme` key is read once as a migration fallback and then removed.
"""

import build_site_v1_7 as base

SITE = base.SITE
CURRENT = "v1.7.1"
MODERN = ("transformer-language-model", "agent-tool-context", "minimax-alpha-beta")

OLD_THEME_RUNTIME = """$('#ap-standard-theme')?.addEventListener('click',()=>{document.body.classList.toggle('ap-standard-dark');localStorage.setItem('ai-playgrounds-theme',document.body.classList.contains('ap-standard-dark')?'dark':'light')});if(localStorage.getItem('ai-playgrounds-theme')==='dark')document.body.classList.add('ap-standard-dark');"""

NEW_THEME_RUNTIME = """const themeButton=$('#ap-standard-theme');function applySharedTheme(value){const dark=value==='dark';document.body.classList.toggle('ap-standard-dark',dark);if(themeButton){themeButton.textContent=dark?'☀️':'🌙';themeButton.setAttribute('aria-pressed',dark?'true':'false')}try{localStorage.setItem('theme',dark?'dark':'light')}catch(_){}}let sharedTheme='light';try{sharedTheme=localStorage.getItem('theme')||localStorage.getItem('ai-playgrounds-theme')||(window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light')}catch(_){}applySharedTheme(sharedTheme);try{localStorage.removeItem('ai-playgrounds-theme')}catch(_){}themeButton?.addEventListener('click',()=>applySharedTheme(document.body.classList.contains('ap-standard-dark')?'light':'dark'));"""


def patch_modern_theme_contract() -> None:
    for slug in MODERN:
        path = SITE / "playgrounds" / slug / "index.html"
        html = path.read_text(encoding="utf-8")
        if OLD_THEME_RUNTIME not in html:
            raise RuntimeError(f"Modern-shell theme runtime marker changed: {slug}")
        html = html.replace(OLD_THEME_RUNTIME, NEW_THEME_RUNTIME, 1)
        html = html.replace('content="1.7.0"', 'content="1.7.1"')
        html = html.replace('data-ai-playgrounds-analytics="v1.7.0"', 'data-ai-playgrounds-analytics="v1.7.1"')
        html = html.replace('AI Playgrounds · v1.7.0', 'AI Playgrounds · v1.7.1')
        path.write_text(html, encoding="utf-8")

    # Current generic surfaces show the patch version as provenance only. Historical
    # release-note sections remain unchanged.
    for path in sorted(SITE.rglob("*.html")):
        if path.parent.name in MODERN:
            continue
        html = path.read_text(encoding="utf-8")
        html = html.replace('<span class="site-version">v1.7.0</span>', '<span class="site-version">v1.7.1</span>')
        html = html.replace('data-ai-playgrounds-analytics="v1.7.0"', 'data-ai-playgrounds-analytics="v1.7.1"')
        html = html.replace('<meta name="ai-playgrounds-version" content="1.7.0">', '<meta name="ai-playgrounds-version" content="1.7.1">')
        path.write_text(html, encoding="utf-8")


def validate() -> None:
    files = sorted(p for p in SITE.rglob("*") if p.is_file())
    applets = sorted((SITE / "playgrounds").glob("*/index.html"))
    if len(files) != 58 or len(applets) != 15:
        raise RuntimeError(f"v1.7.1 boundary drift: {len(files)} files / {len(applets)} applets")

    for slug in MODERN:
        html = (SITE / "playgrounds" / slug / "index.html").read_text(encoding="utf-8")
        if "localStorage.setItem('theme'" not in html:
            raise RuntimeError(f"Modern lab does not write shared theme key: {slug}")
        if "localStorage.getItem('theme')||localStorage.getItem('ai-playgrounds-theme')" not in html:
            raise RuntimeError(f"Modern lab lacks legacy-key migration fallback: {slug}")
        if "localStorage.setItem('ai-playgrounds-theme'" in html:
            raise RuntimeError(f"Modern lab still writes obsolete theme key: {slug}")
        if "localStorage.removeItem('ai-playgrounds-theme')" not in html:
            raise RuntimeError(f"Modern lab does not retire obsolete theme key after migration: {slug}")
        if '<meta name="ai-playgrounds-version" content="1.7.1">' not in html:
            raise RuntimeError(f"Modern lab provenance not v1.7.1: {slug}")

    base.base.quick.base.base.impl.base.validate_local_references()


def build_site() -> None:
    base.build_site()
    patch_modern_theme_contract()
    validate()
    print("Built deterministic v1.7.1 patch candidate: shared theme contract across original and modern applets")


if __name__ == "__main__":
    build_site()
