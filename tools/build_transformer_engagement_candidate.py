#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from build_transformer_public_v1_4 import build_public as build_v14_public

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "release-evidence" / "lab13-engagement-candidate.html"

CSS = r'''
<style id="lab13-engagement-excellence-style">
.lab13-eq-shell{margin-top:12px;display:grid;gap:12px}
.lab13-eq-flow,.lab13-eq-actions,.lab13-eq-compare{border:1px solid color-mix(in srgb,var(--accent) 28%,var(--border));border-radius:12px;background:linear-gradient(180deg,color-mix(in srgb,var(--card) 94%,var(--accent)),var(--card));padding:12px}
.lab13-eq-head{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;flex-wrap:wrap}.lab13-eq-head strong{color:var(--accent);font-size:.78rem;text-transform:uppercase;letter-spacing:.05em}.lab13-eq-head p{margin:3px 0 0;color:var(--muted);font-size:.82rem;max-width:760px}
.lab13-eq-flowline{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));align-items:stretch;gap:7px;margin-top:10px}.lab13-eq-node{position:relative;min-width:0;border:1px solid var(--border);border-radius:10px;background:var(--card);padding:10px;overflow:hidden}.lab13-eq-node strong{display:block;color:var(--accent);font-size:.74rem;text-transform:uppercase;letter-spacing:.04em}.lab13-eq-node span{display:block;margin-top:4px;font:12px/1.4 ui-monospace,monospace;overflow-wrap:anywhere}.lab13-eq-arrow{display:flex;align-items:center;justify-content:center;color:var(--muted);font-weight:800;font-size:1.15rem}.lab13-eq-node.eq-active{border-color:var(--accent);box-shadow:0 0 0 3px color-mix(in srgb,var(--accent) 18%,transparent)}
.lab13-eq-flowline.eq-replay .lab13-eq-node:nth-child(1){animation:eqPulse .24s ease 0s both}.lab13-eq-flowline.eq-replay .lab13-eq-node:nth-child(3){animation:eqPulse .24s ease .18s both}.lab13-eq-flowline.eq-replay .lab13-eq-node:nth-child(5){animation:eqPulse .24s ease .36s both}.lab13-eq-flowline.eq-replay .lab13-eq-node:nth-child(7){animation:eqPulse .24s ease .54s both}@keyframes eqPulse{0%{transform:translateY(0);box-shadow:none}45%{transform:translateY(-3px);box-shadow:0 0 0 4px color-mix(in srgb,var(--accent) 22%,transparent)}100%{transform:translateY(0);box-shadow:none}}
.lab13-eq-actionrow{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:10px}.lab13-eq-actionrow button{padding:8px 11px;border:1px solid var(--border);border-radius:8px;background:var(--card);color:var(--fg);font:inherit;cursor:pointer}.lab13-eq-actionrow button.primary{background:var(--accent);border-color:var(--accent);color:white;font-weight:750}.lab13-eq-actionrow button:disabled{opacity:.48;cursor:not-allowed}.lab13-eq-status{color:var(--muted);font-size:.82rem;min-height:1.25em}.lab13-eq-generation{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px}.lab13-eq-generation span{padding:5px 8px;border:1px solid var(--border);border-radius:999px;background:var(--card);font:12px ui-monospace,monospace}.lab13-eq-generation span:last-child{border-color:var(--accent);box-shadow:0 0 0 2px color-mix(in srgb,var(--accent) 14%,transparent)}
.lab13-eq-compare-grid{display:grid;grid-template-columns:minmax(0,.75fr) minmax(0,1.25fr);gap:12px;margin-top:10px}.lab13-eq-metrics{display:grid;gap:7px}.lab13-eq-metric{border:1px solid var(--border);border-radius:9px;background:var(--card);padding:9px}.lab13-eq-metric strong{display:block;color:var(--muted);font-size:.72rem;text-transform:uppercase}.lab13-eq-metric span{display:block;margin-top:3px;font:12px/1.4 ui-monospace,monospace}.lab13-eq-deltas{display:grid;gap:6px}.lab13-eq-delta{display:grid;grid-template-columns:72px 1fr 62px;gap:7px;align-items:center;font-size:.8rem}.lab13-eq-pair{display:grid;gap:3px}.lab13-eq-track{height:7px;border-radius:999px;background:var(--soft);overflow:hidden}.lab13-eq-fill{height:100%;border-radius:999px}.lab13-eq-fill.base{background:var(--muted);opacity:.48}.lab13-eq-fill.now{background:var(--accent)}.lab13-eq-num{text-align:right;font:11px ui-monospace,monospace}
@media(max-width:820px){.lab13-eq-flowline{grid-template-columns:1fr}.lab13-eq-arrow{transform:rotate(90deg);min-height:18px}.lab13-eq-compare-grid{grid-template-columns:1fr}}
@media(max-width:480px){.lab13-eq-actionrow button{width:100%;min-height:44px}.lab13-eq-delta{grid-template-columns:58px 1fr 55px}}
@media(prefers-reduced-motion:reduce){.lab13-eq-flowline.eq-replay .lab13-eq-node{animation:none!important}.lab13-eq-node{transition:none!important}}
</style>
'''

