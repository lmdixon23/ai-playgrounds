#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

import build_site as base
import build_site_v1_5_1 as v151
from build_minimax_alpha_beta_multilingual_candidate import build_candidate as build_lab15

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
RELEASE_VERSION = "1.6.0"
PREVIOUS_VERSION = "1.5.1"
EXPECTED_FILES = 58
EXPECTED_APPLETS = 15
EXPECTED_ACTIVITIES = {"index.html", "nn-1.html", "cnn-1.html"}
LAB15_SLUG = "minimax-alpha-beta"
LAB15_ENTRY = ROOT / "tools" / "applet_v1_6_lab15.json"
GENERATED_MANIFEST = ROOT / "release-evidence" / "applets-v1.6.json"


def release_manifest() -> list[dict[str, object]]:
    inherited = json.loads((ROOT / "tools" / "applets_v1_2.json").read_text(encoding="utf-8"))
    lab14 = json.loads((ROOT / "tools" / "applet_v1_3_lab14.json").read_text(encoding="utf-8"))
    lab15 = json.loads(LAB15_ENTRY.read_text(encoding="utf-8"))
    manifest = inherited + [lab14, lab15]
    slugs = [str(entry.get("slug")) for entry in manifest]
    if len(inherited) != 13 or inherited[-1].get("slug") != "transformer-language-model":
        raise RuntimeError("v1.6 must inherit the exact thirteen-app v1.2 inventory")
    if len(manifest) != 15 or len(set(slugs)) != 15:
        raise RuntimeError("v1.6 composition must contain exactly fifteen unique applets")
    if slugs[-2:] != ["agent-tool-context", LAB15_SLUG]:
        raise RuntimeError("v1.6 composition order must append Lab 15 after the fourteen-app v1.3 inventory")
    return manifest


def write_manifest() -> None:
    manifest = release_manifest()
    GENERATED_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    GENERATED_MANIFEST.write_text(payload, encoding="utf-8")
    (SITE / "applets.json").write_text(payload, encoding="utf-8")


def patch_lab15_public_shell() -> None:
    path = SITE / "playgrounds" / LAB15_SLUG / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    build_lab15(path)
    html = path.read_text(encoding="utf-8")
    if 'name="ai-playgrounds-version"' in html:
        raise RuntimeError("Lab 15 candidate unexpectedly already has public release provenance")
    html = html.replace(
        '<meta name="viewport" content="width=device-width,initial-scale=1">',
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<meta name="ai-playgrounds-version" content="1.6.0">\n'
        '<link rel="canonical" href="https://lmdixon23.github.io/ai-playgrounds/playgrounds/minimax-alpha-beta/">',
        1,
    )
    public_css = '''\n<style id="lab15-v16-public-shell">\n.lab15-public-nav{display:flex;align-items:center;justify-content:space-between;gap:12px;margin:0 0 10px;font-size:.84rem;color:var(--muted)}\n.lab15-public-nav a{font-weight:850;color:var(--accent);text-decoration:none}.lab15-public-nav a:hover{text-decoration:underline}\n@media(max-width:560px){.lab15-public-nav{flex-wrap:wrap}}\n</style>\n'''
    html = html.replace("</head>", public_css + "</head>", 1)
    nav = '<div class="lab15-public-nav" data-lab15-no-translate="true"><a href="../../">AI Playgrounds</a><span>v1.6.0</span></div>'
    if '<main class="shell">' not in html:
        raise RuntimeError("Lab 15 public shell could not locate main container")
    html = html.replace('<main class="shell">', '<main class="shell">' + nav, 1)
    html = html.replace("R6 · EN/ZH/VI/ES", "AI Playgrounds · v1.6.0", 1)
    path.write_text(html, encoding="utf-8")


