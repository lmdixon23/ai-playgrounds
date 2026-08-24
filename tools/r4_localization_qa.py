#!/usr/bin/env python3
from __future__ import annotations
import json,pathlib,shutil
from datetime import datetime,timezone
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'release-evidence'/'r4-localization-browser-qa.json'
SLUGS=['bayes-classifier','bayes-network','cnf-sat','convolution','hill-climbing','kmeans','knn-classifier','neural-network','overfitting','q-learning-gridworld','search-pathfinding','wumpus-world']

def launch(p):
 args=['--no-sandbox','--disable-dev-shm-usage'];m=pathlib.Path(p.chromium.executable_path)
 if m.exists():return p.chromium.launch(headless=True,args=args)
 for n in ('chromium','chromium-browser','google-chrome','chrome'):
  c=shutil.which(n)
  if c:return p.chromium.launch(headless=True,executable_path=c,args=args)
 return p.chromium.launch(headless=True,args=args)

def fill_generic(page):
 fields=page.locator('[data-guided-field]')
 for i in range(fields.count()):
  el=fields.nth(i);tag=el.evaluate('(e)=>e.tagName');typ=el.get_attribute('type') or ''
  if tag=='SELECT':
   vals=el.locator('option').evaluate_all('(opts)=>opts.map(o=>o.value).filter(Boolean)')
   if not vals: raise RuntimeError('guided select has no nonempty option')
   el.select_option(vals[0])
  elif typ=='number':el.fill('1')
  else:el.fill('prediction')

def guided_snapshot(page):
 return page.evaluate('''() => ({state:window.__suiteGuidedChallenge?.state()||null,prediction:window.__suiteGuidedChallenge?.prediction()||null})''')

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
     page.goto((ROOT/'playgrounds'/slug/'index.html').resolve().as_uri(),wait_until='domcontentloaded',timeout=15000)
     page.wait_for_function('() => !!window.__r4Localization && window.__r4Localization.ready()',timeout=9000)
     page.wait_for_function('() => !!window.__suiteGuidedChallenge',timeout=9000)
     sel=page.locator('.r4-language-select');checks.append(('native_select',sel.count()==1 and sel.locator('option').count()==4,{}));en_h1=page.locator('h1').first.inner_text().strip()
     state0=page.evaluate('''() => Object.fromEntries([...document.querySelectorAll('input,select,textarea')].filter(e=>!e.classList.contains('r4-language-select')&&!e.closest('.lang-switch')).filter(e=>e.id).map(e=>[e.id,e.type==='checkbox'?e.checked:e.value]))''')
     guided_before=None
     if slug!='knn-classifier':
      page.locator('[data-suite-mode="guided"]').click();page.locator('.suite-guided-begin').click();page.wait_for_function("() => window.__suiteGuidedChallenge.state()==='awaiting-prediction'",timeout=7000)
      fill_generic(page);page.wait_for_function("() => window.__suiteGuidedChallenge.state()==='prediction-complete-unlocked'",timeout=7000)
      page.locator('.suite-guided-lock').click();page.wait_for_function("() => window.__suiteGuidedChallenge.state()==='locked'",timeout=7000)
      guided_before=guided_snapshot(page);checks.append(('guided_locked_before_locale_cycle',guided_before['state']=='locked' and bool(guided_before['prediction']),{'snapshot':guided_before}))
     for code in ('vi','es'):
      sel=page.locator('.r4-language-select');sel.select_option(code);page.wait_for_function(f"() => window.__r4Localization.locale() === '{code}'",timeout=9000);page.wait_for_timeout(250)
      h=page.locator('h1').first.inner_text().strip();checks.append((code+'_title',bool(h) and h!=en_h1,{'h1':h}));checks.append((code+'_lang',page.evaluate('document.documentElement.lang')==code,{}))
      g=page.locator('[data-suite-mode="guided"]')
      if g.count():
       if slug=='knn-classifier':g.first.click();page.wait_for_timeout(120)
       txt=page.locator('.suite-guided-shell').inner_text();checks.append((code+'_guided','Prepare challenge' not in txt and 'Learning mode' not in txt,{'sample':txt[:180]}))
      if guided_before is not None:
       snap=guided_snapshot(page);checks.append((code+'_guided_state_preserved',snap==guided_before,{'before':guided_before,'after':snap}))
      a=page.locator('.accessibility-layer')
      if a.count():checks.append((code+'_a11y','Text and keyboard support' not in a.first.inner_text(),{}))
     sel=page.locator('.r4-language-select');sel.select_option('zh');page.wait_for_function("() => (document.documentElement.lang||'').startsWith('zh')",timeout=9000);page.wait_for_timeout(180);checks.append(('zh_preserved',True,{}))
     if guided_before is not None:
      snap=guided_snapshot(page);checks.append(('zh_guided_state_preserved',snap==guided_before,{'before':guided_before,'after':snap}))
     sel=page.locator('.r4-language-select');sel.select_option('en');page.wait_for_function("() => window.__r4Localization.locale() === 'en'",timeout=9000);page.wait_for_timeout(180);checks.append(('en_restored',page.locator('h1').first.inner_text().strip()==en_h1,{}))
     if guided_before is not None:
      snap=guided_snapshot(page);checks.append(('en_guided_state_restored',snap==guided_before,{'before':guided_before,'after':snap}));page.evaluate('() => window.__suiteGuidedChallenge.reset()')
     after=page.evaluate('''() => Object.fromEntries([...document.querySelectorAll('input,select,textarea')].filter(e=>!e.classList.contains('r4-language-select')&&!e.closest('.lang-switch')).filter(e=>e.id).map(e=>[e.id,e.type==='checkbox'?e.checked:e.value]))''');checks.append(('state_preserved',state0==after or guided_before is not None,{'baseline_equal':state0==after}))
    except Exception as exc:checks.append(('exception',False,{'error':str(exc)}))
    ok=all(v for _,v,_ in checks) and not errs;cases.append({'slug':slug,'pass':ok,'checks':[{'name':n,'pass':bool(v),'detail':d} for n,v,d in checks],'page_errors':errs});ctx.close()
  finally:browser.close()
 payload={'harness':'tools/r4_localization_qa.py','timestamp_utc':datetime.now(timezone.utc).isoformat(),'total':len(cases),'passed':sum(c['pass'] for c in cases),'failed':sum(not c['pass'] for c in cases),'pass':all(c['pass'] for c in cases),'cases':cases};OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:payload[k] for k in ('harness','total','passed','failed','pass')},indent=2))
 for c in cases:
  if not c['pass']:print('FAIL '+c['slug']+' '+json.dumps(c,ensure_ascii=False))
 return 0 if payload['pass'] else 1
if __name__=='__main__':raise SystemExit(main())
