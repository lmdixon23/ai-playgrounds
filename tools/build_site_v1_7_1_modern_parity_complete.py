#!/usr/bin/env python3
from __future__ import annotations

"""Complete v1.7.1 modern-lab parity composition.

Adds the remaining shared Quick Assign affordances to Labs 13-15 by reading
their existing text-equivalent state. No algorithmic state, challenge logic, or
learner-response storage schema is changed.
"""

import html as html_lib
import json
import re

import build_site_v1_7_1_modern_parity_final as base

SITE = base.SITE
MODERN = base.MODERN
STATE_SOURCE = {
    "transformer-language-model": "stateText",
    "agent-tool-context": "stateText",
    "minimax-alpha-beta": "textState",
}
PACK = {
    "en": {"state":"State snapshot", "empty":"State snapshot appears here.", "refresh":"Refresh state", "copy":"Copy packet", "print":"Print packet", "predict":"Predict", "observe":"Observe", "explain":"Explain", "transfer":"Transfer", "copied":"Copied local lab packet.", "popup":"Popup blocked. Copy the packet instead."},
    "zh": {"state":"状态记录", "empty":"状态记录会显示在这里。", "refresh":"更新状态", "copy":"复制实验包", "print":"打印实验包", "predict":"预测", "observe":"观察", "explain":"解释", "transfer":"迁移", "copied":"已复制本地实验包。", "popup":"弹窗被拦截。请改用复制实验包。"},
    "vi": {"state":"Ảnh chụp trạng thái", "empty":"Ảnh chụp trạng thái sẽ xuất hiện ở đây.", "refresh":"Làm mới trạng thái", "copy":"Sao chép gói bài", "print":"In gói bài", "predict":"Dự đoán", "observe":"Quan sát", "explain":"Giải thích", "transfer":"Chuyển giao", "copied":"Đã sao chép gói bài cục bộ.", "popup":"Cửa sổ bật lên bị chặn. Hãy sao chép gói bài thay thế."},
    "es": {"state":"Captura del estado", "empty":"La captura del estado aparecerá aquí.", "refresh":"Actualizar estado", "copy":"Copiar paquete", "print":"Imprimir paquete", "predict":"Predecir", "observe":"Observar", "explain":"Explicar", "transfer":"Transferir", "copied":"Paquete local copiado.", "popup":"Ventana emergente bloqueada. Copia el paquete en su lugar."},
}

STYLE = r'''<style id="v171-modern-quick-assign-parity-style">
.quick-assign-modern.classroom-lab{margin:8px 0!important;padding:0!important;background:transparent!important;border:0!important;border-radius:0!important;overflow:visible!important}
.quick-assign-modern.classroom-lab>summary{cursor:pointer;padding:10px 12px!important;background:var(--card)!important;border:1px solid var(--border)!important;border-left:4px solid color-mix(in srgb,var(--accent) 62%,var(--border))!important;border-radius:10px!important;color:var(--fg)!important;font:750 .88rem -apple-system,system-ui,sans-serif!important}
.quick-assign-modern.classroom-lab[open]>summary{border-color:color-mix(in srgb,var(--accent) 55%,var(--border))!important}
.quick-assign-modern .quick-assign-modern-body.lab-panel{margin-top:8px;padding:14px;background:var(--card);border:1px solid var(--border);border-radius:8px}
.quick-assign-modern .qa-modern-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px;margin-top:10px}
.quick-assign-modern .qa-modern-field.lab-field{display:flex;margin:0;flex-direction:column;gap:4px}
.quick-assign-modern .qa-modern-field.lab-field>strong{font-family:-apple-system,system-ui,sans-serif;font-size:.82rem;font-weight:700;color:var(--accent)}
.quick-assign-modern .qa-modern-field textarea{min-height:86px;resize:vertical;width:100%;border:1px solid var(--border);border-radius:6px;padding:8px;font:inherit;color:var(--fg);background:var(--bg)}
.quick-assign-modern .qa-modern-state{margin-top:12px;padding:10px 12px;border:1px dashed var(--border);border-radius:8px;background:var(--soft);color:var(--muted);font-family:ui-monospace,monospace;font-size:.78rem;white-space:pre-wrap;max-height:250px;overflow:auto}
.quick-assign-modern .challenge-controls.lab-actions{display:flex!important;flex-wrap:wrap!important;gap:8px;margin-top:12px;align-items:center}
.quick-assign-modern .lab-status{color:var(--muted);font-size:.82rem;min-height:1.2em}
@media(max-width:480px){.quick-assign-modern .qa-modern-grid{grid-template-columns:1fr}.quick-assign-modern .challenge-controls.lab-actions button{width:100%}}
</style>'''


