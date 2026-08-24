#!/usr/bin/env python3
"""Verify every dynamic Wumpus percept-line localization case in VI and ES."""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CATALOG = ROOT / "assets" / "locales" / "wumpus-world-r4.js"

CASES = [
    "(1,1): -no breeze, -no stench",
    "(1,1): breeze, -no stench",
    "(1,1): -no breeze, stench",
    "(1,1): breeze, stench",
    "(1,1): -no breeze, -no stench, GLITTER!",
    "(1,1): breeze, -no stench, GLITTER!",
    "(1,1): -no breeze, stench, GLITTER!",
    "(1,1): breeze, stench, GLITTER!",
]

EXPECTED_TERMS = {
    "vi": {
        "forbidden": ("breeze", "stench", "GLITTER"),
        "required_any": ("gió", "mùi hôi"),
    },
    "es": {
        "forbidden": ("breeze", "stench", "GLITTER"),
        "required_any": ("brisa", "hedor"),
    },
}


def render_with_node() -> dict[str, list[str]]:
    payload = json.dumps(CASES, ensure_ascii=False)
    code = f"""
global.window={{}};
require({json.dumps(str(CATALOG))});
const d=window.__AI_PLAYGROUNDS_R4_LOCALES['wumpus-world'];
const cases={payload};
function apply(locale,input){{
  let out=input;
  for(const row of (d[locale].patterns||[])){{
    out=out.replace(new RegExp(row.source,row.flags||'g'),row.target);
  }}
  return out;
}}
process.stdout.write(JSON.stringify({{vi:cases.map(x=>apply('vi',x)),es:cases.map(x=>apply('es',x))}}));
"""
    proc = subprocess.run(
        ["node", "-e", code],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
    )
    if proc.returncode:
        raise RuntimeError(proc.stderr or proc.stdout)
    return json.loads(proc.stdout)


def main() -> int:
    outputs = render_with_node()
    failures: list[str] = []
    checks = 0

    for locale in ("vi", "es"):
        rows = outputs.get(locale) or []
        if len(rows) != len(CASES):
            failures.append(f"{locale}: output count {len(rows)} != {len(CASES)}")
            continue
        for index, (source, translated) in enumerate(zip(CASES, rows, strict=True)):
            checks += 1
            if translated == source:
                failures.append(f"{locale} case {index}: pattern did not match: {source}")
            if not translated.startswith("(1,1): "):
                failures.append(f"{locale} case {index}: coordinate prefix changed: {translated}")
            for forbidden in EXPECTED_TERMS[locale]["forbidden"]:
                if forbidden.lower() in translated.lower():
                    failures.append(f"{locale} case {index}: English percept term remains: {translated}")
            if not any(term in translated.lower() for term in EXPECTED_TERMS[locale]["required_any"]):
                failures.append(f"{locale} case {index}: expected localized percept vocabulary missing: {translated}")
            if "GLITTER!" in source:
                if locale == "vi" and "lấp lánh" not in translated.lower():
                    failures.append(f"vi case {index}: glitter not localized: {translated}")
                if locale == "es" and "brillo" not in translated.lower():
                    failures.append(f"es case {index}: glitter not localized: {translated}")

    payload = {
        "harness": "tools/verify_wumpus_percept_localization.py",
        "cases_per_locale": len(CASES),
        "checks": checks,
        "failed": len(failures),
        "pass": not failures,
        "outputs": outputs,
        "failures": failures,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    for failure in failures:
        print("FAIL: " + failure, file=sys.stderr)
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
