#!/usr/bin/env python3
from __future__ import annotations

"""Final-composition wrapper for the v1.7 all-lab Quick Assign candidate.

The v1.7 behavior builder owns assignment content. This wrapper contains only
product-level composition corrections found by integrated QA:

* replace the generated modern Quick Assign script with one known-valid runtime;
* preserve JavaScript backslash escapes byte-for-byte during regex replacement;
* open targeted modern Quick Assigns from their canonical assignment URL;
* contain the modern response surface at narrow viewports;
* remove a drifting current-release suffix from Activity Pack pilot footers.
"""

import json
import re

import build_site_v1_7_quick_assigns as quick

SITE = quick.SITE
MODERN_SLUGS = ("transformer-language-model", "agent-tool-context", "minimax-alpha-beta")

MODERN_CONTAINMENT = r'''<style id="v17-modern-quick-assign-containment">
.quick-assign-modern{width:100%!important;max-width:100%!important;min-width:0!important;box-sizing:border-box!important;overflow-wrap:anywhere;overflow-x:clip!important}
.quick-assign-modern *{min-width:0;box-sizing:border-box}
.quick-assign-modern summary,.quick-assign-modern-body,.qa-modern-field{min-width:0!important;max-width:100%!important;box-sizing:border-box!important;white-space:normal!important;overflow-wrap:anywhere!important}
.quick-assign-modern .challenge-controls{display:flex!important;flex-wrap:wrap!important;min-width:0!important;max-width:100%!important}
.quick-assign-modern textarea{display:block;width:100%!important;max-width:100%!important;min-width:0!important;box-sizing:border-box!important}
.quick-assign-modern button{max-width:100%!important;white-space:normal!important;overflow-wrap:anywhere!important}
@media(max-width:480px){
  .quick-assign-modern{width:auto!important;max-width:100%!important;margin-left:0!important;margin-right:0!important;overflow:hidden!important}
  .quick-assign-modern .challenge-controls>*{flex:1 1 140px;max-width:100%!important}
}
</style>'''


def corrected_modern_runtime(row: dict) -> str:
    cfg = quick.MODERN[row["id"]]
    return rf'''<script data-quick-assign-modern-runtime="1">
(() => {{
  'use strict';
  const id = {json.dumps(row["id"])};
  const root = document.querySelector('[data-quick-assign-id="' + id + '"]');
  if (!root) return;
  const key = 'ai-playgrounds-quick-assign:' + id;
  const locale = () => {{
    const value = String(document.documentElement.lang || 'en').toLowerCase();
    return value.startsWith('zh') ? 'zh' : value.startsWith('vi') ? 'vi' : value.startsWith('es') ? 'es' : 'en';
  }};
  function paint() {{
    const language = locale();
    root.querySelectorAll('.qa-i18n').forEach(el => {{
      el.textContent = el.getAttribute('data-qa-' + language) || el.getAttribute('data-qa-en') || '';
    }});
  }}
  function save() {{
    try {{
      const data = {{}};
      root.querySelectorAll('[data-qa-answer]').forEach(el => data[el.dataset.qaAnswer] = el.value);
      localStorage.setItem(key, JSON.stringify(data));
    }} catch (_error) {{}}
  }}
  function load() {{
    try {{
      const data = JSON.parse(localStorage.getItem(key) || '{{}}');
      root.querySelectorAll('[data-qa-answer]').forEach(el => {{
        if (Object.prototype.hasOwnProperty.call(data, el.dataset.qaAnswer)) el.value = data[el.dataset.qaAnswer];
      }});
    }} catch (_error) {{}}
  }}
  root.addEventListener('input', event => {{
    if (event.target && event.target.matches('[data-qa-answer]')) save();
  }});
  root.querySelector('[data-qa-action="clear"]')?.addEventListener('click', () => {{
    root.querySelectorAll('[data-qa-answer]').forEach(el => el.value = '');
    try {{ localStorage.removeItem(key); }} catch (_error) {{}}
  }});
  root.querySelector('[data-qa-action="print"]')?.addEventListener('click', () => window.print());
  root.querySelector('[data-qa-action="copy"]')?.addEventListener('click', async () => {{
    const text = [...root.querySelectorAll('[data-qa-answer]')]
      .map(el => el.dataset.qaAnswer.toUpperCase() + ': ' + el.value)
      .join('\n\n');
    try {{ await navigator.clipboard.writeText(text); }} catch (_error) {{}}
  }});
  window.addEventListener({json.dumps(cfg["event"])}, () => setTimeout(paint, 0));
  document.querySelector('#ap-standard-language-select')?.addEventListener('change', () => setTimeout(paint, 0));
  load();
  paint();
}})();
</script>'''


def repair_modern_generated_runtime() -> None:
    rows = {row["slug"]: row for row in quick.registry()}
    pattern = re.compile(r'<script data-quick-assign-modern-runtime="1">.*?</script>', re.S)
    for slug in MODERN_SLUGS:
        path = SITE / "playgrounds" / slug / "index.html"
        html = path.read_text(encoding="utf-8")
        replacement = corrected_modern_runtime(rows[slug])
        # A callable replacement is required: re.sub replacement strings interpret
        # backslash escapes, which would turn JavaScript "\\n" back into a literal
        # line break inside a quoted string and reintroduce the syntax defect.
        html, count = pattern.subn(lambda _m, value=replacement: value, html, count=1)
        if count != 1:
            raise RuntimeError(f"Modern Quick Assign runtime replacement failed: {slug}")
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
        if html.count('data-quick-assign-modern-runtime="1"') != 1:
            raise RuntimeError(f"Modern Quick Assign runtime must exist exactly once: {slug}")
    for path in sorted((SITE / "activities").glob("*.html")):
        if "current suite release v1.6." in path.read_text(encoding="utf-8"):
            raise RuntimeError(f"Activity Pack current-version drift remains: {path.name}")
    quick.base.base.impl.base.validate_local_references()


def build_site() -> None:
    quick.build_site()
    repair_modern_generated_runtime()
    patch_modern_direct_open()
    decouple_activity_pack_footer()
    validate()
    print("Finalized v1.7 all-lab Quick Assign candidate with byte-stable modern runtime, usable deep links, narrow-view containment, and version-decoupled Activity Pack provenance")


if __name__ == "__main__":
    build_site()
