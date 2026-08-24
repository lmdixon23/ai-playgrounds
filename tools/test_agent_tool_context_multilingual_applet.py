#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILDER = ROOT / "tools" / "build_agent_tool_context_multilingual_candidate.py"
PAGE = ROOT / "release-evidence" / "lab14-agent-tool-context-multilingual-candidate.html"
R4_SOURCE_FREEZE = "9f2f5286f4de3e12a881b61d491c87efe6950166"
R5_LOCALIZATION_FREEZE = "37bdc6a4a84b672ad564d81564e8a055c2b2c9a6"


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
        [sys.executable, str(BUILDER)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if built.returncode:
        print(built.stdout)
        print(built.stderr, file=sys.stderr)
        return built.returncode

    source = PAGE.read_text(encoding="utf-8")
    checks: list[tuple[str, bool, object]] = []
    checks.append(("builder produced four-locale candidate", PAGE.is_file(), {"path": str(PAGE)}))
    checks.append(("candidate remains self-contained", "<script src=" not in source and "lab14-i18n-runtime" in source, {}))
    checks.append(("candidate contains no runtime network primitives", all(token not in source for token in ("fetch(", "XMLHttpRequest", "WebSocket(", "EventSource(")), {}))
    checks.append(("candidate remains non-public", "non-public v1.3 four-locale candidate" in source and PAGE.parent.name == "release-evidence", {}))

    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("Playwright required") from exc

    page_errors: list[str] = []
    console_errors: list[str] = []

    with sync_playwright() as p:
        browser = launch(p)
        try:
            context = browser.new_context(viewport={"width": 1280, "height": 1000})
            page = context.new_page()
            page.on("pageerror", lambda exc: page_errors.append(str(exc)))
            page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            page.goto(PAGE.resolve().as_uri(), wait_until="load", timeout=10_000)
            page.wait_for_function("() => !!window.Lab14Localization && !!window.Lab14Prototype && !!window.AgentToolContextCore")

            checks.append(("four locale controls", page.locator("#lab14-locale-bar button[data-locale]").count() == 4, {"count": page.locator("#lab14-locale-bar button[data-locale]").count()}))
            checks.append(("English is initial locale", page.evaluate("() => window.Lab14Localization.getLocale()") == "en" and page.locator("html").get_attribute("lang") == "en", {}))
            meta = page.evaluate("() => window.Lab14Localization.meta")
            checks.append(("R6 binds exact R4 source freeze", meta.get("r4SourceFreeze") == R4_SOURCE_FREEZE, meta))
            checks.append(("R6 binds exact R5 localization freeze", meta.get("r5LocalizationFreeze") == R5_LOCALIZATION_FREEZE, meta))
            checks.append(("merged catalog contains 163 keys", len(page.evaluate("() => Object.keys(window.Lab14Localization.catalogs.en)")) == 163, {}))

            # Put the deterministic app into a non-initial state before changing locale.
            page.locator("#step").click()
            page.locator("#challengeType").select_option("gate")
            page.locator("#prediction").select_option("reject-invalid")
            page.locator("#lock").click()

            def machine_snapshot() -> str:
                return page.evaluate(
                    """() => JSON.stringify({
                      state:window.Lab14Prototype.getState(),
                      decision:window.Lab14Prototype.getDecision(),
                      scenario:document.querySelector('#scenario').value,
                      challenge:document.querySelector('#challengeType').value,
                      prediction:document.querySelector('#prediction').value,
                      predictionDisabled:document.querySelector('#prediction').disabled,
                      challengeDisabled:document.querySelector('#challengeType').disabled,
                      revealDisabled:document.querySelector('#reveal').disabled
                    })"""
                )

            frozen_machine = machine_snapshot()
            checks.append(("pre-switch challenge remains locked", page.locator("#prediction").is_disabled() and page.locator("#challengeType").is_disabled() and page.locator("#reveal").is_enabled(), {}))

            locale_expectations = {"zh": "zh-Hans", "vi": "vi", "es": "es", "en": "en"}
            for locale, html_lang in locale_expectations.items():
                page.evaluate("locale => window.Lab14Localization.setLocale(locale)", locale)
                page.wait_for_timeout(60)
                title = page.evaluate("locale => window.Lab14Localization.catalogs[locale]['page.title']", locale)
                goal = page.evaluate("locale => window.Lab14Localization.catalogs[locale]['goal.canonical']", locale)
                boundary = page.evaluate("locale => window.Lab14Localization.catalogs[locale]['boundary.label']", locale)
                myth = page.evaluate("locale => window.Lab14Localization.catalogs[locale]['myth.1']", locale)
                terms = page.evaluate("locale => window.Lab14Localization.catalogs[locale]['terms.heading']", locale)
                body = page.locator("body").inner_text()
                state_text = page.locator("#stateText").inner_text()
                checks.append((f"{locale} title localized", page.locator("h1").first.inner_text() == title, {"actual": page.locator("h1").first.inner_text(), "expected": title}))
                checks.append((f"{locale} document language", page.locator("html").get_attribute("lang") == html_lang, {"lang": page.locator("html").get_attribute("lang")}))
                checks.append((f"{locale} major semantic surfaces localized", boundary in body and myth in body and terms in body, {"boundary": boundary, "myth": myth, "terms": terms}))
                checks.append((f"{locale} dynamic goal localized", page.locator("#goal").inner_text() == goal, {"actual": page.locator("#goal").inner_text(), "expected": goal}))
                checks.append((f"{locale} locale switch preserves exact machine state", machine_snapshot() == frozen_machine, {}))
                checks.append((f"{locale} accessible state localizes values only", goal in state_text and '"goal_conditions"' in state_text and "weather.current" in state_text, {"excerpt": state_text[:700]}))
                checks.append((f"{locale} protected tool identifiers remain visible", all(token in body for token in ("weather.current", "unit.convert_temperature", "mail.send", "notes.search", "MCP 2026-07-28")), {}))

            # Dynamic content created after a locale switch must not fall back to English.
            page.evaluate("() => window.Lab14Localization.setLocale('vi')")
            page.locator("#scenario").select_option("injection")
            page.wait_for_timeout(50)
            page.locator("#step").click()
            page.wait_for_timeout(100)
            vi_attack = page.evaluate("() => window.Lab14Localization.catalogs.vi['fixture.note_injection']")
            vi_body = page.locator("body").inner_text()
            checks.append(("Vietnamese post-switch adversarial observation localizes", vi_attack in vi_body and "IGNORE THE CURRENT TASK" not in vi_body, {"expected": vi_attack}))
            checks.append(("localized adversarial observation preserves mail.send", "mail.send" in vi_body, {}))
            underlying = page.evaluate("() => window.Lab14Prototype.getState()")
            checks.append(("localization does not mutate frozen tool observation", any("IGNORE THE CURRENT TASK" in str(item.get("value", "")) for item in underlying.get("context", [])), underlying.get("context", [])))

            # Challenge result is generated after localization and must remain localized.
            page.evaluate("() => window.Lab14Localization.setLocale('es')")
            page.locator("#resetChallenge").click()
            page.locator("#challengeType").select_option("gate")
            page.locator("#prediction").select_option("reject-invalid")
            page.locator("#lock").click()
            page.locator("#reveal").click()
            page.wait_for_timeout(100)
            es_reveal = page.evaluate("() => window.Lab14Localization.catalogs.es['challenge.gate.reveal']")
            es_result = page.locator("#challengeResult").inner_text()
            checks.append(("Spanish post-switch challenge reveal localizes", es_reveal.split("\n", 1)[1] in es_result and "Execution is blocked before authorization" not in es_result, {"text": es_result}))
            checks.append(("Spanish validation JSON preserves schema identifiers", "calendar.create" not in es_result or "day" in es_result and "hour" in es_result, {"text": es_result}))

            # Query parameter locale selection is part of the candidate contract used by R7.
            query_page = context.new_page()
            query_page.on("pageerror", lambda exc: page_errors.append(str(exc)))
            query_page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            query_page.goto(PAGE.resolve().as_uri() + "?lang=zh", wait_until="load", timeout=10_000)
            query_page.wait_for_function("() => !!window.Lab14Localization")
            zh_title = query_page.evaluate("() => window.Lab14Localization.catalogs.zh['page.title']")
            checks.append(("lang query initializes Simplified Chinese", query_page.evaluate("() => window.Lab14Localization.getLocale()") == "zh" and query_page.locator("html").get_attribute("lang") == "zh-Hans" and query_page.locator("h1").first.inner_text() == zh_title, {}))
            query_page.close()
            context.close()

            mobile = browser.new_context(viewport={"width": 390, "height": 844})
            mobile_page = mobile.new_page()
            mobile_page.on("pageerror", lambda exc: page_errors.append(str(exc)))
            mobile_page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            mobile_page.goto(PAGE.resolve().as_uri(), wait_until="load", timeout=10_000)
            mobile_page.wait_for_function("() => !!window.Lab14Localization")
            for locale in ("en", "zh", "vi", "es"):
                mobile_page.evaluate("locale => window.Lab14Localization.setLocale(locale)", locale)
                mobile_page.wait_for_timeout(40)
                overflow = mobile_page.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
                checks.append((f"{locale} mobile root containment", overflow <= 1, {"overflow": overflow}))
            mobile.close()
        finally:
            browser.close()

    failures = [{"name": name, "detail": detail} for name, ok, detail in checks if not ok]
    payload = {
        "harness": "tools/test_agent_tool_context_multilingual_applet.py",
        "candidate": str(PAGE.relative_to(ROOT)),
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
