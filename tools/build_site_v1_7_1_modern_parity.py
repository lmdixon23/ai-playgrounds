#!/usr/bin/env python3
from __future__ import annotations

"""v1.7.1 parity wrapper for Labs 13-15.

This layer changes only shared product chrome and learner-support affordances. It
must not alter Transformer arithmetic, agent-runtime semantics, Minimax/Alpha-
Beta results, Guided Challenge mechanisms, or Quick Assign response state.
"""

import html as html_lib
import json
import re
from pathlib import Path

import build_site_v1_7_final as predecessor

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
DATA = ROOT / "tools" / "modern_parity_v1.json"
MODERN = ("transformer-language-model", "agent-tool-context", "minimax-alpha-beta")

SHELL_LABELS = {
    "en": {"back":"Back to all playgrounds", "theme":"Theme", "reset":"Reset all"},
    "zh": {"back":"返回全部 playground", "theme":"主题", "reset":"全部重置"},
    "vi": {"back":"Quay lại tất cả playground", "theme":"Giao diện", "reset":"Đặt lại tất cả"},
    "es": {"back":"Volver a todos los playgrounds", "theme":"Tema", "reset":"Reiniciar todo"},
}

STYLE = r'''<style id="v171-modern-parity-style">
.ap-modern-skip{position:absolute;left:-999px;top:10px;z-index:10000;padding:10px 14px;background:var(--accent,#3157c8);color:#fff;border-radius:8px;font:700 .9rem -apple-system,system-ui,sans-serif;text-decoration:none}
.ap-modern-skip:focus{left:12px}
.ap-standard-header.page-header{background:var(--card,#fff);border-bottom:1px solid var(--border,#d7dde7);padding:12px 24px}
.ap-standard-header .ap-standard-subtitle{display:none!important}
.ap-standard-header .header-actions button{min-height:38px;display:inline-flex;align-items:center;gap:5px;padding:7px 10px;border-radius:8px}
.ap-modern-tldr{max-width:820px;margin:16px auto 0;background:var(--accent,#3157c8);color:#fff;border-radius:8px;padding:14px 16px;font:.88rem/1.45 -apple-system,system-ui,sans-serif}
.ap-modern-tldr strong{color:rgba(255,255,255,.86);font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;display:block;margin-bottom:6px}
.ap-modern-tldr p{margin:5px 0}
.ap-modern-support{max-width:980px;margin:18px auto;padding:0 20px;color:var(--fg,#172033)}
.ap-modern-support details{margin:10px 0;border:1px solid var(--border,#d7dde7);border-radius:9px;background:var(--card,#fff);padding:0}
.ap-modern-support summary{cursor:pointer;font-weight:800;padding:11px 13px}
.ap-modern-support .ap-support-body{padding:0 13px 13px;color:var(--muted,#637083);line-height:1.5}
.ap-modern-terms{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin:8px 0}
.ap-modern-term{border:1px solid var(--border,#d7dde7);border-radius:8px;padding:9px;background:var(--soft,#f8fafc)}
.ap-modern-term dt{font-weight:800;color:var(--fg,#172033)}
.ap-modern-term dd{margin:3px 0 0}
.ap-standard-footer.ap-modern-rich-footer{max-width:none;padding:18px 24px 30px}
.ap-modern-footer-primary{margin-bottom:7px}
.ap-modern-toast{position:fixed;left:50%;bottom:18px;transform:translateX(-50%);z-index:10000;background:#111827;color:#fff;padding:8px 12px;border-radius:8px;font:600 .82rem -apple-system,system-ui,sans-serif;box-shadow:0 8px 30px rgba(0,0,0,.2)}
body.embed-mode>.ap-standard-header,body.embed-mode>.ap-modern-skip,body.embed-mode>.ap-modern-tldr,body.embed-mode>.ap-modern-support,body.embed-mode>.ap-standard-footer{display:none!important}
body.embed-mode main{margin-top:0!important}
@media(max-width:720px){.ap-standard-header .header-actions{width:100%;display:grid!important;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}.ap-standard-header .header-actions button{width:100%;justify-content:center}.ap-modern-terms{grid-template-columns:1fr}}
@media(pointer:coarse){.ap-standard-header .header-actions button{min-height:44px}}
@media(prefers-reduced-motion:reduce){.ap-modern-toast{transition:none!important}}
</style>'''


def load_data() -> dict:
    return json.loads(DATA.read_text(encoding="utf-8"))


def attrs(values: dict[str, str]) -> str:
    return " ".join(
        f'data-ap-{locale}="{html_lib.escape(str(text), quote=True)}"'
        for locale, text in values.items()
    )


def loc_attr(data: dict, key: str, slug: str | None = None) -> str:
    if slug:
        values = {locale: data["copy"][slug][locale][key] for locale in ("en","zh","vi","es")}
    else:
        values = {locale: data["chrome"][locale][key] for locale in ("en","zh","vi","es")}
    return attrs(values)


