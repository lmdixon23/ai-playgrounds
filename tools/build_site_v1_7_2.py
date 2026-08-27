#!/usr/bin/env python3
from __future__ import annotations

"""Deterministic v1.7.2 modern-parity release composition.

The preceding accessibility builder owns the structured open panel and all
localized copy. This final wrapper replaces only its polling runtime with a
bounded event-driven runtime. Labs 13-15 already contain the Quick Assign and
text-state source nodes when final composition runs, so recurring readiness
polling is unnecessary. It then binds the final artifact to the v1.7.2 release
identity while preserving every historical public release-note card.
"""

import json
import re
import shutil

import build_site_v1_7_2_modern_parity_accessible as base

SITE = base.SITE
MODERN = base.MODERN
CURRENT = "v1.7.2"
SOURCE_IDS = {
    "transformer-language-model": "stateText",
    "agent-tool-context": "stateText",
    "minimax-alpha-beta": "textState",
}


def stable_runtime(slug: str) -> str:
    labels = json.dumps(base.LABELS, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    source_id = SOURCE_IDS[slug]
    return f'''<script id="v172-modern-packet-label-runtime" data-v172-stable-lifecycle="true">
(()=>{{'use strict';
const COPY={labels};
const SOURCE_ID={json.dumps(source_id)};
const norm=v=>{{v=String(v||'').toLowerCase();return v.startsWith('zh')?'zh':v.startsWith('vi')?'vi':v.startsWith('es')?'es':'en'}};
const locale=()=>norm(document.documentElement.lang);
const root=()=>document.querySelector('[data-quick-assign-id]');
const source=()=>document.getElementById(SOURCE_ID);
function sourceText(){{const s=source();return s?String(s.value||s.textContent||'').trim():''}}
function syncAccessibleState(){{
  const out=document.getElementById('ap-modern-a11y-state');if(!out)return;
  const packet=root()?.querySelector('[data-qa-modern-state]');
  const next=sourceText()||String(packet?.textContent||'').trim();
  if(!next)return;
  if(out.textContent!==next){{out.textContent=next;const live=document.getElementById('ap-modern-a11y-live');if(live)live.textContent=next.slice(0,500)}}
}}
function paintLabels(){{
  const qa=root(),l=COPY[locale()]||COPY.en;if(!qa){{syncAccessibleState();return}}
  qa.querySelectorAll('[data-qa-answer]').forEach(el=>{{const key=el.dataset.qaAnswer;if(l[key])el.setAttribute('aria-label',l[key])}});
  for(const key of ['refresh','copy','print','clear']){{const action=key==='refresh'?'refresh-state':key;const button=qa.querySelector('[data-qa-action="'+action+'"]');if(!button)continue;const label=l[key]||COPY.en[key];button.textContent=(key==='refresh'?'↻ ':'')+label;button.setAttribute('aria-label',label)}}
  const state=qa.querySelector('[data-qa-modern-state]');if(state)state.setAttribute('aria-label',l.state||COPY.en.state);
  syncAccessibleState();
}}
let repaintGeneration=0;
function schedulePaint(){{
  const generation=++repaintGeneration;
  const run=()=>{{if(generation===repaintGeneration)paintLabels()}};
  run();queueMicrotask(run);if(window.requestAnimationFrame)requestAnimationFrame(run);
  setTimeout(run,40);setTimeout(run,110);setTimeout(run,180);
}}
const src=source();if(src){{new MutationObserver(syncAccessibleState).observe(src,{{childList:true,subtree:true,characterData:true,attributes:true}});src.addEventListener?.('input',syncAccessibleState);src.addEventListener?.('change',syncAccessibleState)}}
new MutationObserver(schedulePaint).observe(document.documentElement,{{attributes:true,attributeFilter:['lang']}});
window.addEventListener('lab13localechange',schedulePaint);window.addEventListener('lab14localechange',schedulePaint);window.addEventListener('lab15localechange',schedulePaint);
schedulePaint();syncAccessibleState();
}})();</script>'''


def replace_runtime(page: str, slug: str) -> str:
    pattern = re.compile(r'<script\b[^>]*\bid="v172-modern-packet-label-runtime"[^>]*>.*?</script>', re.S | re.I)
    page, count = pattern.subn(stable_runtime(slug), page, count=1)
    if count != 1:
        raise RuntimeError(f"Modern accessibility runtime missing before stable replacement: {slug}")
    return page


def patch_release_identity() -> None:
    for path in sorted(SITE.rglob("*.html")):
        page = path.read_text(encoding="utf-8")
        if path.name != "release-notes.html":
            page = page.replace("v1.7.1", CURRENT)
            page = page.replace('content="1.7.1"', 'content="1.7.2"')
        page = page.replace(
            'data-ai-playgrounds-analytics="v1.7.1"',
            'data-ai-playgrounds-analytics="v1.7.2"',
        )
        page = page.replace(
            '<meta name="ai-playgrounds-version" content="1.7.1">',
            '<meta name="ai-playgrounds-version" content="1.7.2">',
        )
        page = page.replace(
            '<span class="site-version">v1.7.1</span>',
            '<span class="site-version">v1.7.2</span>',
        )
        path.write_text(page, encoding="utf-8")

    notes_path = SITE / "release-notes.html"
    notes = notes_path.read_text(encoding="utf-8")
    anchor = '<section id="release-v1-7-1"'
    if anchor not in notes:
        raise RuntimeError("Release-notes v1.7.1 anchor changed")
    if 'id="release-v1-7-2"' not in notes:
        section = (
            '<section id="release-v1-7-2" style="margin:1rem 0;padding:1rem 1.2rem;'
            'border:1px solid currentColor;border-radius:12px">'
            '<h2>AI Playgrounds v1.7.2: modern-lab parity and release assurance.</h2>'
            '<p>Labs 13–15 now share the mature suite\'s navigation, discovery metadata, '
            'localized learning support, accessibility-oriented text state, and complete '
            'Quick Assign packet actions. The release preserves all fifteen algorithms, '
            'curriculum placement, one-assignment-per-lab architecture, four learner '
            'locales, and the one-time legacy theme migration.</p></section>'
        )
        notes = notes.replace(anchor, section + anchor, 1)
    notes_path.write_text(notes, encoding="utf-8")

    # Keep this historical composition reproducible after later source releases
    # advance repository-level citation metadata. The successor builder copies
    # its own current metadata only after this v1.7.2 layer has validated.
    codemeta_path = SITE / "codemeta.json"
    codemeta = json.loads(codemeta_path.read_text(encoding="utf-8"))
    codemeta["softwareVersion"] = "1.7.2"
    codemeta["identifier"] = "https://github.com/lmdixon23/ai-playgrounds/releases/tag/v1.7.2"
    codemeta_path.write_text(json.dumps(codemeta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    citation_path = SITE / "CITATION.cff"
    citation = citation_path.read_text(encoding="utf-8")
    citation = re.sub(r"(?m)^version:\s*.*$", "version: 1.7.2", citation, count=1)
    citation_path.write_text(citation, encoding="utf-8")


def validate() -> None:
    for slug in MODERN:
        page=(SITE/'playgrounds'/slug/'index.html').read_text(encoding='utf-8')
        required=(
            'id="v172-modern-packet-label-runtime" data-v172-stable-lifecycle="true"',
            'class="accessibility-layer ap-modern-a11y-parity" open',
            'id="ap-modern-a11y-state"', 'syncAccessibleState',
            'setTimeout(run,180)', f'const SOURCE_ID={json.dumps(SOURCE_IDS[slug])}',
        )
        missing=[m for m in required if m not in page]
        if missing: raise RuntimeError(f"Stable modern accessibility lifecycle incomplete for {slug}: {missing}")
        if 'readinessTimer' in page or 'readinessTries' in page or '__v172LabelWrapped' in page:
            raise RuntimeError(f"Polling/wrapped accessibility lifecycle survived stable composition: {slug}")
    # The preceding accessibility wrapper already validated its own structured
    # panel before this runtime replacement. Re-run the immediately preceding
    # Quick Assign/parity validator, not the obsolete polling-runtime validator.
    base.base.validate()

    files = sorted(path for path in SITE.rglob("*") if path.is_file())
    applets = sorted((SITE / "playgrounds").glob("*/index.html"))
    if len(files) != 58 or len(applets) != 15:
        raise RuntimeError(f"v1.7.2 boundary drift: {len(files)} files / {len(applets)} applets")
    for path in applets:
        page = path.read_text(encoding="utf-8")
        if '<meta name="ai-playgrounds-version" content="1.7.2">' not in page:
            raise RuntimeError(f"Applet version metadata not v1.7.2: {path.parent.name}")
        if 'data-ai-playgrounds-analytics="v1.7.2"' not in page:
            raise RuntimeError(f"Applet analytics provenance not v1.7.2: {path.parent.name}")
    home = (SITE / "index.html").read_text(encoding="utf-8")
    if '<span class="site-version">v1.7.2</span>' not in home:
        raise RuntimeError("Homepage visible release version is not v1.7.2")
    notes = (SITE / "release-notes.html").read_text(encoding="utf-8")
    for release in ("release-v1-7-2", "release-v1-7-1", "release-v1-7-0", "release-v1-6-2"):
        if f'id="{release}"' not in notes:
            raise RuntimeError(f"Release-note history missing {release}")
    codemeta = json.loads((SITE / "codemeta.json").read_text(encoding="utf-8"))
    if codemeta.get("softwareVersion") != "1.7.2" or not str(codemeta.get("identifier", "")).endswith("/releases/tag/v1.7.2"):
        raise RuntimeError("Deployed CodeMeta is not bound to v1.7.2")
    citation = (SITE / "CITATION.cff").read_text(encoding="utf-8")
    if re.search(r"(?m)^version:\s*['\"]?1\.7\.2['\"]?\s*$", citation) is None:
        raise RuntimeError("Deployed citation metadata is not bound to v1.7.2")
    base.base.base.candidate.core.validate_local_references()


def build_site() -> None:
    # The inherited historical builder chain was designed around one clean CI
    # composition. Remove only its generated, ignored output so v1.7.2 is safe
    # to invoke repeatedly from any prior release artifact.
    if SITE.exists():
        shutil.rmtree(SITE)
    base.build_site()
    for slug in MODERN:
        path=SITE/'playgrounds'/slug/'index.html'
        page=replace_runtime(path.read_text(encoding='utf-8'),slug)
        path.write_text(page,encoding='utf-8')
    patch_release_identity()
    validate()
    print('Built deterministic v1.7.2 modern-parity release: 15 applets / 58 files / 15 active Quick Assigns')


if __name__=='__main__':
    build_site()