def patch_landing() -> None:
    path = SITE / "index.html"
    html = path.read_text(encoding="utf-8")
    compact = json.dumps(release_manifest(), ensure_ascii=False, separators=(",", ":"))
    html, count = re.subn(
        r"const APPLETS=\[[\s\S]*?\];\nconst COPY=",
        "const APPLETS=" + compact + ";\nconst COPY=",
        html,
        count=1,
    )
    if count != 1:
        raise RuntimeError("Could not synchronize v1.6 landing manifest")
    replacements = {
        "AI Playgrounds | 14 interactive labs for learning artificial intelligence": "AI Playgrounds | 15 interactive labs for learning artificial intelligence",
        "Fourteen multilingual, offline-ready AI interactives": "Fifteen multilingual, offline-ready AI interactives",
        "Fourteen multilingual, single-file AI interactives": "Fifteen multilingual, single-file AI interactives",
        "fourteen multilingual AI labs": "fifteen multilingual AI labs",
        "fourteen multilingual interactives": "fifteen multilingual interactives",
        "Explore all fourteen": "Explore all fifteen",
        "Explore the fourteen applets": "Explore the fifteen applets",
        "14 inspectable applets": "15 inspectable applets",
        "十四个多语言交互工具": "十五个多语言交互工具",
        "探索全部十四个": "探索全部十五个",
        "探索十四个交互工具": "探索十五个交互工具",
        "14 个可检查的交互工具": "15 个可检查的交互工具",
        '"version": "1.5.1"': '"version": "1.6.0"',
        '<meta name="ai-playgrounds-version" content="1.5.1">': '<meta name="ai-playgrounds-version" content="1.6.0">',
        '<span class="site-version">v1.5.1</span>': '<span class="site-version">v1.6.0</span>',
        "twelve Foundations/course-track labs plus two Modern AI extensions": "thirteen Foundations/course-track labs plus two Modern AI extensions",
        "12 Foundations/course-track labs": "13 Foundations/course-track labs",
    }
    for old, new in replacements.items():
        html = html.replace(old, new)
    if LAB15_SLUG not in html or "15 interactive labs" not in html:
        raise RuntimeError("Landing v1.6 transformation did not complete")
    path.write_text(html, encoding="utf-8")


def patch_curriculum() -> None:
    path = SITE / "curriculum.html"
    html = path.read_text(encoding="utf-8")
    if f"playgrounds/{LAB15_SLUG}/index.html" not in html:
        row = (
            '<tr style="--applet-accent:#0d9488"><td data-label="#"><span class="order-dot">15</span></td>'
            '<td data-label="Applet"><a href="playgrounds/minimax-alpha-beta/index.html">Game Trees: Minimax and Alpha-Beta Pruning</a></td>'
            '<td data-label="Concept area">Adversarial search</td>'
            '<td data-label="Why here">Extend search to an opponent: back terminal utilities through alternating MIN/MAX nodes, then prune branches that cannot change the exact minimax result.</td></tr>'
        )
        html = html.replace("</tbody>", row + "</tbody>", 1)
    legend_anchor = '<span style="--legend:#0f766e"><i></i>Agent Tool Use and Context Protocols</span>'
    if legend_anchor in html and "Game Trees: Minimax and Alpha-Beta Pruning</span>" not in html:
        html = html.replace(legend_anchor, legend_anchor + '<span style="--legend:#0d9488"><i></i>Game Trees: Minimax and Alpha-Beta Pruning</span>', 1)
    replacements = {
        "fourteen": "fifteen",
        "Fourteen": "Fifteen",
        "twelve Foundations": "thirteen Foundations",
        "Twelve Foundations": "Thirteen Foundations",
    }
    for old, new in replacements.items():
        html = html.replace(old, new)
    if html.count('class="order-dot"') != 15:
        raise RuntimeError("Built v1.6 curriculum must contain exactly fifteen course rows")
    path.write_text(html, encoding="utf-8")


def patch_teacher_pack() -> None:
    path = SITE / "teacher-pack.html"
    html = path.read_text(encoding="utf-8")
    html = html.replace(
        "Fourteen multilingual AI applets: twelve Foundations/course-track labs plus two Modern AI extensions (Transformer Language Modeling and Agent Tool Use).",
        "Fifteen multilingual AI applets: thirteen Foundations/course-track labs plus two Modern AI extensions (Transformer Language Modeling and Agent Tool Use).",
    )
    html = html.replace(
        "The Foundations/course-track sequence contains twelve labs across search, logic, probability, machine learning, neural representation, vision, and reinforcement learning; two Modern AI extensions continue into Transformers and agent systems.",
        "The Foundations/course-track sequence contains thirteen labs across uninformed/informed search, adversarial search, logic, probability, machine learning, neural representation, vision, and reinforcement learning; two Modern AI extensions continue into Transformers and agent systems.",
    )
    # The older Teacher Pack table predated Labs 13-15. Complete it rather than merely changing the headline count.
    rows: list[str] = []
    if "playgrounds/transformer-language-model/index.html" not in html:
        rows.append('<tr><td><a href="playgrounds/transformer-language-model/index.html">Transformer Language Modeling</a></td><td>Modern NLP</td><td>35 min</td><td>Connect token representation, causal attention, logits, temperature, and next-token probabilities.</td><td>How does changing representation or attention state alter the next-token distribution?</td></tr>')
    if "playgrounds/agent-tool-context/index.html" not in html:
        rows.append('<tr><td><a href="playgrounds/agent-tool-context/index.html">Agent Tool Use and Context Protocols</a></td><td>Modern AI systems</td><td>35 min</td><td>Separate proposed actions, validation, authorization, execution, observations, context updates, and stopping.</td><td>Why is a valid tool call not automatically an authorized or correct action?</td></tr>')
    if f"playgrounds/{LAB15_SLUG}/index.html" not in html:
        rows.append('<tr><td><a href="playgrounds/minimax-alpha-beta/index.html">Game Trees: Minimax and Alpha-Beta Pruning</a></td><td>Adversarial search</td><td>30 min</td><td>Back terminal utilities through alternating MIN/MAX nodes and compare full minimax with safe alpha-beta pruning.</td><td>How can Alpha-Beta skip branches without changing the exact minimax decision?</td></tr>')
    if rows:
        html = html.replace("</tbody>", "".join(rows) + "</tbody>", 1)
    path.write_text(html, encoding="utf-8")


