#!/usr/bin/env python3
from __future__ import annotations

import re
import shutil
from pathlib import Path

import build_site as base
import build_site_v1_5 as v15

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
RELEASE_VERSION = "1.5.1"
PREVIOUS_VERSION = "1.5.0"
EXPECTED_FILES = 57
EXPECTED_APPLETS = 14
EXPECTED_ACTIVITIES = {"index.html", "nn-1.html", "cnn-1.html"}

ANALYTICS_COMMENT = "<!-- AI Playgrounds aggregate analytics: canonical host only; no cookies; no third-party script; DNT/GPC and opt-out respected. -->"
ANALYTICS_RE = re.compile(
    r"\s*<!-- AI Playgrounds aggregate analytics: canonical host only; no cookies; no third-party script; DNT/GPC and opt-out respected\. -->\s*"
    r"<script>\s*\(function \(\) \{.*?window\.aiPlaygroundsAnalytics.*?</script>\s*",
    re.S,
)


def insert_before_last(html: str, marker: str, fragment: str) -> str:
    index = html.rfind(marker)
    if index < 0:
        raise RuntimeError(f"Could not locate final {marker!r} marker")
    return html[:index] + fragment + html[index:]


def page_identity(path: Path) -> tuple[str, str]:
    rel = path.relative_to(SITE).as_posix()
    if rel == "index.html":
        return "landing", "index"
    if rel.startswith("playgrounds/"):
        return "applet", path.parent.name
    if rel.startswith("activities/"):
        return "activity", path.stem if path.name != "index.html" else "activities"
    if rel == "tests/index.html":
        return "tests", "tests"
    return "support", path.stem


