#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
VERSION = "1.5.0"


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
        [sys.executable, str(ROOT / "tools" / "build_site_v1_5.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if build.returncode:
        print(build.stdout)
        print(build.stderr, file=sys.stderr)
        return build.returncode

    checks: list[tuple[str, bool, object]] = []
    files = sorted(path for path in SITE.rglob("*") if path.is_file())
    applets = sorted((SITE / "playgrounds").glob("*/index.html"))
    checks.append(("v1.5 artifact preserves 54-file boundary", len(files) == 54, {"files": len(files)}))
    checks.append(("v1.5 artifact preserves fourteen applets", len(applets) == 14, {"applets": [p.parent.name for p in applets]}))

    for path in applets:
        source = path.read_text(encoding="utf-8")
        checks.append((f"{path.parent.name} has v1.5 metadata", f'name="ai-playgrounds-version" content="{VERSION}"' in source, {}))

    expected = {
        "transformer-language-model": ("Lab13EngagementExperience", "lab13-eq-flowline", "lab13-eq-compare-body"),
        "agent-tool-context": ("Lab14EngagementExperience", "lab14-eq-gates", "lab14-eq-sandbox"),
        "cnf-sat": ("__cnfDpllTreeExperience", "cnf-eq-svg", "cnf-engagement-excellence-runtime"),
        "bayes-network": ("__bayesPosteriorDeltaExperience", "bayes-eq-strip", "bayes-engagement-excellence-runtime"),
    }
    for slug, markers in expected.items():
        source = (SITE / "playgrounds" / slug / "index.html").read_text(encoding="utf-8")
        checks.append((f"{slug} contains accepted engagement layer", all(marker in source for marker in markers), {"markers": markers}))

    no_change = {
        "search-pathfinding", "hill-climbing", "wumpus-world", "bayes-classifier",
        "knn-classifier", "overfitting", "neural-network", "kmeans", "convolution",
        "q-learning-gridworld",
    }
    candidate_runtime_markers = (
        "lab13-engagement-excellence-runtime",
        "lab14-engagement-excellence-runtime",
        "cnf-engagement-excellence-runtime",
        "bayes-engagement-excellence-runtime",
    )
    leaks = {}
    for slug in sorted(no_change):
        source = (SITE / "playgrounds" / slug / "index.html").read_text(encoding="utf-8")
        found = [marker for marker in candidate_runtime_markers if marker in source]
        if found:
            leaks[slug] = found
    checks.append(("ten FAS no-change applets remain free of candidate runtimes", not leaks, {"leaks": leaks}))

    landing = (SITE / "index.html").read_text(encoding="utf-8")
    notes = (SITE / "release-notes.html").read_text(encoding="utf-8")
    checks.append(("landing exposes v1.5 current provenance", "v1.5.0" in landing and 'content="1.5.0"' in landing, {}))
    checks.append(("public release notes contain v1.5 banner", "release-v1-5-0" in notes and "engagement-excellence" in notes.lower(), {}))

    page_errors: list[str] = []
    console_errors: list[str] = []
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("Playwright required") from exc

    with sync_playwright() as p:
        browser = launch(p)
        try:
            # Lab 13: public page keeps the deterministic continuation interaction.
            context = browser.new_context(viewport={"width": 1280, "height": 900})
            page = context.new_page()
            page.on("pageerror", lambda exc: page_errors.append(f"lab13: {exc}"))
            page.on("console", lambda msg: console_errors.append(f"lab13: {msg.text}") if msg.type == "error" else None)
            page.goto((SITE / "playgrounds" / "transformer-language-model" / "index.html").resolve().as_uri(), wait_until="load", timeout=10_000)
            page.wait_for_function("() => !!window.Lab13EngagementExperience")
            before = page.locator("#customPrompt").input_value()
            top = page.evaluate("() => window.Lab13EngagementExperience.snapshot().topToken")
            page.click("#lab13-eq-append")
            page.wait_for_timeout(50)
            after = page.locator("#customPrompt").input_value()
            checks.append(("public Lab 13 deterministic continuation is active", top == "<BOS>" or after != before, {"top": top, "before": before, "after": after}))
            context.close()

            # Lab 14: public page keeps the isolated learner sandbox.
            context = browser.new_context(viewport={"width": 1280, "height": 900})
            page = context.new_page()
            page.on("pageerror", lambda exc: page_errors.append(f"lab14: {exc}"))
            page.on("console", lambda msg: console_errors.append(f"lab14: {msg.text}") if msg.type == "error" else None)
            page.goto((SITE / "playgrounds" / "agent-tool-context" / "index.html").resolve().as_uri(), wait_until="load", timeout=10_000)
            page.wait_for_function("() => !!window.Lab14EngagementExperience")
            canonical_before = page.evaluate("() => window.Lab14Prototype.getState()")
            page.select_option("#lab14-eq-principal", "operator")
            page.select_option("#lab14-eq-tool", "mail.send")
            page.wait_for_timeout(20)
            page.click("#lab14-eq-run")
            page.wait_for_timeout(30)
            sandbox = page.evaluate("() => window.Lab14EngagementExperience.getSandboxState()")
            canonical_after = page.evaluate("() => window.Lab14Prototype.getState()")
            checks.append(("public Lab 14 sandbox is active and isolated", len(sandbox["world"]["mail"]) == 1 and canonical_before == canonical_after, {"sandboxWorld": sandbox["world"], "canonicalSame": canonical_before == canonical_after}))
            context.close()

            # CNF/SAT: public page exposes the tree derived from the actual trace.
            context = browser.new_context(viewport={"width": 1280, "height": 900})
            page = context.new_page()
            page.on("pageerror", lambda exc: page_errors.append(f"cnf: {exc}"))
            page.on("console", lambda msg: console_errors.append(f"cnf: {msg.text}") if msg.type == "error" else None)
            page.goto((SITE / "playgrounds" / "cnf-sat" / "index.html").resolve().as_uri(), wait_until="load", timeout=10_000)
            page.wait_for_function("() => !!window.__cnfDpllTreeExperience")
            page.wait_for_timeout(500)
            trace = page.evaluate("() => window.__cnfDpllTreeExperience.getTrace()")
            checks.append(("public CNF/SAT DPLL tree is bound to a real trace", len(trace) > 0 and page.locator("#cnf-eq-svg .cnf-eq-node").count() >= 1, {"traceLength": len(trace), "visibleNodes": page.locator("#cnf-eq-svg .cnf-eq-node").count()}))
            context.close()

            # Bayesian Network: public page exposes an exact before/after delta after startup settles.
            context = browser.new_context(viewport={"width": 1280, "height": 900})
            page = context.new_page()
            page.on("pageerror", lambda exc: page_errors.append(f"bayes: {exc}"))
            page.on("console", lambda msg: console_errors.append(f"bayes: {msg.text}") if msg.type == "error" else None)
            page.goto((SITE / "playgrounds" / "bayes-network" / "index.html").resolve().as_uri(), wait_until="load", timeout=10_000)
            page.wait_for_function("() => !!window.__bayesPosteriorDeltaExperience")
            page.wait_for_timeout(500)
            page.click("#s3")
            page.wait_for_timeout(60)
            previous = page.evaluate("() => window.__bayesPosteriorDeltaExperience.getPrevious()")
            current = page.evaluate("() => window.__bayesPosteriorDeltaExperience.getCurrent()")
            checks.append(("public Bayesian exact before/after layer is active", previous is not None and current["post"]["B"] > previous["post"]["B"] and page.locator(".bayes-eq-prev-marker").count() == len(current["vars"]), {"priorB": previous["post"]["B"] if previous else None, "currentB": current["post"]["B"], "markers": page.locator(".bayes-eq-prev-marker").count()}))
            context.close()

            # Narrow viewport spot check for all four altered applets in the composed artifact.
            for slug, ready in (
                ("transformer-language-model", "Lab13EngagementExperience"),
                ("agent-tool-context", "Lab14EngagementExperience"),
                ("cnf-sat", "__cnfDpllTreeExperience"),
                ("bayes-network", "__bayesPosteriorDeltaExperience"),
            ):
                context = browser.new_context(viewport={"width": 390, "height": 844})
                page = context.new_page()
                page.on("pageerror", lambda exc, slug=slug: page_errors.append(f"{slug}-mobile: {exc}"))
                page.on("console", lambda msg, slug=slug: console_errors.append(f"{slug}-mobile: {msg.text}") if msg.type == "error" else None)
                page.goto((SITE / "playgrounds" / slug / "index.html").resolve().as_uri(), wait_until="load", timeout=10_000)
                page.wait_for_function(f"() => !!window.{ready}")
                overflow = page.evaluate("() => document.documentElement.scrollWidth-window.innerWidth")
                checks.append((f"public {slug} fits 390px", overflow <= 1, {"overflow": overflow}))
                context.close()
        finally:
            browser.close()

    failures = [{"name": name, "detail": detail} for name, ok, detail in checks if not ok]
    payload = {
        "harness": "tools/test_v1_5_public_integration.py",
        "checks": len(checks),
        "passed": len(checks)-len(failures),
        "failed": len(failures),
        "page_errors": page_errors,
        "console_errors": console_errors,
        "pass": not failures and not page_errors and not console_errors,
        "failures": failures,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
