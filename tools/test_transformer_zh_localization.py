#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CATALOG = ROOT / "tools" / "transformer_language_model_locales.json"
EN_FREEZE = "e89c0b5d8b166b66407fc018deb1b7eec485b6a4"
PLACEHOLDER_RE = re.compile(r"\{([A-Za-z0-9_]+)\}")
CJK_RE = re.compile(r"[\u3400-\u9fff]")


def placeholders(text: str) -> set[str]:
    return set(PLACEHOLDER_RE.findall(text))


def main() -> int:
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    failures: list[str] = []
    checks = 0

    def check(ok: bool, message: str) -> None:
        nonlocal checks
        checks += 1
        if not ok:
            failures.append(message)

    check(data.get("schema") == "ai-playgrounds-lab13-locales-v1", "unexpected localization schema")
    check(data.get("source_freeze_head") == EN_FREEZE, "catalog is not bound to the accepted English freeze head")
    locales = data.get("locales", {})
    check(set(locales) == {"en", "zh"}, f"expected exactly EN+ZH at this gate, got {sorted(locales)}")
    en = locales.get("en", {})
    zh = locales.get("zh", {})
    check(len(en) >= 120, f"English catalog unexpectedly small: {len(en)} keys")
    check(set(en) == set(zh), f"EN/ZH key mismatch: missing_zh={sorted(set(en)-set(zh))}, extra_zh={sorted(set(zh)-set(en))}")

    for key in sorted(set(en) | set(zh)):
        if key not in en or key not in zh:
            continue
        check(bool(str(en[key]).strip()), f"empty English value: {key}")
        check(bool(str(zh[key]).strip()), f"empty Chinese value: {key}")
        check(placeholders(str(en[key])) == placeholders(str(zh[key])), f"placeholder mismatch at {key}: EN={sorted(placeholders(str(en[key])))}, ZH={sorted(placeholders(str(zh[key])))}")

    zh_text = "\n".join(str(v) for v in zh.values())
    cjk_count = len(CJK_RE.findall(zh_text))
    check(cjk_count >= 1800, f"unexpectedly little Simplified-Chinese learner-facing content: {cjk_count} CJK chars")

    required_terms = [
        "词元",
        "嵌入",
        "位置向量",
        "自注意力",
        "查询",
        "键",
        "值",
        "缩放分数",
        "因果掩码",
        "自回归",
        "注意力权重",
        "温度",
        "前馈",
        "残差路径",
        "softmax",
        "logits",
    ]
    for term in required_terms:
        check(term in zh_text, f"required Chinese technical term missing: {term}")

    # Keep mathematical/code symbols and model-data tokens aligned across locales.
    protected = ["<BOS>", "<UNK>", "softmax", "logits", "Q/K/V", "q[0]", "k[0]", "P(sleep)", "αⱼvⱼ"]
    for token in protected:
        en_keys = [key for key, value in en.items() if token in str(value)]
        for key in en_keys:
            check(token in str(zh[key]), f"protected token {token!r} changed or disappeared at {key}")

    for key in ["challenge.1.option0", "challenge.1.option1", "challenge.1.option2", "challenge.1.option3"]:
        check(en[key] == zh[key], f"model-data challenge option must remain identical across EN/ZH: {key}")

    required_precision = {
        "boundary.text": ["确定性的玩具模型", "不能作为对模型推理或理解过程的一般性解释"],
        "distribution.top": ["不代表一次采样输出"],
        "attention_warning.text": ["并不自动等于"],
        "scenario.mask.note": ["自回归依赖约束"],
        "scenario.explanation.note": ["诊断性反例", "并不是完整的因果解释"],
        "misconception.2.response": ["不能直接读出模型的理解"],
        "misconception.7.response": ["概率分布与生成时的选择规则是两回事"],
    }
    for key, phrases in required_precision.items():
        for phrase in phrases:
            check(phrase in zh[key], f"required precision phrase missing at {key}: {phrase}")

    forbidden = [
        "去除固定 logits",
        "注意力权重就是原因",
        "一定会选择概率最高",
        "Transformer 会自动上网",
        "温度会改变模型权重",
    ]
    for phrase in forbidden:
        check(phrase not in zh_text, f"forbidden/weaker Chinese wording present: {phrase}")

    # Specific semantic traps that generic key/placeholder parity would miss.
    check("将固定 logits 除以更高的温度" in zh["challenge.4.explain"], "temperature explanation must say logits are divided by higher temperature")
    check("结构性约束" in zh["misconception.5.response"], "causal mask must remain a structural constraint")
    check("不会发出网络请求" in zh["misconception.4.response"], "no-network evidence boundary weakened")
    check("受源文本约束" in zh["tokenizer.note"], "toy tokenizer source-lock qualification missing")

    payload = {
        "harness": "tools/test_transformer_zh_localization.py",
        "catalog": str(CATALOG.relative_to(ROOT)),
        "source_freeze_head": EN_FREEZE,
        "english_keys": len(en),
        "chinese_keys": len(zh),
        "cjk_chars": cjk_count,
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
