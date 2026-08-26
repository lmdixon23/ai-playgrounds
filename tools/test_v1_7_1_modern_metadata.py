#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
MODERN = ("transformer-language-model", "agent-tool-context", "minimax-alpha-beta")
PUBLIC_ROOT = "https://lmdixon23.github.io/ai-playgrounds/"
ORCID = "https://orcid.org/0009-0001-0592-462X"


def count(pattern: str, source: str) -> int:
    return len(re.findall(pattern, source, flags=re.I | re.S))


def main() -> int:
    manifest = {row["slug"]: row for row in json.loads((SITE / "applets.json").read_text(encoding="utf-8"))}
    checks: list[tuple[str, bool, object]] = []
    def check(name: str, ok: bool, detail: object = None):
        checks.append((name, bool(ok), detail))

    governed = {
        "description": r'<meta\b(?=[^>]*\bname=["\']description["\'])[^>]*>',
        "og:type": r'<meta\b(?=[^>]*\bproperty=["\']og:type["\'])[^>]*>',
        "og:url": r'<meta\b(?=[^>]*\bproperty=["\']og:url["\'])[^>]*>',
        "og:title": r'<meta\b(?=[^>]*\bproperty=["\']og:title["\'])[^>]*>',
        "og:description": r'<meta\b(?=[^>]*\bproperty=["\']og:description["\'])[^>]*>',
        "og:image": r'<meta\b(?=[^>]*\bproperty=["\']og:image["\'])[^>]*>',
        "twitter:card": r'<meta\b(?=[^>]*\bname=["\']twitter:card["\'])[^>]*>',
        "twitter:title": r'<meta\b(?=[^>]*\bname=["\']twitter:title["\'])[^>]*>',
        "twitter:description": r'<meta\b(?=[^>]*\bname=["\']twitter:description["\'])[^>]*>',
        "twitter:image": r'<meta\b(?=[^>]*\bname=["\']twitter:image["\'])[^>]*>',
    }

    for slug in MODERN:
        source = (SITE / "playgrounds" / slug / "index.html").read_text(encoding="utf-8")
        row = manifest[slug]
        canonical = f"{PUBLIC_ROOT}playgrounds/{slug}/"
        expected_title = f'{row["title"]} | AI Playgrounds'

        for label, pattern in governed.items():
            check(f"{slug}: exactly one {label}", count(pattern, source) == 1, count(pattern, source))
        check(f"{slug}: exactly one favicon", count(r'<link\b(?=[^>]*\brel=["\']icon["\'])[^>]*>', source) == 1)
        check(f"{slug}: exactly one JSON-LD", count(r'<script\b(?=[^>]*\btype=["\']application/ld\+json["\'])[^>]*>.*?</script>', source) == 1)
        check(f"{slug}: exactly one canonical", count(r'<link\b(?=[^>]*\brel=["\']canonical["\'])[^>]*>', source) == 1)
        check(f"{slug}: canonical is exact", canonical in source)
        check(f"{slug}: public title carries suite name", f'<title>{expected_title}</title>' in source)
        check(f"{slug}: description comes from final catalogue", row["desc"] in source)
        check(f"{slug}: social image is suite image", f'{PUBLIC_ROOT}og-image.png' in source)
        check(f"{slug}: structured author uses established ORCID", ORCID in source)
        check(f"{slug}: JSON-LD declares web application", '"WebApplication"' in source)
        check(f"{slug}: JSON-LD declares learning resource", '"LearningResource"' in source)
        check(f"{slug}: JSON-LD declares four learner locales", '"inLanguage":["en","zh","vi","es"]' in source)

        for hreflang in ("en", "zh-Hans", "vi", "es", "x-default"):
            pattern = rf'<link\b(?=[^>]*\brel=["\']alternate["\'])(?=[^>]*\bhreflang=["\']{re.escape(hreflang)}["\'])[^>]*>'
            check(f"{slug}: one {hreflang} alternate", count(pattern, source) == 1, count(pattern, source))
        check(f"{slug}: exactly five alternates", count(r'<link\b(?=[^>]*\brel=["\']alternate["\'])[^>]*>', source) == 5)

    failures = [{"name": name, "detail": detail} for name, ok, detail in checks if not ok]
    payload = {
        "harness": "tools/test_v1_7_1_modern_metadata.py",
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
