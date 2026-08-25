#!/usr/bin/env python3
from __future__ import annotations

import html as html_lib
import re
from pathlib import Path

import build_site_v1_6_1_candidate as candidate

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"

ZH = {
    "QA-SEARCH-01": {
        "title": "A* 与 BFS：同一目标，不同搜索工作量",
        "focus": "比较同一迷宫中 A* 与 BFS 的路径质量、搜索工作量和前沿顺序。",
        "look": "优秀回答应区分搜索工作量与路径质量，把启发式与前沿排序联系起来，并避免声称 A* 总是更快。",
    },
    "QA-LOCAL-01": {
        "title": "为什么贪心局部搜索会卡住",
        "focus": "解释局部最优，并比较爬山法与模拟退火或重启等逃逸机制。",
        "look": "优秀回答应说明没有更优邻居并不等于全局最优，并正确解释退火或重启如何改变搜索行为。",
    },
    "QA-WUMPUS-01": {
        "title": "安全、危险还是未知？",
        "focus": "根据感知证据区分已证明安全、可能有危险和仍未确定的状态。",
        "look": "优秀回答应区分未知与危险、蕴含与可能性，并说明概率估计不能证明某格一定安全。",
    },
    "QA-SAT-01": {
        "title": "DPLL 下一步会做什么？",
        "focus": "把 CNF 结构与 DPLL 的传播、分支、冲突和剪枝联系起来。",
        "look": "优秀回答应指出实际的推理或分支证据；单个分支冲突只能剪去该分支，而全局 UNSAT 需要排除相关替代分支。",
    },
}


def bilingual(en: str, zh: str, *, block: bool = False) -> str:
    tag = "div" if block else "span"
    return (
        f'<{tag} class="qa-en">{html_lib.escape(en)}</{tag}>'
        f'<{tag} class="qa-zh">{html_lib.escape(zh)}</{tag}>'
    )


def quick_assign_style() -> str:
    return """<style id="quick-assign-support-i18n">
.qa-zh{display:none}
html[lang^="zh"] .qa-en{display:none!important}
html[lang^="zh"] .qa-zh{display:revert!important}
.quick-assign-support td strong{color:var(--fg,#172033)}
.quick-assign-support .qa-id{white-space:nowrap;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
</style>"""


def canonical_href(row: dict) -> str:
    return f'playgrounds/{row["slug"]}/index.html?mode=classroom#{row["anchor"]}'


def teacher_section(active: list[dict]) -> str:
    rows = []
    for row in active:
        z = ZH[row["id"]]
        rows.append(
            '<tr>'
            f'<td data-label="ID"><strong class="qa-id">{row["id"]}</strong></td>'
            f'<td data-label="Activity / 活动">{bilingual(row["title"], z["title"], block=True)}</td>'
            f'<td data-label="Time / 时间">10-15 min / 10-15 分钟</td>'
            f'<td data-label="Teacher look-for / 教师观察重点">{bilingual(row["teacher_look_for"], z["look"], block=True)}</td>'
            f'<td data-label="Link / 链接"><a href="{canonical_href(row)}">{bilingual("Open", "打开")}</a></td>'
            '</tr>'
        )
    return (
        '<section id="quick-assigns" class="quick-assign-support">'
        f'<h2>{bilingual("Level 1 - Quick Assigns", "Level 1 - 快速任务")}</h2>'
        f'<p>{bilingual("Quick Assigns reuse each applet’s existing Guided Challenge and local response packet. Students predict, run a bounded comparison, record evidence, explain the mechanism, and transfer the idea in about 10-15 minutes. Use the stable ID when assigning work.", "快速任务复用每个 applet 现有的引导挑战和本地作答包。学生先预测，再运行一个有边界的比较，记录证据，解释机制，并在约 10-15 分钟内完成迁移问题。布置作业时请使用稳定 ID。", block=True)}</p>'
        '<table><thead><tr>'
        f'<th>ID</th><th>{bilingual("Activity", "活动")}</th><th>{bilingual("Time", "时间")}</th><th>{bilingual("Teacher look-for", "教师观察重点")}</th><th>{bilingual("Student link", "学生链接")}</th>'
        '</tr></thead><tbody>' + ''.join(rows) + '</tbody></table>'
        f'<p>{bilingual("Level 2 remains the NN-1 and CNN-1 Activity Pack pilot. Level 3 is reserved for future lesson/unit packs and is not currently shipped.", "Level 2 仍是 NN-1 和 CNN-1 Activity Pack 试点。Level 3 预留给未来的课时或单元包，目前尚未发布。", block=True)}</p>'
        '</section>'
    )


