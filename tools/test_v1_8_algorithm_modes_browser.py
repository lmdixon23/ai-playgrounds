#!/usr/bin/env python3
from __future__ import annotations

import http.server
import json
import pathlib
import shutil
import socketserver
import subprocess
import sys
import threading
from contextlib import contextmanager

ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
EVIDENCE = ROOT / "release-evidence" / "v1.8.0-algorithm-modes-browser.json"
SLUGS = ("cnf-sat", "knn-classifier", "hill-climbing")


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


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, _format: str, *args) -> None:
        return


class ReusableServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


@contextmanager
def local_site_server():
    handler = lambda *args, **kwargs: QuietHandler(*args, directory=str(SITE), **kwargs)
    with ReusableServer(("127.0.0.1", 0), handler) as server:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            yield f"http://127.0.0.1:{server.server_address[1]}"
        finally:
            server.shutdown()
            thread.join(timeout=2)


def ensure_site() -> int:
    home = SITE / "index.html"
    if home.is_file() and '<span class="site-version">v1.8.0</span>' in home.read_text(encoding="utf-8"):
        return 0
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "build_site_v1_8.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=150,
    )
    if result.returncode:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
    return result.returncode


def write_evidence(payload: dict) -> None:
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def navigate_ready(page, url: str, feature: str):
    response = page.goto(url, wait_until="domcontentloaded", timeout=20_000)
    page.wait_for_function("() => !!window.__r4Localization && window.__r4Localization.ready()", timeout=12_000)
    page.wait_for_function(f"() => typeof window.{feature} === 'function'", timeout=12_000)
    page.wait_for_selector("details[data-quick-assign-id]", state="attached", timeout=12_000)
    # The shared guided-challenge bundle is deferred and owns some native
    # controls (notably KNN) after initialization. Do not mutate applet state
    # until that final composition layer has completed its synchronous setup.
    page.wait_for_function("() => !!window.__suiteGuidedChallenge", timeout=12_000)
    page.wait_for_timeout(100)
    return response


def set_value(page, selector: str, value: str) -> None:
    page.locator(selector).evaluate(
        "(el,value)=>{el.value=String(value);el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}))}",
        value,
    )


def set_locale(page, locale: str) -> None:
    page.locator(".r4-language-select").select_option(locale)
    page.wait_for_function(
        "locale => window.__r4Localization.locale() === locale && document.documentElement.lang.toLowerCase().startsWith(locale)",
        arg=locale,
        timeout=10_000,
    )
    page.wait_for_timeout(120)


def seed_responses(page, slug: str) -> list[str]:
    fields = page.locator("[data-lab-answer]")
    values = []
    for index in range(fields.count()):
        value = f"v180-{slug}-{index}"
        # Quick Assign answer fields live inside a collapsed disclosure by
        # default. Seed them through the same input/change contract so this
        # state-preservation test does not depend on disclosure visibility.
        fields.nth(index).evaluate(
            "(el,value)=>{el.value=value;el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}))}",
            value,
        )
        values.append(value)
    return values


def response_values(page) -> list[str]:
    return page.locator("[data-lab-answer]").evaluate_all("els=>els.map(el=>el.value)")


