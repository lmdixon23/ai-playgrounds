#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
PUBLIC_PAGE = SITE / "playgrounds" / "transformer-language-model" / "index.html"
PUBLIC_MANIFEST = ROOT / "tools" / "applets_v1_2.json"


def launch(playwright):
    args = ["--no-sandbox", "--disable-dev-shm-usage"]
    managed = pathlib.Path(playwright.chromium.executable_path)
    if managed.exists():
        return playwright.chromium.launch(headless=True, args=args)
    for name in ("chromium", "chromium-browser", "google-chrome", "chrome"):
        candidate = shutil.which(name)
        if candidate:
            return playwright.chromium.launch(
                headless=True,
                executable_path=candidate,
                args=args,
            )
    return playwright.chromium.launch(headless=True, args=args)


def main() -> int:
    build = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "build_site.py")],
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
    legacy_manifest = json.loads((ROOT / "applets.json").read_text(encoding="utf-8"))
    manifest = json.loads(PUBLIC_MANIFEST.read_text(encoding="utf-8"))
    deployed_manifest = json.loads((SITE / "applets.json").read_text(encoding="utf-8"))
    slugs = {entry["slug"] for entry in manifest}
    deployed = {path.parent.name for path in (SITE / "playgrounds").glob("*/index.html")}
    deployed_files = [path for path in SITE.rglob("*") if path.is_file()]

    checks.append(("legacy source manifest remains twelve", len(legacy_manifest) == 12 and all(entry.get("slug") != "transformer-language-model" for entry in legacy_manifest), {"count": len(legacy_manifest)}))
    checks.append(("thirteen v1.2 metadata entries", len(manifest) == 13 and "transformer-language-model" in slugs, {"count": len(manifest), "slugs": sorted(slugs)}))
    checks.append(("deployed manifest equals v1.2 manifest", deployed_manifest == manifest, {}))
    checks.append(("thirteen deployed applets", len(deployed) == 13 and deployed == slugs, {"deployed": sorted(deployed)}))
    checks.append(("minimal v1.2 Pages artifact is 53 files", len(deployed_files) == 53, {"files": len(deployed_files)}))

    home = (SITE / "index.html").read_text(encoding="utf-8")
    curriculum = (SITE / "curriculum.html").read_text(encoding="utf-8")
    release_notes = (SITE / "release-notes.html").read_text(encoding="utf-8")
    sitemap = (SITE / "sitemap.xml").read_text(encoding="utf-8")
    public = PUBLIC_PAGE.read_text(encoding="utf-8")

    checks.append(("landing names thirteen applets", "Explore the thirteen applets" in home and "Explore all thirteen" in home, {}))
    checks.append(("landing manifest contains Lab 13", '"slug":"transformer-language-model"' in home, {}))
    checks.append(("curriculum has thirteenth Lab 13 row", curriculum.count('class="order-dot"') == 13 and "playgrounds/transformer-language-model/index.html" in curriculum, {"rows": curriculum.count('class="order-dot"')}))
    checks.append(("public release notes identify v1.2", "release-v1-2-0" in release_notes and "AI Playgrounds v1.2.0, released August 24, 2026." in release_notes, {}))
    checks.append(("sitemap contains Lab 13", "playgrounds/transformer-language-model/index.html" in sitemap, {}))
    checks.append(("public Lab 13 drops candidate wording", all(term not in public for term in ("English source candidate:", "non-public v1.2 candidate", "v1.2 非公开候选版本", "ứng viên v1.2 chưa công khai", "candidato v1.2 no público")), {}))
    checks.append(("public Lab 13 canonical metadata", "https://lmdixon23.github.io/ai-playgrounds/playgrounds/transformer-language-model/" in public and 'hreflang="vi"' in public and 'hreflang="es"' in public, {}))
    checks.append(("public Lab 13 remains single-file/offline", "<script src=" not in public and "fetch(" not in public and "XMLHttpRequest" not in public, {}))
    checks.append(("public Lab 13 has suite back route", 'href="../../index.html"' in public, {}))

    page_errors: list[str] = []
    console_errors: list[str] = []
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("Playwright required") from exc

    with sync_playwright() as p:
        browser = launch(p)
        try:
            context = browser.new_context(viewport={"width": 1280, "height": 1000})
            page = context.new_page()
            page.on("pageerror", lambda exc: page_errors.append(str(exc)))
            page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

            page.goto((SITE / "index.html").resolve().as_uri(), wait_until="load", timeout=10_000)
            checks.append(("landing renders thirteen cards", page.locator("#appletGrid .applet").count() == 13, {"count": page.locator("#appletGrid .applet").count()}))
            hrefs = page.locator("#appletGrid .applet").evaluate_all("els => els.map(el => el.getAttribute('href'))")
            checks.append(("landing renders Lab 13 route", any("transformer-language-model" in (href or "") for href in hrefs), {"hrefs": hrefs}))

            page.goto(PUBLIC_PAGE.resolve().as_uri() + "?lang=zh", wait_until="load", timeout=10_000)
            page.wait_for_function("() => !!window.Lab13Localization && !!window.TransformerLanguageModelCore")
            zh_title = page.evaluate("() => window.Lab13Localization.catalogs.zh['page.title']")
            checks.append(("query parameter initializes Simplified Chinese", page.locator("html").get_attribute("lang") == "zh-Hans" and page.locator("h1").first.inner_text() == zh_title, {"lang": page.locator("html").get_attribute("lang"), "title": page.locator("h1").first.inner_text()}))
            checks.append(("public page exposes four locale controls", page.locator("#lab13-locale-bar button[data-locale]").count() == 4, {"count": page.locator("#lab13-locale-bar button[data-locale]").count()}))

            canonical = page.evaluate("() => window.TransformerLanguageModelCore.forwardText('I like cats').attention.at(-1)")
            expected = [0.20366059441088602, 0.24469312034003501, 0.2459995865850857, 0.3056466986639933]
            checks.append(("public page preserves frozen arithmetic", all(abs(a-b) < 1e-12 for a,b in zip(canonical, expected)), {"attention": canonical}))

            for locale, html_lang in (("en", "en"), ("zh", "zh-Hans"), ("vi", "vi"), ("es", "es")):
                page.evaluate("locale => window.Lab13Localization.setLocale(locale)", locale)
                page.wait_for_timeout(30)
                expected_title = page.evaluate("locale => window.Lab13Localization.catalogs[locale]['page.title']", locale)
                checks.append((f"{locale} public title parity", page.locator("h1").first.inner_text() == expected_title and page.locator("html").get_attribute("lang") == html_lang, {"title": page.locator("h1").first.inner_text(), "lang": page.locator("html").get_attribute("lang")}))

            context.close()

            mobile = browser.new_context(viewport={"width": 390, "height": 844})
            mobile_page = mobile.new_page()
            mobile_page.on("pageerror", lambda exc: page_errors.append(str(exc)))
            mobile_page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            mobile_page.goto(PUBLIC_PAGE.resolve().as_uri() + "?lang=vi", wait_until="load", timeout=10_000)
            mobile_page.wait_for_function("() => !!window.Lab13Localization")
            overflow = mobile_page.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
            checks.append(("public Lab 13 mobile root containment", overflow <= 1, {"overflow": overflow}))
            mobile.close()
        finally:
            browser.close()

    failures = [{"name": name, "detail": detail} for name, ok, detail in checks if not ok]
    payload = {
        "harness": "tools/test_transformer_public_integration.py",
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