def analytics_block(kind: str, slug: str) -> str:
    return f'''\n{ANALYTICS_COMMENT}\n<script data-ai-playgrounds-analytics="v1.5.1">\n(function () {{\n  'use strict';\n  var CANONICAL_HOST = 'lmdixon23.github.io';\n  var ENDPOINT = 'https://lmdixon23.goatcounter.com/count';\n  var PAGE_KIND = {kind!r};\n  var PAGE_SLUG = {slug!r};\n  var SOURCE_ALLOWLIST = new Set(['hn','linkedin','csta','sigcse','oercommons','merlot','reddit','bluesky','mastodon','devto','hashnode','github','email','school','portfolio','resume','zenodo','jose']);\n  var liveImages = [];\n\n  function storageGet(storage, key) {{ try {{ return storage.getItem(key); }} catch (_) {{ return null; }} }}\n  function storageSet(storage, key, value) {{ try {{ storage.setItem(key, value); }} catch (_) {{}} }}\n  function privacySignal() {{\n    return navigator.globalPrivacyControl === true || navigator.doNotTrack === '1' ||\n      navigator.doNotTrack === 'yes' || window.doNotTrack === '1';\n  }}\n  function clean(value) {{\n    return String(value || '').toLowerCase().replace(/[^a-z0-9._/-]+/g, '-').replace(/-+/g, '-').replace(/^\\/+|\\/+$/g, '').slice(0, 80);\n  }}\n  function normalizePath(path) {{\n    var value = String(path || '/');\n    value = value.replace(/\\/index\\.html$/, '/');\n    if (value === '/ai-playgrounds') value = '/ai-playgrounds/';\n    return value || '/';\n  }}\n  function canonicalPath() {{\n    var link = document.querySelector('link[rel="canonical"]');\n    if (link && link.href) {{\n      try {{ return normalizePath(new URL(link.href, location.href).pathname); }} catch (_) {{}}\n    }}\n    return normalizePath(location.pathname || '/ai-playgrounds/');\n  }}\n\n  var params = new URLSearchParams(location.search);\n  var optedOut = params.get('analytics') === 'off' || storageGet(localStorage, 'ai-playgrounds-analytics') === 'off';\n  var enabled = location.hostname === CANONICAL_HOST && !privacySignal() && !optedOut;\n\n  function transmit(query) {{\n    if (!enabled) return;\n    var img = new Image(1, 1);\n    img.referrerPolicy = 'no-referrer';\n    img.onload = img.onerror = function () {{\n      var i = liveImages.indexOf(img);\n      if (i >= 0) liveImages.splice(i, 1);\n    }};\n    img.src = ENDPOINT + '?' + query.toString();\n    liveImages.push(img);\n  }}\n\n  function campaignQuery() {{\n    var source = clean(params.get('ap_src'));\n    if (!SOURCE_ALLOWLIST.has(source)) return '';\n    var q = new URLSearchParams();\n    q.set('utm_campaign', 'ai-playgrounds');\n    q.set('utm_source', source);\n    return q.toString();\n  }}\n\n  function sendPage() {{\n    var query = new URLSearchParams();\n    query.set('p', canonicalPath());\n    query.set('t', document.title || 'AI Playgrounds');\n    var campaign = campaignQuery();\n    if (campaign) query.set('q', campaign);\n    transmit(query);\n  }}\n\n  function sendEvent(name, title) {{\n    var eventName = clean(name);\n    if (!eventName) return;\n    var query = new URLSearchParams();\n    query.set('p', 'event/' + eventName);\n    query.set('t', title || ('AI Playgrounds event: ' + eventName));\n    query.set('e', '1');\n    transmit(query);\n  }}\n\n  window.aiPlaygroundsAnalytics = {{\n    enabled: enabled,\n    optOut: function () {{ storageSet(localStorage, 'ai-playgrounds-analytics', 'off'); location.reload(); }},\n    optIn: function () {{ storageSet(localStorage, 'ai-playgrounds-analytics', 'on'); location.reload(); }},\n    count: function (name, title) {{ sendEvent(name, title); }}\n  }};\n\n  document.addEventListener('click', function (event) {{\n    var out = event.target.closest('#analytics-opt-out');\n    var inn = event.target.closest('#analytics-opt-in');\n    if (out) {{ event.preventDefault(); window.aiPlaygroundsAnalytics.optOut(); return; }}\n    if (inn) {{ event.preventDefault(); window.aiPlaygroundsAnalytics.optIn(); return; }}\n    if (!enabled) return;\n\n    var link = event.target.closest('a[href]');\n    if (link) {{\n      var href = link.getAttribute('href') || '';\n      var app = href.match(/playgrounds\\/([^/?#]+)\\/?/i);\n      if (app) sendEvent('launch/' + clean(app[1]), 'Launch applet: ' + clean(app[1]));\n      else if (/\\.(pdf|zip|md|docx?|pptx?|csv)(?:[?#]|$)/i.test(href)) sendEvent('resource/' + clean((href.split('/').pop() || 'download').split(/[?#]/)[0]), 'Resource download');\n      else if (/github\\.com\\/lmdixon23\\/ai-playgrounds/i.test(href)) sendEvent('outbound/github', 'Open AI Playgrounds on GitHub');\n    }}\n\n    if (PAGE_KIND === 'applet') {{\n      var control = event.target.closest('main button, main [role="button"], .workspace button, .controls button');\n      if (control && !control.closest('header, nav, footer, .toolbar')) {{\n        var key = 'ai-playgrounds-engaged-' + PAGE_SLUG;\n        if (storageGet(sessionStorage, key) !== '1') {{\n          storageSet(sessionStorage, key, '1');\n          sendEvent('engaged/' + clean(PAGE_SLUG), 'First substantive applet interaction: ' + clean(PAGE_SLUG));\n        }}\n      }}\n    }}\n  }}, true);\n\n  if (!enabled) return;\n  sendPage();\n}})();\n</script>\n'''


