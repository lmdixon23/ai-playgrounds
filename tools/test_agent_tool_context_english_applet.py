#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILDER = ROOT / "tools" / "build_agent_tool_context_english_candidate.py"
PAGE = ROOT / "release-evidence" / "lab14-agent-tool-context-english-candidate.html"


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

    checks.append(("builder produced English candidate", PAGE.is_file(), {"path": str(PAGE)}))
    checks.append(("candidate is self-contained", "<script src=" not in source and 'id="lab14-agent-tool-context-core"' in source, {}))
    checks.append(("candidate has no runtime network primitives", all(token not in source for token in ("fetch(", "XMLHttpRequest", "WebSocket(", "EventSource(")), {}))
    checks.append(("English candidate labeling", "English source candidate:" in source and "non-public v1.3 English candidate" in source, {}))
    checks.append(("eight scenarios encoded", source.count('<option value="') >= 13 and all(value in source for value in ('value="canonical"', 'value="overlap"', 'value="invalid"', 'value="text"', 'value="permission"', 'value="injection"', 'value="mcp"', 'value="termination"')), {}))
    checks.append(("five Guided Challenges encoded", all(value in source for value in ('value="next"', 'value="gate"', 'value="observation"', 'value="trust"', 'value="stop"')), {}))

    required_semantics = [
        "Natural-language text is not an executable structured call.",
        "Availability and authorization are separate runtime states.",
        "Validation establishes only that the argument object satisfies the declared structural contract.",
        "Tool-provided content is an observation with provenance and can be untrusted data.",
        "MCP is one versioned protocol scenario; the conceptual action loop is protocol-neutral.",
        "Validation failure, authorization denial, and execution error occur at different gates.",
        "it does not solve prompt injection generally.",
        "Once the goal conditions are satisfied, termination can be the justified next action.",
    ]
    for phrase in required_semantics:
        checks.append((f"semantic safeguard: {phrase[:34]}", phrase in source, {}))

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
            page.wait_for_function("() => !!window.AgentToolContextCore && !!window.Lab14Prototype")

            checks.append(("English document language", page.locator("html").get_attribute("lang") == "en", {"lang": page.locator("html").get_attribute("lang")}))
            checks.append(("eight scenario choices", page.locator("#scenario option").count() == 8, {"count": page.locator("#scenario option").count()}))
            checks.append(("five challenge choices", page.locator("#challengeType option").count() == 5, {"count": page.locator("#challengeType option").count()}))
            checks.append(("accessible state exposed", page.locator("#stateText[aria-live='polite']").count() == 1, {}))
            checks.append(("five runtime stages", page.locator(".pipeline .stage").count() == 5, {"count": page.locator(".pipeline .stage").count()}))

            initial = page.evaluate("() => ({state:window.Lab14Prototype.getState(),decision:window.Lab14Prototype.getDecision()})")
            checks.append(("canonical initial goal active", initial["state"]["status"] == "active" and initial["state"]["step"] == 0, initial["state"]))
            checks.append(("canonical first action weather.current", initial["decision"]["selected_action"].get("name") == "weather.current", initial["decision"]["selected_action"]))

            page.locator("#step").click()
            after_weather = page.evaluate("() => ({state:window.Lab14Prototype.getState(),decision:window.Lab14Prototype.getDecision()})")
            facts1 = {item["key"]: item["value"] for item in after_weather["state"]["context"]}
            checks.append(("weather observation updates context", facts1.get("temperature_c") == 8, facts1))
            checks.append(("observation changes next action", after_weather["decision"]["selected_action"].get("name") == "unit.convert_temperature", after_weather["decision"]["selected_action"]))

            page.locator("#step").click()
            after_convert = page.evaluate("() => ({state:window.Lab14Prototype.getState(),decision:window.Lab14Prototype.getDecision()})")
            facts2 = {item["key"]: item["value"] for item in after_convert["state"]["context"]}
            checks.append(("temperature conversion exact", abs(float(facts2.get("temperature_f", -999)) - 46.4) < 1e-12, facts2))
            checks.append(("complete goal selects stop", after_convert["decision"]["selected_action"].get("type") == "stop", after_convert["decision"]["selected_action"]))

            page.locator("#step").click()
            final = page.evaluate("() => window.Lab14Prototype.getState()")
            checks.append(("canonical trace terminates", final["status"] == "complete" and final["history"][-1]["event"] == "stopped_complete", {"status": final["status"], "last": final["history"][-1]}))

            def set_scenario(value: str) -> None:
                page.locator("#scenario").select_option(value)
                page.wait_for_timeout(25)

            set_scenario("invalid")
            before = page.evaluate("() => window.Lab14Prototype.getState()")
            page.locator("#step").click()
            invalid = page.evaluate("() => window.Lab14Prototype.getState()")
            checks.append(("invalid arguments rejected before execution", invalid["history"][-1]["event"] == "rejected_invalid" and not invalid["history"][-1]["executed"], invalid["history"][-1]))
            checks.append(("invalid call produces no context side effect", invalid["context"] == before["context"], {"before": before["context"], "after": invalid["context"]}))

            set_scenario("text")
            page.locator("#step").click()
            text_state = page.evaluate("() => window.Lab14Prototype.getState()")
            checks.append(("model text does not execute", text_state["history"][-1]["event"] == "text_only" and not text_state["history"][-1]["executed"], text_state["history"][-1]))
            checks.append(("text claim cannot fabricate temperature", all(item["key"] != "temperature_c" for item in text_state["context"]), text_state["context"]))

            set_scenario("permission")
            page.locator("#step").click()
            denied = page.evaluate("() => window.Lab14Prototype.getState()")
            checks.append(("schema-valid unauthorized call denied", denied["history"][-1]["event"] == "denied_unauthorized" and denied["history"][-1]["validation"]["valid"] and not denied["history"][-1]["authorization"]["authorized"], denied["history"][-1]))
            checks.append(("permission denial prevents mail side effect", denied["world"].get("sent_mail", []) == [], denied["world"]))

            set_scenario("injection")
            injection_initial = page.evaluate("() => window.Lab14Prototype.getState()")
            page.locator("#step").click()
            injection_after = page.evaluate("() => ({state:window.Lab14Prototype.getState(),decision:window.Lab14Prototype.getDecision()})")
            note_fact = next((item for item in injection_after["state"]["context"] if item["key"] == "notes_search_result"), None)
            checks.append(("instruction-like tool content marked untrusted", bool(note_fact) and note_fact["trust"] == "untrusted_content" and note_fact["source"] == "notes.search", note_fact))
            checks.append(("untrusted observation cannot rewrite goal or principal", injection_after["state"]["goal"] == injection_initial["goal"] and injection_after["state"]["principal"] == injection_initial["principal"], {"before": [injection_initial["goal"], injection_initial["principal"]], "after": [injection_after["state"]["goal"], injection_after["state"]["principal"]]}))
            checks.append(("post-observation policy selects stop not injected mail", injection_after["decision"]["selected_action"].get("type") == "stop", injection_after["decision"]["selected_action"]))
            page.locator("#step").click()
            injection_final = page.evaluate("() => window.Lab14Prototype.getState()")
            checks.append(("injection scenario creates no mail side effect", injection_final["world"].get("sent_mail", []) == [], injection_final["world"]))

            set_scenario("mcp")
            mcp_text = page.locator("#mcpText").inner_text()
            checks.append(("MCP inspector is version-scoped", "2026-07-28" in mcp_text and "tools/call" in mcp_text and "weather.current" in mcp_text, {"text": mcp_text[:700]}))
            checks.append(("MCP stateless envelope omits prior handshake/session fields", "initialize" not in mcp_text.lower() and "session" not in mcp_text.lower(), {"text": mcp_text[:700]}))

            set_scenario("termination")
            termination_decision = page.evaluate("() => window.Lab14Prototype.getDecision()")
            checks.append(("satisfied goal prefers stop over redundant call", termination_decision["selected_action"].get("type") == "stop", termination_decision))
            page.locator("#step").click()
            termination = page.evaluate("() => window.Lab14Prototype.getState()")
            checks.append(("termination executes no tool", termination["history"][-1]["event"] == "stopped_complete" and not termination["history"][-1]["executed"], termination["history"][-1]))

            page.locator("#challengeType").select_option("gate")
            page.locator("#prediction").select_option("reject-invalid")
            page.locator("#lock").click()
            checks.append(("challenge commit freezes prediction", page.locator("#prediction").is_disabled() and page.locator("#challengeType").is_disabled() and page.locator("#reveal").is_enabled(), {}))
            page.locator("#reveal").click()
            challenge_text = page.locator("#challengeResult").inner_text()
            checks.append(("challenge reveal exposes validation mechanism", not page.locator("#challengeResult").is_hidden() and "Prediction matched" in challenge_text and "missing required property" in challenge_text, {"text": challenge_text}))
            page.locator("#resetChallenge").click()
            checks.append(("challenge reset restores prediction state", page.locator("#prediction").is_enabled() and page.locator("#reveal").is_disabled() and page.locator("#challengeResult").is_hidden(), {}))

            state_text = page.locator("#stateText").inner_text()
            checks.append(("text-equivalent state contains runtime state and decision", '"state"' in state_text and '"decision"' in state_text and '"principal"' in state_text and '"goal_conditions"' in state_text, {"excerpt": state_text[:500]}))
            checks.append(("English misconception panel present", page.locator("#model-check li").count() == 10 and page.locator("#key-terms").count() == 1, {"misconceptions": page.locator("#model-check li").count()}))

            overflow = page.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
            checks.append(("desktop root containment", overflow <= 1, {"overflow": overflow}))
            context.close()

            mobile = browser.new_context(viewport={"width": 390, "height": 844})
            mobile_page = mobile.new_page()
            mobile_page.on("pageerror", lambda exc: page_errors.append(str(exc)))
            mobile_page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            mobile_page.goto(PAGE.resolve().as_uri(), wait_until="load", timeout=10_000)
            mobile_page.wait_for_function("() => !!window.Lab14Prototype")
            mobile_overflow = mobile_page.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
            checks.append(("mobile root containment", mobile_overflow <= 1, {"overflow": mobile_overflow}))
            checks.append(("mobile retains all scenarios and challenges", mobile_page.locator("#scenario option").count() == 8 and mobile_page.locator("#challengeType option").count() == 5, {"scenarios": mobile_page.locator("#scenario option").count(), "challenges": mobile_page.locator("#challengeType option").count()}))
            mobile.close()
        finally:
            browser.close()

    failures = [{"name": name, "detail": detail} for name, ok, detail in checks if not ok]
    payload = {
        "harness": "tools/test_agent_tool_context_english_applet.py",
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
