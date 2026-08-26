#!/usr/bin/env python3
from __future__ import annotations

"""Final accessibility/localization wrapper for modern-lab parity.

The v1.7.0 modern packets own response persistence and the v1.7.1 complete
wrapper owns state snapshot/copy/print behavior. This layer supplies the
remaining mature-suite accessibility contract without creating new algorithmic
state: localized Quick Assign accessible names plus an open keyboard/text-state
panel that mirrors each modern lab's existing stateText/textState output.
"""

import json
import re

import build_site_v1_7_1_modern_parity_complete as base

SITE = base.SITE
MODERN = base.MODERN
LABELS = {
    "en": {"predict":"Predict", "observe":"Observe", "explain":"Explain", "transfer":"Transfer", "refresh":"Refresh state", "copy":"Copy packet", "print":"Print packet", "clear":"Clear local draft", "state":"State snapshot"},
    "zh": {"predict":"预测", "observe":"观察", "explain":"解释", "transfer":"迁移", "refresh":"更新状态", "copy":"复制实验包", "print":"打印实验包", "clear":"清除本地草稿", "state":"状态记录"},
    "vi": {"predict":"Dự đoán", "observe":"Quan sát", "explain":"Giải thích", "transfer":"Chuyển giao", "refresh":"Làm mới trạng thái", "copy":"Sao chép gói bài", "print":"In gói bài", "clear":"Xóa bản nháp cục bộ", "state":"Ảnh chụp trạng thái"},
    "es": {"predict":"Predecir", "observe":"Observar", "explain":"Explicar", "transfer":"Transferir", "refresh":"Actualizar estado", "copy":"Copiar paquete", "print":"Imprimir paquete", "clear":"Borrar borrador local", "state":"Captura del estado"},
}
A11Y = {
    "en": {
        "summary":"♿ Text and keyboard support",
        "title":"Text and keyboard support",
        "intro":"Use the controls by keyboard and read the same current model state as text. The text state below mirrors the lab's existing accessible numeric state; it does not create a second simulation state.",
        "keyboard":"Keyboard path",
        "k1":"Use Tab and Shift+Tab to move through controls.",
        "k2":"Use Enter or Space on buttons, and arrow keys on sliders or select controls.",
        "k3":"Use the text-state panel when color, animation, or spatial position is not available.",
        "state":"Text state summary",
        "state_wait":"Current text state is preparing…",
        "motion":"Reduced motion and non-visual support",
        "motion_copy":"Reduced-motion preferences are honored where the lab animates. Important numeric results remain available in text, so the main result does not depend only on color or motion.",
        "note":"Accessibility note: this is a structured text equivalent and keyboard-support layer. It does not replace a full human assistive-technology audit.",
    },
    "zh": {
        "summary":"♿ 文本与键盘支持",
        "title":"文本与键盘支持",
        "intro":"可以使用键盘操作控件，并以文本读取同一个当前模型状态。下方文本直接镜像实验原有的无障碍数值状态，不会创建第二套模拟状态。",
        "keyboard":"键盘操作路径",
        "k1":"使用 Tab 和 Shift+Tab 在控件之间移动。",
        "k2":"按钮使用 Enter 或空格键；滑块和选择控件使用方向键。",
        "k3":"当颜色、动画或空间位置不可用时，请使用文本状态面板。",
        "state":"文本状态摘要",
        "state_wait":"正在准备当前文本状态…",
        "motion":"减少动态效果与非视觉支持",
        "motion_copy":"实验包含动画时会尊重减少动态效果的系统偏好。重要数值结果同时以文本提供，因此主要结论不只依赖颜色或动画。",
        "note":"无障碍说明：此层提供结构化文本等价信息和键盘支持，但不能替代完整的人工辅助技术审计。",
    },
    "vi": {
        "summary":"♿ Hỗ trợ văn bản và bàn phím",
        "title":"Hỗ trợ văn bản và bàn phím",
        "intro":"Dùng bàn phím để điều khiển và đọc cùng một trạng thái mô hình hiện tại dưới dạng văn bản. Trạng thái bên dưới phản chiếu trực tiếp trạng thái số có thể truy cập đã có của lab; nó không tạo trạng thái mô phỏng thứ hai.",
        "keyboard":"Lộ trình bàn phím",
        "k1":"Dùng Tab và Shift+Tab để di chuyển giữa các điều khiển.",
        "k2":"Dùng Enter hoặc Space cho nút; dùng phím mũi tên cho thanh trượt và ô chọn.",
        "k3":"Dùng bảng trạng thái văn bản khi không thể dựa vào màu sắc, chuyển động hoặc vị trí không gian.",
        "state":"Tóm tắt trạng thái dạng văn bản",
        "state_wait":"Đang chuẩn bị trạng thái văn bản hiện tại…",
        "motion":"Giảm chuyển động và hỗ trợ phi trực quan",
        "motion_copy":"Tùy chọn giảm chuyển động được tôn trọng ở nơi lab có hoạt ảnh. Các kết quả số quan trọng vẫn có dạng văn bản, nên kết quả chính không chỉ phụ thuộc vào màu sắc hoặc chuyển động.",
        "note":"Lưu ý khả năng truy cập: lớp này cung cấp văn bản tương đương có cấu trúc và hỗ trợ bàn phím; nó không thay thế một cuộc kiểm tra thủ công đầy đủ bằng công nghệ hỗ trợ.",
    },
    "es": {
        "summary":"♿ Soporte de texto y teclado",
        "title":"Soporte de texto y teclado",
        "intro":"Usa el teclado para operar los controles y lee como texto el mismo estado actual del modelo. El estado inferior refleja el estado numérico accesible que ya posee el laboratorio; no crea un segundo estado de simulación.",
        "keyboard":"Recorrido con teclado",
        "k1":"Usa Tab y Shift+Tab para desplazarte entre los controles.",
        "k2":"Usa Enter o Espacio en los botones y las flechas en deslizadores y controles de selección.",
        "k3":"Usa el panel de estado textual cuando no estén disponibles el color, la animación o la posición espacial.",
        "state":"Resumen textual del estado",
        "state_wait":"Preparando el estado textual actual…",
        "motion":"Movimiento reducido y soporte no visual",
        "motion_copy":"Se respeta la preferencia de movimiento reducido donde el laboratorio usa animación. Los resultados numéricos importantes también están disponibles como texto, por lo que el resultado principal no depende solo del color o del movimiento.",
        "note":"Nota de accesibilidad: esta capa ofrece un equivalente textual estructurado y soporte de teclado; no sustituye una auditoría humana completa con tecnologías de asistencia.",
    },
}

