#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
LAB15 = SITE / "playgrounds" / "minimax-alpha-beta" / "index.html"


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


def main() -> int:
    build = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "build_site_v1_6_public.py")],
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
    files = sorted(p for p in SITE.rglob("*") if p.is_file())
    applets = sorted((SITE / "playgrounds").glob("*/index.html"))
    activities = sorted((SITE / "activities").glob("*.html"))
    checks.append(("v1.6 boundary is 58 files", len(files) == 58, {"files": len(files)}))
    checks.append(("v1.6 boundary is 15 applets", len(applets) == 15, {"applets": len(applets)}))
    checks.append(("Activity Pack canaries remain exactly three pages", len(activities) == 3, {"activities": [p.name for p in activities]}))

    manifest = json.loads((SITE / "applets.json").read_text(encoding="utf-8"))
    checks.append(("public manifest contains fifteen unique applets with Lab 15", len(manifest) == 15 and len({x["slug"] for x in manifest}) == 15 and manifest[-1]["slug"] == "minimax-alpha-beta", {"slugs": [x["slug"] for x in manifest]}))

    bad_analytics = []
    for p in sorted(SITE.rglob("*.html")):
        s = p.read_text(encoding="utf-8")
        if s.count('data-ai-playgrounds-analytics="v1.6.0"') != 1 or 'data-ai-playgrounds-analytics="v1.5.1"' in s:
            bad_analytics.append(p.relative_to(SITE).as_posix())
    checks.append(("v1.6 analytics is exactly once on every public HTML page", not bad_analytics, {"bad": bad_analytics}))

    version_bad = []
    for p in applets:
        if 'name="ai-playgrounds-version" content="1.6.0"' not in p.read_text(encoding="utf-8"):
            version_bad.append(p.parent.name)
    checks.append(("all fifteen applets expose v1.6 provenance", not version_bad, {"bad": version_bad}))

    landing = (SITE / "index.html").read_text(encoding="utf-8")
    curriculum = (SITE / "curriculum.html").read_text(encoding="utf-8")
    teacher = (SITE / "teacher-pack.html").read_text(encoding="utf-8")
    sitemap = (SITE / "sitemap.xml").read_text(encoding="utf-8")
    foundations = curriculum[:curriculum.find("</tbody>")]
    checks.append(("landing exposes fifteen labs including Lab 15", "15 interactive labs" in landing and "minimax-alpha-beta" in landing, {}))
    checks.append(("curriculum has thirteen Foundations rows and fifteen applet cards", curriculum.count('class="order-dot"') == 13 and curriculum.count('class="applet-card"') == 15, {"rows": curriculum.count('class="order-dot"'), "cards": curriculum.count('class="applet-card"')}))
    checks.append(("Foundations table contains Lab 15 but not the two modern/boundary labs", "minimax-alpha-beta" in foundations and "transformer-language-model" not in foundations and "agent-tool-context" not in foundations, {}))
    checks.append(("Teacher Pack exposes 13 Foundations + 2 Modern and Lab 15", "thirteen Foundations/course-track labs" in teacher and "minimax-alpha-beta" in teacher, {}))
    checks.append(("sitemap exposes Lab 15", "playgrounds/minimax-alpha-beta/" in sitemap, {}))

    lab = LAB15.read_text(encoding="utf-8")
    checks.append(("Lab 15 remains one self-contained minimax/alpha-beta artifact", lab.count("function minimax(") == 1 and lab.count("function alphaBeta(") == 1 and all(token not in lab for token in ("fetch(", "XMLHttpRequest", "WebSocket", "EventSource", "<script src=")), {}))
    checks.append(("Lab 15 retains multilingual, public-shell, and version contracts", all(marker in lab for marker in ("R6-Multilingual", "window.Lab15Localization", "lab15-v16-public-shell", 'name="ai-playgrounds-version" content="1.6.0"')), {}))

    page_errors: list[str] = []
    console_errors: list[str] = []
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("Playwright is required") from exc

    with sync_playwright() as p:
        browser = launch(p)
        try:
            context = browser.new_context(viewport={"width": 1100, "height": 900})
            page = context.new_page()
            page.on("pageerror", lambda exc: page_errors.append(f"desktop: {exc}"))
            page.on("console", lambda msg: console_errors.append(f"desktop: {msg.text}") if msg.type == "error" else None)
            page.goto(LAB15.resolve().as_uri() + "?lang=en", wait_until="domcontentloaded", timeout=30_000)
            page.wait_for_function("() => !!window.Lab15Prototype && !!window.Lab15Localization")

            page.select_option("#scenario", "first_prune")
            page.select_option("#algorithm", "alpha_beta")
            prune_index = page.evaluate("() => window.Lab15Prototype.getResult().trace.findIndex(e => e.event==='prune')")
            page.evaluate("i => window.Lab15Prototype.setTraceIndex(i)", prune_index)
            page.wait_for_timeout(80)
            cutoff = page.evaluate("() => ({state:window.Lab15Prototype.getVisibleState(), title:document.querySelector('#traceTitle').textContent, text:document.querySelector('#textState').textContent})")
            checks.append(("public Lab 15 exposes a real safe cutoff with B2 unevaluated", prune_index >= 0 and "B2" in cutoff["state"]["pruned"] and "B2" not in cutoff["state"]["visited"] and "prune" in cutoff["title"].lower() and "pruned_not_evaluated=B2" in cutoff["text"], cutoff))

            page.select_option("#scenario", "good_ordering")
            page.select_option("#algorithm", "alpha_beta")
            page.select_option("#order", "configured")
            good = page.evaluate("() => window.Lab15Prototype.getResult()")
            page.select_option("#order", "reverse")
            poor = page.evaluate("() => window.Lab15Prototype.getResult()")
            checks.append(("move ordering changes search work but not result", good["root_value"] == poor["root_value"] and good["selected_child"] == poor["selected_child"] and len(good["evaluated_leaves"]) < len(poor["evaluated_leaves"]), {"goodLeaves": len(good["evaluated_leaves"]), "poorLeaves": len(poor["evaluated_leaves"]), "root": good["root_value"]}))

            page.select_option("#challengeSelect", "greedy")
            page.click("#challengeBegin")
            page.select_option('[data-challenge-field="move"]', "B")
            page.click("#challengeLock")
            locked = page.locator('[data-challenge-field="move"]').is_disabled() and not page.locator("#challengeReveal").is_disabled()
            page.click("#challengeReveal")
            actual = page.locator("#challengeActual").inner_text()
            checks.append(("prediction is locked before reveal", locked, {}))
            checks.append(("greedy-trap challenge reveals the opponent-backup mechanism", "Prediction matched" in actual and "MIN can force A down" in actual, {"actual": actual}))

            page.select_option("#scenario", "first_prune")
            page.select_option("#algorithm", "alpha_beta")
            machine = page.evaluate("() => JSON.stringify({r:window.Lab15Prototype.getResult(),i:window.Lab15Prototype.getTraceIndex(),c:window.Lab15Prototype.getChallengeState()})")
            locale_ok = True
            for code in ("zh", "vi", "es", "en"):
                page.select_option("#lab15-language-select", code)
                page.wait_for_timeout(80)
                after = page.evaluate("() => JSON.stringify({r:window.Lab15Prototype.getResult(),i:window.Lab15Prototype.getTraceIndex(),c:window.Lab15Prototype.getChallengeState()})")
                locale_ok = locale_ok and after == machine
            checks.append(("locale switching is presentation-only", locale_ok, {}))
            context.close()

            for label, width, height in (("portrait", 390, 844), ("landscape", 844, 390), ("split", 640, 720)):
                context = browser.new_context(viewport={"width": width, "height": height}, has_touch=True, is_mobile=(label != "split"), reduced_motion="reduce")
                page = context.new_page()
                page.on("pageerror", lambda exc, label=label: page_errors.append(f"{label}: {exc}"))
                page.on("console", lambda msg, label=label: console_errors.append(f"{label}: {msg.text}") if msg.type == "error" else None)
                page.goto(LAB15.resolve().as_uri() + "?lang=es", wait_until="domcontentloaded", timeout=30_000)
                page.wait_for_function("() => !!window.Lab15Prototype")
                overflow = page.evaluate("() => document.documentElement.scrollWidth-innerWidth")
                checks.append((f"Lab 15 page contains at {width}x{height}", overflow <= 2, {"overflow": overflow}))
                context.close()

            context = browser.new_context(viewport={"width": 390, "height": 844}, reduced_motion="reduce")
            page = context.new_page()
            page.goto(LAB15.resolve().as_uri() + "?lang=vi", wait_until="domcontentloaded", timeout=30_000)
            page.wait_for_function("() => !!window.Lab15Prototype")
            page.evaluate("() => {document.documentElement.style.fontSize='200%'}")
            page.wait_for_timeout(80)
            overflow = page.evaluate("() => document.documentElement.scrollWidth-innerWidth")
            checks.append(("Lab 15 survives 200% text enlargement at 390px", overflow <= 2, {"overflow": overflow}))
            context.close()
        finally:
            browser.close()

    failures = [{"name": name, "detail": detail} for name, ok, detail in checks if not ok]
    payload = {
        "harness": "tools/test_v1_6_public_release.py",
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