def main() -> int:
    if ensure_site():
        return 1

    from playwright.sync_api import sync_playwright

    checks: list[tuple[str, bool, object]] = []

    def check(name: str, ok: bool, detail: object = None) -> None:
        checks.append((name, bool(ok), {} if detail is None else detail))

    page_errors: list[str] = []
    console_errors: list[str] = []
    diagnostics: list[dict] = []
    instrumentation = """
Object.defineProperty(navigator,'clipboard',{configurable:true,value:{
  writeText:async text=>{window.__v180Clipboard=String(text)},
  readText:async()=>window.__v180Clipboard||''
}});
"""

    with local_site_server() as origin, sync_playwright() as playwright:
        browser = launch(playwright)
        try:
            # CNF/SAT: actual CDCL trace, learned-clause rendering, state, share, reset.
            context = browser.new_context(viewport={"width": 1180, "height": 900}, reduced_motion="reduce")
            context.set_default_timeout(10_000)
            context.add_init_script(instrumentation)
            page = context.new_page()
            local_page_errors: list[str] = []
            local_console_errors: list[str] = []
            page.on("pageerror", lambda exc: local_page_errors.append(str(exc)))
            page.on("console", lambda msg: local_console_errors.append(msg.text) if msg.type == "error" else None)
            stage = "cnf navigate"
            try:
                response = navigate_ready(page, f"{origin}/playgrounds/cnf-sat/index.html?lang=en", "__cdclModeTest")
                check("cnf-sat: final artifact HTTP 200", response is not None and response.status == 200)
                responses = seed_responses(page, "cnf")
                stage = "cnf CDCL"
                page.locator("#exCdcl").click()
                page.wait_for_function("() => window.__cnfDpllPresentationState.getTrace().some(row=>row.action==='learn')")
                acceptance = page.evaluate("() => window.__cdclModeTest()")
                check("cnf-sat: deterministic CDCL acceptance contract", acceptance.get("pass") is True, acceptance)
                trace = page.evaluate("() => window.__cnfDpllPresentationState.getTrace()")
                actions = [row["action"] for row in trace]
                check("cnf-sat: trace distinguishes all CDCL actions", all(action in actions for action in ("decision", "propagation", "conflict", "learn", "backjump", "sat")), actions)
                page.evaluate("() => window.__cnfDpllTreeExperience.render()")
                check("cnf-sat: inherited trace visualization accepts the CDCL schema", page.evaluate("() => window.__cnfDpllTreeExperience.getVisibleNodeCount()") >= 1)
                check("cnf-sat: auxiliary trace presentation identifies CDCL mode", "CDCL" in page.locator("#cnf-eq-title").inner_text())
                learn_index = actions.index("learn")
                page.locator("#dpllReset").evaluate("el=>{el.disabled=false;el.click()}")
                page.wait_for_function("() => window.__cnfDpllPresentationState.getIndex()===0")
                for _ in range(learn_index):
                    page.locator("#dpllStep").evaluate("el=>{el.disabled=false;el.click()}")
                page.wait_for_function(
                    "target => window.__cnfDpllPresentationState.getIndex()===target",
                    arg=learn_index,
                )
                learned_chips = page.locator("#dpllClauses .clause-chip.learned")
                learned_detail = {
                    "index": page.evaluate("() => window.__cnfDpllPresentationState.getIndex()"),
                    "action": page.locator("#dpllAction").inner_text(),
                    "chips": learned_chips.all_inner_texts(),
                }
                check("cnf-sat: learned clause is visually identified", learned_chips.count() >= 1 and any("L1" in item for item in learned_detail["chips"]), learned_detail)
                formula = page.locator("#input").input_value()
                trace_before = page.evaluate("() => window.__cnfDpllPresentationState.getTrace()")
                index_before = page.evaluate("() => window.__cnfDpllPresentationState.getIndex()")
                english_action = page.locator("#dpllAction").inner_text()
                for locale in ("zh", "vi", "es"):
                    set_locale(page, locale)
                    state = {
                        "formula": page.locator("#input").input_value(),
                        "mode": page.locator("#solverMode").input_value(),
                        "index": page.evaluate("() => window.__cnfDpllPresentationState.getIndex()"),
                        "trace": page.evaluate("() => window.__cnfDpllPresentationState.getTrace()"),
                        "responses": response_values(page),
                        "action": page.locator("#dpllAction").inner_text(),
                    }
                    check(f"cnf-sat: EN->{locale} preserves formula/mode/trace/responses", state["formula"] == formula and state["mode"] == "cdcl" and state["index"] == index_before and state["trace"] == trace_before and state["responses"] == responses, state)
                    check(f"cnf-sat: CDCL action localizes in {locale}", state["action"] != english_action, state["action"])
                    set_locale(page, "en")
                    check(f"cnf-sat: {locale}->EN restores English without state loss", page.locator("#input").input_value() == formula and page.locator("#solverMode").input_value() == "cdcl" and response_values(page) == responses and page.evaluate("() => window.__cnfDpllPresentationState.getIndex()") == index_before)
                stage = "cnf share/reset"
                page.locator("#shareLink").click()
                page.wait_for_function("() => String(window.__v180Clipboard||'').includes('solver=cdcl')")
                shared = page.evaluate("() => window.__v180Clipboard")
                check("cnf-sat: share preserves CDCL mode and formula but excludes responses", "solver=cdcl" in shared and "f=" in shared and all(value not in shared for value in responses), shared)
                page.locator("#hardReset").click()
                page.wait_for_function("() => document.getElementById('solverMode').value==='dpll'")
                dpll = page.evaluate("() => window.__cnfAcceptanceTest()")
                check("cnf-sat: hard reset restores the original DPLL path", dpll.get("pass") is True and page.locator("#solverMode").input_value() == "dpll", dpll)
            except Exception as exc:
                diagnostics.append({"slug": "cnf-sat", "stage": stage, "error": str(exc)})
                check(f"cnf-sat: exception at {stage}", False, str(exc))
            page_errors.extend(f"cnf-sat: {item}" for item in local_page_errors)
            console_errors.extend(f"cnf-sat: {item}" for item in local_console_errors)
            context.close()

            # KNN: real neighbor inspection, four-locale state restoration, share/reset.
            context = browser.new_context(viewport={"width": 1180, "height": 900}, reduced_motion="reduce", has_touch=True)
            context.set_default_timeout(10_000)
            context.add_init_script(instrumentation)
            page = context.new_page()
            local_page_errors = []
            local_console_errors = []
            page.on("pageerror", lambda exc: local_page_errors.append(str(exc)))
            page.on("console", lambda msg: local_console_errors.append(msg.text) if msg.type == "error" else None)
            stage = "knn navigate"
            try:
                response = navigate_ready(page, f"{origin}/playgrounds/knn-classifier/index.html?lang=en", "__knnModeTest")
                check("knn-classifier: final artifact HTTP 200", response is not None and response.status == 200)
                acceptance = page.evaluate("() => window.__knnModeTest()")
                check("knn-classifier: deterministic classification/regression contract", acceptance.get("pass") is True, acceptance)
                responses = seed_responses(page, "knn")
                page.locator('[data-suite-mode="guided"]').click()
                page.wait_for_selector("#guidedStart", state="visible")
                page.locator("#guidedStart").click()
                page.locator("#cv").click(position={"x": 320, "y": 240})
                set_locale(page, "zh")
                set_locale(page, "en")
                check("knn-classifier: classification guided query survives a locale round trip", "Step 2" in page.locator("#guidedStatus").inner_text())
                page.locator("#guidedReset").click()
                stage = "knn regression mode"
                page.locator("#taskMode").select_option("regression")
                page.locator("#metricSel").select_option("manhattan")
                page.locator("#weightSel").select_option("distance")
                set_value(page, "#k", "7")
                set_value(page, "#xScale", "2")
                set_value(page, "#targetValue", "73")
                mode_state = page.evaluate(
                    "() => ({task:document.getElementById('taskMode').value,inspectorHidden:document.getElementById('regressionInspector').hidden,guidedHidden:document.getElementById('knnGuided').hidden})"
                )
                check(
                    "knn-classifier: regression mode exposes its inspector and hides the classification challenge",
                    mode_state["task"] == "regression" and mode_state["inspectorHidden"] is False and mode_state["guidedHidden"] is True,
                    mode_state,
                )
                stage = "knn regression hover"
                box = page.locator("#cv").bounding_box()
                if box is None:
                    raise RuntimeError("KNN canvas has no bounding box")
                # Dispatch the canvas's real mousemove contract directly. A
                # physical page.mouse move is nondeterministic in a touch-enabled
                # Chromium context and occasionally fails to emit hover state.
                page.locator("#cv").evaluate(
                    "(el,point)=>{const r=el.getBoundingClientRect();el.dispatchEvent(new MouseEvent('mousemove',{bubbles:true,clientX:r.left+r.width*point.x,clientY:r.top+r.height*point.y}))}",
                    {"x": 0.52, "y": 0.47},
                )
                page.wait_for_function("() => document.querySelectorAll('#regressionNeighborTable tbody tr').length===7")
                equation = page.locator("#regressionEquation").inner_text()
                check("knn-classifier: selected neighbors and weighted mean are inspectable", "Σ(wᵢyᵢ)" in equation and page.locator("#regressionNeighborTable tbody tr").count() == 7, equation)
                numeric_rows = page.locator("#regressionNeighborTable tbody tr").evaluate_all("rows=>rows.map(row=>[...row.cells].map(cell=>cell.textContent.trim()))")
                for locale in ("zh", "vi", "es"):
                    set_locale(page, locale)
                    state = {
                        "task": page.locator("#taskMode").input_value(),
                        "k": page.locator("#k").input_value(),
                        "metric": page.locator("#metricSel").input_value(),
                        "weight": page.locator("#weightSel").input_value(),
                        "scale": page.locator("#xScale").input_value(),
                        "target": page.locator("#targetValue").input_value(),
                        "rows": page.locator("#regressionNeighborTable tbody tr").evaluate_all("rows=>rows.map(row=>[...row.cells].map(cell=>cell.textContent.trim()))"),
                        "responses": response_values(page),
                        "targetAria": page.locator("#targetValue").get_attribute("aria-label"),
                    }
                    check(f"knn-classifier: EN->{locale} preserves mode/query-neighbors/k/state/responses", state["task"] == "regression" and state["k"] == "7" and state["metric"] == "manhattan" and state["weight"] == "distance" and state["scale"] == "2" and state["target"] == "73" and state["rows"] == numeric_rows and state["responses"] == responses, state)
                    check(f"knn-classifier: new accessible control localizes in {locale}", state["targetAria"] != "Continuous target for a newly added point", state["targetAria"])
                    set_locale(page, "en")
                    check(f"knn-classifier: {locale}->EN restores regression state", page.locator("#taskMode").input_value() == "regression" and page.locator("#k").input_value() == "7" and response_values(page) == responses)
                stage = "knn share/reset"
                page.locator("#shareLink").click()
                page.wait_for_function("() => String(window.__v180Clipboard||'').includes('task=regression')")
                shared = page.evaluate("() => window.__v180Clipboard")
                check("knn-classifier: share preserves regression controls and excludes responses", all(token in shared for token in ("task=regression", "k=7", "metric=manhattan", "weight=distance", "scale=2", "target=73")) and all(value not in shared for value in responses), shared)
                page.locator("#hardReset").click()
                page.wait_for_function("() => document.getElementById('taskMode').value==='classification' && document.getElementById('k').value==='5'")
                reset_acceptance = page.evaluate("() => window.__knnModeTest()")
                check("knn-classifier: hard reset restores classification and its historical behavior", reset_acceptance.get("pass") is True and page.locator("#taskMode").input_value() == "classification", reset_acceptance)
                page.locator("#shareLink").click()
                page.wait_for_function("() => String(window.__v180Clipboard||'').includes('task=classification') && String(window.__v180Clipboard||'').includes('ds=moons')")
                check("knn-classifier: hard reset also restores the shareable default dataset", "ds=moons" in page.evaluate("() => window.__v180Clipboard"))
            except Exception as exc:
                diagnostics.append({"slug": "knn-classifier", "stage": stage, "error": str(exc)})
                check(f"knn-classifier: exception at {stage}", False, str(exc))
            page_errors.extend(f"knn-classifier: {item}" for item in local_page_errors)
            console_errors.extend(f"knn-classifier: {item}" for item in local_console_errors)
            context.close()

            # Hill climbing: responsive seeded runner, aggregates, locale state, share/reset.
            context = browser.new_context(viewport={"width": 1180, "height": 900}, reduced_motion="reduce")
            context.set_default_timeout(12_000)
            context.add_init_script(instrumentation)
            page = context.new_page()
            local_page_errors = []
            local_console_errors = []
            page.on("pageerror", lambda exc: local_page_errors.append(str(exc)))
            page.on("console", lambda msg: local_console_errors.append(msg.text) if msg.type == "error" else None)
            stage = "hill navigate"
            try:
                response = navigate_ready(page, f"{origin}/playgrounds/hill-climbing/index.html?lang=en", "__hillBenchmarkTest")
                check("hill-climbing: final artifact HTTP 200", response is not None and response.status == 200)
                acceptance = page.evaluate("() => window.__hillBenchmarkTest()")
                original = page.evaluate("() => window.__hillAcceptanceTest()")
                check("hill-climbing: deterministic matched-start benchmark contract", acceptance.get("pass") is True, acceptance)
                check("hill-climbing: original single-run control contract remains valid", original.get("pass") is True, original)
                responses = seed_responses(page, "hill")
                stage = "hill benchmark"
                page.locator("#probSel").select_option("queens")
                set_value(page, "#benchmarkRuns", "4")
                set_value(page, "#benchmarkSteps", "40")
                set_value(page, "#benchmarkSeed", "4242")
                page.locator("[data-benchmark-algo]").evaluate_all("els=>els.forEach(el=>{el.checked=['simple','steepest','sa'].includes(el.dataset.benchmarkAlgo)})")
                page.locator("#benchmarkRun").click()
                page.wait_for_function("() => !document.getElementById('benchmarkRun').disabled && document.querySelectorAll('#benchmarkResults tbody tr').length===3", timeout=20_000)
                status = page.locator("#benchmarkStatus").inner_text()
                numeric_rows = page.locator("#benchmarkResults tbody tr").evaluate_all("rows=>rows.map(row=>[...row.cells].slice(1).map(cell=>cell.textContent.trim()))")
                check("hill-climbing: success frequency and cost appear in separate result columns", page.locator("#benchmarkResults thead th").count() == 6 and all(len(row) == 5 for row in numeric_rows), numeric_rows)
                check("hill-climbing: benchmark reports completed runs and reproducibility seed", "4242" in status and all(row[-1] == "4/4" for row in numeric_rows), {"status": status, "rows": numeric_rows})
                for locale in ("zh", "vi", "es"):
                    stage = f"hill locale {locale}"
                    set_locale(page, locale)
                    page.wait_for_function("() => document.querySelectorAll('#benchmarkResults tbody tr').length===3")
                    state = {
                        "runs": page.locator("#benchmarkRuns").input_value(),
                        "steps": page.locator("#benchmarkSteps").input_value(),
                        "seed": page.locator("#benchmarkSeed").input_value(),
                        "rows": page.locator("#benchmarkResults tbody tr").evaluate_all("rows=>rows.map(row=>[...row.cells].slice(1).map(cell=>cell.textContent.trim()))"),
                        "responses": response_values(page),
                        "firstHeading": page.locator("#benchmarkResults thead th").first.inner_text(),
                    }
                    check(f"hill-climbing: EN->{locale} preserves benchmark/results/responses", state["runs"] == "4" and state["steps"] == "40" and state["seed"] == "4242" and state["rows"] == numeric_rows and state["responses"] == responses, state)
                    check(f"hill-climbing: benchmark headings localize in {locale}", state["firstHeading"] != "Algorithm", state["firstHeading"])
                    set_locale(page, "en")
                    page.wait_for_function("() => document.querySelectorAll('#benchmarkResults tbody tr').length===3")
                    check(f"hill-climbing: {locale}->EN restores benchmark state", page.locator("#benchmarkRuns").input_value() == "4" and page.locator("#benchmarkResults tbody tr").count() == 3 and response_values(page) == responses)
                stage = "hill share/reset"
                page.locator("#shareLink").click()
                page.wait_for_function("() => String(window.__v180Clipboard||'').includes('benchSeed=4242')")
                shared = page.evaluate("() => window.__v180Clipboard")
                check("hill-climbing: share preserves benchmark controls and excludes responses", all(token in shared for token in ("benchRuns=4", "benchSteps=40", "benchSeed=4242", "benchAlgos=simple%2Csteepest%2Csa")) and all(value not in shared for value in responses), shared)
                page.locator("#hardReset").click()
                page.wait_for_function("() => document.getElementById('benchmarkRuns').value==='20' && !document.querySelector('#benchmarkResults tbody tr')")
                check("hill-climbing: hard reset restores benchmark defaults without removing single-run mode", page.locator("#benchmarkSeed").input_value() == "1729" and page.evaluate("() => window.__hillAcceptanceTest().pass") is True)
            except Exception as exc:
                diagnostics.append({"slug": "hill-climbing", "stage": stage, "error": str(exc)})
                check(f"hill-climbing: exception at {stage}", False, str(exc))
            page_errors.extend(f"hill-climbing: {item}" for item in local_page_errors)
            console_errors.extend(f"hill-climbing: {item}" for item in local_console_errors)
            context.close()

            # Mobile/reduced-motion smoke against the exact final artifact.
            for slug, feature in (("cnf-sat", "__cdclModeTest"), ("knn-classifier", "__knnModeTest"), ("hill-climbing", "__hillBenchmarkTest")):
                context = browser.new_context(viewport={"width": 390, "height": 844}, reduced_motion="reduce", has_touch=True)
                page = context.new_page()
                local_errors: list[str] = []
                page.on("pageerror", lambda exc, target=local_errors: target.append(str(exc)))
                try:
                    navigate_ready(page, f"{origin}/playgrounds/{slug}/index.html?lang=es", feature)
                    overflow = page.evaluate("() => document.documentElement.scrollWidth-window.innerWidth")
                    reduced = page.evaluate("() => matchMedia('(prefers-reduced-motion: reduce)').matches")
                    check(f"{slug}: 390px final page has no horizontal page overflow", overflow <= 1, overflow)
                    check(f"{slug}: reduced-motion preference reaches the final page", reduced)
                except Exception as exc:
                    diagnostics.append({"slug": slug, "stage": "mobile", "error": str(exc)})
                    check(f"{slug}: mobile exception", False, str(exc))
                page_errors.extend(f"{slug} mobile: {item}" for item in local_errors)
                context.close()
        finally:
            browser.close()

    failures = [{"name": name, "detail": detail} for name, ok, detail in checks if not ok]
    payload = {
        "harness": "tools/test_v1_8_algorithm_modes_browser.py",
        "checks": len(checks),
        "passed": len(checks) - len(failures),
        "failed": len(failures),
        "page_errors": page_errors,
        "console_errors": console_errors,
        "diagnostics": diagnostics,
        "pass": not failures and not page_errors and not console_errors,
        "failures": failures,
    }
    write_evidence(payload)
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
