#!/usr/bin/env python3
"""Fail-closed pedagogical contract checks for AI Playgrounds v1.1 development."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "release-evidence" / "pedagogical-contracts.json"

APPLETS = {
    "knn": ROOT / "playgrounds/knn-classifier/index.html",
    "search": ROOT / "playgrounds/search-pathfinding/index.html",
    "hill": ROOT / "playgrounds/hill-climbing/index.html",
    "wumpus": ROOT / "playgrounds/wumpus-world/index.html",
    "sat": ROOT / "playgrounds/cnf-sat/index.html",
    "bayes": ROOT / "playgrounds/bayes-classifier/index.html",
    "bayes_network": ROOT / "playgrounds/bayes-network/index.html",
    "overfitting": ROOT / "playgrounds/overfitting/index.html",
    "neural": ROOT / "playgrounds/neural-network/index.html",
    "kmeans": ROOT / "playgrounds/kmeans/index.html",
    "convolution": ROOT / "playgrounds/convolution/index.html",
    "q_learning": ROOT / "playgrounds/q-learning-gridworld/index.html",
}

REQUIRED = {
    "knn": [
        "Guided challenge: predict before reveal",
        "Closeness rule:",
        "Voting rule:",
        "metric ball with the classifier's full decision boundary",
        "const guided = {",
        "guidedLock",
        "guidedReveal",
        "not a universally correct k",
    ],
    "search": [
        "fixed grid and neighbor order",
        "One trace is not a general runtime ranking",
        "number of edges from the start",
    ],
    "hill": [
        "best-improvement",
        "any finite run can still miss the global optimum",
        "Naming note:",
    ],
    "wumpus": [
        "AIMA-inspired hybrid",
        "Whether expected value is higher depends",
        "independent per-cell pit prior",
        "hidden ground truth versus what this simplified inference system has derived",
    ],
    "sat": [
        "Conflicting XOR constraints create a contradiction",
        "logically equivalent",
        "equisatisfiable",
        "separate DPLL pruning trace",
    ],
    "bayes": [
        "99 percent sensitivity and 99 percent specificity",
        "conditional-independence assumption",
        "repeated tests can share systematic errors",
    ],
    "bayes_network": [
        "Two reports are conditionally independent given the alarm",
        "active-trail, Bayes-ball-style rules directly on the DAG",
        "relative to a conditioning set",
    ],
    "overfitting": [
        "Validation MSE (repeatedly viewed)",
        "functions as validation data, not as an untouched final test set",
        "finite samples and model mismatch can still produce poor generalization",
    ],
    "neural": [
        "one affine map",
        "original x-y features",
        "optimization still has to find suitable parameters",
    ],
    "kmeans": [
        "not proof of a uniquely true k",
        "three generating groups",
        "a centroid is only a point",
    ],
    "convolution": [
        "mathematically it is cross-correlation",
        "numerically largest activation",
        "larger theoretical receptive field",
        "One feature-map response",
    ],
    "q_learning": [
        "Step costs and discounting both create time preference",
        "gamma=0.9 with gamma=1",
        "later terminal reward is still discounted",
        "max=\"1\" min=\"0\" step=\"0.01\" type=\"range\" value=\"0.9\"",
    ],
}

FORBIDDEN = {
    "knn": [
        "sharp diamond boundaries",
        "Straight, axis-aligned segments: Manhattan's diamond contours",
        "highest CV accuracy is the right pick",
        "CV 准确率最高的 k 才是正确选择",
    ],
    "search": [
        "Which search will reach a goal first",
        "fast but inefficient route",
    ],
    "hill": [
        "Eventually finds the global optimum",
        "Use the traveling salesperson problem (TSP) with steepest-ascent",
        "Steepest-ascent:",
    ],
    "wumpus": [
        "Sutton-style risk-taking",
        "higher expected value",
        "low expected value",
        "what the agent SHOULD know",
    ],
    "sat": [
        "Exclusive OR creates a contradiction",
        "Load the exclusive-OR (XOR) contradiction",
    ],
    "bayes": [
        "99 percent accurate test",
        "This is why doctors retest",
        "这正是医生复检的原因",
    ],
    "bayes_network": [
        "Two independent reports strengthen the evidence",
        "on the moralized DAG",
    ],
    "overfitting": [
        "σ=0 makes overfitting impossible",
        "overfitting can't happen",
        "Test MSE (held out)",
        "More data also fixes it",
    ],
    "neural": [
        "collapse to one linear map",
        "composition of linear maps is linear",
        "Provably unsolvable by any linear model since Minsky 1969",
    ],
    "kmeans": [
        "highest mean silhouette",
        "peaks at the true number of clusters",
        "The highest score wins",
        "Gaussian-shaped centroid",
        "silhouette CAN identify the right k",
    ],
    "convolution": [
        "What the CNN \"sees.\"",
        "keeps only its strongest activation",
        "detect a pattern larger than either filter alone",
    ],
    "q_learning": [
        "every path has the same return",
        "no time pressure",
        "removes time pressure",
    ],
}


class IdParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []

    def handle_starttag(self, tag: str, attrs):
        for key, value in attrs:
            if key == "id" and value:
                self.ids.append(value)


def main() -> int:
    checks: list[dict] = []
    failures: list[str] = []

    for slug, path in APPLETS.items():
        if not path.is_file():
            failures.append(f"missing applet: {path}")
            continue
        text = path.read_text(encoding="utf-8-sig")

        for phrase in REQUIRED.get(slug, []):
            ok = phrase in text
            checks.append({"applet": slug, "kind": "required", "phrase": phrase, "pass": ok})
            if not ok:
                failures.append(f"{slug}: missing required phrase: {phrase}")

        for phrase in FORBIDDEN.get(slug, []):
            ok = phrase not in text
            checks.append({"applet": slug, "kind": "forbidden", "phrase": phrase, "pass": ok})
            if not ok:
                failures.append(f"{slug}: forbidden phrase remains: {phrase}")

        shared_contracts = ["Predict first", "Explain afterward", "Misconceptions to test"]
        if slug != "overfitting":
            shared_contracts.append("What this model leaves out")
        for shared in shared_contracts:
            ok = shared in text
            checks.append({"applet": slug, "kind": "shared-learning-contract", "phrase": shared, "pass": ok})
            if not ok:
                failures.append(f"{slug}: shared learning contract missing: {shared}")

        parser = IdParser()
        parser.feed(text)
        dupes = sorted([item for item, count in Counter(parser.ids).items() if count > 1])
        ok = not dupes
        checks.append({"applet": slug, "kind": "unique-html-ids", "pass": ok, "duplicates": dupes})
        if dupes:
            failures.append(f"{slug}: duplicate HTML ids: {dupes}")

    workflow = ROOT / ".github/workflows/verify.yml"
    workflow_ok = workflow.is_file() and "python tools/verify_pedagogical_contracts.py" in workflow.read_text(encoding="utf-8-sig")
    checks.append({"kind": "workflow-gate", "pass": workflow_ok})
    if not workflow_ok:
        failures.append("verify workflow does not run pedagogical contract checks")

    docs = [ROOT / "docs/PEDAGOGICAL_RED_TEAM_V1_1.md", ROOT / "docs/GUIDED_CHALLENGE_ARCHITECTURE.md"]
    for doc in docs:
        ok = doc.is_file() and doc.stat().st_size > 500
        checks.append({"kind": "documentation", "path": str(doc.relative_to(ROOT)), "pass": ok})
        if not ok:
            failures.append(f"missing or undersized documentation: {doc}")

    payload = {
        "harness": "tools/verify_pedagogical_contracts.py",
        "applet_count": len(APPLETS),
        "checks": len(checks),
        "passed": sum(1 for c in checks if c.get("pass")),
        "failed": sum(1 for c in checks if not c.get("pass")),
        "failures": failures,
        "pass": not failures,
        "details": checks,
    }
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: payload[k] for k in ("harness", "applet_count", "checks", "passed", "failed", "pass")}, indent=2))
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
