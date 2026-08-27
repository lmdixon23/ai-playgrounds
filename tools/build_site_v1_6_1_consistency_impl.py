#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

import build_site as base
import build_site_v1_6_1_public as predecessor

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
CATALOGUE_LOCALES = ROOT / "tools" / "catalogue_locales_v1.json"
HOME_LOCALES = ROOT / "tools" / "home_locales_v1.json"
EXPECTED_APPLETS = 15

REQUIRED_CARD_FIELDS = (
    "slug", "icon", "category", "category_en", "category_zh", "title", "title_zh",
    "desc", "desc_zh", "time", "level", "featured", "featured_zh", "accent",
    "accent_name", "course_order", "showcase_order", "course_phase",
)

MODERN = {
    "transformer-language-model": {
        "api": "Lab13Localization",
        "event": "lab13localechange",
        "hide": ".suite-back,.top,#lab13-locale-bar,[data-lab13-v14-provenance]",
    },
    "agent-tool-context": {
        "api": "Lab14Localization",
        "event": "lab14localechange",
        "hide": ".suite-back,.top,#lab14-locale-bar,[data-lab14-v14-provenance]",
    },
    "minimax-alpha-beta": {
        "api": "Lab15Localization",
        "event": "lab15localechange",
        "hide": ".lab15-public-nav,#lab15-locale-bar,main.shell>.hero>.pill,main.shell>.hero>h1,main.shell>.hero>p:first-of-type",
    },
}

CHROME = {
    "en": {"back":"AI Playgrounds", "language":"Language", "theme":"Theme", "reset":"Reset", "home":"Home", "curriculum":"Curriculum", "teacher":"Teacher Pack", "source":"Source", "citation":"Citation"},
    "zh": {"back":"AI Playgrounds", "language":"语言", "theme":"主题", "reset":"重置", "home":"首页", "curriculum":"课程", "teacher":"教师包", "source":"源代码", "citation":"引用"},
    "vi": {"back":"AI Playgrounds", "language":"Ngôn ngữ", "theme":"Giao diện", "reset":"Đặt lại", "home":"Trang chủ", "curriculum":"Chương trình", "teacher":"Teacher Pack", "source":"Mã nguồn", "citation":"Trích dẫn"},
    "es": {"back":"AI Playgrounds", "language":"Idioma", "theme":"Tema", "reset":"Reiniciar", "home":"Inicio", "curriculum":"Currículo", "teacher":"Teacher Pack", "source":"Código fuente", "citation":"Citación"},
}

HOME_STYLE = r'''
<style id="v161-home-consistency-style">
.lang{border:0!important;background:transparent!important;overflow:visible!important;padding:0!important}
.lang button[data-lang],.lang .v14-language-select{display:none!important}
.ap-home-language-select{min-height:42px;padding:7px 34px 7px 11px;border:1px solid var(--line);border-radius:10px;background:var(--surface);color:var(--text);font:inherit;cursor:pointer}
.ap-home-language-select:focus-visible{outline:3px solid color-mix(in srgb,var(--accent) 55%,transparent);outline-offset:2px}
@media(pointer:coarse){.ap-home-language-select{min-height:44px}}
</style>
'''

SUPPORT_SELECT_FIX = r'''
<style id="v161-select-shell-fix">
.support-language-switch,.lang{border:0!important;background:transparent!important;overflow:visible!important;padding:0!important;box-shadow:none!important}
.support-language-switch .v14-language-select,.lang .v14-language-select{border-radius:10px!important;max-width:100%;margin:0}
</style>
'''

