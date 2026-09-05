#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import subprocess
import sys
import threading
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = ROOT / '_site'
OUT = ROOT / 'release-evidence' / 'v1.9-baseline'
BASELINE_SHA = 'd1c72e10e6c5bf64b9a4bbed578b2305d1c988d0'
ALLOWED_DIFF = {
    '.github/workflows/verify.yml',
    'tools/capture_v1_9_baseline.py',
}
VIEWPORTS = {
    'desktop_1366': {'width': 1366, 'height': 900, 'is_mobile': False},
    'phone_390': {'width': 390, 'height': 844, 'is_mobile': True},
}
THEMES = ('light', 'dark')
EXPECTED_SLUGS = {
    'search-pathfinding',
    'hill-climbing',
    'wumpus-world',
    'cnf-sat',
    'bayes-classifier',
    'bayes-network',
    'knn-classifier',
    'overfitting',
    'neural-network',
    'kmeans',
    'convolution',
    'q-learning-gridworld',
    'transformer-language-model',
    'agent-tool-context',
    'minimax-alpha-beta',
}


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        return


def run(command: list[str], timeout: int = 240) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=timeout,
    )


def sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def ensure_baseline_commit() -> None:
    probe = run(['git', 'cat-file', '-e', f'{BASELINE_SHA}^{{commit}}'], timeout=20)
    if probe.returncode == 0:
        return
    fetched = run(['git', 'fetch', '--no-tags', '--depth=1', 'origin', BASELINE_SHA], timeout=90)
    if fetched.returncode:
        raise RuntimeError(
            fetched.stderr.strip()
            or fetched.stdout.strip()
            or f'Could not fetch exact baseline commit {BASELINE_SHA}'
        )
    probe = run(['git', 'cat-file', '-e', f'{BASELINE_SHA}^{{commit}}'], timeout=20)
    if probe.returncode:
        raise RuntimeError(f'Exact baseline commit remains unavailable after fetch: {BASELINE_SHA}')


def assert_evidence_only_diff() -> list[str]:
    ensure_baseline_commit()
    diff = run(['git', 'diff', '--name-only', f'{BASELINE_SHA}..HEAD'], timeout=30)
    if diff.returncode:
        raise RuntimeError(diff.stderr.strip() or diff.stdout.strip() or 'git diff failed')
    changed = sorted(line.strip() for line in diff.stdout.splitlines() if line.strip())
    unexpected = sorted(set(changed) - ALLOWED_DIFF)
    if unexpected:
        raise RuntimeError(f'Baseline capture branch changes product inputs: {unexpected}')
    return changed


def build_site() -> dict[str, str]:
    built = run([sys.executable, 'tools/build_site_v1_8_1.py'], timeout=240)
    if built.returncode:
        raise RuntimeError(built.stderr[-12000:] or built.stdout[-12000:] or 'v1.8.1 build failed')
    files = sorted(path for path in SITE.rglob('*') if path.is_file())
    applets = sorted((SITE / 'playgrounds').glob('*/index.html'))
    slugs = {path.parent.name for path in applets}
    if len(files) != 58 or len(applets) != 15 or slugs != EXPECTED_SLUGS:
        raise RuntimeError(
            f'Baseline boundary mismatch: files={len(files)}, applets={len(applets)}, '
            f'missing={sorted(EXPECTED_SLUGS - slugs)}, extra={sorted(slugs - EXPECTED_SLUGS)}'
        )
    return {str(path.relative_to(SITE)): sha256(path) for path in files}


