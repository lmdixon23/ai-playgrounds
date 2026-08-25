#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "release-evidence" / "lab14-engagement-candidate.html"


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
        [sys.executable, str(ROOT / "tools" / "build_agent_tool_context_engagement_candidate.py"), "--output", str(OUTPUT)],
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
    checks.append(("engagement runtime is embedded", "Lab14EngagementExperience" in source and "lab14-eq-gates" in source and "lab14-eq-sandbox" in source, {}))
    checks.append(("simulation boundary is explicit", "SIMULATED WORLD" in source and "no real external action" in source and "learner-selected test call" in source, {}))
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
            page.goto(OUTPUT.resolve().as_uri() + "?lang=en", wait_until="load", timeout=10_000)
            page.wait_for_function("() => !!window.Lab14EngagementExperience")

            checks.append(("action packet lane exposes seven runtime gates", page.locator("#lab14-eq-gates .lab14-eq-gate").count() == 7 and page.locator("#lab14-eq-gates").is_visible(), {"gates": page.locator("#lab14-eq-gates .lab14-eq-gate").count()}))
            initial = page.evaluate("() => window.Lab14Prototype.getState()")
            checks.append(("main simulated world initially mirrors canonical state", initial["world"] == {"calendar": [], "mail": [], "drafts": []} and "0" in page.locator("#lab14-eq-worldgrid").inner_text(), {"world": initial["world"]}))

            page.click("#step")
            page.wait_for_timeout(40)
            first = page.evaluate("() => window.Lab14Prototype.getState()")
            gates = page.locator("#lab14-eq-gates .lab14-eq-gate")
            checks.append(("successful tool call traverses through context update", first["history"][-1]["event"] == "executed_ok" and gates.locator(".passed").count() == 6 and "temperature_c" in page.locator("#lab14-eq-delta-list").inner_text(), {"event": first["history"][-1], "passed": gates.locator(".passed").count(), "delta": page.locator("#lab14-eq-delta-list").inner_text()}))

            page.select_option("#scenario", "permission")
            page.wait_for_timeout(20)
            before_denied = page.evaluate("() => window.Lab14Prototype.getState()")
            page.click("#step")
            page.wait_for_timeout(40)
            denied = page.evaluate("() => window.Lab14Prototype.getState()")
            gate_classes = page.locator("#lab14-eq-gates .lab14-eq-gate").evaluate_all("els => els.map(el=>el.className)")
            checks.append(("denied action stops at authorization and cannot mutate world", denied["history"][-1]["event"] == "denied_unauthorized" and before_denied["world"] == denied["world"] and "blocked" in gate_classes[2] and "passed" not in gate_classes[3], {"event": denied["history"][-1], "world": denied["world"], "classes": gate_classes}))

            main_before_sandbox = page.evaluate("() => window.Lab14Prototype.getState()")
            page.select_option("#lab14-eq-principal", "operator")
            page.select_option("#lab14-eq-tool", "mail.send")
            page.wait_for_timeout(10)
            page.click("#lab14-eq-run")
            page.wait_for_timeout(20)
            sandbox = page.evaluate("() => window.Lab14EngagementExperience.getSandboxState()")
            main_after_sandbox = page.evaluate("() => window.Lab14Prototype.getState()")
            checks.append(("learner sandbox can mutate only its isolated simulated world", len(sandbox["world"]["mail"]) == 1 and main_before_sandbox == main_after_sandbox and "executed_ok" in page.locator("#lab14-eq-result").inner_text(), {"sandboxWorld": sandbox["world"], "mainSame": main_before_sandbox == main_after_sandbox}))

            page.click("#lab14-eq-reset")
            page.select_option("#lab14-eq-principal", "assistant")
            page.select_option("#lab14-eq-tool", "mail.send")
            page.wait_for_timeout(10)
            page.click("#lab14-eq-run")
            page.wait_for_timeout(20)
            unauthorized_sandbox = page.evaluate("() => window.Lab14EngagementExperience.getSandboxState()")
            checks.append(("sandbox denial is side-effect free", unauthorized_sandbox["history"][-1]["event"] == "denied_unauthorized" and unauthorized_sandbox["world"]["mail"] == [] and "simulated world unchanged" in page.locator("#lab14-eq-result").inner_text(), {"event": unauthorized_sandbox["history"][-1], "world": unauthorized_sandbox["world"]}))

            page.click("#lab14-eq-reset")
            page.select_option("#lab14-eq-tool", "calendar.create")
            page.wait_for_timeout(10)
            page.fill("#lab14-eq-args", '{"title":"Review"}')
            page.click("#lab14-eq-run")
            page.wait_for_timeout(20)
            invalid_sandbox = page.evaluate("() => window.Lab14EngagementExperience.getSandboxState()")
            checks.append(("sandbox schema rejection is side-effect free", invalid_sandbox["history"][-1]["event"] == "rejected_invalid" and invalid_sandbox["world"] == {"calendar": [], "mail": [], "drafts": []}, {"event": invalid_sandbox["history"][-1], "world": invalid_sandbox["world"]}))

            machine_before_locale = page.evaluate("() => window.Lab14Prototype.getState()")
            sandbox_before_locale = page.evaluate("() => window.Lab14EngagementExperience.getSandboxState()")
            page.select_option("#lab14-language-select", "zh")
            page.wait_for_timeout(50)
            machine_after_locale = page.evaluate("() => window.Lab14Prototype.getState()")
            sandbox_after_locale = page.evaluate("() => window.Lab14EngagementExperience.getSandboxState()")
            checks.append(("locale switch preserves both canonical and sandbox machine state", machine_before_locale == machine_after_locale and sandbox_before_locale == sandbox_after_locale and "模拟世界" in page.locator("#lab14-eq-world-title").inner_text(), {"lang": page.locator("html").get_attribute("lang")}))
            context.close()

            reduced = browser.new_context(viewport={"width": 900, "height": 900}, reduced_motion="reduce")
            rpage = reduced.new_page()
            rpage.on("pageerror", lambda exc: page_errors.append(str(exc)))
            rpage.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            rpage.goto(OUTPUT.resolve().as_uri(), wait_until="load", timeout=10_000)
            rpage.wait_for_function("() => !!window.Lab14EngagementExperience")
            rpage.click("#step")
            rpage.wait_for_timeout(30)
            checks.append(("reduced-motion path preserves gate result without replay animation", not rpage.locator("#lab14-eq-gates").evaluate("el => el.classList.contains('eq-replay')") and "temperature_c" in rpage.locator("#lab14-eq-delta-list").inner_text(), {}))
            reduced.close()

            mobile = browser.new_context(viewport={"width": 390, "height": 844})
            mpage = mobile.new_page()
            mpage.on("pageerror", lambda exc: page_errors.append(str(exc)))
            mpage.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            mpage.goto(OUTPUT.resolve().as_uri() + "?lang=es", wait_until="load", timeout=10_000)
            mpage.wait_for_function("() => !!window.Lab14EngagementExperience")
            overflow = mpage.evaluate("() => document.documentElement.scrollWidth-window.innerWidth")
            checks.append(("agent engagement layer fits 390px mobile", overflow <= 1 and mpage.locator("#lab14-eq-run").is_visible(), {"overflow": overflow}))
            mobile.close()
        finally:
            browser.close()

    failures = [{"name": name, "detail": detail} for name, ok, detail in checks if not ok]
    payload = {
        "harness": "tools/test_agent_tool_context_engagement_candidate.py",
        "checks": len(checks),
        "passed": len(checks)-len(failures),
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
