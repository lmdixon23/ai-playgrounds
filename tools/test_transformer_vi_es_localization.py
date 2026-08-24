#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = ROOT / "tools" / "transformer_language_model_locales.json"
VI_ES = ROOT / "tools" / "transformer_language_model_locales_vi_es.json"
EN_FREEZE = "e89c0b5d8b166b66407fc018deb1b7eec485b6a4"
PLACEHOLDER_RE = re.compile(r"\{([A-Za-z0-9_]+)\}")
VI_DIACRITIC_RE = re.compile(r"[ăâđêôơưĂÂĐÊÔƠƯáàảãạấầẩẫậắằẳẵặéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ]", re.I)
ES_DIACRITIC_RE = re.compile(r"[áéíóúüñ¿¡]", re.I)


def placeholders(text: str) -> set[str]:
    return set(PLACEHOLDER_RE.findall(text))


def main() -> int:
    base = json.loads(BASE.read_text(encoding="utf-8"))
    extra = json.loads(VI_ES.read_text(encoding="utf-8"))
    failures: list[str] = []
    checks = 0

    def check(ok: bool, message: str) -> None:
        nonlocal checks
        checks += 1
        if not ok:
            failures.append(message)

    check(base.get("source_freeze_head") == EN_FREEZE, "base catalog is not bound to accepted English freeze")
    check(extra.get("schema") == "ai-playgrounds-lab13-vi-es-v1", "unexpected VI/ES localization schema")
    check(extra.get("source_freeze_head") == EN_FREEZE, "VI/ES catalog is not bound to accepted English freeze")
    check(extra.get("base_catalog") == "tools/transformer_language_model_locales.json", "VI/ES base-catalog pointer changed")

    en = base.get("locales", {}).get("en", {})
    locales = extra.get("locales", {})
    check(set(locales) == {"vi", "es"}, f"expected exactly VI+ES in extension catalog, got {sorted(locales)}")
    check(len(en) >= 120, f"English source catalog unexpectedly small: {len(en)} keys")

    for locale in ("vi", "es"):
        loc = locales.get(locale, {})
        check(set(loc) == set(en), f"EN/{locale.upper()} key mismatch: missing={sorted(set(en)-set(loc))}, extra={sorted(set(loc)-set(en))}")
        for key in sorted(set(en) | set(loc)):
            if key not in en or key not in loc:
                continue
            check(bool(str(loc[key]).strip()), f"empty {locale} value: {key}")
            check(placeholders(str(en[key])) == placeholders(str(loc[key])), f"placeholder mismatch at {locale}:{key}: EN={sorted(placeholders(str(en[key])))}, LOC={sorted(placeholders(str(loc[key])))}")

    vi = locales.get("vi", {})
    es = locales.get("es", {})
    vi_text = "\n".join(str(v) for v in vi.values())
    es_text = "\n".join(str(v) for v in es.values())

    check(len(VI_DIACRITIC_RE.findall(vi_text)) >= 500, "Vietnamese catalog has unexpectedly little Vietnamese diacritic content")
    check(len(ES_DIACRITIC_RE.findall(es_text)) >= 80, "Spanish catalog has unexpectedly little Spanish diacritic/punctuation content")

    vi_required = [
        "tự chú ý",
        "vector vị trí",
        "truy vấn",
        "khóa",
        "giá trị",
        "mặt nạ nhân quả",
        "tự hồi quy",
        "trọng số chú ý",
        "nhiệt độ",
        "kết nối phần dư",
        "feed-forward",
        "softmax",
        "logits",
    ]
    es_required = [
        "autoatención",
        "vectores de posición",
        "consulta",
        "clave",
        "valor",
        "máscara causal",
        "autorregresiva",
        "pesos de atención",
        "temperatura",
        "rutas residuales",
        "feed-forward",
        "softmax",
        "logits",
    ]
    for term in vi_required:
        check(term.lower() in vi_text.lower(), f"required Vietnamese technical term missing: {term}")
    for term in es_required:
        check(term.lower() in es_text.lower(), f"required Spanish technical term missing: {term}")

    protected = ["<BOS>", "<UNK>", "softmax", "logits", "Q/K/V", "q[0]", "k[0]", "P(sleep)", "αⱼvⱼ"]
    for locale, loc in (("vi", vi), ("es", es)):
        for token in protected:
            for key, value in en.items():
                if token in str(value):
                    check(token in str(loc[key]), f"protected token {token!r} changed/disappeared at {locale}:{key}")
        for key in ["challenge.1.option0", "challenge.1.option1", "challenge.1.option2", "challenge.1.option3"]:
            check(en[key] == loc[key], f"model-data challenge option changed at {locale}:{key}")

    vi_precision = {
        "boundary.text": ["mô hình đồ chơi xác định", "không phải là lời giải thích tổng quát"],
        "distribution.top": ["không phải một đầu ra đã lấy mẫu"],
        "attention_warning.text": ["không tự động là nguyên nhân"],
        "scenario.mask.note": ["ràng buộc phụ thuộc tự hồi quy"],
        "scenario.explanation.note": ["phản ví dụ chẩn đoán", "không phải một lời giải thích nhân quả đầy đủ"],
        "misconception.4.response": ["không thực hiện yêu cầu mạng"],
        "misconception.5.response": ["ràng buộc cấu trúc"],
        "misconception.7.response": ["hai việc khác nhau"],
    }
    es_precision = {
        "boundary.text": ["modelo de juguete determinista", "no constituyen una explicación general"],
        "distribution.top": ["no una salida muestreada"],
        "attention_warning.text": ["no es automáticamente la causa"],
        "scenario.mask.note": ["restricción de dependencia autorregresiva"],
        "scenario.explanation.note": ["contraejemplo diagnóstico", "no una explicación causal completa"],
        "misconception.4.response": ["no realiza ninguna solicitud de red"],
        "misconception.5.response": ["restricción estructural"],
        "misconception.7.response": ["son cosas distintas"],
    }
    for key, phrases in vi_precision.items():
        for phrase in phrases:
            check(phrase.lower() in vi[key].lower(), f"required Vietnamese precision phrase missing at {key}: {phrase}")
    for key, phrases in es_precision.items():
        for phrase in phrases:
            check(phrase.lower() in es[key].lower(), f"required Spanish precision phrase missing at {key}: {phrase}")

    # Semantic traps: temperature must divide fixed logits; mask is structural;
    # the ablation remains explicitly diagnostic rather than a complete explanation.
    check("Chia các logits cố định cho một nhiệt độ cao hơn" in vi["challenge.4.explain"], "Vietnamese temperature explanation must say fixed logits are divided by higher temperature")
    check("Dividir logits fijos por una temperatura mayor" in es["challenge.4.explain"], "Spanish temperature explanation must say fixed logits are divided by higher temperature")
    check("không phải một lời giải thích nhân quả đầy đủ" in vi["scenario.explanation.note"], "Vietnamese ablation qualification weakened")
    check("no una explicación causal completa" in es["scenario.explanation.note"], "Spanish ablation qualification weakened")

    vi_forbidden = [
        "mô hình hiểu vì",
        "trọng số chú ý lớn nhất là nguyên nhân",
        "nhiệt độ thay đổi trọng số mô hình",
        "luôn chọn token có xác suất cao nhất",
    ]
    es_forbidden = [
        "el modelo entiende porque",
        "el mayor peso de atención es la causa",
        "la temperatura cambia los pesos del modelo",
        "siempre se elige el token más probable",
    ]

    # Misconception claim strings intentionally state false propositions so learners
    # can reject them. Forbidden wording must therefore be absent from explanatory,
    # instructional, and result text, not from the quoted misconception claims.
    vi_assertive_text = "\n".join(str(value) for key, value in vi.items() if not key.endswith(".claim"))
    es_assertive_text = "\n".join(str(value) for key, value in es.items() if not key.endswith(".claim"))
    for phrase in vi_forbidden:
        check(phrase.lower() not in vi_assertive_text.lower(), f"forbidden/weaker Vietnamese wording present outside a misconception claim: {phrase}")
    for phrase in es_forbidden:
        check(phrase.lower() not in es_assertive_text.lower(), f"forbidden/weaker Spanish wording present outside a misconception claim: {phrase}")

    # Ensure the four guided challenge contracts each retain Prompt -> prediction
    # -> mechanism -> explanation -> transfer semantics in both languages.
    for locale, loc in (("vi", vi), ("es", es)):
        for idx in range(1, 5):
            check(bool(loc[f"challenge.{idx}.prompt"].strip()), f"missing challenge prompt: {locale}:{idx}")
            check(bool(loc[f"challenge.{idx}.mechanism"].strip()), f"missing challenge mechanism: {locale}:{idx}")
            check(bool(loc[f"challenge.{idx}.explain"].strip()), f"missing challenge explanation: {locale}:{idx}")
            check(bool(loc[f"challenge.{idx}.transfer"].strip()), f"missing challenge transfer: {locale}:{idx}")

    payload = {
        "harness": "tools/test_transformer_vi_es_localization.py",
        "source_freeze_head": EN_FREEZE,
        "english_keys": len(en),
        "vietnamese_keys": len(vi),
        "spanish_keys": len(es),
        "vietnamese_diacritics": len(VI_DIACRITIC_RE.findall(vi_text)),
        "spanish_diacritics": len(ES_DIACRITIC_RE.findall(es_text)),
        "checks": checks,
        "failed": len(failures),
        "pass": not failures,
        "failures": failures,
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    for failure in failures:
        print("FAIL: " + failure, file=sys.stderr)
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