def capture() -> dict:
    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:
        raise RuntimeError(f'Playwright unavailable: {exc}') from exc

    handler = lambda *args, **kwargs: QuietHandler(*args, directory=str(SITE), **kwargs)
    server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    port = server.server_address[1]

    records: list[dict] = []
    failures: list[dict] = []
    screenshots = OUT / 'screenshots'
    screenshots.mkdir(parents=True, exist_ok=True)

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True, args=['--no-sandbox', '--disable-dev-shm-usage'])
            try:
                for viewport_name, viewport in VIEWPORTS.items():
                    for theme in THEMES:
                        for slug in sorted(EXPECTED_SLUGS):
                            context = browser.new_context(
                                viewport={'width': viewport['width'], 'height': viewport['height']},
                                is_mobile=viewport['is_mobile'],
                                device_scale_factor=1,
                                locale='en-US',
                            )
                            context.add_init_script(
                                script=(
                                    "try { localStorage.setItem('theme', "
                                    + json.dumps(theme)
                                    + "); } catch (_) {}"
                                )
                            )
                            page = context.new_page()
                            console_errors: list[str] = []
                            page_errors: list[str] = []
                            page.on('console', lambda message, target=console_errors: target.append(message.text) if message.type == 'error' else None)
                            page.on('pageerror', lambda error, target=page_errors: target.append(str(error)))
                            url = f'http://127.0.0.1:{port}/playgrounds/{slug}/?lang=en&analytics=off'
                            try:
                                page.goto(url, wait_until='domcontentloaded', timeout=15000)
                                page.wait_for_timeout(300)
                                page.add_style_tag(
                                    content='*,*::before,*::after{animation-duration:0s!important;animation-delay:0s!important;transition-duration:0s!important;caret-color:transparent!important}'
                                )
                                page.evaluate('() => window.scrollTo(0, 0)')
                                page.wait_for_timeout(80)

                                version = page.locator('meta[name="ai-playgrounds-version"]').get_attribute('content') or ''
                                body_class = page.locator('body').get_attribute('class') or ''
                                dark_active = 'dark-mode' in body_class.split() or 'ap-standard-dark' in body_class.split()
                                theme_ok = dark_active if theme == 'dark' else not dark_active
                                title = page.title()
                                language = page.locator('html').get_attribute('lang') or ''
                                dimensions = page.evaluate(
                                    '() => ({width:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight})'
                                )

                                shot_dir = screenshots / viewport_name
                                shot_dir.mkdir(parents=True, exist_ok=True)
                                shot = shot_dir / f'{slug}-{theme}.png'
                                page.screenshot(path=str(shot), full_page=False, animations='disabled')

                                record = {
                                    'slug': slug,
                                    'viewport': viewport_name,
                                    'theme': theme,
                                    'url': url,
                                    'title': title,
                                    'lang': language,
                                    'version': version,
                                    'body_class': body_class,
                                    'theme_ok': theme_ok,
                                    'document_dimensions': dimensions,
                                    'console_errors': console_errors,
                                    'page_errors': page_errors,
                                    'screenshot': str(shot.relative_to(ROOT)),
                                    'screenshot_sha256': sha256(shot),
                                    'pass': version == '1.8.1' and bool(title.strip()) and theme_ok and not console_errors and not page_errors,
                                }
                                records.append(record)
                                if not record['pass']:
                                    failures.append(record)
                            except Exception as exc:
                                record = {
                                    'slug': slug,
                                    'viewport': viewport_name,
                                    'theme': theme,
                                    'url': url,
                                    'console_errors': console_errors,
                                    'page_errors': page_errors + [f'{type(exc).__name__}: {exc}'],
                                    'pass': False,
                                }
                                records.append(record)
                                failures.append(record)
                            finally:
                                context.close()
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

    expected = len(EXPECTED_SLUGS) * len(VIEWPORTS) * len(THEMES)
    if len(records) != expected:
        raise RuntimeError(f'Expected {expected} captures, got {len(records)}')
    return {
        'expected_captures': expected,
        'captures': len(records),
        'failed': len(failures),
        'pass': not failures,
        'records': records,
        'failures': failures,
    }


def write_report(payload: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'baseline.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    hashes = payload['artifact_sha256']
    (OUT / 'final-artifact-sha256.json').write_text(json.dumps(hashes, indent=2, sort_keys=True) + '\n', encoding='utf-8')

    lines = [
        '# v1.9 baseline capture evidence',
        '',
        f'- Baseline source SHA: `{payload["baseline_source_sha"]}`',
        f'- Evidence HEAD: `{payload["evidence_head"]}`',
        f'- GitHub head SHA: `{payload.get("github_head_sha") or "not-set"}`',
        f'- Generated files: `{len(hashes)}`',
        f'- Captures: `{payload["browser"]["captures"]}`',
        f'- Capture failures: `{payload["browser"]["failed"]}`',
        f'- Overall: `{"PASS" if payload["pass"] else "FAIL"}`',
        '',
        '## Matrix',
        '',
        '- 15 generated applets',
        '- desktop 1366×900',
        '- phone 390×844',
        '- light theme',
        '- dark theme',
        '- English initial state',
        '',
        '## Evidence boundary',
        '',
        'These captures are diagnostic pre-refactor evidence. They are not permanent visual-regression goldens and do not establish accessibility conformance or human usability.',
    ]
    if payload['browser']['failures']:
        lines.extend(['', '## Failures', ''])
        for failure in payload['browser']['failures']:
            lines.append(
                f'- `{failure.get("slug")}` / `{failure.get("viewport")}` / `{failure.get("theme")}`: '
                + '; '.join(failure.get('page_errors', []) + failure.get('console_errors', []))
            )
    (OUT / 'REPORT.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    changed = assert_evidence_only_diff()
    hashes = build_site()
    browser = capture()
    evidence_head = run(['git', 'rev-parse', 'HEAD'], timeout=20).stdout.strip()
    payload = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'baseline_source_sha': BASELINE_SHA,
        'evidence_head': evidence_head,
        'github_head_sha': os.environ.get('GITHUB_HEAD_SHA'),
        'allowed_branch_diff': changed,
        'artifact_sha256': hashes,
        'browser': browser,
        'pass': len(hashes) == 58 and browser['pass'],
    }
    write_report(payload)
    print(json.dumps({
        'baseline_source_sha': BASELINE_SHA,
        'generated_files': len(hashes),
        'captures': browser['captures'],
        'capture_failures': browser['failed'],
        'pass': payload['pass'],
        'evidence': str(OUT.relative_to(ROOT)),
    }, indent=2))
    return 0 if payload['pass'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