def upgrade_analytics() -> None:
    pages = sorted(path for path in SITE.rglob("*.html") if path.is_file())
    for path in pages:
        html = path.read_text(encoding="utf-8")
        html = ANALYTICS_RE.sub("\n", html, count=1)
        if 'data-ai-playgrounds-analytics="v1.5.1"' in html:
            raise RuntimeError(f"Analytics v1.5.1 would be applied twice: {path.relative_to(SITE)}")
        kind, slug = page_identity(path)
        html = insert_before_last(html, "</body>", analytics_block(kind, slug))
        path.write_text(html, encoding="utf-8")


def patch_knn_touch_recovery() -> None:
    path = SITE / "playgrounds" / "knn-classifier" / "index.html"
    html = path.read_text(encoding="utf-8")
    old = '''  cv.addEventListener('click', e => {\n    const {x, y} = canvasCoords(e);\n    if (guided.active) {\n      if (guided.locked) return;\n      guided.query = {x, y};\n      guided.predictedNeighbors.clear();\n      guided.revealed = false; guided.actual = null;\n      updateGuidedUI(); render();\n      return;\n    }\n    points.push({x, y, c: addClass});\n    render();\n  });'''
    new = '''  // v1.5.1 touch recovery: once a Guided Challenge query exists, a near-miss\n  // around a training point selects that point instead of unexpectedly moving the\n  // query and clearing the learner's prediction. Distances are measured in CSS\n  // pixels so the tolerance stays usable as the SVG scales on phones.\n  cv.addEventListener('click', e => {\n    const {x, y} = canvasCoords(e);\n    if (guided.active) {\n      if (guided.locked) return;\n      if (guided.query) {\n        const rect = cv.getBoundingClientRect();\n        let nearest = null;\n        points.forEach((p, idx) => {\n          const dx = (p.x - x) * rect.width / cv.width;\n          const dy = (p.y - y) * rect.height / cv.height;\n          const distance = Math.hypot(dx, dy);\n          if (!nearest || distance < nearest.distance) nearest = {idx, distance};\n        });\n        if (nearest && nearest.distance <= 22) {\n          handleGuidedNeighbor(nearest.idx);\n          return;\n        }\n      }\n      guided.query = {x, y};\n      guided.predictedNeighbors.clear();\n      guided.revealed = false; guided.actual = null;\n      updateGuidedUI(); render();\n      return;\n    }\n    points.push({x, y, c: addClass});\n    render();\n  });'''
    if old not in html:
        raise RuntimeError("Could not locate KNN Guided Challenge canvas click handler")
    html = html.replace(old, new, 1)
    path.write_text(html, encoding="utf-8")


def patch_bayes_mobile_methods() -> None:
    path = SITE / "playgrounds" / "bayes-network" / "index.html"
    html = path.read_text(encoding="utf-8")
    if "v151-bayes-mobile-methods" in html:
        raise RuntimeError("Bayesian responsive fix would be applied twice")
    css = '''\n<style id="v151-bayes-mobile-methods">\n@media (max-width: 640px) {\n  .control-row .method-tabs {\n    flex: 1 1 100%;\n    width: 100%;\n    display: grid;\n    grid-template-columns: repeat(2, minmax(0, 1fr));\n    overflow: visible;\n  }\n  .control-row .method-tabs button {\n    min-width: 0;\n    white-space: normal;\n    line-height: 1.25;\n    border-right: 1px solid var(--border);\n    border-bottom: 1px solid var(--border);\n  }\n  .control-row .method-tabs button:nth-child(2n) { border-right: 0; }\n  .control-row .method-tabs button:nth-last-child(-n+2) { border-bottom: 0; }\n}\n</style>\n'''
    html = html.replace("</head>", css + "</head>", 1)
    path.write_text(html, encoding="utf-8")


def patch_neural_network_landscape() -> None:
    path = SITE / "playgrounds" / "neural-network" / "index.html"
    html = path.read_text(encoding="utf-8")
    if "v151-neural-transport-reflow" in html:
        raise RuntimeError("Neural Network transport fix would be applied twice")
    css = '''\n<style id="v151-neural-transport-reflow">\n@media (max-width: 900px) {\n  #nnScrubGroup {\n    min-width: 0 !important;\n    flex: 1 1 100% !important;\n    flex-wrap: wrap !important;\n  }\n  #nnScrub { min-width: 120px !important; flex: 1 1 180px !important; }\n  #nnLive { white-space: normal; }\n}\n</style>\n'''
    html = html.replace("</head>", css + "</head>", 1)
    path.write_text(html, encoding="utf-8")