def loc_attrs(key: str) -> str:
    return base.candidate.attrs({locale: PACK[locale][key] for locale in ("en", "zh", "vi", "es")})


def patch_markup(page: str, slug: str) -> str:
    marker = f'data-quick-assign-id="{re.escape({"transformer-language-model":"QA-TRANSFORMER-01","agent-tool-context":"QA-AGENT-01","minimax-alpha-beta":"QA-MINIMAX-01"}[slug])}"'
    # Locate the actual modern Quick Assign details element around its unique ID.
    start_match = re.search(r'<details\b[^>]*\bclass="[^"]*quick-assign-modern[^"]*"[^>]*\bdata-quick-assign-id="[^"]+"[^>]*>', page, flags=re.I)
    if not start_match:
        # Attribute order in the generated artifact may place data before class.
        start_match = re.search(r'<details\b(?=[^>]*\bclass="[^"]*quick-assign-modern[^"]*")(?=[^>]*\bdata-quick-assign-id="[^"]+")[^>]*>', page, flags=re.I)
    if not start_match:
        raise RuntimeError(f"Modern Quick Assign start tag missing: {slug}")
    end = page.find('</details>', start_match.end())
    if end < 0:
        raise RuntimeError(f"Modern Quick Assign end tag missing: {slug}")
    end += len('</details>')
    segment = page[start_match.start():end]
    if 'data-qa-modern-state' in segment:
        raise RuntimeError(f"Modern state snapshot would be applied twice: {slug}")

    segment = re.sub(
        r'<details\b([^>]*\bclass=")([^"]*\bquick-assign-modern\b[^"]*)("[^>]*)>',
        lambda m: '<details' + m.group(1) + (m.group(2) + ' classroom-lab quick-assign').replace('  ', ' ') + m.group(3) + '>',
        segment, count=1, flags=re.I,
    )
    segment = segment.replace('class="quick-assign-modern-body"', 'class="quick-assign-modern-body lab-panel"', 1)
    segment = segment.replace('class="qa-modern-field"', 'class="qa-modern-field lab-field"')

    first_field = segment.find('<label class="qa-modern-field lab-field">')
    actions = segment.find('<div class="challenge-controls">')
    if first_field < 0 or actions < 0 or actions <= first_field:
        raise RuntimeError(f"Modern Quick Assign field/action markers missing: {slug}")
    segment = segment[:first_field] + '<div class="qa-modern-grid">' + segment[first_field:actions] + '</div>' + segment[actions:]
    segment = segment.replace('<div class="challenge-controls">', '<div class="challenge-controls lab-actions">', 1)

    state = (
        f'<div class="qa-modern-state lab-state" data-qa-modern-state aria-live="polite" {loc_attrs("empty")}>{html_lib.escape(PACK["en"]["empty"])}</div>'
    )
    refresh = (
        f'<button type="button" data-qa-action="refresh-state" {loc_attrs("refresh")}>↻ <span>{html_lib.escape(PACK["en"]["refresh"])}</span></button>'
    )
    actions_marker = '<div class="challenge-controls lab-actions">'
    segment = segment.replace(actions_marker, state + actions_marker + refresh, 1)
    status = '<span class="lab-status" data-qa-modern-status aria-live="polite"></span>'
    segment = segment.replace('</div></div></details>', status + '</div></div></details>', 1)

    return page[:start_match.start()] + segment + page[end:]


