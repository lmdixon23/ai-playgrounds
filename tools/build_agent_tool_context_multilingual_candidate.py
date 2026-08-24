#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
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

CSS = r'''\n<style id="lab14-i18n-style">\n.lab14-locale-bar{display:flex;justify-content:flex-end;align-items:center;gap:7px;flex-wrap:wrap;margin:0 0 14px;padding:8px 10px;background:var(--card);border:1px solid var(--border);border-radius:10px;font-family:system-ui,-apple-system,sans-serif}\n.lab14-locale-bar .locale-label{color:var(--muted);font-size:.78rem;font-weight:700;margin-right:2px}\n.lab14-locale-bar button{border:1px solid var(--border);background:var(--card);color:var(--fg);border-radius:7px;padding:6px 9px;cursor:pointer;min-height:34px}\n.lab14-locale-bar button[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:700}\n@media(max-width:480px){.lab14-locale-bar{justify-content:flex-start}.lab14-locale-bar button{min-height:42px}}\n</style>\n'''

BAR = r'''\n<section id="lab14-locale-bar" class="lab14-locale-bar" aria-label="Language" data-lab14-no-translate="true">\n  <span class="locale-label">Language</span>\n  <button type="button" data-locale="en">EN</button>\n  <button type="button" data-locale="zh">中文</button>\n  <button type="button" data-locale="vi">VI</button>\n  <button type="button" data-locale="es">ES</button>\n</section>\n'''

