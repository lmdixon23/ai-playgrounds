#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

import build_site_v1_6_public as v16

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
REGISTRY = ROOT / "tools" / "quick_assigns_v1.json"
EXPECTED_FILES = 58
EXPECTED_APPLETS = 15
EXPECTED_FOUNDATIONS = 13

ACTIVE_COPY = {
    "QA-SEARCH-01": {
        "vi": {
            "summary": "🧪 Bài tập nhanh · QA-SEARCH-01 · 10–15 phút",
            "title": "A* và BFS: cùng mục tiêu, khác lượng công việc",
            "intro": "Dự đoán thuật toán tìm kiếm nào sẽ làm ít việc hơn, chạy phép so sánh rồi giải thích cách frontier và heuristic làm thay đổi quá trình tìm kiếm.",
            "predict": "Trước khi chạy, thuật toán nào sẽ thăm ít ô hơn trong mê cung này, và vì sao?",
            "observe": "Chạy ít nhất hai thuật toán. Ghi lại độ dài đường đi, số nút đã thăm và một mẫu frontier nhìn thấy được.",
            "explain": "Heuristic đã thay đổi điều gì trong quá trình tìm kiếm?",
            "transfer": "Khi nào BFS sẽ an toàn hơn greedy best-first search hoặc weighted A*?",
        },
        "es": {
            "summary": "🧪 Tarea rápida · QA-SEARCH-01 · 10–15 min",
            "title": "A* frente a BFS: mismo objetivo, distinto trabajo",
            "intro": "Predice qué búsqueda hará menos trabajo, ejecuta una comparación y explica cómo la frontera y la heurística cambiaron el proceso.",
            "predict": "Antes de ejecutar, ¿qué algoritmo visitará menos celdas en este laberinto y por qué?",
            "observe": "Ejecuta al menos dos algoritmos. Registra la longitud de la ruta, los nodos visitados y un patrón visible de la frontera.",
            "explain": "¿Qué cambió la heurística en el proceso de búsqueda?",
            "transfer": "¿Cuándo sería BFS una opción más segura que greedy best-first search o weighted A*?",
        },
    },
    "QA-LOCAL-01": {
        "vi": {
            "summary": "🧪 Bài tập nhanh · QA-LOCAL-01 · 10–15 phút",
            "title": "Vì sao tìm kiếm cục bộ bị mắc kẹt hoặc thoát ra",
            "intro": "Chạy một quỹ đạo tìm kiếm cục bộ hoặc benchmark khởi động lại có hạt giống và được ghép cặp, rồi giải thích vì sao thuật toán bị mắc kẹt, thoát ra hoặc thành công ổn định.",
            "predict": "Trước khi chạy, bạn dự đoán chiến lược nào thành công ổn định nhất và chiến lược nào đạt chi phí thấp nhất? Vì sao hai kết quả có thể khác nhau?",
            "observe": "Chạy một lần tìm kiếm hoặc benchmark khởi động lại lặp lại. Ghi lại bài toán, thuật toán, tỷ lệ thành công, chi phí cuối trung bình và chi phí tốt nhất trung bình phù hợp.",
            "explain": "Quy tắc tìm kiếm chọn bước đi như thế nào, và vì sao tần suất thành công cùng chi phí trung bình có thể xếp hạng thuật toán khác nhau?",
            "transfer": "Loại bài toán tối ưu nào cần khởi động lại hoặc simulated annealing thay vì hill climbing tham lam đơn thuần?",
        },
        "es": {
            "summary": "🧪 Tarea rápida · QA-LOCAL-01 · 10–15 min",
            "title": "Por qué la búsqueda local se atasca o escapa",
            "intro": "Ejecuta una trayectoria de búsqueda local o un benchmark de reinicios con semilla y emparejados; explica por qué el algoritmo se atasca, escapa o tiene éxito de forma fiable.",
            "predict": "Antes de ejecutar, ¿qué estrategia seleccionada tendrá éxito con mayor fiabilidad y cuál alcanzará el coste más bajo? ¿Por qué pueden diferir?",
            "observe": "Ejecuta una búsqueda o el benchmark de reinicios repetidos. Registra el problema, algoritmo, tasa de éxito, coste final medio y mejor coste medio pertinentes.",
            "explain": "¿Cómo eligió movimientos la regla de búsqueda y por qué la frecuencia de éxito y el coste medio pueden ordenar los algoritmos de forma distinta?",
            "transfer": "¿Qué tipo de problema de optimización necesitaría reinicios o simulated annealing en lugar de hill climbing voraz?",
        },
    },
    "QA-WUMPUS-01": {
        "vi": {
            "summary": "🧪 Bài tập nhanh · QA-WUMPUS-01 · 10–15 phút",
            "title": "An toàn, rủi ro hay chưa biết?",
            "intro": "Chạy một chiến lược tác tử, kiểm tra thế giới và bản đồ tri thức rồi giải thích cách percept hỗ trợ hành động an toàn.",
            "predict": "Trước khi bước tiếp, ô hoặc hành động nào nên được xem là an toàn, rủi ro hay chưa biết? Vì sao?",
            "observe": "Bước tác tử. Ghi lại điểm, số bước, trạng thái và một suy luận từ bản đồ tri thức.",
            "explain": "Các percept biện minh cho hành động tiếp theo hoặc giúp tác tử tránh một ô nguy hiểm như thế nào?",
            "transfer": "Ở đâu khác một tác tử AI phải hành động khi chỉ có thông tin một phần?",
        },
        "es": {
            "summary": "🧪 Tarea rápida · QA-WUMPUS-01 · 10–15 min",
            "title": "¿Seguro, arriesgado o desconocido?",
            "intro": "Ejecuta una estrategia del agente, inspecciona el mundo y el mapa de conocimiento y explica cómo las percepciones justifican una acción segura.",
            "predict": "Antes de avanzar, ¿qué casilla o acción debería ser segura, arriesgada o desconocida? ¿Por qué?",
            "observe": "Avanza el agente. Registra la puntuación, el número de pasos, el estado y una inferencia del mapa de conocimiento.",
            "explain": "¿Cómo justificaron las percepciones la siguiente acción del agente o evitaron una casilla peligrosa?",
            "transfer": "¿En qué otros contextos tendría que actuar un agente de IA con información parcial?",
        },
    },
    "QA-SAT-01": {
        "vi": {
            "summary": "🧪 Bài tập nhanh · QA-SAT-01 · 10–15 phút",
            "title": "SAT, UNSAT hay suy ra truy vấn?",
            "intro": "Chuyển một cơ sở tri thức, kiểm tra bằng chứng DPLL hoặc CDCL, rồi giải thích CNF, mệnh đề học được và bước nhảy lùi chứng minh điều gì.",
            "predict": "Trước khi chuyển đổi, bạn dự đoán ví dụ này là SAT, UNSAT hay suy ra truy vấn? Vì sao?",
            "observe": "Chạy phép chuyển đổi và xem một vết DPLL hoặc CDCL. Ghi lại kết quả CNF chính cùng mọi quyết định, lan truyền, xung đột, mệnh đề học được hoặc bước nhảy lùi.",
            "explain": "CNF giúp kiểm tra điều gì dễ hơn? Nếu dùng CDCL, vì sao mệnh đề học được hợp lệ và mức nhảy lùi an toàn?",
            "transfer": "Khi nào một hệ cơ sở tri thức cần resolution thay vì chỉ dựa vào trực giác bảng chân trị?",
        },
        "es": {
            "summary": "🧪 Tarea rápida · QA-SAT-01 · 10–15 min",
            "title": "¿SAT, UNSAT o se deriva la consulta?",
            "intro": "Convierte una base de conocimiento, inspecciona evidencia DPLL o CDCL y explica qué establecen CNF, las cláusulas aprendidas y los saltos hacia atrás.",
            "predict": "Antes de convertir, ¿esperas que el ejemplo sea SAT, UNSAT o que implique la consulta? ¿Por qué?",
            "observe": "Ejecuta la conversión e inspecciona una traza DPLL o CDCL. Registra el resultado CNF clave y cualquier decisión, propagación, conflicto, cláusula aprendida o salto hacia atrás.",
            "explain": "¿Qué facilita comprobar CNF? Si usas CDCL, ¿por qué es válida la cláusula aprendida y seguro el nivel de salto?",
            "transfer": "¿Cuándo necesitaría un sistema de conocimiento resolución en lugar de una intuición basada solo en tablas de verdad?",
        },
    },
}


