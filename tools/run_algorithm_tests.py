#!/usr/bin/env python3
"""Run the browser-based AI Playgrounds algorithm regression suite.

The gate requires:
- exactly 45 registered test cases,
- zero failed cases,
- zero skipped cases,
- zero JavaScript page errors,
- zero console errors.

A JSON report is written under release-evidence/.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[1]
TEST_PAGE = ROOT / "tests" / "index.html"
EVIDENCE_PATH = ROOT / "release-evidence" / "algorithm-tests.json"
DEFAULT_EXPECTED_TOTAL = 45


def git_head() -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            text=True,
        ).strip()
    except Exception:
        return None


def launch_chromium(playwright: Any):
    args = ["--no-sandbox", "--disable-dev-shm-usage"]
    managed = pathlib.Path(playwright.chromium.executable_path)

    if managed.exists():
        return playwright.chromium.launch(headless=True, args=args), str(managed)

    for executable_name in (
        "chromium",
        "chromium-browser",
        "google-chrome",
        "chrome",
        "msedge",
    ):
        candidate = shutil.which(executable_name)
        if candidate:
            return (
                playwright.chromium.launch(
                    headless=True,
                    executable_path=candidate,
                    args=args,
                ),
                candidate,
            )

    return playwright.chromium.launch(headless=True, args=args), str(managed)


def collect_results(page: Any) -> dict[str, Any]:
    return page.evaluate(
        """() => {
            const summary = document.querySelector("#summary");
            const rows = [...document.querySelectorAll("#output .case")];

            const passed = rows.filter(row => row.querySelector(".pass"));
            const failed = rows.filter(row => row.querySelector(".fail"));
            const skipped = rows.filter(row => row.classList.contains("skipped"));

            return {
                summary: summary ? summary.textContent.trim() : "",
                summary_classes: summary ? [...summary.classList] : [],
                total: rows.length,
                passed: passed.length,
                failed: failed.length,
                skipped: skipped.length,
                failures: failed.map(row => row.innerText.trim()),
                skips: skipped.map(row => row.innerText.trim()),
                groups: [...document.querySelectorAll("#output .group")].map(
                    group => ({
                        name: (group.querySelector("h2")?.textContent || "").trim(),
                        total: group.querySelectorAll(".case").length,
                        passed: group.querySelectorAll(".case .pass").length,
                        failed: group.querySelectorAll(".case .fail").length,
                        skipped: group.querySelectorAll(".case.skipped").length,
                    })
                ),
            };
        }"""
    )


def run(expected_total: int, allow_skips: bool) -> dict[str, Any]:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError(
            "Playwright is not installed. Run: python -m pip install playwright"
        ) from exc

    if not TEST_PAGE.is_file():
        raise FileNotFoundError(f"Algorithm test page is missing: {TEST_PAGE}")

    page_errors: list[str] = []
    console_errors: list[str] = []

    with sync_playwright() as playwright:
        browser = None
        browser_path = None
        try:
            browser, browser_path = launch_chromium(playwright)
            context = browser.new_context(
                viewport={"width": 1280, "height": 900},
                locale="en-US",
                reduced_motion="reduce",
            )
            page = context.new_page()
            page.on("pageerror", lambda error: page_errors.append(str(error)))
            page.on(
                "console",
                lambda message: (
                    console_errors.append(message.text)
                    if message.type == "error"
                    else None
                ),
            )

            page.goto(
                TEST_PAGE.resolve().as_uri(),
                wait_until="load",
                timeout=15_000,
            )

            page.wait_for_function(
                """() => {
                    const summary = document.querySelector("#summary");
                    return summary && (
                        summary.classList.contains("all-pass") ||
                        summary.classList.contains("some-fail")
                    );
                }""",
                timeout=15_000,
            )

            results = collect_results(page)
        finally:
            if browser is not None:
                browser.close()

    passed_gate = (
        results["total"] == expected_total
        and results["passed"] + results["skipped"] == expected_total
        and results["failed"] == 0
        and (allow_skips or results["skipped"] == 0)
        and "all-pass" in results["summary_classes"]
        and not page_errors
        and not console_errors
    )

    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "git_head": git_head(),
        "test_page": str(TEST_PAGE.relative_to(ROOT)),
        "browser": browser_path,
        "expected_total": expected_total,
        "allow_skips": allow_skips,
        "page_errors": page_errors,
        "console_errors": console_errors,
        "results": results,
        "pass": passed_gate,
    }


def print_report(report: dict[str, Any]) -> None:
    results = report["results"]

    print(
        "Algorithm tests: "
        f"{results['passed']} pass, "
        f"{results['failed']} fail, "
        f"{results['skipped']} skip, "
        f"{results['total']} total"
    )
    print(f"Expected total: {report['expected_total']}")
    print(f"Summary: {results['summary']}")

    for group in results["groups"]:
        print(
            "  "
            f"{group['name']}: "
            f"{group['passed']} pass, "
            f"{group['failed']} fail, "
            f"{group['skipped']} skip"
        )

    if results["failures"]:
        print("\nFailed tests:")
        for failure in results["failures"]:
            print(f"  - {failure}")

    if results["skips"]:
        print("\nSkipped tests:")
        for skipped in results["skips"]:
            print(f"  - {skipped}")

    if report["page_errors"]:
        print("\nJavaScript page errors:")
        for error in report["page_errors"]:
            print(f"  - {error}")

    if report["console_errors"]:
        print("\nConsole errors:")
        for error in report["console_errors"]:
            print(f"  - {error}")

    print(
        "\nVERDICT: "
        + (
            "ALGORITHM TESTS PASSED"
            if report["pass"]
            else "ALGORITHM TESTS FAILED"
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--expected-total",
        type=int,
        default=DEFAULT_EXPECTED_TOTAL,
    )
    parser.add_argument(
        "--allow-skips",
        action="store_true",
        help="Do not fail solely because a test is skipped.",
    )
    parser.add_argument(
        "--json",
        type=pathlib.Path,
        default=EVIDENCE_PATH,
    )
    args = parser.parse_args()

    try:
        report = run(
            expected_total=args.expected_total,
            allow_skips=args.allow_skips,
        )
    except Exception as exc:
        report = {
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "git_head": git_head(),
            "expected_total": args.expected_total,
            "allow_skips": args.allow_skips,
            "error": f"{type(exc).__name__}: {exc}",
            "pass": False,
        }
        print(
            f"Algorithm test runner error: {report['error']}",
            file=sys.stderr,
        )

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    if "results" in report:
        print_report(report)

    try:
        evidence_display = args.json.resolve().relative_to(ROOT.resolve())
    except ValueError:
        evidence_display = args.json

    print(f"Evidence: {evidence_display}")
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
