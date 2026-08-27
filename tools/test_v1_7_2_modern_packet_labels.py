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
EVIDENCE = ROOT / "release-evidence" / "v1.7.2-modern-behavior-qa.json"
MODERN = ("transformer-language-model", "agent-tool-context", "minimax-alpha-beta")
SOURCE_IDS = {
    "transformer-language-model": "stateText",
    "agent-tool-context": "stateText",
    "minimax-alpha-beta": "textState",
}
MECHANISM_CONTROLS = {
    "transformer-language-model": "#temperature",
    "agent-tool-context": "#scenario",
    "minimax-alpha-beta": "#algorithm",
}
EXPECTED = {
    "en": {"predict": "Predict", "observe": "Observe", "explain": "Explain", "transfer": "Transfer", "refresh": "Refresh state", "copy": "Copy packet", "print": "Print packet", "clear": "Clear local draft"},
    "zh": {"predict": "预测", "observe": "观察", "explain": "解释", "transfer": "迁移", "refresh": "更新状态", "copy": "复制实验包", "print": "打印实验包", "clear": "清除本地草稿"},
    "vi": {"predict": "Dự đoán", "observe": "Quan sát", "explain": "Giải thích", "transfer": "Chuyển giao", "refresh": "Làm mới trạng thái", "copy": "Sao chép gói bài", "print": "In gói bài", "clear": "Xóa bản nháp cục bộ"},
    "es": {"predict": "Predecir", "observe": "Observar", "explain": "Explicar", "transfer": "Transferir", "refresh": "Actualizar estado", "copy": "Copiar paquete", "print": "Imprimir paquete", "clear": "Borrar borrador local"},
}


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


@contextmanager
def local_site_server():
    handler = lambda *args, **kwargs: QuietHandler(*args, directory=str(SITE), **kwargs)
    with socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler) as server:
        server.daemon_threads = True
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            yield f"http://127.0.0.1:{server.server_address[1]}"
        finally:
            server.shutdown()
            thread.join(timeout=2)


def write_payload(payload: dict) -> None:
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def ensure_site() -> int:
    notes = SITE / "release-notes.html"
    if notes.is_file() and 'id="release-v1-7-2"' in notes.read_text(encoding="utf-8"):
        return 0
    build = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "build_site_v1_7_2.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=90,
    )
    if build.returncode:
        payload = {
            "harness": "tools/test_v1_7_2_modern_packet_labels.py",
            "stage": "build",
            "pass": False,
            "stdout": build.stdout[-12000:],
            "stderr": build.stderr[-12000:],
        }
        write_payload(payload)
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    return build.returncode


def state_text(page, source_id: str) -> str:
    return page.evaluate(
        "sid=>{const el=document.getElementById(sid);return String(el?.value||el?.textContent||'').trim()}",
        source_id,
    )


def navigate_ready(page, uri: str):
    """Wait for the final app contract, not the incidental window-load event."""
    response = page.goto(uri, wait_until="commit", timeout=20_000)
    page.wait_for_selector("#ap-standard-language-select", timeout=20_000)
    page.wait_for_selector("details[data-quick-assign-id]", timeout=20_000)
    page.wait_for_selector("#ap-modern-a11y-state", timeout=20_000)
    return response


def set_locale(page, locale: str) -> None:
    page.locator("#ap-standard-language-select").evaluate(
        "(el,value)=>{el.value=value;el.dispatchEvent(new Event('change',{bubbles:true}))}",
        locale,
    )
    page.wait_for_function(
        "value=>document.documentElement.lang.toLowerCase().startsWith(value)",
        arg=locale,
        timeout=10_000,
    )


def change_mechanism_state(page, slug: str) -> tuple[str, str]:
    source_id = SOURCE_IDS[slug]
    before = state_text(page, source_id)
    control = page.locator(MECHANISM_CONTROLS[slug])
    if slug == "transformer-language-model":
        control.evaluate(
            "el=>{const next=Math.min(Number(el.max),Number(el.value)+Number(el.step||0.25));el.value=String(next);el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}))}"
        )
    else:
        control.evaluate(
            "el=>{const options=[...el.options];const next=options.find(o=>o.value!==el.value);if(!next)throw new Error('No alternate mechanism option');el.value=next.value;el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}))}"
        )
    page.wait_for_function(
        "arg=>{const el=document.getElementById(arg.id);return String(el?.value||el?.textContent||'').trim()!==arg.before}",
        arg={"id": source_id, "before": before},
        timeout=5_000,
    )
    return before, state_text(page, source_id)


