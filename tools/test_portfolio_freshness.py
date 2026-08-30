#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import tempfile
import unittest
from datetime import date
from pathlib import Path

from check_portfolio_freshness import (
    DOI,
    MANIFEST_PATH,
    SURFACE_PATHS,
    ReleaseBoundary,
    check_portfolio,
    load_portfolio_files,
)


class PortfolioFreshnessTests(unittest.TestCase):
    tag = "v1.8.1"
    boundary = ReleaseBoundary(tag=tag, published=date(2026, 8, 27))

    def fixture(self, root: Path) -> None:
        release_href = (
            "https://github.com/lmdixon23/ai-playgrounds/releases/tag/"
            f"{self.tag}"
        )
        files = {
            "projects/ai-playgrounds.html": (
                f"<title>AI Playgrounds {self.tag} — Project case study</title>\n"
                f"<p>current release {self.tag}</p>\n"
                f"<a href=\"{release_href}\">release</a>\n"
                f"<p>{self.tag} has not been assigned the archived v1.0.1 version DOI.</p>\n"
                "<p>Those product and test counts describe the historical archive. "
                f"They are not presented as totals for the larger {self.tag} assurance stack.</p>\n"
                f"<p>{DOI}</p>\n"
            ),
            "index.html": (
                f"<p>current {self.tag} boundary</p>\n"
                f"<a href=\"{release_href}\">release</a>\n"
            ),
            "README.md": (
                f"current {self.tag} educational-software release\n"
                f"{DOI}\nthat version DOI is not assigned to {self.tag}\n"
            ),
            "sitemap.xml": (
                '<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                "  <url>\n"
                "    <loc>https://lmdixon23.github.io/projects/ai-playgrounds.html</loc>\n"
                "    <lastmod>2026-08-29</lastmod>\n"
                "  </url>\n"
                "</urlset>\n"
            ),
        }
        for relative, text in files.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8", newline="\n")
        manifest = "".join(
            f"{hashlib.sha256((root / relative).read_bytes()).hexdigest()}  {relative}\n"
            for relative in SURFACE_PATHS
        )
        (root / MANIFEST_PATH).write_text(manifest, encoding="utf-8", newline="\n")

    def load(self, root: Path) -> dict[str, bytes]:
        return load_portfolio_files(root, "unused")

    def test_current_surfaces_pass(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            self.assertEqual(check_portfolio(self.load(root), self.boundary), [])

    def test_stale_homepage_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            home = root / "index.html"
            home.write_text(
                home.read_text(encoding="utf-8").replace(self.tag, "v1.7.2"),
                encoding="utf-8",
                newline="\n",
            )
            failures = check_portfolio(self.load(root), self.boundary)
            self.assertTrue(any("homepage current-release marker" in item for item in failures))
            self.assertTrue(any("index.html hash mismatch" in item for item in failures))

    def test_doi_boundary_is_required(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            case = root / "projects/ai-playgrounds.html"
            case.write_text(
                case.read_text(encoding="utf-8").replace(
                    f"{self.tag} has not been assigned the archived v1.0.1 version DOI.",
                    f"{self.tag} uses the archived DOI.",
                ),
                encoding="utf-8",
                newline="\n",
            )
            failures = check_portfolio(self.load(root), self.boundary)
            self.assertTrue(any("current-versus-DOI boundary" in item for item in failures))

    def test_sitemap_cannot_predate_release(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            sitemap = root / "sitemap.xml"
            sitemap.write_text(
                sitemap.read_text(encoding="utf-8").replace("2026-08-29", "2026-08-26"),
                encoding="utf-8",
                newline="\n",
            )
            failures = check_portfolio(self.load(root), self.boundary)
            self.assertTrue(any("predates release" in item for item in failures))

    def test_integrity_record_must_match(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            manifest = root / MANIFEST_PATH
            manifest.write_text(
                manifest.read_text(encoding="utf-8").replace(
                    hashlib.sha256((root / "README.md").read_bytes()).hexdigest(),
                    "0" * 64,
                ),
                encoding="utf-8",
                newline="\n",
            )
            failures = check_portfolio(self.load(root), self.boundary)
            self.assertTrue(any("README.md hash mismatch" in item for item in failures))


if __name__ == "__main__":
    unittest.main()
