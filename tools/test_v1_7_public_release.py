#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
REGISTRY = ROOT / "tools" / "quick_assigns_v2.json"


def main() -> int:
    run = subprocess.run([sys.executable, str(ROOT / "tools" / "build_site_v1_7.py")], cwd=ROOT, text=True, capture_output=True)
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
    check("public boundary 58 files / 15 applets", len(files) == 58 and len(applets) == 15, {"files": len(files), "applets": len(applets)})
    check("15 active unique Quick Assigns", len(rows) == 15 and len({r["id"] for r in rows}) == 15 and all(r.get("status") == "active" for r in rows))

    current_pages = [p for p in SITE.rglob("*.html") if p.name != "release-notes.html"]
    for path in current_pages:
        html = path.read_text(encoding="utf-8")
        if path in applets:
            check(f"{path.parent.name} version metadata 1.7.0", '<meta name="ai-playgrounds-version" content="1.7.0">' in html)
            check(f"{path.parent.name} analytics provenance 1.7.0", 'data-ai-playgrounds-analytics="v1.7.0"' in html)
        check(f"{path.relative_to(SITE)} no stale current v1.6.2 analytics", 'data-ai-playgrounds-analytics="v1.6.2"' not in html)

    home = (SITE / "index.html").read_text(encoding="utf-8")
    check("home visible release is v1.7.0", '<span class="site-version">v1.7.0</span>' in home)
    check("home has no undefined catalogue output", "undefinedundefined" not in home and re.search(r'>\s*undefined\s*<', home) is None)
    check("home retains four-language runtime and alternates", 'v161-home-four-locale-runtime' in home and 'hreflang="vi"' in home and 'hreflang="es"' in home)

    teacher = (SITE / "teacher-pack.html").read_text(encoding="utf-8")
    curriculum = (SITE / "curriculum.html").read_text(encoding="utf-8")
    for row in rows:
        canonical = f'playgrounds/{row["slug"]}/index.html?mode=classroom#{row["anchor"]}'
        source = (SITE / "playgrounds" / row["slug"] / "index.html").read_text(encoding="utf-8")
        check(f"{row['id']} exactly one applet surface", source.count(f'data-quick-assign-id="{row["id"]}"') == 1)
        check(f"{row['id']} Teacher Pack canonical link", row["id"] in teacher and canonical in teacher)
        check(f"{row['id']} Curriculum canonical link", row["id"] in curriculum and canonical in curriculum)

    for slug in ("transformer-language-model", "agent-tool-context", "minimax-alpha-beta"):
        html = (SITE / "playgrounds" / slug / "index.html").read_text(encoding="utf-8")
        check(f"{slug} modern Quick Assign runtime", html.count('data-quick-assign-modern-runtime="1"') == 1)
        check(f"{slug} canonical direct-open runtime", html.count('data-v17-quick-assign-direct-open="1"') == 1)
        check(f"{slug} modern Quick Assign containment", html.count('id="v17-modern-quick-assign-containment"') == 1)
    minimax = (SITE / "playgrounds" / "minimax-alpha-beta" / "index.html").read_text(encoding="utf-8")
    check("Minimax challenge selector mobile containment", '#challengeSelect{width:100%!important;max-width:100%!important;min-width:0!important' in minimax)

    for path in sorted((SITE / "activities").glob("*.html")):
        html = path.read_text(encoding="utf-8")
        check(f"{path.name} Activity Pack has no drifting current suite release", "current suite release v1.6." not in html and "current suite release v1.7." not in html)

    notes = (SITE / "release-notes.html").read_text(encoding="utf-8")
    check("release-note history preserved", all(f'id="release-{v}"' in notes for v in ("v1-7-0", "v1-6-2", "v1-6-1", "v1-6-0")))

    failures = [{"name": n, "detail": d} for n, ok, d in checks if not ok]
    payload = {
        "harness": "tools/test_v1_7_public_release.py",
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
