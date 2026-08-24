#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "release-evidence" / "lab14-agent-tool-context-v1.4-experience.html"


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
        [sys.executable, str(ROOT / "tools" / "build_agent_tool_context_public_v1_4.py"), "--output", str(OUTPUT)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if build.returncode:
        print(build.stdout)
        print(build.stderr, file=sys.stderr)
        return build.returncode

    source = OUTPUT.read_text(encoding="utf-8")
    checks: list[tuple[str, bool, object]] = []
    checks.append(("v1.4 version is secondary provenance", 'name="ai-playgrounds-version" content="1.4.0"' in source and 'data-lab14-v14-provenance' in source and "v1.4.0" in source, {}))
    checks.append(("prominent v1.3 badge removed", "AI Playgrounds v1.3" not in source, {}))
    checks.append(("v1.4 action journey runtime embedded", "Lab14V14Experience" in source and "lab14-language-select" in source and "p-update" in source and "p-stop" in source, {}))
    checks.append(("single-file offline boundary retained", all(token not in source for token in ("<script src=", "fetch(", "XMLHttpRequest", "WebSocket(", "EventSource(")), {}))

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
            page.goto(OUTPUT.resolve().as_uri() + "?lang=zh", wait_until="load", timeout=10_000)
            page.wait_for_function("() => !!window.Lab14Localization && !!window.Lab14Prototype && !!window.Lab14V14Experience")

            checks.append(("native language dropdown is the visible locale control", page.locator("#lab14-language-select").is_visible() and page.locator("#lab14-language-select option").count() == 4 and page.locator("#lab14-locale-bar button[data-locale]:visible").count() == 0, {"options": page.locator("#lab14-language-select option").count()}))
            checks.append(("query locale survives wrapper", page.locator("html").get_attribute("lang") == "zh-Hans" and page.locator("#lab14-language-select").input_value() == "zh", {"lang": page.locator("html").get_attribute("lang"), "select": page.locator("#lab14-language-select").input_value()}))
            checks.append(("runtime path exposes seven stages", page.locator(".pipeline .stage").count() == 7 and page.locator("#p-update").is_visible() and page.locator("#p-stop").is_visible(), {"stages": page.locator(".pipeline .stage").count()}))
            checks.append(("initial selected action is visibly at propose", "weather.current" in page.locator("#lab14-action-chip").inner_text() and "v14-current" in (page.locator("#p-propose").get_attribute("class") or ""), {"action": page.locator("#lab14-action-chip").inner_text(), "proposeClass": page.locator("#p-propose").get_attribute("class")}))

            initial = page.evaluate("() => window.Lab14Prototype.getState()")
            page.select_option("#lab14-language-select", "vi")
            page.wait_for_timeout(40)
            after_locale = page.evaluate("() => window.Lab14Prototype.getState()")
            checks.append(("dropdown locale switch preserves exact machine state", initial == after_locale and page.locator("html").get_attribute("lang") == "vi" and "lang=vi" in page.url, {"lang": page.locator("html").get_attribute("lang"), "url": page.url}))

            page.locator("#step").click()
            page.wait_for_timeout(30)
            first = page.evaluate("() => window.Lab14Prototype.getState()")
            first_decision = page.evaluate("() => window.Lab14Prototype.getDecision()")
            checks.append(("successful observation visibly reaches context update", first["history"][-1]["event"] == "executed_ok" and any(item.get("key") == "temperature_c" and item.get("value") == 8 for item in first["context"]) and "v14-current" in (page.locator("#p-update").get_attribute("class") or "") and "unit.convert_temperature" in page.locator("#lab14-action-chip").inner_text(), {"history": first["history"], "decision": first_decision, "updateClass": page.locator("#p-update").get_attribute("class")}))

            page.locator("#step").click()
            page.wait_for_timeout(30)
            second = page.evaluate("() => window.Lab14Prototype.getState()")
            second_decision = page.evaluate("() => window.Lab14Prototype.getDecision()")
            checks.append(("goal completion makes STOP visibly ready", any(item.get("key") == "temperature_f" and abs(float(item.get("value")) - 46.4) < 1e-12 for item in second["context"]) and second_decision["selected_action"]["type"] == "stop" and "v14-ready" in (page.locator("#p-stop").get_attribute("class") or "") and page.locator("#lab14-action-chip").inner_text() == "STOP", {"decision": second_decision, "stopClass": page.locator("#p-stop").get_attribute("class")}))

            page.locator("#step").click()
            page.wait_for_timeout(30)
            third = page.evaluate("() => window.Lab14Prototype.getState()")
            checks.append(("STOP visibly terminates a satisfied goal", third["status"] == "complete" and third["history"][-1]["event"] == "stopped_complete" and "v14-current" in (page.locator("#p-stop").get_attribute("class") or "") and "good" in (page.locator("#p-stop").get_attribute("class") or ""), {"status": third["status"], "event": third["history"][-1], "stopClass": page.locator("#p-stop").get_attribute("class")}))

            page.select_option("#scenario", "invalid")
            page.wait_for_timeout(20)
            page.locator("#step").click()
            page.wait_for_timeout(20)
            invalid = page.evaluate("() => window.Lab14Prototype.getState()")
            checks.append(("schema-invalid call visibly terminates at validation", invalid["history"][-1]["event"] == "rejected_invalid" and "v14-current" in (page.locator("#p-validate").get_attribute("class") or "") and invalid["world"] == {"calendar": [], "mail": [], "drafts": []}, {"event": invalid["history"][-1], "validateClass": page.locator("#p-validate").get_attribute("class")}))

            page.select_option("#scenario", "permission")
            page.wait_for_timeout(20)
            page.locator("#step").click()
            page.wait_for_timeout(20)
            denied = page.evaluate("() => window.Lab14Prototype.getState()")
            checks.append(("unauthorized call visibly terminates at authorization", denied["history"][-1]["event"] == "denied_unauthorized" and "v14-current" in (page.locator("#p-authorize").get_attribute("class") or "") and denied["world"]["mail"] == [], {"event": denied["history"][-1], "authorizeClass": page.locator("#p-authorize").get_attribute("class")}))

            checks.append(("version remains visible but secondary", page.locator(".badge").inner_text() == "AI Playgrounds" and "v1.4.0" in page.locator(".lab14-provenance").inner_text(), {"badge": page.locator(".badge").inner_text(), "footer": page.locator(".lab14-provenance").inner_text()}))
            context.close()

            mobile = browser.new_context(viewport={"width": 390, "height": 844})
            mpage = mobile.new_page()
            mpage.on("pageerror", lambda exc: page_errors.append(str(exc)))
            mpage.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            mpage.goto(OUTPUT.resolve().as_uri() + "?lang=es", wait_until="load", timeout=10_000)
            mpage.wait_for_function("() => !!window.Lab14V14Experience")
            overflow = mpage.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
            checks.append(("v1.4 agent experience fits 390px mobile", overflow <= 1 and mpage.locator("#lab14-language-select").is_visible(), {"overflow": overflow}))
            mobile.close()
        finally:
            browser.close()

    failures = [{"name": name, "detail": detail} for name, ok, detail in checks if not ok]
    payload = {
        "harness": "tools/test_agent_tool_context_v1_4_experience.py",
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