def registry() -> list[dict]:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    return list(data["activities"])


def active_rows() -> list[dict]:
    return [row for row in registry() if row["status"] == "active"]


def patch_currency() -> None:
    landing = SITE / "index.html"
    html = landing.read_text(encoding="utf-8")
    html = html.replace("Fourteen", "Fifteen").replace("fourteen", "fifteen")
    # A current-release landing description may describe the applets as multilingual,
    # but it must not imply that every support page is four-language.
    html = html.replace(
        "Fifteen multilingual, offline-ready AI interactives",
        "Fifteen learner applets with EN/ZH/VI/ES support, offline-ready interaction",
    )
    landing.write_text(html, encoding="utf-8")

    curriculum = SITE / "curriculum.html"
    html = curriculum.read_text(encoding="utf-8")
    html = re.sub(
        r'<meta content="[^"]*foundational AI applets\." name="description"/?>',
        '<meta content="Course-aligned pathways for 13 Foundations/course-track AI labs plus two Modern AI extensions." name="description"/>',
        html,
        count=1,
    )
    html = html.replace("fourteen foundational applets", "thirteen Foundations/course-track labs plus two Modern AI extensions")
    html = html.replace("Fourteen foundational applets", "Thirteen Foundations/course-track labs plus two Modern AI extensions")
    curriculum.write_text(html, encoding="utf-8")

    teacher = SITE / "teacher-pack.html"
    html = teacher.read_text(encoding="utf-8")
    scope_note = (
        '<div class="note" id="locale-scope-note"><strong>Language scope:</strong> '
        'All 15 learner applets support English, Simplified Chinese, Vietnamese, and Spanish. '
        'This Teacher Pack and the current curriculum/navigation support pages use English and Simplified Chinese; '
        'the NN-1 and CNN-1 Activity Pack pilot is English-only.</div>'
    )
    if 'id="locale-scope-note"' not in html:
        marker = "<h1>Teacher Pack</h1>"
        if marker not in html:
            marker = "</h1>"
            at = html.find(marker)
            if at < 0:
                raise RuntimeError("Could not place Teacher Pack locale scope note")
            at += len(marker)
            html = html[:at] + scope_note + html[at:]
        else:
            html = html.replace(marker, marker + scope_note, 1)
    teacher.write_text(html, encoding="utf-8")


