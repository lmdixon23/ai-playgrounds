#!/usr/bin/env python3
from __future__ import annotations
import json,pathlib,shutil
from datetime import datetime,timezone
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'release-evidence'/'r4-localization-browser-qa.json'
SLUGS='''+repr(SLUGS)+'''
def launch(p):
 args=['--no-sandbox','--disable-dev-shm-usage'];m=pathlib.Path(p.chromium.executable_path)
 if m.exists():return p.chromium.launch(headless=True,args=args)
 for n in ('chromium','chromium-browser','google-chrome','chrome'):
  c=shutil.which(n)
  if c:return p.chromium.launch(headless=True,executable_path=c,args=args)
 return p.chromium.launch(headless=True,args=args)
def main():
 from playwright.sync_api import sync_playwright
 cases=[]
 with sync_playwright() as p:
  browser=launch(p)
  try:
   for slug in SLUGS:
    ctx=browser.new_context(viewport={'width':1280,'height':900});page=ctx.new_page();page.set_default_timeout(9000);errs=[];checks=[]
    page.on('pageerror',lambda exc,a=errs:a.append(str(exc)))
    try:
     page.goto((ROOT/'playgrounds'/slug/'index.html').resolve().as_uri(),wait_until='domcontentloaded',timeout=15000);page.wait_for_function('() => !!window.__r4Localization && window.__r4Localization.ready()',timeout=9000)
     sel=page.locator('.r4-language-select');checks.append(('native_select',sel.count()==1 and sel.locator('option').count()==4,{}));en_h1=page.locator('h1').first.inner_text().strip()
     state=page.evaluate('''() => Object.fromEntries([...document.querySelectorAll('input,select,textarea')].filter(e=>!e.classList.contains('r4-language-select')&&!e.closest('.lang-switch')).filter(e=>e.id).map(e=>[e.id,e.type==='checkbox'?e.checked:e.value]))''')
     for code in ('vi','es'):
      sel.select_option(code);page.wait_for_function(f"() => window.__r4Localization.locale() === '{code}'",timeout=9000);page.wait_for_timeout(250);h=page.locator('h1').first.inner_text().strip();checks.append((code+'_title',bool(h) and h!=en_h1,{'h1':h}));checks.append((code+'_lang',page.evaluate('document.documentElement.lang')==code,{}));
      g=page.locator('[data-suite-mode="guided"]');
      if g.count(): g.first.click();page.wait_for_timeout(120);txt=page.locator('.suite-guided-shell').inner_text();checks.append((code+'_guided','Prepare challenge' not in txt and 'Learning mode' not in txt,{'sample':txt[:180]}))
      a=page.locator('.accessibility-layer');
      if a.count():checks.append((code+'_a11y','Text and keyboard support' not in a.first.inner_text(),{}))
     sel.select_option('zh');page.wait_for_timeout(180);checks.append(('zh_preserved',page.evaluate("(document.documentElement.lang||'').startsWith('zh')"),{}));sel=page.locator('.r4-language-select');sel.select_option('en');page.wait_for_timeout(180);checks.append(('en_restored',page.locator('h1').first.inner_text().strip()==en_h1,{}));after=page.evaluate('''() => Object.fromEntries([...document.querySelectorAll('input,select,textarea')].filter(e=>!e.classList.contains('r4-language-select')&&!e.closest('.lang-switch')).filter(e=>e.id).map(e=>[e.id,e.type==='checkbox'?e.checked:e.value]))''');checks.append(('state_preserved',state==after,{}))
    except Exception as exc:checks.append(('exception',False,{'error':str(exc)}))
    ok=all(v for _,v,_ in checks) and not errs;cases.append({'slug':slug,'pass':ok,'checks':[{'name':n,'pass':bool(v),'detail':d} for n,v,d in checks],'page_errors':errs});ctx.close()
  finally:browser.close()
 payload={'harness':'tools/r4_localization_qa.py','timestamp_utc':datetime.now(timezone.utc).isoformat(),'total':len(cases),'passed':sum(c['pass'] for c in cases),'failed':sum(not c['pass'] for c in cases),'pass':all(c['pass'] for c in cases),'cases':cases};OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:payload[k] for k in ('harness','total','passed','failed','pass')},indent=2));
 for c in cases:
  if not c['pass']:print('FAIL '+c['slug']+' '+json.dumps(c,ensure_ascii=False))
 return 0 if payload['pass'] else 1
if __name__=='__main__':raise SystemExit(main())
