#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"


def main() -> int:
    run = subprocess.run([sys.executable, str(ROOT / "tools" / "build_site_v1_6_2.py")], cwd=ROOT, text=True, capture_output=True)
    if run.returncode:
        print(run.stdout)
        print(run.stderr, file=sys.stderr)
        return run.returncode

    checks: list[tuple[str, bool, dict]] = []
    def check(name: str, ok: bool, detail=None) -> None:
        checks.append((name, bool(ok), detail or {}))

    html_files = sorted(SITE.rglob("*.html"))
    applets = sorted((SITE / "playgrounds").glob("*/index.html"))
    check("15 public applets", len(applets) == 15, {"count": len(applets)})

    for path in applets:
        rel = str(path.relative_to(SITE))
        html = path.read_text(encoding="utf-8")
        check(f"{rel}: v1.6.2 metadata", '<meta name="ai-playgrounds-version" content="1.6.2">' in html)
        check(f"{rel}: v1.6.2 analytics marker", html.count('data-ai-playgrounds-analytics="v1.6.2"') == 1, {"count": html.count('data-ai-playgrounds-analytics="v1.6.2"')})
        check(f"{rel}: no stale analytics marker", 'data-ai-playgrounds-analytics="v1.6.0"' not in html and 'data-ai-playgrounds-analytics="v1.6.1"' not in html)

    for path in html_files:
        rel = str(path.relative_to(SITE))
        html = path.read_text(encoding="utf-8")
        if 'data-ai-playgrounds-analytics=' in html:
            check(f"{rel}: measured-page analytics provenance", html.count('data-ai-playgrounds-analytics="v1.6.2"') == 1)

    home = (SITE / "index.html").read_text(encoding="utf-8")
    check("home visible version current", '<span class="site-version">v1.6.2</span>' in home)
    check("home no legacy visible current-version marker", '<span class="site-version">v1.6.0</span>' not in home and '<span class="site-version">v1.6.1</span>' not in home)
    check("home retains fifteen-lab current copy", "Explore the fifteen applets" in home and "15 inspectable applets" in home)
    check("home no literal undefined", "undefinedundefined" not in home and ">undefined<" not in home)

    for slug in ("transformer-language-model", "agent-tool-context", "minimax-alpha-beta"):
        html = (SITE / "playgrounds" / slug / "index.html").read_text(encoding="utf-8")
        check(f"{slug}: no stale v1.6.0 token", "v1.6.0" not in html)
        check(f"{slug}: shared shell current", 'data-ap-standard-shell' in html and 'AI Playgrounds · v1.6.2' in html)

    for page in ("teacher-pack.html", "curriculum.html", "quality.html", "student-lab.html", "research-and-citation.html"):
        path = SITE / page
        if not path.exists():
            continue
        html = path.read_text(encoding="utf-8")
        if 'data-v14-support-version="true"' in html:
            check(f"{page}: support provenance current", 'data-v14-support-version="true">AI Playgrounds · v1.6.2<' in html)

    notes = (SITE / "release-notes.html").read_text(encoding="utf-8")
    check("release notes current and historical ordering", notes.find('id="release-v1-6-2"') < notes.find('id="release-v1-6-1"') < notes.find('id="release-v1-6-0"'))

    failures = [{"name": name, "detail": detail} for name, ok, detail in checks if not ok]
    payload = {
        "harness": "tools/test_v1_6_2_public_provenance.py",
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
