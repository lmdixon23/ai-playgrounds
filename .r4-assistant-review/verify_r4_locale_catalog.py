#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, pathlib, re, shutil, subprocess

ROOT=pathlib.Path(__file__).resolve().parents[1]
ASCII_WORD=re.compile(r'[A-Za-z]{2,}')
SKIP_EXACT={'EN','中文','English','简体中文','Tiếng Việt','Español','GitHub','ORCID'}
# Dynamic numeric observations are applet state, not stable localization keys.
# In Overfitting these values are regenerated from the current random sample, so
# exact-string catalogs would necessarily fail whenever the sample changes.
DYNAMIC_DATA=(
    re.compile(r'^\(\s*[+\-−]?(?:\d+(?:\.\d+)?|\.\d+)\s*,\s*[+\-−]?(?:\d+(?:\.\d+)?|\.\d+)\s*\)\s+residual\s*=\s*[+\-−]?(?:\d+(?:\.\d+)?|\.\d+)$', re.I),
)
# Short invariant technical labels may legitimately stay identical across locales.
INVARIANT_TECH={
    'A*','BFS','DFS','Dijkstra','DPLL','CNF','SAT','UNSAT','ReLU','Adam','SGD',
    'Q-learning','SARSA','Expected SARSA','Gibbs','EM','GMM','KNN','k-means','k-means++',
    'D-separation','Bayes','Manhattan','Chebyshev','Euclidean','MSE','L1','L2','Ridge',
    'Sobel-X','Sobel-Y','XOR','AND','OR','NOT','TD','CPT','DAG','LMS','URL','JSON','PNG',
}

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
    if any(pattern.fullmatch(s) for pattern in DYNAMIC_DATA): return False
    if not ASCII_WORD.search(s): return False
    if re.fullmatch(r'[A-Za-z0-9_./:+×−–—↺↑←→<>=%()\[\],;|* ]+',s) and len(s)<24: return False
    return True

def identity_allowed(s):
    s=norm(s)
    if s in INVARIANT_TECH: return True
    # Equations, selector-like tokens, and compact labels composed only of known
    # technical names/numbers/symbols may remain language-invariant.
    if len(s) <= 36:
        cleaned=re.sub(r'[^A-Za-z*+\-0-9]+',' ',s).strip()
        tokens={t for t in cleaned.split() if t}
        if tokens and all(t in INVARIANT_TECH or t.isdigit() or re.fullmatch(r'[A-Z0-9]+',t) for t in tokens):
            return True
    return False

def collect_sources(slug):
    from playwright.sync_api import sync_playwright
    page_path=ROOT/'playgrounds'/slug/'index.html'
    with sync_playwright() as p:
        browser=launch(p)
        try:
            ctx=browser.new_context(viewport={'width':1280,'height':900})
            page=ctx.new_page(); page.set_default_timeout(8000)
            errors=[]; page.on('pageerror',lambda exc: errors.append(str(exc)))
            page.goto(page_path.resolve().as_uri(),wait_until='domcontentloaded',timeout=12000)
            page.wait_for_timeout(700)
            if page.evaluate("() => !!window.__r4Localization && window.__r4Localization.ready()"):
                page.evaluate("() => window.__r4Localization.setLocale('en', {immediate:true})")
                page.wait_for_timeout(250)
            else:
                en=page.locator('button[data-lang=\"en\"]')
                if en.count(): en.first.click(); page.wait_for_timeout(250)
            rows=page.evaluate('''() => {
              const skip=n=>{const e=n.nodeType===1?n:n.parentElement;if(!e)return true;return !!e.closest('script,style,noscript,template,[data-essay-lang="zh"],[lang="zh"],.lang-switch')};
              const out=[]; const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
              while(w.nextNode()){const n=w.currentNode;if(skip(n))continue;const t=(n.nodeValue||'').replace(/\\s+/g,' ').trim();if(t)out.push(t)}
              document.querySelectorAll('[title],[aria-label],[placeholder]').forEach(el=>{if(skip(el))return;['title','aria-label','placeholder'].forEach(a=>{const v=(el.getAttribute(a)||'').replace(/\\s+/g,' ').trim();if(v)out.push(v)})});
              return out;
            }''')
            title=norm(page.title())
            description=norm(page.locator('meta[name="description"]').get_attribute('content') or '')
            ctx.close()
        finally: browser.close()
    if errors: raise RuntimeError(f'{slug}: page errors: {errors}')
    return {norm(x) for x in rows if translatable(norm(x))}, title, description

