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
        "Temperature rescales fixed logits before softmax",
        "causal mask",
        "structural constraint",
        "The model stores complete answers and retrieves them",
        "Accessible numeric state",
        "Q/K perturbation",
        "finite-ablation",
        "Guided Challenges",
        "Scaled scores q·k / √dₖ",
        "Causal mask",
        "Attention weights after softmax",
    )
    for phrase in required_source:
        checks.append((f"source contract: {phrase}", phrase in source, {}))

    checks.append(
        ("single-file candidate has no external script", "<script src=" not in source, {})
    )
    checks.append(
        (
            "candidate has no fetch/XHR dependency",
            "fetch(" not in source and "XMLHttpRequest" not in source,
            {},
        )
    )
    checks.append(
        (
            "candidate is outside public playgrounds",
            PAGE.parent.name == "tools" and "playgrounds" not in PAGE.parts[-2:],
            {"path": str(PAGE)},
        )
    )

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

            checks.append(
                (
                    "four pipeline stages",
                    page.locator(".stage").count() == 4,
                    {"count": page.locator(".stage").count()},
                )
            )
            checks.append(
                (
                    "canonical token strip",
                    page.locator(".token").count() == 4,
                    {"count": page.locator(".token").count()},
                )
            )
            checks.append(
                (
                    "12 vocabulary rows",
                    page.locator(".bar-row").count() == 12,
                    {"count": page.locator(".bar-row").count()},
                )
            )
            vectors_text = page.locator("#vectors").inner_text()
            checks.append(
                (
                    "embedding and position are visible",
                    "embedding" in vectors_text and "position" in vectors_text,
                    {},
                )
            )

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
            checks.append(
                (
                    "canonical embedded-core fixture",
                    all(abs(a - b) < 1e-12 for a, b in zip(canonical, expected)),
                    {"actual": canonical},
                )
            )

            # The raw scaled-score matrix, structural mask, and post-softmax
            # attention weights are separate views of the same four-token state.
            checks.append(
                (
                    "score matrix exposes all 16 pre-mask scores",
                    page.locator("#scoreMatrix td").count() == 16
                    and "MASK" not in page.locator("#scoreMatrix").inner_text(),
                    {"count": page.locator("#scoreMatrix td").count()},
                )
            )
            checks.append(
                (
                    "causal mask is a separate structural matrix",
                    page.locator("#maskMatrix td").count() == 16
                    and "MASK" in page.locator("#maskMatrix").inner_text()
                    and "ALLOW" in page.locator("#maskMatrix").inner_text(),
                    {"text": page.locator("#maskMatrix").inner_text()[:240]},
                )
            )
            masked_text = (
                page.locator("#matrix tr").nth(1).locator("td").nth(1).inner_text()
            )
            checks.append(
                ("future source visibly masked", masked_text == "MASK", {"text": masked_text})
            )

            # Permitted attention cells are keyboard-operable and update the same
            # synchronized numeric/text state as pointer selection.
            permitted_cells = page.locator("#matrix .cell-btn")
            checks.append(
                (
                    "permitted matrix cells are interactive controls",
                    permitted_cells.count() == 10,
                    {"count": permitted_cells.count()},
                )
            )
            first_cell = permitted_cells.first
            first_cell.focus()
            first_cell.press("Enter")
            pair_text = page.locator("#pairDetail").inner_text()
            checks.append(
                (
                    "keyboard attention-cell inspection updates pair detail",
                    "Raw q·k" in pair_text
                    and "q·k/√dₖ" in pair_text
                    and "attention weight" in pair_text,
                    {"text": pair_text},
                )
            )

            state_text = page.locator("#stateText").inner_text()
            checks.append(
                (
                    "text-equivalent state covers required numeric layers",
                    all(
                        term in state_text
                        for term in (
                            "query q:",
                            "source keys:",
                            "raw scaled scores:",
                            "causal mask row:",
                            "masked/unmasked scores:",
                            "attention row:",
                            "logits:",
                            "probabilities:",
                            "temperature:",
                            "position information:",
                            "causal mask:",
                        )
                    ),
                    {"state": state_text[:500]},
                )
            )

            # Constrained learner text exercises <UNK>, punctuation tokenization,
            # and the six-token context boundary while retaining <BOS>.
            page.locator("#customPrompt").fill("I adore cats.")
            page.locator("#applyCustom").click()
            custom_tokens = page.locator(".token").all_inner_texts()
            custom_note = page.locator("#customNote").inner_text()
            checks.append(
                (
                    "custom text exposes unknown-token behavior",
                    any("<UNK>" in token for token in custom_tokens)
                    and any("." in token for token in custom_tokens)
                    and "1 unknown piece" in custom_note,
                    {"tokens": custom_tokens, "note": custom_note},
                )
            )

            page.locator("#customPrompt").fill(
                "i like cats dogs sleep play run because"
            )
            page.locator("#applyCustom").click()
            long_tokens = page.locator(".token").all_inner_texts()
            long_note = page.locator("#customNote").inner_text()
            checks.append(
                (
                    "custom text enforces max context and preserves BOS",
                    len(long_tokens) == 6
                    and "<BOS>" in long_tokens[0]
                    and "context truncated to 6 tokens" in long_note,
                    {"tokens": long_tokens, "note": long_note},
                )
            )

            # Each frozen scenario must expose a real arithmetic mechanism.
            page.locator("#scenario").select_option("qk")
            page.wait_for_timeout(20)
            qk_note = page.locator("#scenarioNote").inner_text()
            qk_delta = page.evaluate(
                """() => {
                  const C=window.TransformerLanguageModelCore;
                  const a=C.forwardText('I like cats');
                  const b=C.forwardWithPerturbation('I like cats',{},'q0');
                  return Math.abs(a.rawScores.at(-1)[3]-b.rawScores.at(-1)[3]);
                }"""
            )
            checks.append(
                (
                    "Q/K perturbation changes a scaled score",
                    qk_delta > 1e-6
                    and "final query q[0] is increased by 0.50" in qk_note,
                    {"delta": qk_delta, "note": qk_note},
                )
            )

            page.locator("#scenario").select_option("order")
            page.wait_for_timeout(20)
            order_note = page.locator("#scenarioNote").inner_text()
            checks.append(
                (
                    "order/position scenario exposes ablation result",
                    "positions on" in order_note and "positions off" in order_note,
                    {"note": order_note},
                )
            )

            page.locator("#scenario").select_option("mask")
            page.wait_for_timeout(20)
            mask_note = page.locator("#scenarioNote").inner_text()
            checks.append(
                ("mask-leak scenario disables mask", not page.locator("#mask").is_checked(), {})
            )
            checks.append(
                (
                    "mask-leak scenario names autoregressive violation",
                    "autoregressive dependency constraint" in mask_note,
                    {"note": mask_note},
                )
            )
            checks.append(
                (
                    "mask-off matrix marks all sources allowed",
                    "MASK" not in page.locator("#maskMatrix").inner_text(),
                    {"text": page.locator("#maskMatrix").inner_text()[:240]},
                )
            )

            page.locator("#scenario").select_option("temperature")
            page.wait_for_timeout(20)
            temp_note = page.locator("#scenarioNote").inner_text()
            checks.append(
                (
                    "temperature scenario sets T=2",
                    page.locator("#temperature").input_value() == "2",
                    {},
                )
            )
            checks.append(
                (
                    "temperature scenario reports entropy with fixed logits",
                    "entropy rises" in temp_note and "logits stay fixed" in temp_note,
                    {"note": temp_note},
                )
            )

            page.locator("#scenario").select_option("explanation")
            page.wait_for_timeout(20)
            explanation_note = page.locator("#scenarioNote").inner_text()
            ablation = page.evaluate(
                """() => {
                  const a=window.TransformerLanguageModelCore.finiteAttentionAblation('sleep sleep i');
                  return {weight:a.largestWeight.index,impact:a.largestImpact.index,top:a.topToken};
                }"""
            )
            checks.append(
                (
                    "attention-not-explanation has executable counterexample",
                    ablation["weight"] != ablation["impact"]
                    and "largest final-row attention weight" in explanation_note
                    and "largest finite-ablation effect" in explanation_note
                    and "not a complete causal explanation" in explanation_note,
                    {"ablation": ablation, "note": explanation_note},
                )
            )

            # Challenge fixtures are isolated from arbitrary experiment state.
            challenge_labels = page.locator("#prediction option").all_inner_texts()
            checks.append(
                (
                    "challenge 1 options remain bound to canonical fixture",
                    any("cats @ 3" in label for label in challenge_labels),
                    {"options": challenge_labels},
                )
            )

            def run_challenge(kind: str, choice: str) -> str:
                page.locator("#challengeType").select_option(kind)
                page.locator("#prediction").select_option(choice)
                page.locator("#lock").click()
                assert page.locator("#prediction").is_disabled()
                assert page.locator("#challengeType").is_disabled()
                assert not page.locator("#reveal").is_disabled()
                page.locator("#reveal").click()
                text = page.locator("#challengeResult").inner_text()
                page.locator("#resetChallenge").click()
                return text

            attention_challenge = run_challenge("attention", "3")
            checks.append(
                (
                    "challenge 1 reveals score and attention rows",
                    "prediction matched" in attention_challenge
                    and "Scaled-score row:" in attention_challenge
                    and "Attention row:" in attention_challenge,
                    {"text": attention_challenge},
                )
            )

            mask_challenge = run_challenge("mask", "future")
            checks.append(
                (
                    "challenge 2 predicts causal-mask leakage",
                    "prediction matched" in mask_challenge
                    and "later source positions" in mask_challenge
                    and "Transfer:" in mask_challenge,
                    {"text": mask_challenge},
                )
            )

            substitution_challenge = run_challenge("substitution", "local-increase")
            checks.append(
                (
                    "challenge 3 predicts QKV scope and probability direction",
                    "prediction matched" in substitution_challenge
                    and "Earlier-position Q/K/V max Δ" in substitution_challenge
                    and "substituted-position Q/K/V max Δ" in substitution_challenge
                    and "P(sleep):" in substitution_challenge
                    and "Transfer:" in substitution_challenge,
                    {"text": substitution_challenge},
                )
            )

            temperature_challenge = run_challenge("temperature", "flatter")
            checks.append(
                (
                    "challenge 4 predicts temperature transfer",
                    "prediction matched" in temperature_challenge
                    and "Entropy:" in temperature_challenge
                    and "Logits are identical" in temperature_challenge
                    and "Transfer:" in temperature_challenge,
                    {"text": temperature_challenge},
                )
            )

            # Small-screen rendering remains bounded; each matrix owns its overflow
            # instead of widening the document.
            page.set_viewport_size({"width": 390, "height": 844})
            page.wait_for_timeout(30)
            body_width = page.evaluate("() => document.documentElement.scrollWidth")
            checks.append(
                (
                    "mobile candidate has no material horizontal overflow",
                    body_width <= 410,
                    {"scrollWidth": body_width},
                )
            )

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
