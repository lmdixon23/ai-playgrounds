#!/usr/bin/env python3
"""English single-file and browser QA for Lab 15 R4."""

from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "release-evidence" / "lab15-minimax-alpha-beta-english-candidate.html"

EXPECTED_SCENARIOS = [
    "simple_backup",
    "greedy_trap",
    "first_prune",
    "good_ordering",
    "poor_ordering",
    "no_prune",
    "tied_optimum",
    "deep_cutoff",
    "boundary_terminal",
    "boundary_chain",
    "boundary_unbalanced",
]


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
    build = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools" / "build_minimax_alpha_beta_english_candidate.py"),
            "--output",
            str(OUTPUT),
        ],
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
    checks.append(
        (
            "candidate is one self-contained HTML file",
            OUTPUT.is_file()
            and 'id="lab15-minimax-alpha-beta-core"' in source
            and 'src="minimax_alpha_beta_core.js"' not in source,
            {"bytes": OUTPUT.stat().st_size},
        )
    )
    checks.append(
        (
            "candidate contains exactly one search implementation per algorithm",
            source.count("function minimax(") == 1
            and source.count("function alphaBeta(") == 1,
            {
                "minimaxDefinitions": source.count("function minimax("),
                "alphaBetaDefinitions": source.count("function alphaBeta("),
            },
        )
    )
    checks.append(
        (
            "candidate has no runtime network transport dependency",
            all(
                token not in source
                for token in ("fetch(", "XMLHttpRequest", "WebSocket", "EventSource")
            ),
            {},
        )
    )
    checks.append(
        (
            "R4 stage and predict-lock-reveal workflow are explicit",
            'name="lab15-candidate-stage" content="R4-English"' in source
            and "Predict first, lock the prediction" in source
            and "challengeLock" in source
            and "challengeReveal" in source,
            {},
        )
    )
    checks.append(
        (
            "reduced-motion and narrow-width contracts are present",
            "prefers-reduced-motion:reduce" in source
            and "@media(max-width:560px)" in source
            and "overflow:auto" in source,
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
            page.goto(OUTPUT.resolve().as_uri(), wait_until="load", timeout=10_000)
            page.wait_for_function(
                "() => !!window.Lab15GameTreeCore && !!window.Lab15Prototype"
            )

            scenario_names = page.evaluate(
                "() => window.Lab15GameTreeCore.scenarioNames()"
            )
            checks.append(
                (
                    "all frozen R0/R1 scenarios are present in the English candidate",
                    scenario_names == EXPECTED_SCENARIOS,
                    {"scenarios": scenario_names},
                )
            )

            browser_parity = page.evaluate(
                """() => window.Lab15GameTreeCore.scenarioNames().map(name => {
                  const C = window.Lab15GameTreeCore;
                  const tree = C.scenario(name);
                  const mm = C.minimax(tree);
                  const ab = C.alphaBeta(tree);
                  return {
                    name,
                    mmRoot: mm.root_value,
                    abRoot: ab.root_value,
                    mmMove: mm.selected_child,
                    abMove: ab.selected_child,
                    mmLeaves: mm.evaluated_leaves.length,
                    abLeaves: ab.evaluated_leaves.length,
                    overlap: ab.pruned_nodes.filter(id => ab.visited_nodes.includes(id))
                  };
                })"""
            )
            parity_ok = all(
                row["mmRoot"] == row["abRoot"]
                and row["mmMove"] == row["abMove"]
                and row["abLeaves"] <= row["mmLeaves"]
                and not row["overlap"]
                for row in browser_parity
            )
            checks.append(
                (
                    "every browser scenario preserves minimax/alpha-beta value and visit invariants",
                    parity_ok,
                    {"rows": browser_parity},
                )
            )

            initial = page.evaluate("() => window.Lab15Prototype.getResult()")
            checks.append(
                (
                    "canonical result exists but remains concealed before playback",
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

            page.select_option("#scenario", "first_prune")
            page.select_option("#algorithm", "alpha_beta")
            page.click("#endTrace")
            prune_state = page.evaluate(
                "() => window.Lab15Prototype.getVisibleState()"
            )
            prune_result = page.evaluate("() => window.Lab15Prototype.getResult()")
            text_state = page.locator("#textState").inner_text()
            checks.append(
                (
                    "first-prune trace marks B2 skipped rather than evaluated",
                    prune_state["pruned"] == ["B2"]
                    and "B2" not in prune_result["visited_nodes"]
                    and page.locator("#tree .node.pruned").count() == 1
                    and "pruned_not_evaluated=B2" in text_state,
                    {
                        "pruned": prune_state["pruned"],
                        "visited": prune_result["visited_nodes"],
                        "text": text_state,
                    },
                )
            )

            page.select_option("#scenario", "good_ordering")
            page.select_option("#algorithm", "alpha_beta")
            page.select_option("#order", "configured")
            page.click("#endTrace")
            good = page.evaluate("() => window.Lab15Prototype.getResult()")
            page.click("#saveBaseline")
            page.select_option("#order", "reverse")
            page.click("#endTrace")
            reversed_result = page.evaluate("() => window.Lab15Prototype.getResult()")
            comparison = page.locator("#baseline").inner_text()
            checks.append(
                (
                    "move ordering changes work without changing exact root result",
                    good["root_value"] == reversed_result["root_value"] == 8
                    and good["selected_child"] == reversed_result["selected_child"] == "A"
                    and len(good["evaluated_leaves"]) == 4
                    and len(reversed_result["evaluated_leaves"]) == 6,
                    {
                        "good": good,
                        "reversed": reversed_result,
                    },
                )
            )
            checks.append(
                (
                    "saved comparison makes the search-work difference visible",
                    "Saved:" in comparison
                    and "4 leaves" in comparison
                    and "6 leaves" in comparison,
                    {"comparison": comparison},
                )
            )

            page.select_option("#scenario", "tied_optimum")
            page.select_option("#algorithm", "minimax")
            page.select_option("#order", "configured")
            page.click("#endTrace")
            checks.append(
                (
                    "minimax tie view separates exact optimal set from deterministic selection",
                    page.locator("#selectedMove").inner_text() == "A"
                    and page.locator("#optimalSet").inner_text() == "A, B",
                    {
                        "selected": page.locator("#selectedMove").inner_text(),
                        "optimal": page.locator("#optimalSet").inner_text(),
                    },
                )
            )
            page.select_option("#algorithm", "alpha_beta")
            page.click("#endTrace")
            checks.append(
                (
                    "alpha-beta tie view does not overclaim a complete tied optimum set",
                    page.locator("#selectedMove").inner_text() == "A"
                    and "not claimed from pruned trace"
                    in page.locator("#optimalSet").inner_text(),
                    {"optimal": page.locator("#optimalSet").inner_text()},
                )
            )

            page.select_option("#scenario", "no_prune")
            page.select_option("#algorithm", "alpha_beta")
            page.click("#endTrace")
            checks.append(
                (
                    "no-prune fixture visibly demonstrates alpha-beta may evaluate every leaf",
                    page.locator("#leafCount").inner_text() == "4"
                    and page.locator("#prunedCount").inner_text() == "0",
                    {
                        "leaves": page.locator("#leafCount").inner_text(),
                        "pruned": page.locator("#prunedCount").inner_text(),
                    },
                )
            )

            page.select_option("#scenario", "simple_backup")
            page.select_option("#algorithm", "minimax")
            page.select_option("#order", "configured")
            b1 = page.locator('[data-node="B1"]')
            b1.fill("-20")
            b1.press("Tab")
            page.click("#endTrace")
            low = page.evaluate("() => window.Lab15Prototype.getResult()")
            checks.append(
                (
                    "lower-bound utility edit recomputes through the same core",
                    low["root_value"] == 3
                    and low["selected_child"] == "A"
                    and page.locator("#rootValue").inner_text() == "3",
                    low,
                )
            )
            b1 = page.locator('[data-node="B1"]')
            b1.fill("999")
            b1.press("Tab")
            bounded_tree = page.evaluate("() => window.Lab15Prototype.getTree()")
            bounded_b1 = next(
                node for node in bounded_tree["nodes"] if node["id"] == "B1"
            )
            checks.append(
                (
                    "utility editor clamps values to the documented safe range",
                    b1.input_value() == "20" and bounded_b1["utility"] == 20,
                    {
                        "input": b1.input_value(),
                        "utility": bounded_b1["utility"],
                    },
                )
            )

            challenge_cases = [
                ("root", {"move": "B", "value": "4"}),
                ("min", {"value": "3"}),
                ("prune", {"prune": "yes"}),
                ("order", {"order": "good"}),
                ("greedy", {"move": "B"}),
            ]
            challenge_actuals: dict[str, str] = {}
            challenge_ok = True
            for challenge_id, prediction in challenge_cases:
                page.select_option("#challengeSelect", challenge_id)
                page.click("#challengeBegin")
                if not page.locator("#challengeReveal").is_disabled():
                    challenge_ok = False
                if not page.locator("#challengeLock").is_disabled():
                    challenge_ok = False
                for field, value in prediction.items():
                    locator = page.locator(f'[data-challenge-field="{field}"]')
                    if locator.evaluate("el => el.tagName") == "SELECT":
                        locator.select_option(value)
                    else:
                        locator.fill(value)
                if page.locator("#challengeLock").is_disabled():
                    challenge_ok = False
                if not page.locator("#challengeReveal").is_disabled():
                    challenge_ok = False
                page.click("#challengeLock")
                locked_state = page.evaluate(
                    "() => window.Lab15Prototype.getChallengeState().state"
                )
                fields_locked = page.locator("[data-challenge-field]").evaluate_all(
                    "els => els.every(el => el.disabled)"
                )
                if locked_state != "locked" or not fields_locked:
                    challenge_ok = False
                if page.locator("#challengeReveal").is_disabled():
                    challenge_ok = False
                page.click("#challengeReveal")
                revealed_state = page.evaluate(
                    "() => window.Lab15Prototype.getChallengeState().state"
                )
                actual = page.locator("#challengeActual").inner_text()
                challenge_actuals[challenge_id] = actual
                if revealed_state != "revealed" or "Prediction matched" not in actual:
                    challenge_ok = False

            checks.append(
                (
                    "all five Guided Challenges enforce prediction-lock-reveal and accept their frozen correct predictions",
                    challenge_ok,
                    {"actuals": challenge_actuals},
                )
            )
            checks.append(
                (
                    "challenge explanations remain tied to the actual game-tree mechanisms",
                    "MIN returns 3 from A and 4 from B" in challenge_actuals["root"]
                    and "A returns 3" in challenge_actuals["min"]
                    and "alpha=5 and beta=4" in challenge_actuals["prune"]
                    and "evaluates 4 leaves" in challenge_actuals["order"]
                    and "force A down to -4" in challenge_actuals["greedy"],
                    {"actuals": challenge_actuals},
                )
            )

            page.select_option("#challengeSelect", "prune")
            page.click("#challengeBegin")
            page.select_option('[data-challenge-field="prune"]', "yes")
            page.click("#challengeLock")
            page.click("#challengeReveal")
            challenge_prune = page.evaluate(
                "() => window.Lab15Prototype.getVisibleState()"
            )
            checks.append(
                (
                    "prune challenge reveals the actual cutoff event rather than a fabricated animation",
                    challenge_prune["event"]["event"] == "prune"
                    and "B2" in challenge_prune["pruned"],
                    challenge_prune,
                )
            )

            aria = page.locator("#tree").get_attribute("aria-label") or ""
            current_text = page.locator("#textState").inner_text()
            checks.append(
                (
                    "SVG state has a synchronized accessible text equivalent",
                    "Game tree" in aria
                    and "algorithm=alpha_beta" in current_text
                    and "pruned_not_evaluated=B2" in current_text
                    and "alpha=" in current_text
                    and "beta=" in current_text,
                    {"aria": aria, "text": current_text},
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
            rpage.goto(OUTPUT.resolve().as_uri(), wait_until="load", timeout=10_000)
            rpage.wait_for_function("() => !!window.Lab15Prototype")
            rpage.select_option("#scenario", "first_prune")
            rpage.select_option("#algorithm", "alpha_beta")
            rpage.click("#endTrace")
            checks.append(
                (
                    "reduced-motion path retains complete prune and text state",
                    rpage.locator("#tree .node.pruned").count() == 1
                    and "pruned_not_evaluated=B2"
                    in rpage.locator("#textState").inner_text()
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
            mpage.goto(OUTPUT.resolve().as_uri(), wait_until="load", timeout=10_000)
            mpage.wait_for_function("() => !!window.Lab15Prototype")
            page_overflow = mpage.evaluate(
                "() => document.documentElement.scrollWidth - window.innerWidth"
            )
            tree_scroll = mpage.evaluate(
                "() => { const el=document.querySelector('.tree-wrap'); return el.scrollWidth > el.clientWidth; }"
            )
            checks.append(
                (
                    "390px page remains contained while the wide tree scrolls inside its bounded region",
                    page_overflow <= 1
                    and tree_scroll
                    and mpage.locator("#tree").is_visible(),
                    {"pageOverflow": page_overflow, "treeInternalScroll": tree_scroll},
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
        "harness": "tools/test_minimax_alpha_beta_english_applet.py",
        "candidate": str(OUTPUT.relative_to(ROOT)),
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
