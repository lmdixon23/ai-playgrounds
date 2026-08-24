#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import shutil

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
            context = browser.new_context(viewport={"width": 1280, "height": 1000})
            page = context.new_page()
            page.on("pageerror", lambda exc: page_errors.append(str(exc)))
            page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            page.goto(PAGE.resolve().as_uri(), wait_until="load", timeout=10_000)
            page.wait_for_function("() => !!window.TransformerLanguageModelCore")

            checks.append(("four pipeline stages", page.locator(".stage").count() == 4, {"count": page.locator(".stage").count()}))
            checks.append(("six required scenarios", page.locator("#scenario option").count() == 6, {"count": page.locator("#scenario option").count()}))
            checks.append(("four guided challenges", page.locator("#challengeType option").count() == 4, {"count": page.locator("#challengeType option").count()}))
            checks.append(("canonical tokens", page.locator(".token").count() == 4, {"count": page.locator(".token").count()}))
            checks.append(("12 vocabulary bars", page.locator(".bar-row").count() == 12, {"count": page.locator(".bar-row").count()}))
            checks.append(("vector inspector exposes full block state", page.locator("#vectors .vector-row").count() >= 10, {"count": page.locator("#vectors .vector-row").count()}))

            # Frozen canonical arithmetic remains visible in the browser.
            last_attention = page.evaluate("() => window.TransformerLanguageModelCore.forwardText('I like cats').attention.at(-1)")
            expected = [0.20366059441088602, 0.24469312034003501, 0.2459995865850857, 0.3056466986639933]
            checks.append(("canonical attention fixture", all(abs(a-b) < 1e-12 for a,b in zip(last_attention, expected)), {"actual": last_attention}))

            score_text = page.locator("#scoreEquation").inner_text()
            checks.append(("score inspector shows dot product and scaling", "√4" in score_text and "attention weight" in score_text, {"text": score_text}))

            accessible = page.locator("#accessibleState").inner_text()
            checks.append(("text-equivalent state includes core numeric layers", all(term in accessible for term in ("Prompt:", "Q:", "K(source):", "Scaled score:", "Attention row:", "Final logits:", "Next-token probabilities:")), {"text": accessible[:500]}))

            # The causal mask makes future cells unavailable in earlier rows.
            masked_text = page.locator("#matrix tr").nth(1).locator("td").nth(1).inner_text()
            checks.append(("future cell visibly masked", masked_text == "MASK", {"text": masked_text}))
            page.locator("#mask").uncheck()
            page.wait_for_timeout(40)
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

            # Scenario layer must expose the required mechanism families rather than decorative presets.
            page.locator("#scenario").select_option("mask")
            page.wait_for_timeout(40)
            checks.append(("mask-ablation scenario changes model control", not page.locator("#mask").is_checked() and page.locator("#matrix tr").nth(1).locator("td").nth(2).inner_text() != "MASK", {"finding": page.locator("#scenarioFinding").inner_text()}))

            page.locator("#scenario").select_option("order")
            page.wait_for_timeout(40)
            order_finding = page.locator("#scenarioFinding").inner_text()
            checks.append(("order scenario reports position comparison", "positions off" in order_finding and "positions on" in order_finding, {"finding": order_finding}))

            page.locator("#scenario").select_option("temperature")
            page.wait_for_timeout(40)
            temp_finding = page.locator("#scenarioFinding").inner_text()
            checks.append(("temperature scenario reports fixed-logit entropy comparison", "logits are identical" in temp_finding.lower() and "T=0.5" in temp_finding and "T=2.0" in temp_finding, {"finding": temp_finding}))

            page.locator("#scenario").select_option("attentionLimit")
            page.wait_for_timeout(40)
            limit_finding = page.locator("#scenarioFinding").inner_text()
            checks.append(("attention-not-explanation counterexample", "dogs" in limit_finding and "sleep" in limit_finding and "different quantities" in limit_finding, {"finding": limit_finding}))

            # Challenge 1: result cannot be revealed before prediction lock.
            page.locator("#scenario").select_option("canonical")
            page.locator("#challengeType").select_option("attention")
            page.wait_for_timeout(40)
            checks.append(("challenge reveal initially disabled", page.locator("#reveal").is_disabled(), {}))
            page.locator("#prediction").select_option("3")
            page.locator("#lock").click()
            checks.append(("prediction immutable after lock", page.locator("#prediction").is_disabled() and page.locator("#lock").is_disabled(), {}))
            checks.append(("reveal enabled after lock", not page.locator("#reveal").is_disabled(), {}))
            page.locator("#reveal").click()
            challenge_text = page.locator("#challengeResult").inner_text()
            checks.append(("attention reveal identifies canonical highest source", "Prediction matched." in challenge_text and "cats at position 3" in challenge_text and "0.3056" in challenge_text, {"text": challenge_text}))

            # Challenge 2: causal-mask leak is tested using a counterfactual unmasked run.
            page.locator("#challengeType").select_option("maskLeak")
            page.locator("#prediction").select_option("future")
            page.locator("#lock").click()
            page.locator("#reveal").click()
            mask_challenge = page.locator("#challengeResult").inner_text()
            checks.append(("mask-leak challenge exposes future contribution", "Prediction matched." in mask_challenge and "With the mask removed" in mask_challenge, {"text": mask_challenge}))

            # Challenge 3: substitution direction is determined by the frozen model, not a hard-coded UI answer.
            page.locator("#challengeType").select_option("substitution")
            page.locator("#prediction").select_option("increase")
            page.locator("#lock").click()
            page.locator("#reveal").click()
            substitution_challenge = page.locator("#challengeResult").inner_text()
            checks.append(("substitution challenge traces probability change", "Prediction matched." in substitution_challenge and "P(sleep) changes" in substitution_challenge and "Δ =" in substitution_challenge, {"text": substitution_challenge}))

            # Challenge 4: lowering temperature sharpens without mutating logits.
            page.locator("#challengeType").select_option("temperature")
            page.locator("#prediction").select_option("sharper")
            page.locator("#lock").click()
            page.locator("#reveal").click()
            temperature_challenge = page.locator("#challengeResult").inner_text()
            checks.append(("temperature challenge uses entropy mechanism", "Prediction matched." in temperature_challenge and "Logits are unchanged" in temperature_challenge and "entropy" in temperature_challenge.lower(), {"text": temperature_challenge}))

            # Matrix cells are keyboard-focusable and selecting one synchronizes the score inspector.
            first_numeric = page.locator("#matrix tr").nth(4).locator("td").nth(1)
            checks.append(("attention cells keyboard focusable", first_numeric.get_attribute("tabindex") == "0", {"tabindex": first_numeric.get_attribute("tabindex")}))
            first_numeric.click()
            page.wait_for_timeout(20)
            checks.append(("matrix selection synchronizes token/source inspector", page.locator("#sourceToken").input_value() == "1" and "q3 · k1" in page.locator("#scoreEquation").inner_text(), {"score": page.locator("#scoreEquation").inner_text()}))

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
