#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import shutil
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from build_transformer_public import build_public as build_transformer_public


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
PUBLIC_MANIFEST = ROOT / "tools" / "applets_v1_2.json"

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
    "media/AI_Playgrounds_Demo_15s.gif",
    "media/AI_Playgrounds_Demo_15s.mp4",
    "assets/guided-challenges.css",
    "assets/guided-challenges.js",
    "assets/localization-r4.css",
    "assets/localization-r4.js",
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

LEGACY_SOURCE_APPLETS = {
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
PUBLIC_APPLETS = LEGACY_SOURCE_APPLETS | {"transformer-language-model"}

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


def public_manifest() -> list[dict[str, object]]:
    manifest = json.loads(PUBLIC_MANIFEST.read_text(encoding="utf-8"))
    if len(manifest) != 13 or {entry.get("slug") for entry in manifest} != PUBLIC_APPLETS:
        raise RuntimeError("v1.2 public manifest must contain exactly the thirteen release applets")
    return manifest


def transform_landing() -> None:
    path = SITE / "index.html"
    html = path.read_text(encoding="utf-8")
    manifest = public_manifest()

    compact = json.dumps(manifest, ensure_ascii=False, separators=(",", ":"))
    html, count = re.subn(
        r"const APPLETS=\[[\s\S]*?\];\nconst COPY=",
        "const APPLETS=" + compact + ";\nconst COPY=",
        html,
        count=1,
    )
    if count != 1:
        raise RuntimeError("Could not synchronize landing-page applet manifest")

    replacements = {
        "AI Playgrounds | Twelve interactive foundations of AI": "AI Playgrounds | Thirteen interactive foundations of AI",
        "Twelve bilingual, offline-ready AI interactives for search, logic, probability, machine learning, vision, and reinforcement learning.": "Thirteen multilingual, offline-ready AI interactives for search, logic, probability, machine learning, neural networks, computer vision, reinforcement learning, and Transformer language modeling.",
        "Twelve bilingual, single-file AI interactives built for classroom use and independent exploration.": "Thirteen multilingual, single-file AI interactives built for classroom use and independent exploration.",
        "AI Playgrounds: twelve bilingual interactives for foundational artificial intelligence": "AI Playgrounds: thirteen multilingual interactives for foundational artificial intelligence",
        "Twelve bilingual, offline-ready interactives for foundational artificial intelligence.": "Thirteen multilingual, offline-ready interactives for foundational artificial intelligence.",
        "Twelve bilingual interactives for search, logic, probability, machine learning, vision, and reinforcement learning. Each runs as one portable HTML file, with no account or backend.": "Thirteen multilingual interactives for search, logic, probability, machine learning, neural networks, computer vision, reinforcement learning, and Transformer language modeling. Each deployed applet remains portable and offline-ready, with no account or backend.",
        "Explore all twelve": "Explore all thirteen",
        "Explore the twelve applets": "Explore the thirteen applets",
        "12 inspectable applets": "13 inspectable applets",
        "English + Simplified Chinese": "EN + ZH + VI + ES",
        "十二个双语交互工具，涵盖搜索、逻辑、概率、机器学习、视觉和强化学习。每个工具都是一个可离线运行的 HTML 文件，不需要账户或后端。": "十三个多语言交互工具，涵盖搜索、逻辑、概率、机器学习、神经网络、计算机视觉、强化学习与 Transformer 语言建模。每个已部署工具都可离线使用，不需要账户或后端。",
        "探索全部十二个": "探索全部十三个",
        "探索十二个交互工具": "探索十三个交互工具",
        "12 个可检查的交互工具": "13 个可检查的交互工具",
        "英语 + 简体中文": "英语 + 简体中文 + 越南语 + 西班牙语",
        '"inLanguage":["en","zh"]': '"inLanguage":["en","zh","vi","es"]',
        '"inLanguage": ["en", "zh-Hans"]': '"inLanguage": ["en", "zh-Hans", "vi", "es"]',
        '"version": "1.0.1"': '"version": "1.2.0"',
    }
    for old, new in replacements.items():
        html = html.replace(old, new)

    if "transformer-language-model" not in html or "Explore the thirteen applets" not in html:
        raise RuntimeError("Landing-page v1.2 transformation did not complete")
    path.write_text(html, encoding="utf-8")


def transform_curriculum() -> None:
    path = SITE / "curriculum.html"
    html = path.read_text(encoding="utf-8")
    html = html.replace(
        "Course-aligned and quick-entry sequences for twelve foundational AI applets.",
        "Course-aligned and quick-entry sequences for thirteen foundational AI applets.",
    )
    legend_anchor = '<span style="--legend:#b91c1c"><i></i>Q-Learning Gridworld</span>'
    legend_extra = legend_anchor + '<span style="--legend:#6d28d9"><i></i>Transformer Language Modeling</span>'
    if legend_anchor in html and "<i></i>Transformer Language Modeling</span>" not in html:
        html = html.replace(legend_anchor, legend_extra, 1)

    row = (
        '<tr style="--applet-accent:#6d28d9"><td data-label="#"><span class="order-dot">13</span></td>'
        '<td data-label="Applet"><a href="playgrounds/transformer-language-model/index.html">Transformer Language Modeling</a></td>'
        '<td data-label="Concept area">Generative language models</td>'
        '<td data-label="Why here">Connect token representation, causal self-attention, and next-token probabilities after the earlier neural-network foundations.</td></tr>'
    )
    if "playgrounds/transformer-language-model/index.html" not in html:
        html = html.replace("</tbody>", row + "</tbody>", 1)

    if html.count('class="order-dot"') != 13:
        raise RuntimeError("Built curriculum must contain exactly thirteen course rows")
    path.write_text(html, encoding="utf-8")


def transform_release_notes() -> None:
    path = SITE / "release-notes.html"
    html = path.read_text(encoding="utf-8")
    banner = (
        '<section id="release-v1-2-0" style="margin:1rem 0;padding:1rem 1.2rem;border:1px solid currentColor;border-radius:12px">'
        '<h2>AI Playgrounds v1.2.0, released August 24, 2026.</h2>'
        '<p>v1.2.0 adds Lab 13, Transformer Language Modeling, as the thirteenth public applet with EN, ZH, VI, and ES semantic parity, deterministic reference arithmetic, prediction-before-reveal challenges, and offline browser operation.</p>'
        '</section>'
    )
    if "release-v1-2-0" not in html:
        html, count = re.subn(r"(<main[^>]*>)", r"\1" + banner, html, count=1)
        if count != 1:
            raise RuntimeError("Could not insert v1.2 release note into public page")
    path.write_text(html, encoding="utf-8")


def build_site() -> None:
    if SITE.exists():
        shutil.rmtree(SITE)

    SITE.mkdir(parents=True)

    for relative_path in ROOT_PUBLIC_FILES:
        copy_file(relative_path)

    # The legacy source manifest remains bound to the twelve source applets used by
    # the inherited v1.1 release checker. The deployed v1.2 manifest is a separate,
    # explicit thirteen-applet release input.
    shutil.copy2(PUBLIC_MANIFEST, SITE / "applets.json")

    copy_file("tests/index.html")

    locale_dir = ROOT / "assets" / "locales"
    shared_locale = locale_dir / "common-r4.js"
    if not shared_locale.is_file():
        raise RuntimeError("Missing shared R4 locale catalog: common-r4.js")

    applet_locale_sources = sorted(
        path
        for path in locale_dir.glob("*-r4.js")
        if path.name != "common-r4.js"
    )
    catalog_applets = {
        source.name.removesuffix("-r4.js")
        for source in applet_locale_sources
    }
    if catalog_applets != LEGACY_SOURCE_APPLETS:
        missing = sorted(LEGACY_SOURCE_APPLETS - catalog_applets)
        unexpected = sorted(catalog_applets - LEGACY_SOURCE_APPLETS)
        raise RuntimeError(
            "R4 legacy applet locale catalog mismatch. "
            f"Missing={missing}; unexpected={unexpected}"
        )
    if len(applet_locale_sources) != 12:
        raise RuntimeError(
            f"Expected 12 legacy applet R4 locale catalogs, found {len(applet_locale_sources)}"
        )

    copy_file(str(shared_locale.relative_to(ROOT)))
    for source in applet_locale_sources:
        copy_file(str(source.relative_to(ROOT)))

    applet_sources = sorted((ROOT / "playgrounds").glob("*/index.html"))
    applet_names = {path.parent.name for path in applet_sources}

    if applet_names != LEGACY_SOURCE_APPLETS:
        missing = sorted(LEGACY_SOURCE_APPLETS - applet_names)
        unexpected = sorted(applet_names - LEGACY_SOURCE_APPLETS)
        raise RuntimeError(
            f"Legacy source applet set mismatch. Missing={missing}; unexpected={unexpected}"
        )

    for source in applet_sources:
        relative_path = source.relative_to(ROOT)
        destination = SITE / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    # Lab 13 is generated from its independently verified English source and frozen
    # four-locale catalogs. The deployed result is still one self-contained HTML file.
    build_transformer_public(
        SITE / "playgrounds" / "transformer-language-model" / "index.html"
    )

    transform_landing()
    transform_curriculum()
    transform_release_notes()


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

    if deployed_applets != PUBLIC_APPLETS:
        missing = sorted(PUBLIC_APPLETS - deployed_applets)
        unexpected = sorted(deployed_applets - PUBLIC_APPLETS)
        raise RuntimeError(
            f"The deployed v1.2 applet set is incorrect. Missing={missing}; unexpected={unexpected}"
        )

    if len(list(SITE.rglob("playgrounds/*/index.html"))) != 13:
        raise RuntimeError("The v1.2 deployment must contain exactly thirteen applets.")

    deployed_locale_sources = sorted((SITE / "assets" / "locales").glob("*-r4.js"))
    if len(deployed_locale_sources) != 13:
        raise RuntimeError(
            "The deployment must contain exactly twelve legacy applet R4 catalogs "
            "plus common-r4.js; Lab 13 locales are embedded in its single HTML file."
        )
    if not (SITE / "assets" / "locales" / "common-r4.js").is_file():
        raise RuntimeError("The shared R4 locale catalog was not deployed.")


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
