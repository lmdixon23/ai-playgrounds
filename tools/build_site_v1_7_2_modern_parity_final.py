#!/usr/bin/env python3
from __future__ import annotations

"""Final validation wrapper for the v1.7.2 modern-lab parity candidate.

This layer standardizes suite-level affordances around Labs 13-15 without
changing Transformer arithmetic, agent-runtime semantics, Minimax/Alpha-Beta
results, Guided Challenges, or Quick Assign response state.
"""

import html as html_lib
import json
import re

import build_site_v1_7_2_modern_parity as candidate

SITE = candidate.SITE
MODERN = candidate.MODERN
ESTABLISHED_PORTFOLIO = "https://lmdixon23.github.io/"
ESTABLISHED_ORCID = "https://orcid.org/0009-0001-0592-462X"
PUBLIC_ROOT = "https://lmdixon23.github.io/ai-playgrounds/"
OG_IMAGE = PUBLIC_ROOT + "og-image.png"
FAVICON = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%230284c7'/%3E%3Cpath d='M13 10l9 6-9 6z' fill='%23ffffff'/%3E%3C/svg%3E"
SETTINGS_LABELS = {
    "en": "Current settings (.json)",
    "zh": "当前设置（.json）",
    "vi": "Cài đặt hiện tại (.json)",
    "es": "Configuración actual (.json)",
}
THEME_LABELS = {
    "en": "Toggle dark or light theme",
    "zh": "切换深色或浅色主题",
    "vi": "Chuyển giao diện tối hoặc sáng",
    "es": "Cambiar entre tema oscuro y claro",
}

TOOLBAR_STYLE = r'''<style id="v172-modern-toolbar-parity-style">
.ap-standard-header .header-prefs #ap-standard-theme{width:38px;padding:6px;justify-content:center;font-size:0;line-height:1}
.ap-standard-header .header-prefs #ap-standard-theme::first-letter{font-size:1rem}
.ap-standard-header .header-more{position:relative}
.ap-standard-header .header-more>summary{list-style:none;cursor:pointer;user-select:none;min-height:38px;display:inline-flex;align-items:center;gap:5px;padding:7px 10px;border:1px solid var(--border,#d7dde7);border-radius:8px;background:var(--card,#fff);color:var(--fg,#172033);font:inherit}
.ap-standard-header .header-more>summary::-webkit-details-marker{display:none}
.ap-standard-header .header-more-menu{position:absolute;right:0;top:calc(100% + 6px);z-index:80;min-width:220px;padding:7px;background:var(--card,#fff);border:1px solid var(--border,#d7dde7);border-radius:10px;box-shadow:0 16px 35px rgba(15,23,42,.18);display:grid;gap:5px}
.ap-standard-header .header-more-menu button{width:100%;text-align:left;justify-content:flex-start;white-space:normal}
@media(pointer:coarse){.ap-standard-header .header-more>summary{min-height:44px}.ap-standard-header .header-prefs #ap-standard-theme{min-height:44px;width:44px}}
@media(max-width:720px){.ap-standard-header .header-actions{width:100%;display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important}.ap-standard-header .header-actions>button,.ap-standard-header .header-actions>.header-more,.ap-standard-header .header-more>summary{width:100%;justify-content:center}.ap-standard-header .header-more-menu{right:auto;left:0;max-width:min(290px,90vw)}}
</style>'''


def quick_assign_surface_count(page: str) -> int:
    return len(re.findall(r'<[^>]+\bdata-quick-assign-id\s*=', page, flags=re.I))


def manifest_by_slug() -> dict[str, dict]:
    rows = json.loads((SITE / "applets.json").read_text(encoding="utf-8"))
    return {row["slug"]: row for row in rows}


