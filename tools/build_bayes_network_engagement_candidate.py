#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import build_site_v1_4

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "_site" / "playgrounds" / "bayes-network" / "index.html"

ADAPTER = r'''
    window.__bayesPosteriorPresentationSnapshot = {
      preset: currentPreset,
      vars: net.vars.slice(),
      labels: Object.assign({}, net.labels),
      evidence: Object.assign({}, evidence),
      method,
      post: Object.assign({}, post),
      meta
    };
    window.dispatchEvent(new CustomEvent('bayesposteriorchange'));
'''

CSS = r'''
<style id="bayes-engagement-excellence-style">
.bayes-eq-strip{margin:0 0 10px;padding:10px 12px;border:1px solid color-mix(in srgb,var(--accent) 32%,var(--border));border-radius:10px;background:linear-gradient(180deg,color-mix(in srgb,var(--card) 92%,var(--accent)),var(--card));display:flex;align-items:flex-start;justify-content:space-between;gap:12px;flex-wrap:wrap}.bayes-eq-strip strong{display:block;color:var(--accent);font-size:.78rem;text-transform:uppercase;letter-spacing:.05em}.bayes-eq-strip p{margin:3px 0 0;color:var(--muted);font-size:.8rem;max-width:760px}.bayes-eq-mode{padding:4px 7px;border:1px solid var(--border);border-radius:999px;background:var(--card);color:var(--muted);font:11px/1.3 ui-monospace,monospace}.infer-cell .bar{position:relative}.bayes-eq-prev-marker{position:absolute;top:-3px;bottom:-3px;width:3px;border-radius:3px;background:var(--fg);opacity:.55;transform:translateX(-1.5px);pointer-events:none}.bayes-eq-delta{margin-top:7px;padding-top:6px;border-top:1px dashed var(--border);font:11px/1.4 ui-monospace,monospace;color:var(--muted);min-height:2.7em}.bayes-eq-delta b{color:var(--fg)}.infer-cell.bayes-eq-largest{border-color:var(--accent);box-shadow:0 0 0 2px color-mix(in srgb,var(--accent) 17%,transparent)}.bayes-eq-up{color:var(--true)!important}.bayes-eq-down{color:var(--false)!important}.bayes-eq-flat{color:var(--muted)!important}
@media(max-width:560px){.bayes-eq-strip{display:block}.bayes-eq-mode{display:inline-block;margin-top:7px}}
@media(prefers-reduced-motion:reduce){.infer-cell .bar .fill,.bayes-eq-prev-marker{transition:none!important}}
</style>
'''