SCRIPT = r'''
<script id="lab13-engagement-excellence-runtime">
(()=>{'use strict';
const C=window.TransformerLanguageModelCore;if(!C)return;
const $=s=>document.querySelector(s);
const COPY={
 en:{title:'See one state travel through the model',desc:'This is a state-derived replay of the already-computed toy Transformer, not a claim about wall-clock execution order.',tokens:'Tokens',represent:'Represent',attend:'Attend',predict:'Predict',continue:'Continue the toy text',append:'Append argmax token',appendHelp:'The button applies an explicit deterministic selection rule: append the highest-probability display token, then recompute. It is not sampling.',save:'Save current as baseline',clear:'Clear baseline',compare:'Compare one change',none:'Save a baseline, change one model control, and the exact before/after differences appear here.',base:'Baseline',now:'Current',top:'top probability',attention:'final attention L1 Δ',probDelta:'largest probability Δ',special:'The highest-probability token is a structural special token and is not appendable as surface text.',appended:'Appended by argmax rule',window:'The toy context window kept <BOS> and the most recent surface tokens.'},
 zh:{title:'观察一个状态贯穿模型',desc:'这是对已经计算完成的玩具 Transformer 状态进行的可视重放，并不表示真实的墙钟执行时序。',tokens:'词元',represent:'表示',attend:'注意',predict:'预测',continue:'继续玩具文本',append:'追加 argmax 词元',appendHelp:'此按钮使用明确的确定性选择规则：追加显示分布中概率最高的词元，然后重新计算。它不是采样。',save:'把当前状态保存为基线',clear:'清除基线',compare:'比较一次改变',none:'先保存基线，再改变一个模型控制项；这里会显示精确的前后差异。',base:'基线',now:'当前',top:'最高概率',attention:'最终注意力 L1 Δ',probDelta:'最大概率 Δ',special:'概率最高的是结构性特殊词元，不能作为表面文本追加。',appended:'按 argmax 规则追加',window:'玩具上下文窗口保留了 <BOS> 和最近的表面词元。'},
 vi:{title:'Theo dõi một trạng thái đi qua mô hình',desc:'Đây là phát lại trực quan từ trạng thái Transformer đồ chơi đã được tính, không phải tuyên bố về thứ tự thời gian thực thi.',tokens:'Token',represent:'Biểu diễn',attend:'Chú ý',predict:'Dự đoán',continue:'Tiếp tục văn bản đồ chơi',append:'Nối token argmax',appendHelp:'Nút này dùng quy tắc chọn xác định rõ ràng: nối token hiển thị có xác suất cao nhất rồi tính lại. Đây không phải lấy mẫu.',save:'Lưu trạng thái hiện tại làm mốc',clear:'Xóa mốc',compare:'So sánh một thay đổi',none:'Lưu một mốc, thay đổi một điều khiển mô hình và các khác biệt trước/sau chính xác sẽ xuất hiện ở đây.',base:'Mốc',now:'Hiện tại',top:'xác suất cao nhất',attention:'L1 Δ chú ý cuối',probDelta:'Δ xác suất lớn nhất',special:'Token có xác suất cao nhất là token cấu trúc đặc biệt nên không thể nối như văn bản bề mặt.',appended:'Đã nối theo quy tắc argmax',window:'Cửa sổ ngữ cảnh đồ chơi giữ <BOS> và các token bề mặt gần nhất.'},
 es:{title:'Sigue un estado a través del modelo',desc:'Esta es una repetición visual derivada del estado del Transformer de juguete ya calculado, no una afirmación sobre el orden temporal real de ejecución.',tokens:'Tokens',represent:'Representar',attend:'Atender',predict:'Predecir',continue:'Continuar el texto de juguete',append:'Añadir token argmax',appendHelp:'El botón aplica una regla de selección determinista explícita: añade el token visible de mayor probabilidad y recalcula. No es muestreo.',save:'Guardar estado actual como base',clear:'Borrar base',compare:'Comparar un cambio',none:'Guarda una base, cambia un control del modelo y aquí aparecerán las diferencias exactas antes/después.',base:'Base',now:'Actual',top:'probabilidad máxima',attention:'L1 Δ de atención final',probDelta:'Δ máxima de probabilidad',special:'El token de mayor probabilidad es un token estructural especial y no puede añadirse como texto superficial.',appended:'Añadido por regla argmax',window:'La ventana de contexto de juguete conservó <BOS> y los tokens superficiales más recientes.'}
};
let baseline=null,replayTimer=null,lastFingerprint='';
function locale(){return window.Lab13Localization?.getLocale?.()||'en'}function cp(){return COPY[locale()]||COPY.en}
function current(){const text=$('#customPrompt')?.value||'';const options={usePositions:!!$('#positions')?.checked,causalMask:!!$('#mask')?.checked,temperature:Number($('#temperature')?.value||1)};return C.forwardWithPerturbation(text,options,$('#perturb')?.value||'none')}
function snapshot(){const r=current(),top=C.topTokens(r,1)[0],row=r.attention.at(-1);return{text:$('#customPrompt')?.value||'',tokens:r.tokens.slice(),topToken:top[0],topProbability:top[1],probabilities:r.probabilities.slice(),attention:row.slice(),positions:r.usePositions,mask:r.causalMask,temperature:r.temperature,perturbation:r.perturbation}}
function fingerprint(s){return JSON.stringify([s.text,s.positions,s.mask,s.temperature,s.perturbation,s.probabilities.map(x=>x.toFixed(8))])}
function install(){const journey=$('#lab13-mechanism-journey');if(!journey||$('#lab13-eq-shell'))return;const shell=document.createElement('section');shell.id='lab13-eq-shell';shell.className='lab13-eq-shell';shell.setAttribute('data-lab13-no-machine-state','true');shell.innerHTML=`<section class="lab13-eq-flow" aria-labelledby="lab13-eq-title"><div class="lab13-eq-head"><div><strong id="lab13-eq-title"></strong><p id="lab13-eq-desc"></p></div></div><div id="lab13-eq-flowline" class="lab13-eq-flowline"><div class="lab13-eq-node"><strong data-eq-label="tokens"></strong><span id="lab13-eq-tokens"></span></div><div class="lab13-eq-arrow" aria-hidden="true">→</div><div class="lab13-eq-node"><strong data-eq-label="represent"></strong><span id="lab13-eq-represent"></span></div><div class="lab13-eq-arrow" aria-hidden="true">→</div><div class="lab13-eq-node"><strong data-eq-label="attend"></strong><span id="lab13-eq-attend"></span></div><div class="lab13-eq-arrow" aria-hidden="true">→</div><div class="lab13-eq-node"><strong data-eq-label="predict"></strong><span id="lab13-eq-predict"></span></div></div></section><section class="lab13-eq-actions"><div class="lab13-eq-head"><div><strong id="lab13-eq-continue-title"></strong><p id="lab13-eq-append-help"></p></div></div><div class="lab13-eq-actionrow"><button id="lab13-eq-append" class="primary" type="button"></button><span id="lab13-eq-status" class="lab13-eq-status" aria-live="polite"></span></div><div id="lab13-eq-generation" class="lab13-eq-generation" aria-label="Current toy token sequence"></div></section><section class="lab13-eq-compare"><div class="lab13-eq-head"><div><strong id="lab13-eq-compare-title"></strong><p id="lab13-eq-compare-help"></p></div><div class="lab13-eq-actionrow" style="margin-top:0"><button id="lab13-eq-save" type="button"></button><button id="lab13-eq-clear" type="button"></button></div></div><div id="lab13-eq-compare-body" class="lab13-eq-compare-grid"></div></section>`;journey.insertAdjacentElement('afterend',shell);$('#lab13-eq-append').addEventListener('click',appendArgmax);$('#lab13-eq-save').addEventListener('click',()=>{baseline=snapshot();render(false)});$('#lab13-eq-clear').addEventListener('click',()=>{baseline=null;render(false)});for(const selector of ['#prompt','#applyCustom','#positions','#mask','#temperature','#perturb','#scenario']){const el=$(selector);if(el)el.addEventListener(selector==='#prompt'||selector==='#scenario'?'change':selector==='#applyCustom'?'click':'input',()=>queueMicrotask(()=>render(true)))}window.addEventListener('lab13localechange',()=>queueMicrotask(()=>render(false)));render(false)}
function setText(id,text){const el=$(id);if(el)el.textContent=text}
function localize(){const c=cp();setText('#lab13-eq-title',c.title);setText('#lab13-eq-desc',c.desc);for(const key of ['tokens','represent','attend','predict']){const el=$(`[data-eq-label="${key}"]`);if(el)el.textContent=c[key]}setText('#lab13-eq-continue-title',c.continue);setText('#lab13-eq-append-help',c.appendHelp);setText('#lab13-eq-append',c.append);setText('#lab13-eq-save',c.save);setText('#lab13-eq-clear',c.clear);setText('#lab13-eq-compare-title',c.compare);}
function render(replay){if(!$('#lab13-eq-shell'))return;localize();const c=cp(),s=snapshot(),r=current(),last=r.tokens.length-1,row=r.attention[last],win=row.map((w,i)=>({w,i})).reduce((a,b)=>b.w>a.w?b:a);setText('#lab13-eq-tokens',r.tokens.join(' · '));setText('#lab13-eq-represent',`${r.tokens[last]} @ ${last} · position ${r.usePositions?'on':'off'}`);setText('#lab13-eq-attend',`${r.tokens[win.i]} @ ${win.i} · ${(100*win.w).toFixed(1)}%`);setText('#lab13-eq-predict',`${s.topToken} · ${(100*s.topProbability).toFixed(1)}%`);const gen=$('#lab13-eq-generation');gen.innerHTML='';r.tokens.forEach(token=>{const chip=document.createElement('span');chip.textContent=token;gen.appendChild(chip)});const fp=fingerprint(s);if(replay&&fp!==lastFingerprint&&!matchMedia('(prefers-reduced-motion: reduce)').matches){const line=$('#lab13-eq-flowline');line.classList.remove('eq-replay');void line.offsetWidth;line.classList.add('eq-replay');clearTimeout(replayTimer);replayTimer=setTimeout(()=>line.classList.remove('eq-replay'),900)}lastFingerprint=fp;renderCompare(s,c)}
function renderCompare(s,c){const root=$('#lab13-eq-compare-body');if(!baseline){$('#lab13-eq-compare-help').textContent=c.none;root.innerHTML='';return}$('#lab13-eq-compare-help').textContent=`${c.base}: ${baseline.text || '—'} → ${c.now}: ${s.text || '—'}`;const maxDelta=Math.max(...s.probabilities.map((p,i)=>Math.abs(p-baseline.probabilities[i]))),attnN=Math.max(s.attention.length,baseline.attention.length),attnDelta=Array.from({length:attnN},(_,i)=>Math.abs((s.attention[i]||0)-(baseline.attention[i]||0))).reduce((a,b)=>a+b,0);const metrics=document.createElement('div');metrics.className='lab13-eq-metrics';metrics.innerHTML=`<div class="lab13-eq-metric"><strong>${c.top}</strong><span>${c.base}: ${baseline.topToken} ${(100*baseline.topProbability).toFixed(2)}%<br>${c.now}: ${s.topToken} ${(100*s.topProbability).toFixed(2)}%</span></div><div class="lab13-eq-metric"><strong>${c.probDelta}</strong><span>${(100*maxDelta).toFixed(2)} percentage points</span></div><div class="lab13-eq-metric"><strong>${c.attention}</strong><span>${attnDelta.toFixed(4)}</span></div>`;const deltas=document.createElement('div');deltas.className='lab13-eq-deltas';const order=C.VOCAB.map((token,i)=>({token,i,d:Math.abs(s.probabilities[i]-baseline.probabilities[i])})).sort((a,b)=>b.d-a.d||a.token.localeCompare(b.token)).slice(0,5);for(const item of order){const row=document.createElement('div');row.className='lab13-eq-delta';const max=Math.max(s.probabilities[item.i],baseline.probabilities[item.i],.0001);row.innerHTML=`<span>${item.token}</span><div class="lab13-eq-pair"><div class="lab13-eq-track"><div class="lab13-eq-fill base" style="width:${100*baseline.probabilities[item.i]/max}%"></div></div><div class="lab13-eq-track"><div class="lab13-eq-fill now" style="width:${100*s.probabilities[item.i]/max}%"></div></div></div><span class="lab13-eq-num">${(100*(s.probabilities[item.i]-baseline.probabilities[item.i])).toFixed(2)}pp</span>`;deltas.appendChild(row)}root.innerHTML='';root.append(metrics,deltas)}
function appendArgmax(){const c=cp(),s=snapshot(),token=s.topToken,status=$('#lab13-eq-status');if(token==='<BOS>'){status.textContent=c.special;return}let surface=token;if(token==='<UNK>')surface='mystery';const input=$('#customPrompt'),before=C.toyTokenize(input.value),next=(input.value.trim()+' '+surface).trim();input.value=next;$('#applyCustom')?.click();const after=C.toyTokenize(next);const shifted=before.length>=C.MAX_CONTEXT&&after.length===C.MAX_CONTEXT;queueMicrotask(()=>{status.textContent=`${c.appended}: ${token}.${shifted?' '+c.window:''}`;render(true)})}
function init(){if(!window.Lab13Localization||!$('#lab13-mechanism-journey'))return setTimeout(init,0);install();window.Lab13EngagementExperience={snapshot,saveBaseline:()=>{baseline=snapshot();render(false)},clearBaseline:()=>{baseline=null;render(false)},appendArgmax,getBaseline:()=>baseline&&JSON.parse(JSON.stringify(baseline))}}
init();
})();
</script>
'''


def build_candidate(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    build_v14_public(output)
    html = output.read_text(encoding="utf-8")
    html = html.replace("</head>", CSS + "\n</head>", 1)
    html = html.replace("</body>", SCRIPT + "\n</body>", 1)
    required = (
        'id="lab13-engagement-excellence-style"',
        'id="lab13-engagement-excellence-runtime"',
        'Lab13EngagementExperience',
        'Append argmax token',
        'Save current as baseline',
    )
    missing = [marker for marker in required if marker not in html]
    if missing:
        raise RuntimeError(f"Lab 13 engagement candidate incomplete: {missing}")
    for token in ("<script src=", "fetch(", "XMLHttpRequest", "WebSocket(", "EventSource("):
        if token in html:
            raise RuntimeError(f"Lab 13 engagement candidate violates one-file/offline boundary: {token}")
    output.write_text(html, encoding="utf-8")
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    result = build_candidate(output)
    print(f"Built Lab 13 engagement candidate: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