def packet_runtime(slug: str) -> str:
    data = json.dumps(PACK, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    source_id = STATE_SOURCE[slug]
    return f'''<script id="v171-modern-packet-runtime">
(()=>{{'use strict';const COPY={data};const root=document.querySelector('[data-quick-assign-id]');if(!root)return;const source=document.getElementById({json.dumps(source_id)});const state=root.querySelector('[data-qa-modern-state]');const status=root.querySelector('[data-qa-modern-status]');const norm=v=>{{v=String(v||'').toLowerCase();return v.startsWith('zh')?'zh':v.startsWith('vi')?'vi':v.startsWith('es')?'es':'en'}};const locale=()=>norm(document.documentElement.lang);const labels=()=>COPY[locale()]||COPY.en;
function refresh(){{if(!state)return;const value=(source?.textContent||'').trim();state.textContent=value||labels().empty}}
function answers(){{const out={{}};root.querySelectorAll('[data-qa-answer]').forEach(el=>out[el.dataset.qaAnswer]=(el.value||'').trim());return out}}
function packet(){{const l=labels(),a=answers();return['# '+(document.getElementById('ap-standard-title')?.textContent||document.title),'','## '+l.state,(state?.textContent||l.empty),'','## '+l.predict,a.predict||'','','## '+l.observe,a.observe||'','','## '+l.explain,a.explain||'','','## '+l.transfer,a.transfer||''].join('\\n')}}
function setStatus(text){{if(status)status.textContent=text}}
async function copyPacket(){{const text=packet();try{{await navigator.clipboard.writeText(text);setStatus(labels().copied)}}catch(_e){{window.prompt('Copy this lab packet:',text)}}}}
function printable(markdown){{const esc=v=>String(v).replace(/[&<>"']/g,ch=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[ch]));return String(markdown).split(/\\r?\\n/).map(line=>{{if(line.startsWith('# '))return'<h1>'+esc(line.slice(2))+'</h1>';if(line.startsWith('## '))return'<h2>'+esc(line.slice(3))+'</h2>';if(!line.trim())return'';return'<p>'+esc(line)+'</p>'}}).join('')}}
function printPacket(){{const w=window.open('','_blank');if(!w){{setStatus(labels().popup);return}}const body=printable(packet());w.document.open();w.document.write('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Lab packet</title><style>@page{{size:A4;margin:14mm}}body{{font-family:system-ui,sans-serif;max-width:820px;margin:28px auto;line-height:1.45;padding:0 18px;color:#111827}}h1{{font-size:1.6rem}}h2{{font-size:1.05rem;margin-top:18px;border-bottom:1px solid #dbe4ee;padding-bottom:4px}}p{{white-space:pre-wrap}}@media print{{body{{margin:0;max-width:none;padding:0}}}}</style></head><body>'+body+'</body></html>');w.document.close();setTimeout(()=>{{try{{w.focus();w.print()}}catch(_e){{}}}},250)}}
root.addEventListener('click',event=>{{const button=event.target?.closest?.('[data-qa-action]');if(!button)return;const action=button.dataset.qaAction;if(action==='refresh-state'||action==='copy'||action==='print'){{event.preventDefault();event.stopImmediatePropagation();if(action==='refresh-state')refresh();if(action==='copy')copyPacket();if(action==='print')printPacket()}}}},true);
new MutationObserver(()=>setTimeout(refresh,0)).observe(document.documentElement,{{attributes:true,attributeFilter:['lang']}});refresh();
}})();</script>'''


def validate() -> None:
    for slug in MODERN:
        source = (SITE / "playgrounds" / slug / "index.html").read_text(encoding="utf-8")
        required = (
            'class="card quick-assign-modern classroom-lab quick-assign"',
            'class="quick-assign-modern-body lab-panel"',
            'class="qa-modern-grid"',
            'data-qa-modern-state',
            'data-qa-action="refresh-state"',
            'class="challenge-controls lab-actions"',
            'data-qa-modern-status',
            'id="v171-modern-packet-runtime"',
        )
        missing = [m for m in required if m not in source]
        if missing:
            raise RuntimeError(f"Modern Quick Assign parity incomplete for {slug}: {missing}")
        if source.count('data-qa-modern-state') < 1:
            raise RuntimeError(f"No modern state snapshot: {slug}")
    base.validate()


def build_site() -> None:
    base.build_site()
    for slug in MODERN:
        path = SITE / "playgrounds" / slug / "index.html"
        page = path.read_text(encoding="utf-8")
        if 'id="v171-modern-quick-assign-parity-style"' not in page:
            page = page.replace('</head>', STYLE + '\n</head>', 1)
        page = patch_markup(page, slug)
        page = page.replace('</body>', packet_runtime(slug) + '\n</body>', 1)
        path.write_text(page, encoding="utf-8")
    validate()
    print("Completed v1.7.1 modern Quick Assign parity with state snapshot, refresh, packet copy, and packet-only print")


if __name__ == "__main__":
    build_site()
