#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
SITE=ROOT/'_site'
REGISTRY=ROOT/'tools'/'quick_assigns_v2.json'
MODERN={'transformer-language-model','agent-tool-context','minimax-alpha-beta'}
INITIAL={'QA-SEARCH-01','QA-LOCAL-01','QA-WUMPUS-01','QA-SAT-01'}


def launch(playwright):
    args=['--no-sandbox','--disable-dev-shm-usage']
    managed=pathlib.Path(playwright.chromium.executable_path)
    if managed.exists(): return playwright.chromium.launch(headless=True,args=args)
    for name in ('chromium','chromium-browser','google-chrome','chrome'):
        candidate=shutil.which(name)
        if candidate: return playwright.chromium.launch(headless=True,executable_path=candidate,args=args)
    return playwright.chromium.launch(headless=True,args=args)


def main()->int:
    run=subprocess.run([sys.executable,str(ROOT/'tools'/'build_site_v1_7_final.py')],cwd=ROOT,text=True,capture_output=True)
    if run.returncode:
        print(run.stdout);print(run.stderr,file=sys.stderr);return run.returncode
    rows=json.loads(REGISTRY.read_text(encoding='utf-8'))['activities']
    checks=[]
    def check(name,ok,detail=None): checks.append((name,bool(ok),detail or {}))
    check('15 active registry rows',len(rows)==15 and all(r.get('status')=='active' and r.get('locales')==['en','zh','vi','es'] for r in rows),{'count':len(rows)})
    check('15 unique stable IDs',len({r['id'] for r in rows})==15)
    for r in rows:
        html=(SITE/'playgrounds'/r['slug']/'index.html').read_text(encoding='utf-8')
        check(f"{r['id']} surfaces once",html.count(f'data-quick-assign-id="{r["id"]}"')==1)
        check(f"{r['id']} anchor",f'id="{r["anchor"]}"' in html)
        check(f"{r['id']} inquiry fields",all((f'data-qa-answer="{k}"' if r['slug'] in MODERN else f'data-lab-answer="{k}"') in html for k in ('predict','observe','explain','transfer')))
    for page_name in ('teacher-pack.html','curriculum.html'):
        html=(SITE/page_name).read_text(encoding='utf-8')
        check(f'{page_name} lists 15 IDs',sum(1 for r in rows if r['id'] in html)==15)
        check(f'{page_name} has 15 canonical links',sum(1 for r in rows if f'playgrounds/{r["slug"]}/index.html?mode=classroom#{r["anchor"]}' in html)==15)

    page_errors=[];console_errors=[]
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser=launch(p)
        try:
            ctx=browser.new_context(viewport={'width':1280,'height':900},reduced_motion='reduce')
            page=ctx.new_page();page.on('pageerror',lambda exc:page_errors.append(str(exc)));page.on('console',lambda msg:console_errors.append(msg.text) if msg.type=='error' else None)
            # Verify the eleven newly activated assignments. The initial four keep
            # their already-frozen v1.6.1 gate in the same Verify workflow.
            for r in [x for x in rows if x['id'] not in INITIAL]:
                url=(SITE/'playgrounds'/r['slug']/'index.html').resolve().as_uri()+f'?mode=classroom&lang=en#{r["anchor"]}'
                page.goto(url,wait_until='load',timeout=20_000)
                qa=page.locator(f'[data-quick-assign-id="{r["id"]}"]')
                check(f"{r['id']} direct link resolves",qa.count()==1)
                check(f"{r['id']} in viewport document",qa.evaluate('el=>!!el&&el.isConnected'))
                if r['slug'] in MODERN:
                    check(f"{r['id']} direct link opens response surface",qa.evaluate('el=>el.open===true'))
                    title=qa.locator('.quick-assign-modern-body h2 .qa-i18n')
                    en=title.inner_text()
                    field=qa.locator('[data-qa-answer="predict"]');field.fill('keep-this-response')
                    for loc in ('zh','vi','es'):
                        page.select_option('#ap-standard-language-select',loc);page.wait_for_timeout(90)
                        check(f"{r['id']} title switches {loc}",title.inner_text()!=en,{'title':title.inner_text()})
                        check(f"{r['id']} response survives {loc}",field.input_value()=='keep-this-response')
                    page.select_option('#ap-standard-language-select','en');page.wait_for_timeout(90)
                    check(f"{r['id']} title restores EN",title.inner_text()==en)
                    check(f"{r['id']} response survives EN roundtrip",field.input_value()=='keep-this-response')
                else:
                    summary=qa.locator('summary').inner_text()
                    sel=page.locator('.r4-language-select');check(f"{r['id']} has four-language select",sel.count()==1)
                    for loc in ('vi','es'):
                        page.select_option('.r4-language-select',loc);page.wait_for_timeout(100)
                        check(f"{r['id']} packet summary switches {loc}",qa.locator('summary').inner_text()!=summary,{'summary':qa.locator('summary').inner_text()})
                        page.select_option('.r4-language-select','en');page.wait_for_timeout(100)
                        check(f"{r['id']} packet summary restores EN from {loc}",qa.locator('summary').inner_text()==summary)
            ctx.close()
            mobile=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,reduced_motion='reduce')
            mpage=mobile.new_page()
            for slug in sorted(MODERN):
                mpage.goto((SITE/'playgrounds'/slug/'index.html').resolve().as_uri()+'?lang=es',wait_until='load',timeout=20_000)
                layout=mpage.evaluate("""() => {
                  const width=innerWidth;
                  const scroll=Math.max(document.documentElement.scrollWidth,document.body.scrollWidth);
                  const offenders=[...document.querySelectorAll('body *')].map(el=>{
                    const r=el.getBoundingClientRect(),s=getComputedStyle(el);
                    return {tag:el.tagName,id:el.id||'',cls:typeof el.className==='string'?el.className.slice(0,120):'',left:Math.round(r.left),right:Math.round(r.right),w:Math.round(r.width),display:s.display,text:(el.textContent||'').trim().replace(/\\s+/g,' ').slice(0,100)};
                  }).filter(x=>x.display!=='none'&&(x.right>width+2||x.left<-2)).slice(0,12);
                  return {width,scroll,overflow:scroll-width,offenders};
                }""")
                check(f'{slug} Quick Assign 390px containment',layout['overflow']<=1,layout)
            mobile.close()
        finally: browser.close()
    failures=[{'name':n,'detail':d} for n,ok,d in checks if not ok]
    payload={'harness':'tools/test_v1_7_all_quick_assigns.py','checks':len(checks),'passed':len(checks)-len(failures),'failed':len(failures),'page_errors':page_errors,'console_errors':console_errors,'pass':not failures and not page_errors and not console_errors,'failures':failures}
    print(json.dumps(payload,indent=2,ensure_ascii=False));return 0 if payload['pass'] else 1

if __name__=='__main__':raise SystemExit(main())
