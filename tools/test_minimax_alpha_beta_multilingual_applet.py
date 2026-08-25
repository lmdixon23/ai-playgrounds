#!/usr/bin/env python3
"""R6 four-locale browser/state-preservation QA for Lab 15."""

from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "release-evidence" / "lab15-minimax-alpha-beta-multilingual-candidate.html"
R4_SOURCE_FREEZE = "f904e6d68f71602dced73e99d259eee055899bc2"


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


def snapshot(page):
    return page.evaluate(
        """() => ({
          tree: window.Lab15Prototype.getTree(),
          result: window.Lab15Prototype.getResult(),
          traceIndex: window.Lab15Prototype.getTraceIndex(),
          visible: window.Lab15Prototype.getVisibleState(),
          challenge: window.Lab15Prototype.getChallengeState(),
          scenario: document.querySelector('#scenario').value,
          algorithm: document.querySelector('#algorithm').value,
          order: document.querySelector('#order').value,
          utilities: [...document.querySelectorAll('[data-node]')].map(el => [el.dataset.node, el.value]),
          challengeFields: [...document.querySelectorAll('[data-challenge-field]')].map(el => ({name:el.dataset.challengeField,value:el.value,disabled:el.disabled}))
        })"""
    )


def set_locale(page, code: str) -> None:
    page.select_option("#lab15-language-select", code)
    expected = {"en": "en", "zh": "zh-Hans", "vi": "vi", "es": "es"}[code]
    page.wait_for_function(
        "([code,expected]) => window.Lab15Localization && window.Lab15Localization.locale()===code && document.documentElement.lang===expected",
        arg=[code, expected],
    )
    page.wait_for_timeout(80)


