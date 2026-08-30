#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import date
from pathlib import Path

SOURCE_REPOSITORY = "lmdixon23/ai-playgrounds"
PORTFOLIO_REPOSITORY = "lmdixon23/lmdixon23.github.io"
DEFAULT_PORTFOLIO_BASE_URL = (
    "https://raw.githubusercontent.com/"
    f"{PORTFOLIO_REPOSITORY}/main"
)
DOI = "10.5281/zenodo.21854217"
ARCHIVED_VERSION = "v1.0.1"
SEMVER_TAG = re.compile(r"v\d+\.\d+\.\d+")
SURFACE_PATHS = (
    "projects/ai-playgrounds.html",
    "index.html",
    "README.md",
    "sitemap.xml",
)
MANIFEST_PATH = "SHA256SUMS.txt"


@dataclass(frozen=True)
class ReleaseBoundary:
    tag: str
    published: date


def request_bytes(url: str, *, authenticated: bool = False) -> bytes:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "ai-playgrounds-portfolio-freshness/1",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if authenticated and token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.read()
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError(f"Unable to fetch {url}: {exc}") from exc


def release_boundary(tag_override: str | None, date_override: str | None) -> ReleaseBoundary:
    if tag_override and date_override:
        return ReleaseBoundary(validate_tag(tag_override), parse_date(date_override, "release date"))

    if tag_override:
        encoded = urllib.parse.quote(validate_tag(tag_override), safe="")
        endpoint = f"https://api.github.com/repos/{SOURCE_REPOSITORY}/releases/tags/{encoded}"
    else:
        endpoint = f"https://api.github.com/repos/{SOURCE_REPOSITORY}/releases/latest"

    try:
        payload = json.loads(request_bytes(endpoint, authenticated=True))
    except json.JSONDecodeError as exc:
        raise RuntimeError("GitHub release metadata was not valid JSON") from exc

    tag = validate_tag(str(payload.get("tag_name", "")))
    if tag_override and tag != tag_override:
        raise RuntimeError(f"GitHub returned release {tag} while {tag_override} was requested")
    published_at = payload.get("published_at") or payload.get("created_at")
    if not isinstance(published_at, str):
        raise RuntimeError(f"Release {tag} has no publication date")
    return ReleaseBoundary(tag, parse_date(published_at[:10], "release publication date"))


def validate_tag(tag: str) -> str:
    if SEMVER_TAG.fullmatch(tag) is None:
        raise RuntimeError(f"Release tag must use vX.Y.Z format: {tag!r}")
    return tag


