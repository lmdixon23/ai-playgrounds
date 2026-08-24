# Lab 13 English Source Audit

Status: **candidate implemented; English source is not frozen yet**.

Scope: `tools/transformer_language_model_applet_en.html` on the clean post-v1.1 Lab 13 branch.

This audit is deliberately stricter than a visual review. It compares the English candidate against the frozen mechanism contract in `docs/LAB13_TRANSFORMER_LANGUAGE_MODEL_ARCHITECTURE.md` and distinguishes implemented behavior from remaining acceptance work.

## 1. Current positive findings

The candidate now establishes the next implementation layer beyond the R1 foundation:

1. **Single-file offline candidate.** The HTML contains its deterministic JavaScript model directly and has no external script, fetch, XHR, backend, account, or API dependency.
2. **Frozen arithmetic preserved.** The embedded model uses the same vocabulary, embeddings, position vectors, Q/K/V projections, feed-forward transform, output projection, causal mask, stable softmax, and temperature operation as the reference core.
3. **Visible causal pipeline.** The learner can inspect token IDs, token embedding, position vector, input vector, Q/K/V values, attention row, attention output, final state, logits, and next-token probabilities.
4. **Causal mask is structural in the interface.** Future cells are rendered as `MASK`, rather than anthropomorphized as a model choosing not to look.
5. **Position ablation is numerically exposed.** The order scenario compares `I like cats` with `like i cats` and reports the maximum probability delta with position information on versus off.
6. **Mask leakage is numerically exposed.** The mask scenario selects an earlier destination and reports the nonzero future-source attention that appears when the mask is removed.
7. **Temperature is correctly scoped.** The candidate reports an entropy comparison while explicitly stating that temperature rescales fixed logits and does not retrain the model.
8. **Prediction-before-reveal exists for the first Guided Challenge.** The learner must commit before the canonical attention row and score row are revealed.
9. **Evidence boundaries and misconception corrections are explicit.** The source rejects frontier-model equivalence, attention-as-explanation, internet-search, stored-answer retrieval, token-equals-word, position-equals-meaning, and temperature-changes-weights interpretations.
10. **Text-equivalent numeric state exists.** Prompt, tokens, IDs, selected token, query, source keys, attention row, logits, probabilities, temperature, position state, and mask state are available as text.

## 2. Adversarial findings that block English source freeze

These are material blockers, not optional polish.

### A. Q/K perturbation scenario is not yet implemented

The architecture requires an experiment that changes one query/key component and lets the learner observe the resulting score and attention change. The candidate currently asks the learner to transfer toward such a perturbation, but it does not yet provide the control.

**Required correction:** add a bounded deterministic Q/K component perturbation with independent regression coverage.

### B. Attention-not-explanation needs an executable counterexample

The current candidate states the limitation correctly, but the dedicated scenario remains explanatory rather than computational. A stronger fixture has already been identified in the frozen toy model: for `sleep sleep i`, the largest final-row attention weight is on the final `i`, while finite ablation of an earlier `sleep` value contribution can change the top output logit more.

**Required correction:** encode this counterexample in the browser with clearly labeled finite-ablation semantics and state that the ablation itself is diagnostic, not a complete causal explanation.

### C. Guided Challenges 2–4 are absent

Only Challenge 1, highest permitted attention, is implemented.

Still required:

- causal-mask leak prediction;
- token-substitution direction prediction;
- temperature sharpness/flatness transfer prediction.

Each must preserve `Prompt -> Commit prediction -> Reveal mechanism -> Compare -> Explain -> Transfer`.

### D. Challenge state is not yet isolated from arbitrary scenario state

The reveal calculation for Challenge 1 is bound to the canonical `I like cats` fixture, while the prediction options are currently regenerated from the active experiment prompt. If a learner changes scenarios before entering the challenge, the option labels can cease to correspond to the canonical reveal fixture.

**Required correction:** either bind both prediction and reveal to an explicit challenge fixture or derive both from the same current state. This is a correctness blocker.

### E. Optional constrained text input is not yet implemented

The architecture permits prepared prompts plus optional learner text constrained to the toy vocabulary. The candidate currently uses prepared prompts only.

**Required correction before source freeze:** add a constrained text path or explicitly defer it in the architecture. The preferred path is to add it because it makes the source-locked tokenizer limitation directly testable, including `<UNK>` behavior and maximum-context truncation.

### F. Attention-cell keyboard inspection is incomplete

Token selection is keyboard accessible because tokens are buttons. Individual matrix cells are static table cells, so a keyboard user cannot select a query/source pair for synchronized inspection.

**Required correction:** make permitted attention cells keyboard-operable controls or provide an equivalent query/source selector that updates the same text state.

### G. The candidate is intentionally outside the public deployment boundary

This is not a defect at this checkpoint. `tools/build_site.py` must continue to deploy exactly the existing twelve applets until the English source is frozen and ZH/VI/ES parity work is complete. Navigation, `applets.json`, curriculum, sitemap, release metadata, and Pages deployment scope must not be expanded yet.

## 3. Source-freeze decision

**Decision: HOLD.**

The single-file English candidate is a material implementation advance and is suitable for continued machine verification. It is not yet the English semantic freeze because A–F above affect mechanism completeness, challenge correctness, or accessibility.

The next implementation checkpoint should close A–F in one coherent English-only increment, rerun the Python/JavaScript/reference chain plus candidate browser QA, and only then freeze English semantics for Simplified-Chinese parity.

## 4. Release-boundary decision

No public Lab 13 deployment, v1.2 release metadata change, tag, release, DOI mutation, or Paper 7 change is authorized by this checkpoint.
