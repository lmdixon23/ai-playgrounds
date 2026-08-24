#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from build_transformer_multilingual_candidate import build as build_multilingual, load_catalogs

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "_site" / "playgrounds" / "transformer-language-model" / "index.html"
CANONICAL = "https://lmdixon23.github.io/ai-playgrounds/playgrounds/transformer-language-model/"
PUBLIC_BADGE = "AI Playgrounds v1.2"

HEAD = f"""
<meta name="description" content="Trace toy tokens through position-aware causal self-attention to exact next-token probabilities in a deterministic, offline Transformer language-model lab.">
<link rel="canonical" href="{CANONICAL}">
<link rel="alternate" hreflang="en" href="{CANONICAL}?lang=en">
<link rel="alternate" hreflang="zh-Hans" href="{CANONICAL}?lang=zh">
<link rel="alternate" hreflang="vi" href="{CANONICAL}?lang=vi">
<link rel="alternate" hreflang="es" href="{CANONICAL}?lang=es">
<link rel="alternate" hreflang="x-default" href="{CANONICAL}?lang=en">
<meta property="og:type" content="website">
<meta property="og:url" content="{CANONICAL}">
<meta property="og:title" content="Transformer Language Modeling | AI Playgrounds">
<meta property="og:description" content="Inspect token representations, causal self-attention, logits, and next-token probabilities in a deterministic teaching model.">
<meta property="og:image" content="https://lmdixon23.github.io/ai-playgrounds/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Transformer Language Modeling | AI Playgrounds">
<meta name="twitter:description" content="Inspect a deterministic Transformer language-model mechanism from tokens to next-token probabilities.">
<style id="lab13-public-shell">
.suite-back{{display:inline-flex;margin:0 0 14px;color:var(--accent);font-weight:750;text-decoration:none}}
.suite-back:focus-visible{{outline:3px solid color-mix(in srgb,var(--accent) 55%,transparent);outline-offset:3px}}
</style>
"""


def build_public(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    build_multilingual(output)
    html = output.read_text(encoding="utf-8")
    catalogs = load_catalogs()

    html = html.replace(
        "<title>Transformer Language Modeling — Lab 13 English Candidate</title>",
        "<title>Transformer Language Modeling | AI Playgrounds</title>",
        1,
    )
    english_source_subtitle = (
        "English source candidate: trace a tiny deterministic decoder-like block from "
        "toy tokens to causal self-attention to next-token probabilities. Every displayed "
        "number is computed locally from fixed teaching weights."
    )
    html = html.replace(english_source_subtitle, catalogs["en"]["page.subtitle"])

    # A release badge is locale-neutral. Replacing all catalog variants prevents a
    # locale switch from reintroducing the earlier non-public candidate wording.
    for locale in ("en", "zh", "vi", "es"):
        html = html.replace(str(catalogs[locale]["page.badge"]), PUBLIC_BADGE)

    html = html.replace("</head>", HEAD + "\n</head>", 1)
    html = html.replace(
        "<main>\n  <div class=\"top\">",
        '<main>\n  <a class="suite-back" href="../../index.html">← AI Playgrounds</a>\n  <div class="top">',
        1,
    )
    html = html.replace(
        "document.title=`${CATALOGS[active]['page.title']} — Lab 13`;",
        "document.title=`${CATALOGS[active]['page.title']} | AI Playgrounds`;",
    )
    html = html.replace(
        "setLocale('en');\n})();",
        "const requested=new URLSearchParams(location.search).get('lang');\n"
        "setLocale(LOCALES.includes(requested)?requested:'en');\n})();",
        1,
    )

    forbidden = (
        "English source candidate:",
        "non-public v1.2 candidate",
        "v1.2 非公开候选版本",
        "ứng viên v1.2 chưa công khai",
        "candidato v1.2 no público",
    )
    remaining = [phrase for phrase in forbidden if phrase in html]
    if remaining:
        raise RuntimeError(f"Public Lab 13 still contains candidate wording: {remaining}")
    if 'href="../../index.html"' not in html or CANONICAL not in html:
        raise RuntimeError("Public Lab 13 shell metadata/back route was not installed")
    if "fetch(" in html or "XMLHttpRequest" in html or "<script src=" in html:
        raise RuntimeError("Public Lab 13 must remain one-file and network-independent")

    output.write_text(html, encoding="utf-8")
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    result = build_public(output)
    print(f"Built public Lab 13: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
