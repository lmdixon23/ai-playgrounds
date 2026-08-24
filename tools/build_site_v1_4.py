#!/usr/bin/env python3
from __future__ import annotations

from html import escape
from pathlib import Path

import build_site as base
import build_site_v1_3 as v13
from build_agent_tool_context_public_v1_4 import build_public as build_agent_v14
from build_transformer_public_v1_4 import build_public as build_transformer_v14

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
RELEASE_VERSION = "1.4.0"

SELECT_STYLE = r'''
<style id="v14-language-select-style">
.v14-language-select{min-height:38px;padding:6px 32px 6px 10px;border:1px solid var(--border,#cbd5e1);border-radius:8px;background:var(--card,#fff);color:inherit;font:inherit;cursor:pointer}
.v14-language-select:focus-visible{outline:3px solid color-mix(in srgb,var(--accent,#2563eb) 45%,transparent);outline-offset:2px}
.support-language-switch button[data-support-lang],.lang button[data-lang]{display:none!important}
@media(pointer:coarse){.v14-language-select{min-height:44px}}
</style>
'''

VERSION_STYLE = r'''
<style id="v14-version-provenance-style">
.v14-version-provenance{max-width:1180px;margin:22px auto 10px;padding:12px 18px;border-top:1px solid var(--border,#dbe4ee);color:var(--muted,#64748b);font:12px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;text-align:center}
.v14-release-zh{display:none}html[lang^="zh"] .v14-release-en{display:none}html[lang^="zh"] .v14-release-zh{display:inline}
</style>
'''

SUPPORT_SELECT_SCRIPT = r'''
<script id="v14-support-language-select">
(()=>{'use strict';
const root=document.querySelector('.support-language-switch');if(!root||root.querySelector('.v14-language-select'))return;
const buttons=[...root.querySelectorAll('button[data-support-lang]')];if(!buttons.length)return;
const names={en:'English',zh:'简体中文',vi:'Tiếng Việt',es:'Español'};
const select=document.createElement('select');select.className='v14-language-select';select.setAttribute('aria-label','Language / 语言');
for(const button of buttons){const code=button.dataset.supportLang,option=document.createElement('option');option.value=code;option.textContent=names[code]||button.textContent.trim()||code;select.appendChild(option)}
const current=buttons.find(button=>button.getAttribute('aria-pressed')==='true');select.value=current?current.dataset.supportLang:buttons[0].dataset.supportLang;
select.addEventListener('change',()=>{if(window.setSupportLanguage)window.setSupportLanguage(select.value,true);else buttons.find(button=>button.dataset.supportLang===select.value)?.click()});
document.addEventListener('supportlanguagechange',event=>{if(event.detail&&event.detail.language)select.value=event.detail.language});root.appendChild(select);
})();
</script>
'''

LANDING_SELECT_SCRIPT = r'''
<script id="v14-landing-language-select">
(()=>{'use strict';
const root=document.querySelector('.lang');if(!root||root.querySelector('.v14-language-select'))return;
const buttons=[...root.querySelectorAll('button[data-lang]')];if(!buttons.length)return;
const names={en:'English',zh:'简体中文',vi:'Tiếng Việt',es:'Español'};
const select=document.createElement('select');select.className='v14-language-select';select.setAttribute('aria-label','Language / 语言');
for(const button of buttons){const code=button.dataset.lang,option=document.createElement('option');option.value=code;option.textContent=names[code]||button.textContent.trim()||code;select.appendChild(option)}
function sync(){const current=buttons.find(button=>button.classList.contains('active'));select.value=current?current.dataset.lang:buttons[0].dataset.lang}
sync();select.addEventListener('change',()=>{buttons.find(button=>button.dataset.lang===select.value)?.click();queueMicrotask(sync)});root.appendChild(select);
})();
</script>
'''

TRACK_STYLE = r'''
<style id="v14-curriculum-track-style">
.v14-track-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin:18px 0}.v14-track-card{background:var(--card);border:1px solid var(--border);border-radius:18px;padding:20px}.v14-track-card.foundation{border-top:4px solid #2563eb}.v14-track-card.extension{border-top:4px solid #0f766e}.v14-track-card h3{margin:.1rem 0 .45rem}.v14-track-card p{margin:.35rem 0}.v14-track-tag{display:inline-flex;padding:3px 8px;border:1px solid var(--border);border-radius:999px;font-size:.74rem;font-weight:800;color:var(--muted)}.v14-zh{display:none}html[lang^="zh"] .v14-en{display:none}html[lang^="zh"] .v14-zh{display:inline}html[lang^="zh"] .v14-zh.v14-block{display:block}@media(max-width:680px){.v14-track-grid{grid-template-columns:1fr}}
</style>
'''

