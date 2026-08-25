#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys

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


def overflow(page) -> dict:
    return page.evaluate("""() => {
      const d=document.documentElement,b=document.body;
      const scroll=Math.max(d.scrollWidth,b?b.scrollWidth:0);
      return {innerWidth,scrollWidth:scroll,overflow:scroll-innerWidth};
    }""")


def main() -> int:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "build_site_v1_5_1.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode:
        print(proc.stdout)
        print(proc.stderr, file=sys.stderr)
        return proc.returncode

    from playwright.sync_api import sync_playwright

    results: list[dict] = []
    page_errors: list[str] = []
    console_errors: list[str] = []

    def record(name: str, passed: bool, detail=None):
        results.append({"name": name, "pass": bool(passed), "detail": detail})

    with sync_playwright() as p:
        browser = launch(p)
        try:
            # Narrow desktop / split-screen canary across all fourteen applets.
            context = browser.new_context(viewport={"width": 640, "height": 720}, reduced_motion="reduce")
            for applet in sorted((SITE / "playgrounds").glob("*/index.html")):
                slug = applet.parent.name
                page = context.new_page()
                page.on("pageerror", lambda exc, slug=slug: page_errors.append(f"{slug}@640: {exc}"))
                page.on("console", lambda msg, slug=slug: console_errors.append(f"{slug}@640: {msg.text}") if msg.type == "error" else None)
                page.goto(applet.resolve().as_uri(), wait_until="domcontentloaded", timeout=10_000)
                page.wait_for_timeout(80)
                metric = overflow(page)
                record(f"{slug} fits 640px split-screen", metric["overflow"] <= 2, metric)
                page.close()
            context.close()

            # Both Activity Packs must retain their complete learner workflow on phone
            # portrait and short phone landscape. Associated labels are required for
            # every written response field, and toolbar actions keep 44px targets.
            for activity in ("nn-1", "cnn-1"):
                html_path = SITE / "activities" / f"{activity}.html"
                for label, width, height in (("portrait", 390, 844), ("landscape", 844, 390)):
                    context = browser.new_context(viewport={"width": width, "height": height}, has_touch=True, is_mobile=True, reduced_motion="reduce")
                    page = context.new_page()
                    page.on("pageerror", lambda exc, a=activity, label=label: page_errors.append(f"{a}@{label}: {exc}"))
                    page.on("console", lambda msg, a=activity, label=label: console_errors.append(f"{a}@{label}: {msg.text}") if msg.type == "error" else None)
                    page.goto(html_path.resolve().as_uri(), wait_until="load", timeout=10_000)
                    metric = overflow(page)
                    record(f"{activity} fits phone {label}", metric["overflow"] <= 2, metric)
                    semantics = page.evaluate("""() => ({
                      textareas:[...document.querySelectorAll('textarea')].map(t=>({id:t.id,label:!!document.querySelector(`label[for="${CSS.escape(t.id)}"]`)})),
                      controls:[...document.querySelectorAll('.toolbar button,.toolbar a.button')].map(el=>({text:el.textContent.trim(),height:el.getBoundingClientRect().height}))
                    })""")
                    record(
                        f"{activity} response fields have explicit labels ({label})",
                        bool(semantics["textareas"]) and all(item["id"] and item["label"] for item in semantics["textareas"]),
                        semantics["textareas"],
                    )
                    record(
                        f"{activity} toolbar targets are at least 44px ({label})",
                        bool(semantics["controls"]) and all(item["height"] >= 43.5 for item in semantics["controls"]),
                        semantics["controls"],
                    )
                    context.close()

            # CNN-1 receives the same PWP-derived persistence/recovery proof already
            # exercised for NN-1 in the primary v1.5.1 HCI gate.
            activity_html = (SITE / "activities" / "cnn-1.html").read_text(encoding="utf-8")
            context = browser.new_context(viewport={"width": 1024, "height": 768})
            page = context.new_page()
            page.route("http://activity.test/cnn-1.html", lambda route: route.fulfill(status=200, content_type="text/html", body=activity_html))
            page.goto("http://activity.test/cnn-1.html", wait_until="load")
            page.fill("#r1p", "Saved CNN prediction")
            page.wait_for_timeout(40)
            page.reload(wait_until="load")
            record("CNN-1 autosave survives reload", page.input_value("#r1p") == "Saved CNN prediction", {"value": page.input_value("#r1p")})
            page.once("dialog", lambda dialog: dialog.accept())
            page.click("#clearBtn")
            page.wait_for_timeout(30)
            focused = page.evaluate("() => document.activeElement && document.activeElement.id")
            record("CNN-1 guarded clear removes local response and returns focus", page.input_value("#r1p") == "" and focused == "r1p", {"focused": focused})
            context.close()
        finally:
            browser.close()

    failures = [item for item in results if not item["pass"]]
    payload = {
        "harness": "tools/test_v1_5_1_hci_extended.py",
        "checks": len(results),
        "passed": len(results) - len(failures),
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
