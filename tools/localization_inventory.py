#!/usr/bin/env python3
from __future__ import annotations
import json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'release-evidence'/'localization-r4-inventory.json'
APPLETS=['bayes-classifier','bayes-network','cnf-sat','convolution','hill-climbing','kmeans','knn-classifier','neural-network','overfitting','q-learning-gridworld','search-pathfinding','wumpus-world']

LANG_BUTTON_RE=re.compile(r'data-lang=["\']([^"\']+)["\']')
HREFLANG_RE=re.compile(r'hreflang=["\']([^"\']+)["\']')
ESSAY_RE=re.compile(r'data-essay-lang=["\']([^"\']+)["\']')
I18N_RE=re.compile(r'data-i18n=["\']([^"\']+)["\']')


def main()->int:
    rows=[]
    totals={'data_i18n':0,'clipboard_surfaces':0,'scenario_markers':0,'tour_markers':0,'a11y_markers':0}
    for slug in APPLETS:
        p=ROOT/'playgrounds'/slug/'index.html'
        text=p.read_text(encoding='utf-8-sig')
        langs=sorted(set(LANG_BUTTON_RE.findall(text)))
        hrefs=sorted(set(HREFLANG_RE.findall(text)))
        essays=sorted(set(ESSAY_RE.findall(text)))
        i18n_keys=sorted(set(I18N_RE.findall(text)))
        row={
            'slug':slug,
            'bytes':len(text.encode('utf-8')),
            'language_controls':langs,
            'hreflang':hrefs,
            'essay_locales':essays,
            'data_i18n_keys':len(i18n_keys),
            'has_strings_table':'const STRINGS' in text,
            'has_learner_profile':'const profile =' in text,
            'has_a11y_config':'const A11Y_CONFIG' in text,
            'has_translation_completion':'applet-translation-completion' in text,
            'clipboard_surfaces':text.count('navigator.clipboard')+text.count('clipboard.writeText'),
            'scenario_markers':text.count('data-scenario-index'),
            'tour_markers':text.count('LESSON_TOUR'),
            'a11y_markers':text.count('A11Y_CONFIG'),
            'guided_shared_reference':'guided-challenges.js' in text,
        }
        totals['data_i18n']+=len(i18n_keys)
        for key in ('clipboard_surfaces','scenario_markers','tour_markers','a11y_markers'):
            totals[key]+=row[key]
        rows.append(row)
    shared=(ROOT/'assets/guided-challenges.js').read_text(encoding='utf-8-sig')
    payload={
        'harness':'tools/localization_inventory.py',
        'applets':len(rows),
        'totals':totals,
        'shared_guided_bytes':len(shared.encode('utf-8')),
        'shared_guided_has_en':"en: {" in shared,
        'shared_guided_has_zh':"zh: {" in shared,
        'shared_guided_has_vi':"vi: {" in shared,
        'shared_guided_has_es':"es: {" in shared,
        'rows':rows,
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(payload,ensure_ascii=False,indent=2))
    return 0

if __name__=='__main__': raise SystemExit(main())