def main() -> int:
    if ensure_site():
        return 1

    checks: list[tuple[str, bool, object]] = []

    def check(name: str, ok: bool, detail: object = None) -> None:
        checks.append((name, bool(ok), detail))

    page_errors: list[str] = []
    console_errors: list[str] = []
    diagnostics: list[dict] = []

    from playwright.sync_api import sync_playwright

    instrumentation = """
    Object.defineProperty(navigator,'share',{configurable:true,value:undefined});
    Object.defineProperty(navigator,'clipboard',{configurable:true,value:{
      writeText:async text=>{window.__v172Clipboard=String(text)},
      readText:async()=>window.__v172Clipboard||''
    }});
    window.print=()=>{document.documentElement.dataset.v172PrintCalled='true'};
    """

    with local_site_server() as origin, sync_playwright() as playwright:
        browser = launch(playwright)
        try:
            for slug in MODERN:
                print(f"v1.7.2 behavior: {slug}", flush=True)
                context = browser.new_context(
                    viewport={"width": 390, "height": 844},
                    reduced_motion="reduce",
                    accept_downloads=True,
                )
                context.set_default_timeout(8_000)
                context.add_init_script(instrumentation)
                page = context.new_page()
                local_page_errors: list[str] = []
                local_console_errors: list[str] = []
                page.on("pageerror", lambda exc, target=local_page_errors: target.append(str(exc)))
                page.on("console", lambda msg, target=local_console_errors: target.append(msg.text) if msg.type == "error" else None)
                stage = "navigate"
                try:
                    response = navigate_ready(page, f"{origin}/playgrounds/{slug}/index.html?lang=en")
                    check(f"{slug}: local artifact HTTP 200", response is not None and response.status == 200, None if response is None else response.status)
                    qa = page.locator("details[data-quick-assign-id]")
                    qa.evaluate("el=>el.open=true")

                    stage = "mechanism"
                    source_id = SOURCE_IDS[slug]
                    page.wait_for_function(
                        "sid=>{const el=document.getElementById(sid);return !!String(el?.value||el?.textContent||'').trim()}",
                        arg=source_id,
                    )
                    before, after = change_mechanism_state(page, slug)
                    check(f"{slug}: real mechanism control changes accessible state", before != after, {"before": before[:160], "after": after[:160]})
                    qa.locator('[data-qa-action="refresh-state"]').click()
                    page.wait_for_function(
                        "sid=>{const source=document.getElementById(sid);const packet=document.querySelector('[data-qa-modern-state]');return String(source?.value||source?.textContent||'').trim()===String(packet?.textContent||'').trim()}",
                        arg=source_id,
                    )
                    snapshot = qa.locator("[data-qa-modern-state]").evaluate("el=>el.textContent.trim()")
                    check(f"{slug}: Refresh captures changed mechanism state", snapshot == after, {"state": after[:180], "snapshot": snapshot[:180]})
                    page.wait_for_function(
                        "sid=>{const source=document.getElementById(sid);const mirror=document.getElementById('ap-modern-a11y-state');return String(source?.value||source?.textContent||'').trim()===String(mirror?.textContent||'').trim()}",
                        arg=source_id,
                    )

                    stage = "responses-locales"
                    sentinels = {key: f"v172-{slug}-{key}" for key in ("predict", "observe", "explain", "transfer")}
                    for key, value in sentinels.items():
                        qa.locator(f'[data-qa-answer="{key}"]').fill(value)
                    english_summary = page.locator("#ap-modern-a11y>summary").inner_text().strip()
                    for locale in ("en", "zh", "vi", "es"):
                        print(f"v1.7.2 behavior: {slug} -> {locale}", flush=True)
                        set_locale(page, locale)
                        page.wait_for_function(
                            "expected=>document.querySelector('[data-qa-answer=\"predict\"]')?.getAttribute('aria-label')===expected",
                            arg=EXPECTED[locale]["predict"],
                        )
                        for key in ("predict", "observe", "explain", "transfer"):
                            check(
                                f"{slug}: {locale} {key} accessible label",
                                qa.locator(f'[data-qa-answer="{key}"]').get_attribute("aria-label") == EXPECTED[locale][key],
                            )
                            check(
                                f"{slug}: {key} response survives {locale} switch",
                                qa.locator(f'[data-qa-answer="{key}"]').input_value() == sentinels[key],
                            )
                        for action, key in (("refresh-state", "refresh"), ("copy", "copy"), ("print", "print"), ("clear", "clear")):
                            check(
                                f"{slug}: {locale} {action} accessible label",
                                qa.locator(f'[data-qa-action="{action}"]').get_attribute("aria-label") == EXPECTED[locale][key],
                            )
                        if locale != "en":
                            check(
                                f"{slug}: accessibility panel localizes to {locale}",
                                page.locator("#ap-modern-a11y>summary").inner_text().strip() != english_summary,
                            )

                    set_locale(page, "en")
                    page.wait_for_function(
                        "expected=>document.querySelector('[data-qa-answer=\"predict\"]')?.getAttribute('aria-label')===expected",
                        arg=EXPECTED["en"]["predict"],
                    )
                    after = state_text(page, source_id)
                    qa.locator('[data-qa-action="refresh-state"]').click()
                    page.wait_for_function(
                        "sid=>{const source=document.getElementById(sid);const packet=document.querySelector('[data-qa-modern-state]');return String(source?.value||source?.textContent||'').trim()===String(packet?.textContent||'').trim()}",
                        arg=source_id,
                    )

                    stage = "copy-share-embed"
                    qa.locator('[data-qa-action="copy"]').click()
                    page.wait_for_function("()=>!!window.__v172Clipboard")
                    packet = page.evaluate("window.__v172Clipboard")
                    check(f"{slug}: copied packet contains refreshed state", after in packet)
                    check(f"{slug}: copied packet contains all responses", all(value in packet for value in sentinels.values()), packet[-500:])

                    page.locator("#ap-modern-share").click()
                    page.wait_for_function("slug=>String(window.__v172Clipboard||'').includes('/playgrounds/'+slug+'/')", arg=slug)
                    shared = page.evaluate("window.__v172Clipboard")
                    check(f"{slug}: Share fallback copies current public URL", shared.startswith(origin) and f"/playgrounds/{slug}/" in shared, shared)

                    page.locator("#ap-modern-more").evaluate("el=>el.open=true")
                    page.locator("#ap-modern-embed").click()
                    page.wait_for_function("()=>String(window.__v172Clipboard||'').startsWith('<iframe')")
                    embed = page.evaluate("window.__v172Clipboard")
                    check(f"{slug}: Embed copies iframe markup", "<iframe" in embed and "embed=1" in embed and slug in embed, embed)

                    stage = "settings"
                    page.locator("#ap-modern-more").evaluate("el=>el.open=true")
                    with page.expect_download(timeout=5_000) as download_info:
                        page.locator("#ap-modern-settings-json").click()
                    download = download_info.value
                    settings = json.loads(pathlib.Path(download.path()).read_text(encoding="utf-8"))
                    serialized = json.dumps(settings, ensure_ascii=False)
                    check(f"{slug}: settings export identifies applet", settings.get("slug") == slug, settings)
                    check(f"{slug}: settings export contains mechanism values", bool(settings.get("values")), settings)
                    check(f"{slug}: settings export excludes response fields", all(value not in serialized for value in sentinels.values()), settings)

                    stage = "print"
                    with page.expect_popup(timeout=5_000) as popup_info:
                        qa.locator('[data-qa-action="print"]').click()
                    popup = popup_info.value
                    popup.wait_for_selector("body")
                    popup.wait_for_timeout(80)
                    printed = popup.locator("body").inner_text()
                    state_probe = max((line.strip() for line in after.splitlines() if line.strip()), key=len)
                    check(f"{slug}: print packet contains refreshed state", state_probe in printed, state_probe)
                    check(f"{slug}: print packet contains all responses", all(value in printed for value in sentinels.values()), printed[-500:])
                    check(
                        f"{slug}: print packet excludes application chrome",
                        popup.locator(".ap-standard-header,#ap-modern-more,[data-quick-assign-id]").count() == 0,
                    )
                    popup.close()

                    stage = "reduced-motion"
                    motion = page.locator("#ap-modern-a11y .ap-modern-a11y-card").first.evaluate(
                        "el=>{const s=getComputedStyle(el);return {animationName:s.animationName,animationDuration:s.animationDuration,transitionDuration:s.transitionDuration}}"
                    )
                    check(
                        f"{slug}: reduced-motion style is computed",
                        motion["animationName"] == "none"
                        and set(motion["animationDuration"].split(", ")) <= {"0s"}
                        and set(motion["transitionDuration"].split(", ")) <= {"0s"},
                        motion,
                    )
                except Exception as exc:
                    diagnostic = {
                        "slug": slug,
                        "stage": stage,
                        "error": str(exc),
                        "page_errors": local_page_errors,
                        "console_errors": local_console_errors,
                    }
                    diagnostics.append(diagnostic)
                    check(f"{slug}: exception at {stage}", False, diagnostic)
                page_errors.extend(local_page_errors)
                console_errors.extend(local_console_errors)
                context.close()

            for slug in MODERN:
                context = browser.new_context(viewport={"width": 1024, "height": 768})
                context.add_init_script(
                    "try{localStorage.removeItem('theme');localStorage.setItem('ai-playgrounds-theme','dark')}catch(_e){}"
                )
                page = context.new_page()
                local_errors: list[str] = []
                page.on("pageerror", lambda exc, target=local_errors: target.append(str(exc)))
                page.goto(f"{origin}/playgrounds/{slug}/index.html?lang=en", wait_until="load", timeout=20_000)
                page.wait_for_function("()=>document.body.classList.contains('ap-standard-dark')")
                storage = page.evaluate(
                    "()=>({theme:localStorage.getItem('theme'),legacy:localStorage.getItem('ai-playgrounds-theme'),pressed:document.getElementById('ap-standard-theme')?.getAttribute('aria-pressed')})"
                )
                check(
                    f"{slug}: legacy theme migrates once to canonical key",
                    storage == {"theme": "dark", "legacy": None, "pressed": "true"},
                    storage,
                )
                page_errors.extend(local_errors)
                context.close()
        finally:
            browser.close()

    failures = [{"name": name, "detail": detail} for name, ok, detail in checks if not ok]
    payload = {
        "harness": "tools/test_v1_7_2_modern_packet_labels.py",
        "checks": len(checks),
        "passed": len(checks) - len(failures),
        "failed": len(failures),
        "page_errors": page_errors,
        "console_errors": console_errors,
        "diagnostics": diagnostics,
        "pass": not failures and not page_errors and not console_errors,
        "failures": failures,
    }
    write_payload(payload)
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
