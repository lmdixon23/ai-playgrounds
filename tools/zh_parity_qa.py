#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, re, shutil, sys, time
from datetime import datetime, timezone

ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'release-evidence'/'zh-parity-browser-qa.json'
SLUGS=['bayes-classifier','bayes-network','cnf-sat','convolution','hill-climbing','kmeans','knn-classifier','neural-network','overfitting','q-learning-gridworld','search-pathfinding','wumpus-world']
CJK=re.compile(r'[\u3400-\u9fff]')

def launch(p):
    args=['--no-sandbox','--disable-dev-shm-usage']
    managed=pathlib.Path(p.chromium.executable_path)
    if managed.exists(): return p.chromium.launch(headless=True,args=args)
    for name in ('chromium','chromium-browser','google-chrome','chrome'):
        candidate=shutil.which(name)
        if candidate: return p.chromium.launch(headless=True,executable_path=candidate,args=args)
    return p.chromium.launch(headless=True,args=args)

def has_cjk(text): return bool(CJK.search(text or ''))
def mode_text(text): return (text or '').strip().rstrip(':：').strip()

def main():
    from playwright.sync_api import sync_playwright
    cases=[]; failures=[]
    with sync_playwright() as p:
        browser=launch(p)
        try:
            for slug in SLUGS:
                ctx=browser.new_context(viewport={'width':1280,'height':900})
                page=ctx.new_page(); page.set_default_timeout(7000)
                page_errors=[]; checks=[]; t0=time.perf_counter()
                page.on('pageerror',lambda exc,arr=page_errors: arr.append(str(exc)))
                try:
                    page.goto((ROOT/'playgrounds'/slug/'index.html').resolve().as_uri(),wait_until='domcontentloaded',timeout=12000)
                    page.wait_for_function('() => !!window.__suiteGuidedChallenge',timeout=7000)
                    zh=page.locator('button[data-lang="zh"]'); en=page.locator('button[data-lang="en"]')
                    if not zh.count() or not en.count(): raise RuntimeError('language-switch buttons missing')
                    zh.first.click()
                    page.wait_for_function("() => (document.documentElement.lang || '').toLowerCase().startsWith('zh')",timeout=7000)
                    page.wait_for_timeout(120)
                    h1=page.locator('h1').first.inner_text().strip()
                    checks.append(('zh_h1_visible',has_cjk(h1),{'h1':h1}))
                    mode_label=page.locator('.suite-guided-mode-label').inner_text().strip()
                    guided_label=page.locator('[data-suite-mode="guided"]').inner_text().strip()
                    explore_label=page.locator('[data-suite-mode="explore"]').inner_text().strip()
                    checks.append(('shared_mode_copy_zh',mode_text(mode_label)=='学习模式' and guided_label=='引导挑战' and explore_label=='自由探索',{'mode':mode_label,'guided':guided_label,'explore':explore_label}))
                    page.locator('[data-suite-mode="guided"]').click(); page.wait_for_timeout(100)
                    if slug=='knn-classifier':
                        start=page.locator('#guidedStart').inner_text().strip()
                        checks.append(('knn_native_guided_copy_zh',has_cjk(start) and start!='Start challenge',{'start':start}))
                    else:
                        title=page.locator('.suite-guided-title').inner_text().strip()
                        prompt=page.locator('.suite-guided-prompt').inner_text().strip()
                        checks.append(('guided_title_prompt_zh',has_cjk(title) and has_cjk(prompt),{'title':title,'prompt':prompt[:240]}))
                        forbidden=['Prepare challenge','Lock prediction','Reveal mechanism','Try changed case']
                        panel=page.locator('.suite-guided-panel').inner_text()
                        checks.append(('no_guided_english_fallback_in_zh',not any(x in panel for x in forbidden),{'found':[x for x in forbidden if x in panel]}))
                    en.first.click()
                    page.wait_for_function("() => (document.documentElement.lang || '').toLowerCase().startsWith('en')",timeout=7000)
                    page.wait_for_timeout(100)
                    english_mode=page.locator('.suite-guided-mode-label').inner_text().strip()
                    checks.append(('returns_to_english',mode_text(english_mode)=='Learning mode',{'mode':english_mode}))
                except Exception as exc:
                    checks.append(('exception',False,{'error':str(exc)}))
                passed=all(bool(x[1]) for x in checks) and not page_errors
                record={'slug':slug,'pass':passed,'checks':[{'name':n,'pass':bool(ok),'detail':detail} for n,ok,detail in checks],'page_errors':page_errors,'elapsed_s':round(time.perf_counter()-t0,3)}
                cases.append(record)
                if not passed: failures.append(slug)
                ctx.close()
        finally:
            browser.close()
    payload={'harness':'tools/zh_parity_qa.py','timestamp_utc':datetime.now(timezone.utc).isoformat(),'total':len(cases),'passed':sum(x['pass'] for x in cases),'failed':sum(not x['pass'] for x in cases),'pass':not failures,'failed_slugs':failures,'cases':cases}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:payload[k] for k in ('harness','total','passed','failed','pass')},indent=2))
    for rec in cases:
        if not rec['pass']:
            print('FAIL '+rec['slug'],file=sys.stderr)
            for c in rec['checks']:
                if not c['pass']: print('  '+c['name']+': '+json.dumps(c['detail'],ensure_ascii=False),file=sys.stderr)
            for e in rec['page_errors']: print('  pageerror: '+e,file=sys.stderr)
    return 0 if not failures else 1

if __name__=='__main__': raise SystemExit(main())