def translation_extension(activity: dict, english: dict[str, str]) -> str:
    row = ACTIVE_COPY[activity["id"]]
    vi_map = {english[key]: row["vi"][key] for key in english}
    es_map = {english[key]: row["es"][key] for key in english}
    common_en = {
        "State snapshot": "State snapshot",
        "Predict": "Predict",
        "Observe": "Observe",
        "Explain": "Explain",
        "Transfer": "Transfer",
        "State snapshot appears here.": "State snapshot appears here.",
        "↻ Refresh state": "↻ Refresh state",
        "📋 Copy packet": "📋 Copy packet",
        "🖨 Print packet": "🖨 Print packet",
        "Clear local draft": "Clear local draft",
    }
    common_vi = {
        "State snapshot": "Ảnh chụp trạng thái",
        "Predict": "Dự đoán",
        "Observe": "Quan sát",
        "Explain": "Giải thích",
        "Transfer": "Vận dụng",
        "State snapshot appears here.": "Ảnh chụp trạng thái xuất hiện ở đây.",
        "↻ Refresh state": "↻ Cập nhật trạng thái",
        "📋 Copy packet": "📋 Sao chép bài làm",
        "🖨 Print packet": "🖨 In bài làm",
        "Clear local draft": "Xóa bản nháp cục bộ",
    }
    common_es = {
        "State snapshot": "Instantánea del estado",
        "Predict": "Predice",
        "Observe": "Observa",
        "Explain": "Explica",
        "Transfer": "Transfiere",
        "State snapshot appears here.": "La instantánea del estado aparece aquí.",
        "↻ Refresh state": "↻ Actualizar estado",
        "📋 Copy packet": "📋 Copiar respuestas",
        "🖨 Print packet": "🖨 Imprimir respuestas",
        "Clear local draft": "Borrar borrador local",
    }
    vi_map.update({key: common_vi[key] for key in common_en})
    es_map.update({key: common_es[key] for key in common_en})
    return (
        '<script data-quick-assign-locales="1">(function(){'
        'var root=window.__AI_PLAYGROUNDS_R4_LOCALES=window.__AI_PLAYGROUNDS_R4_LOCALES||{};'
        f'var row=root[{json.dumps(activity["slug"])}];if(!row)return;'
        f'Object.assign(row.vi.strings,{json.dumps(vi_map, ensure_ascii=False)});'
        f'Object.assign(row.es.strings,{json.dumps(es_map, ensure_ascii=False)});'
        '})();</script>'
    )


