#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, subprocess, sys, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EVIDENCE=ROOT/'release-evidence'/'guided-challenges.json'
APPLETS=[
 'bayes-classifier','bayes-network','cnf-sat','convolution','hill-climbing','kmeans',
 'knn-classifier','neural-network','overfitting','q-learning-gridworld','search-pathfinding','wumpus-world'
]
START='<!-- suite-guided-challenge-v2:start -->';END='<!-- suite-guided-challenge-v2:end -->'
REQUIRED_STATES=['inactive','awaiting-prediction','prediction-complete-unlocked','locked','revealed','compared','reset']
PREDICTION_TERMS={
 'search-pathfinding':['Next frontier state or coordinate'], 'hill-climbing':['Candidate you expect to be accepted'],
 'wumpus-world':['Predicted knowledge status'], 'cnf-sat':['Next mechanism'],
 'bayes-classifier':['Predicted true positives','Predicted false positives'],
 'bayes-network':['Predicted probability direction','Predicted dependence status'],
 'overfitting':['Training error','Validation error'], 'neural-network':['Predicted boundary family'],
 'knn-classifier':['#knnGuided','guidedLock','guidedReveal'],
 'kmeans':['Predicted cluster assignment','Predicted centroid movement'],
 'convolution':['Predicted output-cell value'], 'q-learning-gridworld':['Predicted action','Predicted Q update direction'],
}
EXPECTED_BLOCK='''<!-- suite-guided-challenge-v2:start -->\n<link href="../../assets/guided-challenges.css" rel="stylesheet"/>\n<script defer src="../../assets/guided-challenges.js"></script>\n<!-- suite-guided-challenge-v2:end -->'''

def block(text:str)->str:
    if text.count(START)!=1 or text.count(END)!=1:return ''
    return START+text.split(START,1)[1].split(END,1)[0]+END

def main()->int:
    checks=[]; failures=[]; hashes=[]
    js_path=ROOT/'assets/guided-challenges.js'; css_path=ROOT/'assets/guided-challenges.css'
    js=js_path.read_text(encoding='utf-8-sig') if js_path.is_file() else ''
    css=css_path.read_text(encoding='utf-8-sig') if css_path.is_file() else ''
    for path,kind in [(js_path,'shared-js'),(css_path,'shared-css')]:
        ok=path.is_file() and path.stat().st_size>500; checks.append({'kind':kind,'pass':ok,'size':path.stat().st_size if path.exists() else 0})
        if not ok: failures.append(f'missing or undersized {kind}')
    if js:
        with tempfile.NamedTemporaryFile('w',suffix='.js',encoding='utf-8',delete=False) as f:
            f.write(js); name=f.name
        proc=subprocess.run(['node','--check',name],capture_output=True,text=True);Path(name).unlink(missing_ok=True)
        ok=proc.returncode==0;checks.append({'kind':'shared-js-syntax','pass':ok})
        if not ok:failures.append('shared guided JavaScript syntax failure: '+proc.stderr[-500:])
    for slug in APPLETS:
        p=ROOT/'playgrounds'/slug/'index.html';ok=p.is_file();checks.append({'kind':'file','applet':slug,'pass':ok})
        if not ok:failures.append(f'{slug}: missing applet file');continue
        text=p.read_text(encoding='utf-8-sig');b=block(text); exact=b==EXPECTED_BLOCK
        checks.append({'kind':'shared-asset-reference','applet':slug,'pass':exact})
        if not exact:failures.append(f'{slug}: guided asset reference block missing, duplicated, or altered')
        hashes.append(hashlib.sha256(b.encode()).hexdigest() if b else '')
        source=js if slug!='knn-classifier' else js+'\n'+text
        for phrase in PREDICTION_TERMS[slug]:
            ok=phrase in source;checks.append({'kind':'prediction-object','applet':slug,'phrase':phrase,'pass':ok})
            if not ok:failures.append(f'{slug}: missing mechanism-specific prediction object {phrase}')
    same=bool(hashes) and len(set(hashes))==1
    checks.append({'kind':'identical-shared-reference-block','pass':same,'unique_hashes':len(set(hashes))})
    if not same:failures.append('guided asset reference block differs across applets')
    for token in ['suite-guided-shell','window.__suiteGuidedChallenge','data-guided-field','aria-live="polite"']:
        ok=token in js;checks.append({'kind':'guided-token','token':token,'pass':ok})
        if not ok:failures.append(f'shared JS missing {token}')
    privacy='localStorage' not in js and 'sessionStorage' not in js
    checks.append({'kind':'prediction-privacy','pass':privacy})
    if not privacy:failures.append('challenge JS must not persist prediction responses')
    for state in REQUIRED_STATES:
        ok=state in js;checks.append({'kind':'state-contract','state':state,'pass':ok})
        if not ok:failures.append(f'missing guided state {state}')
    for token in ["setState('locked')","setState('revealed')","setState('compared')","visibility = 'hidden'","el.disabled = true","button[data-lang]"]:
        ok=token in js;checks.append({'kind':'state-mechanism','token':token,'pass':ok})
        if not ok:failures.append(f'missing state mechanism {token}')
    doc=ROOT/'docs/GUIDED_CHALLENGE_ARCHITECTURE.md';dt=doc.read_text(encoding='utf-8-sig') if doc.is_file() else ''
    for phrase in ['Prompt -> Commit prediction -> Reveal mechanism -> Compare -> Explain -> Transfer','R2 suite-wide implementation','prediction-complete-unlocked','shared external assets']:
        ok=phrase in dt;checks.append({'kind':'architecture-doc','phrase':phrase,'pass':ok})
        if not ok:failures.append(f'architecture doc missing {phrase}')
    wf=ROOT/'.github/workflows/verify.yml';wt=wf.read_text(encoding='utf-8-sig') if wf.is_file() else ''
    for cmd in ['python tools/verify_guided_challenges.py','python tools/guided_challenge_qa.py']:
        ok=cmd in wt;checks.append({'kind':'workflow-gate','command':cmd,'pass':ok})
        if not ok:failures.append(f'workflow missing {cmd}')
    bs=ROOT/'tools/build_site.py';bt=bs.read_text(encoding='utf-8-sig') if bs.is_file() else ''
    for asset in ['assets/guided-challenges.css','assets/guided-challenges.js']:
        ok=asset in bt;checks.append({'kind':'deployment-asset','asset':asset,'pass':ok})
        if not ok:failures.append(f'build_site does not deploy {asset}')
    payload={'harness':'tools/verify_guided_challenges.py','applets':len(APPLETS),'checks':len(checks),'passed':sum(bool(x.get('pass')) for x in checks),'failed':sum(not bool(x.get('pass')) for x in checks),'pass':not failures,'failures':failures,'details':checks}
    EVIDENCE.parent.mkdir(parents=True,exist_ok=True);EVIDENCE.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:payload[k] for k in ('harness','applets','checks','passed','failed','pass')},indent=2))
    for f in failures:print('FAIL: '+f,file=sys.stderr)
    return 0 if not failures else 1
if __name__=='__main__':raise SystemExit(main())
