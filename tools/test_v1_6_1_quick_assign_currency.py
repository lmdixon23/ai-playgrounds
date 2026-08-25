#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
REGISTRY = ROOT / "tools" / "quick_assigns_v1.json"


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
        [sys.executable, str(ROOT / "tools" / "build_site_v1_6_1_public.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if build.returncode:
        print(build.stdout)
        print(build.stderr, file=sys.stderr)
        return build.returncode

    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))["activities"]
    active = [row for row in registry if row["status"] == "active"]
    reserved = [row for row in registry if row["status"] == "reserved"]
    checks: list[tuple[str, bool, object]] = []

    files = sorted(p for p in SITE.rglob("*") if p.is_file())
    applets = sorted((SITE / "playgrounds").glob("*/index.html"))
    checks.append(("public boundary remains 58 files / 15 applets", len(files) == 58 and len(applets) == 15, {"files": len(files), "applets": len(applets)}))
    checks.append(("registry reserves exactly 15 unique IDs", len(registry) == 15 and len({r["id"] for r in registry}) == 15, {"ids": [r["id"] for r in registry]}))
    checks.append(("initial canary set is first four course labs", [r["slug"] for r in active] == ["search-pathfinding", "hill-climbing", "wumpus-world", "cnf-sat"], {"active": [r["id"] for r in active]}))

    landing = (SITE / "index.html").read_text(encoding="utf-8")
    checks.append(("landing has no stale fourteen-app current copy", not re.search(r"\bFourteen\b|\bfourteen\b", landing), {}))
    checks.append(("landing retains fifteen-app currency", "Fifteen" in landing and "15" in landing, {}))
    curriculum = (SITE / "curriculum.html").read_text(encoding="utf-8")
    checks.append(("curriculum states 13 Foundations plus two Modern", ("13 Foundations" in curriculum or "thirteen Foundations" in curriculum) and "two Modern AI extensions" in curriculum, {}))
    checks.append(("curriculum has exactly 13 course rows", curriculum.count('class="order-dot"') == 13, {"rows": curriculum.count('class="order-dot"')}))
    teacher = (SITE / "teacher-pack.html").read_text(encoding="utf-8")
    checks.append(("Teacher Pack scopes learner and support locales separately", "All 15 learner applets support English, Simplified Chinese, Vietnamese, and Spanish" in teacher and "Teacher Pack" in teacher and "English-only" in teacher, {}))

    for row in active:
        src = (SITE / "playgrounds" / row["slug"] / "index.html").read_text(encoding="utf-8")
        checks.append((f"{row['id']} stable anchor and five-stage response surface", src.count(f'data-quick-assign-id="{row["id"]}"') == 1 and f'id="{row["anchor"]}"' in src and all(f'data-lab-answer="{stage}"' in src for stage in ("predict", "observe", "explain", "transfer")) and 'data-lab-action="copy"' in src and 'data-lab-action="print"' in src, {}))
        checks.append((f"{row['id']} carries four-locale Quick Assign overlay", 'data-quick-assign-locales="1"' in src and "r4languagechange" in src, {}))
        canonical_suffix = f"index.html?mode=classroom#{row['anchor']}"
        checks.append((f"{row['id']} Teacher Pack uses classroom-mode deep link", f"playgrounds/{row['slug']}/{canonical_suffix}" in teacher, {}))
        checks.append((f"{row['id']} Curriculum uses classroom-mode deep link", f"playgrounds/{row['slug']}/{canonical_suffix}" in curriculum, {}))
        legacy_suffix = f"index.html#{row['anchor']}"
        checks.append((f"{row['id']} support pages reject hidden-panel legacy deep link", f"playgrounds/{row['slug']}/{legacy_suffix}" not in teacher and f"playgrounds/{row['slug']}/{legacy_suffix}" not in curriculum, {}))
    for row in reserved:
        src = (SITE / "playgrounds" / row["slug"] / "index.html").read_text(encoding="utf-8")
        checks.append((f"reserved ID not surfaced: {row['id']}", f'data-quick-assign-id="{row["id"]}"' not in src, {}))

    page_errors: list[str] = []
    console_errors: list[str] = []
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("Playwright is required") from exc

    expected_words = {
        "en": ("Quick Assign", "Predict"),
        "zh": ("快速任务", "预测"),
        "vi": ("Bài tập nhanh", "Dự đoán"),
        "es": ("Tarea rápida", "Predice"),
    }

    with sync_playwright() as p:
        browser = launch(p)
        try:
            for row in active:
                context = browser.new_context(viewport={"width": 390, "height": 844}, reduced_motion="reduce")
                page = context.new_page()
                page.on("pageerror", lambda exc, aid=row["id"]: page_errors.append(f"{aid}: {exc}"))
                page.on("console", lambda msg, aid=row["id"]: console_errors.append(f"{aid}: {msg.text}") if msg.type == "error" else None)
                url = (SITE / "playgrounds" / row["slug"] / "index.html").resolve().as_uri() + f"?mode=classroom#{row['anchor']}"
                page.goto(url, wait_until="domcontentloaded", timeout=30_000)
                page.wait_for_timeout(250)
                details = page.locator(f"#{row['anchor']}")
                checks.append((f"{row['id']} deep anchor resolves", details.count() == 1, {}))
                mode_selected = page.locator('.learning-mode-tab[data-mode="classroom"]').get_attribute("aria-selected")
                checks.append((f"{row['id']} direct link opens Use in class mode", mode_selected == "true", {"aria_selected": mode_selected}))
                details.evaluate("el => el.open = true")
                predict = details.locator('[data-lab-answer="predict"]')
                predict.fill("state-preservation sentinel")
                for locale in ("en", "zh", "vi", "es"):
                    ready = page.evaluate("() => !!window.__r4Localization && window.__r4Localization.ready()")
                    if ready:
                        page.evaluate("code => window.__r4Localization.setLocale(code,{immediate:true})", locale)
                        page.wait_for_timeout(120)
                    summary = details.locator("summary").inner_text()
                    label = details.locator('label[for="lab-predict"]').inner_text()
                    value = predict.input_value()
                    w1, w2 = expected_words[locale]
                    checks.append((f"{row['id']} {locale} Quick Assign surface and state", w1 in summary and w2 in label and value == "state-preservation sentinel", {"summary": summary, "label": label, "value": value}))
                layout = page.evaluate("""() => {
                    const width = innerWidth;
                    const scroll = document.documentElement.scrollWidth;
                    const offenders = [...document.querySelectorAll('body *')]
                      .filter(el => {
                        const s = getComputedStyle(el);
                        if (s.display === 'none' || s.visibility === 'hidden') return false;
                        const r = el.getBoundingClientRect();
                        return r.right > width + 2 || r.left < -2;
                      })
                      .slice(0, 12)
                      .map(el => {
                        const r = el.getBoundingClientRect();
                        return {
                          tag: el.tagName,
                          id: el.id || '',
                          cls: typeof el.className === 'string' ? el.className.slice(0,120) : '',
                          left: Math.round(r.left),
                          right: Math.round(r.right),
                          width: Math.round(r.width),
                          text: (el.textContent || '').trim().replace(/\\s+/g,' ').slice(0,100)
                        };
                      });
                    return {width,scroll,offenders};
                  }""")
                checks.append((f"{row['id']} 390px containment", layout["scroll"] <= layout["width"] + 2, layout))
                context.close()
        finally:
            browser.close()

    failures = [{"name": name, "detail": detail} for name, ok, detail in checks if not ok]
    payload = {
        "harness": "tools/test_v1_6_1_quick_assign_currency.py",
        "checks": len(checks),
        "passed": len(checks) - len(failures),
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