MODERN_SECTION = r'''
<section id="modern-extensions" aria-labelledby="v14-modern-title">
  <h2 id="v14-modern-title"><span class="v14-en">Modern AI extensions</span><span class="v14-zh">现代 AI 扩展</span></h2>
  <p><span class="v14-en">These labs extend the course-facing foundations into contemporary AI systems. They are optional extensions, not prerequisites for the classical introductory sequence.</span><span class="v14-zh">这些实验把面向课程的基础内容延伸到当代 AI 系统。它们属于可选扩展，而不是经典入门序列的先修要求。</span></p>
  <div class="v14-track-grid">
    <article class="v14-track-card foundation">
      <span class="v14-track-tag"><span class="v14-en">Course boundary</span><span class="v14-zh">课程边界</span></span>
      <h3><a href="playgrounds/transformer-language-model/index.html">Transformer Language Modeling</a></h3>
      <p><span class="v14-en">A bridge between advanced introductory NLP and modern generative language models: inspect causal self-attention and exact next-token probabilities.</span><span class="v14-zh">连接高级入门 NLP 与现代生成式语言模型：检查因果自注意力与精确的下一词元概率。</span></p>
    </article>
    <article class="v14-track-card extension">
      <span class="v14-track-tag"><span class="v14-en">Modern extension</span><span class="v14-zh">现代扩展</span></span>
      <h3><a href="playgrounds/agent-tool-context/index.html">Agent Tool Use and Context Protocols</a></h3>
      <p><span class="v14-en">Go beyond the traditional introductory backbone to inspect tool schemas, authorization, execution, observations, provenance-aware context, and stopping.</span><span class="v14-zh">超出传统入门课程主干，检查工具模式、授权、执行、观察、带来源信息的上下文与停止决策。</span></p>
    </article>
  </div>
</section>
'''

LAB14_COURSE_ROW = (
    '<tr style="--applet-accent:#0f766e"><td data-label="#"><span class="order-dot">14</span></td>'
    '<td data-label="Applet"><a href="playgrounds/agent-tool-context/index.html">Agent Tool Use and Context Protocols</a></td>'
    '<td data-label="Concept area">Agent systems and tool protocols</td>'
    '<td data-label="Why here">Connect goal-directed action selection with schemas, authorization, observations, provenance-aware context updates, and correct stopping.</td></tr>'
)
LAB14_LEGEND = '<span style="--legend:#0f766e"><i></i>Agent Tool Use and Context Protocols</span>'


def insert_before_last(html: str, marker: str, fragment: str) -> str:
    index = html.rfind(marker)
    if index < 0:
        raise RuntimeError(f"Could not locate final {marker} marker")
    return html[:index] + fragment + html[index:]


def upgrade_landing() -> None:
    path = SITE / "index.html"
    html = path.read_text(encoding="utf-8")
    html = html.replace("AI Playgrounds | Fourteen interactive foundations of AI", "AI Playgrounds | Fourteen interactive AI labs")
    html = html.replace("AI Playgrounds: fourteen multilingual interactives for foundational artificial intelligence", "AI Playgrounds: fourteen multilingual AI labs from foundations to modern extensions")
    html = html.replace("Fourteen multilingual, offline-ready interactives for foundational artificial intelligence.", "Fourteen multilingual, offline-ready AI labs spanning foundations and modern extensions.")
    html = html.replace('"version": "1.3.0"', f'"version": "{RELEASE_VERSION}"')
    if 'name="ai-playgrounds-version"' not in html:
        html = html.replace("</head>", f'<meta name="ai-playgrounds-version" content="{RELEASE_VERSION}">\n' + SELECT_STYLE + "\n</head>", 1)
    elif 'id="v14-language-select-style"' not in html:
        html = html.replace("</head>", SELECT_STYLE + "\n</head>", 1)
    html = html.replace(
        '· <a data-t="footerPortfolio"',
        f'· <span class="site-version">v{RELEASE_VERSION}</span> · <a data-t="footerPortfolio"',
        1,
    )
    html = html.replace("</body>", LANDING_SELECT_SCRIPT + "\n</body>", 1)
    path.write_text(html, encoding="utf-8")


