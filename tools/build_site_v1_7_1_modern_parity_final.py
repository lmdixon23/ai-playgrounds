#!/usr/bin/env python3
from __future__ import annotations

"""Final validation wrapper for the v1.7.1 modern-lab parity candidate.

The first parity candidate correctly composed the learner-facing shell, but its
static guard counted every textual occurrence of `data-quick-assign-id`,
including JavaScript selector strings. This wrapper keeps that candidate frozen,
replaces only the surface-count validator with a start-tag count, and enforces
the same established portfolio/ORCID provenance used by the original twelve.
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
    candidate.predecessor.quick.base.base.impl.base.validate_local_references()


def normalize_established_provenance() -> None:
    for slug in MODERN:
        path = SITE / "playgrounds" / slug / "index.html"
        page = path.read_text(encoding="utf-8")
        page = page.replace("https://logandixon.me", ESTABLISHED_PORTFOLIO)
        page = page.replace("https://orcid.org/0009-0008-1712-6630", ESTABLISHED_ORCID)
        if ESTABLISHED_PORTFOLIO not in page or ESTABLISHED_ORCID not in page:
            raise RuntimeError(f"Established modern-lab provenance missing after normalization: {slug}")
        if "https://logandixon.me" in page or "0009-0008-1712-6630" in page:
            raise RuntimeError(f"Unapproved alternate provenance survived normalization: {slug}")
        path.write_text(page, encoding="utf-8")


def build_site() -> None:
    candidate.validate = validate
    candidate.build_site()
    normalize_established_provenance()
    validate()
    print("Finalized v1.7.1 modern-lab parity composition with DOM-level Quick Assign validation and established suite provenance")


if __name__ == "__main__":
    build_site()