SCRIPT = r'''
<script id="bayes-engagement-excellence-runtime">
(()=>{'use strict';
const $=s=>document.querySelector(s);let previous=null,current=null;
const COPY={
 en:{title:'Keep the previous exact belief visible',help:'A dark marker shows the previous exact posterior. The filled bar is the current posterior. This is a before/after comparison only; it does not imply probability literally flows along graph arrows.',first:'Make one evidence or CPT change in Exact or Variable elimination to leave a previous-state marker.',paused:'Exact before/after comparison is paused for sampling methods because Monte Carlo noise can move estimates even when the model has not changed.',before:'before',now:'now',largest:'largest exact change',exact:'exact comparison'},
 zh:{title:'保留上一个精确信念作为参照',help:'深色标记表示上一个精确后验，填充条表示当前后验。这只是前后比较；并不表示概率会沿图中箭头真实流动。',first:'在精确枚举或变量消除模式下改变一次证据或 CPT，即可留下上一状态标记。',paused:'采样方法会暂停精确前后比较，因为即使模型没有改变，蒙特卡洛噪声也可能使估计发生波动。',before:'之前',now:'现在',largest:'最大精确变化',exact:'精确比较'},
 vi:{title:'Giữ niềm tin chính xác trước đó làm mốc',help:'Vạch tối là hậu nghiệm chính xác trước đó; thanh tô là hậu nghiệm hiện tại. Đây chỉ là so sánh trước/sau, không ngụ ý xác suất thực sự chảy dọc các mũi tên của đồ thị.',first:'Hãy thay đổi một bằng chứng hoặc CPT trong chế độ Exact hay Variable elimination để để lại mốc trạng thái trước.',paused:'So sánh trước/sau chính xác tạm dừng với phương pháp lấy mẫu vì nhiễu Monte Carlo có thể làm ước lượng thay đổi ngay cả khi mô hình không đổi.',before:'trước',now:'hiện tại',largest:'thay đổi chính xác lớn nhất',exact:'so sánh chính xác'},
 es:{title:'Mantén visible la creencia exacta anterior',help:'La marca oscura muestra el posterior exacto anterior; la barra rellena muestra el posterior actual. Es una comparación antes/después: no implica que la probabilidad fluya literalmente por las flechas del grafo.',first:'Haz un cambio de evidencia o CPT en Exact o Eliminación de variables para dejar una marca del estado anterior.',paused:'La comparación exacta antes/después se pausa con métodos de muestreo porque el ruido de Monte Carlo puede mover las estimaciones aunque el modelo no cambie.',before:'antes',now:'ahora',largest:'mayor cambio exacto',exact:'comparación exacta'}
};
function clone(v){return JSON.parse(JSON.stringify(v))}function snapshot(){return window.__bayesPosteriorPresentationSnapshot?clone(window.__bayesPosteriorPresentationSnapshot):null}function locale(){const r=window.__r4Localization?.locale?.();if(r)return r;const l=(document.documentElement.lang||'en').toLowerCase();if(l.startsWith('zh'))return'zh';if(l.startsWith('vi'))return'vi';if(l.startsWith('es'))return'es';return'en'}function cp(){return COPY[locale()]||COPY.en}function deterministic(s){return !!s&&(s.method==='exact'||s.method==='ve')}function sameFrame(a,b){return !!a&&!!b&&a.preset===b.preset&&a.method===b.method&&deterministic(a)&&deterministic(b)}
function install(){const section=$('.infer-section');if(!section||$('#bayes-eq-strip'))return;const strip=document.createElement('div');strip.id='bayes-eq-strip';strip.className='bayes-eq-strip';strip.setAttribute('data-r4-no-translate','1');strip.innerHTML='<div><strong id="bayes-eq-title"></strong><p id="bayes-eq-help"></p></div><span id="bayes-eq-mode" class="bayes-eq-mode"></span>';section.insertBefore(strip,$('#postRow'));window.addEventListener('bayesposteriorchange',handle);window.addEventListener('r4languagechange',()=>queueMicrotask(render));document.querySelectorAll('.lang-switch button[data-lang]').forEach(b=>b.addEventListener('click',()=>setTimeout(render,0)));current=snapshot();render()}
function handle(){const next=snapshot();if(current&&sameFrame(current,next)&&JSON.stringify(current.post)!==JSON.stringify(next.post))previous=current;else if(!sameFrame(current,next))previous=null;current=next;queueMicrotask(render)}
function render(){if(!$('#bayes-eq-strip'))return;const c=cp();$('#bayes-eq-title').textContent=c.title;$('#bayes-eq-mode').textContent=current?`${current.method} · ${c.exact}`:c.exact;const cells=[...document.querySelectorAll('#postRow .infer-cell')];cells.forEach(cell=>{cell.classList.remove('bayes-eq-largest');cell.querySelectorAll('.bayes-eq-prev-marker,.bayes-eq-delta').forEach(el=>el.remove())});if(!current){$('#bayes-eq-help').textContent=c.first;return}if(!deterministic(current)){previous=null;$('#bayes-eq-help').textContent=c.paused;return}if(!previous||!sameFrame(previous,current)){previous=null;$('#bayes-eq-help').textContent=c.first;return}const deltas=current.vars.map(v=>({v,d:current.post[v]-previous.post[v],abs:Math.abs(current.post[v]-previous.post[v])})),largest=deltas.reduce((a,b)=>b.abs>a.abs?b:a,deltas[0]);$('#bayes-eq-help').textContent=`${c.largest}: ${current.labels[largest.v]} ${largest.d>=0?'↑':'↓'} ${(100*largest.abs).toFixed(2)} pp. ${c.help}`;current.vars.forEach((v,i)=>{const cell=cells[i];if(!cell)return;const prev=previous.post[v],now=current.post[v],d=now-prev,bar=cell.querySelector('.bar');if(bar){const marker=document.createElement('span');marker.className='bayes-eq-prev-marker';marker.style.left=`${Math.max(0,Math.min(100,prev*100))}%`;marker.title=`${c.before}: ${(100*prev).toFixed(2)}%`;bar.appendChild(marker)}const delta=document.createElement('div');delta.className='bayes-eq-delta '+(d>1e-12?'bayes-eq-up':d<-1e-12?'bayes-eq-down':'bayes-eq-flat');delta.innerHTML=`<b>${c.before}</b> ${(100*prev).toFixed(2)}% → <b>${c.now}</b> ${(100*now).toFixed(2)}%<br>${d>1e-12?'↑':d<-1e-12?'↓':'→'} ${(100*Math.abs(d)).toFixed(2)} pp`;cell.appendChild(delta);if(v===largest.v)cell.classList.add('bayes-eq-largest')})}
function init(){if(!window.__bayesPosteriorPresentationSnapshot||!$('#postRow'))return setTimeout(init,0);install();window.__bayesPosteriorDeltaExperience={getCurrent:()=>clone(current),getPrevious:()=>clone(previous),render}}
init();
})();
</script>
'''


def build_candidate(output: Path) -> Path:
    build_site_v1_4.build_site()
    source = DEFAULT_OUTPUT.read_text(encoding="utf-8")
    marker = "  function renderPosteriors(post, meta) {\n    const row = $('postRow');"
    if marker not in source:
        raise RuntimeError("Could not locate frozen Bayesian posterior renderer for presentation adapter")
    source = source.replace(
        marker,
        "  function renderPosteriors(post, meta) {\n" + ADAPTER + "    const row = $('postRow');",
        1,
    )
    source = source.replace("</head>", CSS + "\n</head>", 1)
    source = source.replace("</body>", SCRIPT + "\n</body>", 1)
    required = (
        "__bayesPosteriorPresentationSnapshot",
        'id="bayes-engagement-excellence-style"',
        'id="bayes-engagement-excellence-runtime"',
        "__bayesPosteriorDeltaExperience",
    )
    missing = [item for item in required if item not in source]
    if missing:
        raise RuntimeError(f"Bayesian engagement candidate incomplete: {missing}")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(source, encoding="utf-8")
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    result = build_candidate(output)
    print(f"Built Bayesian posterior-delta engagement candidate: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