def patch_quality() -> None:
    path = SITE / "quality.html"
    html = path.read_text(encoding="utf-8")
    html = html.replace("Fourteen multilingual, offline-ready applets", "Fifteen multilingual, offline-ready applets")
    html = html.replace("fourteen applets", "fifteen applets")
    html = html.replace("14 applets", "15 applets")
    path.write_text(html, encoding="utf-8")


def update_release_provenance() -> None:
    for path in sorted((SITE / "playgrounds").glob("*/index.html")):
        html = path.read_text(encoding="utf-8")
        if path.parent.name == LAB15_SLUG:
            if 'name="ai-playgrounds-version" content="1.6.0"' not in html:
                raise RuntimeError("Lab 15 public provenance is missing")
        else:
            html = html.replace(
                'name="ai-playgrounds-version" content="1.5.1"',
                'name="ai-playgrounds-version" content="1.6.0"',
                1,
            )
            html = html.replace("AI Playgrounds · v1.5.1", "AI Playgrounds · v1.6.0")
            html = html.replace(">v1.5.1<", ">v1.6.0<")
        path.write_text(html, encoding="utf-8")
    old = 'data-v14-support-version="true">AI Playgrounds · v1.5.1'
    new = 'data-v14-support-version="true">AI Playgrounds · v1.6.0'
    for path in sorted(SITE.glob("*.html")):
        html = path.read_text(encoding="utf-8")
        if old in html:
            path.write_text(html.replace(old, new), encoding="utf-8")


def add_release_banner() -> None:
    path = SITE / "release-notes.html"
    html = path.read_text(encoding="utf-8")
    if "release-v1-6-0" in html:
        return
    marker = '<section id="release-v1-5-1"'
    if marker not in html:
        raise RuntimeError("Could not locate v1.5.1 public release banner")
    banner = (
        '<section id="release-v1-6-0" style="margin:1rem 0;padding:1rem 1.2rem;border:1px solid currentColor;border-radius:12px">'
        '<h2><span class="v14-release-en">AI Playgrounds v1.6.0: Game Trees, Minimax, and Alpha-Beta Pruning.</span><span class="v14-release-zh">AI Playgrounds v1.6.0：博弈树、Minimax 与 Alpha-Beta 剪枝。</span></h2>'
        '<p><span class="v14-release-en">Adds the fifteenth lab and thirteenth Foundations lab: a deterministic adversarial-search playground for MIN/MAX backup, exact alpha-beta cutoffs, move-order work comparisons, and prediction-before-reveal challenges.</span><span class="v14-release-zh">新增第十五个实验、也是第十三个基础课程实验：用确定性博弈树展示 MIN/MAX 回传、精确的 Alpha-Beta 截断、行动顺序对工作量的影响以及先预测后揭示挑战。</span></p>'
        '</section>'
    )
    path.write_text(html.replace(marker, banner + marker, 1), encoding="utf-8")


def update_sitemap() -> None:
    path = SITE / "sitemap.xml"
    xml = path.read_text(encoding="utf-8")
    route = "playgrounds/minimax-alpha-beta/"
    if route not in xml:
        entry = f'  <url><loc>https://lmdixon23.github.io/ai-playgrounds/{route}</loc></url>\n'
        if "</urlset>" not in xml:
            raise RuntimeError("Could not locate sitemap urlset boundary")
        xml = xml.replace("</urlset>", entry + "</urlset>", 1)
    path.write_text(xml, encoding="utf-8")