def metadata_block(row: dict) -> str:
    slug = row["slug"]
    title = f'{row["title"]} | AI Playgrounds'
    description = row["desc"]
    canonical = f"{PUBLIC_ROOT}playgrounds/{slug}/"
    alternates = "".join(
        f'<link rel="alternate" hreflang="{lang}" href="{canonical}?lang={query}">\n'
        for lang, query in (("en", "en"), ("zh-Hans", "zh"), ("vi", "vi"), ("es", "es"), ("x-default", "en"))
    )
    jsonld = {
        "@context": "https://schema.org",
        "@type": ["WebApplication", "LearningResource"],
        "name": title,
        "url": canonical,
        "description": description,
        "applicationCategory": "EducationalApplication",
        "operatingSystem": "Any (web browser)",
        "isAccessibleForFree": True,
        "inLanguage": ["en", "zh", "vi", "es"],
        "license": "https://opensource.org/licenses/MIT",
        "learningResourceType": "interactive simulation",
        "educationalLevel": ["high school", "undergraduate"],
        "isPartOf": {"@type": "WebSite", "name": "AI Playgrounds", "url": PUBLIC_ROOT},
        "author": {"@type": "Person", "name": "Logan M. Dixon", "sameAs": ESTABLISHED_ORCID},
    }
    esc = lambda value: html_lib.escape(str(value), quote=True)
    return (
        f'<meta name="description" content="{esc(description)}">\n'
        f'<meta property="og:type" content="website">\n'
        f'<meta property="og:url" content="{esc(canonical)}">\n'
        f'<meta property="og:title" content="{esc(title)}">\n'
        f'<meta property="og:description" content="{esc(description)}">\n'
        f'<meta property="og:image" content="{esc(OG_IMAGE)}">\n'
        f'<meta name="twitter:card" content="summary_large_image">\n'
        f'<meta name="twitter:title" content="{esc(title)}">\n'
        f'<meta name="twitter:description" content="{esc(description)}">\n'
        f'<meta name="twitter:image" content="{esc(OG_IMAGE)}">\n'
        f'<link rel="icon" href="{FAVICON}">\n'
        + alternates
        + '<script type="application/ld+json">'
        + json.dumps(jsonld, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
        + '</script>\n'
    )


def normalize_head_metadata(page: str, row: dict) -> str:
    head_start = page.find("<head")
    head_open_end = page.find(">", head_start)
    head_end = page.find("</head>", head_open_end)
    if min(head_start, head_open_end, head_end) < 0:
        raise RuntimeError(f'No complete <head> for {row["slug"]}')
    head = page[head_open_end + 1:head_end]

    public_title = f'{row["title"]} | AI Playgrounds'
    head, title_count = re.subn(r'<title>.*?</title>', f'<title>{html_lib.escape(public_title)}</title>', head, count=1, flags=re.S | re.I)
    if title_count != 1:
        raise RuntimeError(f'Missing title element for {row["slug"]}')

    governed_meta = (
        "description", "og:type", "og:url", "og:title", "og:description", "og:image",
        "twitter:card", "twitter:title", "twitter:description", "twitter:image",
    )
    for key in governed_meta:
        head = re.sub(
            rf'<meta\b(?=[^>]*(?:name|property)=["\']{re.escape(key)}["\'])[^>]*>\s*',
            "",
            head,
            flags=re.I,
        )
    head = re.sub(r'<link\b(?=[^>]*\brel=["\']icon["\'])[^>]*>\s*', "", head, flags=re.I)
    head = re.sub(r'<link\b(?=[^>]*\brel=["\']alternate["\'])[^>]*>\s*', "", head, flags=re.I)
    head = re.sub(r'<script\b(?=[^>]*\btype=["\']application/ld\+json["\'])[^>]*>.*?</script>\s*', "", head, flags=re.S | re.I)
    head = head.rstrip() + "\n" + metadata_block(row)
    return page[:head_open_end + 1] + head + page[head_end:]


def more_menu(data: dict) -> str:
    more_attrs = candidate.loc_attr(data, "more")
    settings_attrs = candidate.attrs(SETTINGS_LABELS)
    return (
        f'<details class="header-more" id="ap-modern-more">'
        f'<summary class="header-more-summary" {more_attrs}>••• {html_lib.escape(data["chrome"]["en"]["more"])}</summary>'
        f'<div class="header-more-menu">'
        f'<button id="ap-modern-embed" type="button" {candidate.loc_attr(data,"embed")}>📎 <span>{html_lib.escape(data["chrome"]["en"]["embed"])}</span></button>'
        f'<button id="ap-modern-settings-json" type="button" {settings_attrs}>⬇ <span>{html_lib.escape(SETTINGS_LABELS["en"])}</span></button>'
        f'</div></details>'
    )


def toolbar_runtime(data: dict) -> str:
    labels = json.dumps(THEME_LABELS, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f'''<script id="v172-modern-toolbar-runtime">
(()=>{{'use strict';const THEME_LABELS={labels};const norm=v=>{{v=String(v||'').toLowerCase();return v.startsWith('zh')?'zh':v.startsWith('vi')?'vi':v.startsWith('es')?'es':'en'}};const loc=()=>norm(document.documentElement.lang);const theme=document.getElementById('ap-standard-theme');
function paintTheme(){{if(!theme)return;const dark=document.body.classList.contains('ap-standard-dark');theme.textContent=dark?'☀️':'🌙';const label=THEME_LABELS[loc()]||THEME_LABELS.en;theme.setAttribute('aria-label',label);theme.title=label}}
function stateData(){{const values={{}};document.querySelectorAll('#ap-modern-interactive-start input,#ap-modern-interactive-start select,#ap-modern-interactive-start textarea').forEach(el=>{{if(!el.id||el.closest('[data-quick-assign-id]'))return;if(el.type==='radio'&&!el.checked)return;values[el.id]=el.type==='checkbox'?el.checked:el.value}});return{{applet:document.getElementById('ap-standard-title')?.textContent||document.title,slug:document.body.dataset.apModernParity||'',exported_at:new Date().toISOString(),values}}}}
document.getElementById('ap-modern-settings-json')?.addEventListener('click',()=>{{const data=JSON.stringify(stateData(),null,2);const blob=new Blob([data],{{type:'application/json'}});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=(document.body.dataset.apModernParity||'ai-playground')+'-settings.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);document.getElementById('ap-modern-more')?.removeAttribute('open')}});
theme?.addEventListener('click',()=>setTimeout(paintTheme,0));new MutationObserver(paintTheme).observe(document.documentElement,{{attributes:true,attributeFilter:['lang']}});document.addEventListener('click',e=>{{const more=document.getElementById('ap-modern-more');if(more?.open&&!more.contains(e.target))more.open=false}});paintTheme();
}})();</script>'''


def validate() -> None:
    for slug in MODERN:
        page = (SITE / "playgrounds" / slug / "index.html").read_text(encoding="utf-8")
        required = (
            'class="ap-modern-skip"', 'class="ap-standard-header page-header"',
            'id="ap-modern-share"', 'id="ap-modern-more"', 'id="ap-modern-embed"',
            'id="ap-modern-settings-json"', 'class="ap-modern-tldr"',
            'id="ap-modern-key-terms"', 'id="ap-modern-a11y"', 'id="ap-modern-fidelity"',
            'class="ap-standard-footer ap-modern-rich-footer"', 'id="v172-modern-parity-runtime"',
            'id="v172-modern-toolbar-runtime"', '<meta name="twitter:image"',
            '<script type="application/ld+json">', 'rel="icon"',
        )
        missing = [marker for marker in required if marker not in page]
        if missing:
            raise RuntimeError(f"Modern parity contract incomplete for {slug}: {missing}")
        count = quick_assign_surface_count(page)
        if count != 1:
            raise RuntimeError(f"Expected one Quick Assign element for {slug}, found {count}")
        if "localStorage.setItem('theme'" not in page:
            raise RuntimeError(f"Modern lab does not write the canonical theme preference: {slug}")
        if "localStorage.getItem('theme')||localStorage.getItem('ai-playgrounds-theme')" not in page:
            raise RuntimeError(f"Modern lab lacks the one-time legacy theme migration: {slug}")
        if "localStorage.removeItem('ai-playgrounds-theme')" not in page:
            raise RuntimeError(f"Modern lab does not retire the legacy theme key: {slug}")
        if "localStorage.setItem('ai-playgrounds-theme'" in page:
            raise RuntimeError(f"Modern lab still writes the legacy theme key: {slug}")
        prefs_start = page.find('<div class="header-prefs">')
        prefs_end = page.find('</div>', prefs_start)
        theme_pos = page.find('id="ap-standard-theme"')
        if not (prefs_start >= 0 and prefs_start < theme_pos < prefs_end):
            raise RuntimeError(f"Theme control is not in the shared header preference row: {slug}")
        actions_start = page.find('<div class="header-actions">')
        share_pos = page.find('id="ap-modern-share"')
        more_pos = page.find('id="ap-modern-more"')
        reset_pos = page.find('id="ap-standard-reset"')
        if not (actions_start >= 0 and actions_start < share_pos < more_pos < reset_pos):
            raise RuntimeError(f"Modern action hierarchy is not Share / More / Reset: {slug}")
        for hreflang in ("en", "zh-Hans", "vi", "es", "x-default"):
            if f'hreflang="{hreflang}"' not in page:
                raise RuntimeError(f"Missing {hreflang} alternate for {slug}")
    candidate.core.validate_local_references()


def normalize_shell_provenance_toolbar_and_metadata() -> None:
    rows = manifest_by_slug()
    data = candidate.load_data()
    for slug in MODERN:
        path = SITE / "playgrounds" / slug / "index.html"
        page = path.read_text(encoding="utf-8")

        page = page.replace("https://logandixon.me", ESTABLISHED_PORTFOLIO)
        page = page.replace("https://orcid.org/0009-0008-1712-6630", ESTABLISHED_ORCID)
        # Match the established preference row. The v1.7.1 predecessor owns
        # system-theme fallback and one-time migration from the temporary key.
        theme_match = re.search(r'<button\b[^>]*\bid="ap-standard-theme"[^>]*>.*?</button>', page, flags=re.S | re.I)
        if not theme_match:
            raise RuntimeError(f"Modern theme control missing before hierarchy normalization: {slug}")
        theme_button = theme_match.group(0)
        page = page[:theme_match.start()] + page[theme_match.end():]
        prefs_marker = '<div class="header-prefs">'
        if prefs_marker not in page:
            raise RuntimeError(f"Modern header preference row missing: {slug}")
        page = page.replace(prefs_marker, prefs_marker + theme_button, 1)

        # Match the mature action hierarchy: Share, More (Embed + JSON), Reset.
        embed_match = re.search(r'<button\b[^>]*\bid="ap-modern-embed"[^>]*>.*?</button>', page, flags=re.S | re.I)
        if not embed_match:
            raise RuntimeError(f"Modern Embed action missing before More-menu normalization: {slug}")
        page = page[:embed_match.start()] + page[embed_match.end():]
        share_match = re.search(r'<button\b[^>]*\bid="ap-modern-share"[^>]*>.*?</button>', page, flags=re.S | re.I)
        if not share_match:
            raise RuntimeError(f"Modern Share action missing: {slug}")
        menu = more_menu(data)
        page = page[:share_match.end()] + menu + page[share_match.end():]

        # Keep browser title synchronized with the localized standard-shell H1.
        marker = "$('#ap-standard-title').textContent=f('title',l);"
        replacement = marker + "document.title=f('title',l)+' | AI Playgrounds';"
        if marker not in page:
            raise RuntimeError(f"Standard-shell title synchronization marker missing: {slug}")
        page = page.replace(marker, replacement, 1)

        # Original twelve keep release number in secondary provenance, not the main footer.
        page = page.replace(" · v1.7.2</div>", "</div>")
        if 'id="v172-modern-toolbar-parity-style"' not in page:
            page = page.replace("</head>", TOOLBAR_STYLE + "\n</head>", 1)
        page = normalize_head_metadata(page, rows[slug])
        page = page.replace("</body>", toolbar_runtime(data) + "\n</body>", 1)

        if ESTABLISHED_PORTFOLIO not in page or ESTABLISHED_ORCID not in page:
            raise RuntimeError(f"Established modern-lab provenance missing after normalization: {slug}")
        if "https://logandixon.me" in page or "0009-0008-1712-6630" in page:
            raise RuntimeError(f"Unapproved alternate provenance survived normalization: {slug}")
        path.write_text(page, encoding="utf-8")


def build_site() -> None:
    candidate.build_site()
    normalize_shell_provenance_toolbar_and_metadata()
    validate()
    print("Finalized v1.7.2 modern-lab parity: mature Share/More/Reset toolbar, shared theme preference, established provenance, and complete discovery metadata")


if __name__ == "__main__":
    build_site()
