# R4 Vietnamese and Spanish Semantic Translation Audit

Status: assistant-led semantic review for v1.1.0 R4

Bound source branch: `feature/v1.1.0-vi-es-localization-r4`

This audit replaces the earlier planned external-review handoff at the repository owner's request. It is not represented as a native-speaker or independent human review. The goal is narrower and explicit: inspect the generated Vietnamese and Spanish learner-facing text against the frozen English meaning, correct material semantic mistranslations, and lock high-risk terminology into a reviewed override layer with regression checks.

## Review method

1. Treat the frozen English/R3 mechanism wording as the semantic source of truth.
2. Inspect all twelve R4 locale catalogs, concentrating first on terminology whose mistranslation changes the algorithm, probability statement, epistemic strength, or learner task.
3. Cross-check uncertain technical terms against established Vietnamese and Spanish educational/scientific usage.
4. Put reviewed corrections in `assets/locales/common-r4.js`. The runtime intentionally gives this reviewed common layer precedence over applet-local generated drafts.
5. Strengthen `tools/verify_r4_locale_catalog.py` so its static model uses the same precedence as the browser runtime and rejects untranslated English prose that merely exists as an identity mapping.
6. Keep applet-local generated catalogs as provenance/inventory; reviewed common mappings are the final semantic override for covered strings.

## Material problems found in the machine draft

The audit found errors that coverage-only QA could not detect. Examples include:

- Vietnamese search translated *frontier state* as `trạng thái biên giới`, which reads like a geopolitical border rather than a search frontier.
- Vietnamese hill-climbing translated *tour cost* as `chi phí chuyến tham quan`, which means the cost of a sightseeing trip rather than the optimization route/tour.
- Vietnamese SAT translated logical *literal* as ordinary `nghĩa đen` in some learner text and translated assignment as `bài tập` in some contexts.
- Vietnamese neural-network text translated *epoch* as `kỷ nguyên` and *loss plateaus* with wording implying instability rather than loss leveling off.
- Vietnamese Q-learning translated *agent* as `nhân viên`, *goal* as `bàn thắng`, and long-term *return* as financial profit in some generated text.
- Vietnamese KNN used generic `số liệu` for distance metric and person-neighbor wording where mathematical neighbors were intended.
- Vietnamese Bayesian-network text rendered directed acyclic graph incorrectly and weakened parent/posterior terminology.
- Spanish repeated-test Bayes text rendered “posterior >99%” as `empuja hacia atrás >99%`.
- Spanish Bayesian-network text used `variable principal` for parent variable and had literal machine phrases such as `Terremoto de abrazadera` for “Clamp Earthquake”.
- Multiple catalogs contained English prose mapped to itself. Static source coverage alone therefore overstated translation completeness.

## Reviewed terminology decisions

### Vietnamese

- prior probability: `xác suất tiên nghiệm`
- posterior probability: `xác suất hậu nghiệm`
- odds: `tỷ suất chênh`
- likelihood ratio: `tỷ số khả dĩ`
- conditional independence: `độc lập có điều kiện`
- directed acyclic graph: `đồ thị có hướng không chu trình`
- parent variable: `biến cha`
- explaining away: `giải thích triệt tiêu (explaining away)`
- CNF: `dạng chuẩn hội`
- literal: retain the technical word `literal`, with Vietnamese definition on first explanatory use
- satisfiability: `tính thỏa được`
- simulated annealing: `mô phỏng luyện kim`
- distance metric: `độ đo khoảng cách`
- feature scaling: `co giãn đặc trưng`
- validation set/error: `tập xác thực` / `lỗi xác thực`
- affine: `affine` / `biến đổi affine`
- cross-correlation: `tương quan chéo`
- reinforcement-learning agent: `tác nhân`
- return: `tổng phần thưởng` where the reinforcement-learning meaning is intended
- moving window: `cửa sổ trượt`

### Spanish

- prior probability: `probabilidad a priori`
- posterior probability: `probabilidad posterior`
- odds: `odds` / `momios` only where needed for the explicit mathematical object; explanatory prose avoids mistranslating it as a generic probability
- likelihood ratio: `razón de verosimilitud`
- conditional independence: `independencia condicional`
- directed acyclic graph: `grafo acíclico dirigido`
- parent variable: `variable padre`
- explaining away: `explaining away` with `explicación por descarte` as the explanatory gloss
- CNF: `forma normal conjuntiva`
- literal: `literal`
- satisfiability: `satisfacibilidad`
- simulated annealing: `recocido simulado`
- distance metric: `métrica de distancia`
- feature scaling: `escalado de características`
- validation set/error: `conjunto de validación` / `error de validación`
- affine: `afín`
- cross-correlation: `correlación cruzada`
- reinforcement-learning agent: `agente`
- return: `retorno acumulado`
- moving window: `ventana móvil`

## Terminology cross-checks

Terminology was cross-checked against established usage in Vietnamese AI/logic/probability teaching material and Spanish probability/AI/logic sources. In particular:

- Vietnamese AI lecture material uses `dạng chuẩn hội (CNF)` and retains `literal` as the logic term.
- Vietnamese Bayesian-network teaching material uses conditional-independence and parent-variable terminology consistent with `độc lập có điều kiện` and `biến cha`.
- Vietnamese probability/clinical-statistics material uses prior/posterior probability and likelihood-ratio terminology consistent with `xác suất tiên nghiệm`, `xác suất hậu nghiệm`, `tỷ suất chênh`, and `tỷ số khả dĩ`.
- Vietnamese deep-learning material distinguishes `tương quan chéo` from `tích chập`.
- Spanish logic material uses `forma normal conjuntiva`, `cláusula`, `literal`, and `satisfacibilidad`.
- Spanish Bayesian-network material uses `independencia condicional`, `variable padre`, and DAG terminology.
- Spanish optimization material uses `recocido simulado`.
- Spanish medical/probability material uses `razón de verosimilitud`, sensitivity/specificity, and prior/posterior probability terminology.

## Regression boundary

R4 is not considered ready merely because every English source has a dictionary key. The final gate must establish:

- no missing rendered VI/ES source translations;
- no nontrivial rendered English prose left as an identity translation unless explicitly classified as a language-invariant technical label;
- reviewed common terminology overrides applet-local machine drafts in both static verification and browser runtime;
- Wumpus dynamic percept strings remain fully localized;
- all pre-existing pedagogical, Guided Challenge, Simplified-Chinese, algorithm, deployment, and responsive-browser gates remain green.

This audit does not claim independent native-speaker certification. It records an assistant-led semantic and terminology review requested by the repository owner.