def main() -> int:
    build = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools" / "build_minimax_alpha_beta_multilingual_candidate.py"),
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
            "R6 candidate is a self-contained four-locale artifact bound to the frozen R4 source",
            'name="lab15-candidate-stage" content="R6-Multilingual"' in source
            and 'id="lab15-locale-data"' in source
            and 'id="lab15-r6-localization-runtime"' in source
            and R4_SOURCE_FREEZE in source
            and all(token in source for token in ("zh-Hans", "Tiếng Việt", "Español")),
            {"bytes": OUTPUT.stat().st_size},
        )
    )
    checks.append(
        (
            "R6 preserves exactly one minimax and one alpha-beta implementation",
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
            "R6 keeps the candidate offline and transport-free",
            all(
                token not in source
                for token in ("fetch(", "XMLHttpRequest", "WebSocket", "EventSource")
            ),
            {},
        )
    )
    checks.append(
        (
            "developer badge is locale-neutral rather than untranslated English prose",
            "R6 · EN/ZH/VI/ES" in source and "R6 four-locale candidate" not in source,
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
            page.goto(OUTPUT.resolve().as_uri() + "?lang=en", wait_until="domcontentloaded", timeout=30_000)
            page.wait_for_function(
                "() => !!window.Lab15Prototype && !!window.Lab15Localization"
            )

            static_expectations = {
                "en": {
                    "lang": "en",
                    "title": "Game Trees: Minimax and Alpha-Beta Pruning",
                    "scenario": "Scenario",
                    "challenge": "Challenge",
                    "body": ("Model boundary:", "skipped nodes are not evaluated."),
                },
                "zh": {
                    "lang": "zh-Hans",
                    "title": "博弈树：Minimax 与 Alpha-Beta 剪枝",
                    "scenario": "场景",
                    "challenge": "挑战",
                    "body": ("模型边界：", "被跳过的节点不会被算法求值。"),
                },
                "vi": {
                    "lang": "vi",
                    "title": "Cây trò chơi: Minimax và cắt tỉa Alpha-Beta",
                    "scenario": "Kịch bản",
                    "challenge": "Thử thách",
                    "body": ("Giới hạn mô hình:", "các nút bị bỏ qua không được thuật toán đánh giá."),
                },
                "es": {
                    "lang": "es",
                    "title": "Árboles de juego: Minimax y poda Alpha-Beta",
                    "scenario": "Escenario",
                    "challenge": "Desafío",
                    "body": ("Límite del modelo:", "los nodos omitidos no son evaluados por el algoritmo."),
                },
            }

            initial_state = snapshot(page)
            locale_static: dict[str, object] = {}
            for code in ("en", "zh", "vi", "es", "en"):
                set_locale(page, code)
                body = page.locator("body").inner_text()
                exp = static_expectations[code]
                ok = (
                    page.locator("html").get_attribute("lang") == exp["lang"]
                    and page.title() == exp["title"]
                    and page.locator('label[for="scenario"]').inner_text() == exp["scenario"]
                    and page.locator('label[for="challengeSelect"] strong').inner_text() == exp["challenge"]
                    and all(phrase in body for phrase in exp["body"])
                    and page.locator("#lab15-language-select").input_value() == code
                )
                locale_static[code] = {
                    "lang": page.locator("html").get_attribute("lang"),
                    "title": page.title(),
                    "scenario": page.locator('label[for="scenario"]').inner_text(),
                    "challenge": page.locator('label[for="challengeSelect"] strong').inner_text(),
                }
                checks.append((f"{code} localizes the complete static teaching shell", ok, locale_static[code]))
                checks.append(
                    (
                        f"{code} static locale switch preserves exact Lab 15 machine/challenge state",
                        snapshot(page) == initial_state,
                        {"locale": code},
                    )
                )

            page.select_option("#scenario", "first_prune")
            page.select_option("#algorithm", "alpha_beta")
            prune_index = page.evaluate(
                "() => window.Lab15Prototype.getResult().trace.findIndex(e => e.event==='prune')"
            )
            page.evaluate("index => window.Lab15Prototype.setTraceIndex(index)", prune_index)
            page.wait_for_timeout(80)
            prune_machine = snapshot(page)
            dynamic_expectations = {
                "en": ("prune", "will not be evaluated", "PRUNED", "not evaluated after cutoff"),
                "zh": ("剪枝", "不会被算法求值", "已剪枝", "截断后未求值"),
                "vi": ("cắt tỉa", "không được thuật toán đánh giá", "ĐÃ CẮT", "không được đánh giá sau khi cắt"),
                "es": ("podar", "no será evaluado por el algoritmo", "PODADO", "no evaluado después del corte"),
            }
            for code in ("zh", "vi", "es", "en"):
                set_locale(page, code)
                title = page.locator("#traceTitle").inner_text()
                explanation = page.locator("#traceExplanation").inner_text()
                pruned_label = page.locator("#tree .node.pruned .value").inner_text()
                svg_title = page.locator("#tree .node.pruned title").inner_text()
                expected = dynamic_expectations[code]
                checks.append(
                    (
                        f"{code} localizes the actual cutoff event including SVG prune state",
                        expected[0].lower() in title.lower()
                        and expected[1].lower() in explanation.lower()
                        and pruned_label == expected[2]
                        and expected[3].lower() in svg_title.lower()
                        and "B2" in explanation
                        and "alpha" in explanation
                        and "beta" in explanation,
                        {
                            "title": title,
                            "explanation": explanation,
                            "prunedLabel": pruned_label,
                            "svgTitle": svg_title,
                        },
                    )
                )
                checks.append(
                    (
                        f"{code} dynamic locale switch preserves the exact cutoff machine state",
                        snapshot(page) == prune_machine,
                        {"locale": code, "traceIndex": prune_index},
                    )
                )

            set_locale(page, "en")
            page.select_option("#challengeSelect", "root")
            page.click("#challengeBegin")
            page.select_option('[data-challenge-field="move"]', "B")
            page.fill('[data-challenge-field="value"]', "4")
            page.click("#challengeLock")
            locked = snapshot(page)
            for code in ("zh", "vi", "es", "en"):
                set_locale(page, code)
                checks.append(
                    (
                        f"{code} preserves a locked Guided Challenge prediction exactly",
                        snapshot(page) == locked
                        and page.locator('[data-challenge-field="move"]').input_value() == "B"
                        and page.locator('[data-challenge-field="value"]').input_value() == "4"
                        and page.locator('[data-challenge-field="move"]').is_disabled()
                        and page.locator('[data-challenge-field="value"]').is_disabled(),
                        {"locale": code},
                    )
                )

            set_locale(page, "zh")
            page.click("#challengeReveal")
            page.wait_for_timeout(80)
            revealed_machine = snapshot(page)
            revealed_texts = {"zh": page.locator("#challengeActual").inner_text()}
            checks.append(
                (
                    "Simplified Chinese reveal localizes both prediction verdict and mechanism explanation",
                    "预测正确" in revealed_texts["zh"]
                    and "MIN 从 A 返回 3、从 B 返回 4" in revealed_texts["zh"],
                    {"actual": revealed_texts["zh"]},
                )
            )
            reveal_phrases = {
                "vi": ("Dự đoán khớp", "MIN trả về 3 từ A và 4 từ B"),
                "es": ("La predicción coincidió", "MIN devuelve 3 desde A y 4 desde B"),
                "en": ("Prediction matched", "MIN returns 3 from A and 4 from B"),
            }
            for code in ("vi", "es", "en"):
                set_locale(page, code)
                actual = page.locator("#challengeActual").inner_text()
                revealed_texts[code] = actual
                checks.append(
                    (
                        f"already-revealed challenge re-localizes to {code} without recomputation",
                        all(phrase in actual for phrase in reveal_phrases[code])
                        and snapshot(page) == revealed_machine,
                        {"actual": actual},
                    )
                )

            page.select_option("#scenario", "good_ordering")
            page.select_option("#algorithm", "alpha_beta")
            page.select_option("#order", "configured")
            page.click("#endTrace")
            page.click("#saveBaseline")
            page.select_option("#order", "reverse")
            page.click("#endTrace")
            baseline_state = snapshot(page)
            comparison_phrases = {
                "zh": ("已保存：", "求值 4 个叶节点", "求值 6 个叶节点"),
                "vi": ("Đã lưu:", "đánh giá 4 lá", "đánh giá 6 lá"),
                "es": ("Guardado:", "4 hojas evaluadas", "6 hojas evaluadas"),
                "en": ("Saved:", "4 leaves", "6 leaves"),
            }
            for code in ("zh", "vi", "es", "en"):
                set_locale(page, code)
                comparison = page.locator("#baseline").inner_text()
                checks.append(
                    (
                        f"dynamic saved-run comparison localizes to {code}",
                        all(phrase in comparison for phrase in comparison_phrases[code])
                        and snapshot(page) == baseline_state,
                        {"comparison": comparison},
                    )
                )

            context.close()

            deep_link_expectations = {
                "zh": ("zh-Hans", "博弈树：Minimax 与 Alpha-Beta 剪枝"),
                "vi": ("vi", "Cây trò chơi: Minimax và cắt tỉa Alpha-Beta"),
                "es": ("es", "Árboles de juego: Minimax y poda Alpha-Beta"),
            }
            for code, (html_lang, title) in deep_link_expectations.items():
                linked = browser.new_context(viewport={"width": 900, "height": 900})
                lpage = linked.new_page()
                lpage.on("pageerror", lambda exc: page_errors.append(str(exc)))
                lpage.on(
                    "console",
                    lambda msg: console_errors.append(msg.text)
                    if msg.type == "error"
                    else None,
                )
                lpage.goto(
                    OUTPUT.resolve().as_uri() + f"?lang={code}",
                    wait_until="domcontentloaded",
                    timeout=30_000,
                )
                lpage.wait_for_function("() => !!window.Lab15Localization")
                checks.append(
                    (
                        f"{code} query deep link initializes the requested locale",
                        lpage.locator("html").get_attribute("lang") == html_lang
                        and lpage.title() == title
                        and lpage.locator("#lab15-language-select").input_value() == code,
                        {
                            "lang": lpage.locator("html").get_attribute("lang"),
                            "title": lpage.title(),
                        },
                    )
                )
                linked.close()

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
            rpage.goto(OUTPUT.resolve().as_uri() + "?lang=vi", wait_until="domcontentloaded", timeout=30_000)
            rpage.wait_for_function("() => !!window.Lab15Localization")
            rpage.select_option("#scenario", "first_prune")
            rpage.select_option("#algorithm", "alpha_beta")
            ri = rpage.evaluate(
                "() => window.Lab15Prototype.getResult().trace.findIndex(e => e.event==='prune')"
            )
            rpage.evaluate("index => window.Lab15Prototype.setTraceIndex(index)", ri)
            rpage.wait_for_timeout(80)
            checks.append(
                (
                    "Vietnamese reduced-motion path keeps complete localized prune and text state",
                    rpage.locator("#tree .node.pruned .value").inner_text() == "ĐÃ CẮT"
                    and "cắt tỉa" in rpage.locator("#traceTitle").inner_text().lower()
                    and "pruned_not_evaluated=B2" in rpage.locator("#textState").inner_text(),
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
            mpage.goto(OUTPUT.resolve().as_uri() + "?lang=es", wait_until="domcontentloaded", timeout=30_000)
            mpage.wait_for_function("() => !!window.Lab15Localization")
            page_overflow = mpage.evaluate(
                "() => document.documentElement.scrollWidth - window.innerWidth"
            )
            tree_scroll = mpage.evaluate(
                "() => { const el=document.querySelector('.tree-wrap'); return el.scrollWidth > el.clientWidth; }"
            )
            checks.append(
                (
                    "Spanish R6 page fits 390px while the wide tree remains internally scrollable",
                    page_overflow <= 1
                    and tree_scroll
                    and mpage.locator("#lab15-language-select").is_visible(),
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
        "harness": "tools/test_minimax_alpha_beta_multilingual_applet.py",
        "candidate": str(OUTPUT.relative_to(ROOT)),
        "r4_source_freeze": R4_SOURCE_FREEZE,
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