STANDARD_SHELL_STYLE = r'''
<style id="v161-standard-applet-shell-style">
.ap-standard-header{background:var(--card,#fff);border-bottom:1px solid var(--border,#d7dde7);padding:12px 24px;color:var(--fg,#172033)}
.ap-standard-header .header-utility{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-bottom:10px}
.ap-standard-header .header-prefs{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.ap-standard-header .header-main{display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap}
.ap-standard-header .header-title-wrap{min-width:0;flex:1 1 520px}
.ap-standard-header h1{margin:0;font-size:1.5rem;line-height:1.2}
.ap-standard-header .ap-standard-subtitle{margin:.25rem 0 0;color:var(--muted,#637083);max-width:920px;font-size:.9rem}
.ap-standard-header .back{color:var(--accent,#3157c8);text-decoration:none;font-size:.9rem;font-weight:700}
.ap-standard-header .header-actions{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.ap-standard-header label{font-size:.78rem;font-weight:800;color:var(--muted,#637083)}
.ap-standard-header select,.ap-standard-header button{min-height:38px;border:1px solid var(--border,#d7dde7);border-radius:7px;background:var(--card,#fff);color:var(--fg,#172033);font:inherit;padding:6px 10px}
.ap-standard-header select{padding-right:32px;cursor:pointer}.ap-standard-header button{cursor:pointer}
.ap-standard-header :focus-visible,.ap-standard-footer :focus-visible{outline:2px solid var(--accent,#3157c8);outline-offset:2px}
.ap-standard-footer{margin:28px auto 0;max-width:1220px;padding:18px 24px 32px;border-top:1px solid var(--border,#d7dde7);color:var(--muted,#637083);font-size:.82rem;text-align:center}
.ap-standard-footer a{color:var(--accent,#3157c8)}
body.ap-standard-dark{--bg:#0f172a;--card:#172033;--fg:#e2e8f0;--muted:#a9b6c9;--border:#334155;--soft:#1e293b;background:var(--bg)!important;color:var(--fg)!important}
body.ap-standard-dark .ap-standard-header select,body.ap-standard-dark .ap-standard-header button{background:var(--card);color:var(--fg)}
@media(pointer:coarse){.ap-standard-header select,.ap-standard-header button{min-height:44px}}
@media(max-width:480px){.ap-standard-header{padding:12px 16px}.ap-standard-header .header-actions,.ap-standard-header .header-prefs{width:100%}.ap-standard-header select{flex:1 1 170px;min-width:0}.ap-standard-header .header-actions button{flex:1}.ap-standard-footer{padding-left:16px;padding-right:16px}}
@media(prefers-reduced-motion:reduce){.ap-standard-header *,.ap-standard-footer *{transition:none!important}}
</style>
'''


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def enrich_manifest() -> list[dict]:
    manifest_path = SITE / "applets.json"
    manifest = _load_json(manifest_path)
    locale_rows = _load_json(CATALOGUE_LOCALES)
    if len(manifest) != EXPECTED_APPLETS:
        raise RuntimeError(f"Expected {EXPECTED_APPLETS} applets before catalogue enrichment, found {len(manifest)}")
    by_slug = {row.get("slug"): row for row in manifest}
    if set(by_slug) != set(locale_rows):
        raise RuntimeError(f"Catalogue locale registry mismatch: manifest={sorted(by_slug)} locales={sorted(locale_rows)}")
    for slug, row in by_slug.items():
        missing = [field for field in REQUIRED_CARD_FIELDS if not row.get(field)]
        if missing:
            raise RuntimeError(f"Incomplete catalogue schema for {slug}: {missing}")
        row.update(locale_rows[slug])
        for field in ("category_vi","category_es","title_vi","title_es","desc_vi","desc_es","featured_vi","featured_es"):
            if not row.get(field):
                raise RuntimeError(f"Missing four-language catalogue field {field}: {slug}")
        if not isinstance(row.get("keywords"), list) or not row["keywords"]:
            raise RuntimeError(f"Missing search keywords: {slug}")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def patch_r4_roundtrip_source() -> None:
    path = SITE / "assets" / "localization-r4.js"
    source = path.read_text(encoding="utf-8")
    old_text = "if (!applying && current !== 'vi' && current !== 'es') originalText.set(node, live);\n    if (!applying && (current === 'vi' || current === 'es')) originalText.set(node, live);"
    new_text = "if (!originalText.has(node)) originalText.set(node, live);"
    old_attr = "if (!applying) state[attr] = live;\n      const source = Object.prototype.hasOwnProperty.call(state, attr) ? state[attr] : live;"
    new_attr = "if (!Object.prototype.hasOwnProperty.call(state, attr)) state[attr] = live;\n      const source = Object.prototype.hasOwnProperty.call(state, attr) ? state[attr] : live;"
    if old_text not in source or old_attr not in source:
        raise RuntimeError("R4 locale-source patch markers changed; refusing a silent partial fix")
    source = source.replace(old_text, new_text, 1).replace(old_attr, new_attr, 1)
    source = source.replace("(() => {\n  'use strict';", "(() => {\n  'use strict';\n  // v1.6.1: preserve canonical source text across VI/ES round trips.", 1)
    path.write_text(source, encoding="utf-8")


