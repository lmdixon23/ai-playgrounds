#!/usr/bin/env python3
from __future__ import annotations

"""Thin corrective wrapper around the first v1.6.1 consistency implementation.

The original implementation is retained verbatim as
`build_site_v1_6_1_consistency_impl.py` for auditability. This wrapper corrects
one static/runtime distinction discovered by CI (the home language select is
created at runtime), and applies one final human-readable category fix before
running the final-composition checks.
"""

import re

import build_site_v1_6_1_consistency_impl as impl

SITE = impl.SITE


def validate(manifest: list[dict]) -> None:
    impl.base.validate_local_references()
    home = (SITE / "index.html").read_text(encoding="utf-8")
    if "undefinedundefined" in home or re.search(r">\s*undefined\s*<", home):
        raise RuntimeError("Landing page contains a literal undefined card value")
    # The select itself is created by the final runtime; static HTML must contain
    # the runtime contract, while Playwright verifies the actual rendered select.
    for marker in ("ap-home-language-select", "v161-home-four-locale-runtime"):
        if marker not in home:
            raise RuntimeError(f"Landing page lacks four-language runtime marker: {marker}")
    if 'hreflang="vi"' not in home or 'hreflang="es"' not in home:
        raise RuntimeError("Landing page lacks VI/ES discovery metadata")
    if len(manifest) != 15:
        raise RuntimeError("v1.6.1 consistency composition must contain 15 applets")
    for slug in impl.MODERN:
        source = (SITE / "playgrounds" / slug / "index.html").read_text(encoding="utf-8")
        if source.count("data-ap-standard-shell") != 1 or source.count("data-ap-standard-footer") != 1:
            raise RuntimeError(f"Modern applet lacks exactly one standard outer shell: {slug}")
    r4 = (SITE / "assets" / "localization-r4.js").read_text(encoding="utf-8")
    if "preserve canonical source text across VI/ES round trips" not in r4:
        raise RuntimeError("R4 locale round-trip patch missing from final composition")
    for page in ("teacher-pack.html", "curriculum.html", "quality.html", "research-and-citation.html"):
        source = (SITE / page).read_text(encoding="utf-8")
        if "v14-language-select" in source and 'id="v161-select-shell-fix"' not in source:
            raise RuntimeError(f"Support page language selector shell was not flattened: {page}")


def patch_human_categories() -> None:
    path = SITE / "index.html"
    html = path.read_text(encoding="utf-8")
    old = "const category=apField(a,'category')||apField(a,'category_en')||a.course_phase||'AI';"
    new = "const category=(lang==='en'?(a.category_en||a.category):((a['category_'+lang])||a.category_en||a.category))||a.course_phase||'AI';"
    if old not in html:
        raise RuntimeError("Landing category-renderer marker changed")
    html = html.replace(old, new, 1)
    path.write_text(html, encoding="utf-8")


def build_site() -> None:
    impl.validate = validate
    impl.build_site()
    patch_human_categories()
    impl.base.validate_local_references()
    print("Finalized v1.6.1 consistency composition with runtime language-selector validation and human-readable card categories")


if __name__ == "__main__":
    build_site()
