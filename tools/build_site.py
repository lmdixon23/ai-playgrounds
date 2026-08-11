#!/usr/bin/env python3
from __future__ import annotations

import shutil
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"

ROOT_PUBLIC_FILES = (
    ".nojekyll",
    "404.html",
    "curriculum.html",
    "index.html",
    "quality.html",
    "release-notes.html",
    "research-and-citation.html",
    "student-lab.html",
    "teacher-pack.html",
    "og-image.png",
    "media/AI_Playgrounds_Demo_15s.mp4",
    "robots.txt",
    "sitemap.xml",
    # Deliberately public files linked from the live application.
    "ARCHITECTURE.md",
    "CITATION.cff",
    "CONTRIBUTING.md",
    "LICENSE",
    "STUDENT_LAB_PACKET_TEMPLATE.md",
    "TEACHER_PACK.md",
    "applets.json",
    "codemeta.json",
)

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

FORBIDDEN_DEPLOYED_PATHS = (
    ".git",
    ".github",
    "_local",
    "docs",
    "release-evidence",
    "research",
    "tools",
    "README.md",
    "CHANGELOG.md",
    "CURRICULUM.md",
    "QUALITY.md",
    "RELEASE_NOTES.md",
    "SECURITY.md",
)


class LocalReferenceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: list[str] = []

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        values = dict(attrs)

        if tag in {"a", "link"} and values.get("href"):
            self.references.append(str(values["href"]))

        if tag in {"img", "script", "source"} and values.get("src"):
            self.references.append(str(values["src"]))


def copy_file(relative_path: str) -> None:
    source = ROOT / relative_path
    destination = SITE / relative_path

    if not source.is_file():
        raise FileNotFoundError(f"Required public file is missing: {relative_path}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def build_site() -> None:
    if SITE.exists():
        shutil.rmtree(SITE)

    SITE.mkdir(parents=True)

    for relative_path in ROOT_PUBLIC_FILES:
        copy_file(relative_path)

    copy_file("tests/index.html")

    applet_sources = sorted((ROOT / "playgrounds").glob("*/index.html"))
    applet_names = {path.parent.name for path in applet_sources}

    if applet_names != EXPECTED_APPLETS:
        missing = sorted(EXPECTED_APPLETS - applet_names)
        unexpected = sorted(applet_names - EXPECTED_APPLETS)
        raise RuntimeError(
            f"Applet set mismatch. Missing={missing}; unexpected={unexpected}"
        )

    for source in applet_sources:
        relative_path = source.relative_to(ROOT)
        destination = SITE / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def is_external(reference: str) -> bool:
    if reference.startswith("#"):
        return True

    parsed = urlsplit(reference)

    return parsed.scheme in {
        "data",
        "http",
        "https",
        "javascript",
        "mailto",
        "tel",
    } or bool(parsed.netloc)


def validate_local_references() -> None:
    failures: list[str] = []
    site_root = SITE.resolve()

    for html_path in sorted(SITE.rglob("*.html")):
        parser = LocalReferenceParser()
        parser.feed(html_path.read_text(encoding="utf-8", errors="replace"))

        for reference in parser.references:
            if is_external(reference):
                continue

            parsed = urlsplit(reference)
            relative_target = unquote(parsed.path)

            # Empty paths refer to the current page with a query or fragment.
            if not relative_target:
                continue

            candidate = (html_path.parent / relative_target).resolve()

            try:
                candidate.relative_to(site_root)
            except ValueError:
                failures.append(
                    f"{html_path.relative_to(SITE)} -> {reference}: "
                    "target escapes the deployment root"
                )
                continue

            if relative_target.endswith("/"):
                candidate = candidate / "index.html"

            if not candidate.exists():
                failures.append(
                    f"{html_path.relative_to(SITE)} -> {reference}: "
                    f"missing {candidate.relative_to(site_root)}"
                )

    if failures:
        formatted = "\n".join(f"  - {failure}" for failure in failures)
        raise RuntimeError(f"Broken local deployment links:\n{formatted}")


def validate_boundary() -> None:
    for forbidden in FORBIDDEN_DEPLOYED_PATHS:
        if (SITE / forbidden).exists():
            raise RuntimeError(f"Forbidden deployment path exists: {forbidden}")

    deployed_applets = {
        path.parent.name
        for path in (SITE / "playgrounds").glob("*/index.html")
    }

    if deployed_applets != EXPECTED_APPLETS:
        raise RuntimeError("The deployed applet set is incomplete.")

    if len(list(SITE.rglob("playgrounds/*/index.html"))) != 12:
        raise RuntimeError("The deployment must contain exactly twelve applets.")


def main() -> None:
    build_site()
    validate_boundary()
    validate_local_references()

    deployed_files = sorted(
        str(path.relative_to(SITE))
        for path in SITE.rglob("*")
        if path.is_file()
    )

    print(f"Built minimal Pages artifact: {len(deployed_files)} files")
    print("Deployment boundary: PASS")

    for deployed_file in deployed_files:
        print(f"  {deployed_file}")


if __name__ == "__main__":
    main()