def tldr(data: dict, slug: str) -> str:
    c = data["copy"][slug]["en"]
    chrome = data["chrome"]["en"]
    return f'''<aside class="ap-modern-tldr" aria-label="{html_lib.escape(chrome['biglabel'])}">
<strong {loc_attr(data,'biglabel')}>{html_lib.escape(chrome['biglabel'])}</strong>
<p {loc_attr(data,'big',slug)}>{html_lib.escape(c['big'])}</p>
<p><b {loc_attr(data,'watchlabel')}>{html_lib.escape(chrome['watchlabel'])}</b>: <span {loc_attr(data,'watch',slug)}>{html_lib.escape(c['watch'])}</span></p>
</aside>'''


def support(data: dict, slug: str) -> str:
    c = data["copy"][slug]["en"]
    chrome = data["chrome"]["en"]
    terms = "".join(
        f'<div class="ap-modern-term"><dt>{html_lib.escape(term)}</dt><dd>{html_lib.escape(desc)}</dd></div>'
        for term, desc in c["terms"]
    )
    return f'''<section class="ap-modern-support" aria-label="Learning support">
<details id="ap-modern-key-terms"><summary {loc_attr(data,'terms')}>{html_lib.escape(chrome['terms'])}</summary><div class="ap-support-body"><dl id="ap-modern-terms-list" class="ap-modern-terms">{terms}</dl></div></details>
<details id="ap-modern-a11y"><summary {loc_attr(data,'a11y')}>{html_lib.escape(chrome['a11y'])}</summary><div class="ap-support-body" {loc_attr(data,'a11ybody')}>{html_lib.escape(chrome['a11ybody'])}</div></details>
<details id="ap-modern-fidelity"><summary {loc_attr(data,'fidelity')}>{html_lib.escape(chrome['fidelity'])}</summary><div class="ap-support-body" {loc_attr(data,'fidelity',slug)}>{html_lib.escape(c['fidelity'])}</div></details>
</section>'''


def rich_footer(data: dict) -> str:
    c = data["chrome"]["en"]
    return f'''<footer class="ap-standard-footer ap-modern-rich-footer" data-ap-standard-footer>
<div class="ap-modern-footer-primary"><a href="#top" {loc_attr(data,'backtop')}>{html_lib.escape(c['backtop'])}</a> · <span {loc_attr(data,'made')}>{html_lib.escape(c['made'])}</span></div>
<div>© 2026 Logan M. Dixon · <a href="https://logandixon.me" {loc_attr(data,'portfolio')}>{html_lib.escape(c['portfolio'])}</a> · <a href="../../index.html">AI Playgrounds</a> · <a href="../../curriculum.html">Curriculum</a> · <a href="../../teacher-pack.html">Teacher Pack</a> · <a href="https://github.com/lmdixon23/ai-playgrounds">Source</a> · MIT · <a href="../../research-and-citation.html">Citation</a> · <a href="https://github.com/lmdixon23/ai-playgrounds/issues" {loc_attr(data,'report')}>{html_lib.escape(c['report'])}</a> · <a href="https://orcid.org/0009-0008-1712-6630">ORCID</a> · v1.7.1</div>
</footer>'''


