#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from build_transformer_public import build_public as build_v13_public

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "_site" / "playgrounds" / "transformer-language-model" / "index.html"
RELEASE_VERSION = "1.4.0"

CSS = r'''
<style id="lab13-v14-experience-style">
#lab13-locale-bar{align-items:center}
#lab13-locale-bar button[data-locale]{display:none!important}
.lab13-language-select{min-height:36px;padding:6px 32px 6px 10px;border:1px solid var(--border);border-radius:7px;background:var(--card);color:var(--fg);font:inherit;cursor:pointer}
.lab13-language-select:focus-visible{outline:3px solid color-mix(in srgb,var(--accent) 45%,transparent);outline-offset:2px}
.lab13-journey{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-top:10px;padding:10px 12px;border:1px solid color-mix(in srgb,var(--accent) 28%,var(--border));border-radius:10px;background:color-mix(in srgb,var(--card) 92%,var(--accent))}
.lab13-journey-copy{min-width:0}.lab13-journey-copy strong{display:block;color:var(--accent);font-size:.78rem;text-transform:uppercase;letter-spacing:.05em}.lab13-journey-copy span{display:block;margin-top:2px;font-size:.88rem}
.lab13-journey-actions{display:flex;gap:7px;flex-wrap:wrap}.lab13-journey-actions button{padding:6px 10px;border:1px solid var(--border);border-radius:7px;background:var(--card);color:var(--fg);font:inherit;cursor:pointer}.lab13-journey-actions button:disabled{opacity:.42;cursor:not-allowed}
.pipeline .stage.lab13-journey-stage{cursor:pointer;transition:transform .16s ease,border-color .16s ease,box-shadow .16s ease,background .16s ease}
.pipeline .stage.lab13-journey-stage:hover{transform:translateY(-1px)}
.pipeline .stage.lab13-journey-stage[aria-current="step"]{border-color:var(--accent);box-shadow:0 0 0 3px color-mix(in srgb,var(--accent) 18%,transparent);background:color-mix(in srgb,var(--card) 90%,var(--accent))}
.lab13-focus-target{outline:3px solid color-mix(in srgb,var(--accent) 38%,transparent);outline-offset:3px;box-shadow:0 10px 28px color-mix(in srgb,var(--accent) 12%,transparent);transition:outline-color .16s ease,box-shadow .16s ease}
.lab13-provenance{margin:24px 0 4px;padding-top:14px;border-top:1px solid var(--border);color:var(--muted);font-size:.78rem;text-align:center}.lab13-provenance a{color:var(--accent)}
@media(max-width:480px){.lab13-journey{align-items:stretch}.lab13-journey-actions{width:100%}.lab13-journey-actions button{flex:1;min-height:42px}.lab13-language-select{min-height:44px;max-width:100%}}
@media(prefers-reduced-motion:reduce){.pipeline .stage.lab13-journey-stage,.lab13-focus-target{transition:none!important}}
</style>
'''

FOOTER = r'''
<footer class="lab13-provenance" data-lab13-v14-provenance>
  <span>AI Playgrounds</span> · <span>v1.4.0</span> ·
  <a href="https://github.com/lmdixon23/ai-playgrounds" data-lab13-source>Source</a> ·
  <a href="../../research-and-citation.html" data-lab13-citation>Citation</a>
</footer>
'''

