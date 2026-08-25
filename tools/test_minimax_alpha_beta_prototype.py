#!/usr/bin/env python3
"""Browser QA for the Lab 15 English minimax/alpha-beta R3 prototype."""

from __future__ import annotations

import json
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROTOTYPE = ROOT / "tools" / "minimax_alpha_beta_prototype.html"


def launch(playwright):
    args = ["--no-sandbox", "--disable-dev-shm-usage"]
    managed = pathlib.Path(playwright.chromium.executable_path)
    if managed.exists():
        return playwright.chromium.launch(headless=True, args=args)
    for name in ("chromium", "chromium-browser", "google-chrome", "chrome"):
        candidate = shutil.which(name)
        if candidate:
            return playwright.chromium.launch(
                headless=True, executable_path=candidate, args=args
            )
    return playwright.chromium.launch(headless=True, args=args)


def main() -> int:
    source = PROTOTYPE.read_text(encoding="utf-8")
    checks: list[tuple[str, bool, object]] = []
    checks.append(
        (
            "prototype consumes independent core instead of defining a second solver",
            'src="minimax_alpha_beta_core.js"' in source
            and "function minimax(" not in source
            and "function alphaBeta(" not in source,
            {},
        )
    )
    checks.append(
        (
            "prototype exposes five prediction-before-reveal challenges",
            source.count('<option value="root">') == 1
            and source.count('<option value="min">') == 1
            and source.count('<option value="prune">') == 1
            and source.count('<option value="order">') == 1
            and source.count('<option value="greedy">') == 1,
            {},
        )
    )
    checks.append(
        (
            "misconception boundaries are explicit in learner-facing source",
            "skipped nodes are not evaluated" in source
            and "cannot change the exact minimax value" in source
            and "not claimed from pruned trace" in source,
            {},
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
            context = browser.new_context(viewport={"width": 1280, "height": 1000})
            page = context.new_page()
            page.on("pageerror", lambda exc: page_errors.append(str(exc)))
            page.on(
                "console",
                lambda msg: console_errors.append(msg.text)
                if msg.type == "error"
                else None,
            )
            page.goto(PROTOTYPE.resolve().as_uri(), wait_until="load", timeout=10_000)
            page.wait_for_function("() => !!window.Lab15Prototype")

            initial = page.evaluate("() => window.Lab15Prototype.getResult()")
            checks.append(
                (
                    "canonical simple backup is exact but concealed before playback",
                    initial["root_value"] == 4
                    and initial["selected_child"] == "B"
                    and page.locator("#rootValue").inner_text() == "hidden"
                    and page.locator("#selectedMove").inner_text() == "hidden",
                    {
                        "root": initial["root_value"],
                        "move": initial["selected_child"],
                        "visibleRoot": page.locator("#rootValue").inner_text(),
                    },
                )
            )
            checks.append(
                (
                    "tree renders every canonical node without starting search",
                    page.locator("#tree .node").count() == 7
                    and page.evaluate(
                        "() => window.Lab15Prototype.getTraceIndex()"
                    )
                    == -1,
                    {
                        "nodes": page.locator("#tree .node").count(),
                        "traceIndex": page.evaluate(
                            "() => window.Lab15Prototype.getTraceIndex()"
                        ),
                    },
                )
            )

            page.click("#stepTrace")
            first_visible = page.evaluate(
                "() => window.Lab15Prototype.getVisibleState()"
            )
            checks.append(
                (
                    "one playback step reveals exactly the first trace transition",
                    page.evaluate("() => window.Lab15Prototype.getTraceIndex()") == 0
                    and first_visible["visited"] == ["R"]
                    and first_visible["pruned"] == [],
                    first_visible,
                )
            )

            page.click("#endTrace")
            checks.append(
                (
                    "complete minimax trace reveals root result and full exact optimum",
                    page.locator("#rootValue").inner_text() == "4"
                    and page.locator("#selectedMove").inner_text() == "B"
                    and page.locator("#optimalSet").inner_text() == "B"
                    and page.locator("#leafCount").inner_text() == "4",
                    {
                        "root": page.locator("#rootValue").inner_text(),
                        "move": page.locator("#selectedMove").inner_text(),
                        "optimal": page.locator("#optimalSet").inner_text(),
                        "leaves": page.locator("#leafCount").inner_text(),
                    },
                )
            )

            page.select_option("#algorithm", "alpha_beta")
            page.click("#endTrace")
            ab_simple = page.evaluate("() => window.Lab15Prototype.getResult()")
            checks.append(
                (
                    "algorithm switch preserves exact root decision without overclaiming tie set",
                    ab_simple["root_value"] == 4
                    and ab_simple["selected_child"] == "B"
                    and ab_simple["optimal_children"] is None
                    and "not claimed" in page.locator("#optimalSet").inner_text(),
                    {
                        "root": ab_simple["root_value"],
                        "move": ab_simple["selected_child"],
                        "optimal": ab_simple["optimal_children"],
                    },
                )
            )

            page.select_option("#scenario", "first_prune")
            page.select_option("#algorithm", "alpha_beta")
            page.click("#endTrace")
            prune_state = page.evaluate(
                "() => window.Lab15Prototype.getVisibleState()"
            )
            prune_result = page.evaluate("() => window.Lab15Prototype.getResult()")
            checks.append(
                (
                    "first-prune scenario visibly distinguishes skipped from evaluated nodes",
                    prune_state["pruned"] == ["B2"]
                    and "B2" not in prune_result["visited_nodes"]
                    and page.locator("#tree .node.pruned").count() == 1
                    and page.locator("#prunedCount").inner_text() == "1",
                    {
                        "pruned": prune_state["pruned"],
                        "visited": prune_result["visited_nodes"],
                        "prunedDom": page.locator("#tree .node.pruned").count(),
                    },
                )
            )

            page.select_option("#scenario", "good_ordering")
            page.select_option("#algorithm", "alpha_beta")
            page.click("#endTrace")
            good_result = page.evaluate("() => window.Lab15Prototype.getResult()")
            good_leaves = int(page.locator("#leafCount").inner_text())
            page.click("#saveBaseline")
            page.select_option("#order", "reverse")
            page.click("#endTrace")
            reverse_result = page.evaluate("() => window.Lab15Prototype.getResult()")
            reverse_leaves = int(page.locator("#leafCount").inner_text())
            checks.append(
                (
                    "move ordering changes work but not the exact game result",
                    good_result["root_value"] == reverse_result["root_value"] == 8
                    and good_leaves == 4
                    and reverse_leaves == 6,
                    {
                        "goodLeaves": good_leaves,
                        "reverseLeaves": reverse_leaves,
                        "goodRoot": good_result["root_value"],
                        "reverseRoot": reverse_result["root_value"],
                    },
                )
            )
            checks.append(
                (
                    "saved comparison makes the work difference explicit",
                    "Saved:" in page.locator("#baseline").inner_text()
                    and "4 leaves" in page.locator("#baseline").inner_text()
                    and "6 leaves" in page.locator("#baseline").inner_text(),
                    {"text": page.locator("#baseline").inner_text()},
                )
            )

            page.select_option("#scenario", "simple_backup")
            page.select_option("#algorithm", "minimax")
            utility = page.locator('[data-node="B1"]')
            utility.fill("1")
            utility.press("Tab")
            page.click("#endTrace")
            edited = page.evaluate("() => window.Lab15Prototype.getResult()")
            checks.append(
                (
                    "bounded terminal-utility edit recomputes the same core deterministically",
                    edited["root_value"] == 3
                    and edited["selected_child"] == "A"
                    and page.locator("#rootValue").inner_text() == "3",
                    edited,
                )
            )

            page.select_option("#scenario", "tied_optimum")
            page.select_option("#algorithm", "minimax")
            page.click("#endTrace")
            checks.append(
                (
                    "tie scenario separates exact optimal set from deterministic selected child",
                    page.locator("#selectedMove").inner_text() == "A"
                    and page.locator("#optimalSet").inner_text() == "A, B",
                    {
                        "selected": page.locator("#selectedMove").inner_text(),
                        "optimal": page.locator("#optimalSet").inner_text(),
                    },
                )
            )

            page.select_option("#scenario", "no_prune")
            page.select_option("#algorithm", "alpha_beta")
            page.click("#endTrace")
            checks.append(
                (
                    "no-prune scenario blocks the claim that alpha-beta always prunes",
                    page.locator("#leafCount").inner_text() == "4"
                    and page.locator("#prunedCount").inner_text() == "0",
                    {
                        "leaves": page.locator("#leafCount").inner_text(),
                        "pruned": page.locator("#prunedCount").inner_text(),
                    },
                )
            )

            page.select_option("#challengeSelect", "root")
            page.click("#challengeBegin")
            checks.append(
                (
                    "guided reveal is disabled before a complete locked prediction",
                    page.evaluate(
                        "() => window.Lab15Prototype.getChallengeState().state"
                    )
                    == "awaiting"
                    and page.locator("#challengeReveal").is_disabled()
                    and page.locator("#challengeLock").is_disabled(),
                    {},
                )
            )
            page.select_option('[data-challenge-field="move"]', "B")
            page.fill('[data-challenge-field="value"]', "4")
            checks.append(
                (
                    "complete prediction enables lock but not reveal",
                    not page.locator("#challengeLock").is_disabled()
                    and page.locator("#challengeReveal").is_disabled(),
                    {},
                )
            )
            page.click("#challengeLock")
            checks.append(
                (
                    "locked prediction is immutable and enables reveal",
                    page.evaluate(
                        "() => window.Lab15Prototype.getChallengeState().state"
                    )
                    == "locked"
                    and page.locator(
                        '[data-challenge-field="move"]'
                    ).is_disabled()
                    and page.locator(
                        '[data-challenge-field="value"]'
                    ).is_disabled()
                    and not page.locator("#challengeReveal").is_disabled(),
                    {},
                )
            )
            page.click("#challengeReveal")
            checks.append(
                (
                    "root challenge reveals mechanism-specific comparison",
                    page.evaluate(
                        "() => window.Lab15Prototype.getChallengeState().state"
                    )
                    == "revealed"
                    and "Prediction matched" in page.locator(
                        "#challengeActual"
                    ).inner_text()
                    and "MIN returns 3 from A and 4 from B"
                    in page.locator("#challengeActual").inner_text(),
                    {"actual": page.locator("#challengeActual").inner_text()},
                )
            )

            page.select_option("#challengeSelect", "prune")
            page.click("#challengeBegin")
            page.select_option('[data-challenge-field="prune"]', "yes")
            page.click("#challengeLock")
            page.click("#challengeReveal")
            challenge_prune_state = page.evaluate(
                "() => window.Lab15Prototype.getVisibleState()"
            )
            checks.append(
                (
                    "pruning challenge freezes at the actual cutoff rather than a fabricated explanation",
                    challenge_prune_state["event"]["event"] == "prune"
                    and "B2" in challenge_prune_state["pruned"]
                    and "not evaluated" in page.locator(
                        "#challengeActual"
                    ).inner_text(),
                    {
                        "event": challenge_prune_state["event"],
                        "actual": page.locator("#challengeActual").inner_text(),
                    },
                )
            )

            text_state = page.locator("#textState").inner_text()
            checks.append(
                (
                    "text equivalent carries the current search and prune state",
                    "algorithm=alpha_beta" in text_state
                    and "pruned_not_evaluated=B2" in text_state
                    and "alpha=" in text_state
                    and "beta=" in text_state,
                    {"text": text_state},
                )
            )
            context.close()

            reduced = browser.new_context(
                viewport={"width": 900, "height": 900}, reduced_motion="reduce"
            )
            rpage = reduced.new_page()
            rpage.on("pageerror", lambda exc: page_errors.append(str(exc)))
            rpage.on(
                "console",
                lambda msg: console_errors.append(msg.text)
                if msg.type == "error"
                else None,
            )
            rpage.goto(PROTOTYPE.resolve().as_uri(), wait_until="load", timeout=10_000)
            rpage.wait_for_function("() => !!window.Lab15Prototype")
            checks.append(
                (
                    "reduced-motion path retains complete SVG and text mechanisms",
                    rpage.locator("#tree").is_visible()
                    and rpage.locator("#textState").is_visible()
                    and rpage.locator("#stepTrace").is_visible(),
                    {},
                )
            )
            reduced.close()

            mobile = browser.new_context(viewport={"width": 390, "height": 844})
            mpage = mobile.new_page()
            mpage.on("pageerror", lambda exc: page_errors.append(str(exc)))
            mpage.on(
                "console",
                lambda msg: console_errors.append(msg.text)
                if msg.type == "error"
                else None,
            )
            mpage.goto(PROTOTYPE.resolve().as_uri(), wait_until="load", timeout=10_000)
            mpage.wait_for_function("() => !!window.Lab15Prototype")
            overflow = mpage.evaluate(
                "() => document.documentElement.scrollWidth - window.innerWidth"
            )
            checks.append(
                (
                    "390px viewport contains the page while tree scrolls inside its own region",
                    overflow <= 1
                    and mpage.locator(".tree-wrap").is_visible()
                    and mpage.locator("#tree").is_visible(),
                    {"overflow": overflow},
                )
            )
            mobile.close()
        finally:
            browser.close()

    failures = [
        {"name": name, "detail": detail}
        for name, ok, detail in checks
        if not ok
    ]
    payload = {
        "harness": "tools/test_minimax_alpha_beta_prototype.py",
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
