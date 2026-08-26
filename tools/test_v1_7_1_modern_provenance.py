#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
MODERN = ("transformer-language-model", "agent-tool-context", "minimax-alpha-beta")
PORTFOLIO = "https://lmdixon23.github.io/"
ORCID = "https://orcid.org/0009-0001-0592-462X"


def main() -> int:
    checks = []
    for slug in MODERN:
        source = (SITE / "playgrounds" / slug / "index.html").read_text(encoding="utf-8")
        prefs_start = source.find('<div class="header-prefs">')
        prefs_end = source.find('</div>', prefs_start)
        theme_pos = source.find('id="ap-standard-theme"')
        checks.extend([
            (f"{slug}: established portfolio", PORTFOLIO in source),
            (f"{slug}: established ORCID", ORCID in source),
            (f"{slug}: no alternate portfolio", "https://logandixon.me" not in source),
            (f"{slug}: no alternate ORCID", "0009-0008-1712-6630" not in source),
            (f"{slug}: shared theme preference key", "ai-playgrounds-theme" not in source and "localStorage.setItem('theme'" in source),
            (f"{slug}: theme lives in header preference row", prefs_start >= 0 and prefs_start < theme_pos < prefs_end),
        ])
    failed = [name for name, ok in checks if not ok]
    payload = {
        "harness": "tools/test_v1_7_1_modern_provenance.py",
        "checks": len(checks),
        "passed": len(checks) - len(failed),
        "failed": len(failed),
        "pass": not failed,
        "failures": failed,
    }
    print(json.dumps(payload, indent=2))
    return 0 if payload["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