def upgrade_analytics() -> None:
    pages = sorted(path for path in SITE.rglob("*.html") if path.is_file())
    for path in pages:
        html = path.read_text(encoding="utf-8")
        html = v151.ANALYTICS_RE.sub("\n", html, count=1)
        if 'data-ai-playgrounds-analytics="v1.5.1"' in html or 'data-ai-playgrounds-analytics="v1.6.0"' in html:
            raise RuntimeError(f"Analytics v1.6 would be applied twice: {path.relative_to(SITE)}")
        kind, slug = v151.page_identity(path)
        block = v151.analytics_block(kind, slug).replace(
            'data-ai-playgrounds-analytics="v1.5.1"',
            'data-ai-playgrounds-analytics="v1.6.0"',
            1,
        )
        html = v151.insert_before_last(html, "</body>", block)
        path.write_text(html, encoding="utf-8")


def build_site() -> None:
    v151.build_site()
    v151.validate_boundary()
    patch_lab15_public_shell()
    write_manifest()
    patch_landing()
    patch_curriculum()
    patch_teacher_pack()
    patch_quality()
    update_release_provenance()
    add_release_banner()
    update_sitemap()
    upgrade_analytics()


def validate_boundary() -> None:
    base.validate_local_references()
    files = sorted(path for path in SITE.rglob("*") if path.is_file())
    if len(files) != EXPECTED_FILES:
        raise RuntimeError(f"Expected {EXPECTED_FILES} v1.6 files, found {len(files)}")
    applets = sorted((SITE / "playgrounds").glob("*/index.html"))
    if len(applets) != EXPECTED_APPLETS:
        raise RuntimeError(f"Expected {EXPECTED_APPLETS} applets, found {len(applets)}")
    if {p.parent.name for p in applets} != {str(x["slug"]) for x in release_manifest()}:
        raise RuntimeError("v1.6 deployed applet set does not match its release manifest")
    activities = {p.name for p in (SITE / "activities").glob("*.html")}
    if activities != EXPECTED_ACTIVITIES:
        raise RuntimeError(f"v1.6 Activity Pack boundary changed: {sorted(activities)}")

    for path in sorted(SITE.rglob("*.html")):
        source = path.read_text(encoding="utf-8")
        if source.count('data-ai-playgrounds-analytics="v1.6.0"') != 1:
            raise RuntimeError(f"v1.6 analytics coverage mismatch: {path.relative_to(SITE)}")
        if v151.ANALYTICS_COMMENT not in source:
            raise RuntimeError(f"analytics privacy marker missing: {path.relative_to(SITE)}")

    lab15 = SITE / "playgrounds" / LAB15_SLUG / "index.html"
    source = lab15.read_text(encoding="utf-8")
    if source.count("function minimax(") != 1 or source.count("function alphaBeta(") != 1:
        raise RuntimeError("Public Lab 15 must preserve exactly one minimax and one alpha-beta implementation")
    if any(token in source for token in ("fetch(", "XMLHttpRequest", "WebSocket", "EventSource", "<script src=")):
        raise RuntimeError("Public Lab 15 must remain self-contained/offline")
    for marker in ("window.Lab15Prototype", "window.Lab15Localization", "R6-Multilingual", 'name="ai-playgrounds-version" content="1.6.0"'):
        if marker not in source:
            raise RuntimeError(f"Public Lab 15 missing required marker: {marker}")

    landing = (SITE / "index.html").read_text(encoding="utf-8")
    curriculum = (SITE / "curriculum.html").read_text(encoding="utf-8")
    teacher = (SITE / "teacher-pack.html").read_text(encoding="utf-8")
    if "15 interactive labs" not in landing or LAB15_SLUG not in landing:
        raise RuntimeError("v1.6 landing integration is incomplete")
    if curriculum.count('class="order-dot"') != 15 or LAB15_SLUG not in curriculum:
        raise RuntimeError("v1.6 curriculum integration is incomplete")
    if "thirteen Foundations/course-track labs" not in teacher or LAB15_SLUG not in teacher:
        raise RuntimeError("v1.6 Teacher Pack integration is incomplete")
    if "release-v1-6-0" not in (SITE / "release-notes.html").read_text(encoding="utf-8"):
        raise RuntimeError("v1.6 public release banner is missing")


def main() -> None:
    build_site()
    validate_boundary()
    print(f"Built v1.6 candidate: {EXPECTED_FILES} files / {EXPECTED_APPLETS} applets / {len(EXPECTED_ACTIVITIES)} activity pages")
    print("v1.6 public deployment boundary: PASS")


if __name__ == "__main__":
    main()
