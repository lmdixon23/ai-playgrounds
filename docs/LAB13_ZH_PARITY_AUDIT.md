# Lab 13 Simplified Chinese Semantic Parity Audit

Status: **Simplified-Chinese semantic-catalog parity candidate**. This gate becomes effective only when the exact branch head containing the catalog, this audit, the dedicated parity harness, and the permanent workflow step receives a complete `Verify` PASS.

English source freeze: `e89c0b5d8b166b66407fc018deb1b7eec485b6a4`.

Scope: `tools/transformer_language_model_locales.json`, specifically the `en` and `zh` semantic catalogs. This checkpoint does **not** yet claim four-locale browser integration or public Lab 13 release readiness.

## 1. Translation policy

English remains the semantic source of truth. Simplified Chinese is translated against that frozen source rather than against a moving browser implementation.

The catalog deliberately separates **learner-interface prose** from **model data**:

- learner-interface prose is translated;
- prepared prompt strings such as `I like cats` remain unchanged;
- toy-vocabulary token strings and special tokens such as `<BOS>` and `<UNK>` remain unchanged;
- mathematical and code-facing symbols such as `Q`, `K`, `V`, `q`, `k`, `v`, `softmax`, `logits`, `d_k`, and `alpha_j v_j` remain stable where translation would weaken correspondence with equations or executable state.

This policy prevents localization from silently changing the deterministic toy-model inputs or arithmetic.

## 2. Technical terminology decisions

The Simplified-Chinese catalog uses terminology consistent with contemporary Chinese-language Transformer instruction while keeping the applet's exact mechanism boundaries explicit:

- token → **词元**;
- embedding → **嵌入**;
- position vector / position information → **位置向量 / 位置信息**;
- self-attention → **自注意力**;
- query / key / value → **查询 / 键 / 值**;
- scaled score → **缩放分数**;
- causal mask → **因果掩码**;
- autoregressive → **自回归**;
- attention weight → **注意力权重**;
- temperature → **温度**;
- feed-forward transform → **前馈变换**;
- residual path → **残差路径**.

`softmax` and `logits` remain as technical identifiers in the explanatory text. The surrounding Chinese prose explains their role rather than replacing them with terminology that could become ambiguous relative to the displayed calculation.

## 3. Semantic invariants preserved

The translation retains all source-level epistemic and pedagogical constraints:

1. The model is explicitly a deterministic **toy model**, not a pretrained frontier LLM.
2. Attention weights are numeric mixing coefficients and are **not** presented as a general explanation of reasoning or understanding.
3. The largest attention weight is not equated with the cause of the prediction.
4. The causal mask remains a **structural constraint** on permitted source positions.
5. Removing the causal mask is identified as violating the relevant **autoregressive dependency constraint**.
6. Temperature rescales fixed logits before softmax and does not retrain the model or alter learned weights.
7. The displayed top-probability token is explicitly distinguished from a sampled generation output.
8. The applet is stated to make no network or retrieval request.
9. The tokenizer remains qualified as a source-locked teaching fixture rather than a universal tokenizer.
10. The finite-ablation attention counterexample remains a **diagnostic counterexample**, not a complete causal explanation.

## 4. Guided Challenge parity

All four Guided Challenges have one-to-one semantic keys in English and Simplified Chinese:

- highest permitted attention;
- causal-mask leakage;
- token substitution with both Q/K/V scope and probability-direction prediction;
- temperature transfer.

Placeholders carrying numeric evidence are identical across locales. Challenge model-data options (`<BOS>`, `i`, `like`, `cats`) remain byte-for-byte identical so a locale switch cannot alter the deterministic fixture.

## 5. Adversarial machine gate

`tools/test_transformer_zh_localization.py` verifies at minimum:

- the catalog is bound to the accepted English freeze head;
- exact EN/ZH key parity;
- nonempty values;
- exact placeholder-set parity for every key;
- substantial Simplified-Chinese learner-facing content;
- required Transformer terminology;
- preservation of protected mathematical/model symbols;
- unchanged model-data challenge options;
- preservation of the evidence boundary, structural-mask language, no-network statement, attention-not-explanation qualification, and top-probability-versus-sampling distinction;
- the temperature mechanism states that fixed logits are **divided by** the higher temperature rather than using an ambiguous transformation verb;
- rejection of known weaker or misleading formulations.

A generic dictionary-coverage check is not sufficient for this gate; the harness contains semantic traps aimed at the claims most likely to become misleading under translation.

## 6. Review policy

No external colleague cold pass is required for Lab 13. Translation and adversarial semantic review are performed within the project. Technical terminology is cross-checked when uncertainty is material, then locked into machine-testable invariants where feasible.

This does not convert machine checks into a claim of universal translation quality. It establishes bounded semantic parity for the frozen Lab 13 teaching contract.

## 7. Acceptance decision

**Candidate acceptance: HOLD pending exact-head `Verify`.**

If the exact head containing this audit and the dedicated Simplified-Chinese semantic-catalog test passes the complete permanent workflow, EN/ZH catalog semantic parity is accepted and the project may proceed to Vietnamese and Spanish catalogs.

Any failure in the dedicated test or inherited workflow leaves this gate ineffective. The defect must be corrected without weakening the English source contract merely to obtain a pass.

## 8. Remaining localization/release work

After this gate passes:

1. translate the same frozen catalog into Vietnamese and Spanish;
2. run exact key/placeholder/protected-symbol parity and separate in-project adversarial semantic audits for VI/ES;
3. integrate EN/ZH/VI/ES into a single offline browser candidate while preserving experiment and Guided Challenge state across locale switches;
4. verify that locale switching cannot mutate toy-model arithmetic;
5. only then move Lab 13 into the public `playgrounds/` boundary and update navigation, curriculum, sitemap, applet inventory, and v1.2 release metadata;
6. run the complete cumulative v1.2 release gate before any merge/tag/release action.
