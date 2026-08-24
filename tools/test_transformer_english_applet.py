#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAGE = ROOT / "tools" / "transformer_language_model_applet_en.html"


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
    checks: list[tuple[str, bool, object]] = []

    required_source = (
        "toy deterministic model",
        "Attention is not an explanation",
        "source-locked toy tokenizer",
        "Temperature rescales the fixed logits before softmax",
        "causal mask",
        "structural constraint",
        "The model stores complete answers and retrieves them",
        "Accessible numeric state",
    )
    for phrase in required_source:
        checks.append((f"source contract: {phrase}", phrase in source, {}))

    checks.append(("single-file candidate has no external script", "<script src=" not in source, {}))
    checks.append(("candidate has no fetch/XHR dependency", "fetch(" not in source and "XMLHttpRequest" not in source, {}))
    checks.append(("candidate is not under public playgrounds", "tools/transformer_language_model_applet_en.html" in str(PAGE).replace("\\", "/"), {}))

    page_errors: list[str] = []
    console_errors: list[str] = []

    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("Playwright required") from exc

    with sync_playwright() as p:
        browser = launch(p)
        try:
            context = browser.new_context(viewport={"width": 1280, "height": 900})
            page = context.new_page()
            page.on("pageerror", lambda exc: page_errors.append(str(exc)))
            page.on(
                "console",
                lambda msg: console_errors.append(msg.text)
                if msg.type == "error"
                else None,
            )
            page.goto(PAGE.resolve().as_uri(), wait_until="load", timeout=10_000)
            page.wait_for_function("() => !!window.TransformerLanguageModelCore")

            checks.append(("four pipeline stages", page.locator(".stage").count() == 4, {"count": page.locator(".stage").count()}))
            checks.append(("canonical token strip", page.locator(".token").count() == 4, {"count": page.locator(".token").count()}))
            checks.append(("12 vocabulary rows", page.locator(".bar-row").count() == 12, {"count": page.locator(".bar-row").count()}))
            checks.append(("embedding and position are visible", "embedding" in page.locator("#vectors").inner_text() and "position" in page.locator("#vectors").inner_text(), {}))

            canonical = page.evaluate(
                "() => window.TransformerLanguageModelCore.forwardText('I like cats')"
                ".attention.at(-1)"
            )
            expected = [
                0.20366059441088602,
                0.24469312034003501,
                0.2459995865850857,
                0.3056466986639933,
            ]
            checks.append(("canonical embedded-core fixture", all(abs(a - b) < 1e-12 for a, b in zip(canonical, expected)), {"actual": canonical}))

            masked_text = page.locator("#matrix tr").nth(1).locator("td").nth(1).inner_text()
            checks.append(("future source visibly masked", masked_text == "MASK", {"text": masked_text}))

            state_text = page.locator("#stateText").inner_text()
            checks.append(("text-equivalent state includes q/logits/probabilities", all(term in state_text for term in ("query q:", "logits:", "probabilities:")), {"state": state_text[:260]}))

            page.locator("#scenario").select_option("order")
            page.wait_for_timeout(30)
            order_note = page.locator("#scenarioNote").inner_text()
            checks.append(("order/position scenario exposes ablation result", "positions on" in order_note and "positions off" in order_note, {"note": order_note}))

            page.locator("#scenario").select_option("mask")
            page.wait_for_timeout(30)
            mask_note = page.locator("#scenarioNote").inner_text()
            checks.append(("mask-leak scenario disables mask", not page.locator("#mask").is_checked(), {}))
            checks.append(("mask-leak scenario names autoregressive violation", "autoregressive dependency constraint" in mask_note, {"note": mask_note}))

            page.locator("#scenario").select_option("temperature")
            page.wait_for_timeout(30)
            temp_note = page.locator("#scenarioNote").inner_text()
            checks.append(("temperature scenario sets T=2", page.locator("#temperature").input_value() == "2", {}))
            checks.append(("temperature scenario reports entropy comparison", "entropy rises" in temp_note and "logits stay fixed" in temp_note, {"note": temp_note}))

            page.locator("#scenario").select_option("canonical")
            page.wait_for_timeout(30)
            checks.append(("challenge reveal initially disabled", page.locator("#reveal").is_disabled(), {}))
            page.locator("#prediction").select_option("3")
            page.locator("#lock").click()
            checks.append(("prediction immutable after commit", page.locator("#prediction").is_disabled() and page.locator("#lock").is_disabled(), {}))
            checks.append(("reveal enabled after commit", not page.locator("#reveal").is_disabled(), {}))
            page.locator("#reveal").click()
            challenge = page.locator("#challengeResult").inner_text()
            checks.append(("challenge reveals score and weight rows", "Scaled-score row:" in challenge and "Attention row:" in challenge, {"text": challenge}))
            checks.append(("canonical challenge winner is cats", "cats at position 3" in challenge and "0.3056" in challenge, {"text": challenge}))

            # Small-screen rendering remains usable at the candidate stage.
            page.set_viewport_size({"width": 390, "height": 844})
            page.wait_for_timeout(30)
            body_width = page.evaluate("() => document.documentElement.scrollWidth")
            checks.append(("mobile candidate has no material horizontal overflow", body_width <= 410, {"scrollWidth": body_width}))

            context.close()
        finally:
            browser.close()

    failures = [
        {"name": name, "detail": detail}
        for name, ok, detail in checks
        if not ok
    ]
    payload = {
        "harness": "tools/test_transformer_english_applet.py",
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
