#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from build_agent_tool_context_public import build_public as build_v13_public

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "_site" / "playgrounds" / "agent-tool-context" / "index.html"
RELEASE_VERSION = "1.4.0"

CSS = r'''
<style id="lab14-v14-experience-style">
#lab14-locale-bar{align-items:center}
#lab14-locale-bar button[data-locale]{display:none!important}
.lab14-language-select{min-height:36px;padding:6px 32px 6px 10px;border:1px solid var(--border);border-radius:7px;background:var(--card);color:var(--fg);font:inherit;cursor:pointer}
.lab14-language-select:focus-visible{outline:3px solid color-mix(in srgb,var(--accent) 45%,transparent);outline-offset:2px}
.pipeline{grid-template-columns:repeat(7,minmax(0,1fr))}
.pipeline .stage{position:relative;transition:transform .16s ease,border-color .16s ease,box-shadow .16s ease,background .16s ease}
.pipeline .stage.v14-current{transform:translateY(-2px);box-shadow:0 0 0 3px color-mix(in srgb,var(--accent) 20%,transparent);border-color:var(--accent)}
.pipeline .stage.v14-ready{box-shadow:inset 0 -4px 0 color-mix(in srgb,var(--accent) 62%,transparent)}
.lab14-action-journey{display:grid;grid-template-columns:minmax(0,1fr) minmax(260px,.8fr);gap:12px;margin-top:10px;padding:12px;border:1px solid color-mix(in srgb,var(--accent) 28%,var(--border));border-radius:10px;background:color-mix(in srgb,var(--card) 92%,var(--accent))}
.lab14-action-journey strong{display:block;color:var(--accent);font-size:.78rem;text-transform:uppercase;letter-spacing:.05em}.lab14-action-chip{margin-top:5px;padding:8px 10px;border:1px solid var(--border);border-radius:8px;background:var(--card);font:12px/1.45 ui-monospace,monospace;overflow-wrap:anywhere}.lab14-journey-status{align-self:center;color:var(--muted);font-size:.84rem}
.lab14-provenance{margin:24px 0 4px;padding-top:14px;border-top:1px solid var(--border);color:var(--muted);font-size:.78rem;text-align:center}.lab14-provenance a{color:var(--accent)}
@media(max-width:980px){.pipeline{grid-template-columns:repeat(4,minmax(0,1fr))}}
@media(max-width:720px){.pipeline{grid-template-columns:repeat(2,minmax(0,1fr))}.lab14-action-journey{grid-template-columns:1fr}}
@media(max-width:480px){.pipeline{grid-template-columns:1fr}.lab14-language-select{min-height:44px;max-width:100%}}
@media(prefers-reduced-motion:reduce){.pipeline .stage{transition:none!important}}
</style>
'''

FOOTER = r'''
<footer class="lab14-provenance" data-lab14-v14-provenance data-lab14-no-translate="true">
  <span>AI Playgrounds</span> · <span>v1.4.0</span> ·
  <a href="https://github.com/lmdixon23/ai-playgrounds" data-lab14-source>Source</a> ·
  <a href="../../research-and-citation.html" data-lab14-citation>Citation</a>
</footer>
'''