def patch_packet_runtime(html: str) -> str:
    old_lang = "function currentLang() { return document.documentElement.lang && document.documentElement.lang.toLowerCase().startsWith('zh') ? 'zh' : 'en'; }"
    new_lang = """function currentLang() {
    const raw = String(document.documentElement.lang || 'en').toLowerCase();
    if (raw.startsWith('zh')) return 'zh';
    if (raw.startsWith('vi')) return 'vi';
    if (raw.startsWith('es')) return 'es';
    return 'en';
  }"""
    if old_lang not in html:
        raise RuntimeError("Quick Assign could not locate response-packet locale function")
    html = html.replace(old_lang, new_lang, 1)
    old_text = "function textFor(el, lang) { return el.getAttribute(lang === 'zh' ? 'data-lab-zh' : 'data-lab-en') || el.textContent; }"
    new_text = """function textFor(el, lang) {
    if ((lang === 'vi' || lang === 'es') && window.__r4Localization) {
      const source = el.getAttribute('data-lab-en') || el.textContent;
      return window.__r4Localization.translateString(source, lang);
    }
    return el.getAttribute(lang === 'zh' ? 'data-lab-zh' : 'data-lab-en') || el.textContent;
  }"""
    if old_text not in html:
        raise RuntimeError("Quick Assign could not locate response-packet text function")
    html = html.replace(old_text, new_text, 1)
    old_labels = "const labels = lang === 'zh' ? {title: LAB_CONFIG.zhTitle, state:'状态记录', predict:'预测', observe:'观察', explain:'解释', transfer:'迁移'} : {title: LAB_CONFIG.title, state:'State snapshot', predict:'Predict', observe:'Observe', explain:'Explain', transfer:'Transfer'};"
    new_labels = """const baseLabels = {title: LAB_CONFIG.title, state:'State snapshot', predict:'Predict', observe:'Observe', explain:'Explain', transfer:'Transfer'};
    const labels = lang === 'zh' ? {title: LAB_CONFIG.zhTitle, state:'状态记录', predict:'预测', observe:'观察', explain:'解释', transfer:'迁移'} : ((lang === 'vi' || lang === 'es') && window.__r4Localization ? Object.fromEntries(Object.entries(baseLabels).map(([k,v]) => [k, window.__r4Localization.translateString(v, lang)])) : baseLabels);"""
    if old_labels not in html:
        raise RuntimeError("Quick Assign could not locate response-packet label map")
    html = html.replace(old_labels, new_labels, 1)
    old_value = "return value ? field.label + ': ' + value : null;"
    new_value = """const label = ((currentLang() === 'vi' || currentLang() === 'es') && window.__r4Localization) ? window.__r4Localization.translateString(field.label, currentLang()) : field.label;
    return value ? label + ': ' + value : null;"""
    if old_value not in html:
        raise RuntimeError("Quick Assign could not locate response-packet state label")
    html = html.replace(old_value, new_value, 1)
    listener = "window.addEventListener('r4languagechange', () => setTimeout(applyLabLang, 0));\n  "
    marker = "document.querySelectorAll('.lang-switch button').forEach(button => button.addEventListener('click', () => setTimeout(applyLabLang, 0)));"
    if marker not in html:
        raise RuntimeError("Quick Assign could not locate response-packet language listener")
    html = html.replace(marker, marker + "\n  " + listener, 1)
    return html