RUNTIME_TEMPLATE = r'''\n<script id="lab14-i18n-runtime">\n(()=>{'use strict';\nconst CATALOGS=__CATALOGS__;\nconst META={r4SourceFreeze:'__R4__',r5LocalizationFreeze:'__R5__'};\nconst LOCALES=['en','zh','vi','es'];\nconst HTML_LANG={en:'en',zh:'zh-Hans',vi:'vi',es:'es'};\nconst PLACEHOLDER=/\\{([A-Za-z0-9_]+)\\}/g;\nlet active='en',mutating=false,observer=null;\nfunction escapeRe(value){return value.replace(/[.*+?^${}()|[\\]\\\\]/g,'\\\\$&')}\nfunction compile(template){\n  const names=[];let source='^',last=0,m;PLACEHOLDER.lastIndex=0;\n  while((m=PLACEHOLDER.exec(template))){source+=escapeRe(template.slice(last,m.index))+'([\\\\s\\\\S]+?)';names.push(m[1]);last=m.index+m[0].length}\n  source+=escapeRe(template.slice(last))+'$';\n  return{re:new RegExp(source),names,literal:template.replace(PLACEHOLDER,'').length};\n}\nconst exact=new Map(),patterns=[],staticPatterns=[];\nfor(const key of Object.keys(CATALOGS.en)){\n  for(const locale of LOCALES){\n    const value=String(CATALOGS[locale][key]),compiled=compile(value),entry={key,locale,value,...compiled};\n    if(compiled.names.length===0){exact.set(value,key);if(value.length>=2)staticPatterns.push(entry)}else patterns.push(entry);\n  }\n}\npatterns.sort((a,b)=>b.literal-a.literal||a.names.length-b.names.length);\nstaticPatterns.sort((a,b)=>b.value.length-a.value.length);\nfunction formatTarget(key,vars,target,depth){\n  const template=String(CATALOGS[target][key]);\n  return template.replace(PLACEHOLDER,(_,name)=>translateCore(Object.hasOwn(vars,name)?String(vars[name]):`{${name}}`,target,depth+1));\n}\nfunction directMatch(text,target,depth){\n  const exactKey=exact.get(text);if(exactKey!==undefined)return String(CATALOGS[target][exactKey]);\n  for(const p of patterns){const match=p.re.exec(text);if(!match)continue;const vars={};p.names.forEach((name,index)=>{vars[name]=match[index+1]});return formatTarget(p.key,vars,target,depth)}\n  return null;\n}\nfunction prefixedMatch(text,target,depth){\n  for(const p of staticPatterns){if(text===p.value||!text.startsWith(p.value))continue;const rest=text.slice(p.value.length);if(!/^[\\s:;,.!?→()\\-]/.test(rest))continue;return String(CATALOGS[target][p.key])+translateCore(rest,target,depth+1)}\n  return null;\n}\nfunction translateJsonValue(value,target){\n  if(typeof value==='string')return translateCore(value,target,0);\n  if(Array.isArray(value))return value.map(item=>translateJsonValue(item,target));\n  if(value&&typeof value==='object'){const out={};for(const [key,item] of Object.entries(value))out[key]=translateJsonValue(item,target);return out}\n  return value;\n}\nfunction translateJsonText(text,target){\n  const trimmed=text.trim();if(!trimmed||!['{','['].includes(trimmed[0]))return null;\n  try{return JSON.stringify(translateJsonValue(JSON.parse(trimmed),target))}catch(_){return null}\n}\nfunction translateCore(text,target,depth=0){\n  if(depth>6||!text)return text;\n  const direct=directMatch(text,target,depth);if(direct!==null)return direct;\n  const jsonText=translateJsonText(text,target);if(jsonText!==null)return jsonText;\n  if(text.startsWith('TEXT: '))return 'TEXT: '+translateCore(text.slice(6),target,depth+1);\n  if(text.includes('\\n'))return text.split('\\n').map(line=>translateCore(line,target,depth+1)).join('\\n');\n  const prefixed=prefixedMatch(text,target,depth);if(prefixed!==null)return prefixed;\n  return text;\n}\nfunction translateTextValue(value,target){const match=String(value).match(/^(\\s*)([\\s\\S]*?)(\\s*)$/);if(!match)return value;return match[1]+translateCore(match[2],target,0)+match[3]}\nfunction translateState(){\n  const node=document.querySelector('#stateText');if(!node)return;\n  try{const parsed=JSON.parse(node.textContent);node.textContent=JSON.stringify(translateJsonValue(parsed,active),null,2)}catch(_){/* state may be between renders */}\n}\nfunction shouldSkip(node){const parent=node.parentElement;if(!parent)return true;return !!parent.closest('script,style,#lab14-locale-bar,#stateText,[data-lab14-no-translate]')}\nfunction observe(){if(observer)observer.observe(document.body,{subtree:true,childList:true,characterData:true,attributes:false})}\nfunction translateTree(root=document.body){\n  if(mutating||!root)return;mutating=true;if(observer)observer.disconnect();\n  try{\n    const walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT),nodes=[];let node;while((node=walker.nextNode()))nodes.push(node);\n    for(const textNode of nodes){if(shouldSkip(textNode))continue;const next=translateTextValue(textNode.nodeValue,active);if(next!==textNode.nodeValue)textNode.nodeValue=next}\n    const elements=root.querySelectorAll?root.querySelectorAll('[title],[aria-label],[placeholder]'):[];\n    for(const element of elements){if(element.closest('#lab14-locale-bar,[data-lab14-no-translate]'))continue;for(const attr of ['title','aria-label','placeholder'])if(element.hasAttribute(attr)){const before=element.getAttribute(attr),after=translateTextValue(before,active);if(after!==before)element.setAttribute(attr,after)}}\n    translateState();\n    document.title=`${CATALOGS[active]['page.title']} — Lab 14`;\n  }finally{mutating=false;observe()}\n}\nfunction updateButtons(){for(const button of document.querySelectorAll('#lab14-locale-bar button[data-locale]'))button.setAttribute('aria-pressed',button.dataset.locale===active?'true':'false')}\nfunction setLocale(locale){if(!LOCALES.includes(locale))throw new Error(`Unsupported locale: ${locale}`);active=locale;document.documentElement.lang=HTML_LANG[locale];updateButtons();translateTree(document.body);window.dispatchEvent(new CustomEvent('lab14localechange',{detail:{locale}}))}\nfunction getLocale(){return active}\nfor(const button of document.querySelectorAll('#lab14-locale-bar button[data-locale]'))button.addEventListener('click',()=>setLocale(button.dataset.locale));\nobserver=new MutationObserver(records=>{\n  if(mutating)return;const roots=new Set();\n  for(const record of records){for(const node of record.addedNodes){if(node.nodeType===Node.ELEMENT_NODE)roots.add(node);else if(node.nodeType===Node.TEXT_NODE&&node.parentElement)roots.add(node.parentElement)}if(record.type==='characterData'&&record.target.parentElement)roots.add(record.target.parentElement)}\n  for(const root of roots)translateTree(root);\n});\nobserve();\nwindow.Lab14Localization={setLocale,getLocale,catalogs:CATALOGS,translate:translateCore,meta:META};\nconst requested=new URLSearchParams(location.search).get('lang');\nactive='en';document.documentElement.lang='en';updateButtons();document.title=`${CATALOGS.en['page.title']} — Lab 14`;\nif(LOCALES.includes(requested)&&requested!=='en')window.setTimeout(()=>setLocale(requested),0);\n})();\n</script>\n'''


def materialize_template(value: str) -> str:
    """Turn layout \n markers into newlines without touching intentional \\n JS escapes."""
    return re.sub(r"(?<!\\)\\n", "\n", value)


def load_catalogs() -> dict[str, dict[str, str]]:
    merged: dict[str, dict[str, str]] = {}
    for path in (PRIMARY, DYNAMIC):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("source_freeze_head") != R4_SOURCE_FREEZE:
            raise RuntimeError(f"{path.name} is not bound to the frozen R4 source")
        strings = payload.get("strings", {})
        for key, entry in strings.items():
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
    runtime_template = materialize_template(RUNTIME_TEMPLATE)
    runtime = runtime_template.replace("__CATALOGS__", payload).replace("__R4__", R4_SOURCE_FREEZE).replace("__R5__", R5_LOCALIZATION_FREEZE)
    css = materialize_template(CSS)
    bar = materialize_template(BAR)

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

    generated = source.replace("</style>", "</style>\n" + css, 1)
    generated = generated.replace("<main>", "<main>\n" + bar, 1)
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