SCRIPT = r'''
<script id="lab14-v14-experience-runtime">
(()=>{'use strict';
const LOCALES=['en','zh','vi','es'];
const NAMES={en:'English',zh:'简体中文',vi:'Tiếng Việt',es:'Español'};
const COPY={
 en:{language:'Language',journey:'Action through the runtime',selected:'Selected action',source:'Source',citation:'Citation',update:'Update / choose next',stop:'Stop',idle:'The selected model output is waiting at Propose.',text:'Text output stops before tool validation because no tool call was executed.',invalidType:'The model output is not a supported action type.',invalid:'Rejected at Validate: the tool call does not satisfy the runtime schema.',denied:'Denied at Authorize: the schema is valid, but this principal lacks permission.',error:'The tool executed and returned an error observation; the error is added to context.',ok:'The observation has been added to context. The runtime now chooses the next action.',complete:'The goal is satisfied and STOP has completed the run.',premature:'STOP was proposed before the goal conditions were satisfied.',budget:'The step budget is exhausted; no further execution is allowed.',nextStop:'Goal conditions are satisfied. STOP is the justified next action.',nextAction:'Context updated; a new action has been selected.'},
 zh:{language:'语言',journey:'动作如何通过运行时',selected:'已选择动作',source:'源代码',citation:'引用',update:'更新 / 选择下一步',stop:'停止',idle:'已选择的模型输出正在“提出”阶段等待。',text:'文本输出在工具验证前结束，因为没有执行工具调用。',invalidType:'模型输出不是受支持的动作类型。',invalid:'在“验证”阶段被拒绝：工具调用不符合运行时模式。',denied:'在“授权”阶段被拒绝：模式有效，但当前主体没有权限。',error:'工具已执行并返回错误观察；该错误被加入上下文。',ok:'观察已加入上下文。运行时现在选择下一步动作。',complete:'目标已满足，STOP 已完成运行。',premature:'在目标条件满足之前提出了 STOP。',budget:'步骤预算已耗尽；不能继续执行。',nextStop:'目标条件已满足。STOP 是合理的下一步动作。',nextAction:'上下文已更新；新的动作已被选择。'},
 vi:{language:'Ngôn ngữ',journey:'Hành trình của hành động qua runtime',selected:'Hành động được chọn',source:'Mã nguồn',citation:'Trích dẫn',update:'Cập nhật / chọn bước tiếp',stop:'Dừng',idle:'Đầu ra mô hình đã chọn đang chờ ở bước Đề xuất.',text:'Đầu ra văn bản dừng trước bước xác thực công cụ vì không có lệnh gọi công cụ nào được thực thi.',invalidType:'Đầu ra mô hình không phải kiểu hành động được hỗ trợ.',invalid:'Bị từ chối ở bước Xác thực: lệnh gọi công cụ không thỏa lược đồ runtime.',denied:'Bị từ chối ở bước Phân quyền: lược đồ hợp lệ nhưng vai trò này không có quyền.',error:'Công cụ đã chạy và trả về quan sát lỗi; lỗi được thêm vào ngữ cảnh.',ok:'Quan sát đã được thêm vào ngữ cảnh. Runtime giờ chọn hành động tiếp theo.',complete:'Mục tiêu đã thỏa mãn và STOP đã kết thúc lần chạy.',premature:'STOP được đề xuất trước khi các điều kiện mục tiêu được thỏa mãn.',budget:'Ngân sách bước đã hết; không thể thực thi thêm.',nextStop:'Các điều kiện mục tiêu đã thỏa mãn. STOP là hành động tiếp theo hợp lý.',nextAction:'Ngữ cảnh đã cập nhật; một hành động mới đã được chọn.'},
 es:{language:'Idioma',journey:'Recorrido de la acción por el runtime',selected:'Acción seleccionada',source:'Código fuente',citation:'Citación',update:'Actualizar / elegir siguiente',stop:'Detener',idle:'La salida del modelo seleccionada espera en Proponer.',text:'La salida de texto se detiene antes de validar herramientas porque no se ejecutó ninguna llamada.',invalidType:'La salida del modelo no es un tipo de acción compatible.',invalid:'Rechazada en Validar: la llamada no satisface el esquema del runtime.',denied:'Denegada en Autorizar: el esquema es válido, pero este principal no tiene permiso.',error:'La herramienta se ejecutó y devolvió una observación de error; el error se añade al contexto.',ok:'La observación se añadió al contexto. El runtime elige ahora la acción siguiente.',complete:'El objetivo está satisfecho y STOP completó la ejecución.',premature:'STOP se propuso antes de satisfacer las condiciones del objetivo.',budget:'Se agotó el presupuesto de pasos; no se permite más ejecución.',nextStop:'Las condiciones del objetivo están satisfechas. STOP es la siguiente acción justificada.',nextAction:'El contexto se actualizó; se ha seleccionado una nueva acción.'}
};
const $=s=>document.querySelector(s),all=s=>[...document.querySelectorAll(s)];
function locale(){return (window.Lab14Localization&&window.Lab14Localization.getLocale())||'en'}
function c(){return COPY[locale()]||COPY.en}
function updateUrl(value){try{const u=new URL(location.href);u.searchParams.set('lang',value);history.replaceState(null,'',u)}catch(_){}}
function actionText(action){if(!action)return '—';if(action.type==='stop')return 'STOP';if(action.type==='text')return `TEXT: ${action.text}`;return `${action.name}(${JSON.stringify(action.arguments)})`}
function installLanguageSelect(){
 const bar=$('#lab14-locale-bar');if(!bar||$('#lab14-language-select'))return;
 const label=bar.querySelector('.locale-label');if(label)label.id='lab14-language-label';
 const select=document.createElement('select');select.id='lab14-language-select';select.className='lab14-language-select';select.setAttribute('aria-labelledby','lab14-language-label');select.setAttribute('data-lab14-no-translate','true');
 for(const code of LOCALES){const option=document.createElement('option');option.value=code;option.textContent=NAMES[code];select.appendChild(option)}
 bar.appendChild(select);select.value=locale();select.addEventListener('change',()=>window.Lab14Localization.setLocale(select.value));
}
function makeStage(id,n,label){const d=document.createElement('div');d.id=id;d.className='stage';d.setAttribute('data-lab14-no-translate','true');d.innerHTML=`<strong>${n} · <span></span></strong><span class="v14-stage-note"></span>`;d.querySelector('strong span').textContent=label;return d}
function installJourney(){
 const pipeline=$('.pipeline');if(!pipeline||$('#p-update'))return;
 pipeline.appendChild(makeStage('p-update','6',c().update));pipeline.appendChild(makeStage('p-stop','7',c().stop));
 const section=document.createElement('section');section.id='lab14-action-journey';section.className='lab14-action-journey';section.setAttribute('data-lab14-no-translate','true');section.setAttribute('aria-label',c().journey);
 section.innerHTML='<div><strong id="lab14-journey-label"></strong><div id="lab14-action-label" class="tiny"></div><div id="lab14-action-chip" class="lab14-action-chip"></div></div><div id="lab14-journey-status" class="lab14-journey-status" aria-live="polite"></div>';
 pipeline.insertAdjacentElement('afterend',section);
}
function eventMessage(event,decision){
 const copy=c();if(!event)return copy.idle;
 if(event.event==='text_only')return copy.text;if(event.event==='invalid_action_type')return copy.invalidType;if(event.event==='rejected_invalid')return copy.invalid;if(event.event==='denied_unauthorized')return copy.denied;if(event.event==='executed_error')return copy.error;if(event.event==='stopped_complete')return copy.complete;if(event.event==='premature_stop')return copy.premature;if(event.event==='budget_exhausted')return copy.budget;
 if(event.event==='executed_ok'){if(decision&&decision.selected_action&&decision.selected_action.type==='stop')return copy.nextStop;return copy.ok+' '+copy.nextAction}
 return copy.idle;
}
function markCurrent(id){const el=$(`#${id}`);if(el)el.classList.add('v14-current')}
function renderJourney(){
 if(!window.Lab14Prototype)return;
 const state=window.Lab14Prototype.getState(),decision=window.Lab14Prototype.getDecision(),event=state.history[state.history.length-1];
 all('.pipeline .stage').forEach(el=>el.classList.remove('v14-current','v14-ready'));
 for(const id of ['p-update','p-stop']){const el=$(`#${id}`);if(el)el.classList.remove('good','warn','bad')}
 if(!event)markCurrent('p-propose');
 else if(event.event==='rejected_invalid')markCurrent('p-validate');
 else if(event.event==='denied_unauthorized')markCurrent('p-authorize');
 else if(event.event==='executed_error'){markCurrent('p-observe');$('#p-update')?.classList.add('good')}
 else if(event.event==='executed_ok'){markCurrent('p-update');$('#p-update')?.classList.add('good')}
 else if(event.event==='stopped_complete'){markCurrent('p-stop');$('#p-stop')?.classList.add('good')}
 else if(event.event==='premature_stop'){markCurrent('p-stop');$('#p-stop')?.classList.add('bad')}
 else if(event.event==='budget_exhausted'){markCurrent('p-stop');$('#p-stop')?.classList.add('bad')}
 else markCurrent('p-propose');
 if(state.status==='active'&&decision&&decision.selected_action){if(decision.selected_action.type==='stop')$('#p-stop')?.classList.add('v14-ready');else $('#p-propose')?.classList.add('v14-ready')}
 const action=decision&&decision.selected_action;if($('#lab14-action-chip'))$('#lab14-action-chip').textContent=actionText(action);
 if($('#lab14-journey-status'))$('#lab14-journey-status').textContent=eventMessage(event,decision);
}
function localizeExperience(){
 const copy=c(),select=$('#lab14-language-select'),label=$('#lab14-language-label');if(select)select.value=locale();if(label)label.textContent=copy.language;
 if($('#lab14-journey-label'))$('#lab14-journey-label').textContent=copy.journey;if($('#lab14-action-label'))$('#lab14-action-label').textContent=copy.selected;
 const update=$('#p-update strong span'),stop=$('#p-stop strong span');if(update)update.textContent=copy.update;if(stop)stop.textContent=copy.stop;
 if($('#lab14-action-journey'))$('#lab14-action-journey').setAttribute('aria-label',copy.journey);
 if($('[data-lab14-source]'))$('[data-lab14-source]').textContent=copy.source;if($('[data-lab14-citation]'))$('[data-lab14-citation]').textContent=copy.citation;
 renderJourney();
}
function installStateHooks(){
 for(const selector of ['#step','#reset','#scenario']){const el=$(selector);if(el)el.addEventListener(selector==='#scenario'?'change':'click',()=>queueMicrotask(renderJourney));}
}
let deferredInit=false;
function init(){
 if(!window.Lab14Localization||!window.Lab14Prototype){
  if(document.readyState==='loading'&&!deferredInit){deferredInit=true;document.addEventListener('DOMContentLoaded',init,{once:true});return}
  console.error('Lab 14 journey could not start because its localization or prototype runtime is unavailable');return;
 }
 installLanguageSelect();installJourney();installStateHooks();localizeExperience();
 window.addEventListener('lab14localechange',()=>{updateUrl(locale());localizeExperience()});
 window.Lab14V14Experience={render:renderJourney};
}
init();
})();
</script>
'''


