#!/usr/bin/env python3
from __future__ import annotations

"""Final corrective wrapper around the v1.6.1 consistency implementation.

The substantive implementation remains in `build_site_v1_6_1_consistency_impl.py`
for auditability. This wrapper contains only lifecycle corrections discovered by
the final browser gate:

* the home search input originally retained the pre-v1.6.1 renderer as its event
  listener even after the richer 15-lab renderer replaced the global function;
* R4 VI/ES overlays refreshed known applet layers after activating the overlay
  locale, which allowed native renderers to overwrite the stored English source;
* delayed VI/ES activation could outlive a later language choice and reapply a
  superseded translation after the learner had already returned to English.

The fixes preserve the existing product architecture rather than weakening the
consistency tests.
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


def patch_home_runtime() -> None:
    path = SITE / "index.html"
    html = path.read_text(encoding="utf-8")

    old_category = "const category=apField(a,'category')||apField(a,'category_en')||a.course_phase||'AI';"
    new_category = "const category=(lang==='en'?(a.category_en||a.category):((a['category_'+lang])||a.category_en||a.category))||a.course_phase||'AI';"
    if old_category not in html:
        raise RuntimeError("Landing category-renderer marker changed")
    html = html.replace(old_category, new_category, 1)

    # The base page registered its input listener before the v1.6.1 renderer was
    # installed. JavaScript event listeners retain the old function object, so
    # aliases that exist only in the enriched keyword registry never reached the
    # new renderer. Register the final renderer after replacement; it runs last.
    old_install = "function install(){const root=document.querySelector('.lang');"
    new_install = "function install(){const search=document.getElementById('search');if(search)search.addEventListener('input',renderApplets);const root=document.querySelector('.lang');"
    if old_install not in html:
        raise RuntimeError("Landing final-runtime install marker changed")
    html = html.replace(old_install, new_install, 1)

    path.write_text(html, encoding="utf-8")


def patch_r4_roundtrip_lifecycle() -> None:
    path = SITE / "assets" / "localization-r4.js"
    source = path.read_text(encoding="utf-8")

    # Capture stable page identity before any overlay is activated. The original
    # twelve applets all have a static H1 and English document title; keeping these
    # two identity anchors separate from mutable experiment state makes EN recovery
    # deterministic even when an applet renderer replaces text nodes.
    ordered_marker = "  const ordered = { vi: null, es: null };"
    ordered_replacement = (
        ordered_marker
        + "\n  let canonicalDocumentTitle = '';"
        + "\n  let canonicalHeadingText = '';"
        + "\n  let pendingOverlayTimer = null;"
    )
    if ordered_marker not in source:
        raise RuntimeError("R4 ordered-map marker changed")
    source = source.replace(ordered_marker, ordered_replacement, 1)

    # Refresh native/app-specific layers while the renderer is explicitly in
    # English, then activate VI/ES and apply the overlay. Previously `current` was
    # set to VI/ES first, so wrapped `tr()` calls could emit translated strings
    # that the observer then mistook for canonical source text.
    old_overlay = """  function activateOverlay(locale) {
    current = locale;
    document.documentElement.lang = locale;
    refreshKnownLayers();
    wrapTr();
    patchClipboard();
    applyMetadata(locale);
    translateTree(document.body);
    updateSelect(locale);
    updateUrl(locale);
    persist(locale);
    window.dispatchEvent(new CustomEvent('r4languagechange', { detail: { locale } }));
  }"""
    new_overlay = """  function activateOverlay(locale) {
    current = 'en';
    document.documentElement.lang = 'en';
    refreshKnownLayers();
    current = locale;
    document.documentElement.lang = locale;
    wrapTr();
    patchClipboard();
    applyMetadata(locale);
    translateTree(document.body);
    updateSelect(locale);
    updateUrl(locale);
    persist(locale);
    window.dispatchEvent(new CustomEvent('r4languagechange', { detail: { locale } }));
  }"""
    if old_overlay not in source:
        raise RuntimeError("R4 overlay lifecycle marker changed")
    source = source.replace(old_overlay, new_overlay, 1)

    old_setlocale_start = """  function setLocale(locale, options = {}) {
    locale = normalizeLocale(locale);
    if (!SUPPORTED.includes(locale)) locale = 'en';
    restoreTree(document.body);"""
    new_setlocale_start = """  function setLocale(locale, options = {}) {
    locale = normalizeLocale(locale);
    if (!SUPPORTED.includes(locale)) locale = 'en';
    if (pendingOverlayTimer !== null) {
      clearTimeout(pendingOverlayTimer);
      pendingOverlayTimer = null;
    }
    restoreTree(document.body);"""
    if old_setlocale_start not in source:
        raise RuntimeError("R4 setLocale start marker changed")
    source = source.replace(old_setlocale_start, new_setlocale_start, 1)

    old_native_branch = """    if (locale === 'en' || locale === 'zh') {
      current = locale;
      clickNative(locale);
      document.documentElement.lang = locale === 'zh' ? 'zh' : 'en';
      applyMetadata(locale);
      updateSelect(locale);
      updateUrl(locale);
      persist(locale);
      window.dispatchEvent(new CustomEvent('r4languagechange', { detail: { locale } }));
      return;
    }"""
    new_native_branch = """    if (locale === 'en' || locale === 'zh') {
      current = locale;
      clickNative(locale);
      document.documentElement.lang = locale === 'zh' ? 'zh' : 'en';
      refreshKnownLayers();
      if (locale === 'en') {
        const heading = document.querySelector('h1');
        if (heading && canonicalHeadingText) {
          applying = true;
          try { heading.textContent = canonicalHeadingText; } finally { applying = false; }
        }
      }
      applyMetadata(locale);
      if (locale === 'en' && canonicalDocumentTitle) document.title = canonicalDocumentTitle;
      updateSelect(locale);
      updateUrl(locale);
      persist(locale);
      window.dispatchEvent(new CustomEvent('r4languagechange', { detail: { locale } }));
      return;
    }"""
    if old_native_branch not in source:
        raise RuntimeError("R4 native-locale branch marker changed")
    source = source.replace(old_native_branch, new_native_branch, 1)

    old_schedule = """    current = 'en';
    clickNative('en');
    setTimeout(() => activateOverlay(locale), options.immediate ? 0 : 60);"""
    new_schedule = """    current = 'en';
    clickNative('en');
    pendingOverlayTimer = setTimeout(() => {
      pendingOverlayTimer = null;
      activateOverlay(locale);
    }, options.immediate ? 0 : 60);"""
    if old_schedule not in source:
        raise RuntimeError("R4 delayed-overlay marker changed")
    source = source.replace(old_schedule, new_schedule, 1)

    old_init = """  function init() {
    installSelect();"""
    new_init = """  function init() {
    canonicalDocumentTitle = document.title;
    const initialHeading = document.querySelector('h1');
    canonicalHeadingText = initialHeading ? initialHeading.textContent : '';
    installSelect();"""
    if old_init not in source:
        raise RuntimeError("R4 init marker changed")
    source = source.replace(old_init, new_init, 1)

    source = source.replace(
        "// v1.6.1: preserve canonical source text across VI/ES round trips.",
        "// v1.6.1: preserve canonical source text across VI/ES round trips, refresh native layers before overlay activation, and cancel superseded locale timers.",
        1,
    )
    path.write_text(source, encoding="utf-8")


def build_site() -> None:
    impl.validate = validate
    impl.build_site()
    patch_home_runtime()
    patch_r4_roundtrip_lifecycle()
    impl.base.validate_local_references()
    print("Finalized v1.6.1 consistency composition with enriched search binding and cancellable reversible VI/ES locale lifecycle")


if __name__ == "__main__":
    build_site()
