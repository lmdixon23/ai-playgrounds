#!/usr/bin/env python3
from __future__ import annotations

import http.server
import json
import pathlib
import shutil
import socketserver
import subprocess
import sys
import threading
from contextlib import contextmanager

from modern_learning_v1_8_1 import LABS, LOCALES


ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
EVIDENCE = ROOT / "release-evidence" / "v1.8.1-modern-learner-parity-browser.json"
MODERN = tuple(LABS)


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, _format: str, *args) -> None:
        return


@contextmanager
def local_site_server():
    handler = lambda *args, **kwargs: QuietHandler(*args, directory=str(SITE), **kwargs)
    with socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler) as server:
        server.daemon_threads = True
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            yield f"http://127.0.0.1:{server.server_address[1]}"
        finally:
            server.shutdown()
            thread.join(timeout=2)


def launch(playwright):
    args = ["--no-sandbox", "--disable-dev-shm-usage"]
    managed = pathlib.Path(playwright.chromium.executable_path)
    if managed.exists():
        return playwright.chromium.launch(headless=True, args=args)
    for name in ("chromium", "chromium-browser", "google-chrome", "chrome"):
        candidate = shutil.which(name)
        if candidate:
            return playwright.chromium.launch(headless=True, executable_path=candidate, args=args)
    return playwright.chromium.launch(headless=True, args=args)


def ensure_build() -> None:
    home = SITE / "index.html"
    if home.is_file() and '<span class="site-version">v1.8.1</span>' in home.read_text(encoding="utf-8"):
        return
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "build_site_v1_8_1.py")], cwd=ROOT,
        text=True, capture_output=True, check=False, timeout=180,
    )
    if result.returncode:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise SystemExit(result.returncode)


def set_locale(page, locale: str) -> None:
    page.locator("#ap-standard-language-select").evaluate(
        "(el,value)=>{el.value=value;el.dispatchEvent(new Event('change',{bubbles:true}))}", locale
    )
    page.wait_for_function(
        "value=>document.documentElement.lang.toLowerCase().startsWith(value)", arg=locale, timeout=12_000
    )
    page.wait_for_timeout(80)


def navigate_ready(page, uri: str):
    response = page.goto(uri, wait_until="commit", timeout=25_000)
    page.wait_for_selector("#ap-standard-language-select", state="visible", timeout=25_000)
    page.wait_for_selector("#ap-modern-learning .scenario-card", state="visible", timeout=25_000)
    page.wait_for_selector("details[data-quick-assign-id]", state="attached", timeout=25_000)
    return response


CONTRAST_JS = r"""
([frontSelector, backSelector, frontProperty, backProperty]) => {
  const front=document.querySelector(frontSelector),back=document.querySelector(backSelector||frontSelector);
  if(!front||!back)return {ratio:0,missing:true};
  const parse=value=>{const m=String(value).match(/[\d.]+/g);return m?m.map(Number):null};
  const fg=parse(getComputedStyle(front)[frontProperty||'color'])?.slice(0,3);
  const background=(element,property)=>{
    if(property!=='backgroundColor')return parse(getComputedStyle(element)[property])?.slice(0,3);
    for(let node=element;node;node=node.parentElement){
      const value=parse(getComputedStyle(node).backgroundColor);
      if(value&&value.length>=3&&(value.length<4||value[3]>.001))return value.slice(0,3);
    }
    return null;
  };
  const bg=background(back,backProperty||'backgroundColor');
  if(!fg||!bg)return {ratio:0,fg,bg};
  const lum=rgb=>{const v=rgb.map(x=>x/255).map(x=>x<=.04045?x/12.92:Math.pow((x+.055)/1.055,2.4));return .2126*v[0]+.7152*v[1]+.0722*v[2]};
  const a=lum(fg),b=lum(bg),ratio=(Math.max(a,b)+.05)/(Math.min(a,b)+.05);
  return {ratio,fg,bg};
}
"""


def contrast(page, front: str, back: str | None = None, front_property: str = "color", back_property: str = "backgroundColor") -> dict:
    return page.evaluate(CONTRAST_JS, [front, back or front, front_property, back_property])


