#!/usr/bin/env python3
from __future__ import annotations

import http.server
import json
import pathlib
import shutil
import socketserver
import subprocess
import sys
import threading
from contextlib import contextmanager

ROOT=pathlib.Path(__file__).resolve().parents[1]
SITE=ROOT/'_site'
EVIDENCE=ROOT/'release-evidence'/'v1.7.1-modern-packet-label-qa.json'
MODERN=('transformer-language-model','agent-tool-context','minimax-alpha-beta')
SOURCE_IDS={'transformer-language-model':'stateText','agent-tool-context':'stateText','minimax-alpha-beta':'textState'}
EXPECTED={
'en':{'predict':'Predict','observe':'Observe','explain':'Explain','transfer':'Transfer','refresh':'Refresh state','copy':'Copy packet','print':'Print packet','clear':'Clear local draft'},
'vi':{'predict':'Dự đoán','observe':'Quan sát','explain':'Giải thích','transfer':'Chuyển giao','refresh':'Làm mới trạng thái','copy':'Sao chép gói bài','print':'In gói bài','clear':'Xóa bản nháp cục bộ'},
'es':{'predict':'Predecir','observe':'Observar','explain':'Explicar','transfer':'Transferir','refresh':'Actualizar estado','copy':'Copiar paquete','print':'Imprimir paquete','clear':'Borrar borrador local'},
}


def launch(playwright):
    args=['--no-sandbox','--disable-dev-shm-usage']
    managed=pathlib.Path(playwright.chromium.executable_path)
    if managed.exists():return playwright.chromium.launch(headless=True,args=args)
    for name in ('chromium','chromium-browser','google-chrome','chrome'):
        candidate=shutil.which(name)
        if candidate:return playwright.chromium.launch(headless=True,executable_path=candidate,args=args)
    return playwright.chromium.launch(headless=True,args=args)


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self,_format:str,*args)->None:return


@contextmanager
def local_site_server():
    handler=lambda *args,**kwargs:QuietHandler(*args,directory=str(SITE),**kwargs)
    with socketserver.ThreadingTCPServer(('127.0.0.1',0),handler) as server:
        server.daemon_threads=True
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:yield f'http://127.0.0.1:{server.server_address[1]}'
        finally:server.shutdown();thread.join(timeout=2)


def write_payload(payload:dict)->None:
    EVIDENCE.parent.mkdir(parents=True,exist_ok=True);EVIDENCE.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')