def curriculum_section(active: list[dict]) -> str:
    rows = []
    for row in active:
        z = ZH[row["id"]]
        rows.append(
            '<tr>'
            f'<td data-label="ID"><strong class="qa-id">{row["id"]}</strong></td>'
            f'<td data-label="Applet"><a href="{canonical_href(row)}">{bilingual(row["title"], z["title"], block=True)}</a></td>'
            f'<td data-label="Focus / 重点">{bilingual(row["objective"], z["focus"], block=True)}</td>'
            f'<td data-label="Time / 时间">10-15 min / 10-15 分钟</td>'
            '</tr>'
        )
    return (
        '<section id="quick-assigns" class="quick-assign-support">'
        f'<h2>{bilingual("Beginning-of-course Quick Assigns", "学期初快速任务")}</h2>'
        f'<p>{bilingual("These Level-1 activities turn the existing in-applet response packets into stable, directly assignable 10-15 minute tasks. The link opens the applet in Use in class mode so the response packet is visible immediately.", "这些 Level 1 活动把 applet 内已有的作答包正式化为稳定、可直接布置的 10-15 分钟任务。链接会直接以“课堂使用”模式打开 applet，使作答包立即可见。", block=True)}</p>'
        '<table><thead><tr>'
        f'<th>ID</th><th>{bilingual("Activity", "活动")}</th><th>{bilingual("Focus", "重点")}</th><th>{bilingual("Time", "时间")}</th>'
        '</tr></thead><tbody>' + ''.join(rows) + '</tbody></table>'
        '</section>'
    )


def add_style(html: str) -> str:
    if 'id="quick-assign-support-i18n"' in html:
        return html
    if "</head>" not in html:
        raise RuntimeError("Support page lacks </head> for Quick Assign style")
    return html.replace("</head>", quick_assign_style() + "</head>", 1)


def patch_teacher(active: list[dict]) -> None:
    path = SITE / "teacher-pack.html"
    html = add_style(path.read_text(encoding="utf-8"))
    section = teacher_section(active)
    if 'id="quick-assigns"' in html:
        html, count = re.subn(r'<section id="quick-assigns"[^>]*>.*?</section>', section, html, count=1, flags=re.S)
        if count != 1:
            raise RuntimeError("Could not replace generated Teacher Pack Quick Assign section")
    else:
        marker = '<section id="activity-packs">'
        if marker not in html:
            marker = '<h2>Ready-to-assign Activity Packs</h2>'
        if marker not in html:
            raise RuntimeError("Could not place Teacher Pack Quick Assign section")
        html = html.replace(marker, section + marker, 1)
    path.write_text(html, encoding="utf-8")


def patch_curriculum(active: list[dict]) -> None:
    path = SITE / "curriculum.html"
    html = add_style(path.read_text(encoding="utf-8"))
    section = curriculum_section(active)
    if 'id="quick-assigns"' in html:
        html, count = re.subn(r'<section id="quick-assigns"[^>]*>.*?</section>', section, html, count=1, flags=re.S)
        if count != 1:
            raise RuntimeError("Could not replace Curriculum Quick Assign section")
    else:
        markers = (
            '<section><h2>Course and AIMA-aligned applet sequence</h2>',
            '<section><h2>Foundations / course-track sequence</h2>',
            '<section><h2>Applet map</h2>',
        )
        marker = next((m for m in markers if m in html), None)
        if marker is None:
            raise RuntimeError("Could not place Curriculum Quick Assign section")
        html = html.replace(marker, section + marker, 1)
    path.write_text(html, encoding="utf-8")


def patch_localized_select_containment() -> None:
    """Contain two existing selectors whose translated labels exceed phone width."""
    fixes = {
        SITE / "playgrounds" / "search-pathfinding" / "index.html": "#algoSel",
        SITE / "playgrounds" / "wumpus-world" / "index.html": "#strategySel",
    }
    for path, selector in fixes.items():
        html = path.read_text(encoding="utf-8")
        if 'id="v161-localized-select-containment"' in html:
            raise RuntimeError(f"Localized-select containment would be applied twice: {path}")
        css = (
            '<style id="v161-localized-select-containment">'
            '@media(max-width:640px){'
            f'{selector}' + '{width:100%!important;max-width:100%!important;min-width:0!important;}'
            '}'
            '</style>'
        )
        if "</head>" not in html:
            raise RuntimeError(f"Could not place mobile selector fix: {path}")
        html = html.replace("</head>", css + "</head>", 1)
        path.write_text(html, encoding="utf-8")


def validate_public_links(active: list[dict]) -> None:
    for page_name in ("teacher-pack.html", "curriculum.html"):
        html = (SITE / page_name).read_text(encoding="utf-8")
        if html.count('id="quick-assigns"') != 1:
            raise RuntimeError(f"{page_name} must contain exactly one Quick Assign section")
        if 'id="quick-assign-support-i18n"' not in html:
            raise RuntimeError(f"{page_name} lacks Quick Assign EN/ZH display scope")
        for row in active:
            canonical = canonical_href(row)
            legacy = f'playgrounds/{row["slug"]}/index.html#{row["anchor"]}'
            if canonical not in html:
                raise RuntimeError(f"{page_name} lacks canonical classroom-mode Quick Assign link for {row['id']}")
            if legacy in html:
                raise RuntimeError(f"{page_name} retains hidden-panel Quick Assign link for {row['id']}")
    for rel in ("playgrounds/search-pathfinding/index.html", "playgrounds/wumpus-world/index.html"):
        html = (SITE / rel).read_text(encoding="utf-8")
        if html.count('id="v161-localized-select-containment"') != 1:
            raise RuntimeError(f"{rel} lacks exactly one localized-selector containment rule")


def build_site() -> None:
    candidate.build_site()
    active = [row for row in candidate.registry() if row["status"] == "active"]
    patch_teacher(active)
    patch_curriculum(active)
    patch_localized_select_containment()
    validate_public_links(active)
    print("Built canonical v1.6.1 public candidate with bilingual support routes, classroom-mode Quick Assign deep links, and localized mobile control containment")


if __name__ == "__main__":
    build_site()
