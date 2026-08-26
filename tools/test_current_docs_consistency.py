#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CURRENT_DOCS = {
    "README.md": [
        "15 multilingual applets",
        "13 Foundations",
        "2 Modern AI extensions",
        "Quick Assign",
    ],
    "QUALITY.md": [
        "Fifteen multilingual",
        "Thirteen Foundations/course-track labs plus two Modern AI extensions",
        "All fifteen public applets have one stable Quick Assign ID",
        "English, Simplified Chinese, Vietnamese, and Spanish",
    ],
    "ARCHITECTURE.md": [
        "metadata for all fifteen applets",
        "13 Foundations/course-track labs",
        "2 Modern AI extensions",
        "All fifteen learner applets",
        "one stable Level-1 Quick Assign",
    ],
    "docs/LAUNCH_KIT.md": [
        "15 multilingual",
        "13 Foundations/course-track labs plus 2 Modern AI extensions",
        "one stable 10–15 minute Level-1 Quick Assign for every applet",
    ],
    "docs/SHOW_HN_READINESS.md": [
        "current v1.7.0 product",
        "15 learner applets",
        "one Level-1 Quick Assign per applet",
    ],
    "docs/CONTRIBUTOR_ONRAMP.md": [
        "English, Simplified Chinese, Vietnamese, and Spanish",
        "APPLET_DESIGN_SYSTEM_CONTRACT.md",
        "Every public applet has one stable Level-1 Quick Assign",
    ],
    "docs/PUBLIC_SURFACE_LOCALE_MATRIX.md": [
        "current v1.7.0 claim-scoping control",
        "All 15 Level-1 Quick Assigns",
        "Landing page | yes | yes | yes | yes",
    ],
    "docs/QUICK_ASSIGN_ARCHITECTURE.md": [
        "active v1.7.0 contract",
        "All fifteen public applets have one active v1.7.0 Quick Assign",
        "QA-TRANSFORMER-01",
        "QA-AGENT-01",
    ],
}

FORBIDDEN_CURRENT_PHRASES = (
    "twelve bilingual",
    "Twelve bilingual",
    "Fourteen multilingual, offline-ready applets",
    "metadata for the twelve applets",
    "Status: v1.6.1 candidate",
    "first four active canaries are required",
    "remaining eleven IDs are reserved",
)


def main() -> int:
    failures: list[str] = []

    for rel, required in CURRENT_DOCS.items():
        path = ROOT / rel
        if not path.is_file():
            failures.append(f"missing current doc: {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in required:
            if marker not in text:
                failures.append(f"{rel}: missing current marker: {marker}")
        lowered = text.lower()
        for phrase in FORBIDDEN_CURRENT_PHRASES:
            if phrase.lower() in lowered:
                failures.append(f"{rel}: stale current-facing phrase remains: {phrase}")

    scorecard = (ROOT / "docs/SCORECARD.md").read_text(encoding="utf-8")
    if "Historical snapshot" not in scorecard or "not the current v1.7.0 product inventory" not in scorecard:
        failures.append("docs/SCORECARD.md: launch-era numbers are not explicitly marked historical")

    locale = (ROOT / "docs/PUBLIC_SURFACE_LOCALE_MATRIX.md").read_text(encoding="utf-8")
    for marker in (
        "Teacher Pack | yes | yes | no | no",
        "Curriculum Map | yes | yes | no | no",
        "NN-1 Activity Pack | yes | no | no | no",
        "CNN-1 Activity Pack | yes | no | no | no",
    ):
        if marker not in locale:
            failures.append(f"docs/PUBLIC_SURFACE_LOCALE_MATRIX.md: missing bounded-support marker: {marker}")

    if failures:
        print("CURRENT DOC CONSISTENCY: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"CURRENT DOC CONSISTENCY: PASS ({len(CURRENT_DOCS)} current docs + historical scorecard boundary)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