A11Y_STYLE = r'''<style id="v171-modern-a11y-parity-style">
.ap-modern-a11y-parity .ap-support-body{padding-top:2px}
.ap-modern-a11y-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
.ap-modern-a11y-card{border:1px solid var(--border,#d7dde7);border-radius:8px;padding:10px;background:var(--soft,#f8fafc);min-width:0}
.ap-modern-a11y-card h3{margin:0 0 6px;font-size:.86rem;color:var(--fg,#172033)}
.ap-modern-a11y-card ul{margin:0;padding-left:20px}.ap-modern-a11y-card li{margin:4px 0}
.ap-modern-a11y-state-card{grid-column:1/-1}
.ap-modern-a11y-state{margin:7px 0 0;max-height:260px;overflow:auto;white-space:pre-wrap;overflow-wrap:anywhere;border:1px dashed var(--border,#d7dde7);border-radius:7px;padding:9px;background:var(--card,#fff);color:var(--fg,#172033);font:12px/1.5 ui-monospace,SFMono-Regular,Consolas,monospace}
.ap-modern-a11y-note{margin:10px 0 0;font-size:.8rem;color:var(--muted,#637083)}
.ap-modern-sr-only{position:absolute!important;width:1px!important;height:1px!important;padding:0!important;margin:-1px!important;overflow:hidden!important;clip:rect(0,0,0,0)!important;white-space:nowrap!important;border:0!important}
@media(max-width:680px){.ap-modern-a11y-grid{grid-template-columns:1fr}.ap-modern-a11y-state-card{grid-column:auto}}
@media(prefers-reduced-motion:reduce){.ap-modern-a11y-parity *{scroll-behavior:auto!important;transition:none!important;animation:none!important}}
</style>'''


