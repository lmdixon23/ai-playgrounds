#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILDER = ROOT / "tools" / "build_transformer_multilingual_candidate.py"
PAGE = ROOT / "release-evidence" / "lab13-transformer-multilingual-candidate.html"


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
    checks.append(("builder produced one HTML candidate", PAGE.is_file(), {"path": str(PAGE)}))
    checks.append(("candidate remains single-file", "<script src=" not in source, {}))
    checks.append(("candidate contains no runtime fetch/XHR", "fetch(" not in source and "XMLHttpRequest" not in source, {}))
    checks.append(("candidate embeds localization runtime", "window.Lab13Localization" in source and "lab13-i18n-runtime" in source, {}))
    checks.append(("candidate remains outside public playgrounds", PAGE.parent.name == "release-evidence", {"path": str(PAGE)}))

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
            page.wait_for_function("() => !!window.Lab13Localization && !!window.TransformerLanguageModelCore")

            checks.append(("four locale controls", page.locator("#lab13-locale-bar button[data-locale]").count() == 4, {"count": page.locator("#lab13-locale-bar button[data-locale]").count()}))
            checks.append(("English is initial locale", page.evaluate("() => window.Lab13Localization.getLocale()") == "en" and page.locator("html").get_attribute("lang") == "en", {}))

            # Establish non-default experiment and locked-challenge state before any
            # locale switch. Locale changes must not mutate these controls or arithmetic.
            page.locator("#customPrompt").fill("I adore cats.")
            page.locator("#applyCustom").click()
            page.locator("#positions").uncheck()
            page.locator("#temperature").fill("1.75")
            page.locator("#perturb").select_option("q0")
            page.wait_for_timeout(30)
            permitted = page.locator("#matrix .cell-btn")
            permitted.nth(permitted.count() - 1).click()
            page.locator("#challengeType").select_option("substitution")
            page.locator("#prediction").select_option("local-increase")
            page.locator("#lock").click()

            def arithmetic_snapshot() -> str:
                return page.evaluate(
                    """() => {
                      const C=window.TransformerLanguageModelCore;
                      const text=document.querySelector('#customPrompt').value;
                      const r=C.forwardWithPerturbation(text,{
                        usePositions:document.querySelector('#positions').checked,
                        causalMask:document.querySelector('#mask').checked,
                        temperature:Number(document.querySelector('#temperature').value)
                      },document.querySelector('#perturb').value);
                      return JSON.stringify({
                        tokens:r.tokens,tokenIds:r.tokenIds,inputs:r.inputs,
                        queries:r.queries,keys:r.keys,values:r.values,
                        rawScores:r.rawScores,maskedScores:r.maskedScores,
                        attention:r.attention,finalStates:r.finalStates,
                        logits:r.logits,probabilities:r.probabilities,
                        temperature:r.temperature,causalMask:r.causalMask,
                        usePositions:r.usePositions,perturbation:r.perturbation
                      });
                    }"""
                )

            def ui_state() -> dict[str, object]:
                return page.evaluate(
                    """() => ({
                      text:document.querySelector('#customPrompt').value,
                      positions:document.querySelector('#positions').checked,
                      mask:document.querySelector('#mask').checked,
                      temperature:document.querySelector('#temperature').value,
                      perturb:document.querySelector('#perturb').value,
                      challenge:document.querySelector('#challengeType').value,
                      prediction:document.querySelector('#prediction').value,
                      predictionDisabled:document.querySelector('#prediction').disabled,
                      challengeDisabled:document.querySelector('#challengeType').disabled,
                      revealDisabled:document.querySelector('#reveal').disabled,
                      activePair:document.querySelectorAll('#matrix .cell-btn.active').length
                    })"""
                )

            frozen_arithmetic = arithmetic_snapshot()
            frozen_ui = ui_state()
            checks.append(("pre-switch challenge is locked", bool(frozen_ui["predictionDisabled"]) and bool(frozen_ui["challengeDisabled"]) and not bool(frozen_ui["revealDisabled"]), frozen_ui))
            checks.append(("pre-switch matrix pair remains selected", frozen_ui["activePair"] == 1, frozen_ui))

            locale_expectations = {
                "zh": "zh-Hans",
                "vi": "vi",
                "es": "es",
                "en": "en",
            }
            for locale, html_lang in locale_expectations.items():
                page.evaluate("locale => window.Lab13Localization.setLocale(locale)", locale)
                page.wait_for_timeout(40)
                catalog_title = page.evaluate("locale => window.Lab13Localization.catalogs[locale]['page.title']", locale)
                catalog_boundary = page.evaluate("locale => window.Lab13Localization.catalogs[locale]['boundary.label']", locale)
                catalog_challenge = page.evaluate("locale => window.Lab13Localization.catalogs[locale]['challenge.title']", locale)
                body_text = page.locator("body").inner_text()
                checks.append((f"{locale} title localized", page.locator("h1").first.inner_text() == catalog_title, {"title": page.locator("h1").first.inner_text(), "expected": catalog_title}))
                checks.append((f"{locale} document language", page.locator("html").get_attribute("lang") == html_lang, {"lang": page.locator("html").get_attribute("lang")}))
                checks.append((f"{locale} major semantic surfaces localized", catalog_boundary in body_text and catalog_challenge in body_text, {"boundary": catalog_boundary, "challenge": catalog_challenge}))
                checks.append((f"{locale} locale switch preserves UI state", ui_state() == frozen_ui, {"actual": ui_state(), "expected": frozen_ui}))
                checks.append((f"{locale} locale switch preserves exact arithmetic", arithmetic_snapshot() == frozen_arithmetic, {}))
                token_text = " ".join(page.locator(".token").all_inner_texts())
                checks.append((f"{locale} model tokens remain untranslated", "<BOS>" in token_text and "<UNK>" in token_text and "." in token_text, {"tokens": token_text}))

            # Dynamic rerenders produced by the English implementation must be
            # translated by the observer rather than reverting the interface to English.
            page.evaluate("() => window.Lab13Localization.setLocale('vi')")
            page.locator("#resetChallenge").click()
            page.locator("#scenario").select_option("temperature")
            page.wait_for_timeout(80)
            vi_template = page.evaluate("() => window.Lab13Localization.catalogs.vi['scenario.temperature.note']")
            vi_prefix = vi_template.split("{cold}", 1)[0]
            vi_note = page.locator("#scenarioNote").inner_text()
            checks.append(("Vietnamese dynamic scenario rerender remains localized", vi_prefix in vi_note and "entropy rises" not in vi_note, {"text": vi_note, "prefix": vi_prefix}))

            # Challenge result is generated after localization and must translate
            # compare/mechanism/explain/transfer text while preserving model data.
            page.evaluate("() => window.Lab13Localization.setLocale('es')")
            page.locator("#challengeType").select_option("substitution")
            page.locator("#prediction").select_option("local-increase")
            page.locator("#lock").click()
            page.locator("#reveal").click()
            page.wait_for_timeout(80)
            es_compare = page.evaluate("() => window.Lab13Localization.catalogs.es['challenge.compare_match']")
            es_result = page.locator("#challengeResult").inner_text()
            checks.append(("Spanish post-switch challenge result localizes dynamically", es_compare in es_result and "P(sleep)" in es_result and "Compare: prediction matched." not in es_result, {"text": es_result}))

            # The localized text-equivalent state must retain all numerical values and
            # protected identifiers even though its labels change.
            es_state = page.locator("#stateText").inner_text()
            es_state_label = page.evaluate("() => window.Lab13Localization.catalogs.es['state.logits']")
            checks.append(("Spanish text-equivalent numeric state localized", es_state_label in es_state and "logits" in es_state.lower() and "P(sleep)" not in es_state, {"state": es_state[:700]}))

            context.close()

            # Responsive root containment for every locale. Wide matrices may scroll
            # inside their own wrappers but must not force document-level overflow.
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
            mobile_page.wait_for_function("() => !!window.Lab13Localization")
            for locale in ("en", "zh", "vi", "es"):
                mobile_page.evaluate("locale => window.Lab13Localization.setLocale(locale)", locale)
                mobile_page.wait_for_timeout(30)
                overflow = mobile_page.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
                checks.append((f"{locale} mobile root has no horizontal overflow", overflow <= 1, {"overflow": overflow}))
            mobile.close()
        finally:
            browser.close()

    failures = [
        {"name": name, "detail": detail}
        for name, ok, detail in checks
        if not ok
    ]
    payload = {
        "harness": "tools/test_transformer_multilingual_applet.py",
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
