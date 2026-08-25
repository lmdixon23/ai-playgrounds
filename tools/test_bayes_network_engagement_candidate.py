#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "_site" / "playgrounds" / "bayes-network" / "index.html"


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


def machine_snapshot(page):
    """Exclude presentation-only timing metadata from the posterior state invariant."""
    return page.evaluate("""() => {
      const s=window.__bayesPosteriorDeltaExperience.getCurrent();
      return {preset:s.preset,vars:s.vars,labels:s.labels,evidence:s.evidence,method:s.method,post:s.post};
    }""")


def main() -> int:
    build = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "build_bayes_network_engagement_candidate.py"), "--output", str(OUTPUT)],
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
    checks.append(("candidate derives from existing posterior renderer", source.count("function inferExact(") == 1 and "__bayesPosteriorPresentationSnapshot" in source, {"inferExactDefinitions": source.count("function inferExact(")}))
    checks.append(("candidate explicitly rejects fake probability-flow semantics", "does not imply probability literally flows along graph arrows" in source, {}))
    checks.append(("sampling-noise confound is explicitly blocked", "Monte Carlo noise can move estimates" in source, {}))

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
            page.wait_for_function("() => !!window.__bayesPosteriorDeltaExperience")
            # v1.4 learning-mode and guided-challenge startup intentionally uses
            # deferred restoration. Do not mutate evidence before that settles.
            page.wait_for_timeout(500)

            initial = page.evaluate("() => window.__bayesPosteriorDeltaExperience.getCurrent()")
            checks.append(("initial exact snapshot is available without a fabricated baseline", initial["method"] == "exact" and page.evaluate("() => window.__bayesPosteriorDeltaExperience.getPrevious()") is None and page.locator(".bayes-eq-prev-marker").count() == 0, {"method": initial["method"], "burglary": initial["post"]["B"]}))

            page.click("#s3")
            page.wait_for_timeout(60)
            both = page.evaluate("() => window.__bayesPosteriorDeltaExperience.getCurrent()")
            prior = page.evaluate("() => window.__bayesPosteriorDeltaExperience.getPrevious()")
            checks.append(("exact evidence change leaves the previous posterior as a ghost baseline", prior is not None and both["post"]["B"] > prior["post"]["B"] and page.locator(".bayes-eq-prev-marker").count() == len(both["vars"]), {"priorB": prior["post"]["B"] if prior else None, "bothB": both["post"]["B"], "markers": page.locator(".bayes-eq-prev-marker").count(), "evidence": both["evidence"]}))

            page.click("#s5")
            page.wait_for_timeout(60)
            with_eq = page.evaluate("() => window.__bayesPosteriorDeltaExperience.getCurrent()")
            before_eq = page.evaluate("() => window.__bayesPosteriorDeltaExperience.getPrevious()")
            b_index = with_eq["vars"].index("B")
            b_delta_text = page.locator("#postRow .infer-cell").nth(b_index).locator(".bayes-eq-delta").inner_text()
            checks.append(("explaining away becomes an exact visible downward before-after delta", before_eq is not None and with_eq["post"]["B"] < before_eq["post"]["B"] and "↓" in b_delta_text and page.locator("#postRow .infer-cell.bayes-eq-largest").count() == 1, {"beforeB": before_eq["post"]["B"] if before_eq else None, "afterB": with_eq["post"]["B"], "delta": b_delta_text, "evidence": with_eq["evidence"]}))

            state_before_sampling = page.evaluate("() => window.__bayesPosteriorDeltaExperience.getCurrent()")
            page.click("[data-m='gibbs']")
            page.wait_for_timeout(80)
            sampling = page.evaluate("() => window.__bayesPosteriorDeltaExperience.getCurrent()")
            checks.append(("sampling mode suppresses exact causal delta instead of conflating Monte Carlo noise", sampling["method"] == "gibbs" and page.evaluate("() => window.__bayesPosteriorDeltaExperience.getPrevious()") is None and page.locator(".bayes-eq-prev-marker").count() == 0 and "Monte Carlo noise" in page.locator("#bayes-eq-help").inner_text(), {"beforeMethod": state_before_sampling["method"], "afterMethod": sampling["method"], "help": page.locator("#bayes-eq-help").inner_text()}))

            page.click("[data-m='exact']")
            page.wait_for_timeout(60)
            exact_before_locale = machine_snapshot(page)
            page.select_option(".r4-language-select", "es")
            page.wait_for_timeout(180)
            exact_after_locale = machine_snapshot(page)
            locale_title = page.locator("#bayes-eq-title").inner_text()
            checks.append(("locale switch preserves Bayesian machine state", exact_before_locale == exact_after_locale, {"before": exact_before_locale, "after": exact_after_locale, "lang": page.locator("html").get_attribute("lang")}))
            checks.append(("posterior comparison surface localizes independently", "mantén visible" in locale_title.lower(), {"lang": page.locator("html").get_attribute("lang"), "title": locale_title, "locale": page.evaluate("() => window.__r4Localization.locale()"), "noTranslate": page.locator("#bayes-eq-strip").get_attribute("data-r4-no-translate")}))
            context.close()

            reduced = browser.new_context(viewport={"width": 900, "height": 900}, reduced_motion="reduce")
            rpage = reduced.new_page()
            rpage.on("pageerror", lambda exc: page_errors.append(str(exc)))
            rpage.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            rpage.goto(OUTPUT.resolve().as_uri(), wait_until="load", timeout=10_000)
            rpage.wait_for_function("() => !!window.__bayesPosteriorDeltaExperience")
            rpage.wait_for_timeout(500)
            rpage.click("#s3")
            rpage.wait_for_timeout(50)
            checks.append(("reduced-motion path retains exact numeric before-after comparison", rpage.locator(".bayes-eq-delta").count() > 0 and rpage.locator(".bayes-eq-prev-marker").count() > 0, {}))
            reduced.close()

            mobile = browser.new_context(viewport={"width": 390, "height": 844})
            mpage = mobile.new_page()
            mpage.on("pageerror", lambda exc: page_errors.append(str(exc)))
            mpage.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            mpage.goto(OUTPUT.resolve().as_uri() + "?lang=vi", wait_until="load", timeout=10_000)
            mpage.wait_for_function("() => !!window.__bayesPosteriorDeltaExperience")
            mpage.wait_for_timeout(500)
            mpage.click("#s3")
            mpage.wait_for_timeout(50)
            overflow = mpage.evaluate("() => document.documentElement.scrollWidth-window.innerWidth")
            checks.append(("posterior delta layer fits 390px mobile", overflow <= 1 and mpage.locator("#bayes-eq-strip").is_visible(), {"overflow": overflow}))
            mobile.close()
        finally:
            browser.close()

    failures = [{"name": name, "detail": detail} for name, ok, detail in checks if not ok]
    payload = {
        "harness": "tools/test_bayes_network_engagement_candidate.py",
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
