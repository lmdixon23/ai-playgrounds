#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "_site" / "playgrounds" / "cnf-sat" / "index.html"


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
        [sys.executable, str(ROOT / "tools" / "build_cnf_sat_engagement_candidate.py"), "--output", str(OUTPUT)],
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
    checks.append(("candidate exposes existing DPLL trace read-only", "window.__cnfDpllPresentationState" in source and "getTrace" in source and "dpllTrace(deep, vars)" in source, {}))
    checks.append(("candidate adds no second DPLL solver", source.count("function dpllTrace(") == 1, {"dpllTraceDefinitions": source.count("function dpllTrace(")}))
    checks.append(("tree runtime is presentation-only over trace", "__cnfDpllTreeExperience" in source and "data-r4-no-translate" in source, {}))

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
            page.wait_for_function("() => !!window.__cnfDpllPresentationState && !!window.__cnfDpllTreeExperience")

            trace = page.evaluate("() => window.__cnfDpllPresentationState.getTrace()")
            checks.append(("default formula generates a visible tree from actual trace", len(trace) > 0 and page.locator("#cnf-eq-svg .cnf-eq-node").count() == 1, {"traceLength": len(trace), "visibleNodes": page.locator("#cnf-eq-svg .cnf-eq-node").count()}))

            page.click("#dpllStep")
            page.wait_for_timeout(30)
            checks.append(("stepping the existing DPLL player grows the same tree", page.evaluate("() => window.__cnfDpllPresentationState.getIndex()") == 1 and page.locator("#cnf-eq-svg .cnf-eq-node").count() == 2, {"index": page.evaluate("() => window.__cnfDpllPresentationState.getIndex()"), "nodes": page.locator("#cnf-eq-svg .cnf-eq-node").count()}))

            # Parser-valid two-variable UNSAT instance with no initial unit or pure literal.
            # DPLL must make a real branch, hit a contradiction, backtrack to the sibling,
            # and hit the second contradiction. Written using the applet's documented word
            # operators rather than programming-language aliases the parser does not promise.
            formula = "(A or B) and ((not A) or B) and (A or (not B)) and ((not A) or (not B))"
            page.fill("#input", formula)
            page.click("#convertBtn")
            page.wait_for_timeout(40)
            branch_trace = page.evaluate("() => window.__cnfDpllPresentationState.getTrace()")
            actions = [row["action"] for row in branch_trace]
            parse_error = page.locator("#parseOut .error").count()
            required_actions = {"branch+", "branch-", "unsat"}
            has_required_actions = required_actions.issubset(set(actions))
            checks.append(("adversarial UNSAT fixture parses and contains branch conflict and backtrack", parse_error == 0 and has_required_actions, {"formula": formula, "parseErrors": parse_error, "actions": actions, "traceLength": len(branch_trace)}))

            first_unsat = actions.index("unsat") if "unsat" in actions else None
            if first_unsat is not None:
                for _ in range(first_unsat):
                    page.click("#dpllStep")
                page.wait_for_timeout(30)
                conflict_ok = (
                    page.evaluate("() => window.__cnfDpllPresentationState.getIndex()") == first_unsat
                    and page.locator("#cnf-eq-svg .cnf-eq-node.unsat").count() >= 1
                    and page.locator("#cnf-eq-svg .cnf-eq-node").count() == first_unsat + 1
                )
            else:
                conflict_ok = False
            checks.append(("conflict becomes a visible pruned leaf", conflict_ok, {"firstUnsat": first_unsat, "index": page.evaluate("() => window.__cnfDpllPresentationState.getIndex()"), "unsatNodes": page.locator("#cnf-eq-svg .cnf-eq-node.unsat").count(), "actions": actions}))

            backtrack_index = actions.index("branch-") if "branch-" in actions else None
            if backtrack_index is not None:
                page.click("#dpllReset")
                for _ in range(backtrack_index):
                    page.click("#dpllStep")
                page.wait_for_timeout(30)
                path_text = page.locator("#cnf-eq-path").inner_text()
                backtrack_ok = (
                    page.evaluate("() => window.__cnfDpllPresentationState.getIndex()") == backtrack_index
                    and page.locator("#cnf-eq-svg .cnf-eq-node.backtrack").count() >= 1
                    and "backtrack" in path_text.lower()
                )
            else:
                path_text = page.locator("#cnf-eq-path").inner_text()
                backtrack_ok = False
            checks.append(("backtracking opens a sibling branch rather than crossing the conflict", backtrack_ok, {"backtrackIndex": backtrack_index, "path": path_text, "backtrackNodes": page.locator("#cnf-eq-svg .cnf-eq-node.backtrack").count(), "actions": actions}))

            trace_before_locale = page.evaluate("() => window.__cnfDpllPresentationState.getTrace()")
            index_before_locale = page.evaluate("() => window.__cnfDpllPresentationState.getIndex()")
            page.select_option(".r4-language-select", "vi")
            page.wait_for_timeout(100)
            trace_after_locale = page.evaluate("() => window.__cnfDpllPresentationState.getTrace()")
            index_after_locale = page.evaluate("() => window.__cnfDpllPresentationState.getIndex()")
            checks.append(("four-locale overlay preserves DPLL state and localizes tree", trace_before_locale == trace_after_locale and index_before_locale == index_after_locale and "Xem DPLL" in page.locator("#cnf-eq-title").inner_text(), {"lang": page.locator("html").get_attribute("lang"), "index": index_after_locale}))
            context.close()

            reduced = browser.new_context(viewport={"width": 900, "height": 900}, reduced_motion="reduce")
            rpage = reduced.new_page()
            rpage.on("pageerror", lambda exc: page_errors.append(str(exc)))
            rpage.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            rpage.goto(OUTPUT.resolve().as_uri(), wait_until="load", timeout=10_000)
            rpage.wait_for_function("() => !!window.__cnfDpllTreeExperience")
            checks.append(("reduced-motion path retains complete text and SVG state", rpage.locator("#cnf-eq-step").is_visible() and rpage.locator("#cnf-eq-path").is_visible() and rpage.locator("#cnf-eq-svg").is_visible(), {}))
            reduced.close()

            mobile = browser.new_context(viewport={"width": 390, "height": 844})
            mpage = mobile.new_page()
            mpage.on("pageerror", lambda exc: page_errors.append(str(exc)))
            mpage.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            mpage.goto(OUTPUT.resolve().as_uri() + "?lang=es", wait_until="load", timeout=10_000)
            mpage.wait_for_function("() => !!window.__cnfDpllTreeExperience")
            overflow = mpage.evaluate("() => document.documentElement.scrollWidth-window.innerWidth")
            checks.append(("DPLL tree panel fits the 390px page boundary", overflow <= 1 and mpage.locator("#cnf-eq-tree").is_visible(), {"overflow": overflow}))
            mobile.close()
        finally:
            browser.close()

    failures = [{"name": name, "detail": detail} for name, ok, detail in checks if not ok]
    payload = {
        "harness": "tools/test_cnf_sat_engagement_candidate.py",
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
