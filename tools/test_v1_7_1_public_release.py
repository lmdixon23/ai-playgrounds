#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
MODERN = ("transformer-language-model", "agent-tool-context", "minimax-alpha-beta")
REGISTRY = ROOT / "tools" / "quick_assigns_v2.json"


def main() -> int:
    run = subprocess.run([sys.executable, str(ROOT / "tools" / "build_site_v1_7_1.py")], cwd=ROOT, text=True, capture_output=True)
    if run.returncode:
        print(run.stdout)
        print(run.stderr, file=sys.stderr)
        return run.returncode

    checks: list[tuple[str, bool, object]] = []
    def check(name: str, ok: bool, detail=None) -> None:
        checks.append((name, bool(ok), detail or {}))

    files = sorted(p for p in SITE.rglob("*") if p.is_file())
    applets = sorted((SITE / "playgrounds").glob("*/index.html"))
    rows = json.loads(REGISTRY.read_text(encoding="utf-8"))["activities"]
    check("v1.7.1 public boundary remains 58 files / 15 applets", len(files) == 58 and len(applets) == 15, {"files": len(files), "applets": len(applets)})
    check("v1.7.1 preserves 15 active Quick Assigns", len(rows) == 15 and len({r["id"] for r in rows}) == 15 and all(r.get("status") == "active" for r in rows))

    for path in applets:
        html = path.read_text(encoding="utf-8")
        slug = path.parent.name
        check(f"{slug}: version metadata v1.7.1", '<meta name="ai-playgrounds-version" content="1.7.1">' in html)
        check(f"{slug}: analytics provenance v1.7.1", 'data-ai-playgrounds-analytics="v1.7.1"' in html)
        check(f"{slug}: no literal undefined output", "undefinedundefined" not in html and re.search(r'>\s*undefined\s*<', html) is None)

    home = (SITE / "index.html").read_text(encoding="utf-8")
    check("homepage visible release is v1.7.1", '<span class="site-version">v1.7.1</span>' in home)
    check("homepage retains 15-card/four-locale composition", 'v161-home-four-locale-runtime' in home and 'hreflang="vi"' in home and 'hreflang="es"' in home)

    teacher = (SITE / "teacher-pack.html").read_text(encoding="utf-8")
    curriculum = (SITE / "curriculum.html").read_text(encoding="utf-8")
    for row in rows:
        canonical = f'playgrounds/{row["slug"]}/index.html?mode=classroom#{row["anchor"]}'
        check(f"{row['id']}: Teacher Pack canonical link preserved", row["id"] in teacher and canonical in teacher)
        check(f"{row['id']}: Curriculum canonical link preserved", row["id"] in curriculum and canonical in curriculum)

    for slug in MODERN:
        html = (SITE / "playgrounds" / slug / "index.html").read_text(encoding="utf-8")
        for marker in (
            'class="ap-standard-header page-header"', 'id="ap-modern-share"', 'id="ap-modern-more"',
            'id="ap-modern-embed"', 'id="ap-modern-settings-json"', 'class="ap-modern-tldr"',
            'id="ap-modern-key-terms"', 'id="ap-modern-a11y"', 'id="ap-modern-a11y-state"',
            'id="ap-modern-fidelity"', 'class="ap-standard-footer ap-modern-rich-footer"',
            'id="v171-modern-toolbar-runtime"', 'id="v171-modern-packet-runtime"',
            'id="v171-modern-packet-label-runtime"', '<script type="application/ld+json">',
            'hreflang="en"', 'hreflang="zh-Hans"', 'hreflang="vi"', 'hreflang="es"', 'hreflang="x-default"',
        ):
            check(f"{slug}: {marker}", marker in html)
        panel = re.search(r'<details\s+id="ap-modern-a11y"([^>]*)>', html, flags=re.I)
        check(f"{slug}: structured accessibility panel is open", bool(panel and "open" in panel.group(1).lower()))
        check(f"{slug}: one Quick Assign surface", html.count('data-quick-assign-id="') == 1)
        check(f"{slug}: shared theme namespace", "ai-playgrounds-theme" not in html)

    notes = (SITE / "release-notes.html").read_text(encoding="utf-8")
    check("v1.7.1 and v1.7.0 release history present", 'id="release-v1-7-1"' in notes and 'id="release-v1-7-0"' in notes)

    failures = [{"name": n, "detail": d} for n, ok, d in checks if not ok]
    payload = {
        "harness": "tools/test_v1_7_1_public_release.py",
        "checks": len(checks),
        "passed": len(checks) - len(failures),
        "failed": len(failures),
        "pass": not failures,
        "failures": failures,
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
