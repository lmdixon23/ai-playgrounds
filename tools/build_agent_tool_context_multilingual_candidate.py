#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from build_agent_tool_context_english_candidate import build as build_english

ROOT = Path(__file__).resolve().parents[1]
PRIMARY = ROOT / "tools" / "agent_tool_context_locales.json"
DYNAMIC = ROOT / "tools" / "agent_tool_context_locales_dynamic.json"
DEFAULT_OUTPUT = ROOT / "release-evidence" / "lab14-agent-tool-context-multilingual-candidate.html"
ENGLISH_INTERMEDIATE = ROOT / "release-evidence" / "lab14-agent-tool-context-r6-english-source.html"
R4_SOURCE_FREEZE = "9f2f5286f4de3e12a881b61d491c87efe6950166"
R5_LOCALIZATION_FREEZE = "37bdc6a4a84b672ad564d81564e8a055c2b2c9a6"
LOCALES = ("en", "zh", "vi", "es")

CSS = r'''
<style id="lab14-i18n-style">
.lab14-locale-bar{display:flex;justify-content:flex-end;align-items:center;gap:7px;flex-wrap:wrap;margin:0 0 14px;padding:8px 10px;background:var(--card);border:1px solid var(--border);border-radius:10px;font-family:system-ui,-apple-system,sans-serif}
.lab14-locale-bar .locale-label{color:var(--muted);font-size:.78rem;font-weight:700;margin-right:2px}
.lab14-locale-bar button{border:1px solid var(--border);background:var(--card);color:var(--fg);border-radius:7px;padding:6px 9px;cursor:pointer;min-height:34px}
.lab14-locale-bar button[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:700}
@media(max-width:480px){.lab14-locale-bar{justify-content:flex-start}.lab14-locale-bar button{min-height:42px}}
</style>
'''

BAR = r'''
<section id="lab14-locale-bar" class="lab14-locale-bar" aria-label="Language" data-lab14-no-translate="true">
  <span class="locale-label">Language</span>
  <button type="button" data-locale="en">EN</button>
  <button type="button" data-locale="zh">中文</button>
  <button type="button" data-locale="vi">VI</button>
  <button type="button" data-locale="es">ES</button>
</section>
'''

