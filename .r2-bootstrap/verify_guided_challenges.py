#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT/'release-evidence'/'guided-challenges.json'
APPLETS = [
 'bayes-classifier','bayes-network','cnf-sat','convolution','hill-climbing','kmeans',
 'knn-classifier','neural-network','overfitting','q-learning-gridworld','search-pathfinding','wumpus-world'
]
MARKER_START='<!-- suite-guided-challenge-v2:start -->'
MARKER_END='<!-- suite-guided-challenge-v2:end -->'
REQUIRED_STATES=['inactive','awaiting-prediction','prediction-complete-unlocked','locked','revealed','compared','reset']
PREDICTION_TERMS={
 'search-pathfinding':['Next frontier state or coordinate'],
 'hill-climbing':['Candidate you expect to be accepted'],
 'wumpus-world':['Predicted knowledge status'],
 'cnf-sat':['Next mechanism'],
 'bayes-classifier':['Predicted true positives','Predicted false positives'],
 'bayes-network':['Predicted probability direction','Predicted dependence status'],
 'overfitting':['Training error','Validation error'],
 'neural-network':['Predicted boundary family'],
 'knn-classifier':['#knnGuided','guidedLock','guidedReveal'],
 'kmeans':['Predicted cluster assignment','Predicted centroid movement'],
 'convolution':['Predicted output-cell value'],
 'q-learning-gridworld':['Predicted action','Predicted Q update direction'],
}

def block(text:str)->str:
    if text.count(MARKER_START)!=1 or text.count(MARKER_END)!=1:
        return ''
    return text.split(MARKER_START,1)[1].split(MARKER_END,1)[0]

def main()->int:
    checks=[]; failures=[]; hashes=[]
    for slug in APPLETS:
        p=ROOT/'playgrounds'/slug/'index.html'
        ok=p.is_file(); checks.append({'kind':'file','applet':slug,'pass':ok})
        if not ok:
            failures.append(f'{slug}: missing applet file'); continue
        text=p.read_text(encoding='utf-8-sig')
        b=block(text)
        ok=bool(b); checks.append({'kind':'single-guided-block','applet':slug,'pass':ok})
        if not ok:
            failures.append(f'{slug}: guided block missing or duplicated'); continue
        hashes.append(hashlib.sha256(b.encode('utf-8')).hexdigest())
        for token in ['suite-guided-shell','window.__suiteGuidedChallenge','data-guided-field','aria-live="polite"']:
            tok_ok=token in b; checks.append({'kind':'guided-token','applet':slug,'token':token,'pass':tok_ok})
            if not tok_ok: failures.append(f'{slug}: missing guided token {token}')
        for phrase in PREDICTION_TERMS[slug]:
            ph_ok=phrase in (b if slug!='knn-classifier' else text); checks.append({'kind':'prediction-object','applet':slug,'phrase':phrase,'pass':ph_ok})
            if not ph_ok: failures.append(f'{slug}: missing mechanism-specific prediction object {phrase}')
        privacy_ok='localStorage' not in b and 'sessionStorage' not in b
        checks.append({'kind':'prediction-privacy','applet':slug,'pass':privacy_ok})
        if not privacy_ok: failures.append(f'{slug}: challenge block must not persist prediction responses')
        id_leak_ok=not re.search(r'<(?:input|select|textarea)[^>]+id=["\'](?:guided|suite-guided)', b, re.I)
        checks.append({'kind':'share-url-response-isolation','applet':slug,'pass':id_leak_ok})
        if not id_leak_ok: failures.append(f'{slug}: challenge prediction input has an id and could enter shared state')
    same=bool(hashes) and len(set(hashes))==1
    checks.append({'kind':'identical-shared-guided-block','pass':same,'unique_hashes':len(set(hashes))})
    if not same: failures.append('guided challenge embedded block differs across applets')

    exemplar=(ROOT/'playgrounds'/'bayes-classifier'/'index.html').read_text(encoding='utf-8-sig') if (ROOT/'playgrounds'/'bayes-classifier'/'index.html').is_file() else ''
    b=block(exemplar)
    for state in REQUIRED_STATES:
        ok=state in b; checks.append({'kind':'state-contract','state':state,'pass':ok})
        if not ok: failures.append(f'missing guided state {state}')
    for token in ['setState(\'locked\')','setState(\'revealed\')','setState(\'compared\')','visibility = \'hidden\'','el.disabled = true','button[data-lang]']:
        ok=token in b; checks.append({'kind':'state-mechanism','token':token,'pass':ok})
        if not ok: failures.append(f'missing state mechanism {token}')

    doc=ROOT/'docs'/'GUIDED_CHALLENGE_ARCHITECTURE.md'
    doc_text=doc.read_text(encoding='utf-8-sig') if doc.is_file() else ''
    for phrase in ['Prompt -> Commit prediction -> Reveal mechanism -> Compare -> Explain -> Transfer','suite-wide R2','prediction-complete-unlocked']:
        ok=phrase in doc_text; checks.append({'kind':'architecture-doc','phrase':phrase,'pass':ok})
        if not ok: failures.append(f'architecture doc missing {phrase}')

    workflow=ROOT/'.github/workflows/verify.yml'
    wf=workflow.read_text(encoding='utf-8-sig') if workflow.is_file() else ''
    for cmd in ['python tools/verify_guided_challenges.py','python tools/guided_challenge_qa.py']:
        ok=cmd in wf; checks.append({'kind':'workflow-gate','command':cmd,'pass':ok})
        if not ok: failures.append(f'workflow missing {cmd}')

    payload={'harness':'tools/verify_guided_challenges.py','applets':len(APPLETS),'checks':len(checks),'passed':sum(bool(x.get('pass')) for x in checks),'failed':sum(not bool(x.get('pass')) for x in checks),'pass':not failures,'failures':failures,'details':checks}
    EVIDENCE.parent.mkdir(parents=True,exist_ok=True)
    EVIDENCE.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:payload[k] for k in ('harness','applets','checks','passed','failed','pass')},indent=2))
    for f in failures: print('FAIL: '+f,file=sys.stderr)
    return 0 if not failures else 1
if __name__=='__main__': raise SystemExit(main())
