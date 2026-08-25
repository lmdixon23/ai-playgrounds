#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"


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


def parse_query(url: str) -> dict[str, list[str]]:
    return urllib.parse.parse_qs(urllib.parse.urlsplit(url).query, keep_blank_values=True)


def main() -> int:
    build = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "build_site_v1_5_1.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if build.returncode:
        print(build.stdout)
        print(build.stderr, file=sys.stderr)
        return build.returncode

    checks: list[tuple[str, bool, object]] = []
    page_errors: list[str] = []
    console_errors: list[str] = []

    files = sorted(path for path in SITE.rglob("*") if path.is_file())
    html_pages = sorted(path for path in SITE.rglob("*.html") if path.is_file())
    applets = sorted((SITE / "playgrounds").glob("*/index.html"))
    activities = sorted((SITE / "activities").glob("*.html"))
    checks.append(("v1.5.1 file boundary", len(files) == 57, {"files": len(files)}))
    checks.append(("v1.5.1 applet boundary", len(applets) == 14, {"applets": len(applets)}))
    checks.append(("Activity Pack canary boundary", [p.name for p in activities] == ["cnn-1.html", "index.html", "nn-1.html"], {"activities": [p.name for p in activities]}))
    analytics_missing = []
    analytics_duplicate = []
    for path in html_pages:
        source = path.read_text(encoding="utf-8")
        count = source.count('data-ai-playgrounds-analytics="v1.5.1"')
        if count == 0:
            analytics_missing.append(path.relative_to(SITE).as_posix())
        elif count != 1:
            analytics_duplicate.append((path.relative_to(SITE).as_posix(), count))
    checks.append(("analytics covers every public HTML page exactly once", not analytics_missing and not analytics_duplicate, {"htmlPages": len(html_pages), "missing": analytics_missing, "duplicates": analytics_duplicate}))

    landing = (SITE / "index.html").read_text(encoding="utf-8")
    checks.append(("landing metadata reflects fourteen multilingual labs", "14 interactive labs" in landing and "Fourteen multilingual" in landing and '"inLanguage":["en","zh","vi","es"]' in landing, {}))
    teacher = (SITE / "teacher-pack.html").read_text(encoding="utf-8")
    checks.append(("Teacher Pack exposes Activity Pack canaries and course/modern split", "NN-1" in teacher and "CNN-1" in teacher and "twelve Foundations/course-track labs plus two Modern AI extensions" in teacher, {}))

    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("Playwright is required") from exc

    with sync_playwright() as p:
        browser = launch(p)
        try:
            # KNN: state-recovery contract. A tap just outside the tiny visible point
            # target but within the 22px tolerance must select a predicted neighbor,
            # not silently relocate the query and clear progress.
            context = browser.new_context(viewport={"width": 390, "height": 844}, has_touch=True, is_mobile=True)
            page = context.new_page()
            page.on("pageerror", lambda exc: page_errors.append(f"knn: {exc}"))
            page.on("console", lambda msg: console_errors.append(f"knn: {msg.text}") if msg.type == "error" else None)
            page.goto((SITE / "playgrounds" / "knn-classifier" / "index.html").resolve().as_uri(), wait_until="load", timeout=10_000)
            page.locator('[data-suite-mode="guided"]').click(force=True)
            page.locator("#guidedStart").click(force=True)
            cv = page.locator("#cv").bounding_box()
            checks.append(("KNN canvas available", cv is not None, {"box": cv}))
            if cv:
                page.locator("#cv").evaluate("""(cv,pos) => {
                    const r=cv.getBoundingClientRect();
                    cv.dispatchEvent(new MouseEvent('click',{
                        bubbles:true,cancelable:true,view:window,
                        clientX:r.left+r.width*pos.x,
                        clientY:r.top+r.height*pos.y
                    }));
                }""", {"x": 0.52, "y": 0.52})
                page.wait_for_timeout(30)
                query_status = page.locator("#guidedStatus").inner_text()
                checks.append(("KNN query placement advances challenge", "Step 2" in query_status, {"status": query_status}))
                point = page.locator('[data-role="point"]').first.bounding_box()
                if point:
                    # Exercise the canvas handler itself at a location that misses the
                    # old ~12px visible target but remains inside the new 22px CSS
                    # tolerance. This reproduces an imprecise touch without letting
                    # an overlay element intercept the event.
                    page.locator("#cv").evaluate("""(cv,pos) => {
                        cv.dispatchEvent(new MouseEvent('click',{
                            bubbles:true,cancelable:true,view:window,
                            clientX:pos.x,clientY:pos.y
                        }));
                    }""", {
                        "x": point["x"] + point["width"] / 2 + 13,
                        "y": point["y"] + point["height"] / 2,
                    })
                    page.wait_for_timeout(40)
                    status = page.locator("#guidedStatus").inner_text()
                    checks.append(("KNN near-miss selects rather than resets", "(1/" in status, {"status": status, "point": point}))
                else:
                    checks.append(("KNN near-miss selects rather than resets", False, {"error": "no point hit target"}))
            context.close()

            # Bayesian Network: all four inference choices remain visible at 390px in
            # longer locales; component-level clipping is checked rather than only page overflow.
            context = browser.new_context(viewport={"width": 390, "height": 844}, has_touch=True, is_mobile=True)
            page = context.new_page()
            page.on("pageerror", lambda exc: page_errors.append(f"bayes: {exc}"))
            page.on("console", lambda msg: console_errors.append(f"bayes: {msg.text}") if msg.type == "error" else None)
            page.goto((SITE / "playgrounds" / "bayes-network" / "index.html").resolve().as_uri(), wait_until="load", timeout=10_000)
            for locale in ("en", "zh", "vi", "es"):
                ready = page.evaluate("() => !!window.__r4Localization && window.__r4Localization.ready()")
                if ready:
                    page.evaluate("code => window.__r4Localization.setLocale(code,{immediate:true})", locale)
                    page.wait_for_timeout(80)
                boxes = page.evaluate("""() => {
                  const group=document.querySelector('.method-tabs');
                  if(!group)return null;
                  const g=group.getBoundingClientRect();
                  return {group:{left:g.left,right:g.right,width:g.width},buttons:[...group.querySelectorAll('button')].map(b=>{const r=b.getBoundingClientRect();return {left:r.left,right:r.right,width:r.width,text:b.textContent.trim()}})};
                }""")
                ok = bool(boxes) and len(boxes["buttons"]) == 4 and all(b["left"] >= boxes["group"]["left"] - 1 and b["right"] <= boxes["group"]["right"] + 1 and b["width"] >= 70 for b in boxes["buttons"])
                checks.append((f"Bayesian method choices fit at 390px ({locale})", ok, boxes))
            context.close()

            # Tiny NN: short landscape must reflow the history transport rather than
            # widen the page beyond the viewport.
            context = browser.new_context(viewport={"width": 844, "height": 390}, has_touch=True, is_mobile=True)
            page = context.new_page()
            page.on("pageerror", lambda exc: page_errors.append(f"neural-landscape: {exc}"))
            page.on("console", lambda msg: console_errors.append(f"neural-landscape: {msg.text}") if msg.type == "error" else None)
            page.goto((SITE / "playgrounds" / "neural-network" / "index.html").resolve().as_uri(), wait_until="load", timeout=10_000)
            nn_layout = page.evaluate("""() => {const doc=document.documentElement,g=document.querySelector('#nnScrubGroup');const r=g?.getBoundingClientRect();return {innerWidth,scrollWidth:doc.scrollWidth,group:r?{left:r.left,right:r.right,width:r.width}:null};}""")
            ok = nn_layout["scrollWidth"] <= nn_layout["innerWidth"] + 2 and (not nn_layout["group"] or nn_layout["group"]["right"] <= nn_layout["innerWidth"] + 2)
            checks.append(("Tiny Neural Network transport fits 844x390", ok, nn_layout))
            context.close()

            # Text enlargement stress: 200% root text on every applet at a 390px viewport.
            context = browser.new_context(viewport={"width": 390, "height": 844}, has_touch=True, is_mobile=True, reduced_motion="reduce")
            for applet in applets:
                page = context.new_page()
                slug = applet.parent.name
                page.on("pageerror", lambda exc, slug=slug: page_errors.append(f"{slug}-text200: {exc}"))
                page.on("console", lambda msg, slug=slug: console_errors.append(f"{slug}-text200: {msg.text}") if msg.type == "error" else None)
                page.goto(applet.resolve().as_uri(), wait_until="domcontentloaded", timeout=10_000)
                page.evaluate("() => { document.documentElement.style.fontSize='200%'; }")
                page.wait_for_timeout(60)
                overflow = page.evaluate("() => Math.max(document.documentElement.scrollWidth,document.body.scrollWidth)-innerWidth")
                checks.append((f"{slug} survives 200% text enlargement at 390px", overflow <= 2, {"overflow": overflow}))
                page.close()
            context.close()

            # Activity Pack state/recovery contract over a stable HTTP-like origin.
            activity_html = (SITE / "activities" / "nn-1.html").read_text(encoding="utf-8")
            context = browser.new_context(viewport={"width": 1024, "height": 768})
            page = context.new_page()
            page.route("http://activity.test/nn-1.html", lambda route: route.fulfill(status=200, content_type="text/html", body=activity_html))
            page.goto("http://activity.test/nn-1.html", wait_until="load")
            page.fill("#r1p", "My saved prediction")
            page.wait_for_timeout(40)
            page.reload(wait_until="load")
            restored = page.input_value("#r1p")
            checks.append(("NN-1 autosave survives reload", restored == "My saved prediction", {"value": restored}))
            page.once("dialog", lambda dialog: dialog.accept())
            page.click("#clearBtn")
            page.wait_for_timeout(30)
            cleared = page.input_value("#r1p")
            focused = page.evaluate("() => document.activeElement && document.activeElement.id")
            checks.append(("NN-1 clear is guarded and returns focus to first response", cleared == "" and focused == "r1p", {"cleared": cleared, "focused": focused}))
            context.close()

            # GoatCounter contract on canonical origin: page title + canonical path +
            # campaign query, then a true event with e=1. No request should be emitted
            # when analytics=off.
            activity_html = (SITE / "activities" / "nn-1.html").read_text(encoding="utf-8")
            captured: list[str] = []
            context = browser.new_context(viewport={"width": 1024, "height": 768})
            page = context.new_page()
            def canonical(route):
                route.fulfill(status=200, content_type="text/html", body=activity_html)
            def counter(route, request):
                captured.append(request.url)
                route.fulfill(status=200, content_type="image/gif", body=b"GIF89a")
            page.route("https://lmdixon23.github.io/ai-playgrounds/activities/nn-1.html**", canonical)
            page.route("https://lmdixon23.goatcounter.com/count**", counter)
            page.goto("https://lmdixon23.github.io/ai-playgrounds/activities/nn-1.html?ap_src=linkedin", wait_until="load")
            page.wait_for_timeout(100)
            page.evaluate("() => window.aiPlaygroundsAnalytics.count('qa/check','QA check')")
            page.wait_for_timeout(100)
            parsed = [parse_query(url) for url in captured]
            pageviews = [q for q in parsed if q.get("e") != ["1"]]
            events = [q for q in parsed if q.get("e") == ["1"]]
            pageview_ok = any(q.get("p") == ["/ai-playgrounds/activities/nn-1.html"] and q.get("t", [""])[0].startswith("NN-1") and "utm_campaign=ai-playgrounds" in urllib.parse.unquote(q.get("q", [""])[0]) and "utm_source=linkedin" in urllib.parse.unquote(q.get("q", [""])[0]) for q in pageviews)
            event_ok = any(q.get("p") == ["event/qa/check"] and q.get("e") == ["1"] and q.get("t") == ["QA check"] for q in events)
            checks.append(("GoatCounter pageview uses canonical path, title, and campaign semantics", pageview_ok, {"captured": captured}))
            checks.append(("GoatCounter synthetic interactions are true events", event_ok, {"events": events}))
            context.close()

            captured_off: list[str] = []
            context = browser.new_context(viewport={"width": 1024, "height": 768})
            page = context.new_page()
            page.route("https://lmdixon23.github.io/ai-playgrounds/activities/nn-1.html**", canonical)
            page.route("https://lmdixon23.goatcounter.com/count**", lambda route, request: (captured_off.append(request.url), route.fulfill(status=200, content_type="image/gif", body=b"GIF89a")))
            page.goto("https://lmdixon23.github.io/ai-playgrounds/activities/nn-1.html?analytics=off", wait_until="load")
            page.wait_for_timeout(100)
            checks.append(("analytics=off sends no GoatCounter request", not captured_off, {"captured": captured_off}))
            context.close()
        finally:
            browser.close()

    failures = [{"name": name, "detail": detail} for name, ok, detail in checks if not ok]
    payload = {
        "harness": "tools/test_v1_5_1_hci_adoption.py",
        "checks": len(checks),
        "passed": len(checks) - len(failures),
        "failed": len(failures),
        "page_errors": page_errors,
        "console_errors": console_errors,
        "pass": not failures and not page_errors and not console_errors,
        "failures": failures,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
