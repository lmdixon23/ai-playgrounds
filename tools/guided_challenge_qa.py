#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, shutil, sys, time
from datetime import datetime, timezone

ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'release-evidence'/'guided-challenge-qa.json'
SLUGS=['bayes-classifier','bayes-network','cnf-sat','convolution','hill-climbing','kmeans','knn-classifier','neural-network','overfitting','q-learning-gridworld','search-pathfinding','wumpus-world']

def launch(p):
    args=['--no-sandbox','--disable-dev-shm-usage']
    managed=pathlib.Path(p.chromium.executable_path)
    if managed.exists(): return p.chromium.launch(headless=True,args=args)
    for name in ('chromium','chromium-browser','google-chrome','chrome'):
        c=shutil.which(name)
        if c:return p.chromium.launch(headless=True,executable_path=c,args=args)
    return p.chromium.launch(headless=True,args=args)

def state(page): return page.evaluate('() => window.__suiteGuidedChallenge?.state() || null')
def history(page): return page.evaluate('() => window.__suiteGuidedChallenge?.history() || []')
def has_r4(page): return bool(page.evaluate('() => !!window.__r4Localization && window.__r4Localization.ready()'))
def wait_state(page,want,timeout=5000): page.wait_for_function('(want)=>window.__suiteGuidedChallenge&&window.__suiteGuidedChallenge.state()===want',arg=want,timeout=timeout)

def switch_native_locale(page,code):
    btn=page.locator(f'button[data-lang="{code}"]')
    if not btn.count(): raise RuntimeError(f'native language control missing: {code}')
    btn.first.click()
    if code=='zh': page.wait_for_function("() => (document.documentElement.lang||'').toLowerCase().startsWith('zh')")
    else: page.wait_for_function("(code)=>(document.documentElement.lang||'').toLowerCase().startsWith(code)",arg=code)
    page.wait_for_timeout(100)

def fill_generic(page):
    fields=page.locator('[data-guided-field]')
    for i in range(fields.count()):
        el=fields.nth(i); tag=el.evaluate('(e)=>e.tagName'); typ=el.get_attribute('type') or ''
        if tag=='SELECT':
            vals=el.locator('option').evaluate_all('(opts)=>opts.map(o=>o.value).filter(Boolean)')
            if not vals: raise RuntimeError('guided select has no nonempty option')
            el.select_option(vals[0])
        elif typ=='number': el.fill('1')
        else: el.fill('prediction')

