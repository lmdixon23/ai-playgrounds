# Lab 13 Vietnamese and Spanish Semantic Audit

Status: **PASS — VI/ES semantic-catalog parity accepted**.

English source freeze: `e89c0b5d8b166b66407fc018deb1b7eec485b6a4`.

Accepted EN/ZH catalog parity receipt: `f550b21d37951a511c4b311b33981284fd4f9d8f`, `Verify` run #120 (`32730071342`) PASS.

Accepted VI/ES semantic-catalog receipt: `84a027795beed4b03df2af056a4ac1c68eab356e`, `Verify` run #131 (`32731989720`) PASS. The permanent workflow passed every inherited v1.1 gate, all Lab 13 reference/prototype/English/ZH gates, the newly registered VI/ES semantic gate, and the full browser/responsive suite.

Scope: `tools/transformer_language_model_locales_vi_es.json` against the English key set in `tools/transformer_language_model_locales.json`. This checkpoint covers semantic catalogs only; multilingual browser integration remains a separate gate.

## 1. Review method

Vietnamese and Spanish were translated directly within the project from the frozen English semantics. No external colleague cold pass is required.

The review used four layers:

1. direct key-by-key translation from the English source freeze;
2. technical-terminology cross-checking where the Vietnamese or Spanish term could materially change the mechanism described;
3. a manual adversarial reread focused on evidence boundaries, causal-mask semantics, temperature, sampling, Q/K/V, and the attention-not-explanation counterexample;
4. a machine gate enforcing key, placeholder, protected-symbol, terminology, and claim-level invariants.

The purpose is bounded semantic parity, not a claim that every possible regional style preference has been optimized.

## 2. Model-data and symbol policy

The same non-translation boundary used for Simplified Chinese applies to Vietnamese and Spanish:

- prepared model prompts such as `I like cats` remain unchanged;
- toy-vocabulary token strings remain unchanged;
- `<BOS>` and `<UNK>` remain unchanged;
- `Q`, `K`, `V`, `q`, `k`, `v`, `q[0]`, `k[0]`, `softmax`, `logits`, `P(sleep)`, and `alpha_j v_j`-style mathematical identifiers remain stable where they are part of the displayed model calculation.

Learner-interface prose surrounding those tokens is translated. This prevents a localization change from becoming a model-input change.

## 3. Vietnamese terminology decisions

The catalog uses:

- self-attention → **tự chú ý**;
- query / key / value → **truy vấn / khóa / giá trị**;
- embedding vector → **vector nhúng / embedding** where correspondence to the technical term is useful;
- position vector → **vector vị trí**;
- causal mask → **mặt nạ nhân quả**;
- autoregressive → **tự hồi quy**;
- attention weight → **trọng số chú ý**;
- feed-forward transform → **biến đổi feed-forward**;
- residual path → **đường / kết nối phần dư**;
- temperature → **nhiệt độ**.

For scaled dot-product attention, the prose describes the arithmetic directly (`q·k / sqrt(d_k)`) and uses **điểm đã chia tỉ lệ** rather than introducing a less transparent synonym.

## 4. Spanish terminology decisions

The catalog uses:

- self-attention → **autoatención**;
- query / key / value → **consulta / clave / valor**;
- embedding vector → **vector de embedding**;
- position vector → **vector de posición**;
- causal mask → **máscara causal**;
- autoregressive → **autorregresivo / autorregresiva**;
- attention weight → **peso de atención**;
- feed-forward transform → **transformación feed-forward**;
- residual path → **ruta residual**;
- temperature → **temperatura**;
- scaled score → **puntuación escalada**.

`softmax` and `logits` remain technical identifiers, with their role explained in the surrounding Spanish prose.

## 5. High-risk semantic claims preserved

Both catalogs explicitly preserve the following source claims:

1. The applet is a deterministic toy model, not a pretrained frontier LLM.
2. Attention weights show a numeric mixing mechanism and are not a general explanation of reasoning or understanding.
3. The largest attention weight is not automatically the cause of a final logit.
4. The causal mask is a structural constraint on permitted source positions.
5. Mask removal creates an autoregressive dependency violation for the tested earlier position.
6. Temperature acts on fixed logits before softmax and does not retrain the model or change learned weights.
7. Raising temperature divides the fixed logits by a larger temperature and flattens the tested distribution.
8. The top-probability token shown in the panel is not the same thing as a sampled generation output.
9. The applet performs no network request or retrieval call.
10. The tokenizer is a source-locked teaching fixture, not a universal tokenizer.
11. The `sleep sleep i` finite ablation is a diagnostic counterexample to “largest attention = cause,” not a complete causal explanation.

## 6. Guided Challenge parity

All four challenge families preserve the frozen sequence:

`Prompt -> Commit prediction -> Reveal mechanism -> Compare -> Explain -> Transfer`

The machine catalog keeps separate semantic keys for prompt, mechanism, explanation, and transfer in both VI and ES. Numeric placeholders are required to match English exactly.

The token-substitution challenge retains its two-part requirement: predict both the Q/K/V scope of the substitution and the direction of the named `P(sleep)` change.

## 7. Dedicated adversarial machine gate

`tools/test_transformer_vi_es_localization.py` verifies:

- source-freeze binding;
- exact VI/ES key parity against frozen English;
- nonempty values;
- exact placeholder-set parity per key;
- substantial locale-native orthography;
- required Vietnamese and Spanish Transformer terminology;
- protected symbols and model-data tokens;
- byte-identical challenge model-token options;
- evidence-boundary language;
- structural causal-mask semantics;
- autoregressive leak semantics;
- top-probability versus sampling distinction;
- no-network claim;
- diagnostic-ablation qualification;
- explicit division of fixed logits by higher temperature;
- all four prompt/mechanism/explain/transfer challenge components;
- rejection of known stronger or misleading phrasings outside intentionally false misconception claims.

The first permanent VI/ES workflow run exposed a validator-scope defect: the forbidden-phrase scan also inspected the quoted misconception claims, where false propositions are intentionally stated so learners can reject them. The validator was corrected to keep the prohibition on explanatory, instructional, and result text while excluding only keys ending in `.claim`. No semantic requirement was weakened. Run #131 then passed all 794 VI/ES checks.

A failure is to be corrected in the catalog or implementation. The semantic requirements are not to be weakened merely to make the gate pass.

## 8. Acceptance decision

**PASS.**

The complete permanent workflow passed at exact semantic head `84a027795beed4b03df2af056a4ac1c68eab356e`; VI/ES semantic-catalog parity is accepted.

The next task is a single offline four-locale browser candidate with state-preserving locale switching and arithmetic-invariance tests. Public `playgrounds/` integration remains blocked until that browser gate passes.
