#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

import build_site as base
from build_agent_tool_context_public import build_public as build_agent_public

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
V12_MANIFEST = ROOT / "tools" / "applets_v1_2.json"
LAB14_ENTRY = ROOT / "tools" / "applet_v1_3_lab14.json"
GENERATED_MANIFEST = ROOT / "release-evidence" / "applets-v1.3.json"


def release_manifest() -> list[dict[str, object]]:
    inherited = json.loads(V12_MANIFEST.read_text(encoding="utf-8"))
    lab14 = json.loads(LAB14_ENTRY.read_text(encoding="utf-8"))
    manifest = inherited + [lab14]
    slugs = [str(entry.get("slug")) for entry in manifest]
    if len(inherited) != 13 or "transformer-language-model" not in slugs:
        raise RuntimeError("v1.3 must inherit the exact thirteen-app v1.2 release inventory")
    if len(manifest) != 14 or slugs.count("agent-tool-context") != 1 or len(set(slugs)) != 14:
        raise RuntimeError("v1.3 release composition must contain exactly fourteen unique applets")
    if int(lab14.get("course_order", 0)) != 14 or int(lab14.get("showcase_order", 0)) != 14:
        raise RuntimeError("Lab 14 release metadata must occupy course/showcase order 14")
    return manifest


def write_release_manifest() -> None:
    GENERATED_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    GENERATED_MANIFEST.write_text(
        json.dumps(release_manifest(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def transform_landing_v13(original) -> None:
    original()
    path = SITE / "index.html"
    html = path.read_text(encoding="utf-8")
    replacements = {
        "AI Playgrounds | Thirteen interactive foundations of AI": "AI Playgrounds | Fourteen interactive foundations of AI",
        "Thirteen multilingual, offline-ready AI interactives for search, logic, probability, machine learning, neural networks, computer vision, reinforcement learning, and Transformer language modeling.": "Fourteen multilingual, offline-ready AI interactives for search, logic, probability, machine learning, neural networks, computer vision, reinforcement learning, Transformer language modeling, and agent tool use.",
        "Thirteen multilingual, single-file AI interactives built for classroom use and independent exploration.": "Fourteen multilingual, single-file AI interactives built for classroom use and independent exploration.",
        "AI Playgrounds: thirteen multilingual interactives for foundational artificial intelligence": "AI Playgrounds: fourteen multilingual interactives for foundational artificial intelligence",
        "Thirteen multilingual, offline-ready interactives for foundational artificial intelligence.": "Fourteen multilingual, offline-ready interactives for foundational artificial intelligence.",
        "Thirteen multilingual interactives for search, logic, probability, machine learning, neural networks, computer vision, reinforcement learning, and Transformer language modeling. Each deployed applet remains portable and offline-ready, with no account or backend.": "Fourteen multilingual interactives for search, logic, probability, machine learning, neural networks, computer vision, reinforcement learning, Transformer language modeling, and agent tool use. Each deployed applet remains portable and offline-ready, with no account or backend.",
        "Explore all thirteen": "Explore all fourteen",
        "Explore the thirteen applets": "Explore the fourteen applets",
        "13 inspectable applets": "14 inspectable applets",
        "十三个多语言交互工具，涵盖搜索、逻辑、概率、机器学习、神经网络、计算机视觉、强化学习与 Transformer 语言建模。每个已部署工具都可离线使用，不需要账户或后端。": "十四个多语言交互工具，涵盖搜索、逻辑、概率、机器学习、神经网络、计算机视觉、强化学习、Transformer 语言建模与智能体工具调用。每个已部署工具都可离线使用，不需要账户或后端。",
        "探索全部十三个": "探索全部十四个",
        "探索十三个交互工具": "探索十四个交互工具",
        "13 个可检查的交互工具": "14 个可检查的交互工具",
        '"version": "1.2.0"': '"version": "1.3.0"',
    }
    for old, new in replacements.items():
        html = html.replace(old, new)
    if "agent-tool-context" not in html or "Explore the fourteen applets" not in html:
        raise RuntimeError("Landing-page v1.3 transformation did not complete")
    path.write_text(html, encoding="utf-8")


def transform_curriculum_v13(original) -> None:
    original()
    path = SITE / "curriculum.html"
    html = path.read_text(encoding="utf-8")
    legend_anchor = '<span style="--legend:#6d28d9"><i></i>Transformer Language Modeling</span>'
    legend_extra = legend_anchor + '<span style="--legend:#0f766e"><i></i>Agent Tool Use and Context Protocols</span>'
    if legend_anchor in html and "<i></i>Agent Tool Use and Context Protocols</span>" not in html:
        html = html.replace(legend_anchor, legend_extra, 1)
    row = (
        '<tr style="--applet-accent:#0f766e"><td data-label="#"><span class="order-dot">14</span></td>'
        '<td data-label="Applet"><a href="playgrounds/agent-tool-context/index.html">Agent Tool Use and Context Protocols</a></td>'
        '<td data-label="Concept area">Agent systems and tool protocols</td>'
        '<td data-label="Why here">Connect goal-directed action selection with schemas, authorization, observations, provenance-aware context updates, and correct stopping.</td></tr>'
    )
    if "playgrounds/agent-tool-context/index.html" not in html:
        html = html.replace("</tbody>", row + "</tbody>", 1)
    html = html.replace(
        "Course-aligned and quick-entry sequences for thirteen foundational AI applets.",
        "Course-aligned and quick-entry sequences for fourteen foundational AI applets.",
    )
    if html.count('class="order-dot"') != 14:
        raise RuntimeError("Built curriculum must contain exactly fourteen course rows")
    path.write_text(html, encoding="utf-8")


def transform_release_notes_v13(original) -> None:
    original()
    path = SITE / "release-notes.html"
    html = path.read_text(encoding="utf-8")
    banner = (
        '<section id="release-v1-3-0" style="margin:1rem 0;padding:1rem 1.2rem;border:1px solid currentColor;border-radius:12px">'
        '<h2>AI Playgrounds v1.3.0, released August 25, 2026.</h2>'
        '<p>v1.3.0 adds Lab 14, Agent Tool Use and Context Protocols, as the fourteenth public applet with EN, ZH, VI, and ES semantic and browser parity, deterministic tool/runtime behavior, provenance-aware context, permission boundaries, and explicit stop decisions.</p>'
        '</section>'
    )
    if "release-v1-3-0" not in html:
        html, count = re.subn(r"(<main[^>]*>)", r"\1" + banner, html, count=1)
        if count != 1:
            raise RuntimeError("Could not insert v1.3 release note into public page")
    path.write_text(html, encoding="utf-8")


def build_site() -> None:
    write_release_manifest()

    base.PUBLIC_MANIFEST = GENERATED_MANIFEST
    base.PUBLIC_APPLETS = base.LEGACY_SOURCE_APPLETS | {
        "transformer-language-model",
        "agent-tool-context",
    }
    base.public_manifest = release_manifest

    original_transformer = base.build_transformer_public
    original_landing = base.transform_landing
    original_curriculum = base.transform_curriculum
    original_release_notes = base.transform_release_notes

    def build_generated(output: Path) -> None:
        original_transformer(output)
        build_agent_public(SITE / "playgrounds" / "agent-tool-context" / "index.html")

    base.build_transformer_public = build_generated
    base.transform_landing = lambda: transform_landing_v13(original_landing)
    base.transform_curriculum = lambda: transform_curriculum_v13(original_curriculum)
    base.transform_release_notes = lambda: transform_release_notes_v13(original_release_notes)

    base.build_site()


def validate_boundary() -> None:
    manifest = release_manifest()
    expected = {str(entry["slug"]) for entry in manifest}

    for forbidden in base.FORBIDDEN_DEPLOYED_PATHS:
        if (SITE / forbidden).exists():
            raise RuntimeError(f"Forbidden deployment path exists: {forbidden}")

    deployed = {path.parent.name for path in (SITE / "playgrounds").glob("*/index.html")}
    if deployed != expected:
        raise RuntimeError(
            f"The deployed v1.3 applet set is incorrect. Missing={sorted(expected-deployed)}; unexpected={sorted(deployed-expected)}"
        )
    if len(list(SITE.rglob("playgrounds/*/index.html"))) != 14:
        raise RuntimeError("The v1.3 deployment must contain exactly fourteen applets")

    locale_sources = sorted((SITE / "assets" / "locales").glob("*-r4.js"))
    if len(locale_sources) != 13 or not (SITE / "assets" / "locales" / "common-r4.js").is_file():
        raise RuntimeError("Legacy locale deployment boundary changed unexpectedly")

    agent_page = SITE / "playgrounds" / "agent-tool-context" / "index.html"
    if not agent_page.is_file():
        raise RuntimeError("Public Lab 14 page is missing")
    source = agent_page.read_text(encoding="utf-8")
    if "<script src=" in source or "fetch(" in source or "XMLHttpRequest" in source:
        raise RuntimeError("Public Lab 14 is not self-contained/offline")


def main() -> None:
    build_site()
    validate_boundary()
    base.validate_local_references()

    deployed_files = sorted(path for path in SITE.rglob("*") if path.is_file())
    if len(deployed_files) != 54:
        raise RuntimeError(f"Expected a 54-file minimal v1.3 Pages artifact, found {len(deployed_files)}")

    print(f"Built minimal v1.3 Pages artifact: {len(deployed_files)} files")
    print("Deployment boundary: PASS")
    for path in deployed_files:
        print(f"  {path.relative_to(SITE)}")


if __name__ == "__main__":
    main()