def attrs(values: dict[str, str]) -> str:
    import html as html_lib
    return " ".join(
        f'data-ap-{locale}="{html_lib.escape(str(text), quote=True)}"'
        for locale, text in values.items()
    )


def a11y_attrs(key: str) -> str:
    return attrs({locale: A11Y[locale][key] for locale in ("en", "zh", "vi", "es")})


def structured_a11y() -> str:
    import html as html_lib
    en = A11Y["en"]
    return f'''<details id="ap-modern-a11y" class="accessibility-layer ap-modern-a11y-parity" open>
<summary {a11y_attrs("summary")}>{html_lib.escape(en["summary"])}</summary>
<div class="ap-support-body" role="region" aria-labelledby="ap-modern-a11y-title">
<h2 id="ap-modern-a11y-title" class="ap-modern-sr-only" {a11y_attrs("title")}>{html_lib.escape(en["title"])}</h2>
<p {a11y_attrs("intro")}>{html_lib.escape(en["intro"])}</p>
<div class="ap-modern-a11y-grid">
<section class="ap-modern-a11y-card" aria-labelledby="ap-modern-a11y-keyboard-title">
<h3 id="ap-modern-a11y-keyboard-title" {a11y_attrs("keyboard")}>{html_lib.escape(en["keyboard"])}</h3>
<ul><li {a11y_attrs("k1")}>{html_lib.escape(en["k1"])}</li><li {a11y_attrs("k2")}>{html_lib.escape(en["k2"])}</li><li {a11y_attrs("k3")}>{html_lib.escape(en["k3"])}</li></ul>
</section>
<section class="ap-modern-a11y-card" aria-labelledby="ap-modern-a11y-motion-title">
<h3 id="ap-modern-a11y-motion-title" {a11y_attrs("motion")}>{html_lib.escape(en["motion"])}</h3>
<p {a11y_attrs("motion_copy")}>{html_lib.escape(en["motion_copy"])}</p>
</section>
<section class="ap-modern-a11y-card ap-modern-a11y-state-card" aria-labelledby="ap-modern-a11y-state-title">
<h3 id="ap-modern-a11y-state-title" {a11y_attrs("state")}>{html_lib.escape(en["state"])}</h3>
<pre id="ap-modern-a11y-state" class="ap-modern-a11y-state" aria-live="polite" tabindex="0" {a11y_attrs("state_wait")}>{html_lib.escape(en["state_wait"])}</pre>
</section>
</div>
<p class="ap-modern-a11y-note" {a11y_attrs("note")}>{html_lib.escape(en["note"])}</p>
<span id="ap-modern-a11y-live" class="ap-modern-sr-only" role="status" aria-live="polite" aria-atomic="true"></span>
</div></details>'''


