#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
EVIDENCE = ROOT / "release-evidence" / "v1.7.1-modern-packet-label-qa.json"
MODERN = ("transformer-language-model", "agent-tool-context", "minimax-alpha-beta")
EXPECTED = {
    "en": {"predict":"Predict", "observe":"Observe", "explain":"Explain", "transfer":"Transfer", "refresh":"Refresh state", "copy":"Copy packet", "print":"Print packet", "clear":"Clear local draft"},
    "vi": {"predict":"Dự đoán", "observe":"Quan sát", "explain":"Giải thích", "transfer":"Chuyển giao", "refresh":"Làm mới trạng thái", "copy":"Sao chép gói bài", "print":"In gói bài", "clear":"Xóa bản nháp cục bộ"},
    "es": {"predict":"Predecir", "observe":"Observar", "explain":"Explicar", "transfer":"Transferir", "refresh":"Actualizar estado", "copy":"Copiar paquete", "print":"Imprimir paquete", "clear":"Borrar borrador local"},
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


def write_payload(payload: dict) -> None:
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    build = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "build_site_v1_7_1_modern_parity_accessible.py")],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    if build.returncode:
        payload = {
            "harness": "tools/test_v1_7_1_modern_packet_labels.py",
            "stage": "build",
            "pass": False,
            "stdout": build.stdout[-12000:],
            "stderr": build.stderr[-12000:],
        }
        write_payload(payload)
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return build.returncode

    checks: list[tuple[str, bool, object]] = []
    def check(name: str, ok: bool, detail: object = None):
        checks.append((name, bool(ok), detail))

    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("Playwright is required for modern packet-label QA") from exc

    page_errors: list[str] = []
    console_errors: list[str] = []
    with sync_playwright() as p:
        browser = launch(p)
        try:
            context = browser.new_context(viewport={"width": 390, "height": 844}, reduced_motion="reduce")
            context.set_default_timeout(12_000)
            for slug in MODERN:
                # This gate owns DOM/localization/accessibility parity. Real file://
                # navigation is already exercised by the dedicated Lab 13/14/15 and
                # final browser suites. Load the exact generated single-file document
                # directly so irrelevant browser lifecycle timing cannot mask the
                # contract this gate is designed to test.
                page = context.new_page()
                page.on("pageerror", lambda exc: page_errors.append(str(exc)))
                page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
                html = (SITE / "playgrounds" / slug / "index.html").read_text(encoding="utf-8")
                page.set_content(html, wait_until="domcontentloaded", timeout=30_000)
                page.wait_for_selector("#ap-standard-language-select", state="attached", timeout=12_000)
                page.wait_for_selector("#ap-modern-a11y", state="attached", timeout=12_000)
                page.wait_for_selector("details[data-quick-assign-id]", state="attached", timeout=12_000)
                page.wait_for_selector("#ap-modern-a11y-state", state="attached", timeout=12_000)
                page.wait_for_function(
                    "() => { const el=document.querySelector('#ap-modern-a11y-state'); return el && el.textContent.trim() && !el.textContent.toLowerCase().includes('preparing'); }",
                    timeout=12_000,
                )

                a11y = page.locator("#ap-modern-a11y")
                check(f"{slug}: structured accessibility layer open by default", a11y.get_attribute("open") is not None)
                check(f"{slug}: accessibility keyboard card present", a11y.locator("#ap-modern-a11y-keyboard-title").count() == 1)
                check(f"{slug}: accessibility reduced-motion card present", a11y.locator("#ap-modern-a11y-motion-title").count() == 1)
                a11y_state = a11y.locator("#ap-modern-a11y-state")
                check(f"{slug}: accessibility text state present", a11y_state.count() == 1)
                state_value = (a11y_state.text_content() or "").strip()
                check(f"{slug}: accessibility text state mirrors a real mechanism state", bool(state_value) and "preparing" not in state_value.lower(), state_value[:160])

                qa = page.locator("details[data-quick-assign-id]")
                qa.evaluate("el=>el.open=true")
                page.wait_for_timeout(120)

                original_answers = {}
                for key in ("predict", "observe", "explain", "transfer"):
                    field = qa.locator(f'[data-qa-answer="{key}"]')
                    label = field.get_attribute("aria-label") or ""
                    original_answers[key] = label
                    check(f"{slug}: EN {key} aria-label", label == EXPECTED["en"][key], label)
                for action, expected_key in (("refresh-state", "refresh"), ("copy", "copy"), ("print", "print"), ("clear", "clear")):
                    button = qa.locator(f'[data-qa-action="{action}"]')
                    actual = button.get_attribute("aria-label")
                    check(f"{slug}: EN {action} label", actual == EXPECTED["en"][expected_key], actual)

                for locale in ("vi", "es"):
                    page.select_option("#ap-standard-language-select", locale)
                    page.wait_for_function(
                        "loc => document.documentElement.lang.toLowerCase().startsWith(loc)",
                        arg=locale,
                        timeout=12_000,
                    )
                    page.wait_for_timeout(220)
                    check(f"{slug}: accessibility summary localizes to {locale}", (a11y.locator("summary").inner_text() or "").strip() not in ("", "♿ Text and keyboard support"))
                    for key in ("predict", "observe", "explain", "transfer"):
                        field = qa.locator(f'[data-qa-answer="{key}"]')
                        actual = field.get_attribute("aria-label")
                        check(f"{slug}: {locale} {key} aria-label", actual == EXPECTED[locale][key], actual)
                    for action, expected_key in (("refresh-state", "refresh"), ("copy", "copy"), ("print", "print"), ("clear", "clear")):
                        button = qa.locator(f'[data-qa-action="{action}"]')
                        actual = button.get_attribute("aria-label")
                        check(f"{slug}: {locale} {action} label", actual == EXPECTED[locale][expected_key], actual)
                    page.select_option("#ap-standard-language-select", "en")
                    page.wait_for_function("() => document.documentElement.lang.toLowerCase().startsWith('en')", timeout=12_000)
                    page.wait_for_timeout(220)
                    check(f"{slug}: accessibility summary restores English after {locale}", a11y.locator("summary").inner_text().strip() == "♿ Text and keyboard support")
                    for key, expected in original_answers.items():
                        actual = qa.locator(f'[data-qa-answer="{key}"]').get_attribute("aria-label")
                        check(f"{slug}: EN {key} aria-label restores after {locale}", actual == expected, actual)

                qa.locator('[data-qa-action="refresh-state"]').click()
                state_text = qa.locator("[data-qa-modern-state]").inner_text().strip()
                check(f"{slug}: state snapshot remains available after label round trips", bool(state_text), state_text[:120])
                page.close()
            context.close()
        finally:
            browser.close()

    failures = [{"name": n, "detail": d} for n, ok, d in checks if not ok]
    payload = {
        "harness": "tools/test_v1_7_1_modern_packet_labels.py",
        "stage": "browser",
        "checks": len(checks),
        "passed": len(checks) - len(failures),
        "failed": len(failures),
        "page_errors": page_errors,
        "console_errors": console_errors,
        "pass": not failures and not page_errors and not console_errors,
        "failures": failures,
    }
    write_payload(payload)
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