RUNTIME_TEMPLATE = r'''
<script id="lab14-i18n-runtime">
(()=>{'use strict';
const CATALOGS=__CATALOGS__;
const META={r4SourceFreeze:'__R4__',r5LocalizationFreeze:'__R5__'};
const LOCALES=['en','zh','vi','es'];
const HTML_LANG={en:'en',zh:'zh-Hans',vi:'vi',es:'es'};
let active='en',observer=null,mutating=false;

function parseTemplate(template){
  const parts=[],names=[];let pos=0;
  while(pos<template.length){
    const open=template.indexOf('{',pos);if(open<0){parts.push(template.slice(pos));break;}
    const close=template.indexOf('}',open+1);if(close<0){parts.push(template.slice(pos));break;}
    const name=template.slice(open+1,close);
    if(!/^[A-Za-z0-9_]+$/.test(name)){parts.push(template.slice(pos));break;}
    parts.push(template.slice(pos,open));names.push(name);pos=close+1;
    if(pos===template.length)parts.push('');
  }
  if(parts.length===0)parts.push(template);
  return {parts,names,literal:parts.reduce((n,p)=>n+p.length,0)};
}
const exact=new Map(),templates=[],staticEntries=[];
for(const key of Object.keys(CATALOGS.en)){
  for(const locale of LOCALES){
    const value=String(CATALOGS[locale][key]);
    const parsed=parseTemplate(value);const entry={key,locale,value,...parsed};
    if(parsed.names.length===0){if(!exact.has(value))exact.set(value,key);if(value.length>=2)staticEntries.push(entry)}
    else templates.push(entry);
  }
}
templates.sort((a,b)=>b.literal-a.literal||a.names.length-b.names.length);
staticEntries.sort((a,b)=>b.value.length-a.value.length);

function matchTemplate(entry,text){
  const {parts,names}=entry;if(!text.startsWith(parts[0]))return null;
  let pos=parts[0].length;const vars={};
  for(let i=0;i<names.length;i++){
    const next=parts[i+1];
    if(next===''){vars[names[i]]=text.slice(pos);pos=text.length;continue;}
    const at=text.indexOf(next,pos);if(at<0)return null;
    vars[names[i]]=text.slice(pos,at);pos=at+next.length;
  }
  return pos===text.length?vars:null;
}
function translateTemplate(key,vars,target,depth){
  const template=String(CATALOGS[target][key]);let out='',pos=0;
  while(pos<template.length){
    const open=template.indexOf('{',pos);if(open<0){out+=template.slice(pos);break;}
    const close=template.indexOf('}',open+1);if(close<0){out+=template.slice(pos);break;}
    const name=template.slice(open+1,close);out+=template.slice(pos,open);
    out+=translateCore(Object.hasOwn(vars,name)?String(vars[name]):`{${name}}`,target,depth+1);pos=close+1;
  }
  return out;
}
function translateJsonValue(value,target){
  if(typeof value==='string')return translateCore(value,target,1);
  if(Array.isArray(value))return value.map(v=>translateJsonValue(v,target));
  if(value&&typeof value==='object'){const out={};for(const [k,v] of Object.entries(value))out[k]=translateJsonValue(v,target);return out;}
  return value;
}
function translateCore(text,target,depth=0){
  if(depth>8||text===null||text===undefined)return text;
  text=String(text);if(!text)return text;
  const key=exact.get(text);if(key!==undefined)return String(CATALOGS[target][key]);
  for(const entry of templates){const vars=matchTemplate(entry,text);if(vars!==null)return translateTemplate(entry.key,vars,target,depth);}
  const trimmed=text.trim();
  if(trimmed&&(trimmed[0]==='{'||trimmed[0]==='[')){
    try{return JSON.stringify(translateJsonValue(JSON.parse(trimmed),target));}catch(_){}
  }
  if(text.startsWith('TEXT: '))return 'TEXT: '+translateCore(text.slice(6),target,depth+1);
  if(text.includes('\n'))return text.split('\n').map(line=>translateCore(line,target,depth+1)).join('\n');
  for(const entry of staticEntries){
    if(text===entry.value||!text.startsWith(entry.value))continue;
    const rest=text.slice(entry.value.length);if(!rest||!' :;,.!?→()-'.includes(rest[0]))continue;
    return String(CATALOGS[target][entry.key])+translateCore(rest,target,depth+1);
  }
  return text;
}
function translateTextValue(value,target){
  const raw=String(value);const core=raw.trim();if(!core)return raw;
  const lead=raw.slice(0,raw.length-raw.trimStart().length);const trail=raw.slice(raw.trimEnd().length);
  return lead+translateCore(core,target,0)+trail;
}
function shouldSkip(node){
  const p=node.parentElement;if(!p)return true;
  return p.tagName==='SCRIPT'||p.tagName==='STYLE'||!!p.closest('#lab14-locale-bar,#stateText,[data-lab14-no-translate]');
}
function translateState(){
  const node=document.getElementById('stateText');if(!node)return;
  try{const next=JSON.stringify(translateJsonValue(JSON.parse(node.textContent),active),null,2);if(node.textContent!==next)node.textContent=next;}catch(_){}
}
function observe(){if(observer)observer.observe(document.body,{subtree:true,childList:true,characterData:true});}
function translateTree(root=document.body){
  if(!root||mutating)return;mutating=true;if(observer)observer.disconnect();
  try{
    const walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);const nodes=[];let n;while((n=walker.nextNode()))nodes.push(n);
    for(const node of nodes){if(shouldSkip(node))continue;const next=translateTextValue(node.nodeValue,active);if(next!==node.nodeValue)node.nodeValue=next;}
    const elements=root.querySelectorAll?root.querySelectorAll('[title],[aria-label],[placeholder]'):[];
    for(const el of elements){if(el.closest('#lab14-locale-bar,[data-lab14-no-translate]'))continue;for(const attr of ['title','aria-label','placeholder'])if(el.hasAttribute(attr)){const before=el.getAttribute(attr),after=translateTextValue(before,active);if(after!==before)el.setAttribute(attr,after);}}
    translateState();document.title=`${CATALOGS[active]['page.title']} — Lab 14`;
  }finally{mutating=false;observe();}
}
function updateButtons(){for(const button of document.querySelectorAll('#lab14-locale-bar button[data-locale]'))button.setAttribute('aria-pressed',button.dataset.locale===active?'true':'false');}
function setLocale(locale){
  if(!LOCALES.includes(locale))throw new Error(`Unsupported locale: ${locale}`);
  active=locale;document.documentElement.lang=HTML_LANG[locale];updateButtons();translateTree(document.body);
  window.dispatchEvent(new CustomEvent('lab14localechange',{detail:{locale}}));
}
function getLocale(){return active;}
for(const button of document.querySelectorAll('#lab14-locale-bar button[data-locale]'))button.addEventListener('click',()=>setLocale(button.dataset.locale));
observer=new MutationObserver(records=>{
  if(mutating||active==='en')return;const roots=new Set();
  for(const record of records){
    for(const node of record.addedNodes){if(node.nodeType===Node.ELEMENT_NODE)roots.add(node);else if(node.nodeType===Node.TEXT_NODE&&node.parentElement)roots.add(node.parentElement);}
    if(record.type==='characterData'&&record.target.parentElement)roots.add(record.target.parentElement);
  }
  for(const root of roots)translateTree(root);
});
observe();window.Lab14Localization={setLocale,getLocale,catalogs:CATALOGS,translate:translateCore,meta:META};
active='en';document.documentElement.lang='en';updateButtons();document.title=`${CATALOGS.en['page.title']} — Lab 14`;
const requested=new URLSearchParams(location.search).get('lang');if(LOCALES.includes(requested)&&requested!=='en')setTimeout(()=>setLocale(requested),0);
})();
</script>
'''


