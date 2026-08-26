#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
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


def main() -> int:
    build = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "build_site_v1_7_1_modern_parity_accessible.py")],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    if build.returncode:
        print(build.stdout)
        print(build.stderr, file=sys.stderr)
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
            page = context.new_page()
            page.on("pageerror", lambda exc: page_errors.append(str(exc)))
            page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            for slug in MODERN:
                page.goto((SITE / "playgrounds" / slug / "index.html").resolve().as_uri() + "?lang=en", wait_until="load", timeout=20_000)
                page.wait_for_selector("#ap-standard-language-select", timeout=5_000)
                qa = page.locator("details[data-quick-assign-id]")
                qa.evaluate("el=>el.open=true")
                page.wait_for_timeout(40)

                original_answers = {}
                for key in ("predict", "observe", "explain", "transfer"):
                    field = qa.locator(f'[data-qa-answer="{key}"]')
                    label = field.get_attribute("aria-label") or ""
                    original_answers[key] = label
                    check(f"{slug}: EN {key} aria-label", label == EXPECTED["en"][key], label)
                for action, expected_key in (("refresh-state", "refresh"), ("copy", "copy"), ("print", "print"), ("clear", "clear")):
                    button = qa.locator(f'[data-qa-action="{action}"]')
                    check(f"{slug}: EN {action} label", button.get_attribute("aria-label") == EXPECTED["en"][expected_key], button.get_attribute("aria-label"))

                for locale in ("vi", "es"):
                    page.select_option("#ap-standard-language-select", locale)
                    page.wait_for_timeout(120)
                    for key in ("predict", "observe", "explain", "transfer"):
                        field = qa.locator(f'[data-qa-answer="{key}"]')
                        check(f"{slug}: {locale} {key} aria-label", field.get_attribute("aria-label") == EXPECTED[locale][key], field.get_attribute("aria-label"))
                    for action, expected_key in (("refresh-state", "refresh"), ("copy", "copy"), ("print", "print"), ("clear", "clear")):
                        button = qa.locator(f'[data-qa-action="{action}"]')
                        check(f"{slug}: {locale} {action} label", button.get_attribute("aria-label") == EXPECTED[locale][expected_key], button.get_attribute("aria-label"))
                    page.select_option("#ap-standard-language-select", "en")
                    page.wait_for_timeout(120)
                    for key, expected in original_answers.items():
                        check(f"{slug}: EN {key} aria-label restores after {locale}", qa.locator(f'[data-qa-answer="{key}"]').get_attribute("aria-label") == expected)

                qa.locator('[data-qa-action="refresh-state"]').click()
                state_text = qa.locator("[data-qa-modern-state]").inner_text().strip()
                check(f"{slug}: state snapshot remains available after label round trips", bool(state_text), state_text[:120])
            context.close()
        finally:
            browser.close()

    failures = [{"name": n, "detail": d} for n, ok, d in checks if not ok]
    payload = {
        "harness": "tools/test_v1_7_1_modern_packet_labels.py",
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