def patch_quick_assign(activity: dict) -> None:
    path = SITE / "playgrounds" / activity["slug"] / "index.html"
    html = path.read_text(encoding="utf-8")
    details_marker = '<details class="classroom-lab"'
    if details_marker not in html:
        raise RuntimeError(f"{activity['slug']} has no classroom-lab response packet")
    html = html.replace(details_marker, f'<details class="classroom-lab quick-assign" id="{activity["anchor"]}" data-quick-assign-id="{activity["id"]}"', 1)

    summary_old = 'data-lab-en="🧪 Student response packet" data-lab-zh="🧪 课堂实验模式">🧪 Student response packet</span>'
    summary_en = f'🧪 Quick Assign · {activity["id"]} · 10–15 min'
    summary_zh = f'🧪 快速任务 · {activity["id"]} · 10–15 分钟'
    summary_new = f'data-lab-en="{summary_en}" data-lab-zh="{summary_zh}">{summary_en}</span>'
    if summary_old not in html:
        raise RuntimeError(f"{activity['slug']} Quick Assign summary contract changed")
    html = html.replace(summary_old, summary_new, 1)

    intro_match = re.search(r'<p class="lab-intro" data-lab-en="([^"]+)" data-lab-zh="([^"]+)">([^<]+)</p>', html)
    if not intro_match:
        raise RuntimeError(f"{activity['slug']} Quick Assign intro not found")
    english = {"summary": summary_en, "title": activity["title"], "intro": intro_match.group(1)}
    for key, answer in (("predict", "predict"), ("observe", "observe"), ("explain", "explain"), ("transfer", "transfer")):
        match = re.search(rf'<textarea data-lab-answer="{answer}" data-lab-en="([^"]+)"', html)
        if not match:
            raise RuntimeError(f"{activity['slug']} Quick Assign {key} prompt not found")
        english[key] = match.group(1)

    meta = (
        f'<div class="quick-assign-meta" data-r4-no-translate="1" style="margin:0 0 10px;padding:9px 11px;border:1px solid var(--border);border-left:4px solid var(--accent);border-radius:8px;">'
        f'<strong>{activity["id"]}</strong> · Level 1 · 10–15 min<br><span>{activity["title"]}</span></div>'
    )
    panel = '<div class="lab-panel">'
    if panel not in html:
        raise RuntimeError(f"{activity['slug']} Quick Assign panel not found")
    html = html.replace(panel, panel + meta, 1)

    # The applet-specific R4 catalog is loaded before the shared overlay. Add only
    # Quick-Assign-specific strings to that catalog without forking the main locale files.
    loc_marker = '<script src="../../assets/localization-r4.js"></script>'
    if loc_marker not in html:
        raise RuntimeError(f"{activity['slug']} R4 runtime marker missing")
    html = html.replace(loc_marker, translation_extension(activity, english) + loc_marker, 1)
    html = patch_packet_runtime(html)
    path.write_text(html, encoding="utf-8")


def patch_teacher_quick_assigns() -> None:
    path = SITE / "teacher-pack.html"
    html = path.read_text(encoding="utf-8")
    rows = active_rows()
    body = ''.join(
        f'<tr><td><strong>{row["id"]}</strong></td><td>{row["title"]}</td><td>10–15 min</td><td>{row["teacher_look_for"]}</td><td><a href="playgrounds/{row["slug"]}/index.html#{row["anchor"]}">Open</a></td></tr>'
        for row in rows
    )
    section = (
        '<section id="quick-assigns"><h2>Level 1 · Quick Assigns</h2>'
        '<p>Quick Assigns reuse the applet’s existing Guided Challenge and local response packet. '
        'Students predict, run a bounded comparison, record evidence, explain the mechanism, and transfer the idea in about 10–15 minutes. '
        'Use the stable ID when assigning work.</p>'
        '<table><thead><tr><th>ID</th><th>Activity</th><th>Time</th><th>Teacher look-for</th><th>Student link</th></tr></thead><tbody>'
        + body + '</tbody></table>'
        '<p><strong>Level 2:</strong> NN-1 and CNN-1 remain the 30–50 minute Activity Pack canaries. '
        '<strong>Level 3:</strong> full lesson/unit packs are reserved for future development and are not currently shipped.</p></section>'
    )
    if 'id="quick-assigns"' not in html:
        anchor = '<section id="activity-packs">'
        if anchor in html:
            html = html.replace(anchor, section + anchor, 1)
        else:
            # v1.6 Teacher Pack can differ from the v1.5.1 source layout.
            marker = '<h2>Ready-to-assign Activity Packs</h2>'
            at = html.find(marker)
            if at < 0:
                raise RuntimeError("Could not place Teacher Pack Quick Assign table")
            section_start = html.rfind('<section', 0, at)
            if section_start < 0:
                section_start = at
            html = html[:section_start] + section + html[section_start:]
    path.write_text(html, encoding="utf-8")


