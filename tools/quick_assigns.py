#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "src" / "product" / "quick-assigns.json"
HISTORICAL_REGISTRY = ROOT / "tools" / "quick_assigns_v2.json"
PHASE = "v1.9-r6a-canonical-quick-assign-registry"
EXPECTED_SEQUENCE = ["predict", "run", "observe", "explain", "transfer"]
EXPECTED_LOCALES = ["en", "zh", "vi", "es"]
EXPECTED_ACTIVITY_COUNT = 15
EXPECTED_HISTORICAL_SHA256 = "9c94549a36e72ba465b08ed1df703b3482d3a6ff72c47893bdb5660497eacc51"
ID_PATTERN = re.compile(r"^QA-[A-Z0-9]+(?:-[A-Z0-9]+)*-[0-9]{2}$")
REQUIRED_ACTIVITY_FIELDS = {
    "id",
    "slug",
    "status",
    "title",
    "anchor",
    "source",
    "objective",
    "teacher_look_for",
    "locales",
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def load_json(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError(f"JSON object required: {path.relative_to(ROOT)}")
    return payload


def load_and_validate(*, require_historical_equivalence: bool = False) -> dict[str, object]:
    if not REGISTRY.is_file():
        raise RuntimeError("Canonical Quick Assign registry is missing")

    payload = load_json(REGISTRY)
    if payload.get("schema_version") != 1:
        raise RuntimeError("Canonical Quick Assign schema version must be 1")
    if payload.get("phase") != PHASE:
        raise RuntimeError(f"Canonical Quick Assign phase must be {PHASE}")
    if payload.get("level_1_duration_minutes") != "10-15":
        raise RuntimeError("Quick Assign duration boundary changed")
    if payload.get("sequence") != EXPECTED_SEQUENCE:
        raise RuntimeError("Quick Assign inquiry sequence changed")

    historical = payload.get("historical_equivalence")
    expected_historical = {
        "source": "tools/quick_assigns_v2.json",
        "schema_version": 2,
        "role": "test-only-regression-and-provenance",
        "sha256": EXPECTED_HISTORICAL_SHA256,
    }
    if historical != expected_historical:
        raise RuntimeError("Historical Quick Assign provenance declaration changed")

    activities = payload.get("activities")
    if not isinstance(activities, list) or len(activities) != EXPECTED_ACTIVITY_COUNT:
        raise RuntimeError("Canonical Quick Assign registry must contain exactly 15 activities")

    ids: list[str] = []
    slugs: list[str] = []
    anchors: list[str] = []
    for index, row in enumerate(activities):
        if not isinstance(row, dict):
            raise RuntimeError(f"Quick Assign row {index} must be an object")
        if set(row) != REQUIRED_ACTIVITY_FIELDS:
            missing = sorted(REQUIRED_ACTIVITY_FIELDS - set(row))
            extra = sorted(set(row) - REQUIRED_ACTIVITY_FIELDS)
            raise RuntimeError(f"Quick Assign fields changed for row {index}: missing={missing}, extra={extra}")
        activity_id = row.get("id")
        slug = row.get("slug")
        anchor = row.get("anchor")
        if not isinstance(activity_id, str) or not ID_PATTERN.fullmatch(activity_id):
            raise RuntimeError(f"Invalid Quick Assign ID: {activity_id!r}")
        if not isinstance(slug, str) or not slug:
            raise RuntimeError(f"Invalid Quick Assign slug for {activity_id}")
        if anchor != f"quick-assign-{activity_id.lower()}":
            raise RuntimeError(f"Quick Assign anchor does not match stable ID for {activity_id}")
        if row.get("status") != "active":
            raise RuntimeError(f"Current Quick Assign must remain active: {activity_id}")
        if row.get("locales") != EXPECTED_LOCALES:
            raise RuntimeError(f"Quick Assign locale boundary changed for {activity_id}")
        for field in ("title", "source", "objective", "teacher_look_for"):
            if not isinstance(row.get(field), str) or not row[field].strip():
                raise RuntimeError(f"Quick Assign field {field} is empty for {activity_id}")
        ids.append(activity_id)
        slugs.append(slug)
        anchors.append(anchor)

    if len(set(ids)) != EXPECTED_ACTIVITY_COUNT:
        raise RuntimeError("Canonical Quick Assign IDs are not unique")
    if len(set(slugs)) != EXPECTED_ACTIVITY_COUNT:
        raise RuntimeError("Canonical Quick Assign slugs are not unique")
    if len(set(anchors)) != EXPECTED_ACTIVITY_COUNT:
        raise RuntimeError("Canonical Quick Assign anchors are not unique")

    historical_equivalent: bool | None = None
    historical_digest: str | None = None
    if require_historical_equivalence:
        if not HISTORICAL_REGISTRY.is_file():
            raise RuntimeError("Historical Quick Assign registry is missing")
        historical_digest = digest(HISTORICAL_REGISTRY)
        if historical_digest != EXPECTED_HISTORICAL_SHA256:
            raise RuntimeError("Historical Quick Assign registry digest changed")
        historical_payload = load_json(HISTORICAL_REGISTRY)
        if historical_payload.get("schema_version") != 2:
            raise RuntimeError("Historical Quick Assign schema version changed")
        historical_equivalent = all(
            payload.get(field) == historical_payload.get(field)
            for field in ("level_1_duration_minutes", "sequence", "activities")
        )
        if not historical_equivalent:
            raise RuntimeError("Canonical Quick Assign handoff differs from frozen historical semantics")

    return {
        "manifest": payload,
        "activities": activities,
        "by_slug": {row["slug"]: row for row in activities},
        "ids": ids,
        "slugs": slugs,
        "anchors": anchors,
        "sha256": digest(REGISTRY),
        "historical_sha256": historical_digest,
        "historical_equivalent": historical_equivalent,
    }


def validate_emitted(site: Path, state: dict[str, object]) -> dict[str, object]:
    activities = state["activities"]
    surface_checks = 0
    for row in activities:
        path = site / "playgrounds" / row["slug"] / "index.html"
        if not path.is_file():
            raise RuntimeError(f"Generated Quick Assign applet is missing: {row['slug']}")
        html = path.read_text(encoding="utf-8")
        if html.count(f'data-quick-assign-id="{row["id"]}"') != 1:
            raise RuntimeError(f"Generated Quick Assign surface count changed for {row['id']}")
        if html.count(f'id="{row["anchor"]}"') != 1:
            raise RuntimeError(f"Generated Quick Assign anchor count changed for {row['id']}")
        surface_checks += 2

    support_checks = 0
    for public_path in ("teacher-pack.html", "curriculum.html"):
        path = site / public_path
        if not path.is_file():
            raise RuntimeError(f"Generated Quick Assign support page is missing: {public_path}")
        content = path.read_text(encoding="utf-8")
        semantic_fields = (
            ("title", "objective")
            if public_path == "curriculum.html"
            else ("title", "teacher_look_for")
        )
        for row in activities:
            link = f'playgrounds/{row["slug"]}/index.html?mode=classroom#{row["anchor"]}'
            if content.count(row["id"]) != 1 or content.count(link) != 1:
                raise RuntimeError(f"Generated {public_path} Quick Assign binding count changed for {row['id']}")
            support_checks += 2
            for field in semantic_fields:
                if content.count(escape(row[field])) != 1:
                    raise RuntimeError(f"Generated {public_path} Quick Assign {field} changed for {row['id']}")
                support_checks += 1

    return {
        "activity_count": len(activities),
        "surface_checks": surface_checks,
        "support_checks": support_checks,
        "pass": True,
    }