def copy_activity_packs() -> None:
    source_dir = ROOT / "activities"
    target_dir = SITE / "activities"
    target_dir.mkdir(parents=True, exist_ok=True)
    for name in sorted(EXPECTED_ACTIVITIES):
        src = source_dir / name
        if not src.is_file():
            raise RuntimeError(f"Missing activity source: {src}")
        shutil.copy2(src, target_dir / name)


def patch_landing_metadata() -> None:
    """Bind to the exact generated v1.5 landing contract, not stale source copy."""
    path = SITE / "index.html"
    html = path.read_text(encoding="utf-8")
    inherited = {
        "<title>AI Playgrounds | Fourteen interactive AI labs</title>",
        "Fourteen multilingual, offline-ready AI interactives for search, logic, probability, machine learning, neural networks, computer vision, reinforcement learning, Transformer language modeling, and agent tool use.",
        "Fourteen multilingual, single-file AI interactives built for classroom use and independent exploration.",
        "AI Playgrounds: fourteen multilingual AI labs from foundations to modern extensions",
        '"description":"Fourteen multilingual, offline-ready AI labs spanning foundations and modern extensions."',
        '"inLanguage":["en","zh","vi","es"]',
    }
    missing = sorted(marker for marker in inherited if marker not in html)
    if missing:
        raise RuntimeError(f"Inherited v1.5 landing metadata contract changed: {missing}")
    html = html.replace(
        "<title>AI Playgrounds | Fourteen interactive AI labs</title>",
        "<title>AI Playgrounds | 14 interactive labs for learning artificial intelligence</title>",
        1,
    )
    path.write_text(html, encoding="utf-8")


def patch_teacher_and_quality_copy() -> None:
    teacher = SITE / "teacher-pack.html"
    html = teacher.read_text(encoding="utf-8")
    html = html.replace(
        "Twelve bilingual, single-file AI applets for search, logic, probability, machine learning, vision, and reinforcement learning.",
        "Fourteen multilingual AI applets: twelve Foundations/course-track labs plus two Modern AI extensions (Transformer Language Modeling and Agent Tool Use).",
    )
    html = html.replace(
        "The full sequence follows search, logic, probability, machine learning, neural representation, vision, and reinforcement learning.",
        "The Foundations/course-track sequence contains twelve labs across search, logic, probability, machine learning, neural representation, vision, and reinforcement learning; two Modern AI extensions continue into Transformers and agent systems.",
    )
    activity_section = '''\n<section id="activity-packs">\n<h2>Ready-to-assign Activity Packs</h2>\n<p>Two pilot student activities turn the applets into assignable inquiry labs. Responses stay in the learner's browser; the pages can also be printed. Teacher answer keys are intentionally not published on the student site.</p>\n<div class="quick-grid">\n<div><h3>NN-1 · Make it fail, then make it learn</h3><p>Neural-network capacity, non-linearity, training, and generalization. About 35–45 minutes.</p><p><a class="button" href="activities/nn-1.html">Open NN-1</a></p></div>\n<div><h3>CNN-1 · Be the filter</h3><p>Convolution arithmetic, edge direction, learned filters, and pooling. About 40–50 minutes.</p><p><a class="button" href="activities/cnn-1.html">Open CNN-1</a></p></div>\n</div>\n</section>\n'''
    marker = "<section>\n<h2>Quick-entry four-app sampler</h2>"
    if marker not in html:
        raise RuntimeError("Could not locate Teacher Pack sampler boundary")
    html = html.replace(marker, activity_section + marker, 1)
    teacher.write_text(html, encoding="utf-8")

    quality = SITE / "quality.html"
    q = quality.read_text(encoding="utf-8")
    q = q.replace("Twelve fully bilingual, offline-ready applets", "Fourteen multilingual, offline-ready applets")
    quality.write_text(q, encoding="utf-8")


