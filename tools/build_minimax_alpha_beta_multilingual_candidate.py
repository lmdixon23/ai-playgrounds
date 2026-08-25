#!/usr/bin/env python3
"""Build the R6 EN/ZH/VI/ES Lab 15 candidate over the frozen R4 English source."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from build_minimax_alpha_beta_english_candidate import build_candidate as build_english

ROOT = Path(__file__).resolve().parents[1]
R4_SOURCE_FREEZE = "f904e6d68f71602dced73e99d259eee055899bc2"
DEFAULT_OUTPUT = ROOT / "release-evidence" / "lab15-minimax-alpha-beta-multilingual-candidate.html"
LOCALES = ("en", "zh", "vi", "es")

STYLE = r'''
<style id="lab15-r6-locale-style">
.lab15-locale-bar{display:flex;justify-content:flex-end;align-items:center;gap:8px;margin:0 0 12px;padding:8px 10px;border:1px solid var(--border);border-radius:10px;background:var(--card)}
.lab15-locale-bar label{font-size:.78rem;font-weight:800;color:var(--muted)}
.lab15-language-select{min-height:38px;padding:6px 32px 6px 10px;border:1px solid var(--border);border-radius:8px;background:var(--card);color:var(--fg);font:inherit;cursor:pointer}
.lab15-language-select:focus-visible{outline:3px solid #3157c855;outline-offset:2px}
@media(pointer:coarse){.lab15-language-select{min-height:44px}}
@media(max-width:560px){
  html,body{max-width:100%;overflow-x:hidden}
  .shell,.grid,.panel,.challenge-grid,.challenge-box,.controls,.summary,.utility-list,.transport,.tree-wrap{min-width:0;max-width:100%}
  .shell{width:100%}
  .tree-wrap{width:100%;overflow-x:auto;overflow-y:hidden}
  .utility-item label{min-width:0;flex-wrap:wrap;overflow-wrap:anywhere}
  .utility-item input{max-width:100%}
  .lab15-locale-bar{justify-content:stretch;flex-wrap:wrap;min-width:0;max-width:100%}
  .lab15-language-select{flex:1 1 180px;min-width:0;max-width:100%}
}
</style>
'''

RUNTIME = r'''
<script id="lab15-r6-localization-runtime">
(() => {
  "use strict";
  const DATA = JSON.parse(document.getElementById("lab15-locale-data").textContent);
  const LOCALES = ["en", "zh", "vi", "es"];
  const NAMES = {en:"English", zh:"简体中文", vi:"Tiếng Việt", es:"Español"};
  const HTML_LANG = {en:"en", zh:"zh-Hans", vi:"vi", es:"es"};
  const catalogs = DATA.catalogs;
  let current = "en";
  let scheduled = false;
  let observer = null;
  let mutating = false;

  const exactToKey = new Map();
  const phraseEntries = [];
  const templateEntries = [];

  function escapeRe(text){return text.replace(/[.*+?^${}()|[\]\\]/g,"\\$&")}
  function compileTemplate(value, key){
    const names=[];
    let cursor=0, pattern="^";
    const re=/\{([A-Za-z0-9_]+)\}/g;
    let match;
    while((match=re.exec(value))){
      pattern += escapeRe(value.slice(cursor,match.index));
      names.push(match[1]);
      pattern += "([\\s\\S]*?)";
      cursor = match.index + match[0].length;
    }
    pattern += escapeRe(value.slice(cursor)) + "$";
    return {key,names,re:new RegExp(pattern),literal:value.replace(/\{[A-Za-z0-9_]+\}/g,"").length};
  }
  for(const locale of LOCALES){
    const cat=catalogs[locale];
    for(const [key,value] of Object.entries(cat)){
      if(!exactToKey.has(value)) exactToKey.set(value,key);
      if(/\{[A-Za-z0-9_]+\}/.test(value)) templateEntries.push(compileTemplate(value,key));
      else if(value.length>=8) phraseEntries.push({key,value,length:value.length});
    }
  }
  templateEntries.sort((a,b)=>b.literal-a.literal);
  phraseEntries.sort((a,b)=>b.length-a.length);

  function format(template,args){
    return template.replace(/\{([A-Za-z0-9_]+)\}/g,(_,name)=>Object.prototype.hasOwnProperty.call(args,name)?args[name]:`{${name}}`);
  }
  function direct(text){
    const key=exactToKey.get(text);
    return key && Object.prototype.hasOwnProperty.call(catalogs[current],key) ? catalogs[current][key] : null;
  }
  function translateTemplate(text){
    for(const entry of templateEntries){
      const match=entry.re.exec(text);
      if(!match) continue;
      const args={};
      entry.names.forEach((name,index)=>{
        const raw=match[index+1];
        const translated=direct(raw);
        args[name]=translated===null ? raw : translated;
      });
      return format(catalogs[current][entry.key],args);
    }
    return null;
  }
  function translateScalar(text){
    if(!text) return text;
    const exact=direct(text); if(exact!==null) return exact;
    if(text.includes("\n")){
      return text.split("\n").map(line=>translateScalar(line)).join("\n");
    }
    const ws=/^(\s*)([\s\S]*?)(\s*)$/.exec(text);
    if(ws && ws[2]){
      const coreDirect=direct(ws[2]);
      if(coreDirect!==null) return ws[1]+coreDirect+ws[3];
      const coreTemplate=translateTemplate(ws[2]);
      if(coreTemplate!==null) return ws[1]+coreTemplate+ws[3];
    }
    const templated=translateTemplate(text); if(templated!==null) return templated;
    let out=text;
    for(const entry of phraseEntries){
      if(!out.includes(entry.value)) continue;
      const target=catalogs[current][entry.key];
      if(target!==entry.value) out=out.split(entry.value).join(target);
    }
    return out;
  }
  function skipElement(el){
    return !!(el && el.closest && el.closest("#lab15-locale-data,[data-lab15-no-translate]"));
  }
  function localizeAttributes(el){
    if(skipElement(el)) return;
    for(const name of ["aria-label","title","placeholder"]){
      if(!el.hasAttribute || !el.hasAttribute(name)) continue;
      const before=el.getAttribute(name), after=translateScalar(before);
      if(after!==before) el.setAttribute(name,after);
    }
  }
  function localizeTextNode(node){
    if(!node || node.nodeType!==Node.TEXT_NODE) return;
    const parent=node.parentElement;
    if(!parent || ["SCRIPT","STYLE","NOSCRIPT"].includes(parent.tagName) || skipElement(parent)) return;
    const before=node.nodeValue, after=translateScalar(before);
    if(after!==before) node.nodeValue=after;
  }
  function localizeTree(root){
    if(!root) return;
    if(root.nodeType===Node.TEXT_NODE){localizeTextNode(root);return;}
    if(root.nodeType!==Node.ELEMENT_NODE && root.nodeType!==Node.DOCUMENT_NODE) return;
    if(root.nodeType===Node.ELEMENT_NODE) localizeAttributes(root);
    const walker=document.createTreeWalker(root,NodeFilter.SHOW_ELEMENT|NodeFilter.SHOW_TEXT);
    let node=walker.currentNode;
    while(node){
      if(node.nodeType===Node.TEXT_NODE) localizeTextNode(node);
      else if(node.nodeType===Node.ELEMENT_NODE) localizeAttributes(node);
      node=walker.nextNode();
    }
  }
  function updateChrome(){
    const htmlLang=HTML_LANG[current];
    if(document.documentElement.lang!==htmlLang) document.documentElement.lang=htmlLang;
    const nextTitle=translateScalar(document.title);
    if(document.title!==nextTitle) document.title=nextTitle;
    const label=document.getElementById("lab15-language-label");
    const labelText=catalogs[current]["locale.language"];
    if(label && label.textContent!==labelText) label.textContent=labelText;
    const select=document.getElementById("lab15-language-select");
    if(select && select.value!==current) select.value=current;
  }
  function updateUrl(){
    try{const url=new URL(location.href);url.searchParams.set("lang",current);history.replaceState(null,"",url)}catch(_){ }
  }
  function observe(){
    if(observer && !mutating){
      observer.observe(document.body,{subtree:true,childList:true,characterData:true,attributes:true,attributeFilter:["aria-label","title","placeholder"]});
    }
  }
  function localizeScoped(root=document.body){
    if(!root || mutating) return;
    mutating=true;
    if(observer) observer.disconnect();
    try{
      localizeTree(root);
      updateChrome();
    }finally{
      mutating=false;
      observe();
    }
  }
  function localizeAll(){localizeScoped(document.body)}
  function schedule(){
    if(scheduled) return;
    scheduled=true;
    queueMicrotask(()=>{
      scheduled=false;
      localizeAll();
    });
  }
  function setLocale(code,{updateHistory=true}={}){
    if(!LOCALES.includes(code)) code="en";
    current=code;
    localizeAll();
    if(updateHistory) updateUrl();
    window.dispatchEvent(new CustomEvent("lab15localechange",{detail:{locale:current}}));
    return current;
  }
  function installBar(){
    const main=document.querySelector("main.shell"); if(!main || document.getElementById("lab15-locale-bar")) return;
    const bar=document.createElement("div");bar.id="lab15-locale-bar";bar.className="lab15-locale-bar";bar.setAttribute("data-lab15-no-translate","true");
    const label=document.createElement("label");label.id="lab15-language-label";label.htmlFor="lab15-language-select";
    const select=document.createElement("select");select.id="lab15-language-select";select.className="lab15-language-select";select.setAttribute("aria-labelledby","lab15-language-label");
    for(const code of LOCALES){const option=document.createElement("option");option.value=code;option.textContent=NAMES[code];select.appendChild(option)}
    select.addEventListener("change",()=>setLocale(select.value));bar.append(label,select);main.prepend(bar);
  }
  function initialLocale(){
    try{const value=new URL(location.href).searchParams.get("lang");return LOCALES.includes(value)?value:"en"}catch(_){return"en"}
  }
  function init(){
    installBar();
    current=initialLocale();
    localizeAll();
    observer=new MutationObserver(mutations=>{
      if(mutating) return;
      if(mutations.some(m=>m.type==="characterData" || m.type==="attributes" || m.addedNodes.length || m.removedNodes.length)) schedule();
    });
    observe();
    window.Lab15Localization={
      locale:()=>current,
      getLocale:()=>current,
      setLocale:(code)=>setLocale(code),
      catalog:(code=current)=>({...catalogs[code]}),
      locales:()=>LOCALES.slice(),
      sourceFreeze:()=>DATA.source_freeze_head,
      relocalize:()=>localizeAll()
    };
  }
  init();
})();
</script>
'''


def load_catalogs() -> dict[str, dict[str, str]]:
    catalogs: dict[str, dict[str, str]] = {}
    for locale in LOCALES:
        path = ROOT / "tools" / f"minimax_alpha_beta_locale_{locale}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("source_freeze_head") != R4_SOURCE_FREEZE:
            raise RuntimeError(f"{path.name} is not bound to the R4 source freeze")
        if data.get("locale") != locale or data.get("schema") != "ai-playgrounds-lab15-locale-v1":
            raise RuntimeError(f"invalid Lab 15 locale metadata: {path.name}")
        strings = data.get("strings")
        if not isinstance(strings, dict):
            raise RuntimeError(f"missing Lab 15 strings: {path.name}")
        catalogs[locale] = {str(key): str(value) for key, value in strings.items()}

    fragments_path = ROOT / "tools" / "minimax_alpha_beta_locale_fragments.json"
    fragments = json.loads(fragments_path.read_text(encoding="utf-8"))
    if fragments.get("source_freeze_head") != R4_SOURCE_FREEZE:
        raise RuntimeError("Lab 15 locale fragments are not bound to the R4 source freeze")
    if fragments.get("schema") != "ai-playgrounds-lab15-locale-fragments-v1":
        raise RuntimeError("invalid Lab 15 locale fragment schema")
    fragment_locales = fragments.get("locales")
    if not isinstance(fragment_locales, dict) or set(fragment_locales) != set(LOCALES):
        raise RuntimeError("Lab 15 locale fragment set mismatch")

    for locale in LOCALES:
        supplement = fragment_locales[locale]
        if not isinstance(supplement, dict):
            raise RuntimeError(f"invalid Lab 15 fragment catalog: {locale}")
        overlap = set(catalogs[locale]) & set(supplement)
        if overlap:
            raise RuntimeError(f"duplicate Lab 15 locale keys for {locale}: {sorted(overlap)}")
        catalogs[locale].update({str(key): str(value) for key, value in supplement.items()})

    keys = set(catalogs["en"])
    if len(keys) < 120:
        raise RuntimeError("Lab 15 merged presentation catalog is unexpectedly small")
    for locale in LOCALES[1:]:
        if set(catalogs[locale]) != keys:
            raise RuntimeError(f"Lab 15 merged locale key mismatch: {locale}")
    return catalogs


def insert_before_last(text: str, marker: str, fragment: str) -> str:
    index = text.rfind(marker)
    if index < 0:
        raise RuntimeError(f"could not locate final {marker}")
    return text[:index] + fragment + text[index:]


def build_candidate(output: Path) -> Path:
    english_path = ROOT / "release-evidence" / "lab15-minimax-alpha-beta-r6-english-source.html"
    build_english(english_path)
    html = english_path.read_text(encoding="utf-8")
    catalogs = load_catalogs()

    html = html.replace(
        '<meta name="lab15-candidate-stage" content="R4-English">',
        '<meta name="lab15-candidate-stage" content="R6-Multilingual">',
        1,
    )
    html = html.replace("R4 English candidate", "R6 · EN/ZH/VI/ES", 1)
    html = html.replace(
        "<title>Lab 15 Prototype | Minimax and Alpha-Beta</title>",
        f"<title>{catalogs['en']['page.title']}</title>",
        1,
    )
    html = html.replace("</head>", STYLE + "\n</head>", 1)

    payload = json.dumps(
        {"source_freeze_head": R4_SOURCE_FREEZE, "catalogs": catalogs},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).replace("</", "<\\/")
    data_script = f'<script id="lab15-locale-data" type="application/json">{payload}</script>\n'
    html = insert_before_last(html, "</body>", data_script + RUNTIME + "\n")

    required = (
        'name="lab15-candidate-stage" content="R6-Multilingual"',
        'id="lab15-locale-data"',
        'id="lab15-r6-localization-runtime"',
        'id="lab15-r6-locale-style"',
        "window.Lab15Localization",
        R4_SOURCE_FREEZE,
        "R6 · EN/ZH/VI/ES",
        f"<title>{catalogs['en']['page.title']}</title>",
    )
    missing = [item for item in required if item not in html]
    if missing:
        raise RuntimeError(f"Lab 15 R6 candidate incomplete: {missing}")
    if html.count("function minimax(") != 1 or html.count("function alphaBeta(") != 1:
        raise RuntimeError("Lab 15 R6 candidate must preserve exactly one implementation of each search algorithm")
    forbidden = ("fetch(", "XMLHttpRequest", "WebSocket", "EventSource")
    present = [item for item in forbidden if item in html]
    if present:
        raise RuntimeError(f"Lab 15 R6 candidate is not offline/self-contained: {present}")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    result = build_candidate(output)
    catalogs = load_catalogs()
    print(
        "Built Lab 15 R6 four-locale candidate: "
        f"{result} ({result.stat().st_size} bytes, {len(catalogs['en'])} presentation keys/locale)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
