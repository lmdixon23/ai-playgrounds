#!/usr/bin/env python3
"""Build the self-contained English Lab 15 candidate from the accepted R3 prototype."""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOTYPE = ROOT / "tools" / "minimax_alpha_beta_prototype.html"
CORE = ROOT / "tools" / "minimax_alpha_beta_core.js"
DEFAULT_OUTPUT = ROOT / "release-evidence" / "lab15-minimax-alpha-beta-english-candidate.html"


def build_candidate(output: Path) -> Path:
    html = PROTOTYPE.read_text(encoding="utf-8")
    core = CORE.read_text(encoding="utf-8")

    external_marker = '<script src="minimax_alpha_beta_core.js"></script>'
    if html.count(external_marker) != 1:
        raise RuntimeError("R3 prototype must contain exactly one external Lab 15 core marker")

    inline_core = (
        '<script id="lab15-minimax-alpha-beta-core">\n'
        + core
        + '\n</script>'
    )
    html = html.replace(external_marker, inline_core, 1)
    html = html.replace("R3 English prototype", "R4 English candidate", 1)

    stage_meta = '<meta name="lab15-candidate-stage" content="R4-English">\n'
    if "lab15-candidate-stage" not in html:
        html = html.replace("</head>", stage_meta + "</head>", 1)

    required = (
        'id="lab15-minimax-alpha-beta-core"',
        'name="lab15-candidate-stage" content="R4-English"',
        "window.Lab15GameTreeCore",
        "window.Lab15Prototype",
        "Guided Challenge",
        "Pruned nodes",
        "not evaluated",
    )
    missing = [item for item in required if item not in html]
    if missing:
        raise RuntimeError(f"Lab 15 English candidate is incomplete: {missing}")

    forbidden = (
        'src="minimax_alpha_beta_core.js"',
        "fetch(",
        "XMLHttpRequest",
        "WebSocket",
        "EventSource",
    )
    present = [item for item in forbidden if item in html]
    if present:
        raise RuntimeError(f"Lab 15 English candidate is not offline/self-contained: {present}")

    if html.count("function minimax(") != 1:
        raise RuntimeError("Lab 15 candidate must contain exactly one minimax implementation")
    if html.count("function alphaBeta(") != 1:
        raise RuntimeError("Lab 15 candidate must contain exactly one alpha-beta implementation")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    result = build_candidate(output)
    print(
        "Built Lab 15 R4 English single-file candidate: "
        f"{result} ({result.stat().st_size} bytes)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