SCRIPT = r'''
<script id="lab13-v14-experience-runtime">
(()=>{'use strict';
const LOCALES=['en','zh','vi','es'];
const NAMES={en:'English',zh:'简体中文',vi:'Tiếng Việt',es:'Español'};
const COPY={
  en:{language:'Language',journey:'Mechanism journey',previous:'Previous stage',next:'Next stage',source:'Source',citation:'Citation',stages:['Tokenize','Represent','Attend','Predict']},
  zh:{language:'语言',journey:'机制路径',previous:'上一步',next:'下一步',source:'源代码',citation:'引用',stages:['词元化','表示','注意','预测']},
  vi:{language:'Ngôn ngữ',journey:'Hành trình cơ chế',previous:'Bước trước',next:'Bước tiếp',source:'Mã nguồn',citation:'Trích dẫn',stages:['Tách token','Biểu diễn','Chú ý','Dự đoán']},
  es:{language:'Idioma',journey:'Recorrido del mecanismo',previous:'Etapa anterior',next:'Etapa siguiente',source:'Código fuente',citation:'Citación',stages:['Tokenizar','Representar','Atender','Predecir']}
};
let stageIndex=0;
const $=s=>document.querySelector(s);
const all=s=>[...document.querySelectorAll(s)];
function locale(){return (window.Lab13Localization&&window.Lab13Localization.getLocale())||'en'}
function localeCopy(){return COPY[locale()]||COPY.en}
function updateUrl(value){try{const u=new URL(location.href);u.searchParams.set('lang',value);history.replaceState(null,'',u)}catch(_){}}
function installLanguageSelect(){
  const bar=$('#lab13-locale-bar');if(!bar||$('#lab13-language-select'))return;
  const label=bar.querySelector('.locale-label');if(label)label.id='lab13-language-label';
  const select=document.createElement('select');select.id='lab13-language-select';select.className='lab13-language-select';select.setAttribute('aria-labelledby','lab13-language-label');
  for(const code of LOCALES){const option=document.createElement('option');option.value=code;option.textContent=NAMES[code];select.appendChild(option)}
  bar.appendChild(select);select.value=locale();
  select.addEventListener('change',()=>{window.Lab13Localization.setLocale(select.value);updateUrl(select.value)});
}
function targetFor(index){
  if(index===0)return [$('.controls'),$('#tokens')&&$('#tokens').closest('.card')].filter(Boolean);
  if(index===1)return [$('#vectors')&&$('#vectors').closest('.card')].filter(Boolean);
  if(index===2)return [$('#scoreMatrix')&&$('#scoreMatrix').closest('.card')].filter(Boolean);
  return [$('#bars')&&$('#bars').closest('.card')].filter(Boolean);
}
function setStage(index,scroll=false){
  stageIndex=Math.max(0,Math.min(3,index));
  all('.lab13-focus-target').forEach(el=>el.classList.remove('lab13-focus-target'));
  const stages=all('.pipeline .stage');
  stages.forEach((stage,i)=>stage.setAttribute('aria-current',i===stageIndex?'step':'false'));
  const targets=targetFor(stageIndex);targets.forEach(el=>el.classList.add('lab13-focus-target'));
  const c=localeCopy(),status=$('#lab13-journey-status');
  if(status)status.textContent=`${stageIndex+1} / 4 · ${c.stages[stageIndex]}`;
  const prev=$('#lab13-journey-prev'),next=$('#lab13-journey-next');if(prev)prev.disabled=stageIndex===0;if(next)next.disabled=stageIndex===3;
  if(scroll&&targets[0])targets[0].scrollIntoView({block:'center',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});
}
function installJourney(){
  const pipeline=$('.pipeline');if(!pipeline||$('#lab13-mechanism-journey'))return;
  const stages=all('.pipeline .stage');stages.slice(0,4).forEach((stage,i)=>{
    stage.classList.add('lab13-journey-stage');stage.tabIndex=0;stage.setAttribute('role','button');
    stage.addEventListener('click',()=>setStage(i,true));
    stage.addEventListener('keydown',event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();setStage(i,true)}});
  });
  const section=document.createElement('section');section.id='lab13-mechanism-journey';section.className='lab13-journey';section.setAttribute('aria-label','Mechanism journey');
  section.innerHTML='<div class="lab13-journey-copy"><strong id="lab13-journey-label"></strong><span id="lab13-journey-status" aria-live="polite"></span></div><div class="lab13-journey-actions"><button id="lab13-journey-prev" type="button"></button><button id="lab13-journey-next" type="button"></button></div>';
  pipeline.insertAdjacentElement('afterend',section);
  $('#lab13-journey-prev').addEventListener('click',()=>setStage(stageIndex-1,true));
  $('#lab13-journey-next').addEventListener('click',()=>setStage(stageIndex+1,true));
  setStage(0,false);
}
function localizeExperience(){
  const c=localeCopy(),select=$('#lab13-language-select'),label=$('#lab13-language-label');
  if(select)select.value=locale();if(label)label.textContent=c.language;
  const journey=$('#lab13-mechanism-journey');if(journey)journey.setAttribute('aria-label',c.journey);
  if($('#lab13-journey-label'))$('#lab13-journey-label').textContent=c.journey;
  if($('#lab13-journey-prev'))$('#lab13-journey-prev').textContent=`← ${c.previous}`;
  if($('#lab13-journey-next'))$('#lab13-journey-next').textContent=`${c.next} →`;
  if($('[data-lab13-source]'))$('[data-lab13-source]').textContent=c.source;
  if($('[data-lab13-citation]'))$('[data-lab13-citation]').textContent=c.citation;
  setStage(stageIndex,false);
}
function init(){
  if(!window.Lab13Localization)return setTimeout(init,0);
  installLanguageSelect();installJourney();localizeExperience();
  window.addEventListener('lab13localechange',()=>{updateUrl(locale());localizeExperience()});
  window.Lab13V14Experience={getStage:()=>stageIndex,setStage:index=>setStage(index,false)};
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
    html = html.replace(
        "</head>",
        f'<meta name="ai-playgrounds-version" content="{RELEASE_VERSION}">\n' + CSS + "\n</head>",
        1,
    )
    html = html.replace("</main>", FOOTER + "\n</main>", 1)
    html = html.replace("</body>", SCRIPT + "\n</body>", 1)

    required = (
        'id="lab13-v14-experience-runtime"',
        'id="lab13-v14-experience-style"',
        'data-lab13-v14-provenance',
        f'name="ai-playgrounds-version" content="{RELEASE_VERSION}"',
        'Lab13V14Experience',
    )
    missing = [marker for marker in required if marker not in html]
    if missing:
        raise RuntimeError(f"Lab 13 v1.4 experience wrapper is incomplete: {missing}")
    if "AI Playgrounds v1.3" in html:
        raise RuntimeError("Lab 13 v1.4 retains the prominent v1.3 badge")
    for token in ("<script src=", "fetch(", "XMLHttpRequest", "WebSocket(", "EventSource("):
        if token in html:
            raise RuntimeError(f"Lab 13 v1.4 violates one-file/offline boundary: {token}")

    output.write_text(html, encoding="utf-8")
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    result = build_public(output)
    print(f"Built public Lab 13 v1.4 experience: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
