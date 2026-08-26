#!/usr/bin/env python3
from __future__ import annotations

import functools
import http.server
import pathlib
import shutil
import socketserver
import subprocess
import sys
import threading

ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
MODERN = ("transformer-language-model", "agent-tool-context", "minimax-alpha-beta")


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


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
        [sys.executable, str(ROOT / "tools" / "build_site_v1_7_1.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if build.returncode:
        print(build.stdout)
        print(build.stderr, file=sys.stderr)
        return build.returncode

    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("Playwright is required for v1.7.1 modern-shell QA") from exc

    server = Server(("127.0.0.1", 0), functools.partial(QuietHandler, directory=str(SITE)))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_address[1]}"

    checks: list[tuple[str, bool, object]] = []

    def check(name: str, ok: bool, detail: object = None) -> None:
        checks.append((name, bool(ok), detail))

    with sync_playwright() as p:
        browser = launch(p)
        try:
            context = browser.new_context(viewport={"width": 1280, "height": 900}, reduced_motion="reduce")
            page = context.new_page()
            page_errors: list[str] = []
            console_errors: list[str] = []
            page.on("pageerror", lambda exc: page_errors.append(str(exc)))
            page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

            # Establish the shared origin and simulate a theme preference written by an original applet.
            page.goto(base + "/index.html", wait_until="load", timeout=20_000)
            page.evaluate("() => { localStorage.setItem('theme','dark'); localStorage.removeItem('ai-playgrounds-theme'); }")

            for slug in MODERN:
                page.goto(base + f"/playgrounds/{slug}/index.html?lang=en", wait_until="load", timeout=20_000)
                page.wait_for_selector("#ap-standard-theme", timeout=5_000)
                page.wait_for_timeout(100)
                check(f"{slug}: reads shared dark preference", page.locator("body").evaluate("el=>el.classList.contains('ap-standard-dark')"))
                check(f"{slug}: dark control state", page.locator("#ap-standard-theme").get_attribute("aria-pressed") == "true")
                check(f"{slug}: dark control icon", page.locator("#ap-standard-theme").inner_text() == "☀️")
                check(f"{slug}: canonical key retained", page.evaluate("() => localStorage.getItem('theme')") == "dark")
                check(f"{slug}: obsolete key absent", page.evaluate("() => localStorage.getItem('ai-playgrounds-theme')") is None)

                page.locator("#ap-standard-theme").click()
                page.wait_for_timeout(30)
                check(f"{slug}: toggle writes shared light preference", page.evaluate("() => localStorage.getItem('theme')") == "light")
                check(f"{slug}: light control state", page.locator("#ap-standard-theme").get_attribute("aria-pressed") == "false")
                check(f"{slug}: light control icon", page.locator("#ap-standard-theme").inner_text() == "🌙")

                # Restore dark so the next lab tests cross-page continuity rather than page-local state.
                page.evaluate("() => localStorage.setItem('theme','dark')")

            # Migration: an existing v1.7 user may have only the temporary modern-shell key.
            page.evaluate("() => { localStorage.removeItem('theme'); localStorage.setItem('ai-playgrounds-theme','dark'); }")
            page.goto(base + "/playgrounds/transformer-language-model/index.html?lang=en", wait_until="load", timeout=20_000)
            page.wait_for_timeout(100)
            check("legacy modern-shell key migrates to canonical theme", page.evaluate("() => localStorage.getItem('theme')") == "dark")
            check("legacy modern-shell key removed after migration", page.evaluate("() => localStorage.getItem('ai-playgrounds-theme')") is None)
            check("legacy migration preserves dark appearance", page.locator("body").evaluate("el=>el.classList.contains('ap-standard-dark')"))

            # No stored preference: modern shell follows system preference, matching original-app behavior.
            page.evaluate("() => { localStorage.removeItem('theme'); localStorage.removeItem('ai-playgrounds-theme'); }")
            context.close()
            dark_context = browser.new_context(viewport={"width": 1280, "height": 900}, color_scheme="dark", reduced_motion="reduce")
            dark_page = dark_context.new_page()
            dark_page.goto(base + "/playgrounds/minimax-alpha-beta/index.html?lang=en", wait_until="load", timeout=20_000)
            dark_page.wait_for_timeout(100)
            check("modern shell follows dark system preference when unset", dark_page.locator("body").evaluate("el=>el.classList.contains('ap-standard-dark')"))
            check("system-derived preference becomes canonical", dark_page.evaluate("() => localStorage.getItem('theme')") == "dark")
            dark_context.close()

            check("no page errors", not page_errors, page_errors)
            check("no console errors", not console_errors, console_errors)
        finally:
            browser.close()
            server.shutdown()
            server.server_close()

    failed = [(name, detail) for name, ok, detail in checks if not ok]
    if failed:
        print(f"V1.7.1 MODERN SHELL QA: FAIL ({len(checks)-len(failed)}/{len(checks)})")
        for name, detail in failed:
            print(f"- {name}: {detail}")
        return 1

    print(f"V1.7.1 MODERN SHELL QA: PASS ({len(checks)}/{len(checks)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