def replace_section(html: str, section_id: str, replacement: str) -> str:
    pattern = re.compile(rf'<section\b[^>]*\bid="{re.escape(section_id)}"[^>]*>.*?</section>', re.S)
    html, count = pattern.subn(replacement, html, count=1)
    if count != 1:
        raise RuntimeError(f"Could not replace landing section #{section_id}")
    return html


def landing_start_section() -> str:
    return '''<section class="ap-launch" id="start-here" aria-labelledby="ap-start-title">
  <p class="ap-launch__eyebrow" data-t="startEyebrow">Start in five minutes</p>
  <h2 id="ap-start-title" data-t="startTitle">Choose one question, make a prediction, then inspect what the algorithm does.</h2>
  <p class="ap-launch__lead" data-t="startLead">AI Playgrounds is a multilingual, offline-ready suite for learning AI through controlled experiments rather than passive animation.</p>
  <ul class="ap-launch__proof" aria-label="Release evidence"><li data-t="proofAppletCount"></li><li data-t="proofLanguages"></li><li data-t="proofChecks"></li><li data-t="proofOffline"></li><li data-t="proofLicense"></li></ul>
  <div class="ap-launch__grid">
    <article class="ap-launch__card"><h3 data-t="learnerCardTitle"></h3><p data-t="learnerCardCopy"></p><a href="playgrounds/minimax-alpha-beta/index.html?mode=explore&amp;featured=1" data-t="learnerCardLink"></a></article>
    <article class="ap-launch__card"><h3 data-t="educatorCardTitle"></h3><p data-t="educatorCardCopy"></p><a href="teacher-pack.html#quick-assigns" data-t="educatorCardLink"></a></article>
    <article class="ap-launch__card"><h3 data-t="researchCardTitle"></h3><p data-t="researchCardCopy"></p><a href="research-and-citation.html" data-t="researchCardLink"></a></article>
  </div>
  <div class="ap-boundary"><div><h3 data-t="evidenceYesTitle"></h3><p data-t="evidenceYesCopy"></p></div><div><h3 data-t="evidenceNoTitle"></h3><p data-t="evidenceNoCopy"></p></div></div>
</section>'''


def landing_privacy_section() -> str:
    return '''<section class="ap-launch" id="privacy" aria-labelledby="ap-privacy-title">
  <p class="ap-launch__eyebrow" data-t="privacyEyebrow"></p>
  <h2 id="ap-privacy-title" data-t="privacyTitle"></h2>
  <p class="ap-launch__lead" data-t="privacyCopy"></p>
  <div class="ap-privacy-controls"><button type="button" id="analytics-opt-out" data-t="privacyDisable"></button><button type="button" id="analytics-opt-in" data-t="privacyEnable"></button><a href="https://github.com/lmdixon23/ai-playgrounds/blob/main/docs/ANALYTICS_AND_PRIVACY.md" data-t="privacySpec"></a></div>
</section>'''


