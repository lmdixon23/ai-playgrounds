#!/usr/bin/env python3
from __future__ import annotations

"""Stable final lifecycle for v1.7.1 modern accessibility/packet parity.

The preceding accessibility builder owns the structured open panel and all
localized copy. This final wrapper replaces only its polling runtime with a
bounded event-driven runtime. Labs 13-15 already contain the Quick Assign and
text-state source nodes when final composition runs, so recurring readiness
polling is unnecessary.
"""

import json
import re

import build_site_v1_7_1_modern_parity_accessible as base

SITE = base.SITE
MODERN = base.MODERN
SOURCE_IDS = {
    "transformer-language-model": "stateText",
    "agent-tool-context": "stateText",
    "minimax-alpha-beta": "textState",
}


def stable_runtime(slug: str) -> str:
    labels = json.dumps(base.LABELS, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    source_id = SOURCE_IDS[slug]
    return f'''<script id="v171-modern-packet-label-runtime" data-v171-stable-lifecycle="true">
(()=>{{'use strict';
const COPY={labels};
const SOURCE_ID={json.dumps(source_id)};
const norm=v=>{{v=String(v||'').toLowerCase();return v.startsWith('zh')?'zh':v.startsWith('vi')?'vi':v.startsWith('es')?'es':'en'}};
const locale=()=>norm(document.documentElement.lang);
const root=()=>document.querySelector('[data-quick-assign-id]');
const source=()=>document.getElementById(SOURCE_ID);
function sourceText(){{const s=source();return s?String(s.value||s.textContent||'').trim():''}}
function syncAccessibleState(){{
  const out=document.getElementById('ap-modern-a11y-state');if(!out)return;
  const packet=root()?.querySelector('[data-qa-modern-state]');
  const next=sourceText()||String(packet?.textContent||'').trim();
  if(!next)return;
  if(out.textContent!==next){{out.textContent=next;const live=document.getElementById('ap-modern-a11y-live');if(live)live.textContent=next.slice(0,500)}}
}}
function paintLabels(){{
  const qa=root(),l=COPY[locale()]||COPY.en;if(!qa){{syncAccessibleState();return}}
  qa.querySelectorAll('[data-qa-answer]').forEach(el=>{{const key=el.dataset.qaAnswer;if(l[key])el.setAttribute('aria-label',l[key])}});
  for(const key of ['refresh','copy','print','clear']){{const action=key==='refresh'?'refresh-state':key;const button=qa.querySelector('[data-qa-action="'+action+'"]');if(!button)continue;const label=l[key]||COPY.en[key];button.textContent=(key==='refresh'?'↻ ':'')+label;button.setAttribute('aria-label',label)}}
  const state=qa.querySelector('[data-qa-modern-state]');if(state)state.setAttribute('aria-label',l.state||COPY.en.state);
  syncAccessibleState();
}}
let repaintGeneration=0;
function schedulePaint(){{
  const generation=++repaintGeneration;
  const run=()=>{{if(generation===repaintGeneration)paintLabels()}};
  run();queueMicrotask(run);if(window.requestAnimationFrame)requestAnimationFrame(run);
  setTimeout(run,40);setTimeout(run,110);setTimeout(run,180);
}}
const src=source();if(src){{new MutationObserver(syncAccessibleState).observe(src,{{childList:true,subtree:true,characterData:true,attributes:true}});src.addEventListener?.('input',syncAccessibleState);src.addEventListener?.('change',syncAccessibleState)}}
new MutationObserver(schedulePaint).observe(document.documentElement,{{attributes:true,attributeFilter:['lang']}});
window.addEventListener('lab13localechange',schedulePaint);window.addEventListener('lab14localechange',schedulePaint);window.addEventListener('lab15localechange',schedulePaint);
schedulePaint();syncAccessibleState();
}})();</script>'''


def replace_runtime(page: str, slug: str) -> str:
    pattern = re.compile(r'<script\b[^>]*\bid="v171-modern-packet-label-runtime"[^>]*>.*?</script>', re.S | re.I)
    page, count = pattern.subn(stable_runtime(slug), page, count=1)
    if count != 1:
        raise RuntimeError(f"Modern accessibility runtime missing before stable replacement: {slug}")
    return page


def validate() -> None:
    for slug in MODERN:
        page=(SITE/'playgrounds'/slug/'index.html').read_text(encoding='utf-8')
        required=(
            'id="v171-modern-packet-label-runtime" data-v171-stable-lifecycle="true"',
            'class="accessibility-layer ap-modern-a11y-parity" open',
            'id="ap-modern-a11y-state"', 'syncAccessibleState',
            'setTimeout(run,180)', f'const SOURCE_ID={json.dumps(SOURCE_IDS[slug])}',
        )
        missing=[m for m in required if m not in page]
        if missing: raise RuntimeError(f"Stable modern accessibility lifecycle incomplete for {slug}: {missing}")
        if 'readinessTimer' in page or 'readinessTries' in page or '__v171LabelWrapped' in page:
            raise RuntimeError(f"Polling/wrapped accessibility lifecycle survived stable composition: {slug}")
    base.validate()


def build_site() -> None:
    base.build_site()
    for slug in MODERN:
        path=SITE/'playgrounds'/slug/'index.html'
        page=replace_runtime(path.read_text(encoding='utf-8'),slug)
        path.write_text(page,encoding='utf-8')
    validate()
    print('Stabilized v1.7.1 modern accessibility/Quick Assign lifecycle without recurring readiness polling')


if __name__=='__main__':
    build_site()
