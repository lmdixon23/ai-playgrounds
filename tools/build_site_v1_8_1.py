#!/usr/bin/env python3
from __future__ import annotations

"""Compose the v1.8.1 learner-facing parity release.

The v1.8.0 mechanism implementations remain unchanged. This successor adds
the scenario-led teaching sequence used by the first twelve applets, aligns the
modern header controls, removes duplicated state prose, and fixes dark-theme
surfaces in Labs 13-15.
"""

import html as html_lib
import json
import re
import shutil

import build_site as core
import build_site_v1_8 as base
from modern_learning_v1_8_1 import COMMON, LABS, LOCALES


ROOT = base.ROOT
SITE = base.SITE
MODERN = tuple(LABS)
CURRENT = "v1.8.1"
VERSION = "1.8.1"


STYLE = r'''<style id="v181-modern-learner-parity-style">
.ap-standard-header .header-prefs{gap:8px}
.ap-standard-header .header-theme,.ap-standard-header .header-png,.ap-standard-header .header-reset,.ap-standard-header .header-more>summary{min-height:38px;display:inline-flex;align-items:center;justify-content:center;gap:5px;padding:7px 10px;border:1px solid var(--border);border-radius:8px;background:var(--card);color:var(--fg);font:inherit;cursor:pointer}
.ap-standard-header .header-actions{align-items:center}.ap-standard-header .header-reset{margin-left:4px}
.ap-standard-header .modern-lang-switch{display:inline-flex;align-items:center;overflow:hidden;border:1px solid var(--border);border-radius:8px;background:var(--card)}
.ap-standard-header .modern-lang-switch label{padding:0 0 0 9px;color:var(--muted);font-size:.78rem;font-weight:700;white-space:nowrap}
.ap-standard-header .modern-lang-switch select{min-height:36px;border:0!important;border-radius:0!important;background:var(--card);color:var(--fg);padding:6px 9px}
.ap-modern-curriculum{max-width:980px;margin:22px auto 0;padding:0 20px;color:var(--fg);font:15px/1.6 system-ui,-apple-system,sans-serif}
.ap-modern-curriculum details{margin:12px 0}
.ap-modern-curriculum details>summary{cursor:pointer;padding:10px 12px;background:var(--card);border:1px solid var(--border);border-left:4px solid color-mix(in srgb,var(--accent) 62%,var(--border));border-radius:10px;color:var(--fg);font-weight:800}
.ap-modern-featured-body,.scenario-gallery-panel{padding:16px;background:var(--card);border:1px solid var(--border);border-top:0;border-radius:0 0 10px 10px}
.ap-modern-featured-body>strong{display:block;font-size:1.08rem;color:var(--accent);margin-bottom:7px}
.ap-modern-featured-body p{margin:7px 0}
.featured-actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}
.scenario-gallery-intro{margin:0 0 12px;color:var(--muted)}
.scenario-card-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.scenario-card{min-width:0;padding:15px;border:1px solid var(--border);border-radius:10px;background:color-mix(in srgb,var(--card) 97%,var(--accent));box-shadow:0 6px 18px rgba(15,23,42,.05)}
.scenario-card.applied{border-color:var(--accent);box-shadow:0 0 0 2px color-mix(in srgb,var(--accent) 22%,transparent)}
.scenario-card h3{margin:0 0 9px;font-size:1rem;color:var(--fg)}
.scenario-card .scenario-meta{margin:7px 0;line-height:1.5;color:var(--fg)}
.scenario-card .scenario-meta strong{display:block;color:var(--fg);margin-bottom:2px}
.scenario-card button,.featured-actions button{border:0;border-radius:8px;background:var(--accent);color:#fff;font-weight:750;padding:8px 11px;cursor:pointer}
.ap-modern-jump{text-align:center;margin:17px 0 8px}
.ap-modern-jump .jump-link{display:inline-block;padding:7px 14px;border:1px solid var(--border);border-radius:999px;background:var(--card);color:var(--accent);text-decoration:none;font-weight:700;font-size:.84rem}
.ap-modern-essay{max-width:760px;margin:0 auto;padding:30px 0 54px;font-size:1.03rem}
.ap-modern-essay h2{font-size:1.45rem;margin:34px 0 11px;color:var(--accent)}
.ap-modern-essay p{margin:0 0 14px}
.essay-primer{margin:0 0 24px;padding:16px 18px;border-left:4px solid var(--accent);background:color-mix(in srgb,var(--card) 96%,var(--accent));border-radius:10px}
.essay-primer h2{margin:0 0 7px;font-size:1.08rem}
.essay-primer h3{margin:14px 0 8px;font-size:.95rem}
.essay-primer-terms{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin:0}
.essay-primer-terms>div{padding:9px 10px;border:1px solid var(--border);border-radius:8px;background:var(--card)}
.essay-primer-terms dt{font-weight:800;color:var(--fg)}
.essay-primer-terms dd{margin:2px 0 0;color:var(--muted);font-size:.83rem;line-height:1.45}
.for-teachers{background:var(--soft);border:1px solid var(--border);border-radius:10px;padding:20px 22px;margin-top:34px;font-size:.94rem}
.for-teachers h2{margin:0 0 10px;font-size:1.05rem;text-transform:uppercase;letter-spacing:.04em}
.for-teachers h3{font-size:.95rem;margin:16px 0 6px;color:var(--fg)}
.for-teachers ul{margin:5px 0;padding-left:22px}.for-teachers li{margin:5px 0}
.ap-modern-a11y-compact .ap-support-body{padding:13px;color:var(--muted)}
.ap-modern-a11y-compact a{color:var(--accent);font-weight:700}
.ap-modern-back-controls{margin-top:24px}
body.embed-mode .ap-modern-curriculum{display:none!important}
body.ap-standard-dark{--good:#6ee7b7;--warn:#fdba74;--bad:#fca5a5}
body.ap-standard-dark[data-ap-modern-parity="transformer-language-model"]{--accent:#c4b5fd;--accent-strong:#6d28d9}
body.ap-standard-dark[data-ap-modern-parity="agent-tool-context"]{--accent:#5eead4;--accent-strong:#0f766e}
body.ap-standard-dark[data-ap-modern-parity="minimax-alpha-beta"]{--accent:#93c5fd;--accent-strong:#1d4ed8}
body.ap-standard-dark button.primary,body.ap-standard-dark .action.primary,body.ap-standard-dark .scenario-card button,body.ap-standard-dark .featured-actions button{background:var(--accent-strong)!important;color:#fff!important}
body.ap-standard-dark .boundary{background:#292244!important;border-color:#5b4c88!important;color:var(--fg)!important}
body.ap-standard-dark .warning{background:#3b2a16!important;border-color:#854d0e!important;color:#fed7aa!important}
body.ap-standard-dark .matrix td.masked{background:#263348!important;color:#cbd5e1!important}
body.ap-standard-dark .stage.good{border-color:#059669!important}body.ap-standard-dark .stage.warn{border-color:#c2410c!important}body.ap-standard-dark .stage.bad{border-color:#be123c!important}
body.ap-standard-dark .pill.good{border-color:#059669!important}body.ap-standard-dark .pill.warn{border-color:#c2410c!important}body.ap-standard-dark .pill.bad{border-color:#be123c!important}
body.ap-standard-dark .control select,body.ap-standard-dark .control input{background:var(--card)!important;color:var(--fg)!important}
body.ap-standard-dark .tree-wrap{background:linear-gradient(180deg,#111827,#172033)!important}
body.ap-standard-dark .edge{stroke:#64748b!important}
body.ap-standard-dark .node circle{fill:#172033!important;stroke:#94a3b8!important}
body.ap-standard-dark .node.visited circle{fill:#312e81!important}
body.ap-standard-dark .node.returned circle{fill:#064e3b!important;stroke:#6ee7b7!important}
body.ap-standard-dark .node.pruned circle{fill:#4c1d2b!important;stroke:#fda4af!important}
body.ap-standard-dark .metric,body.ap-standard-dark .trace-card,body.ap-standard-dark .baseline{background:var(--card)!important;color:var(--fg)!important}
body.ap-standard-dark .actual{background:#052e2b!important;border-color:#0f766e!important;color:var(--fg)!important}
@media(min-width:980px){.scenario-card-grid{grid-template-columns:repeat(3,minmax(0,1fr))}.scenario-card:last-child:nth-child(3n+2){grid-column:auto}}
@media(max-width:720px){.ap-standard-header .header-main{align-items:flex-start}.ap-standard-header .header-actions{grid-template-columns:repeat(2,minmax(0,1fr))!important}.ap-standard-header .header-actions>.header-png,.ap-standard-header .header-actions>.header-reset{width:100%;margin:0}.scenario-card-grid,.essay-primer-terms{grid-template-columns:1fr}.ap-modern-curriculum{padding:0 14px}.ap-modern-essay{padding-bottom:38px}}
@media(max-width:520px){.ap-standard-header .header-prefs{width:100%}.ap-standard-header .modern-lang-switch{flex:1;min-width:0}.ap-standard-header .modern-lang-switch select{min-width:0;width:100%}}
@media(pointer:coarse){.ap-standard-header .header-theme,.ap-standard-header .header-png,.ap-standard-header .header-reset,.ap-standard-header .header-more>summary,.scenario-card button,.featured-actions button{min-height:44px}}
@media(prefers-reduced-motion:reduce){.scenario-card{transition:none!important}.ap-modern-curriculum{scroll-behavior:auto!important}}
</style>'''


