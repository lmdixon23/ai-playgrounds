#!/usr/bin/env python3
from __future__ import annotations

"""Final validation wrapper for the v1.7.1 modern-lab parity candidate.

The first parity candidate correctly composed the learner-facing shell, but its
static guard counted every textual occurrence of `data-quick-assign-id`,
including JavaScript selector strings. This wrapper keeps that candidate frozen,
replaces only the surface-count validator with a start-tag count, enforces the
same established portfolio/ORCID provenance used by the original twelve, and
aligns theme persistence/header placement with the mature suite shell.
"""

import re

import build_site_v1_7_1_modern_parity as candidate

SITE = candidate.SITE
MODERN = candidate.MODERN
ESTABLISHED_PORTFOLIO = "https://lmdixon23.github.io/"
ESTABLISHED_ORCID = "https://orcid.org/0009-0001-0592-462X"


def quick_assign_surface_count(page: str) -> int:
    return len(re.findall(r'<[^>]+\bdata-quick-assign-id\s*=', page, flags=re.I))


def validate() -> None:
    for slug in MODERN:
        page = (SITE / "playgrounds" / slug / "index.html").read_text(encoding="utf-8")
        required = (
            'class="ap-modern-skip"',
            'class="ap-standard-header page-header"',
            'id="ap-modern-share"',
            'id="ap-modern-embed"',
            'class="ap-modern-tldr"',
            'id="ap-modern-key-terms"',
            'id="ap-modern-a11y"',
            'id="ap-modern-fidelity"',
            'class="ap-standard-footer ap-modern-rich-footer"',
            'id="v171-modern-parity-runtime"',
        )
        missing = [marker for marker in required if marker not in page]
        if missing:
            raise RuntimeError(f"Modern parity contract incomplete for {slug}: {missing}")
        count = quick_assign_surface_count(page)
        if count != 1:
            raise RuntimeError(f"Expected one Quick Assign element for {slug}, found {count}")
        if "ai-playgrounds-theme" in page:
            raise RuntimeError(f"Modern lab still uses a separate theme preference key: {slug}")
        prefs_start = page.find('<div class="header-prefs">')
        prefs_end = page.find('</div>', prefs_start)
        theme_pos = page.find('id="ap-standard-theme"')
        if not (prefs_start >= 0 and prefs_start < theme_pos < prefs_end):
            raise RuntimeError(f"Theme control is not in the shared header preference row: {slug}")
    candidate.predecessor.quick.base.base.impl.base.validate_local_references()


def normalize_shell_and_provenance() -> None:
    for slug in MODERN:
        path = SITE / "playgrounds" / slug / "index.html"
        page = path.read_text(encoding="utf-8")

        # Preserve the exact identity/provenance already used by the original 12.
        page = page.replace("https://logandixon.me", ESTABLISHED_PORTFOLIO)
        page = page.replace("https://orcid.org/0009-0008-1712-6630", ESTABLISHED_ORCID)

        # The original twelve share `theme`; the v1.6.x modern shell accidentally
        # introduced a second preference namespace. Rejoin the existing contract.
        page = page.replace("ai-playgrounds-theme", "theme")

        # Match the established hierarchy: Theme + language are preferences in the
        # utility row; Share / Embed / Reset are actions beside the title.
        theme_match = re.search(r'<button\b[^>]*\bid="ap-standard-theme"[^>]*>.*?</button>', page, flags=re.S | re.I)
        if not theme_match:
            raise RuntimeError(f"Modern theme control missing before hierarchy normalization: {slug}")
        theme_button = theme_match.group(0)
        page = page[:theme_match.start()] + page[theme_match.end():]
        prefs_marker = '<div class="header-prefs">'
        if prefs_marker not in page:
            raise RuntimeError(f"Modern header preference row missing: {slug}")
        page = page.replace(prefs_marker, prefs_marker + theme_button, 1)

        if ESTABLISHED_PORTFOLIO not in page or ESTABLISHED_ORCID not in page:
            raise RuntimeError(f"Established modern-lab provenance missing after normalization: {slug}")
        if "https://logandixon.me" in page or "0009-0008-1712-6630" in page:
            raise RuntimeError(f"Unapproved alternate provenance survived normalization: {slug}")
        path.write_text(page, encoding="utf-8")


def build_site() -> None:
    # Let the base parity layer compose the feature shell, but suppress its original
    # textual Quick Assign validator until the DOM-aware final validation below.
    candidate.validate = lambda: candidate.predecessor.quick.base.base.impl.base.validate_local_references()
    candidate.build_site()
    normalize_shell_and_provenance()
    validate()
    print("Finalized v1.7.1 modern-lab parity composition with shared theme persistence, header hierarchy, DOM-level Quick Assign validation, and established suite provenance")


if __name__ == "__main__":
    build_site()
