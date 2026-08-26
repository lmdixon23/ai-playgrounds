#!/usr/bin/env python3
from __future__ import annotations

"""Final accessibility/localization wrapper for modern Quick Assign parity.

The v1.7.0 modern packets own response persistence and the v1.7.1 complete
wrapper owns state snapshot/copy/print behavior. This layer changes only
learner-facing action labels and textarea accessible names. It deliberately
re-applies those labels after the legacy modern Quick Assign localization
callbacks, whose delayed paints can otherwise restore English labels after a
VI/ES locale switch.
"""

import json

import build_site_v1_7_1_modern_parity_complete as base

SITE = base.SITE
MODERN = base.MODERN
LABELS = {
    "en": {"predict":"Predict", "observe":"Observe", "explain":"Explain", "transfer":"Transfer", "refresh":"Refresh state", "copy":"Copy packet", "print":"Print packet", "clear":"Clear local draft", "state":"State snapshot"},
    "zh": {"predict":"预测", "observe":"观察", "explain":"解释", "transfer":"迁移", "refresh":"更新状态", "copy":"复制实验包", "print":"打印实验包", "clear":"清除本地草稿", "state":"状态记录"},
    "vi": {"predict":"Dự đoán", "observe":"Quan sát", "explain":"Giải thích", "transfer":"Chuyển giao", "refresh":"Làm mới trạng thái", "copy":"Sao chép gói bài", "print":"In gói bài", "clear":"Xóa bản nháp cục bộ", "state":"Ảnh chụp trạng thái"},
    "es": {"predict":"Predecir", "observe":"Observar", "explain":"Explicar", "transfer":"Transferir", "refresh":"Actualizar estado", "copy":"Copiar paquete", "print":"Imprimir paquete", "clear":"Borrar borrador local", "state":"Captura del estado"},
}


def runtime() -> str:
    data = json.dumps(LABELS, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f'''<script id="v171-modern-packet-label-runtime">
(()=>{{'use strict';
const COPY={data};
const root=document.querySelector('[data-quick-assign-id]');
if(!root)return;
const norm=v=>{{v=String(v||'').toLowerCase();return v.startsWith('zh')?'zh':v.startsWith('vi')?'vi':v.startsWith('es')?'es':'en'}};
const locale=()=>norm(document.documentElement.lang);
let paintToken=0;
function paint(){{
  const l=COPY[locale()]||COPY.en;
  root.querySelectorAll('[data-qa-answer]').forEach(el=>{{const key=el.dataset.qaAnswer;if(l[key])el.setAttribute('aria-label',l[key])}});
  for(const key of ['refresh','copy','print','clear']){{
    const action=key==='refresh'?'refresh-state':key;
    const button=root.querySelector('[data-qa-action="'+action+'"]');
    if(!button)continue;
    const label=l[key]||COPY.en[key];
    button.textContent=(key==='refresh'?'↻ ':'')+label;
    button.setAttribute('aria-label',label);
  }}
  const state=root.querySelector('[data-qa-modern-state]');
  if(state)state.setAttribute('aria-label',l.state||COPY.en.state);
}}
function schedulePaint(){{
  const token=++paintToken;
  const run=()=>{{if(token===paintToken)paint()}};
  run();
  queueMicrotask(run);
  if(window.requestAnimationFrame)requestAnimationFrame(run);
  setTimeout(run,20);
  setTimeout(run,55);
  setTimeout(run,95);
}}
function wrapApi(name){{
  const install=()=>{{
    const api=window[name];
    if(!api||typeof api.setLocale!=='function')return false;
    if(api.setLocale.__v171LabelWrapped)return true;
    const original=api.setLocale.bind(api);
    const wrapped=function(...args){{const result=original(...args);schedulePaint();return result}};
    wrapped.__v171LabelWrapped=true;
    api.setLocale=wrapped;
    return true;
  }};
  if(!install()){{let tries=0;const timer=setInterval(()=>{{tries+=1;if(install()||tries>80)clearInterval(timer)}},25)}}
}}
for(const name of ['Lab13Localization','Lab14Localization','Lab15Localization'])wrapApi(name);
new MutationObserver(schedulePaint).observe(document.documentElement,{{attributes:true,attributeFilter:['lang']}});
window.addEventListener('lab13localechange',schedulePaint);
window.addEventListener('lab14localechange',schedulePaint);
window.addEventListener('lab15localechange',schedulePaint);
schedulePaint();
}})();</script>'''


def validate() -> None:
    for slug in MODERN:
        page = (SITE / "playgrounds" / slug / "index.html").read_text(encoding="utf-8")
        if page.count('id="v171-modern-packet-label-runtime"') != 1:
            raise RuntimeError(f"Modern packet label runtime missing or duplicated: {slug}")
        for marker in ("schedulePaint", "__v171LabelWrapped", "setTimeout(run,95)"):
            if marker not in page:
                raise RuntimeError(f"Modern packet label last-writer guard missing for {slug}: {marker}")
    base.validate()


def build_site() -> None:
    base.build_site()
    script = runtime()
    for slug in MODERN:
        path = SITE / "playgrounds" / slug / "index.html"
        page = path.read_text(encoding="utf-8")
        if 'id="v171-modern-packet-label-runtime"' in page:
            raise RuntimeError(f"Modern packet label layer would be applied twice: {slug}")
        page = page.replace("</body>", script + "\n</body>", 1)
        path.write_text(page, encoding="utf-8")
    validate()
    print("Completed v1.7.1 modern Quick Assign label parity with deterministic post-localization repaint")


if __name__ == "__main__":
    build_site()