def runtime(data: dict, slug: str) -> str:
    payload = json.dumps({"copy": data["copy"][slug], "chrome": data["chrome"], "shell": SHELL_LABELS}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f'''<script id="v171-modern-parity-runtime">
(()=>{{'use strict';const D={payload};
const norm=v=>{{v=String(v||'').toLowerCase();return v.startsWith('zh')?'zh':v.startsWith('vi')?'vi':v.startsWith('es')?'es':'en'}};
const locale=()=>norm(document.documentElement.lang);
function paint(){{const l=locale();document.querySelectorAll('[data-ap-en]').forEach(el=>{{const v=el.getAttribute('data-ap-'+l)||el.getAttribute('data-ap-en')||'';if(el.matches('button')){{const sp=el.querySelector('span');if(sp)sp.textContent=v;else el.textContent=v}}else el.textContent=v}});const back=document.querySelector('[data-ap-chrome="back"]');if(back)back.textContent=D.shell[l].back;const theme=document.getElementById('ap-standard-theme');if(theme)theme.textContent='🌙 '+D.shell[l].theme;const reset=document.getElementById('ap-standard-reset');if(reset)reset.textContent='↺ '+D.shell[l].reset;const dl=document.getElementById('ap-modern-terms-list');if(dl){{dl.innerHTML='';for(const pair of D.copy[l].terms){{const wrap=document.createElement('div');wrap.className='ap-modern-term';const dt=document.createElement('dt');dt.textContent=pair[0];const dd=document.createElement('dd');dd.textContent=pair[1];wrap.append(dt,dd);dl.append(wrap)}}}}}}
function toast(key){{document.querySelector('.ap-modern-toast')?.remove();const el=document.createElement('div');el.className='ap-modern-toast';el.setAttribute('role','status');el.textContent=D.chrome[locale()][key]||D.chrome.en[key];document.body.append(el);setTimeout(()=>el.remove(),1800)}}
async function copyText(text,key){{try{{await navigator.clipboard.writeText(text);toast(key)}}catch(_e){{const ta=document.createElement('textarea');ta.value=text;ta.style.position='fixed';ta.style.opacity='0';document.body.append(ta);ta.select();try{{document.execCommand('copy');toast(key)}}catch(_x){{}}ta.remove()}}}}
document.getElementById('ap-modern-share')?.addEventListener('click',async()=>{{const url=location.href;try{{if(navigator.share){{await navigator.share({{title:document.title,url}});return}}}}catch(_e){{}}copyText(url,'copied')}});
document.getElementById('ap-modern-embed')?.addEventListener('click',()=>{{const u=new URL(location.href);u.searchParams.set('embed','1');const code='<iframe src="'+u.href.replace(/"/g,'&quot;')+'" loading="lazy" style="width:100%;min-height:720px;border:0" title="'+document.title.replace(/"/g,'&quot;')+'"></iframe>';copyText(code,'embedcopied')}});
try{{if(new URLSearchParams(location.search).get('embed')==='1')document.body.classList.add('embed-mode')}}catch(_e){{}}
new MutationObserver(paint).observe(document.documentElement,{{attributes:true,attributeFilter:['lang']}});window.addEventListener('lab13localechange',paint);window.addEventListener('lab14localechange',paint);window.addEventListener('lab15localechange',paint);paint();
}})();
</script>'''


def patch(slug: str, data: dict) -> None:
    path = SITE / "playgrounds" / slug / "index.html"
    page = path.read_text(encoding="utf-8")
    if 'id="v171-modern-parity-style"' in page:
        raise RuntimeError(f"Modern parity layer would be applied twice: {slug}")
    if 'class="ap-standard-header"' not in page or 'class="ap-standard-footer' not in page:
        raise RuntimeError(f"Modern standard shell missing before parity patch: {slug}")

    page = page.replace("</head>", STYLE + "\n</head>", 1)
    page = page.replace('<body', f'<body id="top" data-ap-modern-parity="{slug}"', 1)
    body_end = page.find('>', page.find('<body'))
    skip = f'<a class="ap-modern-skip" href="#ap-modern-interactive-start" {loc_attr(data,"skip")}>{html_lib.escape(data["chrome"]["en"]["skip"])}</a>'
    page = page[:body_end+1] + "\n" + skip + page[body_end+1:]
    page = page.replace('<header class="ap-standard-header"', '<header class="ap-standard-header page-header"', 1)

    actions = '<div class="header-actions">'
    buttons = f'<button id="ap-modern-share" type="button" {loc_attr(data,"share")}>🔗 <span>{html_lib.escape(data["chrome"]["en"]["share"])}</span></button><button id="ap-modern-embed" type="button" {loc_attr(data,"embed")}>📎 <span>{html_lib.escape(data["chrome"]["en"]["embed"])}</span></button>'
    if actions not in page:
        raise RuntimeError(f"Modern header actions missing: {slug}")
    page = page.replace(actions, actions + buttons, 1)

    if '<main ' in page:
        page = page.replace('<main ', '<main id="ap-modern-interactive-start" tabindex="-1" ', 1)
    elif '<main>' in page:
        page = page.replace('<main>', '<main id="ap-modern-interactive-start" tabindex="-1">', 1)
    else:
        raise RuntimeError(f"Modern main region missing: {slug}")

    header_end = page.find('</header>')
    page = page[:header_end+9] + "\n" + tldr(data, slug) + page[header_end+9:]
    footer_match = re.search(r'<footer class="ap-standard-footer"[^>]*>.*?</footer>', page, re.S)
    if not footer_match:
        raise RuntimeError(f"Modern standard footer missing: {slug}")
    page = page[:footer_match.start()] + support(data, slug) + "\n" + rich_footer(data) + page[footer_match.end():]
    page = page.replace("</body>", runtime(data, slug) + "\n</body>", 1)
    path.write_text(page, encoding="utf-8")


def validate() -> None:
    for slug in MODERN:
        page = (SITE / "playgrounds" / slug / "index.html").read_text(encoding="utf-8")
        required = (
            'class="ap-modern-skip"', 'class="ap-standard-header page-header"',
            'id="ap-modern-share"', 'id="ap-modern-embed"', 'class="ap-modern-tldr"',
            'id="ap-modern-key-terms"', 'id="ap-modern-a11y"', 'id="ap-modern-fidelity"',
            'class="ap-standard-footer ap-modern-rich-footer"', 'id="v171-modern-parity-runtime"',
        )
        missing = [marker for marker in required if marker not in page]
        if missing:
            raise RuntimeError(f"Modern parity contract incomplete for {slug}: {missing}")
        if page.count('data-quick-assign-id=') != 1:
            raise RuntimeError(f"Modern parity changed Quick Assign surface count: {slug}")
    predecessor.quick.base.base.impl.base.validate_local_references()


def build_site() -> None:
    predecessor.build_site()
    data = load_data()
    for slug in MODERN:
        patch(slug, data)
    validate()
    print("Built v1.7.1 modern-lab parity candidate without changing AI algorithms or assignment state")


if __name__ == "__main__":
    build_site()
