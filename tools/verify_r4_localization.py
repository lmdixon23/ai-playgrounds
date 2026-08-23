#!/usr/bin/env python3
from __future__ import annotations
import json,pathlib,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
SLUGS=['bayes-classifier', 'bayes-network', 'cnf-sat', 'convolution', 'hill-climbing', 'kmeans', 'knn-classifier', 'neural-network', 'overfitting', 'q-learning-gridworld', 'search-pathfinding', 'wumpus-world']
fails=[]
for slug in SLUGS:
 p=ROOT/'playgrounds'/slug/'index.html';s=p.read_text(encoding='utf-8')
 for token in ('localization-r4.css',f'assets/locales/{slug}-r4.js','localization-r4.js','hreflang="vi"','hreflang="es"','"inLanguage":["en","zh","vi","es"]'):
  if token not in s:fails.append(f'{slug}: missing {token}')
 cat=ROOT/'assets'/'locales'/f'{slug}-r4.js'
 if not cat.is_file():fails.append(f'{slug}: missing catalog')
 proc=subprocess.run([sys.executable,str(ROOT/'tools'/'verify_r4_locale_catalog.py'),'--slug',slug],text=True,capture_output=True)
 print(proc.stdout,end='');print(proc.stderr,end='',file=sys.stderr)
 if proc.returncode:fails.append(f'{slug}: exact rendered-source catalog verification failed')
for f in fails:print('FAIL: '+f,file=sys.stderr)
print(json.dumps({'harness':'tools/verify_r4_localization.py','applets':12,'failed':len(fails),'pass':not fails},indent=2))
raise SystemExit(0 if not fails else 1)
