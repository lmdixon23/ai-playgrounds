#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tools" / "transformer_language_model_applet_en.html"
BASE_CATALOG = ROOT / "tools" / "transformer_language_model_locales.json"
VI_ES_CATALOG = ROOT / "tools" / "transformer_language_model_locales_vi_es.json"
DEFAULT_OUTPUT = ROOT / "release-evidence" / "lab13-transformer-multilingual-candidate.html"
EXPECTED_FREEZE = "e89c0b5d8b166b66407fc018deb1b7eec485b6a4"

CSS = r"""
<style id="lab13-i18n-style">
.lab13-locale-bar{display:flex;justify-content:flex-end;align-items:center;gap:7px;flex-wrap:wrap;margin:0 0 14px;padding:8px 10px;background:var(--card);border:1px solid var(--border);border-radius:10px;font-family:system-ui,-apple-system,sans-serif}
.lab13-locale-bar .locale-label{color:var(--muted);font-size:.78rem;font-weight:700;margin-right:2px}
.lab13-locale-bar button{border:1px solid var(--border);background:var(--card);color:var(--fg);border-radius:7px;padding:6px 9px;cursor:pointer;min-height:34px}
.lab13-locale-bar button[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:700}
@media(max-width:480px){.lab13-locale-bar{justify-content:flex-start}.lab13-locale-bar button{min-height:42px}}
</style>
"""

RUNTIME_TEMPLATE = r"""
<script id="lab13-i18n-runtime">
(()=>{'use strict';
const CATALOGS=__CATALOGS__;
const LOCALES=['en','zh','vi','es'];
const HTML_LANG={en:'en',zh:'zh-Hans',vi:'vi',es:'es'};
const DISPLAY={en:'EN',zh:'中文',vi:'VI',es:'ES'};
const PLACEHOLDER=/\{([A-Za-z0-9_]+)\}/g;
let active='en',mutating=false;

function escapeRe(value){return value.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')}
function compile(template){
  const names=[];let source='^',last=0,m;PLACEHOLDER.lastIndex=0;
  while((m=PLACEHOLDER.exec(template))){source+=escapeRe(template.slice(last,m.index))+'([\\s\\S]+?)';names.push(m[1]);last=m.index+m[0].length}
  source+=escapeRe(template.slice(last))+'$';
  return{re:new RegExp(source),names,literal:template.replace(PLACEHOLDER,'').length};
}
const patterns=[];
for(const key of Object.keys(CATALOGS.en)){
  for(const locale of LOCALES){
    const value=String(CATALOGS[locale][key]);
    const compiled=compile(value);patterns.push({key,locale,value,...compiled});
  }
}
patterns.sort((a,b)=>b.literal-a.literal||a.names.length-b.names.length);
const staticPatterns=patterns.filter(p=>p.names.length===0&&p.value.length>=3).sort((a,b)=>b.value.length-a.value.length);

function formatTarget(key,vars,target,depth){
  const template=String(CATALOGS[target][key]);
  return template.replace(PLACEHOLDER,(_,name)=>translateCore(Object.hasOwn(vars,name)?String(vars[name]):`{${name}}`,target,depth+1));
}
function directMatch(text,target,depth){
  for(const p of patterns){
    const match=p.re.exec(text);if(!match)continue;
    const vars={};p.names.forEach((name,index)=>{vars[name]=match[index+1]});
    return formatTarget(p.key,vars,target,depth);
  }
  return null;
}
function prefixedMatch(text,target,depth){
  for(const p of staticPatterns){
    if(text===p.value||!text.startsWith(p.value))continue;
    const rest=text.slice(p.value.length);if(!/^[\s:;,.!?→()\-]/.test(rest))continue;
    const translatedPrefix=String(CATALOGS[target][p.key]);
    return translatedPrefix+translateCore(rest,target,depth+1);
  }
  return null;
}
function translateCore(text,target,depth=0){
  if(depth>4||!text)return text;
  const direct=directMatch(text,target,depth);if(direct!==null)return direct;
  if(text.includes('\n'))return text.split('\n').map(line=>translateCore(line,target,depth+1)).join('\n');
  const prefixed=prefixedMatch(text,target,depth);if(prefixed!==null)return prefixed;
  return text;
}
function translateTextValue(value,target){
  const match=String(value).match(/^(\s*)([\s\S]*?)(\s*)$/);if(!match)return value;
  return match[1]+translateCore(match[2],target,0)+match[3];
}
function shouldSkip(node){
  const parent=node.parentElement;if(!parent)return true;
  return !!parent.closest('script,style,#lab13-locale-bar,[data-lab13-no-translate]');
}
function translateTree(root=document.body){
  if(mutating||!root)return;mutating=true;
  try{
    const walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);const nodes=[];let node;
    while((node=walker.nextNode()))nodes.push(node);
    for(const textNode of nodes){if(shouldSkip(textNode))continue;const next=translateTextValue(textNode.nodeValue,active);if(next!==textNode.nodeValue)textNode.nodeValue=next}
    for(const element of root.querySelectorAll('[title],[aria-label],[placeholder]')){
      if(element.closest('#lab13-locale-bar,[data-lab13-no-translate]'))continue;
      for(const attr of ['title','aria-label','placeholder'])if(element.hasAttribute(attr)){
        const before=element.getAttribute(attr),after=translateTextValue(before,active);if(after!==before)element.setAttribute(attr,after);
      }
    }
    document.title=`${CATALOGS[active]['page.title']} — Lab 13`;
  }finally{mutating=false}
}
function installBar(){
  const main=document.querySelector('main');if(!main||document.getElementById('lab13-locale-bar'))return;
  const bar=document.createElement('section');bar.id='lab13-locale-bar';bar.className='lab13-locale-bar';bar.setAttribute('aria-label','Language');bar.setAttribute('data-lab13-no-translate','true');
  const label=document.createElement('span');label.className='locale-label';label.textContent='Language';bar.appendChild(label);
  for(const locale of LOCALES){const button=document.createElement('button');button.type='button';button.dataset.locale=locale;button.textContent=DISPLAY[locale];button.addEventListener('click',()=>setLocale(locale));bar.appendChild(button)}
  main.prepend(bar);
}
function setLocale(locale){
  if(!LOCALES.includes(locale))throw new Error(`Unsupported locale: ${locale}`);
  active=locale;document.documentElement.lang=HTML_LANG[locale];
  for(const button of document.querySelectorAll('#lab13-locale-bar button[data-locale]'))button.setAttribute('aria-pressed',button.dataset.locale===locale?'true':'false');
  translateTree(document.body);window.dispatchEvent(new CustomEvent('lab13localechange',{detail:{locale}}));
}
function getLocale(){return active}
installBar();
const observer=new MutationObserver(records=>{if(mutating)return;for(const record of records){for(const node of record.addedNodes){if(node.nodeType===Node.ELEMENT_NODE)translateTree(node);else if(node.nodeType===Node.TEXT_NODE&&node.parentElement)translateTree(node.parentElement)}if(record.type==='characterData'&&record.target.parentElement)translateTree(record.target.parentElement)}});
observer.observe(document.body,{subtree:true,childList:true,characterData:true,attributes:false});
window.Lab13Localization={setLocale,getLocale,catalogs:CATALOGS,translate:translateCore};
setLocale('en');
})();
</script>
"""


