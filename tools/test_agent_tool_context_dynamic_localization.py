#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "tools" / "agent_tool_context_locales_dynamic.json"
PROTOTYPE = ROOT / "tools" / "agent_tool_context_prototype.html"
CORE = ROOT / "tools" / "agent_tool_context_core.js"
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
    "assistant",
    "learner",
    "operator",
    "trusted_fixture",
    "untrusted_content",
)
IDENTICAL_ALLOWED_PREFIXES = ("role.", "trust.")
SOURCE_ANCHOR_OVERRIDES = {
    # These learner-facing labels intentionally derive from frozen machine-state
    # identifiers rather than appearing verbatim in the R4 source.
    "runtime.invalid_action": ("invalid_action_type",),
    "runtime.budget_exhausted": ("budget_exhausted",),
    "runtime.execution_error": ("executed_error",),
}


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def source_anchors(key: str, english: str) -> tuple[str, ...]:
    if key in SOURCE_ANCHOR_OVERRIDES:
        return SOURCE_ANCHOR_OVERRIDES[key]
    if PLACEHOLDER.search(english):
        anchors = tuple(
            part.strip()
            for part in PLACEHOLDER.sub("\n", english).splitlines()
            if len(part.strip()) >= 4
        )
        return anchors
    return (english,)


def main() -> int:
    failures: list[str] = []
    checks = 0

    payload = json.loads(CATALOG.read_text(encoding="utf-8"))
    strings = payload.get("strings", {})

    checks += 1
    require(payload.get("source_freeze_head") == SOURCE_FREEZE_HEAD, "dynamic catalog is not bound to the frozen R4 English head", failures)
    checks += 1
    require(len(strings) >= 30, f"dynamic semantic supplement is unexpectedly small: {len(strings)} keys", failures)

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
            if not key.startswith(IDENTICAL_ALLOWED_PREFIXES) and len(en) >= 10 and re.search(r"[A-Za-z]{4}", en):
                checks += 1
                require(value != en, f"{key}/{locale}: nontrivial English text mapped to itself", failures)
            for token in PROTECTED:
                if token in en:
                    checks += 1
                    require(token in value, f"{key}/{locale}: protected identifier changed or disappeared: {token}", failures)

    # Every English dynamic phrase must remain grounded in the frozen R4 source.
    # Machine-state display labels bind to their exact state identifiers through
    # SOURCE_ANCHOR_OVERRIDES rather than pretending the derived prose was literal.
    source = PROTOTYPE.read_text(encoding="utf-8") + "\n" + CORE.read_text(encoding="utf-8")
    for key, entry in strings.items():
        en = str(entry.get("en", ""))
        anchors = source_anchors(key, en)
        checks += 1
        require(bool(anchors) and all(anchor in source for anchor in anchors), f"{key}: English dynamic surface is not grounded in frozen source", failures)

    combined = {locale: "\n".join(str(entry[locale]) for entry in strings.values()) for locale in LOCALES}
    cjk = len(re.findall(r"[\u3400-\u9fff]", combined["zh"]))
    vi_marks = len(re.findall(r"[ăâđêôơưĂÂĐÊÔƠƯàáảãạằắẳẵặầấẩẫậèéẻẽẹềếểễệìíỉĩịòóỏõọồốổỗộờớởỡợùúủũụừứửữựỳýỷỹỵ]", combined["vi"], flags=re.I))
    es_marks = len(re.findall(r"[áéíóúüñ¿¡]", combined["es"], flags=re.I))
    checks += 3
    require(cjk >= 250, f"dynamic Chinese supplement contains too little CJK text: {cjk}", failures)
    require(vi_marks >= 150, f"dynamic Vietnamese supplement contains too few language-specific characters: {vi_marks}", failures)
    require(es_marks >= 25, f"dynamic Spanish supplement contains too few language-specific characters: {es_marks}", failures)

    # Adversarial observation must remain visibly instruction-like in every locale;
    # localization must not sanitize away the attack that the scenario teaches.
    attack = strings["fixture.note_injection"]
    checks += 6
    require("mail.send" in attack["zh"] and "忽略" in attack["zh"], "zh adversarial note lost its instruction-like content", failures)
    require("mail.send" in attack["vi"] and "BỎ QUA" in attack["vi"].upper(), "vi adversarial note lost its instruction-like content", failures)
    require("mail.send" in attack["es"] and "IGNORA" in attack["es"].upper(), "es adversarial note lost its instruction-like content", failures)
    require("当前任务" in attack["zh"], "zh adversarial note no longer refers to the current task", failures)
    require("NHIỆM VỤ HIỆN TẠI" in attack["vi"].upper(), "vi adversarial note no longer refers to the current task", failures)
    require("TAREA ACTUAL" in attack["es"].upper(), "es adversarial note no longer refers to the current task", failures)

    # Validation, authorization, and execution-error categories must remain distinct.
    semantic_requirements = {
        "zh": ("缺少必填参数", "未获授权", "工具执行返回了错误"),
        "vi": ("thiếu đối số bắt buộc", "không được phép", "thực thi công cụ trả về một quan sát lỗi"),
        "es": ("falta el argumento obligatorio", "no autorizado", "ejecución de la herramienta devolvió una observación de error"),
    }
    for locale, terms in semantic_requirements.items():
        text = combined[locale].lower()
        for term in terms:
            checks += 1
            require(term.lower() in text, f"{locale}: missing dynamic semantic distinction: {term}", failures)

    # Goal and model-text surfaces must cover all eight scenarios and all source-side text outputs.
    expected_goal_keys = {f"goal.{name}" for name in ("canonical", "overlap", "invalid", "text", "permission", "injection", "mcp", "termination")}
    checks += 1
    require(expected_goal_keys.issubset(strings), f"missing scenario goal translations: {sorted(expected_goal_keys - set(strings))}", failures)
    checks += 1
    require({"model_text.overlap", "model_text.text_claim", "model_text.convert", "model_text.weather"}.issubset(strings), "model-side text outputs are not fully localized", failures)

    proc = subprocess.run(["node", "--check", str(CORE)], cwd=ROOT, text=True, capture_output=True, check=False)
    checks += 1
    require(proc.returncode == 0, f"JavaScript syntax failure while binding dynamic catalog: {proc.stderr[-500:]}", failures)

    result = {
        "harness": "tools/test_agent_tool_context_dynamic_localization.py",
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