def main()->int:
    build=subprocess.run([sys.executable,str(ROOT/'tools'/'build_site_v1_7_1_modern_parity_stable.py')],cwd=ROOT,text=True,capture_output=True,check=False,timeout=45)
    if build.returncode:
        payload={'harness':'tools/test_v1_7_1_modern_packet_labels.py','stage':'build','pass':False,'stdout':build.stdout[-12000:],'stderr':build.stderr[-12000:]};write_payload(payload);print(json.dumps(payload,indent=2,ensure_ascii=False));return build.returncode

    checks=[]
    def check(name,ok,detail=None):checks.append((name,bool(ok),detail))
    for slug in MODERN:
        html=(SITE/'playgrounds'/slug/'index.html').read_text(encoding='utf-8')
        check(f'{slug}: stable lifecycle marker','data-v171-stable-lifecycle="true"' in html)
        check(f'{slug}: no readiness polling','readinessTimer' not in html and 'readinessTries' not in html and '__v171LabelWrapped' not in html)
        check(f'{slug}: structured accessibility panel','class="accessibility-layer ap-modern-a11y-parity" open' in html and 'id="ap-modern-a11y-state"' in html)
        check(f'{slug}: exact state source binding',f'const SOURCE_ID={json.dumps(SOURCE_IDS[slug])}' in html)
        for locale in ('en','vi','es'):
            for value in EXPECTED[locale].values():check(f'{slug}: static {locale} label catalog contains {value}',value in html)

    page_errors=[];console_errors=[];diagnostics=[]
    from playwright.sync_api import sync_playwright
    with local_site_server() as origin,sync_playwright() as p:
        browser=launch(p)
        try:
            for slug in MODERN:
                context=browser.new_context(viewport={'width':390,'height':844},reduced_motion='reduce');context.set_default_timeout(8000)
                page=context.new_page();local_page_errors=[];local_console_errors=[];stage='navigate'
                page.on('pageerror',lambda exc,a=local_page_errors:a.append(str(exc)));page.on('console',lambda msg,a=local_console_errors:a.append(msg.text) if msg.type=='error' else None)
                try:
                    response=page.goto(f'{origin}/playgrounds/{slug}/index.html?lang=en',wait_until='domcontentloaded',timeout=20000);check(f'{slug}: local artifact HTTP 200',response is not None and response.status==200,None if response is None else response.status)
                    stage='attach';page.wait_for_selector('#ap-standard-language-select',state='attached');page.wait_for_selector('#ap-modern-a11y',state='attached');page.wait_for_selector('details[data-quick-assign-id]',state='attached');page.wait_for_selector('#ap-modern-a11y-state',state='attached')
                    page.wait_for_timeout(300)
                    a11y=page.locator('#ap-modern-a11y');qa=page.locator('details[data-quick-assign-id]');qa.evaluate('el=>el.open=true')
                    check(f'{slug}: accessibility open by default',a11y.get_attribute('open') is not None)
                    check(f'{slug}: keyboard card',a11y.locator('#ap-modern-a11y-keyboard-title').count()==1)
                    check(f'{slug}: reduced-motion card',a11y.locator('#ap-modern-a11y-motion-title').count()==1)
                    stage='state';page.wait_for_function("sid=>{const s=document.getElementById(sid);return !!s&&!!String(s.value||s.textContent||'').trim()}",arg=SOURCE_IDS[slug],timeout=6000)
                    source_text=page.evaluate("sid=>{const s=document.getElementById(sid);return String(s?.value||s?.textContent||'').trim()}",SOURCE_IDS[slug]);mirror=(a11y.locator('#ap-modern-a11y-state').text_content() or '').strip()
                    check(f'{slug}: mirrored accessibility state is populated',bool(mirror),mirror[:160]);check(f'{slug}: mirrored state matches existing mechanism state',mirror==source_text,{'source':source_text[:180],'mirror':mirror[:180]})
                    for key in ('predict','observe','explain','transfer'):check(f'{slug}: EN {key} aria',qa.locator(f'[data-qa-answer="{key}"]').get_attribute('aria-label')==EXPECTED['en'][key])
                    for action,key in (('refresh-state','refresh'),('copy','copy'),('print','print'),('clear','clear')):check(f'{slug}: EN {action} aria',qa.locator(f'[data-qa-action="{action}"]').get_attribute('aria-label')==EXPECTED['en'][key])
                    for locale in ('vi','es'):
                        stage=f'locale-{locale}';page.select_option('#ap-standard-language-select',locale);page.wait_for_function("loc=>document.documentElement.lang.toLowerCase().startsWith(loc)",arg=locale,timeout=8000);page.wait_for_timeout(240)
                        check(f'{slug}: accessibility summary localizes {locale}',a11y.locator('summary').inner_text().strip()!='♿ Text and keyboard support')
                        for key in ('predict','observe','explain','transfer'):check(f'{slug}: {locale} {key} aria',qa.locator(f'[data-qa-answer="{key}"]').get_attribute('aria-label')==EXPECTED[locale][key])
                        for action,key in (('refresh-state','refresh'),('copy','copy'),('print','print'),('clear','clear')):check(f'{slug}: {locale} {action} aria',qa.locator(f'[data-qa-action="{action}"]').get_attribute('aria-label')==EXPECTED[locale][key])
                        page.select_option('#ap-standard-language-select','en');page.wait_for_function("()=>document.documentElement.lang.toLowerCase().startsWith('en')",timeout=8000);page.wait_for_timeout(240);check(f'{slug}: accessibility summary restores EN from {locale}',a11y.locator('summary').inner_text().strip()=='♿ Text and keyboard support')
                    stage='refresh';qa.locator('[data-qa-action="refresh-state"]').click();page.wait_for_timeout(50);check(f'{slug}: packet state remains populated',bool(qa.locator('[data-qa-modern-state]').inner_text().strip()))
                except Exception as exc:
                    snap={'slug':slug,'stage':stage,'error':str(exc),'page_errors':local_page_errors,'console_errors':local_console_errors}
                    try:snap['dom']=page.evaluate("sid=>({lang:document.documentElement.lang,qa:!!document.querySelector('details[data-quick-assign-id]'),a11y:!!document.querySelector('#ap-modern-a11y'),source:document.getElementById(sid)?.value||document.getElementById(sid)?.textContent||null,mirror:document.querySelector('#ap-modern-a11y-state')?.textContent||null})",SOURCE_IDS[slug])
                    except Exception as inner:snap['dom_error']=str(inner)
                    diagnostics.append(snap);check(f'{slug}: exception at {stage}',False,snap)
                page_errors.extend(local_page_errors);console_errors.extend(local_console_errors);context.close()
        finally:browser.close()
    failures=[{'name':n,'detail':d} for n,ok,d in checks if not ok]
    payload={'harness':'tools/test_v1_7_1_modern_packet_labels.py','checks':len(checks),'passed':len(checks)-len(failures),'failed':len(failures),'page_errors':page_errors,'console_errors':console_errors,'diagnostics':diagnostics,'pass':not failures and not page_errors and not console_errors,'failures':failures};write_payload(payload);print(json.dumps(payload,indent=2,ensure_ascii=False));return 0 if payload['pass'] else 1


if __name__=='__main__':raise SystemExit(main())