def load_catalogs() -> dict[str, dict[str, str]]:
    merged: dict[str, dict[str, str]] = {}
    for path in (PRIMARY, DYNAMIC):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("source_freeze_head") != R4_SOURCE_FREEZE:
            raise RuntimeError(f"{path.name} is not bound to the frozen R4 source")
        for key, entry in payload.get("strings", {}).items():
            if set(entry) != set(LOCALES):
                raise RuntimeError(f"{path.name}:{key} does not contain exactly en/zh/vi/es")
            normalized = {locale: str(entry[locale]) for locale in LOCALES}
            if key in merged and merged[key] != normalized:
                raise RuntimeError(f"Conflicting localization key across R5 catalogs: {key}")
            merged[key] = normalized
    if len(merged) != 163:
        raise RuntimeError(f"Expected 163 merged R5 keys, found {len(merged)}")
    catalogs = {locale: {} for locale in LOCALES}
    for key, entry in merged.items():
        for locale in LOCALES:
            catalogs[locale][key] = entry[locale]
    return catalogs


def build(output: Path) -> Path:
    build_english(ENGLISH_INTERMEDIATE)
    source = ENGLISH_INTERMEDIATE.read_text(encoding="utf-8")
    catalogs = load_catalogs()
    payload = json.dumps(catalogs, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    runtime = RUNTIME_TEMPLATE.replace("__CATALOGS__", payload).replace("__R4__", R4_SOURCE_FREEZE).replace("__R5__", R5_LOCALIZATION_FREEZE)

    runtime_js = runtime.split(">", 1)[1].rsplit("</script>", 1)[0]
    syntax = subprocess.run(["node", "--check", "-"], input=runtime_js, text=True, capture_output=True, check=False)
    if syntax.returncode:
        raise RuntimeError(f"R6 localization runtime syntax failure: {syntax.stderr[-1200:]}")

    required = [
        '<html lang="en">',
        '<script id="lab14-agent-tool-context-core">',
        'window.Lab14Prototype',
        'id="model-check"',
        'id="key-terms"',
        '</style>',
        '<main>',
        '</body>',
    ]
    missing = [marker for marker in required if marker not in source]
    if missing:
        raise RuntimeError(f"Frozen R4 English candidate no longer matches R6 builder contract: {missing}")

    generated = source.replace("</style>", "</style>\n" + CSS, 1)
    generated = generated.replace("<main>", "<main>\n" + BAR, 1)
    generated = generated.replace("</body>", runtime + "\n</body>", 1)
    generated = generated.replace("non-public v1.3 English candidate", "non-public v1.3 four-locale candidate", 1)

    if "<script src=" in generated:
        raise RuntimeError("R6 candidate contains an external script dependency")
    for token in ("fetch(", "XMLHttpRequest", "WebSocket(", "EventSource("):
        if token in generated:
            raise RuntimeError(f"R6 candidate contains forbidden runtime network primitive: {token}")
    for locale in ("zh", "vi", "es"):
        if catalogs[locale]["page.title"] not in generated:
            raise RuntimeError(f"R6 candidate does not embed {locale} localization content")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(generated, encoding="utf-8")
    print(json.dumps({
        "builder": "tools/build_agent_tool_context_multilingual_candidate.py",
        "output": str(output.relative_to(ROOT)) if output.is_relative_to(ROOT) else str(output),
        "r4_source_freeze": R4_SOURCE_FREEZE,
        "r5_localization_freeze": R5_LOCALIZATION_FREEZE,
        "locales": list(LOCALES),
        "keys_per_locale": len(catalogs["en"]),
        "bytes": output.stat().st_size,
        "single_file": True,
        "runtime_syntax": "PASS",
        "pass": True,
    }, ensure_ascii=False, indent=2))
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    build(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
