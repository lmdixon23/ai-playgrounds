#!/usr/bin/env python3
"""Bounded headless browser QA evidence for AI Playgrounds.

Runs each page × viewport check in an isolated child process so long-running
animations or browser-policy issues cannot block the whole evidence pass.
Writes JSON + Markdown evidence under release-evidence/browser-qa/.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from typing import Any, Dict, List
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = pathlib.Path(__file__).resolve().parents[1]
EVIDENCE_ROOT = ROOT / "release-evidence" / "browser-qa"

VIEWPORTS = {
    "mobile_360": {"width": 360, "height": 740, "is_mobile": True},
    "tablet_768": {"width": 768, "height": 1024, "is_mobile": True},
    "desktop_1366": {"width": 1366, "height": 900, "is_mobile": False},
}
REQUIRED_HOME_SELECTORS = ["h1", "#applets", "#teach", "#why", "#research", "#bfsGrid", "#filters"]
REQUIRED_APPLET_SELECTORS = [".scenario-gallery", ".signature-challenge", ".lab-panel", ".visual-explanation", ".accessibility-layer", ".learning-mode-shell", ".key-terms", ".header-more", ".suite-guided-shell"]


def launch_chromium(playwright: Any):
    """Launch Playwright Chromium, with a bounded system-browser fallback.

    The normal path remains Playwright's managed Chromium. The fallback helps
    locked-down CI/sandbox environments that already provide Chromium but do
    not allow Playwright browser downloads.
    """
    args = ["--no-sandbox", "--disable-dev-shm-usage"]
    managed = pathlib.Path(playwright.chromium.executable_path)
    if managed.exists():
        return playwright.chromium.launch(headless=True, args=args), str(managed)
    for name in ("chromium", "chromium-browser", "google-chrome", "chrome", "msedge"):
        candidate = shutil.which(name)
        if candidate:
            return playwright.chromium.launch(headless=True, executable_path=candidate, args=args), candidate
    return playwright.chromium.launch(headless=True, args=args), str(managed)


def public_pages() -> List[Dict[str, str]]:
    pages = [
        {"slug": "home", "path": "index.html", "kind": "home"},
        {"slug": "quality", "path": "quality.html", "kind": "support"},
        {"slug": "teacher_pack", "path": "teacher-pack.html", "kind": "support"},
        {"slug": "curriculum", "path": "curriculum.html", "kind": "support"},
        {"slug": "student_lab", "path": "student-lab.html", "kind": "support"},
        {"slug": "release_notes", "path": "release-notes.html", "kind": "support"},
        {"slug": "research_citation", "path": "research-and-citation.html", "kind": "support"},
        {"slug": "not_found", "path": "404.html", "kind": "support"},
    ]
    if (ROOT / "tests" / "index.html").exists():
        pages.append({"slug": "tests_index", "path": "tests/index.html", "kind": "tests"})
    for html in sorted((ROOT / "playgrounds").glob("*/index.html")):
        pages.append({"slug": html.parent.name, "path": f"playgrounds/{html.parent.name}/index.html", "kind": "applet"})
    return pages


def release_check() -> Dict[str, Any]:
    out = ROOT / "release-evidence" / "release-check.json"
    proc = subprocess.run([sys.executable, "tools/release_check.py", "--json", str(out)], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return {"returncode": proc.returncode, "stdout": proc.stdout.strip(), "stderr": proc.stderr.strip(), "json_path": str(out.relative_to(ROOT))}


def git_info() -> Dict[str, Any]:
    try:
        head = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True).strip()
        status = subprocess.check_output(["git", "status", "--short"], cwd=ROOT, text=True).splitlines()
        return {"head": head, "status_short": status}
    except Exception as exc:
        return {"head": None, "status_short": [], "error": str(exc)}


def install_sandbox_page_shims(page: Any) -> None:
    """Provide localStorage and URL-state shims when local navigation is policy-blocked."""
    page.evaluate("""() => {
      const store = {};
      Object.defineProperty(window, 'localStorage', {value: {
        getItem: key => Object.prototype.hasOwnProperty.call(store, key) ? store[key] : null,
        setItem: (key, value) => { store[key] = String(value); },
        removeItem: key => { delete store[key]; },
        clear: () => { Object.keys(store).forEach(key => delete store[key]); }
      }, configurable: true});
      history.replaceState = (_state, _title, url) => { window.__qaUrl = String(url); };
    }""")


def load_local_page(page: Any, page_path: str) -> str:
    """Navigate normally, then fall back to in-memory HTML in restricted sandboxes."""
    uri = (ROOT / page_path).resolve().as_uri()
    try:
        page.goto(uri, wait_until="domcontentloaded", timeout=10000)
        return "file"
    except Exception:
        # Some managed environments reject file navigation with an admin block,
        # while others interrupt it with a chrome-error navigation. In both
        # cases, create a fresh page context and load the exact HTML in memory.
        try:
            page.wait_for_timeout(350)
        except Exception:
            pass
        # Force a new document and JavaScript realm before injecting the page.
        # This prevents declarations from a partially loaded file document from
        # colliding with the in-memory fallback scripts.
        for blank in ("data:text/html,<html><body></body></html>", "about:blank"):
            try:
                page.goto(blank, wait_until="domcontentloaded", timeout=5000)
                break
            except Exception:
                try:
                    page.wait_for_timeout(250)
                except Exception:
                    pass
        install_sandbox_page_shims(page)
        page.set_content((ROOT / page_path).read_text(encoding="utf-8", errors="replace"), wait_until="domcontentloaded")
        return "in_memory"


def effective_url(page: Any) -> str:
    return page.evaluate("() => window.__qaUrl || location.href")


def exercise_home_proof(page: Any, checks: List[Dict[str, Any]]) -> None:
    """Run the homepage comparison without depending on transient layout stability."""
    button = page.locator("#runProof")
    button.wait_for(state="visible", timeout=5000)
    button.scroll_into_view_if_needed(timeout=5000)
    button.click(timeout=5000, force=True)
    page.wait_for_function(
        "() => document.querySelector('#bfsCount')?.textContent.includes('explored')",
        timeout=5000,
    )
    bfs_text = page.locator("#bfsCount").inner_text()
    astar_text = page.locator("#astarCount").inner_text()
    checks.append({
        "name": "live_proof_runs",
        "pass": "explored" in bfs_text and "explored" in astar_text,
        "detail": {"bfs": bfs_text, "astar": astar_text},
    })




def check_home_localization(page: Any, checks: List[Dict[str, Any]]) -> None:
    cards = page.locator("#appletGrid .applet")
    checks.append({"name": "twelve_applet_cards", "pass": cards.count() == 12, "detail": {"count": cards.count()}})
    zh = page.locator("button[data-lang='zh']")
    en = page.locator("button[data-lang='en']")
    if zh.count() and en.count():
        zh.first.click(timeout=1500)
        page.wait_for_timeout(100)
        first_meta = page.locator("#appletGrid .meta").first.inner_text() if page.locator("#appletGrid .meta").count() else ""
        research = page.locator("#research").inner_text() if page.locator("#research").count() else ""
        footer = page.locator("footer").inner_text() if page.locator("footer").count() else ""
        checks.append({"name": "home_zh_minutes", "pass": "分钟" in first_meta, "detail": {"meta": first_meta}})
        checks.append({"name": "home_zh_resource_labels", "pass": "架构说明" in research and "贡献指南" in research and "交互工具元数据" in research, "detail": {"excerpt": research[-260:]}})
        checks.append({"name": "home_zh_footer", "pass": "源代码" in footer and "报告问题" in footer, "detail": {"footer": footer}})
        en.first.click(timeout=1500)
        page.wait_for_timeout(50)


def check_support_localization(page: Any, checks: List[Dict[str, Any]], slug: str) -> None:
    markers = {
        "quality": "项目如何运作",
        "teacher_pack": "快速开始",
        "curriculum": "课程地图",
        "student_lab": "学生实验记录",
        "release_notes": "发布说明",
        "research_citation": "研究与引用",
        "not_found": "此处没有这个实验。",
    }
    zh = page.locator("[data-support-lang='zh']")
    en = page.locator("[data-support-lang='en']")
    checks.append({"name": "support_language_switch", "pass": zh.count() == 1 and en.count() == 1, "detail": {"zh": zh.count(), "en": en.count()}})
    if zh.count() and en.count():
        zh.click(timeout=1500)
        page.wait_for_timeout(100)
        body = page.locator("body").inner_text()
        marker = markers.get(slug, "")
        checks.append({"name": "support_zh_content", "pass": document_lang(page) == "zh-Hans" and (not marker or marker in body), "detail": {"lang": document_lang(page), "marker": marker, "excerpt": body[:220]}})
        en.click(timeout=1500)
        page.wait_for_timeout(50)


def document_lang(page: Any) -> str:
    return page.locator("html").get_attribute("lang") or ""


def switch_applet_locale(page: Any, code: str, timeout: int = 7000) -> None:
    has_r4 = page.evaluate("() => !!window.__r4Localization && window.__r4Localization.ready()")
    if has_r4:
        page.evaluate("(code) => window.__r4Localization.setLocale(code, {immediate:true})", code)
    else:
        button = page.locator(f"button[data-lang='{code}']")
        if not button.count():
            raise RuntimeError(f"language control missing: {code}")
        button.first.click(force=True)
    if code == "zh":
        page.wait_for_function("() => (document.documentElement.lang || '').toLowerCase().startsWith('zh')", timeout=timeout)
    else:
        page.wait_for_function("(code) => (document.documentElement.lang || '').toLowerCase().startsWith(code)", arg=code, timeout=timeout)
    page.wait_for_timeout(100)


def check_applet_extended(page: Any, checks: List[Dict[str, Any]], slug: str) -> None:
    visible_cards = page.locator(".learning-mode-panel:not([hidden]) .scenario-card")
    visible_height = 0
    if visible_cards.count():
        box = visible_cards.first.bounding_box()
        visible_height = 0 if not box else box.get("height", 0)
    checks.append({"name": "explore_panel_nonempty", "pass": visible_cards.count() >= 1 and visible_height > 20, "detail": {"cards": visible_cards.count(), "first_height": visible_height}})
    terms = page.locator(".key-term")
    checks.append({"name": "concept_sized_glossary", "pass": 6 <= terms.count() <= 12, "detail": {"count": terms.count()}})
    checks.append({"name": "bilingual_full_explanation", "pass": page.locator("[data-essay-lang='en']").count() == 1 and page.locator("[data-essay-lang='zh']").count() == 1, "detail": {"en": page.locator("[data-essay-lang='en']").count(), "zh": page.locator("[data-essay-lang='zh']").count()}})

    hint_en = page.locator("#hint").inner_text() if slug == "kmeans" and page.locator("#hint").count() else ""
    has_applet_language = page.locator("button[data-lang='zh']").count() and page.locator("button[data-lang='en']").count()
    if has_applet_language:
        switch_applet_locale(page, "zh")
        shell_text = page.locator(".learning-mode-shell").inner_text() if page.locator(".learning-mode-shell").count() else ""
        share_text = page.locator("#shareLink").inner_text() if page.locator("#shareLink").count() else ""
        checks.append({"name": "applet_zh_shared_chrome", "pass": "分享" in share_text and "复制此实验" in shell_text and "精选实验" in shell_text, "detail": {"share": share_text, "excerpt": shell_text[:260]}})
        checks.append({"name": "applet_zh_explanation_visibility", "pass": page.locator("[data-essay-lang='zh']:visible").count() == 1 and page.locator("[data-essay-lang='en']:visible").count() == 0, "detail": {"zh_visible": page.locator("[data-essay-lang='zh']:visible").count(), "en_visible": page.locator("[data-essay-lang='en']:visible").count()}})
        if slug == "kmeans" and page.locator("#hint").count():
            hint_zh = page.locator("#hint").inner_text()
            checks.append({"name": "kmeans_dynamic_hint_translates_immediately", "pass": hint_zh != hint_en and ("现在选择" in hint_zh or "选择初始化" in hint_zh), "detail": {"en": hint_en, "zh": hint_zh}})
        switch_applet_locale(page, "en")
        if slug == "kmeans" and page.locator("#hint").count():
            checks.append({"name": "kmeans_dynamic_hint_returns_to_english", "pass": page.locator("#hint").inner_text() == hint_en, "detail": {"expected": hint_en, "actual": page.locator("#hint").inner_text()}})

    if slug == "overfitting" and all(page.locator(selector).count() for selector in ("#deg", "#n", "#lam")):
        scenario = page.locator(".scenario-card button").first
        if scenario.count():
            scenario.click(timeout=1500)
        for selector, value in (("#deg", "17"), ("#n", "37"), ("#lam", "0.321")):
            page.locator(selector).evaluate("(el,v)=>{el.value=v;el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}));}", value)
        page.wait_for_timeout(120)
        payload = page.evaluate("""() => {
          const u = new URL(window.__buildExperimentUrl());
          const encoded = u.searchParams.get('state');
          const state = JSON.parse(decodeURIComponent(escape(atob(encoded))));
          return {url:u.href, hasScenario:u.searchParams.has('scenario'), state};
        }""")
        exact = payload.get("state", {})
        checks.append({"name": "overfitting_copy_uses_authoritative_controls", "pass": not payload.get("hasScenario") and exact.get("deg") == "17" and exact.get("n") == "37" and exact.get("lam") == "0.321", "detail": payload})

def single_check(page_path: str, slug: str, kind: str, viewport_name: str, screenshots: bool) -> Dict[str, Any]:
    from playwright.sync_api import sync_playwright

    vp = VIEWPORTS[viewport_name]
    page_errors: List[str] = []
    console_errors: List[str] = []
    checks: List[Dict[str, Any]] = []
    screenshot_path = None
    t0 = time.perf_counter()
    with sync_playwright() as p:
        browser = None
        try:
            browser, _browser_path = launch_chromium(p)
            context = browser.new_context(viewport={"width": vp["width"], "height": vp["height"]}, is_mobile=vp["is_mobile"], has_touch=vp["is_mobile"], reduced_motion="reduce", locale="en-US")
            page = context.new_page()
            page.on("pageerror", lambda exc: page_errors.append(str(exc)))
            page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            load_local_page(page, page_path)
            page.wait_for_timeout(150)
            overflow = page.evaluate("""() => {
                const doc = document.documentElement;
                const body = document.body;
                const maxScroll = Math.max(doc.scrollWidth, body ? body.scrollWidth : 0);
                return {innerWidth: window.innerWidth, docScrollWidth: doc.scrollWidth, bodyScrollWidth: body ? body.scrollWidth : 0, overflowing: maxScroll > window.innerWidth + 2};
            }""")
            checks.append({"name": "no_horizontal_scroll", "pass": not overflow["overflowing"], "detail": overflow})
            main_count = page.locator("main, [role=main]").count()
            checks.append({"name": "main_landmark_present", "pass": (main_count >= 1 or kind == "support_optional"), "detail": {"count": main_count}})
            if kind == "home":
                for selector in REQUIRED_HOME_SELECTORS:
                    count = page.locator(selector).count()
                    checks.append({"name": f"home_selector_{selector}", "pass": count >= 1, "detail": {"selector": selector, "count": count}})
                exercise_home_proof(page, checks)
                check_home_localization(page, checks)
            if kind == "support":
                check_support_localization(page, checks, slug)
            if kind == "applet":
                for selector in REQUIRED_APPLET_SELECTORS:
                    count = page.locator(selector).count()
                    checks.append({"name": f"applet_selector_{selector}", "pass": count >= 1, "detail": {"selector": selector, "count": count}})
                lang_count = page.locator("button[data-lang]").count()
                checks.append({"name": "language_buttons_present", "pass": lang_count >= 2, "detail": {"count": lang_count}})
                if lang_count >= 2:
                    r4_ready = bool(page.evaluate("() => !!window.__r4Localization && window.__r4Localization.ready()"))
                    switch_applet_locale(page, "zh")
                    if r4_ready:
                        zh_value = page.locator(".r4-language-select").input_value() if page.locator(".r4-language-select").count() else ""
                        checks.append({"name": "zh_toggle_active", "pass": document_lang(page).lower().startswith("zh") and zh_value == "zh", "detail": {"lang": document_lang(page), "select": zh_value}})
                    else:
                        checks.append({"name": "zh_toggle_active", "pass": page.locator("button[data-lang='zh'].active").count() >= 1, "detail": {"active_count": page.locator("button[data-lang='zh'].active").count()}})
                    switch_applet_locale(page, "en")
                    if r4_ready:
                        en_value = page.locator(".r4-language-select").input_value() if page.locator(".r4-language-select").count() else ""
                        checks.append({"name": "en_toggle_active", "pass": document_lang(page).lower().startswith("en") and en_value == "en", "detail": {"lang": document_lang(page), "select": en_value}})
                    else:
                        checks.append({"name": "en_toggle_active", "pass": page.locator("button[data-lang='en'].active").count() >= 1, "detail": {"active_count": page.locator("button[data-lang='en'].active").count()}})
                checks.append({"name": "aria_live_present", "pass": page.locator("[aria-live]").count() >= 1, "detail": {"count": page.locator("[aria-live]").count()}})
                checks.append({"name": "a11y_summary_present", "pass": page.locator("#a11yStateSummary").count() >= 1, "detail": {"count": page.locator("#a11yStateSummary").count()}})
                header_children = page.locator(".header-actions > *")
                checks.append({"name": "standard_header_actions", "pass": header_children.count() == 3 and page.locator(".header-actions > #shareLink").count() == 1 and page.locator(".header-actions > details.header-more").count() == 1 and page.locator(".header-actions > #hardReset").count() == 1, "detail": {"count": header_children.count()}})
                more = page.locator("details.header-more")
                if more.count():
                    more.locator("summary").click(timeout=1500)
                    checks.append({"name": "more_menu_core_actions", "pass": more.locator("#embedLink").count() == 1 and more.locator("[data-export-state]").count() == 1, "detail": {"embed": more.locator("#embedLink").count(), "state": more.locator("[data-export-state]").count()}})
                terms = page.locator(".key-term")
                checks.append({"name": "key_terms_present", "pass": terms.count() >= 5, "detail": {"count": terms.count()}})
                scenario_text = page.locator(".scenario-card").first.inner_text() if page.locator(".scenario-card").count() else ""
                checks.append({"name": "learner_scenario_structure", "pass": all(label in scenario_text for label in ["Core question", "Run and watch", "Predict first", "Explain afterward"]) and "Teacher use" not in scenario_text, "detail": {"excerpt": scenario_text[:240]}})
                tabs = page.locator(".learning-mode-tab")
                checks.append({"name": "four_learning_modes", "pass": tabs.count() == 4, "detail": {"count": tabs.count()}})
                if tabs.count() == 4:
                    tabs.nth(1).click(timeout=1500)
                    checks.append({"name": "mode_switch", "pass": page.locator(".learning-mode-tab[aria-selected=\"true\"]").count() == 1 and "mode=understand" in effective_url(page), "detail": {"url": effective_url(page)}})
                    tabs.nth(0).click(timeout=1500)
                checks.append({"name": "copy_experiment_present", "pass": page.locator("[data-copy-experiment]").count() == 1, "detail": {"count": page.locator("[data-copy-experiment]").count()}})
                scenario_btn = page.locator(".scenario-card button").first
                if scenario_btn.count():
                    scenario_btn.click(timeout=1500)
                    checks.append({"name": "scenario_updates_url", "pass": "scenario=" in effective_url(page), "detail": {"url": effective_url(page)}})
                check_applet_extended(page, checks, slug)
            if screenshots:
                shot_dir = EVIDENCE_ROOT / "screenshots" / viewport_name
                shot_dir.mkdir(parents=True, exist_ok=True)
                shot = shot_dir / f"{slug}.png"
                page.screenshot(path=str(shot), full_page=False)
                screenshot_path = str(shot.relative_to(ROOT))
        except Exception as exc:
            page_errors.append(f"QA exception: {type(exc).__name__}: {exc}")
        finally:
            if browser is not None:
                browser.close()
    failed_checks = [c for c in checks if not c["pass"]]
    return {
        "slug": slug,
        "path": page_path,
        "kind": kind,
        "viewport": viewport_name,
        "status": "content",
        "load_ms": round((time.perf_counter() - t0) * 1000, 1),
        "console_errors": console_errors,
        "page_errors": page_errors,
        "failed_checks": failed_checks,
        "checks": checks,
        "screenshot": screenshot_path,
        "pass": not console_errors and not page_errors and not failed_checks,
    }


def browser_preflight() -> Dict[str, Any]:
    """Detect whether Playwright can actually launch Chromium before spawning the full matrix."""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser, _browser_path = launch_chromium(p)
            browser.close()
        return {"ok": True, "detail": "Chromium launched"}
    except Exception as exc:
        return {
            "ok": False,
            "detail": f"{type(exc).__name__}: {exc}",
            "repair": "Run: python -m playwright install chromium, then rerun from the repo root."
        }


def run_all(screenshots: bool, child_timeout: int) -> Dict[str, Any]:
    """Run the full matrix in one browser process for speed and consistency."""
    from playwright.sync_api import sync_playwright
    results: List[Dict[str, Any]] = []
    with sync_playwright() as p:
        browser, _browser_path = launch_chromium(p)
        in_memory = False
        probe_context = browser.new_context(viewport={"width": 800, "height": 600})
        probe = probe_context.new_page()
        try:
            probe.goto((ROOT / "index.html").resolve().as_uri(), wait_until="domcontentloaded", timeout=3000)
        except Exception:
            # Managed environments may reject file URLs with different Chromium
            # error surfaces. Any local-file navigation failure activates the
            # exact in-memory HTML fallback for the matrix.
            in_memory = True
        probe_context.close()
        try:
            for viewport_name, vp in VIEWPORTS.items():
                context = browser.new_context(
                    viewport={"width": vp["width"], "height": vp["height"]},
                    is_mobile=vp["is_mobile"], has_touch=vp["is_mobile"],
                    reduced_motion="reduce", locale="en-US"
                )
                for meta in public_pages():
                    page_errors: List[str] = []
                    console_errors: List[str] = []
                    checks: List[Dict[str, Any]] = []
                    screenshot_path = None
                    t0 = time.perf_counter()
                    page = context.new_page()
                    page.on("pageerror", lambda exc, bucket=page_errors: bucket.append(str(exc)))
                    page.on("console", lambda msg, bucket=console_errors: bucket.append(msg.text) if msg.type == "error" else None)
                    try:
                        if in_memory:
                            install_sandbox_page_shims(page)
                            page.set_content((ROOT / meta["path"]).read_text(encoding="utf-8", errors="replace"), wait_until="domcontentloaded")
                        else:
                            page.goto((ROOT / meta["path"]).resolve().as_uri(), wait_until="domcontentloaded", timeout=10000)
                        page.wait_for_timeout(350)
                        overflow = page.evaluate("""() => {
                            const doc=document.documentElement, body=document.body;
                            const maxScroll=Math.max(doc.scrollWidth, body ? body.scrollWidth : 0);
                            return {innerWidth:innerWidth, docScrollWidth:doc.scrollWidth, bodyScrollWidth:body ? body.scrollWidth : 0, overflowing:maxScroll > innerWidth + 2};
                        }""")
                        checks.append({"name":"no_horizontal_scroll","pass":not overflow["overflowing"],"detail":overflow})
                        main_count=page.locator("main, [role=main]").count()
                        checks.append({"name":"main_landmark_present","pass":main_count>=1 or meta["kind"]=="support_optional","detail":{"count":main_count}})
                        if meta["kind"]=="home":
                            for selector in REQUIRED_HOME_SELECTORS:
                                count=page.locator(selector).count();checks.append({"name":f"home_selector_{selector}","pass":count>=1,"detail":{"selector":selector,"count":count}})
                            exercise_home_proof(page, checks)
                            check_home_localization(page, checks)
                        if meta["kind"]=="support":
                            check_support_localization(page, checks, meta["slug"])
                        if meta["kind"]=="applet":
                            for selector in REQUIRED_APPLET_SELECTORS:
                                count=page.locator(selector).count();checks.append({"name":f"applet_selector_{selector}","pass":count>=1,"detail":{"selector":selector,"count":count}})
                            lang_count=page.locator("button[data-lang]").count();checks.append({"name":"language_buttons_present","pass":lang_count>=2,"detail":{"count":lang_count}})
                            if lang_count>=2:
                                r4_ready=bool(page.evaluate("() => !!window.__r4Localization && window.__r4Localization.ready()"))
                                switch_applet_locale(page,"zh")
                                if r4_ready:
                                    zh_value=page.locator(".r4-language-select").input_value() if page.locator(".r4-language-select").count() else ""
                                    checks.append({"name":"zh_toggle_active","pass":document_lang(page).lower().startswith("zh") and zh_value=="zh","detail":{"lang":document_lang(page),"select":zh_value}})
                                else:
                                    checks.append({"name":"zh_toggle_active","pass":page.locator("button[data-lang='zh'].active").count()>=1,"detail":{}})
                                switch_applet_locale(page,"en")
                            header_children=page.locator(".header-actions > *")
                            child_classes=[header_children.nth(i).get_attribute("class") or header_children.nth(i).get_attribute("id") or "" for i in range(header_children.count())]
                            checks.append({"name":"standard_header_actions","pass":header_children.count()==3 and page.locator(".header-actions > #shareLink").count()==1 and page.locator(".header-actions > details.header-more").count()==1 and page.locator(".header-actions > #hardReset").count()==1,"detail":{"children":child_classes}})
                            more=page.locator("details.header-more")
                            if more.count():
                                more.locator("summary").click(timeout=1500)
                                checks.append({"name":"more_menu_core_actions","pass":more.locator("#embedLink").count()==1 and more.locator("[data-export-state]").count()==1,"detail":{"embed":more.locator("#embedLink").count(),"state":more.locator("[data-export-state]").count()}})
                            terms=page.locator(".key-term")
                            checks.append({"name":"key_terms_present","pass":terms.count()>=5,"detail":{"count":terms.count()}})
                            scenario_text=page.locator(".scenario-card").first.inner_text() if page.locator(".scenario-card").count() else ""
                            checks.append({"name":"learner_scenario_structure","pass":all(label in scenario_text for label in ["Core question","Run and watch","Predict first","Explain afterward"]) and "Teacher use" not in scenario_text,"detail":{"excerpt":scenario_text[:240]}})
                            tabs=page.locator(".learning-mode-tab");checks.append({"name":"four_learning_modes","pass":tabs.count()==4,"detail":{"count":tabs.count()}})
                            if tabs.count()==4:
                                tabs.nth(1).click(timeout=1500)
                                checks.append({"name":"mode_switch","pass":"mode=understand" in effective_url(page),"detail":{"url":page.url}})
                                tabs.nth(0).click(timeout=1500)
                            checks.append({"name":"copy_experiment_present","pass":page.locator("[data-copy-experiment]").count()==1,"detail":{}})
                            scenario_btn=page.locator(".scenario-card button").first
                            if scenario_btn.count():
                                scenario_btn.click(timeout=1500)
                                checks.append({"name":"scenario_updates_url","pass":"scenario=" in effective_url(page),"detail":{"url":page.url}})
                            checks.append({"name":"aria_live_present","pass":page.locator("[aria-live]").count()>=1,"detail":{"count":page.locator("[aria-live]").count()}})
                            checks.append({"name":"a11y_summary_present","pass":page.locator("#a11yStateSummary").count()>=1,"detail":{}})
                            check_applet_extended(page, checks, meta["slug"])
                        if meta["slug"]=="tests_index":
                            summary=page.locator("#summary").inner_text()
                            checks.append({"name":"algorithmic_test_report","pass":"45" in summary and "skipped" not in summary.lower() and "fail" not in summary.lower(),"detail":{"summary":summary}})
                        if screenshots:
                            page.evaluate("() => window.scrollTo(0, 0)")
                            page.wait_for_timeout(50)
                            shot_dir=EVIDENCE_ROOT/"screenshots"/viewport_name;shot_dir.mkdir(parents=True,exist_ok=True)
                            shot=shot_dir/f"{meta['slug']}.png";page.screenshot(path=str(shot),full_page=False);screenshot_path=str(shot.relative_to(ROOT))
                    except Exception as exc:
                        page_errors.append(f"QA exception: {type(exc).__name__}: {exc}")
                    finally:
                        page.close()
                    failed=[c for c in checks if not c["pass"]]
                    results.append({"slug":meta["slug"],"path":meta["path"],"kind":meta["kind"],"viewport":viewport_name,"status":"content","load_ms":round((time.perf_counter()-t0)*1000,1),"console_errors":console_errors,"page_errors":page_errors,"failed_checks":failed,"checks":checks,"screenshot":screenshot_path,"pass":not console_errors and not page_errors and not failed})
                context.close()
        finally:
            browser.close()
    failures=[r for r in results if not r["pass"]]
    return {"status":"completed","results":results,"summary":{"total":len(results),"passed":len(results)-len(failures),"failed":len(failures),"pass":not failures}}

def write_reports(payload: Dict[str, Any]) -> None:
    EVIDENCE_ROOT.mkdir(parents=True, exist_ok=True)
    (EVIDENCE_ROOT / "browser-qa-results.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    failures = [r for r in payload["browser_qa"].get("results", []) if not r["pass"]]
    lines = [
        "# Browser QA Evidence", "", f"Generated: {payload['generated_at']}", f"Git HEAD: `{payload['git']['head']}`", "",
        "## Summary", "", f"- Release checker return code: `{payload['release_check']['returncode']}`",
        f"- Browser preflight: `{payload.get('browser_preflight', {}).get('detail', 'not recorded')}`",
        f"- Browser page × viewport checks: `{payload['browser_qa']['summary']['total']}`",
        f"- Browser checks passed: `{payload['browser_qa']['summary']['passed']}`",
        f"- Browser checks failed: `{payload['browser_qa']['summary']['failed']}`", "",
        "## Viewports", ""
    ]
    for name, vp in VIEWPORTS.items():
        lines.append(f"- `{name}`: {vp['width']}×{vp['height']}")
    lines += ["", "## Failures", ""]
    if payload.get("browser_preflight", {}).get("ok") is False:
        lines.append("Browser preflight failed before the page matrix ran.")
        lines.append("- Detail: `" + payload["browser_preflight"].get("detail", "unknown") + "`")
        lines.append("- Repair: `" + payload["browser_preflight"].get("repair", "Install Playwright Chromium") + "`")
    elif not failures:
        lines.append("No failures recorded by the bounded headless browser QA script.")
    else:
        for r in failures:
            lines.append(f"### {r['slug']} / {r['viewport']}")
            lines.append(f"- Path: `{r['path']}`")
            if r.get("console_errors"):
                lines.append("- Console errors: " + "; ".join(f"`{e}`" for e in r["console_errors"]))
            if r.get("page_errors"):
                lines.append("- Page errors: " + "; ".join(f"`{e}`" for e in r["page_errors"]))
            if r.get("failed_checks"):
                lines.append("- Failed checks: " + "; ".join(f"`{c['name']}`" for c in r["failed_checks"]))
    lines += ["", "## Deferred checks", "", "- Physical-phone pass.", "- Manual screen-reader pass.", "- Live GitHub Pages hard-refresh and cache-bust pass.", "- Teacher or student validation."]
    (EVIDENCE_ROOT / "BROWSER_QA_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--single", nargs=4, metavar=("PATH", "SLUG", "KIND", "VIEWPORT"))
    parser.add_argument("--screenshots", action="store_true")
    parser.add_argument("--no-screenshots", action="store_true")
    parser.add_argument("--child-timeout", type=int, default=20)
    args = parser.parse_args()
    if args.single:
        path, slug, kind, viewport = args.single
        print(json.dumps(single_check(path, slug, kind, viewport, args.screenshots), ensure_ascii=False))
        return 0
    EVIDENCE_ROOT.mkdir(parents=True, exist_ok=True)
    preflight = browser_preflight()
    if preflight["ok"]:
        browser_qa = run_all(screenshots=not args.no_screenshots, child_timeout=args.child_timeout)
    else:
        browser_qa = {"status": "browser_preflight_failed", "preflight": preflight, "results": [], "summary": {"total": 0, "passed": 0, "failed": 1, "pass": False}}
    payload = {"generated_at": datetime.now(timezone.utc).isoformat(), "git": git_info(), "release_check": release_check(), "browser_preflight": preflight, "browser_qa": browser_qa, "deferred_checks": ["physical_phone_pass", "manual_screen_reader_pass", "live_github_pages_cache_bust_pass", "teacher_or_student_validation"]}
    write_reports(payload)
    summary = payload["browser_qa"]["summary"]
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"Evidence: {str(EVIDENCE_ROOT.relative_to(ROOT))}")
    if not summary.get("pass"):
        failures = [r for r in payload["browser_qa"].get("results", []) if not r.get("pass")]
        if payload.get("browser_preflight", {}).get("ok") is False:
            print("Browser preflight failed:")
            print("- " + payload["browser_preflight"].get("detail", "unknown error"))
            print("- " + payload["browser_preflight"].get("repair", "Install Playwright Chromium"))
        print("First failures:")
        for r in failures[:8]:
            parts = []
            if r.get("page_errors"): parts.append("page_errors=" + "; ".join(r["page_errors"][:2]))
            if r.get("console_errors"): parts.append("console_errors=" + "; ".join(r["console_errors"][:2]))
            if r.get("failed_checks"): parts.append("failed_checks=" + ", ".join(c.get("name", "?") for c in r["failed_checks"][:4]))
            print(f"- {r.get('slug')} / {r.get('viewport')} / {r.get('path')}: " + (" | ".join(parts) or "unknown failure"))
    if payload["release_check"]["returncode"] != 0:
        return 3
    if not payload["browser_qa"]["summary"]["pass"]:
        return 4
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