def check_generic(page,slug,checks):
    page.locator('[data-suite-mode="guided"]').click(); checks.append(('guided_mode_visible',not page.locator('.suite-guided-panel').is_hidden(),{}))
    contract=page.evaluate('() => window.__suiteGuidedChallenge.contract()')
    checks.append(('contract_exposes_scenario_mapping',isinstance(contract,dict) and 'scenario' in contract and 'transferScenario' in contract,{'contract':contract}))
    page.locator('.suite-guided-begin').click(); wait_state(page,'awaiting-prediction')
    checks.append(('reveal_disabled_before_lock',page.locator('.suite-guided-reveal').is_disabled(),{}))
    concealed=page.locator('[data-guided-concealed="1"]').count(); should=bool(contract.get('concealOnPrepare')) or not bool(contract.get('action'))
    checks.append(('concealment_timing_matches_challenge_type',concealed>=1 if should else concealed==0,{'concealed':concealed,'should_conceal_on_prepare':should,'contract':contract}))
    counts={sel:page.locator(sel).count() for sel in contract.get('mask',[])}
    checks.append(('configured_mask_selectors_exist',all(n>0 for n in counts.values()),{'selectors':counts}))
    fill_generic(page); wait_state(page,'prediction-complete-unlocked')
    checks.append(('lock_enabled_only_when_complete',not page.locator('.suite-guided-lock').is_disabled(),{}))
    values_before=page.locator('[data-guided-field]').evaluate_all('(els)=>els.map(e=>e.value)')
    page.locator('.suite-guided-lock').click(); wait_state(page,'locked')
    disabled=page.locator('[data-guided-field]').evaluate_all('(els)=>els.every(e=>e.disabled)')
    checks.append(('locked_prediction_immutable',bool(disabled),{'values':values_before}))
    checks.append(('reveal_enabled_after_lock',not page.locator('.suite-guided-reveal').is_disabled(),{}))
    if contract.get('action'):
        n=page.locator('[data-guided-concealed="1"]').count(); checks.append(('step_result_concealed_after_lock',n>=1,{'concealed':n}))
    if has_r4(page):
        checks.append(('language_switch_delegated_to_r4_qa',True,{'reason':'R4 runtime active'}))
    else:
        switch_native_locale(page,'zh')
        values_zh=page.locator('[data-guided-field]').evaluate_all('(els)=>els.map(e=>e.value)')
        checks.append(('language_switch_preserves_locked_prediction',values_zh==values_before and state(page)=='locked',{'before':values_before,'after':values_zh}))
        switch_native_locale(page,'en')
    page.locator('.suite-guided-reveal').click(); wait_state(page,'revealed')
    actual=page.locator('.suite-guided-actual').inner_text().strip()
    checks.append(('reveal_has_text_actual',bool(actual) and 'Inspect the revealed visual result.' not in actual,{'actual':actual[:500]}))
    if contract.get('action'): checks.append(('step_reveal_has_before_after_text','Before the hidden step' in actual and 'After the hidden step' in actual,{'actual':actual[:700]}))
    semantic=True
    if slug=='bayes-network': semantic='conditionally independent given Alarm' in actual
    elif slug=='kmeans': semantic='Point 1:' in actual and 'Centroid 1 at' in actual
    elif slug=='convolution': semantic='Σ =' in actual
    checks.append(('mechanism_specific_actual_text',semantic,{'slug':slug,'actual':actual[:700]}))
    checks.append(('result_unconcealed_after_reveal',page.locator('[data-guided-concealed="1"]').count()==0,{}))
    page.locator('.suite-guided-compare').click(); wait_state(page,'compared')
    checks.append(('compare_precedes_explanation',not page.locator('.suite-guided-explain-wrap').is_hidden(),{}))
    exp=page.locator('[data-guided-explanation]'); exp.fill('The mechanism differed because the ranking or update rule changed.')
    checks.append(('transfer_requires_explanation',not page.locator('.suite-guided-transfer').is_disabled(),{}))
    page.locator('.suite-guided-transfer').click(); wait_state(page,'awaiting-prediction')
    cleared=page.locator('[data-guided-field]').evaluate_all('(els)=>els.every(e=>e.value==="")')
    checks.append(('transfer_requires_new_prediction',bool(cleared),{}))
    transfer_concealed=page.locator('[data-guided-concealed="1"]').count(); transfer_should=bool(contract.get('concealOnPrepare')) or not bool(contract.get('action'))
    checks.append(('transfer_concealment_timing_matches_challenge_type',transfer_concealed>=1 if transfer_should else transfer_concealed==0,{'concealed':transfer_concealed,'should_conceal':transfer_should}))
    page.locator('.suite-guided-reset').click(); wait_state(page,'inactive')
    hist=history(page); checks.append(('reset_returns_inactive_and_records_reset',state(page)=='inactive' and 'reset' in hist,{'history':hist}))

def dispatch_knn_query_click(page,x_fraction=0.53,y_fraction=0.47):
    page.locator('#cv').evaluate('''(cv,pos)=>{const r=cv.getBoundingClientRect();cv.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true,view:window,clientX:r.left+r.width*pos.x,clientY:r.top+r.height*pos.y}));}''',{'x':x_fraction,'y':y_fraction})