def patch_landing(manifest: list[dict]) -> None:
    path = SITE / "index.html"
    html = path.read_text(encoding="utf-8")
    compact = json.dumps(manifest, ensure_ascii=False, separators=(",", ":"))
    html, count = re.subn(r"const APPLETS=\[.*?\];\nconst COPY=", "const APPLETS=" + compact + ";\nconst COPY=", html, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError("Could not replace landing catalogue with enriched 15-applet manifest")
    html = replace_section(html, "start-here", landing_start_section())
    html = replace_section(html, "privacy", landing_privacy_section())
    if 'id="v161-home-consistency-style"' not in html:
        html = html.replace("</head>", HOME_STYLE + "\n</head>", 1)
    copy = _load_json(HOME_LOCALES)
    payload = json.dumps(copy, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    runtime = f'''<script id="v161-home-four-locale-runtime">
(()=>{{'use strict';
const AP_HOME={payload};
const AP_LOCALES=['en','zh','vi','es'];
const AP_NAMES={{en:'English',zh:'简体中文',vi:'Tiếng Việt',es:'Español'}};
const AP_CATEGORY={{all:{{en:'All',zh:'全部',vi:'Tất cả',es:'Todos'}},search:{{en:'Search',zh:'搜索',vi:'Tìm kiếm',es:'Búsqueda'}},logic:{{en:'Logic',zh:'逻辑',vi:'Logic',es:'Lógica'}},probability:{{en:'Probability',zh:'概率',vi:'Xác suất',es:'Probabilidad'}},ml:{{en:'Machine learning',zh:'机器学习',vi:'Học máy',es:'Aprendizaje automático'}},neural:{{en:'Neural networks',zh:'神经网络',vi:'Mạng nơ-ron',es:'Redes neuronales'}},vision:{{en:'Vision',zh:'视觉',vi:'Thị giác',es:'Visión'}},rl:{{en:'Reinforcement learning',zh:'强化学习',vi:'Học tăng cường',es:'Aprendizaje por refuerzo'}}}};
Object.assign(COPY.en,AP_HOME.en);Object.assign(COPY.zh,AP_HOME.zh);COPY.vi=AP_HOME.vi;COPY.es=AP_HOME.es;
function apNorm(v){{v=String(v||'').toLowerCase();if(v.startsWith('zh'))return'zh';if(v.startsWith('vi'))return'vi';if(v.startsWith('es'))return'es';return'en'}}
function apField(a,base){{if(lang==='en')return a[base]??'';const value=a[base+'_'+lang];return value??a[base]??''}}
function apCorpus(a){{const fields=['title','desc','featured','category_en','category_zh','category_vi','category_es','title_zh','title_vi','title_es','desc_zh','desc_vi','desc_es','featured_zh','featured_vi','featured_es','course_phase'];return fields.map(k=>a[k]||'').concat(a.keywords||[]).join(' ').toLowerCase()}}
formatTime=function(value){{const n=parseInt(value,10);return `${{n}} ${{t('minuteUnit')}}`}};
renderFilters=function(){{const root=document.getElementById('filters');root.innerHTML='';Object.keys(AP_CATEGORY).forEach(key=>{{const b=document.createElement('button');b.className='filter'+(filter===key?' active':'');b.textContent=(AP_CATEGORY[key]&&AP_CATEGORY[key][lang])||AP_CATEGORY[key].en;b.onclick=()=>{{filter=key;renderFilters();renderApplets()}};root.appendChild(b)}})}};
renderApplets=function(){{const q=(document.getElementById('search')?.value||'').trim().toLowerCase();const list=APPLETS.filter(a=>(filter==='all'||a.category===filter)&&(!q||apCorpus(a).includes(q)));const root=document.getElementById('appletGrid');root.innerHTML='';if(!list.length){{root.innerHTML=`<div class="empty">${{t('empty')}}</div>`;return}}list.forEach(a=>{{const el=document.createElement('a');el.className='applet';el.style.setProperty('--applet-accent',a.accent||'var(--accent)');el.href=`playgrounds/${{a.slug}}/index.html?mode=explore&featured=1&lang=${{lang}}`;const category=apField(a,'category')||apField(a,'category_en')||a.course_phase||'AI';const title=apField(a,'title')||a.slug;const desc=apField(a,'desc');const featured=apField(a,'featured');el.innerHTML=`<div class="applet-top"><span class="icon">${{a.icon||'•'}}</span><span class="meta">${{category}}<br>${{formatTime(a.time||'')}}</span></div><h3>${{title}}</h3><p>${{desc}}</p><span class="featured">${{featured}} →</span>`;root.appendChild(el)}})}};
function apMetadata(){{const titles={{en:'AI Playgrounds | 15 interactive labs for learning artificial intelligence',zh:'AI Playgrounds | 15 个交互式人工智能学习实验',vi:'AI Playgrounds | 15 phòng thí nghiệm tương tác để học trí tuệ nhân tạo',es:'AI Playgrounds | 15 laboratorios interactivos para aprender inteligencia artificial'}};document.title=titles[lang]||titles.en;const desc=AP_HOME[lang].heroCopy;document.querySelector('meta[name="description"]')?.setAttribute('content',desc);document.querySelectorAll('meta[property="og:description"],meta[name="twitter:description"]').forEach(el=>el.setAttribute('content',desc))}}
applyLanguage=function(){{document.documentElement.lang=lang==='zh'?'zh-Hans':lang;document.querySelectorAll('[data-t]').forEach(el=>el.innerHTML=t(el.dataset.t));document.querySelectorAll('[data-t-placeholder]').forEach(el=>el.placeholder=t(el.dataset.tPlaceholder));document.querySelectorAll('[data-t-aria-label]').forEach(el=>el.setAttribute('aria-label',t(el.dataset.tAriaLabel)));renderFilters();renderApplets();localizeInternalLinks();localStorage.setItem('ai-playgrounds-lang',lang);if(document.getElementById('ap-home-language-select'))document.getElementById('ap-home-language-select').value=lang;apMetadata()}};
function install(){{const root=document.querySelector('.lang');if(root){{root.innerHTML='';const select=document.createElement('select');select.id='ap-home-language-select';select.className='ap-home-language-select';select.setAttribute('aria-label','Language');for(const code of AP_LOCALES){{const o=document.createElement('option');o.value=code;o.textContent=AP_NAMES[code];select.appendChild(o)}}select.addEventListener('change',()=>{{lang=select.value;applyLanguage()}});root.appendChild(select)}}const requested=new URLSearchParams(location.search).get('lang');const saved=localStorage.getItem('ai-playgrounds-lang');lang=requested?apNorm(requested):(saved?apNorm(saved):apNorm(lang));applyLanguage();document.getElementById('runProof')?.addEventListener('click',()=>queueMicrotask(()=>{{if(lang==='vi')document.getElementById('proofResult').textContent=`A* khám phá ít hơn ${{sols.bfs.seen.length-sols.astar.seen.length}} ô với cùng độ dài đường đi.`;if(lang==='es')document.getElementById('proofResult').textContent=`A* explora ${{sols.bfs.seen.length-sols.astar.seen.length}} celdas menos con la misma longitud de ruta.`}}))}}
install();
}})();
</script>'''
    html = html.replace("</body>", runtime + "\n</body>", 1)
    if 'hreflang="vi"' not in html:
        insert = '<link href="https://lmdixon23.github.io/ai-playgrounds/?lang=vi" hreflang="vi" rel="alternate"/><link href="https://lmdixon23.github.io/ai-playgrounds/?lang=es" hreflang="es" rel="alternate"/>'
        html = html.replace('<link href="https://lmdixon23.github.io/ai-playgrounds/?lang=en" hreflang="x-default" rel="alternate"/>', insert + '<link href="https://lmdixon23.github.io/ai-playgrounds/?lang=en" hreflang="x-default" rel="alternate"/>', 1)
    html = re.sub(r'"inLanguage":\[[^\]]*\]', '"inLanguage":["en","zh","vi","es"]', html, count=1)
    path.write_text(html, encoding="utf-8")


def patch_select_shells() -> None:
    for path in sorted(SITE.glob("*.html")):
        html = path.read_text(encoding="utf-8")
        if "v14-language-select" not in html:
            continue
        if 'id="v161-select-shell-fix"' not in html:
            html = html.replace("</head>", SUPPORT_SELECT_FIX + "\n</head>", 1)
        path.write_text(html, encoding="utf-8")


def modern_header(slug: str, entry: dict) -> str:
    return f'''<header class="ap-standard-header" data-ap-standard-shell="{slug}">
  <div class="header-utility"><a class="back" href="../../index.html">← <span data-ap-chrome="back">AI Playgrounds</span></a><div class="header-prefs"><label for="ap-standard-language-select" data-ap-chrome="language">Language</label><select id="ap-standard-language-select" aria-label="Language"><option value="en">English</option><option value="zh">简体中文</option><option value="vi">Tiếng Việt</option><option value="es">Español</option></select></div></div>
  <div class="header-main"><div class="header-title-wrap"><h1 id="ap-standard-title">{entry['title']}</h1><p id="ap-standard-subtitle" class="ap-standard-subtitle">{entry['desc']}</p></div><div class="header-actions"><button id="ap-standard-theme" type="button" data-ap-chrome="theme">Theme</button><button id="ap-standard-reset" type="button" data-ap-chrome="reset">Reset</button></div></div>
</header>'''


def modern_footer() -> str:
    return '''<footer class="ap-standard-footer" data-ap-standard-footer><span>AI Playgrounds · v1.6.1</span> · <a href="../../index.html" data-ap-chrome="home">Home</a> · <a href="../../curriculum.html" data-ap-chrome="curriculum">Curriculum</a> · <a href="../../teacher-pack.html" data-ap-chrome="teacher">Teacher Pack</a> · <a href="https://github.com/lmdixon23/ai-playgrounds" data-ap-chrome="source">Source</a> · <a href="../../research-and-citation.html" data-ap-chrome="citation">Citation</a></footer>'''


def patch_modern_shells(manifest: list[dict]) -> None:
    by_slug = {row["slug"]: row for row in manifest}
    chrome = json.dumps(CHROME, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    for slug, cfg in MODERN.items():
        path = SITE / "playgrounds" / slug / "index.html"
        html = path.read_text(encoding="utf-8")
        entry = by_slug[slug]
        if 'data-ap-standard-shell' in html:
            raise RuntimeError(f"Standard shell would be applied twice: {slug}")
        shell_css = STANDARD_SHELL_STYLE.replace("</style>", f"\n{cfg['hide']}{{display:none!important}}\n</style>")
        html = html.replace("</head>", shell_css + "\n</head>", 1)
        main_match = re.search(r"<main\b", html)
        if not main_match:
            raise RuntimeError(f"No main element for standard shell: {slug}")
        html = html[:main_match.start()] + modern_header(slug, entry) + "\n" + html[main_match.start():]
        data = {k: entry[k] for k in ("title","title_zh","title_vi","title_es","desc","desc_zh","desc_vi","desc_es")}
        payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
        runtime = f'''<script id="v161-standard-shell-runtime">
(()=>{{'use strict';const API={json.dumps(cfg['api'])},EVENT={json.dumps(cfg['event'])},DATA={payload},CHROME={chrome};const $=s=>document.querySelector(s);function norm(v){{v=String(v||'').toLowerCase();if(v.startsWith('zh'))return'zh';if(v.startsWith('vi'))return'vi';if(v.startsWith('es'))return'es';return'en'}}function api(){{return window[API]||null}}function locale(){{const a=api();return norm((a&&((a.getLocale&&a.getLocale())||(a.locale&&a.locale())))||new URL(location.href).searchParams.get('lang')||'en')}}function f(base,l){{if(l==='en')return DATA[base]||'';return DATA[base+'_'+l]||DATA[base]||''}}function sync(value){{const l=norm(value||locale()),c=CHROME[l]||CHROME.en;$('#ap-standard-title').textContent=f('title',l);$('#ap-standard-subtitle').textContent=f('desc',l);const sel=$('#ap-standard-language-select');if(sel)sel.value=l;document.querySelectorAll('[data-ap-chrome]').forEach(el=>{{const k=el.dataset.apChrome;if(c[k])el.textContent=c[k]}})}}let deferredWait=false;function wait(){{const a=api();if(!a||typeof a.setLocale!=='function'){{if(document.readyState==='loading'&&!deferredWait){{deferredWait=true;document.addEventListener('DOMContentLoaded',wait,{{once:true}});return}}console.error('Modern shell could not start because '+API+' is unavailable');return}}const sel=$('#ap-standard-language-select');sync(locale());sel?.addEventListener('change',()=>{{a.setLocale(sel.value);setTimeout(()=>sync(sel.value),0)}});window.addEventListener(EVENT,e=>sync(e.detail&&e.detail.locale));$('#ap-standard-theme')?.addEventListener('click',()=>{{document.body.classList.toggle('ap-standard-dark');localStorage.setItem('ai-playgrounds-theme',document.body.classList.contains('ap-standard-dark')?'dark':'light')}});if(localStorage.getItem('ai-playgrounds-theme')==='dark')document.body.classList.add('ap-standard-dark');$('#ap-standard-reset')?.addEventListener('click',()=>location.reload())}}wait();}})();
</script>'''
        html = html.replace("</body>", modern_footer() + "\n" + runtime + "\n</body>", 1)
        path.write_text(html, encoding="utf-8")


def update_version_provenance() -> None:
    for path in sorted(SITE.rglob("*.html")):
        html = path.read_text(encoding="utf-8")
        html = html.replace('name="ai-playgrounds-version" content="1.6.0"', 'name="ai-playgrounds-version" content="1.6.1"')
        html = html.replace('AI Playgrounds · v1.6.0', 'AI Playgrounds · v1.6.1')
        path.write_text(html, encoding="utf-8")


def validate(manifest: list[dict]) -> None:
    base.validate_local_references()
    home = (SITE / "index.html").read_text(encoding="utf-8")
    if "undefinedundefined" in home or re.search(r'>\s*undefined\s*<', home):
        raise RuntimeError("Landing page contains a literal undefined card value")
    for marker in ('id="ap-home-language-select"','v161-home-four-locale-runtime'):
        if marker not in home:
            raise RuntimeError(f"Landing page lacks four-language runtime marker: {marker}")
    if 'hreflang="vi"' not in home or 'hreflang="es"' not in home:
        raise RuntimeError("Landing page lacks VI/ES discovery metadata")
    if len(manifest) != 15:
        raise RuntimeError("v1.6.1 consistency composition must contain 15 applets")
    for slug in MODERN:
        source = (SITE / "playgrounds" / slug / "index.html").read_text(encoding="utf-8")
        if source.count('data-ap-standard-shell') != 1 or source.count('data-ap-standard-footer') != 1:
            raise RuntimeError(f"Modern applet lacks exactly one standard outer shell: {slug}")
    r4 = (SITE / "assets" / "localization-r4.js").read_text(encoding="utf-8")
    if "preserve canonical source text across VI/ES round trips" not in r4:
        raise RuntimeError("R4 locale round-trip patch missing from final composition")
    for page in ("teacher-pack.html","curriculum.html","quality.html","research-and-citation.html"):
        source=(SITE/page).read_text(encoding="utf-8")
        if "v14-language-select" in source and 'id="v161-select-shell-fix"' not in source:
            raise RuntimeError(f"Support page language selector shell was not flattened: {page}")


def build_site() -> None:
    predecessor.build_site()
    manifest = enrich_manifest()
    patch_r4_roundtrip_source()
    patch_landing(manifest)
    patch_select_shells()
    patch_modern_shells(manifest)
    update_version_provenance()
    validate(manifest)
    print("Built v1.6.1 final consistency candidate: four-language home, complete catalogue/search, reversible R4 locales, shared modern-lab shells")


if __name__ == "__main__":
    build_site()
