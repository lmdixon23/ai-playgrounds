#!/usr/bin/env python3
from __future__ import annotations

"""Final validation wrapper for the v1.7.1 modern-lab parity candidate.

The first parity candidate correctly composed the learner-facing shell, but its
static guard counted every textual occurrence of `data-quick-assign-id`,
including JavaScript selector strings. This wrapper keeps that candidate frozen
and replaces only the surface-count validator with a start-tag count.
"""

import re

import build_site_v1_7_1_modern_parity as candidate

SITE = candidate.SITE
MODERN = candidate.MODERN


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


def build_site() -> None:
    candidate.validate = validate
    candidate.build_site()
    print("Finalized v1.7.1 modern-lab parity composition with DOM-level Quick Assign surface validation")


if __name__ == "__main__":
    build_site()