def upgrade_support_pages() -> None:
    for path in sorted(SITE.rglob("*.html")):
        if path == SITE / "index.html" or "playgrounds" in path.parts:
            continue
        html = path.read_text(encoding="utf-8")
        if "support-language-switch" not in html:
            continue
        if 'id="v14-language-select-style"' not in html:
            html = html.replace("</head>", SELECT_STYLE + "\n" + VERSION_STYLE + "\n</head>", 1)
        if 'id="v14-support-language-select"' not in html:
            html = html.replace("</body>", SUPPORT_SELECT_SCRIPT + "\n</body>", 1)
        if "data-v14-support-version" not in html and "</footer>" in html:
            html = html.replace("</footer>", f'<p data-v14-support-version="true">AI Playgrounds · v{RELEASE_VERSION}</p>\n</footer>', 1)
        path.write_text(html, encoding="utf-8")


def bilingual(en: object, zh: object) -> str:
    return f'<span class="v14-en">{escape(str(en))}</span><span class="v14-zh">{escape(str(zh))}</span>'


def render_complete_applet_map() -> str:
    cards: list[str] = []
    for entry in sorted(v13.release_manifest(), key=lambda item: int(item.get("course_order", 999))):
        slug = escape(str(entry["slug"]), quote=True)
        accent = escape(str(entry.get("accent", "#2563eb")), quote=True)
        icon = escape(str(entry.get("icon", "•")))
        title_en = entry.get("title", slug)
        title_zh = entry.get("title_zh", title_en)
        desc_en = entry.get("desc", "")
        desc_zh = entry.get("desc_zh", desc_en)
        category_en = entry.get("category_en", entry.get("course_phase", "AI"))
        category_zh = entry.get("category_zh", category_en)
        time = escape(str(entry.get("time", "")))
        level = escape(str(entry.get("level", "")))
        cards.append(
            f'<article class="applet-card" style="--applet-accent:{accent}">'
            f'<div class="card-head"><span class="card-icon">{icon}</span><span class="phase">{bilingual(category_en, category_zh)}</span></div>'
            f'<h3><a href="playgrounds/{slug}/index.html">{bilingual(title_en, title_zh)}</a></h3>'
            f'<p>{bilingual(desc_en, desc_zh)}</p>'
            f'<p class="tiny">{time} · {level}</p>'
            '</article>'
        )
    return ''.join(cards)


def transform_curriculum_tracks() -> None:
    path = SITE / "curriculum.html"
    html = path.read_text(encoding="utf-8")
    html = html.replace(LAB14_COURSE_ROW, "")
    html = html.replace(LAB14_LEGEND, "")
    html = html.replace(
        "Course and AIMA-aligned applet sequence",
        '<span class="v14-en">Foundations / course track</span><span class="v14-zh">基础 / 课程路径</span>',
        1,
    )
    anchor = "<section><h2>Applet map</h2>"
    if anchor not in html:
        raise RuntimeError("Could not locate curriculum applet-map anchor for v1.4 track split")
    html = html.replace(anchor, MODERN_SECTION + "\n" + anchor, 1)

    map_section = html.index(anchor)
    grid_anchor = '<div class="applet-grid">'
    grid_start = html.index(grid_anchor, map_section)
    section_end = html.index("</section>", grid_start)
    html = html[:grid_start] + grid_anchor + render_complete_applet_map() + "</div>" + html[section_end:]

    if 'id="v14-curriculum-track-style"' not in html:
        html = html.replace("</head>", TRACK_STYLE + "\n</head>", 1)
    if html.count('class="order-dot"') != 13:
        raise RuntimeError("v1.4 foundations/course table must contain thirteen rows; Lab 14 belongs to Modern Extensions")
    if html.count('class="applet-card"') != 14:
        raise RuntimeError("v1.4 curriculum applet map must contain all fourteen public applets")
    if "modern-extensions" not in html or "Agent Tool Use and Context Protocols" not in html:
        raise RuntimeError("v1.4 curriculum track split did not complete")
    path.write_text(html, encoding="utf-8")


