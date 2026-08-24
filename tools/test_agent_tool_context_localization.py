#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "tools" / "agent_tool_context_locales.json"
BUILDER = ROOT / "tools" / "build_agent_tool_context_english_candidate.py"
ENGLISH = ROOT / "release-evidence" / "lab14-agent-tool-context-english-candidate.html"
SOURCE_FREEZE_HEAD = "9f2f5286f4de3e12a881b61d491c87efe6950166"
LOCALES = ("en", "zh", "vi", "es")
PLACEHOLDER = re.compile(r"\{([A-Za-z0-9_]+)\}")
PROTECTED = (
    "MCP 2026-07-28",
    "weather.current",
    "weather.forecast",
    "unit.convert_temperature",
    "calendar.create",
    "mail.send",
    "notes.search",
    "temperature_c",
    "temperature_f",
)
IDENTICAL_ALLOWED = {
    ("challenge.observation.option_convert", "zh"),
    ("challenge.observation.option_convert", "vi"),
    ("challenge.observation.option_convert", "es"),
    ("controls.principal", "es"),
}


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> int:
    failures: list[str] = []
    checks = 0

    payload = json.loads(CATALOG.read_text(encoding="utf-8"))
    strings = payload.get("strings", {})

    checks += 1
    require(payload.get("source_freeze_head") == SOURCE_FREEZE_HEAD, "catalog is not bound to the frozen R4 English head", failures)
    checks += 1
    require(payload.get("protocol_scope") == "MCP 2026-07-28", "protocol scope drifted from MCP 2026-07-28", failures)
    checks += 1
    require(len(strings) >= 100, f"semantic catalog is unexpectedly small: {len(strings)} keys", failures)

    for key, entry in strings.items():
        checks += 1
        require(set(entry) == set(LOCALES), f"{key}: expected exactly en/zh/vi/es", failures)
        if set(entry) != set(LOCALES):
            continue
        en = str(entry["en"])
        en_placeholders = set(PLACEHOLDER.findall(en))
        for locale in ("zh", "vi", "es"):
            value = str(entry[locale])
            checks += 1
            require(bool(value.strip()), f"{key}/{locale}: empty translation", failures)
            checks += 1
            require(set(PLACEHOLDER.findall(value)) == en_placeholders, f"{key}/{locale}: placeholder mismatch", failures)
            checks += 1
            if (key, locale) not in IDENTICAL_ALLOWED and len(en) >= 12 and re.search(r"[A-Za-z]{4}", en):
                require(value != en, f"{key}/{locale}: nontrivial English prose mapped to itself", failures)
            for token in PROTECTED:
                if token in en:
                    checks += 1
                    require(token in value, f"{key}/{locale}: protected token changed or disappeared: {token}", failures)

    combined = {locale: "\n".join(str(entry[locale]) for entry in strings.values() if locale in entry) for locale in LOCALES}
    cjk = len(re.findall(r"[\u3400-\u9fff]", combined["zh"]))
    vi_marks = len(re.findall(r"[ăâđêôơưĂÂĐÊÔƠƯàáảãạằắẳẵặầấẩẫậèéẻẽẹềếểễệìíỉĩịòóỏõọồốổỗộờớởỡợùúủũụừứửữựỳýỷỹỵ]", combined["vi"], flags=re.I))
    es_marks = len(re.findall(r"[áéíóúüñ¿¡]", combined["es"], flags=re.I))
    checks += 3
    require(cjk >= 1200, f"Chinese catalog contains too little CJK text: {cjk}", failures)
    require(vi_marks >= 350, f"Vietnamese catalog contains too few language-specific characters: {vi_marks}", failures)
    require(es_marks >= 90, f"Spanish catalog contains too few language-specific characters: {es_marks}", failures)

    # High-risk semantic traps: each locale must retain the key distinctions rather
    # than silently collapsing availability, validation, authorization, execution,
    # provenance, termination, or prompt-injection scope.
    semantic_requirements = {
        "zh": ("授权", "模式", "执行", "来源", "停止", "提示注入"),
        "vi": ("quyền", "lược đồ", "thực thi", "nguồn gốc", "dừng", "prompt injection"),
        "es": ("autoriz", "esquema", "ejec", "procedencia", "deten", "inyección"),
    }
    for locale, terms in semantic_requirements.items():
        text = combined[locale].lower()
        for term in terms:
            checks += 1
            require(term.lower() in text, f"{locale}: missing high-risk semantic term {term}", failures)

    # The corrections themselves must remain explicit negations/qualifications.
    checks += 6
    require(strings["myth.2.correction"]["zh"].startswith("不对"), "zh authorization misconception lost explicit rejection", failures)
    require(strings["myth.3.correction"]["zh"].startswith("不对"), "zh schema misconception lost explicit rejection", failures)
    require(strings["myth.2.correction"]["vi"].startswith("Không"), "vi authorization misconception lost explicit rejection", failures)
    require(strings["myth.3.correction"]["vi"].startswith("Không"), "vi schema misconception lost explicit rejection", failures)
    require(strings["myth.2.correction"]["es"].startswith("No"), "es authorization misconception lost explicit rejection", failures)
    require(strings["myth.3.correction"]["es"].startswith("No"), "es schema misconception lost explicit rejection", failures)

    checks += 3
    require("不能普遍解决提示注入" in strings["myth.10.correction"]["zh"], "zh prompt-injection scope overclaim", failures)
    require("không giải quyết prompt injection nói chung" in strings["myth.10.correction"]["vi"].lower(), "vi prompt-injection scope overclaim", failures)
    require("no resuelve la inyección" in strings["myth.10.correction"]["es"].lower(), "es prompt-injection scope overclaim", failures)

    built = subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT, text=True, capture_output=True, check=False)
    checks += 1
    require(built.returncode == 0 and ENGLISH.is_file(), "could not rebuild frozen English candidate for source binding", failures)
    if ENGLISH.is_file():
        source = ENGLISH.read_text(encoding="utf-8")
        source_keys = (
            "page.title", "page.subtitle", "page.badge", "boundary.label", "boundary.text",
            "controls.scenario", "scenario.canonical", "scenario.mcp", "section.context",
            "section.candidates", "section.tools", "section.mcp", "section.trace",
            "challenge.title", "challenge.next.prompt", "challenge.gate.prompt",
            "challenge.observation.prompt", "challenge.trust.prompt", "challenge.stop.prompt",
            "section.accessible", "myth.1", "myth.10.correction", "terms.heading",
        )
        for key in source_keys:
            checks += 1
            require(strings[key]["en"] in source, f"{key}: English catalog source phrase is not present in frozen candidate", failures)

    result = {
        "harness": "tools/test_agent_tool_context_localization.py",
        "catalog": str(CATALOG.relative_to(ROOT)),
        "source_freeze_head": payload.get("source_freeze_head"),
        "keys": len(strings),
        "checks": checks,
        "failed": len(failures),
        "cjk_chars": cjk,
        "vietnamese_diacritics": vi_marks,
        "spanish_diacritics": es_marks,
        "pass": not failures,
        "failures": failures,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