def esc(value: object) -> str:
    return html_lib.escape(str(value), quote=True)


def list_html(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{esc(item)}</li>" for item in items) + "</ul>"


def render_curriculum(slug: str) -> tuple[str, str]:
    lab = LABS[slug]
    copy = lab["copy"]["en"]
    common = COMMON["en"]
    featured_index = lab["featured"]
    featured = copy["scenarios"][featured_index]
    scenario_cards = []
    for index, item in enumerate(copy["scenarios"]):
        scenario_cards.append(
            f'''<article class="scenario-card" data-modern-scenario-card="{index}">
<h3>{esc(common["scenario"])} {index + 1}: {esc(item["title"])}</h3>
<p class="scenario-meta"><strong>{esc(common["core_question"])}:</strong> {esc(item["question"])}</p>
<p class="scenario-meta"><strong>{esc(common["run_watch"])}:</strong> {esc(item["run"])}</p>
<p class="scenario-meta"><strong>{esc(common["predict_first"])}:</strong> {esc(item["predict"])}</p>
<p class="scenario-meta"><strong>{esc(common["explain_after"])}:</strong> {esc(item["explain"])}</p>
<button type="button" data-modern-apply="{index}">{esc(common["apply"])}</button>
</article>'''
        )
    terms = "".join(
        f"<div><dt>{esc(term)}</dt><dd>{esc(definition)}</dd></div>"
        for term, definition in copy["terms"]
    )
    sections = "".join(
        f'<section><h2>{esc(heading)}</h2>{"".join(f"<p>{esc(paragraph)}</p>" for paragraph in paragraphs)}</section>'
        for heading, paragraphs in copy["sections"]
    )
    teacher = copy["teacher"]
    state_id = lab["state_id"]
    entry = f'''<section class="ap-modern-curriculum ap-modern-entry" id="ap-modern-learning" data-modern-learning="{esc(slug)}" aria-label="Learning sequence">
<details class="signature-challenge ap-modern-featured" open>
<summary>{esc(common["featured_summary"])}</summary>
<div class="ap-modern-featured-body"><strong>{esc(featured["title"])}</strong>
<p><b>{esc(common["core_question"])}:</b> {esc(featured["question"])}</p>
<p><em><b>{esc(common["run_watch"])}:</b> {esc(featured["run"])}</em></p>
<div class="featured-actions"><button type="button" data-modern-apply="{featured_index}">{esc(common["start_featured"])}</button></div></div>
</details>
<details class="scenario-gallery" open>
<summary>{esc(common["scenarios_summary"])}</summary>
<div class="scenario-gallery-panel"><p class="scenario-gallery-intro">{esc(common["scenarios_intro"])}</p>
<div class="scenario-card-grid" id="ap-modern-scenario-cards">{"".join(scenario_cards)}</div></div>
</details>
<div class="ap-modern-jump"><a class="jump-link" href="#essay">{esc(common["jump"])}</a></div>
 </section>'''
    explanation = f'''<section class="ap-modern-curriculum ap-modern-explanation" id="ap-modern-explanation">
<article class="essay ap-modern-essay" id="essay">
<section class="essay-primer"><h2>{esc(common["before"])}</h2><p>{esc(copy["primer"])}</p>
<h3>{esc(common["terms"])}</h3><dl class="essay-primer-terms">{terms}</dl></section>
{sections}
<section class="for-teachers"><h2>{esc(common["teachers"])}</h2>
<p><strong>{esc(common["curriculum"])}:</strong> {esc(teacher["curriculum"])}</p>
<h3>{esc(common["pre"])}</h3>{list_html(teacher["pre"])}
<h3>{esc(common["post"])}</h3>{list_html(teacher["post"])}
<p><strong>{esc(common["misconceptions"])}:</strong> {esc(teacher["misconceptions"])}</p></section>
<details id="ap-modern-a11y" class="accessibility-layer ap-modern-a11y-compact">
<summary>{esc(common["a11y_summary"])}</summary><div class="ap-support-body">
<h2 class="ap-modern-sr-only">{esc(common["a11y_title"])}</h2><p>{esc(common["a11y_intro"])}</p>
<p><a href="#{esc(state_id)}">{esc(common["state_link"])}</a></p><p>{esc(common["a11y_note"])}</p></div></details>
<p class="ap-modern-back-controls"><a href="#ap-modern-interactive-start">{esc(common["back_controls"])}</a></p>
</article></section>'''
    return entry, explanation


def runtime(slug: str) -> str:
    payload = json.dumps(
        {"common": COMMON, "copy": LABS[slug]["copy"], "settings": LABS[slug]["settings"], "featured": LABS[slug]["featured"]},
        ensure_ascii=False,
        separators=(",", ":"),
    ).replace("</", "<\\/")
    return f'''<script id="v181-modern-learner-parity-runtime">
(()=>{{'use strict';const DATA={payload};const root=document.getElementById('ap-modern-learning'),essayRoot=document.getElementById('ap-modern-explanation');if(!root||!essayRoot)return;
const norm=v=>{{v=String(v||'').toLowerCase();return v.startsWith('zh')?'zh':v.startsWith('vi')?'vi':v.startsWith('es')?'es':'en'}};
const locale=()=>norm(document.documentElement.lang);const E=v=>String(v??'').replace(/[&<>"']/g,ch=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[ch]));
function list(items){{return'<ul>'+items.map(x=>'<li>'+E(x)+'</li>').join('')+'</ul>'}}
function paint(){{const l=locale(),c=DATA.common[l]||DATA.common.en,d=DATA.copy[l]||DATA.copy.en,f=d.scenarios[DATA.featured];let cards='';d.scenarios.forEach((s,i)=>{{cards+='<article class="scenario-card" data-modern-scenario-card="'+i+'"><h3>'+E(c.scenario)+' '+(i+1)+': '+E(s.title)+'</h3><p class="scenario-meta"><strong>'+E(c.core_question)+':</strong> '+E(s.question)+'</p><p class="scenario-meta"><strong>'+E(c.run_watch)+':</strong> '+E(s.run)+'</p><p class="scenario-meta"><strong>'+E(c.predict_first)+':</strong> '+E(s.predict)+'</p><p class="scenario-meta"><strong>'+E(c.explain_after)+':</strong> '+E(s.explain)+'</p><button type="button" data-modern-apply="'+i+'">'+E(c.apply)+'</button></article>'}});let terms=d.terms.map(x=>'<div><dt>'+E(x[0])+'</dt><dd>'+E(x[1])+'</dd></div>').join('');let sections=d.sections.map(x=>'<section><h2>'+E(x[0])+'</h2>'+x[1].map(p=>'<p>'+E(p)+'</p>').join('')+'</section>').join('');const t=d.teacher;root.innerHTML='<details class="signature-challenge ap-modern-featured" open><summary>'+E(c.featured_summary)+'</summary><div class="ap-modern-featured-body"><strong>'+E(f.title)+'</strong><p><b>'+E(c.core_question)+':</b> '+E(f.question)+'</p><p><em><b>'+E(c.run_watch)+':</b> '+E(f.run)+'</em></p><div class="featured-actions"><button type="button" data-modern-apply="'+DATA.featured+'">'+E(c.start_featured)+'</button></div></div></details><details class="scenario-gallery" open><summary>'+E(c.scenarios_summary)+'</summary><div class="scenario-gallery-panel"><p class="scenario-gallery-intro">'+E(c.scenarios_intro)+'</p><div class="scenario-card-grid" id="ap-modern-scenario-cards">'+cards+'</div></div></details><div class="ap-modern-jump"><a class="jump-link" href="#essay">'+E(c.jump)+'</a></div><article class="essay ap-modern-essay" id="essay"><section class="essay-primer"><h2>'+E(c.before)+'</h2><p>'+E(d.primer)+'</p><h3>'+E(c.terms)+'</h3><dl class="essay-primer-terms">'+terms+'</dl></section>'+sections+'<section class="for-teachers"><h2>'+E(c.teachers)+'</h2><p><strong>'+E(c.curriculum)+':</strong> '+E(t.curriculum)+'</p><h3>'+E(c.pre)+'</h3>'+list(t.pre)+'<h3>'+E(c.post)+'</h3>'+list(t.post)+'<p><strong>'+E(c.misconceptions)+':</strong> '+E(t.misconceptions)+'</p></section><details id="ap-modern-a11y" class="accessibility-layer ap-modern-a11y-compact"><summary>'+E(c.a11y_summary)+'</summary><div class="ap-support-body"><h2 class="ap-modern-sr-only">'+E(c.a11y_title)+'</h2><p>'+E(c.a11y_intro)+'</p><p><a href="#{LABS[slug]["state_id"]}">'+E(c.state_link)+'</a></p><p>'+E(c.a11y_note)+'</p></div></details><p class="ap-modern-back-controls"><a href="#ap-modern-interactive-start">'+E(c.back_controls)+'</a></p></article>';const essay=root.querySelector('.ap-modern-essay');if(essay)essayRoot.replaceChildren(essay)}}
function apply(index){{index=Number(index);const settings=DATA.settings[index];if(!settings)return;for(const [id,value] of Object.entries(settings)){{const control=document.getElementById(id);if(!control)continue;control.value=String(value);control.dispatchEvent(new Event('change',{{bubbles:true}}))}}root.querySelectorAll('.scenario-card').forEach(x=>x.classList.toggle('applied',Number(x.dataset.modernScenarioCard)===index));const c=DATA.common[locale()]||DATA.common.en;const button=root.querySelector('.scenario-card[data-modern-scenario-card="'+index+'"] button');if(button){{button.textContent='✓ '+c.applied;setTimeout(()=>{{if(button.isConnected)button.textContent=c.apply}},1800)}}try{{const u=new URL(location.href);u.searchParams.set('scenario',String(index));u.searchParams.set('mode','explore');u.searchParams.set('lang',locale());u.searchParams.delete('featured');history.replaceState(null,'',u)}}catch(_e){{}}document.getElementById('ap-modern-interactive-start')?.scrollIntoView({{block:'start',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'}})}}
root.addEventListener('click',e=>{{const button=e.target.closest('[data-modern-apply]');if(!button)return;apply(button.dataset.modernApply)}});new MutationObserver(paint).observe(document.documentElement,{{attributes:true,attributeFilter:['lang']}});window.addEventListener('lab13localechange',paint);window.addEventListener('lab14localechange',paint);window.addEventListener('lab15localechange',paint);paint();try{{const p=new URL(location.href).searchParams,n=Number(p.get('scenario'));if(Number.isInteger(n)&&n>=0&&n<DATA.settings.length)setTimeout(()=>apply(n),0)}}catch(_e){{}}
}})();</script>'''


def patch_header(page: str, slug: str) -> str:
    replacements = {
        '<button id="ap-standard-theme"': '<button class="header-theme" id="ap-standard-theme"',
        '<button id="ap-modern-share"': '<button class="header-png" id="ap-modern-share"',
        '<button id="ap-standard-reset"': '<button class="header-reset" id="ap-standard-reset"',
        '<button id="ap-modern-embed"': '<button class="header-png" id="ap-modern-embed"',
        '<button id="ap-modern-settings-json"': '<button class="header-png" id="ap-modern-settings-json"',
        'class="header-more-summary"': 'class="header-more-summary header-png"',
    }
    for old, new in replacements.items():
        if old not in page:
            raise RuntimeError(f"Modern header marker missing for {slug}: {old}")
        page = page.replace(old, new, 1)
    more = re.compile(
        r'<details class="header-more" id="ap-modern-more">'
        r'<summary\b[^>]*>.*?</summary><div class="header-more-menu">(.*?)</div></details>',
        re.S,
    )
    page, count = more.subn(r"\1", page, count=1)
    if count != 1:
        raise RuntimeError(f"Modern secondary actions could not be exposed: {slug}")
    settings_attrs = (
        'data-ap-en="Current settings (.json)" data-ap-zh="当前设置（.json）" '
        'data-ap-vi="Cài đặt hiện tại (.json)" data-ap-es="Configuración actual (.json)"'
    )
    if settings_attrs not in page or '<span>Current settings (.json)</span>' not in page:
        raise RuntimeError(f"Modern settings action labels changed: {slug}")
    page = page.replace(
        settings_attrs,
        'data-ap-en="JSON" data-ap-zh="JSON" data-ap-vi="JSON" data-ap-es="JSON"',
        1,
    ).replace('<span>Current settings (.json)</span>', '<span>JSON</span>', 1)
    pattern = re.compile(r'(<label\b[^>]*\bfor="ap-standard-language-select"[^>]*>.*?</label>)(<select\b[^>]*\bid="ap-standard-language-select"[^>]*>.*?</select>)', re.S | re.I)
    page, count = pattern.subn(r'<div class="lang-switch modern-lang-switch">\1\2</div>', page, count=1)
    if count != 1:
        raise RuntimeError(f"Modern language control could not be normalized: {slug}")
    return page


def patch_quick_assign(page: str, slug: str) -> str:
    old_refresh = "function refresh(){if(!state)return;const value=String(source?.value||source?.textContent||'').trim();state.textContent=value||labels().empty}"
    new_refresh = "function refresh(){if(!state)return;const value=String(source?.value||source?.textContent||'').trim();state.textContent=value||labels().empty;state.dataset.qaStateReady='1'}"
    if old_refresh not in page:
        raise RuntimeError(f"Quick Assign refresh contract changed: {slug}")
    page = page.replace(old_refresh, new_refresh, 1)
    old_tail = "new MutationObserver(()=>setTimeout(refresh,0)).observe(document.documentElement,{attributes:true,attributeFilter:['lang']});refresh();"
    new_tail = "new MutationObserver(()=>{if(state?.dataset.qaStateReady==='1')setTimeout(refresh,0)}).observe(document.documentElement,{attributes:true,attributeFilter:['lang']});"
    if old_tail not in page:
        raise RuntimeError(f"Quick Assign eager-state marker changed: {slug}")
    return page.replace(old_tail, new_tail, 1)


def patch_modern_lab(slug: str) -> None:
    path = SITE / "playgrounds" / slug / "index.html"
    page = path.read_text(encoding="utf-8")
    if 'id="v181-modern-learner-parity-style"' in page:
        raise RuntimeError(f"v1.8.1 modern learner layer would be applied twice: {slug}")
    page = patch_header(page, slug)
    page = patch_quick_assign(page, slug)
    support_start = page.find('<section class="ap-modern-support"')
    footer_start = page.find('<footer class="ap-standard-footer ap-modern-rich-footer"', support_start)
    if not (0 <= support_start < footer_start):
        raise RuntimeError(f"Modern support/footer boundary missing: {slug}")
    page = page[:support_start] + page[footer_start:]
    entry, explanation = render_curriculum(slug)
    qa = re.search(r'<details\b[^>]*\bdata-quick-assign-id\s*=', page, flags=re.I)
    if qa is None:
        raise RuntimeError(f"Quick Assign insertion boundary missing: {slug}")
    qa_end = page.find("</details>", qa.start())
    if qa_end < 0 or page.count("<details", qa.start(), qa_end) != 1:
        raise RuntimeError(f"Quick Assign structural boundary is ambiguous: {slug}")
    qa_end += len("</details>")
    page = (
        page[:qa.start()] + entry + "\n" + page[qa.start():qa_end]
        + "\n" + explanation + page[qa_end:]
    )
    head_close = page.lower().find("</head>", page.lower().find("<head"))
    body_close = page.lower().rfind("</body>")
    if head_close < 0 or body_close < 0:
        raise RuntimeError(f"Complete document boundary missing: {slug}")
    page = page[:head_close] + STYLE + "\n" + page[head_close:]
    body_close = page.lower().rfind("</body>")
    page = page[:body_close] + runtime(slug) + "\n" + page[body_close:]
    path.write_text(page, encoding="utf-8")


def patch_release_identity() -> None:
    for path in sorted(SITE.rglob("*.html")):
        page = path.read_text(encoding="utf-8")
        if path.name != "release-notes.html":
            page = page.replace("v1.8.0", CURRENT)
            page = page.replace('content="1.8.0"', 'content="1.8.1"')
        page = re.sub(r'data-ai-playgrounds-analytics="v\d+\.\d+\.\d+"', 'data-ai-playgrounds-analytics="v1.8.1"', page)
        page = re.sub(r'(<p data-v14-support-version="true">AI Playgrounds · )v\d+\.\d+\.\d+(</p>)', rf"\g<1>{CURRENT}\g<2>", page)
        path.write_text(page, encoding="utf-8")

    notes_path = SITE / "release-notes.html"
    notes = notes_path.read_text(encoding="utf-8")
    anchor = '<section id="release-v1-8-0"'
    if anchor not in notes:
        raise RuntimeError("Release-notes v1.8.0 anchor changed")
    if 'id="release-v1-8-1"' not in notes:
        section = (
            '<section id="release-v1-8-1" style="margin:1rem 0;padding:1rem 1.2rem;'
            'border:1px solid currentColor;border-radius:12px">'
            '<h2>AI Playgrounds v1.8.1: modern-lab learner parity.</h2>'
            '<p>Labs 13–15 now include the same scenario-led learning sequence as the '
            'first twelve applets: a featured experiment, five predict–run–explain '
            'scenarios, a terminology primer, step-by-step explanation, and teacher '
            'prompts in all four learner locales. The release also aligns header '
            'controls, removes duplicated state prose, and fixes dark-theme contrast '
            'without changing any mechanism result.</p></section>'
        )
        notes = notes.replace(anchor, section + anchor, 1)
    notes_path.write_text(notes, encoding="utf-8")
    for name in ("codemeta.json", "CITATION.cff"):
        shutil.copy2(ROOT / name, SITE / name)


def validate() -> None:
    files = sorted(path for path in SITE.rglob("*") if path.is_file())
    applets = sorted((SITE / "playgrounds").glob("*/index.html"))
    if len(files) != 58 or len(applets) != 15:
        raise RuntimeError(f"v1.8.1 boundary drift: {len(files)} files / {len(applets)} applets")
    for slug in MODERN:
        page = (SITE / "playgrounds" / slug / "index.html").read_text(encoding="utf-8")
        required = (
            'id="v181-modern-learner-parity-style"', 'id="v181-modern-learner-parity-runtime"',
            'class="signature-challenge ap-modern-featured"', 'class="scenario-gallery"',
            'class="scenario-card-grid"', 'class="essay-primer"', 'class="for-teachers"',
            'class="header-theme"', 'class="header-png"', 'class="header-reset"',
            'class="lang-switch modern-lang-switch"', 'class="accessibility-layer ap-modern-a11y-compact"',
            "state.dataset.qaStateReady='1'", "if(state?.dataset.qaStateReady==='1')",
        )
        missing = [marker for marker in required if marker not in page]
        if missing:
            raise RuntimeError(f"v1.8.1 learner parity incomplete for {slug}: {missing}")
        if 'id="ap-modern-more"' in page or '<div class="header-more-menu">' in page:
            raise RuntimeError(f"Modern actions remain hidden under a More menu: {slug}")
        header = page[page.find('<header class="ap-standard-header'):page.find('</header>')]
        if not all(header.count(f'id="{control}"') == 1 for control in (
            "ap-modern-share", "ap-modern-embed", "ap-modern-settings-json", "ap-standard-reset"
        )):
            raise RuntimeError(f"Modern visible header action row is incomplete: {slug}")
        initial_markup = page.split('<script id="v181-modern-learner-parity-runtime">', 1)[0]
        if initial_markup.count('data-modern-scenario-card=') != 5:
            raise RuntimeError(f"Expected five initial scenario cards: {slug}")
        entry_at = initial_markup.find('id="ap-modern-learning"')
        qa_at = initial_markup.find('data-quick-assign-id=')
        essay_at = initial_markup.find('id="ap-modern-explanation"')
        if not (0 <= entry_at < qa_at < essay_at):
            raise RuntimeError(f"Modern learner sequence is not scenario → assignment → explanation: {slug}")
        if 'class="accessibility-layer ap-modern-a11y-parity" open' in page or 'id="ap-modern-a11y-state"' in page:
            raise RuntimeError(f"Duplicated open accessibility state survived: {slug}")
        state_id = LABS[slug]["state_id"]
        if page.count(f'id="{state_id}"') != 1:
            raise RuntimeError(f"Canonical text state is not unique: {slug}")
        if 'body.ap-standard-dark .node circle' not in page or 'body.ap-standard-dark .boundary' not in page:
            raise RuntimeError(f"Modern dark-theme contrast layer missing: {slug}")
        for locale in LOCALES:
            if len(LABS[slug]["copy"][locale]["scenarios"]) != 5 or len(LABS[slug]["copy"][locale]["sections"]) < 5:
                raise RuntimeError(f"Localized curriculum depth incomplete: {slug}/{locale}")
    for path in sorted(SITE.rglob("*.html")):
        page = path.read_text(encoding="utf-8")
        if page.count('data-ai-playgrounds-analytics="v1.8.1"') != 1:
            raise RuntimeError(f"HTML analytics provenance not exactly once at v1.8.1: {path.relative_to(SITE)}")
    for path in applets:
        page = path.read_text(encoding="utf-8")
        if '<meta name="ai-playgrounds-version" content="1.8.1">' not in page:
            raise RuntimeError(f"Applet version metadata not v1.8.1: {path.parent.name}")
    manifest = {row["slug"]: row for row in json.loads((SITE / "applets.json").read_text(encoding="utf-8"))}
    for slug in MODERN:
        row = manifest[slug]
        if len(row["desc"].split()) > 18 or len(row["featured"].split()) > 14:
            raise RuntimeError(f"Modern catalogue copy is still too wordy: {slug}")
    home = (SITE / "index.html").read_text(encoding="utf-8")
    if '<span class="site-version">v1.8.1</span>' not in home:
        raise RuntimeError("Homepage visible release version is not v1.8.1")
    notes = (SITE / "release-notes.html").read_text(encoding="utf-8")
    for release in ("release-v1-8-1", "release-v1-8-0", "release-v1-7-2"):
        if f'id="{release}"' not in notes:
            raise RuntimeError(f"Release-note history missing {release}")
    codemeta = json.loads((SITE / "codemeta.json").read_text(encoding="utf-8"))
    if codemeta.get("softwareVersion") != VERSION or not str(codemeta.get("identifier", "")).endswith("/releases/tag/v1.8.1"):
        raise RuntimeError("Deployed CodeMeta is not bound to v1.8.1")
    citation = (SITE / "CITATION.cff").read_text(encoding="utf-8")
    if re.search(r"(?m)^version:\s*['\"]?1\.8\.1['\"]?\s*$", citation) is None:
        raise RuntimeError("Deployed citation metadata is not bound to v1.8.1")
    core.validate_local_references()


def build_site() -> None:
    base.build_site()
    for slug in MODERN:
        patch_modern_lab(slug)
    patch_release_identity()
    validate()
    print("Built deterministic v1.8.1 learner-parity release: 15 applets / 58 files")


if __name__ == "__main__":
    build_site()
