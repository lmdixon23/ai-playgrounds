#!/usr/bin/env python3
from __future__ import annotations

"""Final-composition wrapper for the v1.7 all-lab Quick Assign candidate.

The v1.7 behavior builder owns the assignment content. This wrapper adds only
product-level composition fixes discovered by the integrated browser gate:

* canonical modern-lab Quick Assign URLs open their targeted response surface,
  so a teacher's direct assignment link is immediately usable rather than
  landing on a collapsed details element;
* the Activity Pack pilot footer no longer hard-codes a separate "current suite
  release" value, eliminating the provenance drift found by the v1.6.2 live
  audit.
"""

from pathlib import Path

import build_site_v1_7_quick_assigns as quick

SITE = quick.SITE
MODERN_SLUGS = ("transformer-language-model", "agent-tool-context", "minimax-alpha-beta")


def patch_modern_direct_open() -> None:
    runtime = r'''<script data-v17-quick-assign-direct-open="1">
(() => {
  'use strict';
  function revealTarget() {
    const raw = String(location.hash || '');
    if (!raw.startsWith('#quick-assign-')) return;
    let target = null;
    try { target = document.querySelector(raw); } catch (_error) { return; }
    if (!target || !target.matches('details[data-quick-assign-id]')) return;
    target.open = true;
    requestAnimationFrame(() => target.scrollIntoView({block:'start'}));
  }
  revealTarget();
  window.addEventListener('hashchange', revealTarget);
})();
</script>'''
    for slug in MODERN_SLUGS:
        path = SITE / "playgrounds" / slug / "index.html"
        html = path.read_text(encoding="utf-8")
        if 'data-v17-quick-assign-direct-open="1"' in html:
            raise RuntimeError(f"Direct-open runtime would be applied twice: {slug}")
        if "</body>" not in html:
            raise RuntimeError(f"Modern applet lacks </body>: {slug}")
        html = html.replace("</body>", runtime + "\n</body>", 1)
        path.write_text(html, encoding="utf-8")


def decouple_activity_pack_footer() -> None:
    for path in sorted((SITE / "activities").glob("*.html")):
        html = path.read_text(encoding="utf-8")
        html = html.replace(" · current suite release v1.6.1", "")
        html = html.replace(" · current suite release v1.6.2", "")
        if "current suite release v1.6." in html:
            raise RuntimeError(f"Activity Pack footer retains current-release coupling: {path.name}")
        path.write_text(html, encoding="utf-8")


def validate() -> None:
    for slug in MODERN_SLUGS:
        html = (SITE / "playgrounds" / slug / "index.html").read_text(encoding="utf-8")
        if html.count('data-v17-quick-assign-direct-open="1"') != 1:
            raise RuntimeError(f"Modern Quick Assign direct-open contract missing: {slug}")
    for path in sorted((SITE / "activities").glob("*.html")):
        html = path.read_text(encoding="utf-8")
        if "current suite release v1.6." in html:
            raise RuntimeError(f"Activity Pack current-version drift remains: {path.name}")
    quick.base.base.impl.base.validate_local_references()


def build_site() -> None:
    quick.build_site()
    patch_modern_direct_open()
    decouple_activity_pack_footer()
    validate()
    print("Finalized v1.7 all-lab Quick Assign candidate with usable modern deep links and version-decoupled Activity Pack provenance")


if __name__ == "__main__":
    build_site()
