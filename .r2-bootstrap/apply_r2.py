#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, shutil
from pathlib import Path

APPLETS=[
 'bayes-classifier','bayes-network','cnf-sat','convolution','hill-climbing','kmeans',
 'knn-classifier','neural-network','overfitting','q-learning-gridworld','search-pathfinding','wumpus-world'
]
START='<!-- suite-guided-challenge-v2:start -->'
END='<!-- suite-guided-challenge-v2:end -->'

def read(p:Path)->str: return p.read_text(encoding='utf-8-sig')
def write(p:Path,s:str):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(s.rstrip('\n')+'\n',encoding='utf-8',newline='\n')

def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument('--repo',required=True);ap.add_argument('--payload',required=True);ap.add_argument('--report',required=True);a=ap.parse_args()
    root=Path(a.repo).resolve(); payload=Path(a.payload).resolve(); report=Path(a.report).resolve()
    block=(
        f'\n{START}\n'
        '<link href="../../assets/guided-challenges.css" rel="stylesheet"/>\n'
        '<script defer src="../../assets/guided-challenges.js"></script>\n'
        f'{END}\n'
    )
    ops=[]

    assets=root/'assets'; assets.mkdir(parents=True,exist_ok=True)
    shutil.copy2(payload/'guided_challenges_block.js',assets/'guided-challenges.js')
    shutil.copy2(payload/'guided_challenges_block.css',assets/'guided-challenges.css')
    ops += ['assets/guided-challenges.js','assets/guided-challenges.css']

    for slug in APPLETS:
        p=root/'playgrounds'/slug/'index.html'; text=read(p)
        if START in text or END in text: raise RuntimeError(f'{slug}: R2 guided block already present')
        body_close=text.rfind('</body>')
        if body_close < 0: raise RuntimeError(f'{slug}: missing document </body>')
        text=text[:body_close]+block+text[body_close:]
        write(p,text);ops.append(str(p.relative_to(root)))

    doc=root/'docs/GUIDED_CHALLENGE_ARCHITECTURE.md'; text=read(doc)
    section='''

## R2 suite-wide implementation

R2 implements the challenge discipline across all twelve applets while preserving the existing Explore behavior. The common sequence is:

`Prompt -> Commit prediction -> Reveal mechanism -> Compare -> Explain -> Transfer`

The shared state names are `inactive`, `awaiting-prediction`, `prediction-complete-unlocked`, `locked`, `revealed`, `compared`, and `reset`.

Implementation rules:

- Explore remains the immediate, unrestricted applet path.
- Guided Challenge prepares a deterministic existing applet scenario, conceals the relevant result before the scenario is applied, and freezes ordinary controls while the learner prediction is pending.
- Locking copies the prediction into immutable in-memory state. Prediction controls are disabled before the mechanism can be revealed.
- Any deferred algorithm step is invoked through the same DOM control and event path used by Explore mode; R2 does not maintain a second hidden implementation of the algorithm.
- Reveal removes the concealment and records the applet's text-equivalent state for side-by-side comparison with the locked prediction.
- Compare unlocks the explanation field. Transfer requires an explanation and then prepares a changed scenario that requires a new prediction.
- Challenge response fields deliberately have no element IDs and are never written to localStorage, sessionStorage, analytics, or the share-URL state payload.
- Language switching rerenders labels without changing prediction values or challenge state.
- Reset records the reset transition and returns to inactive state.
- KNN retains the R1 exact-neighbor prototype and moves it under the suite-level Guided Challenge mode. Its transfer case changes the closeness rule and requires a fresh neighbor prediction.
- The suite-level challenge JavaScript and CSS are shared external assets. Applet pages contain only stable references to those assets, avoiding duplicated implementation copies and keeping one canonical state machine.

R2 adds static contract verification and a twelve-applet browser state-transition suite. The browser suite checks reveal-before-lock prevention, immutable locked predictions, bilingual state preservation, text-equivalent actual results, compare-before-explain ordering, transfer-to-new-prediction behavior, reset behavior, and the KNN exact-neighbor path.
'''
    if '## R2 suite-wide implementation' in text: raise RuntimeError('architecture R2 section already present')
    write(doc,text+section);ops.append(str(doc.relative_to(root)))

    for name in ('verify_guided_challenges.py','guided_challenge_qa.py'):
        src=payload/name; dst=root/'tools'/name; shutil.copy2(src,dst);ops.append(str(dst.relative_to(root)))

    bq=root/'tools/browser_qa.py'; text=read(bq)
    old='REQUIRED_APPLET_SELECTORS = [".scenario-gallery", ".signature-challenge", ".lab-panel", ".visual-explanation", ".accessibility-layer", ".learning-mode-shell", ".key-terms", ".header-more"]'
    new='REQUIRED_APPLET_SELECTORS = [".scenario-gallery", ".signature-challenge", ".lab-panel", ".visual-explanation", ".accessibility-layer", ".learning-mode-shell", ".key-terms", ".header-more", ".suite-guided-shell"]'
    if old not in text: raise RuntimeError('browser QA selector anchor missing')
    write(bq,text.replace(old,new,1));ops.append(str(bq.relative_to(root)))

    build=root/'tools/build_site.py'; text=read(build)
    anchor='''    "media/AI_Playgrounds_Demo_15s.mp4",\n    "robots.txt",'''
    replacement='''    "media/AI_Playgrounds_Demo_15s.mp4",\n    "assets/guided-challenges.css",\n    "assets/guided-challenges.js",\n    "robots.txt",'''
    if anchor not in text: raise RuntimeError('build_site public-file anchor missing')
    write(build,text.replace(anchor,replacement,1));ops.append(str(build.relative_to(root)))

    wf=root/'.github/workflows/verify.yml'; text=read(wf)
    anchor='''      - name: Verify pedagogical contracts\n        run: python tools/verify_pedagogical_contracts.py\n'''
    insert=anchor+'''\n      - name: Verify guided challenge contracts\n        run: python tools/verify_guided_challenges.py\n\n      - name: Run guided challenge state QA\n        run: python tools/guided_challenge_qa.py\n'''
    if anchor not in text: raise RuntimeError('verify workflow anchor missing')
    if 'python tools/verify_guided_challenges.py' in text: raise RuntimeError('guided workflow gates already present')
    write(wf,text.replace(anchor,insert,1));ops.append(str(wf.relative_to(root)))

    report.parent.mkdir(parents=True,exist_ok=True)
    payload_out={'pass':True,'changed_files':sorted(set(ops)),'changed_count':len(set(ops)),'applets':len(APPLETS),'shared_assets':2}
    report.write_text(json.dumps(payload_out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(payload_out,indent=2))
    return 0
if __name__=='__main__': raise SystemExit(main())
