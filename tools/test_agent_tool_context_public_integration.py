#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
PUBLIC_PAGE = SITE / "playgrounds" / "agent-tool-context" / "index.html"
R6_BROWSER_FREEZE = "07f89d13269041d9ed66de2362bf84c288bb86de"


def launch(playwright):
    args = ["--no-sandbox", "--disable-dev-shm-usage"]
    managed = pathlib.Path(playwright.chromium.executable_path)
    if managed.exists():
        return playwright.chromium.launch(headless=True, args=args)
    for name in ("chromium", "chromium-browser", "google-chrome", "chrome", "msedge"):
        candidate = shutil.which(name)
        if candidate:
            return playwright.chromium.launch(headless=True, executable_path=candidate, args=args)
    return playwright.chromium.launch(headless=True, args=args)


def main() -> int:
    built = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "build_site_v1_3.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if built.returncode:
        print(built.stdout)
        print(built.stderr, file=sys.stderr)
        return built.returncode

    checks: list[tuple[str, bool, object]] = []
    manifest = json.loads((SITE / "applets.json").read_text(encoding="utf-8"))
    slugs = {entry["slug"] for entry in manifest}
    deployed_files = [path for path in SITE.rglob("*") if path.is_file()]
    public = PUBLIC_PAGE.read_text(encoding="utf-8")
    home = (SITE / "index.html").read_text(encoding="utf-8")
    curriculum = (SITE / "curriculum.html").read_text(encoding="utf-8")
    release_notes = (SITE / "release-notes.html").read_text(encoding="utf-8")
    sitemap = (SITE / "sitemap.xml").read_text(encoding="utf-8")

    lab14 = next((entry for entry in manifest if entry.get("slug") == "agent-tool-context"), None)
    checks.append(("fourteen-entry v1.3 manifest", len(manifest) == 14 and len(slugs) == 14, {"count": len(manifest), "slugs": sorted(slugs)}))
    checks.append(("Lab 14 release metadata present", bool(lab14) and lab14.get("course_order") == 14 and lab14.get("showcase_order") == 14, lab14))
    checks.append(("minimal Pages artifact is 54 files", len(deployed_files) == 54, {"files": len(deployed_files)}))
    checks.append(("public Lab 14 page exists", PUBLIC_PAGE.is_file(), {"path": str(PUBLIC_PAGE)}))
    checks.append(("public Lab 14 drops non-public wording", all(term not in public for term in ("English source candidate:", "non-public v1.3", "R6 candidate")), {}))
    checks.append(("public Lab 14 keeps exact R6 binding", f'name="lab14-r6-freeze" content="{R6_BROWSER_FREEZE}"' in public, {}))
    checks.append(("public Lab 14 canonical and four-locale metadata", "https://lmdixon23.github.io/ai-playgrounds/playgrounds/agent-tool-context/" in public and all(f'hreflang="{lang}"' in public for lang in ("en", "zh-Hans", "vi", "es")), {}))
    checks.append(("public Lab 14 remains single-file/offline", "<script src=" not in public and all(token not in public for token in ("fetch(", "XMLHttpRequest", "WebSocket(", "EventSource(")), {}))
    checks.append(("public Lab 14 suite shell installed", 'href="../../index.html"' in public and "AI Playgrounds v1.3" in public, {}))
    checks.append(("landing includes Lab 14", '"slug":"agent-tool-context"' in home and "Explore the fourteen applets" in home, {}))
    checks.append(("curriculum includes Lab 14 as row fourteen", curriculum.count('class="order-dot"') == 14 and "playgrounds/agent-tool-context/index.html" in curriculum, {"rows": curriculum.count('class="order-dot"')}))
    checks.append(("release notes identify v1.3 Lab 14", "release-v1-3-0" in release_notes and "Agent Tool Use and Context Protocols" in release_notes, {}))
    checks.append(("sitemap includes Lab 14", "playgrounds/agent-tool-context/index.html" in sitemap, {}))

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

            page.goto(PUBLIC_PAGE.resolve().as_uri() + "?lang=zh", wait_until="load", timeout=10_000)
            page.wait_for_function("() => !!window.Lab14Localization && !!window.Lab14Prototype && !!window.AgentToolContextCore")
            zh_title = page.evaluate("() => window.Lab14Localization.catalogs.zh['page.title']")
            checks.append(("query parameter initializes Simplified Chinese", page.locator("html").get_attribute("lang") == "zh-Hans" and page.locator("h1").first.inner_text() == zh_title, {"lang": page.locator("html").get_attribute("lang"), "title": page.locator("h1").first.inner_text()}))
            checks.append(("public Lab 14 exposes four locale controls", page.locator("#lab14-locale-bar button[data-locale]").count() == 4, {"count": page.locator("#lab14-locale-bar button[data-locale]").count()}))
            checks.append(("public page retains eight scenarios", page.locator("#scenario option").count() == 8, {"count": page.locator("#scenario option").count()}))
            checks.append(("public page retains five Guided Challenges", page.locator("#challengeType option").count() == 5, {"count": page.locator("#challengeType option").count()}))

            page.locator("#scenario").select_option("canonical")
            page.locator("#step").click()
            before_switch = page.evaluate("() => JSON.stringify({state:window.Lab14Prototype.getState(),decision:window.Lab14Prototype.getDecision()})")
            for locale, html_lang in (("en", "en"), ("zh", "zh-Hans"), ("vi", "vi"), ("es", "es")):
                page.evaluate("locale => window.Lab14Localization.setLocale(locale)", locale)
                page.wait_for_timeout(40)
                expected_title = page.evaluate("locale => window.Lab14Localization.catalogs[locale]['page.title']", locale)
                checks.append((f"{locale} public title parity", page.locator("h1").first.inner_text() == expected_title and page.locator("html").get_attribute("lang") == html_lang, {"title": page.locator("h1").first.inner_text(), "lang": page.locator("html").get_attribute("lang")}))
                checks.append((f"{locale} locale switch preserves machine state", page.evaluate("() => JSON.stringify({state:window.Lab14Prototype.getState(),decision:window.Lab14Prototype.getDecision()})") == before_switch, {}))

            page.evaluate("() => window.Lab14Localization.setLocale('en')")
            page.locator("#step").click()
            after_convert = page.evaluate("() => ({state:window.Lab14Prototype.getState(),decision:window.Lab14Prototype.getDecision()})")
            facts = {item["key"]: item["value"] for item in after_convert["state"]["context"]}
            checks.append(("public canonical conversion remains exact", facts.get("temperature_c") == 8 and abs(float(facts.get("temperature_f", -999)) - 46.4) < 1e-12, facts))
            checks.append(("public canonical goal selects stop", after_convert["decision"]["selected_action"].get("type") == "stop", after_convert["decision"]["selected_action"]))
            page.locator("#step").click()
            final = page.evaluate("() => window.Lab14Prototype.getState()")
            checks.append(("public canonical trace terminates", final["status"] == "complete" and final["history"][-1]["event"] == "stopped_complete", {"status": final["status"], "last": final["history"][-1]}))

            page.locator("#scenario").select_option("permission")
            page.locator("#step").click()
            denied = page.evaluate("() => window.Lab14Prototype.getState()")
            checks.append(("public permission boundary still denies mail", denied["history"][-1]["event"] == "denied_unauthorized" and denied["world"].get("mail", []) == [], denied["history"][-1]))

            page.evaluate("() => window.Lab14Localization.setLocale('vi')")
            page.locator("#scenario").select_option("injection")
            page.locator("#step").click()
            page.wait_for_timeout(80)
            vi_attack = page.evaluate("() => window.Lab14Localization.catalogs.vi['fixture.note_injection']")
            checks.append(("public adversarial observation localizes without sanitizing", vi_attack in page.locator("body").inner_text() and "mail.send" in page.locator("body").inner_text(), {}))
            injection = page.evaluate("() => window.Lab14Prototype.getState()")
            checks.append(("public adversarial observation cannot change goal/principal", injection["goal"] == "Find the meeting note and report its content." and injection["principal"] == "assistant", {"goal": injection["goal"], "principal": injection["principal"]}))

            context.close()

            mobile = browser.new_context(viewport={"width": 390, "height": 844})
            mobile_page = mobile.new_page()
            mobile_page.on("pageerror", lambda exc: page_errors.append(str(exc)))
            mobile_page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            mobile_page.goto(PUBLIC_PAGE.resolve().as_uri() + "?lang=es", wait_until="load", timeout=10_000)
            mobile_page.wait_for_function("() => !!window.Lab14Localization")
            overflow = mobile_page.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
            checks.append(("public Lab 14 mobile root containment", overflow <= 1, {"overflow": overflow}))
            mobile.close()
        finally:
            browser.close()

    failures = [{"name": name, "detail": detail} for name, ok, detail in checks if not ok]
    payload = {
        "harness": "tools/test_agent_tool_context_public_integration.py",
        "release": "v1.3.0",
        "r6_browser_freeze": R6_BROWSER_FREEZE,
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
