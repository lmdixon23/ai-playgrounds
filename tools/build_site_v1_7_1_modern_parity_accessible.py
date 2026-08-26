#!/usr/bin/env python3
from __future__ import annotations

"""Final accessibility/localization wrapper for modern Quick Assign parity.

The v1.7.0 modern packets already own response persistence and the v1.7.1
complete wrapper owns state snapshot/copy/print behavior. This layer changes
only learner-facing action labels and textarea accessible names so locale
switching is complete without creating a second packet implementation.
"""

import json

import build_site_v1_7_1_modern_parity_complete as base

SITE = base.SITE
MODERN = base.MODERN
LABELS = {
    "en": {"predict":"Predict", "observe":"Observe", "explain":"Explain", "transfer":"Transfer", "refresh":"Refresh state", "copy":"Copy packet", "print":"Print packet", "clear":"Clear local draft"},
    "zh": {"predict":"预测", "observe":"观察", "explain":"解释", "transfer":"迁移", "refresh":"更新状态", "copy":"复制实验包", "print":"打印实验包", "clear":"清除本地草稿"},
    "vi": {"predict":"Dự đoán", "observe":"Quan sát", "explain":"Giải thích", "transfer":"Chuyển giao", "refresh":"Làm mới trạng thái", "copy":"Sao chép gói bài", "print":"In gói bài", "clear":"Xóa bản nháp cục bộ"},
    "es": {"predict":"Predecir", "observe":"Observar", "explain":"Explicar", "transfer":"Transferir", "refresh":"Actualizar estado", "copy":"Copiar paquete", "print":"Imprimir paquete", "clear":"Borrar borrador local"},
}


def runtime() -> str:
    data = json.dumps(LABELS, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f'''<script id="v171-modern-packet-label-runtime">
(()=>{{'use strict';const COPY={data};const root=document.querySelector('[data-quick-assign-id]');if(!root)return;const norm=v=>{{v=String(v||'').toLowerCase();return v.startsWith('zh')?'zh':v.startsWith('vi')?'vi':v.startsWith('es')?'es':'en'}};const locale=()=>norm(document.documentElement.lang);function paint(){{const l=COPY[locale()]||COPY.en;root.querySelectorAll('[data-qa-answer]').forEach(el=>{{const key=el.dataset.qaAnswer;if(l[key])el.setAttribute('aria-label',l[key])}});for(const key of ['refresh','copy','print','clear']){{const action=key==='refresh'?'refresh-state':key;const button=root.querySelector('[data-qa-action="'+action+'"]');if(!button)continue;const label=l[key]||COPY.en[key];button.textContent=(key==='refresh'?'↻ ':'')+label;button.setAttribute('aria-label',label)}}const state=root.querySelector('[data-qa-modern-state]');if(state)state.setAttribute('aria-label',(baseState=>baseState)(locale()==='zh'?'状态记录':locale()==='vi'?'Ảnh chụp trạng thái':locale()==='es'?'Captura del estado':'State snapshot'))}}new MutationObserver(()=>setTimeout(paint,0)).observe(document.documentElement,{{attributes:true,attributeFilter:['lang']}});window.addEventListener('lab13localechange',()=>setTimeout(paint,0));window.addEventListener('lab14localechange',()=>setTimeout(paint,0));window.addEventListener('lab15localechange',()=>setTimeout(paint,0));paint();
}})();</script>'''


def validate() -> None:
    for slug in MODERN:
        page = (SITE / "playgrounds" / slug / "index.html").read_text(encoding="utf-8")
        if page.count('id="v171-modern-packet-label-runtime"') != 1:
            raise RuntimeError(f"Modern packet label runtime missing or duplicated: {slug}")
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
    print("Completed v1.7.1 modern Quick Assign label parity across EN/ZH/VI/ES")


if __name__ == "__main__":
    build_site()
