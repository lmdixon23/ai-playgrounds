# Lab 13 English Source Audit

Status: **English semantic/source freeze candidate**. The freeze becomes effective only if the exact branch head containing this audit passes the complete permanent `Verify` workflow.

Scope: `tools/transformer_language_model_applet_en.html` on the clean post-v1.1 Lab 13 branch.

This audit compares the English candidate against the frozen mechanism contract in `docs/LAB13_TRANSFORMER_LANGUAGE_MODEL_ARCHITECTURE.md`. It distinguishes semantic/source readiness from later localization, public-suite integration, and release readiness.

## 1. Implemented English mechanism boundary

The candidate now closes the English-only implementation obligations needed before localization:

1. **Single-file offline operation.** The HTML embeds its deterministic JavaScript model and has no external script, fetch, XHR, backend, account, or API dependency.
2. **Frozen arithmetic preserved.** The embedded base model uses the same vocabulary, embeddings, position vectors, Q/K/V projections, feed-forward transform, output projection, causal mask, stable softmax, and temperature operation as the independently tested reference core.
3. **Visible causal pipeline.** Learners can inspect surface text, toy token IDs, token embedding, position vector, input vector, Q/K/V values, masked/unmasked scaled scores, attention weights, attention output, final state, logits, and next-token probabilities.
4. **Score, mask, and attention separation.** The pre-mask scaled-score matrix, structural causal-mask matrix, and post-softmax attention-weight matrix are three separate synchronized views. Attention cells display numeric weights while redundant intensity encoding assists visual scanning, so color is not the sole information channel.
5. **Numeric pair inspection.** Selecting a permitted attention cell reports the raw `q·k` dot product, scaled `q·k / sqrt(d_k)` score, and final attention weight for that destination/source pair.
6. **Constrained learner text.** A bounded text path demonstrates the source-locked toy tokenizer, `<UNK>` mapping, punctuation tokenization, and maximum-context truncation while preserving `<BOS>`.
7. **Structural causal masking.** Future cells are rendered as `MASK`; the source explicitly avoids anthropomorphizing masking as a model choosing not to look.
8. **Bounded Q/K perturbation.** The learner can alter one final-query or source-key component by a fixed `+0.50` perturbation and inspect the resulting scaled-score and attention-weight change.
9. **Order/position ablation.** The candidate compares a token swap with position information on versus off and reports the resulting maximum probability delta.
10. **Mask leakage.** An earlier destination can be inspected with the mask disabled; the interface reports the resulting future-source attention mass and identifies the autoregressive dependency violation.
11. **Temperature transfer.** The source compares distribution entropy while preserving logits and explicitly states that temperature does not retrain the model.
12. **Executable attention-not-explanation counterexample.** For `sleep sleep i`, the largest final-row attention weight and the largest finite-ablation effect on the original top-token logit occur at different source positions. The finite ablation removes one `alpha_j v_j` contribution without renormalization and is explicitly scoped as a diagnostic counterexample rather than a complete causal explanation.
13. **All four frozen Guided Challenges.** Highest attention, causal-mask leak, token substitution, and temperature transfer each use an isolated deterministic fixture and enforce `Prompt -> Commit prediction -> Reveal mechanism -> Compare -> Explain -> Transfer`. The substitution challenge requires both the Q/K/V change scope and the direction of a named next-token probability.
14. **Challenge-state isolation.** Prediction choices and reveals are generated from the same fixed challenge fixture rather than from arbitrary experiment state.
15. **Keyboard-operable attention inspection.** Every permitted weight cell is a button; keyboard activation updates the synchronized token/vector/text state and reports the selected query-key calculation.
16. **Text-equivalent numeric state.** The candidate exposes prompt, tokens, IDs, selected token, query, source keys, raw scaled scores, structural mask row, masked/unmasked scores, attention row, logits, probabilities, temperature, position state, mask state, and Q/K perturbation as text.
17. **Explicit evidence boundaries and misconception corrections.** The source rejects frontier-model equivalence, attention-as-understanding/explanation, internet-search behavior, stored-answer retrieval, token-equals-word, position-equals-word-meaning, deterministic top-token selection, and temperature-changes-weights interpretations.
18. **Literal special-token rendering.** `<BOS>` and `<UNK>` are inserted as DOM text rather than HTML so special-token labels remain visible in token controls, matrix headers, and the vocabulary distribution.

