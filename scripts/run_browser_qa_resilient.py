#!/usr/bin/env python3
"""Exact loopback-HTTP browser QA for the AI Playgrounds release surface.

The public deployment contains 21 HTML pages:
  * 1 landing page
  * 7 support/resource pages
  * 1 deployed deterministic test harness
  * 12 applets

The earlier resilient wrapper accidentally excluded tests/index.html while the
canonical deployment builder and canonical browser QA deliberately include it.
This runner uses an explicit release manifest rather than heuristic discovery.
"""

from __future__ import annotations

import argparse
import functools
import http.server
import json
import pathlib
import socketserver
import threading
import time
from datetime import datetime, timezone


EXPECTED_APPLETS = {
    "bayes-classifier",
    "bayes-network",
    "cnf-sat",
    "convolution",
    "hill-climbing",
    "kmeans",
    "knn-classifier",
    "neural-network",
    "overfitting",
    "q-learning-gridworld",
    "search-pathfinding",
    "wumpus-world",
}


TOP_LEVEL_HTML = [
    "index.html",
    "quality.html",
    "teacher-pack.html",
    "curriculum.html",
    "student-lab.html",
    "release-notes.html",
    "research-and-citation.html",
    "404.html",
]


VIEWPORTS = [
    ("desktop", 1440, 900),
    ("tablet", 1024, 768),
    ("mobile", 390, 844),
]


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass


class ReusableThreadingTCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def release_pages(root: pathlib.Path) -> list[pathlib.Path]:
    pages: list[pathlib.Path] = []

    for relative in TOP_LEVEL_HTML:
        path = root / relative
        if not path.is_file():
            raise FileNotFoundError(
                f"Required release page is missing: {relative}"
            )
        pages.append(path)

    test_harness = root / "tests" / "index.html"
    if not test_harness.is_file():
        raise FileNotFoundError(
            "Required deployed test harness is missing: tests/index.html"
        )
    pages.append(test_harness)

    playground_root = root / "playgrounds"

    applet_paths = sorted(
        playground_root.glob("*/index.html")
    )

    applet_names = {
        path.parent.name
        for path in applet_paths
    }

    if applet_names != EXPECTED_APPLETS:
        missing = sorted(
            EXPECTED_APPLETS - applet_names
        )
        unexpected = sorted(
            applet_names - EXPECTED_APPLETS
        )
        raise RuntimeError(
            "Applet manifest mismatch. "
            f"Missing={missing}; unexpected={unexpected}"
        )

    pages.extend(applet_paths)

    if len(pages) != 21:
        raise RuntimeError(
            f"Release HTML manifest must contain 21 pages; found {len(pages)}"
        )

    return pages