def add_activity_links_to_applets() -> None:
    for slug, activity_id, label in (
        ("neural-network", "nn-1", "NN-1 · Core activity"),
        ("convolution", "cnn-1", "CNN-1 · Core activity"),
    ):
        path = SITE / "playgrounds" / slug / "index.html"
        html = path.read_text(encoding="utf-8")
        if f"data-v151-activity-link=\"{activity_id}\"" in html:
            continue
        fragment = (
            f'<p data-v151-activity-link="{activity_id}" style="margin:.5rem 0 0;font-size:.85rem">'
            f'<a href="../../activities/{activity_id}.html" style="font-weight:750">📄 {label}</a>'
            f' <span style="color:var(--muted)">· printable, locally autosaved student worksheet</span></p>'
        )
        marker = "</header>"
        if marker not in html:
            raise RuntimeError(f"Could not locate applet header for activity link: {slug}")
        html = html.replace(marker, fragment + marker, 1)
        path.write_text(html, encoding="utf-8")


def update_release_provenance() -> None:
    for path in sorted((SITE / "playgrounds").glob("*/index.html")):
        html = path.read_text(encoding="utf-8")
        html = html.replace(
            f'name="ai-playgrounds-version" content="{PREVIOUS_VERSION}"',
            f'name="ai-playgrounds-version" content="{RELEASE_VERSION}"',
            1,
        )
        html = html.replace(f"AI Playgrounds · v{PREVIOUS_VERSION}", f"AI Playgrounds · v{RELEASE_VERSION}")
        html = html.replace(f">v{PREVIOUS_VERSION}<", f">v{RELEASE_VERSION}<")
        if f'name="ai-playgrounds-version" content="{RELEASE_VERSION}"' not in html:
            raise RuntimeError(f"Missing v1.5.1 applet metadata: {path.parent.name}")
        path.write_text(html, encoding="utf-8")

    landing = SITE / "index.html"
    html = landing.read_text(encoding="utf-8")
    html = html.replace('"version": "1.5.0"', '"version": "1.5.1"', 1)
    html = html.replace('<meta name="ai-playgrounds-version" content="1.5.0">', '<meta name="ai-playgrounds-version" content="1.5.1">', 1)
    html = html.replace('<span class="site-version">v1.5.0</span>', '<span class="site-version">v1.5.1</span>', 1)
    landing.write_text(html, encoding="utf-8")

    old = 'data-v14-support-version="true">AI Playgrounds · v1.5.0'
    new = 'data-v14-support-version="true">AI Playgrounds · v1.5.1'
    for path in sorted(SITE.glob("*.html")):
        if path.name == "index.html":
            continue
        html = path.read_text(encoding="utf-8")
        if old in html:
            path.write_text(html.replace(old, new), encoding="utf-8")


def add_release_banner() -> None:
    path = SITE / "release-notes.html"
    html = path.read_text(encoding="utf-8")
    if "release-v1-5-1" in html:
        return
    marker = '<section id="release-v1-5-0"'
    if marker not in html:
        raise RuntimeError("Could not locate v1.5 public release banner")
    banner = (
        '<section id="release-v1-5-1" style="margin:1rem 0;padding:1rem 1.2rem;border:1px solid currentColor;border-radius:12px">'
        '<h2><span class="v14-release-en">AI Playgrounds v1.5.1, HCI and adoption hardening.</span><span class="v14-release-zh">AI Playgrounds v1.5.1：HCI 与教学采用加固。</span></h2>'
        '<p><span class="v14-release-en">Corrects analytics coverage and event/campaign semantics, hardens KNN touch recovery plus Bayesian/Neural responsive behavior, refreshes fourteen-lab product copy, and pilots two ready-to-assign Activity Packs without changing any applet algorithm.</span><span class="v14-release-zh">修正分析覆盖和事件/活动语义，加强 KNN 触控恢复以及贝叶斯网络/神经网络的响应式布局，更新十四个实验的产品说明，并试点两个可直接布置的活动包；不改变任何 applet 算法。</span></p>'
        '</section>'
    )
    path.write_text(html.replace(marker, banner + marker, 1), encoding="utf-8")