def parse_date(value: str, label: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise RuntimeError(f"Invalid {label}: {value!r}") from exc


def load_portfolio_files(root: Path | None, base_url: str) -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    for relative in (*SURFACE_PATHS, MANIFEST_PATH):
        if root is not None:
            path = root / relative
            if not path.is_file():
                raise RuntimeError(f"Portfolio surface is missing: {relative}")
            files[relative] = path.read_bytes()
        else:
            url = f"{base_url.rstrip('/')}/{relative}"
            files[relative] = request_bytes(url)
    return files


def decode(files: dict[str, bytes], relative: str) -> str:
    try:
        return files[relative].decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError(f"Portfolio surface is not UTF-8: {relative}") from exc


def require_contains(
    failures: list[str], relative: str, text: str, expected: str, label: str
) -> None:
    if expected not in text:
        failures.append(f"{relative}: missing {label}: {expected}")


def check_sitemap(text: str, boundary: ReleaseBoundary, failures: list[str]) -> None:
    relative = "sitemap.xml"
    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        failures.append(f"{relative}: invalid XML: {exc}")
        return

    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    expected_loc = "https://lmdixon23.github.io/projects/ai-playgrounds.html"
    for entry in root.findall("sm:url", namespace):
        loc = entry.findtext("sm:loc", default="", namespaces=namespace)
        if loc != expected_loc:
            continue
        lastmod = entry.findtext("sm:lastmod", default="", namespaces=namespace)
        try:
            lastmod_date = parse_date(lastmod, "AI Playgrounds sitemap lastmod")
        except RuntimeError as exc:
            failures.append(f"{relative}: {exc}")
            return
        if lastmod_date < boundary.published:
            failures.append(
                f"{relative}: AI Playgrounds lastmod {lastmod_date} predates "
                f"release {boundary.tag} on {boundary.published}"
            )
        return
    failures.append(f"{relative}: missing AI Playgrounds case-study URL")


def check_manifest(files: dict[str, bytes], failures: list[str]) -> None:
    manifest = decode(files, MANIFEST_PATH)
    records: dict[str, str] = {}
    for line_number, line in enumerate(manifest.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        if match is None:
            failures.append(f"{MANIFEST_PATH}:{line_number}: invalid SHA-256 record")
            continue
        digest, relative = match.groups()
        if relative in records:
            failures.append(f"{MANIFEST_PATH}: duplicate entry for {relative}")
        records[relative] = digest

    for relative in SURFACE_PATHS:
        expected = records.get(relative)
        if expected is None:
            failures.append(f"{MANIFEST_PATH}: missing integrity entry for {relative}")
            continue
        actual = hashlib.sha256(files[relative]).hexdigest()
        if actual != expected:
            failures.append(
                f"{MANIFEST_PATH}: {relative} hash mismatch "
                f"(declared {expected}, actual {actual})"
            )


def check_portfolio(files: dict[str, bytes], boundary: ReleaseBoundary) -> list[str]:
    failures: list[str] = []
    case = decode(files, "projects/ai-playgrounds.html")
    home = decode(files, "index.html")
    readme = decode(files, "README.md")
    sitemap = decode(files, "sitemap.xml")
    tag = boundary.tag
    release_href = f"https://github.com/{SOURCE_REPOSITORY}/releases/tag/{tag}"

    require_contains(
        failures,
        "projects/ai-playgrounds.html",
        case,
        f"<title>AI Playgrounds {tag} — Project case study</title>",
        "current case-study title",
    )
    require_contains(
        failures,
        "projects/ai-playgrounds.html",
        case,
        f"current release {tag}",
        "current release marker",
    )
    require_contains(
        failures,
        "projects/ai-playgrounds.html",
        case,
        release_href,
        "exact release link",
    )
    require_contains(
        failures,
        "projects/ai-playgrounds.html",
        case,
        f"{tag} has not been assigned the archived {ARCHIVED_VERSION} version DOI.",
        "current-versus-DOI boundary",
    )
    require_contains(
        failures,
        "projects/ai-playgrounds.html",
        case,
        "Those product and test counts describe the historical archive. "
        f"They are not presented as totals for the larger {tag} assurance stack.",
        "historical-count boundary",
    )
    require_contains(
        failures,
        "projects/ai-playgrounds.html",
        case,
        DOI,
        "archived DOI",
    )

    require_contains(
        failures,
        "index.html",
        home,
        f"current {tag} boundary",
        "homepage current-release marker",
    )
    require_contains(failures, "index.html", home, release_href, "homepage release link")

    require_contains(
        failures,
        "README.md",
        readme,
        f"current {tag} educational-software release",
        "README current-release marker",
    )
    require_contains(
        failures,
        "README.md",
        readme,
        f"that version DOI is not assigned to {tag}",
        "README DOI boundary",
    )
    require_contains(failures, "README.md", readme, DOI, "README archived DOI")

    check_sitemap(sitemap, boundary, failures)
    check_manifest(files, failures)
    return failures


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check that the public portfolio tracks the current AI Playgrounds release."
    )
    parser.add_argument(
        "--release-tag",
        default=os.environ.get("AI_PLAYGROUNDS_RELEASE_TAG") or None,
        help="Release tag to check; defaults to the latest published GitHub release.",
    )
    parser.add_argument(
        "--release-date",
        default=os.environ.get("AI_PLAYGROUNDS_RELEASE_DATE") or None,
        help="ISO release date override for deterministic local tests.",
    )
    parser.add_argument(
        "--portfolio-root",
        type=Path,
        help="Read portfolio surfaces from a local checkout instead of GitHub.",
    )
    parser.add_argument(
        "--portfolio-base-url",
        default=DEFAULT_PORTFOLIO_BASE_URL,
        help="Raw portfolio base URL used for the live check.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        boundary = release_boundary(args.release_tag, args.release_date)
        files = load_portfolio_files(args.portfolio_root, args.portfolio_base_url)
        failures = check_portfolio(files, boundary)
    except RuntimeError as exc:
        print("PORTFOLIO FRESHNESS: FAIL")
        print(f"- {exc}")
        return 1

    if failures:
        print(f"PORTFOLIO FRESHNESS: FAIL ({boundary.tag})")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        "PORTFOLIO FRESHNESS: PASS "
        f"({boundary.tag}; {len(SURFACE_PATHS)} public surfaces; "
        f"{len(SURFACE_PATHS)} integrity records; archived {ARCHIVED_VERSION} DOI preserved)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
