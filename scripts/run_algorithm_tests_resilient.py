#!/usr/bin/env python3
"""Run the AI Playgrounds deterministic algorithm harness over loopback HTTP.

This runner reads the rendered test DOM directly. It does not infer counts from
human-readable summary prose, so an all-pass summary such as
"All 45 tests pass." is handled without requiring a literal "0 fail" token.
"""

from __future__ import annotations

import argparse
import functools
import http.server
import json
import pathlib
import socketserver
import threading
from datetime import datetime, timezone


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass


class ReusableThreadingTCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--output")
    parser.add_argument("--expected-pass", type=int, default=45)
    args = parser.parse_args()

    root = pathlib.Path(args.root).resolve()
    harness = root / "tests" / "index.html"

    output = (
        pathlib.Path(args.output)
        if args.output
        else root / "release-evidence" / "algorithm-tests-resilient.json"
    )

    summary = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "root": str(root),
        "harness": "tests/index.html",
        "expected_pass": args.expected_pass,
        "total": None,
        "passed": None,
        "failed": None,
        "skipped": None,
        "summary_text": None,
        "summary_classes": [],
        "groups": [],
        "failures": [],
        "skips": [],
        "console_errors": [],
        "page_errors": [],
        "browser": "playwright-chromium",
        "error": None,
        "pass": False,
    }

    if not harness.is_file():
        summary["error"] = f"Algorithm test harness missing: {harness}"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return 1

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

            context = browser.new_context(
                viewport={
                    "width": 1280,
                    "height": 900,
                },
                locale="en-US",
                reduced_motion="reduce",
            )

            page = context.new_page()

            page.on(
                "console",
                lambda message: (
                    summary["console_errors"].append(
                        message.text
                    )
                    if message.type == "error"
                    else None
                ),
            )

            page.on(
                "pageerror",
                lambda error: summary["page_errors"].append(
                    str(error)
                ),
            )

            response = page.goto(
                f"http://127.0.0.1:{port}/tests/index.html",
                wait_until="load",
                timeout=30_000,
            )

            if response is None:
                raise RuntimeError(
                    "Algorithm harness navigation returned no HTTP response"
                )

            if response.status != 200:
                raise RuntimeError(
                    f"Algorithm harness returned HTTP {response.status}"
                )

            page.wait_for_function(
                """() => {
                    const summary = document.querySelector('#summary');
                    return summary && (
                        summary.classList.contains('all-pass') ||
                        summary.classList.contains('some-fail')
                    );
                }""",
                timeout=30_000,
            )

            results = page.evaluate(
                """() => {
                    const summaryNode =
                        document.querySelector('#summary');

                    const rows = [
                        ...document.querySelectorAll('#output .case')
                    ];

                    const passed = rows.filter(
                        row => row.querySelector('.pass')
                    );

                    const failed = rows.filter(
                        row => row.querySelector('.fail')
                    );

                    const skipped = rows.filter(
                        row => row.classList.contains('skipped')
                    );

                    const groups = [
                        ...document.querySelectorAll('#output .group')
                    ].map(group => ({
                        name:
                            (
                                group.querySelector('h2')?.textContent ||
                                ''
                            ).trim(),
                        total:
                            group.querySelectorAll('.case').length,
                        passed:
                            group.querySelectorAll('.case .pass').length,
                        failed:
                            group.querySelectorAll('.case .fail').length,
                        skipped:
                            group.querySelectorAll('.case.skipped').length,
                    }));

                    return {
                        summary_text:
                            summaryNode
                                ? summaryNode.textContent.trim()
                                : '',
                        summary_classes:
                            summaryNode
                                ? [...summaryNode.classList]
                                : [],
                        total: rows.length,
                        passed: passed.length,
                        failed: failed.length,
                        skipped: skipped.length,
                        failures:
                            failed.map(
                                row => row.innerText.trim()
                            ),
                        skips:
                            skipped.map(
                                row => row.innerText.trim()
                            ),
                        groups,
                    };
                }"""
            )

            summary.update(results)

            context.close()

    except Exception as exc:
        summary["error"] = (
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

    summary["pass"] = (
        summary["error"] is None
        and summary["total"] == args.expected_pass
        and summary["passed"] == args.expected_pass
        and summary["failed"] == 0
        and summary["skipped"] == 0
        and "all-pass" in summary["summary_classes"]
        and not summary["console_errors"]
        and not summary["page_errors"]
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

    display = {
        "harness": summary["harness"],
        "summary_text": summary["summary_text"],
        "total": summary["total"],
        "passed": summary["passed"],
        "failed": summary["failed"],
        "skipped": summary["skipped"],
        "console_errors": len(
            summary["console_errors"]
        ),
        "page_errors": len(
            summary["page_errors"]
        ),
        "error": summary["error"],
        "pass": summary["pass"],
    }

    print(
        json.dumps(
            display,
            indent=2,
            ensure_ascii=False,
        )
    )

    return 0 if summary["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())