def write_evidence(payload: dict) -> None:
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    ensure_build()
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("Playwright is required for v1.8.1 browser QA") from exc

    checks: list[tuple[str, bool, object]] = []
    page_errors: list[str] = []
    console_errors: list[str] = []

    def check(name: str, ok: bool, detail: object = None) -> None:
        checks.append((name, bool(ok), {} if detail is None else detail))

    with local_site_server() as origin, sync_playwright() as p:
        browser = launch(p)
        try:
            for width, height in ((1280, 900), (390, 844)):
                context = browser.new_context(
                    viewport={"width": width, "height": height},
                    reduced_motion="reduce",
                    has_touch=width == 390,
                )
                page = context.new_page()
                page.on("pageerror", lambda exc: page_errors.append(str(exc)))
                page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
                for slug in MODERN:
                    print(f"v1.8.1 learner parity: {slug} at {width}px", flush=True)
                    response = navigate_ready(page, f"{origin}/playgrounds/{slug}/index.html?lang=en")
                    check(f"{slug}/{width}: local artifact HTTP 200", response is not None and response.status == 200, None if response is None else response.status)
                    check(f"{slug}/{width}: one featured experiment", page.locator(".ap-modern-featured:visible").count() == 1)
                    check(f"{slug}/{width}: five visible scenario cards", page.locator(".scenario-card:visible").count() == 5, page.locator(".scenario-card:visible").count())
                    check(f"{slug}/{width}: terminology primer visible", page.locator(".essay-primer:visible").count() == 1 and page.locator(".essay-primer-terms>div").count() >= 8)
                    check(f"{slug}/{width}: teacher sequence visible", page.locator(".for-teachers:visible").count() == 1)
                    reading_order = page.evaluate("()=>{const e=document.getElementById('ap-modern-learning'),q=document.querySelector('[data-quick-assign-id]'),x=document.getElementById('ap-modern-explanation');return !!(e&&q&&x&&(e.compareDocumentPosition(q)&Node.DOCUMENT_POSITION_FOLLOWING)&&(q.compareDocumentPosition(x)&Node.DOCUMENT_POSITION_FOLLOWING))}")
                    check(f"{slug}/{width}: scenario → Quick Assign → explanation reading order", reading_order)
                    check(f"{slug}/{width}: accessibility disclosure starts closed", page.locator("#ap-modern-a11y").count() == 1 and not page.locator("#ap-modern-a11y").evaluate("el=>el.open"))
                    check(f"{slug}/{width}: no accessibility state mirror", page.locator("#ap-modern-a11y-state").count() == 0)
                    check(f"{slug}/{width}: one canonical native text state", page.locator(f'#{LABS[slug]["state_id"]}').count() == 1)
                    qa = page.locator("details[data-quick-assign-id]")
                    snapshot = qa.locator("[data-qa-modern-state]")
                    snapshot_text = snapshot.text_content() or ""
                    check(f"{slug}/{width}: Quick Assign snapshot waits for request", "appears here" in snapshot_text.lower(), snapshot_text[:120])
                    check(f"{slug}/{width}: aligned header class families", all(page.locator(selector).count() == 1 for selector in (".header-prefs>.header-theme", ".header-prefs>.modern-lang-switch", ".header-actions>.header-reset")))
                    check(
                        f"{slug}/{width}: Share, Embed, JSON, and Reset are visible",
                        page.locator(".header-actions>#ap-modern-share:visible").count() == 1
                        and page.locator(".header-actions>#ap-modern-embed:visible").count() == 1
                        and page.locator(".header-actions>#ap-modern-settings-json:visible").count() == 1
                        and page.locator(".header-actions>#ap-standard-reset:visible").count() == 1
                        and page.locator("#ap-modern-more").count() == 0,
                    )
                    control_styles = page.locator("#ap-modern-share").evaluate("el=>{const s=getComputedStyle(el);return {height:el.getBoundingClientRect().height,radius:s.borderRadius,border:s.borderStyle}}")
                    check(f"{slug}/{width}: shared action geometry", control_styles["height"] >= (44 if width == 390 else 38) and control_styles["radius"] == "8px" and control_styles["border"] != "none", control_styles)
                    overflow = page.evaluate("()=>Math.max(document.documentElement.scrollWidth,document.body.scrollWidth)-innerWidth")
                    check(f"{slug}/{width}: no page-wide overflow", overflow <= 1, overflow)

                    if width == 1280:
                        qa.evaluate("el=>el.open=true")
                        qa.locator('[data-qa-answer="predict"]').fill("preserve this response")
                        first_english = page.locator(".scenario-card h3").first.inner_text()
                        for locale in LOCALES:
                            set_locale(page, locale)
                            check(f"{slug}/{locale}: five localized scenarios remain", page.locator(".scenario-card:visible").count() == 5)
                            check(f"{slug}/{locale}: learner response survives locale switch", qa.locator('[data-qa-answer="predict"]').input_value() == "preserve this response")
                            if locale != "en":
                                check(f"{slug}/{locale}: scenario teaching copy changes", page.locator(".scenario-card h3").first.inner_text() != first_english)
                        set_locale(page, "en")
                        for index, settings in enumerate(LABS[slug]["settings"]):
                            page.locator(f'[data-modern-scenario-card="{index}"] [data-modern-apply="{index}"]').evaluate("el=>el.click()")
                            page.wait_for_timeout(40)
                            for control_id, expected in settings.items():
                                actual = page.locator(f"#{control_id}").input_value()
                                check(f"{slug}: scenario {index + 1} applies {control_id}", actual == str(expected), {"expected": expected, "actual": actual})
                            check(f"{slug}: scenario {index + 1} marks the active card", page.locator(f'[data-modern-scenario-card="{index}"].applied').count() == 1)
                        qa.locator('[data-qa-action="refresh-state"]').click()
                        state_text = snapshot.inner_text().strip()
                        check(f"{slug}: manual Refresh captures mechanism state", bool(state_text) and "appears here" not in state_text.lower(), state_text[:180])
                context.close()

            dark_context = browser.new_context(viewport={"width": 1280, "height": 900}, reduced_motion="reduce", color_scheme="dark")
            dark_context.add_init_script("localStorage.setItem('theme','dark')")
            dark_page = dark_context.new_page()
            dark_page.on("pageerror", lambda exc: page_errors.append(str(exc)))
            dark_page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            for slug in MODERN:
                print(f"v1.8.1 dark contrast: {slug}", flush=True)
                navigate_ready(dark_page, f"{origin}/playgrounds/{slug}/index.html?lang=en")
                check(f"{slug}/dark: shared dark theme active", "ap-standard-dark" in (dark_page.locator("body").get_attribute("class") or ""))
                for label, front, back, fp, bp in (
                    ("header action", "#ap-modern-share", "#ap-modern-share", "color", "backgroundColor"),
                    ("scenario card", ".scenario-card", ".scenario-card", "color", "backgroundColor"),
                    ("essay heading", ".ap-modern-essay h2", ".ap-modern-essay h2", "color", "backgroundColor"),
                    ("scenario action", ".scenario-card button", ".scenario-card button", "color", "backgroundColor"),
                ):
                    result = contrast(dark_page, front, back, fp, bp)
                    check(f"{slug}/dark: {label} contrast ≥ 4.5", result.get("ratio", 0) >= 4.5, result)
                if slug == "transformer-language-model":
                    for label, selector in (("model boundary", ".boundary"), ("warning", ".warning"), ("masked cell", ".matrix td.masked")):
                        result = contrast(dark_page, selector)
                        check(f"{slug}/dark: {label} contrast ≥ 4.5", result.get("ratio", 0) >= 4.5, result)
                elif slug == "agent-tool-context":
                    result = contrast(dark_page, ".pill.good", ".pill.good")
                    check(f"{slug}/dark: semantic status contrast ≥ 4.5", result.get("ratio", 0) >= 4.5, result)
                else:
                    result = contrast(dark_page, ".node text", ".node circle", "fill", "fill")
                    check(f"{slug}/dark: SVG node text contrast ≥ 4.5", result.get("ratio", 0) >= 4.5, result)
                    result = contrast(dark_page, ".metric", ".metric")
                    check(f"{slug}/dark: metric contrast ≥ 4.5", result.get("ratio", 0) >= 4.5, result)
            dark_context.close()

            embed_context = browser.new_context(viewport={"width": 1024, "height": 768}, reduced_motion="reduce")
            embed_page = embed_context.new_page()
            for slug in MODERN:
                response = embed_page.goto(f"{origin}/playgrounds/{slug}/index.html?lang=en&embed=1", wait_until="commit", timeout=25_000)
                embed_page.wait_for_selector("main", state="visible", timeout=25_000)
                check(f"{slug}/embed: local artifact HTTP 200", response is not None and response.status == 200)
                check(f"{slug}/embed: mechanism remains visible", embed_page.locator("main:visible").count() == 1)
                check(f"{slug}/embed: teaching chrome is hidden", embed_page.locator(".ap-modern-curriculum:visible").count() == 0 and embed_page.locator(".ap-standard-header:visible").count() == 0)
            embed_context.close()
        finally:
            browser.close()

    failures = [{"name": name, "detail": detail} for name, ok, detail in checks if not ok]
    payload = {
        "harness": "tools/test_v1_8_1_modern_learner_parity_browser.py",
        "checks": len(checks),
        "passed": len(checks) - len(failures),
        "failed": len(failures),
        "page_errors": page_errors,
        "console_errors": console_errors,
        "pass": not failures and not page_errors and not console_errors,
        "failures": failures,
    }
    write_evidence(payload)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