def load_catalogs() -> dict[str, dict[str, str]]:
    base = json.loads(BASE_CATALOG.read_text(encoding="utf-8"))
    extra = json.loads(VI_ES_CATALOG.read_text(encoding="utf-8"))
    if base.get("source_freeze_head") != EXPECTED_FREEZE:
        raise RuntimeError("Base Lab 13 catalog is not bound to the accepted English freeze")
    if extra.get("source_freeze_head") != EXPECTED_FREEZE:
        raise RuntimeError("VI/ES Lab 13 catalog is not bound to the accepted English freeze")
    catalogs = dict(base.get("locales", {}))
    catalogs.update(extra.get("locales", {}))
    if set(catalogs) != {"en", "zh", "vi", "es"}:
        raise RuntimeError(f"Expected exactly en/zh/vi/es catalogs, found {sorted(catalogs)}")
    keyset = set(catalogs["en"])
    for locale, catalog in catalogs.items():
        if set(catalog) != keyset:
            raise RuntimeError(f"Catalog key mismatch for {locale}")
    return catalogs


def build(output: Path) -> Path:
    source = SOURCE.read_text(encoding="utf-8")
    required_markers = [
        "window.TransformerLanguageModelCore",
        "Guided Challenge",
        "Attention is not an explanation",
        "</style>",
        "</body>",
    ]
    missing = [marker for marker in required_markers if marker not in source]
    if missing:
        raise RuntimeError(f"English applet source no longer matches the frozen builder contract: {missing}")

    catalogs = load_catalogs()
    payload = json.dumps(catalogs, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    runtime = RUNTIME_TEMPLATE.replace("__CATALOGS__", payload)
    generated = source.replace("</style>", "</style>\n" + CSS, 1).replace("</body>", runtime + "\n</body>", 1)

    if "fetch(" in generated or "XMLHttpRequest" in generated:
        raise RuntimeError("Generated multilingual candidate contains a runtime network primitive")
    for locale in ("zh", "vi", "es"):
        if catalogs[locale]["page.title"] not in generated:
            raise RuntimeError(f"Generated candidate does not embed {locale} catalog content")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(generated, encoding="utf-8")
    print(json.dumps({
        "builder": "tools/build_transformer_multilingual_candidate.py",
        "source": str(SOURCE.relative_to(ROOT)),
        "output": str(output.relative_to(ROOT)) if output.is_relative_to(ROOT) else str(output),
        "locales": sorted(catalogs),
        "keys_per_locale": len(catalogs["en"]),
        "bytes": output.stat().st_size,
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