def update_sitemap() -> None:
    path = SITE / "sitemap.xml"
    xml = path.read_text(encoding="utf-8")
    if "/activities/nn-1.html" in xml:
        return
    urls = "".join(
        f"  <url><loc>https://lmdixon23.github.io/ai-playgrounds/{suffix}</loc></url>\n"
        for suffix in ("activities/", "activities/nn-1.html", "activities/cnn-1.html")
    )
    if "</urlset>" not in xml:
        raise RuntimeError("Could not locate sitemap urlset boundary")
    path.write_text(xml.replace("</urlset>", urls + "</urlset>", 1), encoding="utf-8")


def build_site() -> None:
    v15.build_site()
    v15.validate_boundary()
    copy_activity_packs()
    patch_knn_touch_recovery()
    patch_bayes_mobile_methods()
    patch_neural_network_landscape()
    patch_landing_metadata()
    patch_teacher_and_quality_copy()
    add_activity_links_to_applets()
    update_release_provenance()
    add_release_banner()
    update_sitemap()
    upgrade_analytics()


def validate_boundary() -> None:
    base.validate_local_references()
    files = sorted(path for path in SITE.rglob("*") if path.is_file())
    if len(files) != EXPECTED_FILES:
        raise RuntimeError(f"Expected {EXPECTED_FILES} v1.5.1 files, found {len(files)}")

    applets = sorted((SITE / "playgrounds").glob("*/index.html"))
    if len(applets) != EXPECTED_APPLETS:
        raise RuntimeError(f"Expected {EXPECTED_APPLETS} applets, found {len(applets)}")

    activity_names = {p.name for p in (SITE / "activities").glob("*.html")}
    if activity_names != EXPECTED_ACTIVITIES:
        raise RuntimeError(f"Activity Pack boundary mismatch: {sorted(activity_names)}")

    html_pages = sorted(path for path in SITE.rglob("*.html") if path.is_file())
    for path in html_pages:
        source = path.read_text(encoding="utf-8")
        if source.count('data-ai-playgrounds-analytics="v1.5.1"') != 1:
            raise RuntimeError(f"Analytics coverage mismatch: {path.relative_to(SITE)}")
        if ANALYTICS_COMMENT not in source:
            raise RuntimeError(f"Analytics privacy marker missing: {path.relative_to(SITE)}")

    markers = {
        "knn-classifier": "v1.5.1 touch recovery",
        "bayes-network": "v151-bayes-mobile-methods",
        "neural-network": "v151-neural-transport-reflow",
    }
    for slug, marker in markers.items():
        source = (SITE / "playgrounds" / slug / "index.html").read_text(encoding="utf-8")
        if marker not in source:
            raise RuntimeError(f"Missing v1.5.1 HCI marker for {slug}")

    landing = (SITE / "index.html").read_text(encoding="utf-8")
    if "14 interactive labs" not in landing or "Fourteen multilingual" not in landing:
        raise RuntimeError("Landing product metadata is not fourteen-lab/multilingual aware")
    if "release-v1-5-1" not in (SITE / "release-notes.html").read_text(encoding="utf-8"):
        raise RuntimeError("Public release notes lack v1.5.1 banner")


def main() -> None:
    build_site()
    validate_boundary()
    print(f"Built v1.5.1 HCI/adoption candidate: {EXPECTED_FILES} files / {EXPECTED_APPLETS} applets / {len(EXPECTED_ACTIVITIES)} activity pages")
    print("v1.5.1 HCI/adoption deployment boundary: PASS")


if __name__ == "__main__":
    main()
