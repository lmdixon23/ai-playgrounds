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


def main() -> int:
    build = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "build_site_v1_4.py")],
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
    manifest = json.loads((SITE / "applets.json").read_text(encoding="utf-8"))
    files = [p for p in SITE.rglob("*") if p.is_file()]
    applets = sorted((SITE / "playgrounds").glob("*/index.html"))
    checks.append(("v1.4 preserves fourteen-app inventory", len(manifest) == 14 and len(applets) == 14 and len({x["slug"] for x in manifest}) == 14, {"manifest": len(manifest), "applets": len(applets)}))
    checks.append(("v1.4 preserves 54-file deployment boundary", len(files) == 54, {"files": len(files)}))

    lab13 = (SITE / "playgrounds" / "transformer-language-model" / "index.html").read_text(encoding="utf-8")
    lab14 = (SITE / "playgrounds" / "agent-tool-context" / "index.html").read_text(encoding="utf-8")
    checks.append(("Lab 13 engagement wrapper deployed", "Lab13V14Experience" in lab13 and "lab13-mechanism-journey" in lab13 and "lab13-language-select" in lab13, {}))
    checks.append(("Lab 14 engagement wrapper deployed", "Lab14V14Experience" in lab14 and "lab14-action-journey" in lab14 and "lab14-language-select" in lab14, {}))
    checks.append(("prominent v1.3 badges are absent from Labs 13/14", "AI Playgrounds v1.3" not in lab13 and "AI Playgrounds v1.3" not in lab14, {}))
    checks.append(("all fourteen applets carry explicit v1.4 metadata", all('name="ai-playgrounds-version" content="1.4.0"' in p.read_text(encoding="utf-8") for p in applets), {}))
    checks.append(("all fourteen applets expose visible secondary v1.4 provenance", all("v1.4.0" in p.read_text(encoding="utf-8") and ("data-v14-version-provenance" in p.read_text(encoding="utf-8") or "v14-provenance" in p.read_text(encoding="utf-8")) for p in applets), {}))

    curriculum = (SITE / "curriculum.html").read_text(encoding="utf-8")
    checks.append(("curriculum separates foundations and modern extensions", curriculum.count('class="order-dot"') == 13 and 'id="modern-extensions"' in curriculum and "Foundations / course track" in curriculum and "现代 AI 扩展" in curriculum, {"course_rows": curriculum.count('class="order-dot"')}))
    checks.append(("curriculum applet map contains the complete public inventory", curriculum.count('class="applet-card"') == 14 and all(f'playgrounds/{entry["slug"]}/index.html' in curriculum for entry in manifest), {"cards": curriculum.count('class="applet-card"')}))
    checks.append(("Lab 14 is removed from foundations table but retained as an extension and applet-map entry", "Agent Tool Use and Context Protocols</a></td><td data-label=\"Concept area\">Agent systems and tool protocols" not in curriculum and curriculum.count("playgrounds/agent-tool-context/index.html") >= 2, {"agent_links": curriculum.count("playgrounds/agent-tool-context/index.html")}))

    landing = (SITE / "index.html").read_text(encoding="utf-8")
    checks.append(("landing reframes suite as foundations plus extensions", "Fourteen interactive AI labs" in landing and "foundations to modern extensions" in landing and "v1.4.0" in landing, {}))
    checks.append(("landing and support dropdown adapters are embedded", 'id="v14-landing-language-select"' in landing and 'id="v14-support-language-select"' in curriculum, {}))
    release_page = (SITE / "release-notes.html").read_text(encoding="utf-8")
    checks.append(("public release notes expose v1.4 before v1.3 history", 'id="release-v1-4-0"' in release_page and release_page.index('id="release-v1-4-0"') < release_page.index('id="release-v1-3-0"'), {}))

    page_errors: list[str] = []
    console_errors: list[str] = []
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("Playwright required") from exc

    with sync_playwright() as p:
        browser = launch(p)
        try:
            ctx = browser.new_context(viewport={"width": 1280, "height": 960})
            page = ctx.new_page()
            page.on("pageerror", lambda exc: page_errors.append(f"landing: {exc}"))
            page.on("console", lambda msg: console_errors.append(f"landing: {msg.text}") if msg.type == "error" else None)
            page.goto((SITE / "index.html").resolve().as_uri(), wait_until="load", timeout=10_000)
            checks.append(("landing exposes native language select instead of buttons", page.locator(".lang .v14-language-select").is_visible() and page.locator(".lang button[data-lang]:visible").count() == 0 and page.locator(".lang .v14-language-select option").count() == 2, {"options": page.locator(".lang .v14-language-select option").count()}))
            page.select_option(".lang .v14-language-select", "zh")
            page.wait_for_timeout(30)
            landing_lang = page.locator("html").get_attribute("lang") or ""
            checks.append(("landing dropdown drives existing localization", landing_lang.startswith("zh") and "移动" in page.locator("h1").inner_text(), {"lang": landing_lang, "h1": page.locator("h1").inner_text()}))

            page.goto((SITE / "curriculum.html").resolve().as_uri(), wait_until="load", timeout=10_000)
            checks.append(("support page exposes native language select instead of buttons", page.locator(".support-language-switch .v14-language-select").is_visible() and page.locator(".support-language-switch button[data-support-lang]:visible").count() == 0 and page.locator(".support-language-switch .v14-language-select option").count() == 2, {"options": page.locator(".support-language-switch .v14-language-select option").count()}))
            page.select_option(".support-language-switch .v14-language-select", "zh")
            page.wait_for_timeout(30)
            curriculum_lang = page.locator("html").get_attribute("lang") or ""
            checks.append(("curriculum dropdown preserves support localization", curriculum_lang.startswith("zh") and page.locator("#modern-extensions .v14-zh").first.is_visible() and "v1.4.0" in page.locator(".site-footer").inner_text(), {"lang": curriculum_lang}))

            page.goto((SITE / "playgrounds" / "overfitting" / "index.html").resolve().as_uri() + "?lang=vi", wait_until="load", timeout=10_000)
            page.wait_for_function("() => document.querySelector('.r4-language-select')")
            checks.append(("legacy applet native four-language dropdown remains intact", page.locator(".r4-language-select").is_visible() and page.locator(".r4-language-select option").count() == 4 and page.locator(".lang-switch button[data-lang]:visible").count() == 0 and page.locator("html").get_attribute("lang") == "vi", {"options": page.locator(".r4-language-select option").count(), "lang": page.locator("html").get_attribute("lang")}))
            checks.append(("legacy applet version is visible but secondary", page.locator("[data-v14-version-provenance]").is_visible() and "v1.4.0" in page.locator("[data-v14-version-provenance]").inner_text(), {"text": page.locator("[data-v14-version-provenance]").inner_text()}))
            ctx.close()

            mobile = browser.new_context(viewport={"width": 390, "height": 844})
            mpage = mobile.new_page()
            mpage.on("pageerror", lambda exc: page_errors.append(f"mobile: {exc}"))
            mpage.on("console", lambda msg: console_errors.append(f"mobile: {msg.text}") if msg.type == "error" else None)
            for relative in ("index.html", "curriculum.html", "playgrounds/transformer-language-model/index.html", "playgrounds/agent-tool-context/index.html"):
                mpage.goto((SITE / relative).resolve().as_uri(), wait_until="load", timeout=10_000)
                overflow = mpage.evaluate("() => document.documentElement.scrollWidth-window.innerWidth")
                checks.append((f"390px containment: {relative}", overflow <= 1, {"overflow": overflow}))
            mobile.close()
        finally:
            browser.close()

    failures = [{"name": name, "detail": detail} for name, ok, detail in checks if not ok]
    payload = {
        "harness": "tools/test_v1_4_public_integration.py",
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
