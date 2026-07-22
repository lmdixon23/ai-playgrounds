#!/usr/bin/env python3
from __future__ import annotations
import argparse, datetime as dt, json, re, subprocess, tempfile
from dataclasses import dataclass, asdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PLAYGROUNDS=ROOT/'playgrounds'
EXPECTED={
'bayes-classifier','bayes-network','cnf-sat','convolution','hill-climbing','kmeans',
'knn-classifier','neural-network','overfitting','q-learning-gridworld','search-pathfinding','wumpus-world'}
PUBLIC_PAGES=['index.html','teacher-pack.html','curriculum.html','student-lab.html','quality.html','release-notes.html','research-and-citation.html','404.html','tests/index.html']
PUBLIC_DOCS=['README.md','CHANGELOG.md','CITATION.cff','codemeta.json','applets.json','ARCHITECTURE.md','CONTRIBUTING.md','SECURITY.md','LICENSE','QA_CHECKLIST.md','QUALITY.md','RELEASE_NOTES.md','TEACHER_PACK.md','CURRICULUM.md','STUDENT_LAB_PACKET_TEMPLATE.md','CONTENT_STYLE_GUIDE.md']
INTERNAL_TERMS=[r'\x57\x61\x76\x65\s+\d',r'\x53\x74\x61\x62\x69\x6c\x69\x7a\x61\x74\x69\x6f\x6e',r'\x6d\x75\x6c\x74\x69-\x61\x67\x65\x6e\x74',r'\x46\x4d\x45\x41',r'\x63\x6f\x6c\x64[- ]?\x70\x61\x73\x73',r'\x6e\x6f\x74 \x73\x61\x66\x65 \x74\x6f \x63\x6c\x61\x69\x6d',r'\x73\x61\x66\x65 \x63\x6c\x61\x69\x6d',r'\x43\x6c\x61\x73\x73\x72\x6f\x6f\x6d \x4c\x61\x62 \x4d\x6f\x64\x65',r'\x56\x69\x73\x75\x61\x6c \x45\x78\x70\x6c\x61\x6e\x61\x74\x69\x6f\x6e \x4c\x65\x6e\x73',r'\x72\x65\x76\x69\x65\x77 \x66\x69\x78 \x46\d']
SECRET_PATTERNS=[r'AKIA[0-9A-Z]{16}',r'ghp_[A-Za-z0-9]{30,}',r'sk-[A-Za-z0-9]{20,}',r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----']

@dataclass
class Result:
    target:str; check:str; status:str; detail:str

def add(out,target,check,ok,detail): out.append(Result(target,check,'PASS' if ok else 'FAIL',detail))
def text(path): return path.read_text(encoding='utf-8',errors='replace')
def tracked():
    try:return set(subprocess.check_output(['git','ls-files'],cwd=ROOT,text=True).splitlines())
    except:return set()

def inline_scripts(path:Path, out:list[Result]):
    html=text(path)
    matches=list(re.finditer(r'<script([^>]*)>([\s\S]*?)</script>',html,re.I))
    for i,m in enumerate(matches,1):
        attrs,code=m.group(1),m.group(2)
        if re.search(r'type=["\']application/(?:ld\+json|json)["\']',attrs,re.I):
            try: json.loads(code); add(out,str(path.relative_to(ROOT)),f'JSON script {i}',True,'valid JSON')
            except Exception as e: add(out,str(path.relative_to(ROOT)),f'JSON script {i}',False,str(e))
            continue
        if not code.strip(): continue
        with tempfile.NamedTemporaryFile('w',suffix='.js',encoding='utf-8',delete=False) as f:
            f.write(code); name=f.name
        p=subprocess.run(['node','--check',name],capture_output=True,text=True)
        Path(name).unlink(missing_ok=True)
        add(out,str(path.relative_to(ROOT)),f'inline JavaScript {i}',p.returncode==0,'syntax accepted' if p.returncode==0 else (p.stderr.strip()[-500:] or 'syntax error'))

def scenario_count(html:str)->int:
    m=re.search(r'const\s+LESSON_TOUR\s*=\s*\[([\s\S]*?)\n\s*\];',html)
    return len(re.findall(r'\bapply\s*:',m.group(1))) if m else 0

def run()->list[Result]:
    out=[]; files=tracked()
    dirs={p.name for p in PLAYGROUNDS.iterdir() if p.is_dir()} if PLAYGROUNDS.exists() else set()
    add(out,'playgrounds','twelve canonical applets',dirs==EXPECTED,f'found {len(dirs)} applet directories')
    add(out,'repository','internal research tree excluded','research' not in dirs and not (ROOT/'research').exists(),'internal records live outside the public tree')
    add(out,'repository','internal version log excluded',not (ROOT/'VERSION_LOG.md').exists(),'public release uses CHANGELOG.md')
    for rel in PUBLIC_PAGES+PUBLIC_DOCS:
        add(out,rel,'public file present',(ROOT/rel).exists(),'present' if (ROOT/rel).exists() else 'missing')
    for rel in files:
        add(out,rel,'private path not tracked',not (rel.startswith('_local/') or rel.startswith('release-evidence/') or rel.startswith('tools/release-evidence/')),'public or source file' if not rel.startswith(('_local/','release-evidence/','tools/release-evidence/')) else 'private/generated path is tracked')
    public_paths=[ROOT/r for r in PUBLIC_PAGES+PUBLIC_DOCS if (ROOT/r).exists()]+sorted(PLAYGROUNDS.glob('*/index.html'))
    for p in public_paths:
        s=text(p); rel=str(p.relative_to(ROOT))
        add(out,rel,'no em dash','\u2014' not in s,'no em dash character' if '\u2014' not in s else 'em dash remains')
        if p.suffix.lower()=='.html':
            add(out,rel,'portfolio route','https://lmdixon23.github.io/' in s,'portfolio link present')
            add(out,rel,'old duplicated author footer absent','Built by Logan M. Dixon' not in s,'author appears once in the modern footer')
            foot=re.findall(r'<footer[\s\S]*?</footer>',s,re.I)
            if foot:
                add(out,rel,'single footer author name',foot[-1].count('Logan M. Dixon')==1,f"{foot[-1].count('Logan M. Dixon')} author-name occurrence in footer")
        for term in INTERNAL_TERMS:
            found=re.search(term,s,re.I)
            add(out,rel,f'public language excludes {term}',found is None,'clear' if found is None else f'found {found.group(0)!r}')
        for pat in SECRET_PATTERNS:
            add(out,rel,'secret pattern scan',re.search(pat,s) is None,'clear')
    # Landing page
    home=text(ROOT/'index.html')
    for needle,label in [
        ('id="bfsGrid"','live BFS proof'),('id="astarGrid"','live A* proof'),('id="appletGrid"','applet catalogue'),('id="filters"','catalogue filters'),
        ('id="teach"','classroom route'),('id="why"','differentiation section'),('id="research"','research and reuse section'),
        ('research-and-citation.html','citation route'),('CITATION.cff','citation metadata route'),('applets.json','catalogue metadata'),('id="support"','professional support section'),('id="shareProject"','share project action'),('--applet-accent','applet accent system')]:
        add(out,'index.html',label,needle in home,'present' if needle in home else 'missing')
    for slug in sorted(EXPECTED):
        add(out,'index.html',f'explicit route {slug}',f'playgrounds/{slug}/index.html' in home or f'${{a.slug}}/index.html' in home,'direct index route available')
    curriculum=text(ROOT/'curriculum.html')
    for phrase,label in [('Course and AIMA-aligned sequence','primary course sequence'),('Quick-entry four-app sampler','sampler sequence'),('--applet-accent','cross-page applet colors'),('Why this is not the course order','sequence rationale')]:
        add(out,'curriculum.html',label,phrase in curriculum,'present' if phrase in curriculum else 'missing')
    add(out,'curriculum.html','twelve course rows',curriculum.count('class="order-dot"')==12,f"{curriculum.count('class=\"order-dot\"')} rows")
    teacher=text(ROOT/'teacher-pack.html')
    for phrase,label in [('Course and AIMA-aligned applet map','course-aligned applet map'),('Quick-entry four-app sampler','clearly labeled sampler'),('--applet-accent','applet color consistency'),('Star on GitHub','restrained support call to action')]:
        add(out,'teacher-pack.html',label,phrase in teacher,'present' if phrase in teacher else 'missing')
    qa=text(ROOT/'QA_CHECKLIST.md')
    add(out,'QA_CHECKLIST.md','manual screen-reader walkthrough','## Manual screen-reader walkthrough' in qa and 'NVDA' in qa and 'VoiceOver' in qa,'named assistive-technology procedure present')
    style=text(ROOT/'CONTENT_STYLE_GUIDE.md')
    for phrase,label in [
        ('Name the idea before shortening it','term-before-abbreviation rule'),
        ('Use one canonical applet name','canonical-name rule'),
        ('Write scenarios as a reasoning sequence','learner scenario structure'),
        ('Keep the toolbar predictable','toolbar hierarchy'),
        ('Maintain bilingual parity','bilingual writing rule')]:
        add(out,'CONTENT_STYLE_GUIDE.md',label,phrase in style,'present' if phrase in style else 'missing')
    try:
        applet_meta={item['slug']:item for item in json.loads(text(ROOT/'applets.json'))}
    except Exception:
        applet_meta={}
    # Applets
    for slug in sorted(EXPECTED):
        p=PLAYGROUNDS/slug/'index.html'; h=text(p)
        canonical=str(applet_meta.get(slug,{}).get('title','')).strip()
        if canonical:
            canonical_html=canonical.replace('&','&amp;')
            add(out,slug,'canonical browser title',f'<title>{canonical_html} | AI Playgrounds</title>' in h or f'<title>{canonical} | AI Playgrounds</title>' in h,canonical)
            add(out,slug,'canonical page heading',re.search(r'<h1[^>]*>'+re.escape(canonical_html)+r'</h1>',h) is not None or re.search(r'<h1[^>]*>'+re.escape(canonical)+r'</h1>',h) is not None,canonical)
        add(out,slug,'learner content profile','id="learner-content-system"' in h and 'APPLET_LEARNER_PROFILE' in h,'bilingual learner profile present')
        add(out,slug,'learner house style','id="learner-house-style"' in h,'learner-facing component style present')
        add(out,slug,'key terms before explanation',"className='key-terms'" in h and 'Key terms before the explanation' in h,'term primer present')
        add(out,slug,'standard action hierarchy','header-more' in h and 'Current settings (.json)' in h and 'Embed in LMS' in h,'Share, More, and reset hierarchy present')
        add(out,slug,'universal state export','dataset.exportState' in h and "-settings.json" in h,'JSON settings export present')
        add(out,slug,'learner scenario labels',all(x in h for x in ['Core question','Run and watch','Predict first','Explain afterward']),'four-step reasoning labels present')
        add(out,slug,'teacher advice absent from learner profile',not re.search(r'APPLET_LEARNER_PROFILE[\s\S]*?Teacher use',h),'teacher facilitation kept outside learner cards')
        profile_match=re.search(r'const profile = (\{.*?\});\n  window.APPLET_LEARNER_PROFILE',h,re.S)
        if profile_match:
            try:
                profile=json.loads(profile_match.group(1))
                add(out,slug,'six bilingual key terms',len(profile.get('en',{}).get('terms',[]))>=6 and len(profile.get('zh',{}).get('terms',[]))>=6,f"{len(profile.get('en',{}).get('terms',[]))} EN / {len(profile.get('zh',{}).get('terms',[]))} ZH")
                add(out,slug,'five bilingual learner scenarios',len(profile.get('en',{}).get('scenarios',[]))>=5 and len(profile.get('zh',{}).get('scenarios',[]))>=5,f"{len(profile.get('en',{}).get('scenarios',[]))} EN / {len(profile.get('zh',{}).get('scenarios',[]))} ZH")
                big=profile.get('en',{}).get('big','')
                add(out,slug,'purpose avoids unexplained high-risk abbreviations',not re.search(r'\b(?:TSP|SA|HC|DPLL|CNF|CPT|RL|CNN|KNN)\b',big),'plain-language purpose statement')
            except Exception as exc:
                add(out,slug,'learner profile JSON',False,str(exc))
        else:
            add(out,slug,'learner profile JSON',False,'profile block not found')
        add(out,slug,'back route','href="../../index.html"' in h,'returns to suite landing page')
        add(out,slug,'bilingual controls',h.count('data-lang=')>=2,'English and Chinese controls present')
        add(out,slug,'scenario gallery','class="scenario-gallery"' in h,'present')
        n=scenario_count(h); add(out,slug,'five or more scenarios',n>=5,f'{n} scenario definitions')
        add(out,slug,'featured experiment','class="signature-challenge"' in h,'present')
        add(out,slug,'visual explanation','class="visual-explanation"' in h,'present')
        add(out,slug,'student response packet','class="classroom-lab"' in h and 'Student response packet' in h,'present')
        add(out,slug,'text and keyboard support','class="accessibility-layer"' in h and 'Text and keyboard support' in h,'present')
        add(out,slug,'four-mode architecture','id="product-consolidation-script"' in h and 'learning-mode-tabs' in h,'Explore, Understand, classroom, and access modes')
        add(out,slug,'restrained hierarchy','id="product-consolidation-style"' in h and '.learning-mode-panel>details>summary{background:var(--card)!important' in h,'neutral section bars with spotlight bodies')
        add(out,slug,'shareable control state','data-copy-experiment' in h and "searchParams.set('state'" in h,'URL state serializer present')
        add(out,slug,'scenario URL state',"searchParams.set('scenario'" in h,'scenario identifier written to URL')
        add(out,slug,'container query','@container' in h,'component-level responsive rule present')
        add(out,slug,'local packet formatting','markdownToPrintableHtml' in h,'semantic print renderer present')
        add(out,slug,'no static external script',re.search(r'<script[^>]+src=["\']https?://',h,re.I) is None,'no remote runtime script tag')
        add(out,slug,'scholarly identity','Logan M. Dixon' in h and '0009-0001-0592-462X' in h,'public author identity present')
        add(out,slug,'portfolio footer','https://lmdixon23.github.io/' in h and 'footer-portfolio' in h,'portfolio route and bilingual label present')
        add(out,slug,'modern footer course line','Made for the Introduction to AI course at Haidian Kaiwen Academy.' in h,'course line present')
        inline_scripts(p,out)
    # Test suite
    tests=text(ROOT/'tests/index.html')
    add(out,'tests/index.html','main landmark',bool(re.search(r'<main(?:\s|>)',tests,re.I)) and '</main>' in tests,'semantic main region present')
    tests_defined=len(re.findall(r'\btest\(',tests))-1
    add(out,'tests/index.html','complete algorithmic coverage',tests_defined>=45,f'{tests_defined} algorithmic tests defined')
    add(out,'tests/index.html','no skipped applets',re.search(r"\bskip\('",tests) is None,'no explicit skip cases')
    for group in ['Bayes classifier','CNF and DPLL','Wumpus inference','Tiny neural network']:
        add(out,'tests/index.html',f'{group} group',f"group('{group}')" in tests,'present')
    inline_scripts(ROOT/'tests/index.html',out)
    # Metadata and route files
    try:
        meta=json.loads(text(ROOT/'applets.json')); add(out,'applets.json','twelve metadata records',len(meta)==12,f'{len(meta)} records')
        accents=[str(x.get('accent','')).lower() for x in meta]
        add(out,'applets.json','accent metadata',all(re.fullmatch(r'#[0-9a-fA-F]{6}',a) for a in accents),'twelve valid applet accent colors')
        add(out,'applets.json','twelve unique accents',len(set(accents))==12,f'{len(set(accents))} unique colors')
        add(out,'applets.json','named color identities',all(str(x.get('accent_name','')).strip() for x in meta),'each applet has a human-readable accent name')
        for item in meta:
            slug=item['slug']; accent=item['accent'].lower(); page=text(PLAYGROUNDS/slug/'index.html').lower()
            add(out,slug,'metadata accent matches applet',f'--accent: {accent}' in page or f'--accent:{accent}' in page,f'{accent} applied')
        add(out,'index.html','visible catalogue tint','var(--surface) 84%,var(--applet-accent)' in home,'catalogue cards use visible restrained tint')
        add(out,'teacher-pack.html','no global accent override','--applet-accent:#0284c7!important' not in teacher,'inline applet identities remain active')
        add(out,'teacher-pack.html','restrained sampler color cues','class="sequence-table"' in teacher and teacher.count('class="sequence-dot"')==4,'four colored sequence markers')
        add(out,'curriculum.html','restrained sampler color cues',curriculum.count('class="step" style="--applet-accent:')==4,'four colored sampler cards')
        add(out,'applets.json','course sequence metadata',sorted(x.get('course_order') for x in meta)==list(range(1,13)),'course orders 1 through 12 present')
        add(out,'applets.json','showcase sequence metadata',sorted(x.get('showcase_order') for x in meta)==list(range(1,13)),'showcase orders 1 through 12 present')
    except Exception as e:add(out,'applets.json','valid JSON',False,str(e))
    try:json.loads(text(ROOT/'codemeta.json'));add(out,'codemeta.json','valid JSON',True,'valid')
    except Exception as e:add(out,'codemeta.json','valid JSON',False,str(e))
    sitemap=text(ROOT/'sitemap.xml')
    for page in ['research-and-citation.html','quality.html','teacher-pack.html','curriculum.html','student-lab.html','release-notes.html']:
        add(out,'sitemap.xml',f'route {page}',page in sitemap,'listed')
    # Public package leaks and stale artifacts.
    add(out,'playgrounds/AI_playgrounds.zip','stale download absent',not (PLAYGROUNDS/'AI_playgrounds.zip').exists(),'absent')
    return out

def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument('--json',type=Path,default=ROOT/'release-evidence/release-check.json');args=ap.parse_args();dest=args.json if args.json.is_absolute() else ROOT/args.json
    results=run();counts={'PASS':0,'WARN':0,'FAIL':0}
    for r in results:counts[r.status]+=1
    payload={'timestamp_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'root':str(ROOT),'counts':counts,'results':[asdict(r) for r in results]}
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f"AI Playgrounds release check: {counts['PASS']} pass, {counts['WARN']} warn, {counts['FAIL']} fail")
    print(f"Evidence: {dest.relative_to(ROOT) if dest.is_relative_to(ROOT) else dest}")
    for r in results:
        if r.status!='PASS':print(f'{r.status}: {r.target} :: {r.check} :: {r.detail}')
    return 1 if counts['FAIL'] else 0
if __name__=='__main__':raise SystemExit(main())