def runtime(slug: str) -> str:
    data = json.dumps(LABELS, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    source_id = base.STATE_SOURCE[slug]
    return f'''<script id="v171-modern-packet-label-runtime">
(()=>{{'use strict';
const COPY={data};
const root=document.querySelector('[data-quick-assign-id]');
if(!root)return;
const stateSource=document.getElementById({json.dumps(source_id)});
const a11yState=document.getElementById('ap-modern-a11y-state');
const a11yLive=document.getElementById('ap-modern-a11y-live');
const norm=v=>{{v=String(v||'').toLowerCase();return v.startsWith('zh')?'zh':v.startsWith('vi')?'vi':v.startsWith('es')?'es':'en'}};
const locale=()=>norm(document.documentElement.lang);
let paintToken=0;
function syncAccessibleState(){{
  if(!a11yState||!stateSource)return;
  const next=(stateSource.textContent||'').trim();
  if(!next)return;
  if(a11yState.textContent!==next){{a11yState.textContent=next;if(a11yLive)a11yLive.textContent=next.slice(0,500)}}
}}
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
  syncAccessibleState();
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
if(stateSource)new MutationObserver(syncAccessibleState).observe(stateSource,{{childList:true,subtree:true,characterData:true}});
new MutationObserver(schedulePaint).observe(document.documentElement,{{attributes:true,attributeFilter:['lang']}});
window.addEventListener('lab13localechange',schedulePaint);
window.addEventListener('lab14localechange',schedulePaint);
window.addEventListener('lab15localechange',schedulePaint);
schedulePaint();
}})();</script>'''


def insert_before_document_close(page: str, close_tag: str, addition: str, slug: str) -> str:
    """Insert at the actual final document closing tag, not inside JS HTML strings."""
    close = page.lower().rfind(close_tag.lower())
    if close < 0:
        raise RuntimeError(f"Document closing tag {close_tag} missing: {slug}")
    return page[:close] + addition + "\n" + page[close:]


def replace_compact_a11y(page: str, slug: str) -> str:
    pattern = re.compile(r'<details\b[^>]*\bid="ap-modern-a11y"[^>]*>.*?</details>', re.S | re.I)
    page, count = pattern.subn(structured_a11y(), page, count=1)
    if count != 1:
        raise RuntimeError(f"Compact modern accessibility disclosure missing: {slug}")
    return page


def validate() -> None:
    for slug in MODERN:
        page = (SITE / "playgrounds" / slug / "index.html").read_text(encoding="utf-8")
        if page.count('id="v171-modern-packet-label-runtime"') != 1:
            raise RuntimeError(f"Modern packet label runtime missing or duplicated: {slug}")
        for marker in (
            "schedulePaint", "__v171LabelWrapped", "setTimeout(run,95)",
            'class="accessibility-layer ap-modern-a11y-parity" open',
            'id="ap-modern-a11y-state"', 'role="region"', 'syncAccessibleState',
            f'document.getElementById("{base.STATE_SOURCE[slug]}")',
        ):
            if marker not in page:
                raise RuntimeError(f"Modern accessibility/label parity missing for {slug}: {marker}")
        packet_pos = page.rfind('id="v171-modern-packet-runtime"')
        labels_pos = page.rfind('id="v171-modern-packet-label-runtime"')
        body_pos = page.lower().rfind("</body>")
        if not (0 <= packet_pos < labels_pos < body_pos):
            raise RuntimeError(
                f"Modern packet label runtime is not at the final document boundary: {slug} "
                f"packet={packet_pos} labels={labels_pos} body={body_pos}"
            )
        style_pos = page.rfind('id="v171-modern-a11y-parity-style"')
        head_pos = page.lower().rfind("</head>")
        if not (0 <= style_pos < head_pos):
            raise RuntimeError(f"Modern accessibility parity style is not in document head: {slug}")
    base.validate()


def build_site() -> None:
    base.build_site()
    for slug in MODERN:
        path = SITE / "playgrounds" / slug / "index.html"
        page = path.read_text(encoding="utf-8")
        if 'id="v171-modern-packet-label-runtime"' in page or 'id="v171-modern-a11y-parity-style"' in page:
            raise RuntimeError(f"Modern accessibility layer would be applied twice: {slug}")
        page = replace_compact_a11y(page, slug)
        page = insert_before_document_close(page, "</head>", A11Y_STYLE, slug)
        page = insert_before_document_close(page, "</body>", runtime(slug), slug)
        path.write_text(page, encoding="utf-8")
    validate()
    print("Completed v1.7.1 modern accessibility parity: structured open state layer plus deterministic localized Quick Assign labels")


if __name__ == "__main__":
    build_site()