def check_knn(page,checks):
    page.locator('[data-suite-mode="guided"]').click(); page.locator('#guidedStart').click(); wait_state(page,'awaiting-prediction')
    checks.append(('reveal_disabled_before_lock',page.locator('#guidedReveal').is_disabled(),{}))
    if not page.locator('#cv').bounding_box(): raise RuntimeError('KNN canvas has no bounding box')
    dispatch_knn_query_click(page); page.wait_for_timeout(100)
    k=int(page.locator('#k').input_value()); pts=page.locator('#cvOverlay circle[data-role="point"]')
    if pts.count()<k: raise RuntimeError(f'KNN overlay has {pts.count()} points but k={k}')
    for i in range(k): pts.nth(i).click(force=True)
    page.locator('[data-guided-class="A"]').click(); page.wait_for_timeout(80); wait_state(page,'prediction-complete-unlocked')
    checks.append(('knn_exact_neighbor_prediction_complete',not page.locator('#guidedLock').is_disabled(),{'k':k}))
    if has_r4(page):
        checks.append(('knn_language_switch_delegated_to_r4_qa',True,{'reason':'R4 runtime active; R3 certifies native EN/ZH locked prediction'}))
    else:
        switch_native_locale(page,'zh')
        checks.append(('language_switch_preserves_knn_prediction',state(page)=='prediction-complete-unlocked' and not page.locator('#guidedLock').is_disabled(),{}))
        checks.append(('knn_extension_translates_to_chinese',page.locator('.suite-guided-knn-compare').inner_text().strip()=='比较',{'label':page.locator('.suite-guided-knn-compare').inner_text().strip()}))
        switch_native_locale(page,'en')
        checks.append(('knn_extension_returns_to_english',page.locator('.suite-guided-knn-compare').inner_text().strip()=='Compare',{'label':page.locator('.suite-guided-knn-compare').inner_text().strip()}))
    page.locator('#guidedLock').click(); wait_state(page,'locked')
    checks.append(('knn_reveal_enabled_after_lock',not page.locator('#guidedReveal').is_disabled(),{}))
    page.locator('#guidedReveal').click(); wait_state(page,'revealed')
    result=page.locator('#guidedResult').inner_text().strip(); checks.append(('knn_reveal_compares_neighbors',bool(result) and '/' in result,{'result':result[:220]}))
    page.locator('.suite-guided-knn-compare').click(); wait_state(page,'compared')
    exp=page.locator('[data-knn-guided-explain]'); exp.fill('The distance rule changed which points ranked closest.')
    checks.append(('knn_transfer_requires_explanation',not page.locator('.suite-guided-knn-transfer').is_disabled(),{}))
    metric_before=page.locator('#metricSel').input_value(); page.locator('.suite-guided-knn-transfer').click(); wait_state(page,'awaiting-prediction'); metric_after=page.locator('#metricSel').input_value()
    checks.append(('knn_transfer_changes_closeness_rule',metric_before!=metric_after,{'before':metric_before,'after':metric_after}))
    page.locator('.suite-guided-reset').click(); wait_state(page,'inactive'); checks.append(('knn_reset_returns_inactive','reset' in history(page),{'history':history(page)}))

def main()->int:
    from playwright.sync_api import sync_playwright
    cases=[]; failures=[]
    with sync_playwright() as p:
        browser=launch(p)
        try:
            for slug in SLUGS:
                context=browser.new_context(viewport={'width':1280,'height':900}); page=context.new_page(); page.set_default_timeout(5000)
                page_errors=[];console_errors=[];page.on('pageerror',lambda exc,a=page_errors:a.append(str(exc)));page.on('console',lambda msg,a=console_errors:a.append(msg.text) if msg.type=='error' else None)
                checks=[];t0=time.perf_counter()
                try:
                    page.goto((ROOT/'playgrounds'/slug/'index.html').resolve().as_uri(),wait_until='domcontentloaded',timeout=10000); page.wait_for_function('() => !!window.__suiteGuidedChallenge',timeout=5000)
                    checks.append(('initial_explore_inactive',page.evaluate('() => window.__suiteGuidedChallenge.mode()==="explore" && window.__suiteGuidedChallenge.state()==="inactive"'),{}))
                    if slug=='knn-classifier': check_knn(page,checks)
                    else: check_generic(page,slug,checks)
                except Exception as exc: checks.append(('exception',False,{'error':str(exc)}))
                passed=all(bool(x[1]) for x in checks) and not page_errors
                rec={'slug':slug,'pass':passed,'checks':[{'name':n,'pass':bool(ok),'detail':d} for n,ok,d in checks],'page_errors':page_errors,'console_errors':console_errors,'elapsed_s':round(time.perf_counter()-t0,3)};cases.append(rec)
                if not passed: failures.append(slug)
                context.close()
        finally: browser.close()
    payload={'harness':'tools/guided_challenge_qa.py','timestamp_utc':datetime.now(timezone.utc).isoformat(),'total':len(cases),'passed':sum(x['pass'] for x in cases),'failed':sum(not x['pass'] for x in cases),'pass':not failures,'failed_slugs':failures,'cases':cases}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:payload[k] for k in ('harness','total','passed','failed','pass')},indent=2))
    for rec in cases:
        if not rec['pass']:
            print('FAIL '+rec['slug'],file=sys.stderr)
            for c in rec['checks']:
                if not c['pass']: print('  '+c['name']+': '+json.dumps(c['detail'],ensure_ascii=False),file=sys.stderr)
            for e in rec['page_errors']: print('  pageerror: '+e,file=sys.stderr)
    return 0 if not failures else 1
if __name__=='__main__': raise SystemExit(main())