def patch_activity_provenance() -> None:
    # The Activity Packs were introduced in v1.5.1, but their public pages are part
    # of the current deterministic artifact. Preserve both facts instead of leaving
    # an ambiguous stale footer.
    for name in ("index.html", "nn-1.html", "cnn-1.html"):
        path = SITE / "activities" / name
        html = path.read_text(encoding="utf-8")
        html = html.replace('content="1.5.1"', 'content="1.6.1-candidate"')
        html = html.replace('AI Playgrounds · v1.5.1 · Activity Pack pilot', 'AI Playgrounds · Activity Pack pilot introduced in v1.5.1 · current suite candidate v1.6.1')
        path.write_text(html, encoding="utf-8")


def validate() -> None:
    files = [p for p in SITE.rglob('*') if p.is_file()]
    applets = list((SITE / "playgrounds").glob("*/index.html"))
    if len(files) != EXPECTED_FILES or len(applets) != EXPECTED_APPLETS:
        raise RuntimeError(f"v1.6.1 candidate boundary drift: {len(files)} files / {len(applets)} applets")

    landing = (SITE / "index.html").read_text(encoding="utf-8")
    if re.search(r'\bFourteen\b|\bfourteen\b', landing):
        raise RuntimeError("Current landing page still contains stale fourteen-app copy")
    if "Fifteen" not in landing or "15" not in landing:
        raise RuntimeError("Current landing page lacks fifteen-app release currency")

    curriculum = (SITE / "curriculum.html").read_text(encoding="utf-8")
    if "13 Foundations" not in curriculum and "thirteen Foundations" not in curriculum:
        raise RuntimeError("Curriculum lacks the 13-Foundations boundary")
    if curriculum.count('class="order-dot"') != EXPECTED_FOUNDATIONS:
        raise RuntimeError("Curriculum Foundations row count changed")
    if re.search(r'fourteen foundational applets', curriculum, re.I):
        raise RuntimeError("Curriculum still claims fourteen foundational applets")

    ids = [row["id"] for row in registry()]
    if len(ids) != len(set(ids)) or len(ids) != EXPECTED_APPLETS:
        raise RuntimeError("Quick Assign registry must reserve exactly one unique ID per applet")
    active = active_rows()
    if [row["id"] for row in active] != ["QA-SEARCH-01", "QA-LOCAL-01", "QA-WUMPUS-01", "QA-SAT-01"]:
        raise RuntimeError("Initial Quick Assign canary set changed")
    for row in active:
        source = (SITE / "playgrounds" / row["slug"] / "index.html").read_text(encoding="utf-8")
        if source.count(f'data-quick-assign-id="{row["id"]}"') != 1:
            raise RuntimeError(f"{row['id']} must surface exactly once")
        if f'id="{row["anchor"]}"' not in source:
            raise RuntimeError(f"{row['id']} anchor missing")
        if row["title"] not in source:
            raise RuntimeError(f"{row['id']} registry title is not surfaced in the applet")
        for field in ('predict', 'observe', 'explain', 'transfer'):
            if f'data-lab-answer="{field}"' not in source:
                raise RuntimeError(f"{row['id']} lost {field} response field")
        if 'data-lab-action="copy"' not in source or 'data-lab-action="print"' not in source:
            raise RuntimeError(f"{row['id']} lost local copy/print submission path")
        if 'data-quick-assign-locales="1"' not in source or "r4languagechange" not in source:
            raise RuntimeError(f"{row['id']} four-locale Quick Assign overlay missing")
    for row in registry():
        if row["status"] == "reserved":
            source = (SITE / "playgrounds" / row["slug"] / "index.html").read_text(encoding="utf-8")
            if f'data-quick-assign-id="{row["id"]}"' in source:
                raise RuntimeError(f"Reserved Quick Assign surfaced early: {row['id']}")

    teacher = (SITE / "teacher-pack.html").read_text(encoding="utf-8")
    for row in active:
        if row["id"] not in teacher or f'#{row["anchor"]}' not in teacher:
            raise RuntimeError(f"Teacher Pack does not expose {row['id']}")
    if "All 15 learner applets support English, Simplified Chinese, Vietnamese, and Spanish" not in teacher:
        raise RuntimeError("Teacher Pack lacks explicit learner-vs-support locale scope")


def build_site() -> None:
    v16.build_site()
    patch_currency()
    for row in active_rows():
        patch_quick_assign(row)
    patch_teacher_quick_assigns()
    patch_activity_provenance()
    validate()
    print(f"Built v1.6.1 Quick Assign candidate: {EXPECTED_APPLETS} applets / {EXPECTED_FILES} files / {len(active_rows())} active Quick Assigns")


if __name__ == "__main__":
    build_site()