def main() -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--root",
        default=".",
    )

    parser.add_argument(
        "--output",
    )

    parser.add_argument(
        "--expected-pages",
        type=int,
        default=21,
    )

    args = parser.parse_args()

    root = pathlib.Path(
        args.root
    ).resolve()

    output = (
        pathlib.Path(args.output)
        if args.output
        else root
        / "release-evidence"
        / "browser-qa-resilient.json"
    )

    summary = {
        "generated_at_utc":
            datetime.now(
                timezone.utc
            ).isoformat(),
        "root": str(root),
        "expected_pages": args.expected_pages,
        "page_count": None,
        "viewports": len(VIEWPORTS),
        "cases": None,
        "passed": None,
        "failed": None,
        "launch_error": None,
        "pages": [],
        "results": [],
        "pass": False,
    }

    try:
        pages = release_pages(root)
    except Exception as exc:
        summary["launch_error"] = (
            f"{type(exc).__name__}: {exc}"
        )

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output.write_text(
            json.dumps(
                summary,
                indent=2,
                ensure_ascii=False,
            ) + "\n",
            encoding="utf-8",
        )

        print(
            json.dumps(
                {
                    key: summary[key]
                    for key in (
                        "page_count",
                        "cases",
                        "passed",
                        "failed",
                        "launch_error",
                    )
                },
                indent=2,
                ensure_ascii=False,
            )
        )

        return 1

    summary["pages"] = [
        page.relative_to(root).as_posix()
        for page in pages
    ]

    summary["page_count"] = len(pages)

    handler = functools.partial(
        QuietHandler,
        directory=str(root),
    )

    server = ReusableThreadingTCPServer(
        ("127.0.0.1", 0),
        handler,
    )

    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True,
    )

    thread.start()

    port = server.server_address[1]

    browser = None

    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                ],
            )

            for path in pages:
                relative = (
                    path.relative_to(root).as_posix()
                )

                url = (
                    f"http://127.0.0.1:{port}/{relative}"
                )

                for viewport_name, width, height in VIEWPORTS:
                    context = browser.new_context(
                        viewport={
                            "width": width,
                            "height": height,
                        },
                        locale="en-US",
                        reduced_motion="reduce",
                    )

                    page = context.new_page()

                    console_errors: list[str] = []
                    page_errors: list[str] = []

                    page.on(
                        "console",
                        lambda message, bucket=console_errors: (
                            bucket.append(message.text)
                            if message.type == "error"
                            else None
                        ),
                    )

                    page.on(
                        "pageerror",
                        lambda error, bucket=page_errors:
                            bucket.append(str(error)),
                    )

                    started = time.perf_counter()

                    status = None
                    navigation_error = None
                    metrics = {}

                    try:
                        response = page.goto(
                            url,
                            wait_until="domcontentloaded",
                            timeout=30_000,
                        )

                        status = (
                            response.status
                            if response is not None
                            else None
                        )

                        if relative == "tests/index.html":
                            page.wait_for_function(
                                """() => {
                                    const node =
                                        document.querySelector('#summary');

                                    return node && (
                                        node.classList.contains('all-pass') ||
                                        node.classList.contains('some-fail')
                                    );
                                }""",
                                timeout=30_000,
                            )
                        else:
                            page.wait_for_timeout(350)

                        metrics = page.evaluate(
                            """() => ({
                                title:
                                    document.title || '',
                                text:
                                    (
                                        document.body?.innerText || ''
                                    ).trim().length,
                                lang:
                                    document.documentElement.lang || '',
                                scrollWidth:
                                    document.documentElement.scrollWidth,
                                clientWidth:
                                    document.documentElement.clientWidth,
                                buttons:
                                    document.querySelectorAll(
                                        'button,[role="button"]'
                                    ).length
                            })"""
                        )

                    except Exception as exc:
                        navigation_error = (
                            f"{type(exc).__name__}: {exc}"
                        )

                    failures: list[str] = []

                    if status != 200:
                        failures.append(
                            "http-status"
                        )

                    if navigation_error:
                        failures.append(
                            "navigation"
                        )

                    if not metrics.get("title"):
                        failures.append(
                            "missing-title"
                        )

                    if metrics.get("text", 0) < 20:
                        failures.append(
                            "empty-body"
                        )

                    if (
                        metrics.get("scrollWidth", 0)
                        >
                        metrics.get("clientWidth", 0) + 2
                    ):
                        failures.append(
                            "horizontal-overflow"
                        )

                    if console_errors:
                        failures.append(
                            "console-error"
                        )

                    if page_errors:
                        failures.append(
                            "page-error"
                        )

                    result = {
                        "page": relative,
                        "viewport": viewport_name,
                        "width": width,
                        "height": height,
                        "url": url,
                        "status": status,
                        "duration_seconds":
                            round(
                                time.perf_counter() - started,
                                3,
                            ),
                        "metrics": metrics,
                        "console_errors": console_errors,
                        "page_errors": page_errors,
                        "error": navigation_error,
                        "failures": failures,
                        "pass": not failures,
                    }

                    summary["results"].append(
                        result
                    )

                    context.close()

            browser.close()
            browser = None

    except Exception as exc:
        summary["launch_error"] = (
            f"{type(exc).__name__}: {exc}"
        )

    finally:
        if browser is not None:
            try:
                browser.close()
            except Exception:
                pass

        server.shutdown()
        server.server_close()

    summary["cases"] = len(
        summary["results"]
    )

    summary["passed"] = sum(
        1
        for result in summary["results"]
        if result["pass"]
    )

    summary["failed"] = sum(
        1
        for result in summary["results"]
        if not result["pass"]
    )

    expected_cases = (
        args.expected_pages *
        len(VIEWPORTS)
    )

    summary["pass"] = (
        summary["launch_error"] is None
        and summary["page_count"] == args.expected_pages
        and summary["cases"] == expected_cases
        and summary["passed"] == expected_cases
        and summary["failed"] == 0
    )

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output.write_text(
        json.dumps(
            summary,
            indent=2,
            ensure_ascii=False,
        ) + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "page_count":
                    summary["page_count"],
                "cases":
                    summary["cases"],
                "passed":
                    summary["passed"],
                "failed":
                    summary["failed"],
                "launch_error":
                    summary["launch_error"],
                "pass":
                    summary["pass"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )

    if not summary["pass"]:
        failures = [
            result
            for result in summary["results"]
            if not result["pass"]
        ]

        if failures:
            print("First failures:")

            for failure in failures[:10]:
                print(
                    json.dumps(
                        failure,
                        indent=2,
                        ensure_ascii=False,
                    )
                )

        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())