def build_public(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    build_v13_public(output)
    html = output.read_text(encoding="utf-8")
    html = html.replace("AI Playgrounds v1.3", "AI Playgrounds")
    html = html.replace("</head>", f'<meta name="ai-playgrounds-version" content="{RELEASE_VERSION}">\n' + CSS + "\n</head>", 1)
    html = html.replace("</main>", FOOTER + "\n</main>", 1)
    html = html.replace("</body>", SCRIPT + "\n</body>", 1)

    required = ('id="lab14-v14-experience-runtime"','id="lab14-v14-experience-style"','data-lab14-v14-provenance',f'name="ai-playgrounds-version" content="{RELEASE_VERSION}"','Lab14V14Experience','p-update','p-stop')
    missing = [marker for marker in required if marker not in html]
    if missing:
        raise RuntimeError(f"Lab 14 v1.4 experience wrapper is incomplete: {missing}")
    if "AI Playgrounds v1.3" in html:
        raise RuntimeError("Lab 14 v1.4 retains the prominent v1.3 badge")
    for token in ("<script src=", "fetch(", "XMLHttpRequest", "WebSocket(", "EventSource("):
        if token in html:
            raise RuntimeError(f"Lab 14 v1.4 violates one-file/offline boundary: {token}")
    output.write_text(html, encoding="utf-8")
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    result = build_public(output)
    print(f"Built public Lab 14 v1.4 experience: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
