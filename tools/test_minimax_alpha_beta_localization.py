#!/usr/bin/env python3
"""Static semantic-contract gate for the Lab 15 EN/ZH/VI/ES catalogs."""

from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
FREEZE = "f904e6d68f71602dced73e99d259eee055899bc2"
FILES = {
    locale: ROOT / "tools" / f"minimax_alpha_beta_locale_{locale}.json"
    for locale in ("en", "zh", "vi", "es")
}
FRAGMENTS = ROOT / "tools" / "minimax_alpha_beta_locale_fragments.json"
PLACEHOLDER_RE = re.compile(r"\{([A-Za-z0-9_]+)\}")
CJK_RE = re.compile(r"[\u3400-\u9fff]")
VIET_RE = re.compile(r"[ăâđêôơưĂÂĐÊÔƠƯàáảãạằắẳẵặầấẩẫậèéẻẽẹềếểễệìíỉĩịòóỏõọồốổỗộờớởỡợùúủũụừứửữựỳýỷỹỵ]", re.I)
SPANISH_RE = re.compile(r"[áéíóúüñ¿¡]", re.I)


def placeholders(value: str) -> set[str]:
    return set(PLACEHOLDER_RE.findall(value))


def load(locale: str) -> dict[str, str]:
    data = json.loads(FILES[locale].read_text(encoding="utf-8"))
    if data.get("schema") != "ai-playgrounds-lab15-locale-v1":
        raise RuntimeError(f"unexpected Lab 15 locale schema: {locale}")
    if data.get("source_freeze_head") != FREEZE:
        raise RuntimeError(f"Lab 15 locale is not bound to R4 freeze: {locale}")
    if data.get("locale") != locale:
        raise RuntimeError(f"locale self-identifier mismatch: {locale}")
    strings = data.get("strings")
    if not isinstance(strings, dict):
        raise RuntimeError(f"locale strings missing: {locale}")
    return {str(key): str(value) for key, value in strings.items()}


def load_fragments() -> dict[str, dict[str, str]]:
    data = json.loads(FRAGMENTS.read_text(encoding="utf-8"))
    if data.get("schema") != "ai-playgrounds-lab15-locale-fragments-v1":
        raise RuntimeError("unexpected Lab 15 fragment schema")
    if data.get("source_freeze_head") != FREEZE:
        raise RuntimeError("Lab 15 fragments are not bound to the R4 freeze")
    locales = data.get("locales")
    if not isinstance(locales, dict) or set(locales) != set(FILES):
        raise RuntimeError("Lab 15 fragment locale set mismatch")
    return {
        locale: {str(key): str(value) for key, value in strings.items()}
        for locale, strings in locales.items()
    }


