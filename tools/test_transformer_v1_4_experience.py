#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "release-evidence" / "lab13-transformer-v1.4-experience.html"


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
        [sys.executable, str(ROOT / "tools" / "build_transformer_public_v1_4.py"), "--output", str(OUTPUT)],
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
    checks.append(("v1.4 version is secondary provenance", 'name="ai-playgrounds-version" content="1.4.0"' in source and 'data-lab13-v14-provenance' in source and "v1.4.0" in source, {}))
    checks.append(("prominent v1.3 badge removed", "AI Playgrounds v1.3" not in source, {}))
    checks.append(("v1.4 experience runtime embedded", "Lab13V14Experience" in source and "lab13-language-select" in source and "lab13-mechanism-journey" in source, {}))
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
            page.wait_for_function("() => !!window.Lab13Localization && !!window.Lab13V14Experience")

            checks.append(("native language dropdown is the visible locale control", page.locator("#lab13-language-select").is_visible() and page.locator("#lab13-language-select option").count() == 4 and page.locator("#lab13-locale-bar button[data-locale]:visible").count() == 0, {"options": page.locator("#lab13-language-select option").count()}))
            checks.append(("query locale survives wrapper", page.locator("html").get_attribute("lang") == "zh-Hans" and page.locator("#lab13-language-select").input_value() == "zh", {"lang": page.locator("html").get_attribute("lang"), "select": page.locator("#lab13-language-select").input_value()}))
            checks.append(("four mechanism stages are interactive", page.locator(".pipeline .stage.lab13-journey-stage").count() == 4 and page.locator("#lab13-mechanism-journey").is_visible(), {"stages": page.locator(".pipeline .stage.lab13-journey-stage").count()}))

            canonical = page.evaluate("() => window.TransformerLanguageModelCore.forwardText('I like cats').attention.at(-1)")
            expected = [0.20366059441088602, 0.24469312034003501, 0.2459995865850857, 0.3056466986639933]
            checks.append(("frozen Transformer arithmetic is unchanged", all(abs(a-b) < 1e-12 for a,b in zip(canonical, expected)), {"attention": canonical}))

            before = page.evaluate("""() => ({
              prompt: document.querySelector('#prompt').value,
              custom: document.querySelector('#customPrompt').value,
              positions: document.querySelector('#positions').checked,
              mask: document.querySelector('#mask').checked,
              temperature: document.querySelector('#temperature').value,
              perturb: document.querySelector('#perturb').value,
              scenario: document.querySelector('#scenario').value,
              challenge: document.querySelector('#challengeType').value,
              prediction: document.querySelector('#prediction').value,
              revealDisabled: document.querySelector('#reveal').disabled
            })""")
            page.evaluate("() => window.Lab13V14Experience.setStage(2)")
            after_stage = page.evaluate("""() => ({
              prompt: document.querySelector('#prompt').value,
              custom: document.querySelector('#customPrompt').value,
              positions: document.querySelector('#positions').checked,
              mask: document.querySelector('#mask').checked,
              temperature: document.querySelector('#temperature').value,
              perturb: document.querySelector('#perturb').value,
              scenario: document.querySelector('#scenario').value,
              challenge: document.querySelector('#challengeType').value,
              prediction: document.querySelector('#prediction').value,
              revealDisabled: document.querySelector('#reveal').disabled
            })""")
            checks.append(("journey focus is presentation-only", before == after_stage and page.evaluate("() => window.Lab13V14Experience.getStage()") == 2 and page.locator(".lab13-focus-target").count() >= 1, {"before": before, "after": after_stage, "focusTargets": page.locator(".lab13-focus-target").count()}))

            page.select_option("#lab13-language-select", "vi")
            page.wait_for_timeout(40)
            after_locale = page.evaluate("""() => ({
              prompt: document.querySelector('#prompt').value,
              custom: document.querySelector('#customPrompt').value,
              positions: document.querySelector('#positions').checked,
              mask: document.querySelector('#mask').checked,
              temperature: document.querySelector('#temperature').value,
              perturb: document.querySelector('#perturb').value,
              scenario: document.querySelector('#scenario').value,
              challenge: document.querySelector('#challengeType').value,
              prediction: document.querySelector('#prediction').value,
              revealDisabled: document.querySelector('#reveal').disabled
            })""")
            checks.append(("dropdown locale switch preserves learner state", before == after_locale and page.locator("html").get_attribute("lang") == "vi" and page.evaluate("() => window.Lab13V14Experience.getStage()") == 2, {"lang": page.locator("html").get_attribute("lang"), "state": after_locale}))
            checks.append(("locale switch updates shareable query", "lang=vi" in page.url, {"url": page.url}))
            checks.append(("version remains visible but secondary", page.locator(".badge").inner_text() == "AI Playgrounds" and "v1.4.0" in page.locator(".lab13-provenance").inner_text(), {"badge": page.locator(".badge").inner_text(), "footer": page.locator(".lab13-provenance").inner_text()}))
            context.close()

            mobile = browser.new_context(viewport={"width": 390, "height": 844})
            mpage = mobile.new_page()
            mpage.on("pageerror", lambda exc: page_errors.append(str(exc)))
            mpage.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            mpage.goto(OUTPUT.resolve().as_uri() + "?lang=es", wait_until="load", timeout=10_000)
            mpage.wait_for_function("() => !!window.Lab13V14Experience")
            overflow = mpage.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
            checks.append(("v1.4 Transformer experience fits 390px mobile", overflow <= 1 and mpage.locator("#lab13-language-select").is_visible(), {"overflow": overflow}))
            mobile.close()
        finally:
            browser.close()

    failures = [{"name": name, "detail": detail} for name, ok, detail in checks if not ok]
    payload = {
        "harness": "tools/test_transformer_v1_4_experience.py",
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
