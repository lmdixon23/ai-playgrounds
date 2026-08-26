#!/usr/bin/env python3
from __future__ import annotations

"""Final-composition wrapper for the v1.7 all-lab Quick Assign candidate.

The v1.7 behavior builder owns the assignment content. This wrapper contains
only product-level composition fixes found by integrated QA:

* canonical modern-lab Quick Assign URLs open their targeted response surface;
* a generated JavaScript newline escape is normalized before browser execution;
* the modern response surface is explicitly contained at narrow viewports;
* Activity Pack pilot footers do not hard-code a second current-suite version.
"""

import build_site_v1_7_quick_assigns as quick

SITE = quick.SITE
MODERN_SLUGS = ("transformer-language-model", "agent-tool-context", "minimax-alpha-beta")

MODERN_CONTAINMENT = r'''<style id="v17-modern-quick-assign-containment">
.quick-assign-modern{width:100%!important;max-width:100%!important;min-width:0!important;box-sizing:border-box!important;overflow-wrap:anywhere}
.quick-assign-modern-body,.qa-modern-field{min-width:0!important;max-width:100%!important;box-sizing:border-box!important}
.quick-assign-modern .challenge-controls{display:flex!important;flex-wrap:wrap!important;min-width:0!important;max-width:100%!important}
.quick-assign-modern textarea{width:100%!important;max-width:100%!important;min-width:0!important;box-sizing:border-box!important}
.quick-assign-modern button{max-width:100%!important;white-space:normal!important}
@media(max-width:480px){.quick-assign-modern{overflow:hidden}.quick-assign-modern .challenge-controls>*{flex:1 1 150px}}
</style>'''


def repair_modern_generated_runtime() -> None:
    """Repair one Python-to-JS escape boundary in the generated modern layer."""
    bad = "join('\n\n');try{await navigator.clipboard.writeText(text);}"
    good = "join('\\\\n\\\\n');try{await navigator.clipboard.writeText(text);}"
    for slug in MODERN_SLUGS:
        path = SITE / "playgrounds" / slug / "index.html"
        html = path.read_text(encoding="utf-8")
        if bad not in html:
            raise RuntimeError(f"Modern Quick Assign generated-runtime escape marker changed: {slug}")
        html = html.replace(bad, good, 1)
        if 'id="v17-modern-quick-assign-containment"' in html:
            raise RuntimeError(f"Modern containment would be applied twice: {slug}")
        html = html.replace("</head>", MODERN_CONTAINMENT + "\n</head>", 1)
        path.write_text(html, encoding="utf-8")


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
        if html.count('id="v17-modern-quick-assign-containment"') != 1:
            raise RuntimeError(f"Modern Quick Assign containment contract missing: {slug}")
        if "join('\n\n');try{await navigator.clipboard.writeText(text);}" in html:
            raise RuntimeError(f"Modern Quick Assign runtime still contains literal newline escape defect: {slug}")
    for path in sorted((SITE / "activities").glob("*.html")):
        html = path.read_text(encoding="utf-8")
        if "current suite release v1.6." in html:
            raise RuntimeError(f"Activity Pack current-version drift remains: {path.name}")
    quick.base.base.impl.base.validate_local_references()


def build_site() -> None:
    quick.build_site()
    repair_modern_generated_runtime()
    patch_modern_direct_open()
    decouple_activity_pack_footer()
    validate()
    print("Finalized v1.7 all-lab Quick Assign candidate with valid modern runtime, usable deep links, narrow-view containment, and version-decoupled Activity Pack provenance")


if __name__ == "__main__":
    build_site()