def main() -> int:
    catalogs = {locale: load(locale) for locale in FILES}
    fragments = load_fragments()
    for locale in catalogs:
        overlap = set(catalogs[locale]) & set(fragments[locale])
        if overlap:
            raise RuntimeError(f"duplicate base/fragment keys for {locale}: {sorted(overlap)}")
        catalogs[locale].update(fragments[locale])

    en = catalogs["en"]
    failures: list[str] = []
    checks = 0

    def check(ok: bool, message: str) -> None:
        nonlocal checks
        checks += 1
        if not ok:
            failures.append(message)

    check(len(en) >= 120, f"English presentation catalog unexpectedly small: {len(en)}")
    for locale, catalog in catalogs.items():
        check(
            set(catalog) == set(en),
            f"key mismatch for {locale}: missing={sorted(set(en)-set(catalog))}, extra={sorted(set(catalog)-set(en))}",
        )
        for key in sorted(en):
            if key not in catalog:
                continue
            check(bool(catalog[key].strip()), f"empty value: {locale}:{key}")
            check(
                placeholders(en[key]) == placeholders(catalog[key]),
                f"placeholder mismatch at {locale}:{key}: EN={sorted(placeholders(en[key]))}, target={sorted(placeholders(catalog[key]))}",
            )

    zh_text = "\n".join(catalogs["zh"].values())
    vi_text = "\n".join(catalogs["vi"].values())
    es_text = "\n".join(catalogs["es"].values())
    cjk_chars = len(CJK_RE.findall(zh_text))
    vi_diacritics = len(VIET_RE.findall(vi_text))
    es_diacritics = len(SPANISH_RE.findall(es_text))
    check(cjk_chars >= 950, f"unexpectedly little Simplified-Chinese content: {cjk_chars}")
    check(vi_diacritics >= 700, f"unexpectedly little Vietnamese content: {vi_diacritics}")
    check(es_diacritics >= 80, f"unexpectedly little Spanish content: {es_diacritics}")

    protected = ("MAX", "MIN", "Minimax", "Alpha-Beta", "alpha", "beta", "B1", "B2")
    for token in protected:
        for key, english in en.items():
            if token not in english:
                continue
            for locale in ("zh", "vi", "es"):
                check(
                    token in catalogs[locale][key],
                    f"protected token {token!r} changed or disappeared at {locale}:{key}",
                )

    for key in sorted(k for k in en if k.startswith("text.")):
        for locale in ("zh", "vi", "es"):
            check(
                catalogs[locale][key] == en[key],
                f"machine-state template changed at {locale}:{key}",
            )

    required_terms = {
        "zh": ("博弈树", "终局效用值", "剪枝", "最优行动集合", "完全信息"),
        "vi": ("cây trò chơi", "giá trị tiện ích", "cắt tỉa", "tập nước đi tối ưu", "thông tin hoàn hảo"),
        "es": ("árboles de juego", "utilidades terminales", "poda", "conjunto óptimo", "información perfecta"),
    }
    for locale, terms in required_terms.items():
        body = "\n".join(catalogs[locale].values()).lower()
        for term in terms:
            check(term.lower() in body, f"required technical term missing for {locale}: {term}")

    precision = {
        "zh": {
            "hero.boundary": ("算法未求值",),
            "panel.maxmin": ("alpha >= beta", "不会被算法求值"),
            "panel.order": ("不能改变", "精确 Minimax 值"),
            "state.not_claimed": ("不声称完整最优集合",),
            "challenge.prune.actual": ("B2", "算法不会对它求值"),
            "panel.cutoff.tail": ("不会被算法求值",),
        },
        "vi": {
            "hero.boundary": ("thuật toán không đánh giá",),
            "panel.maxmin": ("alpha >= beta", "không được thuật toán đánh giá"),
            "panel.order": ("không thể thay đổi", "giá trị Minimax chính xác"),
            "state.not_claimed": ("không khẳng định tập tối ưu đầy đủ",),
            "challenge.prune.actual": ("B2", "thuật toán không đánh giá nó"),
            "panel.cutoff.tail": ("không được thuật toán đánh giá",),
        },
        "es": {
            "hero.boundary": ("no evaluados por el algoritmo",),
            "panel.maxmin": ("alpha >= beta", "no son evaluados por el algoritmo"),
            "panel.order": ("No puede cambiar", "valor Minimax exacto"),
            "state.not_claimed": ("no afirma el conjunto óptimo completo",),
            "challenge.prune.actual": ("B2", "algoritmo no lo evalúa"),
            "panel.cutoff.tail": ("no son evaluados por el algoritmo",),
        },
    }
    for locale, per_key in precision.items():
        for key, phrases in per_key.items():
            for phrase in phrases:
                check(
                    phrase in catalogs[locale][key],
                    f"precision phrase missing at {locale}:{key}: {phrase}",
                )

    forbidden = {
        "zh": ("Alpha-Beta 近似", "先求值再隐藏", "行动顺序会改变 Minimax 值"),
        "vi": ("Alpha-Beta xấp xỉ", "đánh giá rồi ẩn", "thứ tự nước đi thay đổi giá trị Minimax"),
        "es": ("Alpha-Beta aproxima", "evaluados y luego ocultos", "el orden cambia el valor Minimax"),
    }
    for locale, phrases in forbidden.items():
        body = "\n".join(catalogs[locale].values()).lower()
        for phrase in phrases:
            check(phrase.lower() not in body, f"forbidden/weaker wording present for {locale}: {phrase}")

    payload = {
        "harness": "tools/test_minimax_alpha_beta_localization.py",
        "source_freeze_head": FREEZE,
        "keys_per_locale": len(en),
        "locales": sorted(catalogs),
        "cjk_chars": cjk_chars,
        "vietnamese_diacritics": vi_diacritics,
        "spanish_diacritics": es_diacritics,
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
