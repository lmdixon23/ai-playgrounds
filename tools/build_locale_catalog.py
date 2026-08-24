#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, re, shutil, sys, time
from datetime import datetime, timezone

ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'release-evidence'/'r4-locale-source-catalog.json'
SLUGS=['bayes-classifier','bayes-network','cnf-sat','convolution','hill-climbing','kmeans','knn-classifier','neural-network','overfitting','q-learning-gridworld','search-pathfinding','wumpus-world']
ASCII_WORD=re.compile(r'[A-Za-z]{2,}')
SKIP_EXACT={'EN','中文','English','简体中文','GitHub','ORCID'}

def launch(p):
    args=['--no-sandbox','--disable-dev-shm-usage']
    managed=pathlib.Path(p.chromium.executable_path)
    if managed.exists(): return p.chromium.launch(headless=True,args=args)
    for name in ('chromium','chromium-browser','google-chrome','chrome'):
        candidate=shutil.which(name)
        if candidate: return p.chromium.launch(headless=True,executable_path=candidate,args=args)
    return p.chromium.launch(headless=True,args=args)

def norm(s): return re.sub(r'\s+',' ',str(s or '')).strip()
def translatable(s):
    s=norm(s)
    if not s or s in SKIP_EXACT or len(s)>1200: return False
    if s.startswith(('http://','https://','data:')): return False
    if not ASCII_WORD.search(s): return False
    if re.fullmatch(r'[A-Za-z0-9_./:+×−–—↺↑←→<>=%()\[\],;|* ]+',s) and len(s)<24: return False
    return True

def main():
    from playwright.sync_api import sync_playwright
    catalog={}; page_meta={}; errors=[]
    with sync_playwright() as p:
        browser=launch(p)
        try:
            for slug in SLUGS:
                ctx=browser.new_context(viewport={'width':1280,'height':900})
                page=ctx.new_page(); page.set_default_timeout(8000)
                page_errors=[]; page.on('pageerror',lambda exc,arr=page_errors: arr.append(str(exc)))
                page.goto((ROOT/'playgrounds'/slug/'index.html').resolve().as_uri(),wait_until='domcontentloaded',timeout=12000)
                page.wait_for_timeout(700)
                try:
                    en=page.locator('button[data-lang="en"]')
                    if en.count(): en.first.click(); page.wait_for_timeout(250)
                except Exception: pass
                rows=page.evaluate('''() => {
                  const skipAncestor = n => {
                    const e=n.nodeType===1?n:n.parentElement;
                    if(!e)return true;
                    return !!e.closest('script,style,noscript,template,[data-essay-lang="zh"],[lang="zh"],.lang-switch');
                  };
                  const out=[];
                  const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
                  while(w.nextNode()){
                    const n=w.currentNode;if(skipAncestor(n))continue;
                    const t=(n.nodeValue||'').replace(/\\s+/g,' ').trim();
                    if(t)out.push({kind:'text',source:t});
                  }
                  document.querySelectorAll('[title],[aria-label],[placeholder]').forEach(el=>{
                    if(skipAncestor(el))return;
                    ['title','aria-label','placeholder'].forEach(a=>{const v=(el.getAttribute(a)||'').replace(/\\s+/g,' ').trim();if(v)out.push({kind:a,source:v})});
                  });
                  return out;
                }''')
                unique={}
                for row in rows:
                    s=norm(row.get('source'))
                    if translatable(s): unique.setdefault(s,set()).add(row.get('kind','text'))
                entries=[{'source':s,'kinds':sorted(kinds)} for s,kinds in sorted(unique.items(),key=lambda kv:(kv[0].lower(),kv[0]))]
                catalog[slug]=entries
                page_meta[slug]={
                    'title':norm(page.title()),
                    'description':norm(page.locator('meta[name="description"]').get_attribute('content') or ''),
                    'unique_sources':len(entries),
                    'page_errors':page_errors,
                }
                if page_errors: errors.append({slug:page_errors})
                ctx.close()
        finally: browser.close()
    shared=(ROOT/'assets/guided-challenges.js').read_text(encoding='utf-8-sig')
    shared_strings=[]
    # Conservative source extraction from quoted English strings in the shared challenge layer.
    for q in re.findall(r"'([^'\\]*(?:\\.[^'\\]*)*)'|\"([^\"\\]*(?:\\.[^\"\\]*)*)\"",shared):
        raw=q[0] or q[1]
        s=norm(raw.replace("\\'","'").replace('\\"','"'))
        if translatable(s): shared_strings.append(s)
    shared_strings=sorted(set(shared_strings),key=lambda s:(s.lower(),s))
    all_sources=sorted(set(shared_strings).union(*(set(e['source'] for e in entries) for entries in catalog.values())),key=lambda s:(s.lower(),s))
    payload={
        'harness':'tools/build_locale_catalog.py',
        'generated_utc':datetime.now(timezone.utc).isoformat(),
        'applets':len(SLUGS),
        'total_unique_sources':len(all_sources),
        'shared_guided_unique_sources':len(shared_strings),
        'page_meta':page_meta,
        'shared_guided_sources':shared_strings,
        'catalog':catalog,
        'page_errors':errors,
    }
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'harness':payload['harness'],'applets':payload['applets'],'total_unique_sources':payload['total_unique_sources'],'shared_guided_unique_sources':payload['shared_guided_unique_sources'],'page_errors':len(errors)},indent=2))
    return 0 if not errors else 1

if __name__=='__main__': raise SystemExit(main())
