#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CURRENT_DOCS = (
    "README.md",
    "QUALITY.md",
    "ARCHITECTURE.md",
    "docs/LAUNCH_KIT.md",
    "docs/SHOW_HN_READINESS.md",
    "docs/CONTRIBUTOR_ONRAMP.md",
    "docs/PUBLIC_SURFACE_LOCALE_MATRIX.md",
    "docs/QUICK_ASSIGN_ARCHITECTURE.md",
)

FORBIDDEN_CURRENT_PHRASES = (
    "twelve bilingual",
    "fourteen multilingual, offline-ready applets",
    "metadata for the twelve applets",
    "status: v1.6.1 candidate",
    "first four active canaries are required",
    "remaining eleven ids are reserved",
)

QUICK_ASSIGN_IDS = (
    "QA-SEARCH-01",
    "QA-LOCAL-01",
    "QA-WUMPUS-01",
    "QA-SAT-01",
    "QA-BAYES-01",
    "QA-BN-01",
    "QA-KNN-01",
    "QA-OVERFIT-01",
    "QA-NN-01",
    "QA-KMEANS-01",
    "QA-CNN-01",
    "QA-QL-01",
    "QA-MINIMAX-01",
    "QA-TRANSFORMER-01",
    "QA-AGENT-01",
)


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().replace("–", "-").replace("—", "-")).strip()


def require_all(rel: str, text: str, groups: list[tuple[str, ...]], failures: list[str]) -> None:
    low = normalized(text)
    for group in groups:
        missing = [token for token in group if token.lower() not in low]
        if missing:
            failures.append(f"{rel}: missing semantic markers {missing} from group {group}")


def main() -> int:
    failures: list[str] = []
    docs: dict[str, str] = {}

    for rel in CURRENT_DOCS:
        path = ROOT / rel
        if not path.is_file():
            failures.append(f"missing current doc: {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        docs[rel] = text
        low = normalized(text)
        for phrase in FORBIDDEN_CURRENT_PHRASES:
            if phrase in low:
                failures.append(f"{rel}: stale current-facing phrase remains: {phrase}")

    # Current product identity: verify facts, not one frozen marketing sentence.
    if "README.md" in docs:
        require_all(
            "README.md", docs["README.md"],
            [
                ("15", "multilingual", "offline-ready", "applets"),
                ("13 foundations", "2 modern ai extensions"),
                ("quick assign", "qa-transformer-01", "qa-agent-01"),
                ("english", "simplified chinese", "vietnamese", "spanish"),
                ("v1.7.0",),
            ], failures,
        )

    if "QUALITY.md" in docs:
        require_all(
            "QUALITY.md", docs["QUALITY.md"],
            [
                ("fifteen", "multilingual", "learner applets"),
                ("thirteen foundations/course-track labs", "two modern ai extensions"),
                ("all fifteen", "quick assign"),
                ("english", "simplified chinese", "vietnamese", "spanish"),
                ("evidence limits", "learning gains", "accessibility conformance"),
            ], failures,
        )

    if "ARCHITECTURE.md" in docs:
        require_all(
            "ARCHITECTURE.md", docs["ARCHITECTURE.md"],
            [
                ("metadata for all fifteen applets",),
                ("13 foundations/course-track labs", "2 modern ai extensions"),
                ("original twelve", "labs 13-15", "concept-specific bodies"),
                ("all fifteen", "learner applets", "level-1 quick assign"),
                ("english", "simplified chinese", "vietnamese", "spanish"),
                ("applet_design_system_contract.md",),
            ], failures,
        )

    if "docs/LAUNCH_KIT.md" in docs:
        require_all(
            "docs/LAUNCH_KIT.md", docs["docs/LAUNCH_KIT.md"],
            [
                ("15", "multilingual", "interactive ai labs"),
                ("13 foundations/course-track labs", "2 modern ai extensions"),
                ("quick assign", "every applet"),
                ("english", "simplified chinese", "vietnamese", "spanish"),
                ("learning gains", "accessibility conformance"),
            ], failures,
        )

    if "docs/SHOW_HN_READINESS.md" in docs:
        require_all(
            "docs/SHOW_HN_READINESS.md", docs["docs/SHOW_HN_READINESS.md"],
            [
                ("current v1.7.0 product",),
                ("15 learner applets", "13 foundations/course-track labs", "2 modern ai extensions"),
                ("one level-1 quick assign per applet",),
                ("english", "simplified chinese", "vietnamese", "spanish"),
            ], failures,
        )

    if "docs/CONTRIBUTOR_ONRAMP.md" in docs:
        require_all(
            "docs/CONTRIBUTOR_ONRAMP.md", docs["docs/CONTRIBUTOR_ONRAMP.md"],
            [
                ("english", "simplified chinese", "vietnamese", "spanish"),
                ("applet_design_system_contract.md",),
                ("every public applet", "level-1 quick assign"),
                ("public_surface_locale_matrix.md",),
            ], failures,
        )

    locale_rel = "docs/PUBLIC_SURFACE_LOCALE_MATRIX.md"
    if locale_rel in docs:
        low = normalized(docs[locale_rel])
        require_all(
            locale_rel, docs[locale_rel],
            [
                ("current v1.7.0 claim-scoping control",),
                ("all 15 level-1 quick assigns",),
                ("landing page", "yes | yes | yes | yes"),
                ("teacher pack", "yes | yes | no | no"),
                ("curriculum map", "yes | yes | no | no"),
                ("nn-1 activity pack", "yes | no | no | no"),
                ("cnn-1 activity pack", "yes | no | no | no"),
            ], failures,
        )
        if "fully four-language website" not in low:
            failures.append(f"{locale_rel}: missing explicit overclaim warning")

    qa_rel = "docs/QUICK_ASSIGN_ARCHITECTURE.md"
    if qa_rel in docs:
        require_all(
            qa_rel, docs[qa_rel],
            [
                ("active v1.7.0 contract",),
                ("all fifteen public applets", "active v1.7.0 quick assign"),
                ("predict -> manipulate/run -> observe -> explain -> transfer",),
                ("english", "simplified chinese", "vietnamese", "spanish"),
            ], failures,
        )
        for activity_id in QUICK_ASSIGN_IDS:
            if activity_id not in docs[qa_rel]:
                failures.append(f"{qa_rel}: missing active Quick Assign ID {activity_id}")

    scorecard_path = ROOT / "docs/SCORECARD.md"
    if not scorecard_path.is_file():
        failures.append("missing historical scorecard: docs/SCORECARD.md")
    else:
        score = normalized(scorecard_path.read_text(encoding="utf-8"))
        if "historical snapshot" not in score or "not the current v1.7.0 product inventory" not in score:
            failures.append("docs/SCORECARD.md: launch-era numbers are not explicitly marked historical")

    if failures:
        print("CURRENT DOC CONSISTENCY: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        "CURRENT DOC CONSISTENCY: PASS "
        f"({len(CURRENT_DOCS)} current docs, {len(QUICK_ASSIGN_IDS)} active Quick Assign IDs, historical scorecard boundary)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
