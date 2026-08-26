#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
MODERN = ("transformer-language-model", "agent-tool-context", "minimax-alpha-beta")
ORIGINAL = (
    "search-pathfinding", "hill-climbing", "wumpus-world", "cnf-sat",
    "bayes-classifier", "bayes-network", "knn-classifier", "overfitting",
    "neural-network", "kmeans", "convolution", "q-learning-gridworld",
)


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
        [sys.executable, str(ROOT / "tools" / "build_site_v1_7_1_modern_parity.py")],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    if build.returncode:
        print(build.stdout)
        print(build.stderr, file=sys.stderr)
        return build.returncode

    checks: list[tuple[str, bool, object]] = []
    def check(name: str, ok: bool, detail: object = None):
        checks.append((name, bool(ok), detail))

    for slug in ORIGINAL:
        source = (SITE / "playgrounds" / slug / "index.html").read_text(encoding="utf-8")
        check(f"original lab untouched by parity wrapper: {slug}", "v171-modern-parity" not in source)

    required = (
        'class="ap-modern-skip"', 'class="ap-standard-header page-header"',
        'id="ap-modern-share"', 'id="ap-modern-embed"', 'class="ap-modern-tldr"',
        'id="ap-modern-key-terms"', 'id="ap-modern-a11y"', 'id="ap-modern-fidelity"',
        'class="ap-standard-footer ap-modern-rich-footer"', 'id="v171-modern-parity-runtime"',
    )
    for slug in MODERN:
        source = (SITE / "playgrounds" / slug / "index.html").read_text(encoding="utf-8")
        for marker in required:
            check(f"{slug}: {marker}", marker in source)
        check(f"{slug}: exactly one Quick Assign surface", source.count("data-quick-assign-id=") == 1)
        check(f"{slug}: no second assignment architecture", "Student response packet" not in source)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("Playwright is required for modern parity QA") from exc

    page_errors: list[str] = []
    console_errors: list[str] = []
    with sync_playwright() as p:
        browser = launch(p)
        try:
            for width, height in ((1280, 900), (390, 844)):
                context = browser.new_context(viewport={"width": width, "height": height}, reduced_motion="reduce")
                page = context.new_page()
                page.on("pageerror", lambda exc: page_errors.append(str(exc)))
                page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
                for slug in MODERN:
                    uri = (SITE / "playgrounds" / slug / "index.html").resolve().as_uri() + "?lang=en"
                    page.goto(uri, wait_until="load", timeout=20_000)
                    page.wait_for_selector("#ap-standard-language-select", timeout=5_000)
                    check(f"{slug} {width}: one visible public H1", page.locator("h1:visible").count() == 1, page.locator("h1:visible").count())
                    check(f"{slug} {width}: skip target exists", page.locator("#ap-modern-interactive-start").count() == 1)
                    check(f"{slug} {width}: share and embed visible", page.locator("#ap-modern-share:visible").count() == 1 and page.locator("#ap-modern-embed:visible").count() == 1)
                    check(f"{slug} {width}: orientation visible", page.locator(".ap-modern-tldr:visible").count() == 1)
                    check(f"{slug} {width}: support panels exist", page.locator("#ap-modern-key-terms").count() == 1 and page.locator("#ap-modern-a11y").count() == 1 and page.locator("#ap-modern-fidelity").count() == 1)
                    overflow = page.evaluate("()=>Math.max(document.documentElement.scrollWidth,document.body.scrollWidth)-innerWidth")
                    check(f"{slug} {width}: page containment", overflow <= 1, overflow)

                    original_title = page.locator("#ap-standard-title").inner_text()
                    original_big = page.locator(".ap-modern-tldr").inner_text()
                    for locale in ("vi", "es"):
                        page.select_option("#ap-standard-language-select", locale)
                        page.wait_for_timeout(100)
                        check(f"{slug}: parity copy switches to {locale}", page.locator(".ap-modern-tldr").inner_text() != original_big)
                        page.select_option("#ap-standard-language-select", "en")
                        page.wait_for_timeout(100)
                        check(f"{slug}: EN title restores after {locale}", page.locator("#ap-standard-title").inner_text() == original_title)
                        check(f"{slug}: EN parity copy restores after {locale}", page.locator(".ap-modern-tldr").inner_text() == original_big)

                context.close()

            embed_context = browser.new_context(viewport={"width": 1024, "height": 768}, reduced_motion="reduce")
            embed_page = embed_context.new_page()
            for slug in MODERN:
                uri = (SITE / "playgrounds" / slug / "index.html").resolve().as_uri() + "?lang=en&embed=1"
                embed_page.goto(uri, wait_until="load", timeout=20_000)
                embed_page.wait_for_timeout(50)
                check(f"{slug}: embed mode activates", "embed-mode" in (embed_page.locator("body").get_attribute("class") or ""))
                check(f"{slug}: embed hides suite header", embed_page.locator(".ap-standard-header:visible").count() == 0)
                check(f"{slug}: embed keeps mechanism visible", embed_page.locator("main:visible").count() == 1)
            embed_context.close()
        finally:
            browser.close()

    failures = [{"name": n, "detail": d} for n, ok, d in checks if not ok]
    payload = {
        "harness": "tools/test_v1_7_1_modern_parity.py",
        "checks": len(checks),
        "passed": len(checks) - len(failures),
        "failed": len(failures),
        "page_errors": page_errors,
        "console_errors": console_errors,
        "pass": not failures and not page_errors and not console_errors,
        "failures": failures,
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
