#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from build_agent_tool_context_multilingual_candidate import build as build_multilingual, load_catalogs

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "_site" / "playgrounds" / "agent-tool-context" / "index.html"
CANONICAL = "https://lmdixon23.github.io/ai-playgrounds/playgrounds/agent-tool-context/"
PUBLIC_BADGE = "AI Playgrounds v1.3"
R6_BROWSER_FREEZE = "07f89d13269041d9ed66de2362bf84c288bb86de"

PUBLIC_SUBTITLE = {
    "en": "Inspect the boundary between model output, a structured tool call, runtime validation, authorization, deterministic execution, returned observation, context update, and stopping. Every executable transition is produced by the frozen deterministic teaching policy and in-memory tool world.",
    "zh": "检查模型输出、结构化工具调用、运行时验证、授权、确定性执行、返回观察、上下文更新与停止之间的边界。所有可执行转换均由冻结的确定性教学策略和内存工具环境产生。",
    "vi": "Quan sát ranh giới giữa đầu ra của mô hình, lệnh gọi công cụ có cấu trúc, xác thực khi chạy, phân quyền, thực thi xác định, quan sát trả về, cập nhật ngữ cảnh và dừng. Mọi chuyển trạng thái có thể thực thi đều do chính sách giảng dạy xác định đã đóng băng và môi trường công cụ trong bộ nhớ tạo ra.",
    "es": "Examina la frontera entre la salida del modelo, una llamada estructurada a herramienta, la validación en tiempo de ejecución, la autorización, la ejecución determinista, la observación devuelta, la actualización del contexto y la detención. Cada transición ejecutable procede de la política didáctica determinista congelada y del entorno de herramientas en memoria.",
}

HEAD = f"""
<meta name="description" content="Trace a deterministic agent loop through structured tool calls, validation, authorization, execution, observations, context updates, and stopping.">
<link rel="canonical" href="{CANONICAL}">
<link rel="alternate" hreflang="en" href="{CANONICAL}?lang=en">
<link rel="alternate" hreflang="zh-Hans" href="{CANONICAL}?lang=zh">
<link rel="alternate" hreflang="vi" href="{CANONICAL}?lang=vi">
<link rel="alternate" hreflang="es" href="{CANONICAL}?lang=es">
<link rel="alternate" hreflang="x-default" href="{CANONICAL}?lang=en">
<meta property="og:type" content="website">
<meta property="og:url" content="{CANONICAL}">
<meta property="og:title" content="Agent Tool Use and Context Protocols | AI Playgrounds">
<meta property="og:description" content="Inspect a deterministic agent runtime from proposed actions through validation, authorization, execution, observations, context updates, and stopping.">
<meta property="og:image" content="https://lmdixon23.github.io/ai-playgrounds/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Agent Tool Use and Context Protocols | AI Playgrounds">
<meta name="twitter:description" content="Trace deterministic tool use, provenance-aware context, and stop decisions across a transparent agent runtime.">
<style id="lab14-public-shell">
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
        "<title>Agent Tool Use and Context Protocols — Lab 14 English Candidate</title>",
        "<title>Agent Tool Use and Context Protocols | AI Playgrounds</title>",
        1,
    )

    for locale in ("en", "zh", "vi", "es"):
        html = html.replace(str(catalogs[locale]["page.subtitle"]), PUBLIC_SUBTITLE[locale])
        html = html.replace(str(catalogs[locale]["page.badge"]), PUBLIC_BADGE)

    html = html.replace("non-public v1.3 four-locale candidate", PUBLIC_BADGE)
    html = html.replace("</head>", HEAD + "\n</head>", 1)
    html = html.replace(
        "<main>\n",
        '<main>\n  <a class="suite-back" href="../../index.html">← AI Playgrounds</a>\n',
        1,
    )
    html = html.replace(
        "document.title=`${CATALOGS[active]['page.title']} — Lab 14`;",
        "document.title=`${CATALOGS[active]['page.title']} | AI Playgrounds`;",
    )

    forbidden = (
        "English source candidate:",
        "non-public v1.3",
        "R6 candidate",
    )
    remaining = [phrase for phrase in forbidden if phrase in html]
    if remaining:
        raise RuntimeError(f"Public Lab 14 still contains candidate wording: {remaining}")
    if 'href="../../index.html"' not in html or CANONICAL not in html:
        raise RuntimeError("Public Lab 14 shell metadata/back route was not installed")
    if "fetch(" in html or "XMLHttpRequest" in html or "<script src=" in html:
        raise RuntimeError("Public Lab 14 must remain one-file and network-independent")
    if R6_BROWSER_FREEZE == "":
        raise RuntimeError("R6 browser freeze must be bound before public integration")

    output.write_text(html, encoding="utf-8")
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    result = build_public(output)
    print(f"Built public Lab 14: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
