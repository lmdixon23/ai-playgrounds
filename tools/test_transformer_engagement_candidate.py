#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "release-evidence" / "lab13-engagement-candidate.html"


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
        [sys.executable, str(ROOT / "tools" / "build_transformer_engagement_candidate.py"), "--output", str(OUTPUT)],
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
    checks.append(("engagement layer is embedded", "Lab13EngagementExperience" in source and "lab13-eq-flowline" in source and "lab13-eq-compare-body" in source, {}))
    checks.append(("explicit deterministic continuation language is present", "Append argmax token" in source and "It is not sampling" in source, {}))
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
            page.wait_for_function("() => !!window.Lab13EngagementExperience")

            checks.append(("state-derived four-stage flow is visible", page.locator("#lab13-eq-flowline .lab13-eq-node").count() == 4 and page.locator("#lab13-eq-flowline").is_visible(), {"nodes": page.locator("#lab13-eq-flowline .lab13-eq-node").count()}))

            canonical = page.evaluate("() => window.TransformerLanguageModelCore.forwardText('I like cats').attention.at(-1)")
            expected = [0.20366059441088602, 0.24469312034003501, 0.2459995865850857, 0.3056466986639933]
            checks.append(("frozen Transformer arithmetic remains unchanged", all(abs(a-b) < 1e-12 for a,b in zip(canonical, expected)), {"attention": canonical}))

            snapshot = page.evaluate("() => window.Lab13EngagementExperience.snapshot()")
            direct = page.evaluate("""() => {
              const C=window.TransformerLanguageModelCore;
              const r=C.forwardWithPerturbation(document.querySelector('#customPrompt').value,{usePositions:document.querySelector('#positions').checked,causalMask:document.querySelector('#mask').checked,temperature:Number(document.querySelector('#temperature').value)},document.querySelector('#perturb').value);
              const top=C.topTokens(r,1)[0];return {topToken:top[0],topProbability:top[1],probabilities:r.probabilities,attention:r.attention.at(-1)};
            }""")
            checks.append(("engagement flow derives from canonical model state", snapshot["topToken"] == direct["topToken"] and abs(snapshot["topProbability"]-direct["topProbability"]) < 1e-12 and max(abs(a-b) for a,b in zip(snapshot["attention"], direct["attention"])) < 1e-12, {"snapshot": snapshot, "directTop": direct["topToken"]}))

            model_before_baseline = page.evaluate("() => document.querySelector('#stateText').textContent")
            page.click("#lab13-eq-save")
            baseline = page.evaluate("() => window.Lab13EngagementExperience.getBaseline()")
            model_after_baseline = page.evaluate("() => document.querySelector('#stateText').textContent")
            checks.append(("saving comparison baseline is presentation-only", bool(baseline) and model_before_baseline == model_after_baseline, {"baselineTop": baseline["topToken"] if baseline else None}))

            page.locator("#temperature").evaluate("(el) => {el.value='2';el.dispatchEvent(new Event('input',{bubbles:true}))}")
            page.wait_for_timeout(50)
            compare_text = page.locator("#lab13-eq-compare-body").inner_text()
            current = page.evaluate("() => window.Lab13EngagementExperience.snapshot()")
            checks.append(("baseline comparison reacts to a real model control", current["temperature"] == 2 and "percentage points" in compare_text and page.locator(".lab13-eq-delta").count() == 5, {"compare": compare_text[:500]}))

            page.locator("#temperature").evaluate("(el) => {el.value='1';el.dispatchEvent(new Event('input',{bubbles:true}))}")
            page.wait_for_timeout(30)
            before_append = page.evaluate("() => window.Lab13EngagementExperience.snapshot()")
            input_before = page.locator("#customPrompt").input_value()
            page.click("#lab13-eq-append")
            page.wait_for_timeout(50)
            input_after = page.locator("#customPrompt").input_value()
            after_append = page.evaluate("() => window.Lab13EngagementExperience.snapshot()")
            appendable = before_append["topToken"] != "<BOS>"
            expected_surface = "mystery" if before_append["topToken"] == "<UNK>" else before_append["topToken"]
            checks.append(("argmax continuation is explicit and deterministic", (not appendable) or (input_after == (input_before.strip()+" "+expected_surface).strip() and after_append["text"] == input_after), {"top": before_append["topToken"], "before": input_before, "after": input_after}))

            state_before_locale = page.evaluate("() => window.Lab13EngagementExperience.snapshot()")
            baseline_before_locale = page.evaluate("() => window.Lab13EngagementExperience.getBaseline()")
            page.select_option("#lab13-language-select", "es")
            page.wait_for_timeout(50)
            state_after_locale = page.evaluate("() => window.Lab13EngagementExperience.snapshot()")
            baseline_after_locale = page.evaluate("() => window.Lab13EngagementExperience.getBaseline()")
            checks.append(("locale switch preserves model and comparison state", state_before_locale == state_after_locale and baseline_before_locale == baseline_after_locale and "Sigue un estado" in page.locator("#lab13-eq-title").inner_text(), {"lang": page.locator("html").get_attribute("lang")}))
            context.close()

            reduced = browser.new_context(viewport={"width": 900, "height": 900}, reduced_motion="reduce")
            rpage = reduced.new_page()
            rpage.on("pageerror", lambda exc: page_errors.append(str(exc)))
            rpage.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            rpage.goto(OUTPUT.resolve().as_uri(), wait_until="load", timeout=10_000)
            rpage.wait_for_function("() => !!window.Lab13EngagementExperience")
            rpage.locator("#temperature").evaluate("(el) => {el.value='1.5';el.dispatchEvent(new Event('input',{bubbles:true}))}")
            rpage.wait_for_timeout(30)
            checks.append(("reduced-motion path retains state without replay animation", not rpage.locator("#lab13-eq-flowline").evaluate("el => el.classList.contains('eq-replay')") and len(rpage.locator("#lab13-eq-predict").inner_text()) > 0, {}))
            reduced.close()

            mobile = browser.new_context(viewport={"width": 390, "height": 844})
            mpage = mobile.new_page()
            mpage.on("pageerror", lambda exc: page_errors.append(str(exc)))
            mpage.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            mpage.goto(OUTPUT.resolve().as_uri() + "?lang=vi", wait_until="load", timeout=10_000)
            mpage.wait_for_function("() => !!window.Lab13EngagementExperience")
            overflow = mpage.evaluate("() => document.documentElement.scrollWidth-window.innerWidth")
            checks.append(("engagement layer fits 390px mobile", overflow <= 1 and mpage.locator("#lab13-eq-append").is_visible(), {"overflow": overflow}))
            mobile.close()
        finally:
            browser.close()

    failures = [{"name": name, "detail": detail} for name, ok, detail in checks if not ok]
    payload = {
        "harness": "tools/test_transformer_engagement_candidate.py",
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