def transform_release_notes_v14() -> None:
    path = SITE / "release-notes.html"
    html = path.read_text(encoding="utf-8")
    banner = (
        '<section id="release-v1-4-0" style="margin:1rem 0;padding:1rem 1.2rem;border:1px solid currentColor;border-radius:12px">'
        '<h2><span class="v14-release-en">AI Playgrounds v1.4.0, released August 25, 2026.</span><span class="v14-release-zh">AI Playgrounds v1.4.0，发布于 2026 年 8 月 25 日。</span></h2>'
        '<p><span class="v14-release-en">v1.4 keeps fourteen public applets and improves the Transformer and agent-runtime visual journeys, language selectors, curriculum navigation, and visible release provenance before Lab 15.</span><span class="v14-release-zh">v1.4 保留十四个公开 applet，并在 Lab 15 之前改进 Transformer 与智能体运行时的可视路径、语言选择器、课程导航和可见的版本来源信息。</span></p>'
        '</section>'
    )
    if "release-v1-4-0" not in html:
        marker = '<section id="release-v1-3-0"'
        if marker not in html:
            raise RuntimeError("Could not locate v1.3 release banner for v1.4 insertion")
        html = html.replace(marker, banner + marker, 1)
    path.write_text(html, encoding="utf-8")


def add_release_version_presentation() -> None:
    for path in sorted((SITE / "playgrounds").glob("*/index.html")):
        html = path.read_text(encoding="utf-8")
        if 'name="ai-playgrounds-version"' not in html:
            html = html.replace("</head>", f'<meta name="ai-playgrounds-version" content="{RELEASE_VERSION}">\n</head>', 1)
        if path.parent.name not in {"transformer-language-model", "agent-tool-context"}:
            if 'id="v14-version-provenance-style"' not in html:
                html = html.replace("</head>", VERSION_STYLE + "\n</head>", 1)
            if "data-v14-version-provenance" not in html:
                fragment = f'<div class="v14-version-provenance" data-v14-version-provenance="true" role="contentinfo">AI Playgrounds · v{RELEASE_VERSION}</div>\n'
                html = insert_before_last(html, "</body>", fragment)
        path.write_text(html, encoding="utf-8")


def build_site() -> None:
    v13.build_site()
    build_transformer_v14(SITE / "playgrounds" / "transformer-language-model" / "index.html")
    build_agent_v14(SITE / "playgrounds" / "agent-tool-context" / "index.html")
    upgrade_landing()
    upgrade_support_pages()
    transform_curriculum_tracks()
    transform_release_notes_v14()
    add_release_version_presentation()


def validate_boundary() -> None:
    v13.validate_boundary()
    base.validate_local_references()
    manifest = v13.release_manifest()
    expected = {str(entry["slug"]) for entry in manifest}
    deployed_paths = sorted((SITE / "playgrounds").glob("*/index.html"))
    deployed = {path.parent.name for path in deployed_paths}
    if deployed != expected or len(deployed) != 14:
        raise RuntimeError("v1.4 must preserve the exact fourteen-app v1.3 inventory")
    lab13 = (SITE / "playgrounds" / "transformer-language-model" / "index.html").read_text(encoding="utf-8")
    lab14 = (SITE / "playgrounds" / "agent-tool-context" / "index.html").read_text(encoding="utf-8")
    if "Lab13V14Experience" not in lab13 or "Lab14V14Experience" not in lab14:
        raise RuntimeError("v1.4 engagement wrappers are not present in the deployed Labs 13/14")
    if "AI Playgrounds v1.3" in lab13 or "AI Playgrounds v1.3" in lab14:
        raise RuntimeError("v1.4 public Labs 13/14 retain a prominent v1.3 badge")
    for path in deployed_paths:
        source = path.read_text(encoding="utf-8")
        if f'name="ai-playgrounds-version" content="{RELEASE_VERSION}"' not in source:
            raise RuntimeError(f"Missing v1.4 version metadata: {path.parent.name}")
        if path.parent.name in {"transformer-language-model", "agent-tool-context"}:
            if f"v{RELEASE_VERSION}" not in source:
                raise RuntimeError(f"Missing visible v1.4 provenance: {path.parent.name}")
        elif "data-v14-version-provenance" not in source:
            raise RuntimeError(f"Missing visible v1.4 provenance: {path.parent.name}")
    if "release-v1-4-0" not in (SITE / "release-notes.html").read_text(encoding="utf-8"):
        raise RuntimeError("Public release notes lack the v1.4 release banner")


def main() -> None:
    build_site()
    validate_boundary()
    files = sorted(path for path in SITE.rglob("*") if path.is_file())
    if len(files) != 54:
        raise RuntimeError(f"Expected a 54-file minimal v1.4 Pages artifact, found {len(files)}")
    print(f"Built minimal v1.4 Pages candidate: {len(files)} files / 14 applets")
    print("v1.4 product-quality deployment boundary: PASS")


if __name__ == "__main__":
    main()