def pattern_covers(source, rows):
    for row in rows or []:
        flags=0
        if 'i' in str(row.get('flags','')): flags |= re.I
        try:
            if re.search(str(row.get('source','')), source, flags): return True
        except re.error:
            continue
    return False

def load_locale(slug):
    common_path=ROOT/'assets'/'locales'/'common-r4.js'
    path=ROOT/'assets'/'locales'/f'{slug}-r4.js'
    if not common_path.is_file(): raise RuntimeError(f'missing shared locale file: {common_path}')
    if not path.is_file(): raise RuntimeError(f'missing locale file: {path}')
    js=f'''global.window={{}};\nrequire({json.dumps(str(common_path))});\nrequire({json.dumps(str(path))});\nconst root=window.__AI_PLAYGROUNDS_R4_LOCALES||{{}};\nconst d=root[{json.dumps(slug)}];\nprocess.stdout.write(JSON.stringify({{data:d,common:root.common||{{}}}}));\n'''
    proc=subprocess.run(['node','-e',js],capture_output=True,text=True,encoding='utf-8',errors='replace')
    if proc.returncode: raise RuntimeError(proc.stderr)
    return json.loads(proc.stdout)

def assert_runtime_common():
    runtime=(ROOT/'assets'/'localization-r4.js').read_text(encoding='utf-8-sig')
    # Runtime semantics: applet-local generated strings are the draft; reviewed
    # shared terms are the final override layer. The order is therefore material.
    if 'return Object.assign({}, local, common);' not in runtime:
        raise RuntimeError('R4 runtime no longer gives reviewed common strings precedence over local machine drafts')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--slug',required=True);args=ap.parse_args();slug=args.slug
    sources,title,description=collect_sources(slug); bundle=load_locale(slug); data=bundle.get('data') or {}; common=bundle.get('common') or {}
    assert_runtime_common()
    failures=[]
    if data.get('ready') is not True: failures.append('ready flag is not true')
    for locale in ('vi','es'):
        local=((data.get(locale) or {}).get('strings') or {})
        # Match browser runtime precedence exactly: common reviewed translations win.
        strings=dict(local); strings.update(common.get(locale) or {})
        patterns=(data.get(locale) or {}).get('patterns') or []
        missing=sorted(source for source in sources if source not in strings and not pattern_covers(source,patterns))
        identical=sorted(source for source in sources if source in strings and norm(strings[source])==source and not identity_allowed(source))
        extras=sorted(set(strings)-sources)
        if missing: failures.append(f'{locale}: {len(missing)} missing source translations; first={missing[:12]}')
        if identical: failures.append(f'{locale}: {len(identical)} untranslated English prose strings; first={identical[:12]}')
        meta=(data.get('meta') or {}).get(locale) or {}
        if not meta.get('title') or not meta.get('description'): failures.append(f'{locale}: metadata title/description missing')
        print(json.dumps({'slug':slug,'locale':locale,'rendered_sources':len(sources),'translated_sources':len(strings),'shared_reviewed_sources':len(common.get(locale) or {}),'missing':len(missing),'identical_prose':len(identical),'extras':len(extras),'first_missing':missing[:20],'first_identical_prose':identical[:20]},ensure_ascii=False,indent=2))
    enmeta=(data.get('meta') or {}).get('en') or {}
    if enmeta.get('title')!=title: failures.append(f'English metadata title mismatch: {enmeta.get("title")!r} != {title!r}')
    if enmeta.get('description')!=description: failures.append('English metadata description mismatch')
    for f in failures: print('FAIL: '+f)
    return 0 if not failures else 1

if __name__=='__main__': raise SystemExit(main())
