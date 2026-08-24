#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAGE = ROOT / "tools" / "transformer_language_model_prototype.html"


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
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("Playwright required") from exc

    checks = []
    page_errors = []
    console_errors = []

    with sync_playwright() as p:
        browser = launch(p)
        try:
            context = browser.new_context(viewport={"width": 1280, "height": 900})
            page = context.new_page()
            page.on("pageerror", lambda exc: page_errors.append(str(exc)))
            page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            page.goto(PAGE.resolve().as_uri(), wait_until="load", timeout=10_000)
            page.wait_for_function("() => !!window.TransformerLanguageModelCore")

            checks.append(("four pipeline stages", page.locator(".stage").count() == 4, {"count": page.locator(".stage").count()}))
            checks.append(("canonical tokens", page.locator(".token").count() == 4, {"count": page.locator(".token").count()}))
            checks.append(("12 vocabulary bars", page.locator(".bar-row").count() == 12, {"count": page.locator(".bar-row").count()}))

            # Frozen canonical arithmetic visible in browser.
            last_attention = page.evaluate("() => window.TransformerLanguageModelCore.forwardText('I like cats').attention.at(-1)")
            expected = [0.20366059441088602, 0.24469312034003501, 0.2459995865850857, 0.3056466986639933]
            checks.append(("canonical attention fixture", all(abs(a-b) < 1e-12 for a,b in zip(last_attention, expected)), {"actual": last_attention}))

            # The causal mask makes future cells unavailable in earlier rows.
            masked_text = page.locator("#matrix tr").nth(1).locator("td").nth(1).inner_text()
            checks.append(("future cell visibly masked", masked_text == "MASK", {"text": masked_text}))
            page.locator("#mask").uncheck()
            page.wait_for_timeout(30)
            unmasked_text = page.locator("#matrix tr").nth(1).locator("td").nth(1).inner_text()
            checks.append(("mask toggle reveals numeric weight", unmasked_text != "MASK", {"text": unmasked_text}))
            page.locator("#mask").check()

            # Position ablation changes the final distribution when earlier tokens swap.
            pos_delta = page.evaluate("""() => {
              const C=window.TransformerLanguageModelCore;
              const a=C.forwardTokens(['<BOS>','i','like','cats'],{usePositions:true}).probabilities;
              const b=C.forwardTokens(['<BOS>','like','i','cats'],{usePositions:true}).probabilities;
              return Math.max(...a.map((x,i)=>Math.abs(x-b[i])));
            }""")
            no_pos_delta = page.evaluate("""() => {
              const C=window.TransformerLanguageModelCore;
              const a=C.forwardTokens(['<BOS>','i','like','cats'],{usePositions:false}).probabilities;
              const b=C.forwardTokens(['<BOS>','like','i','cats'],{usePositions:false}).probabilities;
              return Math.max(...a.map((x,i)=>Math.abs(x-b[i])));
            }""")
            checks.append(("position ablation mechanism", pos_delta > 1e-5 and no_pos_delta < 1e-12, {"with_positions": pos_delta, "without_positions": no_pos_delta}))

            # Temperature changes entropy, not logits.
            entropy = page.evaluate("""() => {
              const C=window.TransformerLanguageModelCore;
              const cold=C.forwardText('I like cats',{temperature:0.5});
              const hot=C.forwardText('I like cats',{temperature:2.0});
              return {cold:C.entropy(cold.probabilities), hot:C.entropy(hot.probabilities), logitsSame:cold.logits.every((x,i)=>x===hot.logits[i])};
            }""")
            checks.append(("temperature preserves logits and changes entropy", entropy["logitsSame"] and entropy["cold"] < entropy["hot"], entropy))

            # Guided prediction cannot reveal before lock, then compares the actual row.
            checks.append(("challenge reveal initially disabled", page.locator("#reveal").is_disabled(), {}))
            page.locator("#prediction").select_option("3")
            page.locator("#lock").click()
            checks.append(("prediction immutable after lock", page.locator("#prediction").is_disabled() and page.locator("#lock").is_disabled(), {}))
            checks.append(("reveal enabled after lock", not page.locator("#reveal").is_disabled(), {}))
            page.locator("#reveal").click()
            challenge_text = page.locator("#challengeResult").inner_text()
            checks.append(("reveal identifies canonical highest source", "cats at position 3" in challenge_text and "0.3056" in challenge_text, {"text": challenge_text}))

            # Change prompt and ensure all synchronized views update without errors.
            page.locator("#prompt").select_option("I like dogs")
            page.wait_for_timeout(30)
            tokens = page.locator(".token").all_inner_texts()
            checks.append(("prompt substitution updates token strip", any("dogs" in token for token in tokens), {"tokens": tokens}))

            context.close()
        finally:
            browser.close()

    failures = [{"name": name, "detail": detail} for name, ok, detail in checks if not ok]
    payload = {
        "harness": "tools/test_transformer_prototype.py",
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
