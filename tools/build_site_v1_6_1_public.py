#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import build_site_v1_6_1_candidate as candidate

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"


def patch_quick_assign_links() -> None:
    """Make every surfaced Level-1 activity link enter the existing Use-in-class mode."""
    registry = candidate.registry()
    active = [row for row in registry if row["status"] == "active"]
    targets = [SITE / "teacher-pack.html", SITE / "curriculum.html"]
    for path in targets:
        html = path.read_text(encoding="utf-8")
        for row in active:
            old = f'playgrounds/{row["slug"]}/index.html#{row["anchor"]}'
            new = f'playgrounds/{row["slug"]}/index.html?mode=classroom#{row["anchor"]}'
            html = html.replace(old, new)
        path.write_text(html, encoding="utf-8")


def validate_public_links() -> None:
    active = [row for row in candidate.registry() if row["status"] == "active"]
    for page_name in ("teacher-pack.html", "curriculum.html"):
        html = (SITE / page_name).read_text(encoding="utf-8")
        for row in active:
            canonical = f'playgrounds/{row["slug"]}/index.html?mode=classroom#{row["anchor"]}'
            legacy = f'playgrounds/{row["slug"]}/index.html#{row["anchor"]}'
            if canonical not in html:
                raise RuntimeError(f"{page_name} lacks canonical classroom-mode Quick Assign link for {row['id']}")
            if legacy in html:
                raise RuntimeError(f"{page_name} retains hidden-panel Quick Assign link for {row['id']}")


def build_site() -> None:
    candidate.build_site()
    patch_quick_assign_links()
    validate_public_links()
    print("Built canonical v1.6.1 public candidate with classroom-mode Quick Assign deep links")


if __name__ == "__main__":
    build_site()