## 2. Adversarial corrections completed since the first English candidate

The first audit placed source freeze on HOLD for six material blockers. All six are now closed:

- **A — Q/K perturbation:** closed by explicit query/key component perturbation and browser regression coverage.
- **B — attention-not-explanation counterexample:** closed by the executable `sleep sleep i` finite-ablation fixture.
- **C — Guided Challenges 2–4:** closed; all four architecture-frozen challenges are implemented.
- **D — challenge fixture mismatch:** closed by isolating each prediction/reveal pair from arbitrary experiment/scenario state.
- **E — constrained text input:** closed with `<UNK>`, punctuation, and max-context behavior.
- **F — keyboard attention-cell inspection:** closed by permitted-cell controls plus synchronized pair detail.

A subsequent frozen-contract review identified two additional gaps before accepting the freeze candidate. Both are now closed:

- **G — score/mask separation:** closed by separate scaled-score, mask, and attention matrices.
- **H — two-part substitution challenge:** closed by requiring prediction of both projected Q/K/V scope and named probability direction.

The first full candidate gate then exposed one rendering defect: special tokens written through `innerHTML` were parsed as element names and disappeared visually. That was treated as an applet defect rather than weakening the test. It is now closed by DOM-safe literal text construction across token controls, matrix headers, and vocabulary labels.

## 3. Verification boundary

`tools/test_transformer_english_applet.py` adversarially checks at minimum:

- source/evidence contracts;
- single-file and no-network constraints;
- canonical embedded-core arithmetic;
- distinct full score, mask, and attention matrices;
- causal-mask rendering and mask-off behavior;
- keyboard attention-cell inspection including raw and scaled dot products;
- required text-equivalent state;
- unknown-token and context-truncation behavior, which also regression-test visible `<UNK>` and `<BOS>` rendering;
- Q/K perturbation arithmetic;
- order/position ablation;
- mask leakage;
- temperature/logit invariance;
- the finite-ablation attention counterexample;
- fixture isolation and prediction-before-reveal for all four Guided Challenges;
- the two-part Q/K/V-scope plus probability-direction substitution challenge;
- bounded mobile document width.

This candidate is accepted as the **English semantic/source freeze** only when the exact head containing the candidate, this audit, its QA harness, and the permanent workflow change receives a complete `Verify` PASS. A failure leaves the freeze ineffective and must be corrected before any ZH/VI/ES semantic translation work begins.

## 4. Deliberately unresolved work after English freeze

The following items remain required for Lab 13 release readiness and are deliberately not part of the English source-freeze gate:

1. Simplified-Chinese translation and separate semantic parity audit.
2. Vietnamese and Spanish translation catalogs, machine parity/state tests, and a separate adversarial semantic review pass performed within the project. No external colleague cold pass is required.
3. Four-locale browser state preservation and arithmetic-invariance testing.
4. Public `playgrounds/` integration only after localization acceptance.
5. Navigation, `applets.json`, curriculum, sitemap, release metadata, and deployment-boundary expansion from twelve to thirteen applets.
6. Full public mobile/tablet/desktop QA after integration.
7. v1.2 release/tag/DOI actions only after the cumulative v1.2 release gate passes.

## 5. Deployment and provenance decision

The English candidate remains under `tools/`, so the public Pages boundary continues to contain exactly the existing twelve applets. No public Lab 13 deployment, version tag, release, DOI mutation, or Paper 7 change is authorized by this checkpoint.
