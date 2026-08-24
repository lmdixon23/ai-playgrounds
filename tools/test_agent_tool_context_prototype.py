#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAGE = ROOT / "tools" / "agent_tool_context_prototype.html"
CORE = ROOT / "tools" / "agent_tool_context_core.js"


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
    source = PAGE.read_text(encoding="utf-8")
    core_source = CORE.read_text(encoding="utf-8")
    checks: list[tuple[str, bool, object]] = []
    checks.append(("prototype exists", PAGE.is_file(), {"path": str(PAGE)}))
    checks.append(("independent JavaScript core exists", CORE.is_file(), {"path": str(CORE)}))
    checks.append(("prototype references local core", 'src="agent_tool_context_core.js"' in source, {}))
    checks.append(("prototype has no runtime fetch/XHR", "fetch(" not in source and "XMLHttpRequest" not in source, {}))
    checks.append(("prototype remains non-public", PAGE.parent.name == "tools" and "non-public v1.3 candidate" in source, {}))
    checks.append(("core exposes MCP 2026-07-28", "2026-07-28" in core_source and "mcp20260728Envelope" in core_source, {}))

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
            page.on(
                "console",
                lambda msg: console_errors.append(msg.text)
                if msg.type == "error"
                else None,
            )
            page.goto(PAGE.resolve().as_uri(), wait_until="load", timeout=10_000)
            page.wait_for_function("() => !!window.AgentToolContextCore && !!window.Lab14Prototype")

            checks.append(("eight scenarios", page.locator("#scenario option").count() == 8, {"count": page.locator("#scenario option").count()}))
            checks.append(("seven deterministic tools", page.locator("#tools .tool").count() == 7, {"count": page.locator("#tools .tool").count()}))
            initial = page.evaluate("() => ({state:window.Lab14Prototype.getState(),decision:window.Lab14Prototype.getDecision()})")
            checks.append(("canonical initial action is current weather", initial["decision"]["selected_action"].get("name") == "weather.current", initial["decision"]))
            checks.append(("canonical initial context has city only", initial["state"]["context"][0]["key"] == "city" and len(initial["state"]["context"]) == 1, initial["state"]["context"]))

            page.locator("#step").click()
            after_weather = page.evaluate("() => ({state:window.Lab14Prototype.getState(),decision:window.Lab14Prototype.getDecision()})")
            facts_after_weather = {item["key"]: item["value"] for item in after_weather["state"]["context"]}
            checks.append(("weather observation adds exact Celsius fact", facts_after_weather.get("temperature_c") == 8, facts_after_weather))
            checks.append(("observation changes next action to conversion", after_weather["decision"]["selected_action"].get("name") == "unit.convert_temperature", after_weather["decision"]))

            page.locator("#step").click()
            after_conversion = page.evaluate("() => ({state:window.Lab14Prototype.getState(),decision:window.Lab14Prototype.getDecision()})")
            facts_after_conversion = {item["key"]: item["value"] for item in after_conversion["state"]["context"]}
            checks.append(("conversion adds exact Fahrenheit fact", facts_after_conversion.get("temperature_f") == 46.4, facts_after_conversion))
            checks.append(("completed facts make stop the next action", after_conversion["decision"]["selected_action"].get("type") == "stop", after_conversion["decision"]))

            page.locator("#step").click()
            completed = page.evaluate("() => window.Lab14Prototype.getState()")
            checks.append(("canonical trace explicitly stops complete", completed["status"] == "complete" and completed["history"][-1]["event"] == "stopped_complete", completed["history"][-1]))
            checks.append(("completed trace disables execution button", page.locator("#step").is_disabled(), {}))

            page.locator("#scenario").select_option("overlap")
            page.wait_for_timeout(20)
            overlap = page.evaluate("() => window.Lab14Prototype.getDecision()")
            checks.append(("overlap scenario chooses current not forecast", overlap["selected_action"].get("name") == "weather.current", overlap))

            page.locator("#scenario").select_option("invalid")
            page.locator("#step").click()
            invalid = page.evaluate("() => window.Lab14Prototype.getState()")
            checks.append(("invalid arguments are rejected before execution", invalid["history"][-1]["event"] == "rejected_invalid" and not invalid["history"][-1]["executed"], invalid["history"][-1]))
            checks.append(("invalid calendar call has no side effect", invalid["world"]["calendar"] == [], invalid["world"]))

            page.locator("#scenario").select_option("text")
            page.locator("#step").click()
            text_state = page.evaluate("() => window.Lab14Prototype.getState()")
            text_facts = {item["key"]: item["value"] for item in text_state["context"]}
            checks.append(("model text is not execution", text_state["history"][-1]["event"] == "text_only" and "temperature_c" not in text_facts, text_state["history"][-1]))

            page.locator("#scenario").select_option("permission")
            page.locator("#step").click()
            permission = page.evaluate("() => window.Lab14Prototype.getState()")
            checks.append(("permission gate denies visible tool", permission["history"][-1]["event"] == "denied_unauthorized", permission["history"][-1]))
            checks.append(("permission denial prevents mail side effect", permission["world"]["mail"] == [], permission["world"]))

            page.locator("#scenario").select_option("injection")
            goal_before = page.locator("#goal").inner_text()
            page.locator("#step").click()
            injection = page.evaluate("() => ({state:window.Lab14Prototype.getState(),decision:window.Lab14Prototype.getDecision()})")
            note = next(item for item in injection["state"]["context"] if item["key"] == "notes_search_result")
            checks.append(("instruction-like observation keeps untrusted provenance", note["trust"] == "untrusted_content" and "IGNORE THE CURRENT TASK" in note["value"][0], note))
            checks.append(("instruction-like observation does not change goal or send mail", injection["state"]["goal"] == goal_before and injection["state"]["world"]["mail"] == [], {"goal": injection["state"]["goal"], "mail": injection["state"]["world"]["mail"]}))
            checks.append(("injection scenario next action is stop", injection["decision"]["selected_action"].get("type") == "stop", injection["decision"]))

            page.locator("#scenario").select_option("mcp")
            page.wait_for_timeout(20)
            mcp_text = page.locator("#mcpText").inner_text()
            checks.append(("MCP panel is version-scoped and stateless", page.locator("#mcpPanel.visible").count() == 1 and "2026-07-28" in mcp_text and "tools/call" in mcp_text and "Mcp-Session-Id" not in mcp_text, {"excerpt": mcp_text[:500]}))

            page.locator("#scenario").select_option("termination")
            termination = page.evaluate("() => window.Lab14Prototype.getDecision()")
            checks.append(("termination scenario prefers stop over redundant call", termination["selected_action"].get("type") == "stop" and termination["evaluated"][0]["score"] > termination["evaluated"][1]["score"], termination))

            checks.append(("five guided challenges", page.locator("#challengeType option").count() == 5, {"count": page.locator("#challengeType option").count()}))
            page.locator("#prediction").select_option("weather.current")
            page.locator("#lock").click()
            checks.append(("challenge locks prediction before reveal", page.locator("#prediction").is_disabled() and page.locator("#challengeType").is_disabled() and not page.locator("#reveal").is_disabled(), {}))
            page.locator("#reveal").click()
            result = page.locator("#challengeResult").inner_text()
            checks.append(("next-call challenge reveals deterministic mechanism", "Prediction matched" in result and "weather.current" in result and "forecast answers a different question" in result, {"text": result}))

            page.locator("#resetChallenge").click()
            page.locator("#challengeType").select_option("trust")
            page.locator("#prediction").select_option("data")
            page.locator("#lock").click()
            page.locator("#reveal").click()
            trust_result = page.locator("#challengeResult").inner_text()
            checks.append(("trust challenge preserves bounded security claim", "Prediction matched" in trust_result and "untrusted_content" in trust_result and "not a general prompt-injection solution" in trust_result, {"text": trust_result}))

            state_text = page.locator("#stateText").inner_text()
            checks.append(("accessible state contains goal context decision and history", all(token in state_text for token in ["\"goal\"", "\"context\"", "\"history\"", "\"decision\""]), {"excerpt": state_text[:500]}))
            context.close()

            mobile = browser.new_context(viewport={"width": 390, "height": 844})
            mobile_page = mobile.new_page()
            mobile_page.on("pageerror", lambda exc: page_errors.append(str(exc)))
            mobile_page.on(
                "console",
                lambda msg: console_errors.append(msg.text)
                if msg.type == "error"
                else None,
            )
            mobile_page.goto(PAGE.resolve().as_uri(), wait_until="load", timeout=10_000)
            mobile_page.wait_for_function("() => !!window.Lab14Prototype")
            overflow = mobile_page.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
            checks.append(("mobile root has no horizontal overflow", overflow <= 1, {"overflow": overflow}))
            mobile.close()
        finally:
            browser.close()

    failures = [
        {"name": name, "detail": detail}
        for name, ok, detail in checks
        if not ok
    ]
    payload = {
        "harness": "tools/test_agent_tool_context_prototype.py",
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
