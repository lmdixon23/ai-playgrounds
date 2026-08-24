# Lab 13 — Transformer Language Modeling

Status: architecture freeze candidate for AI Playgrounds v1.2.0.

## 1. Decision

Lab 13 is **Transformer Language Modeling**, not a generic NLP survey.

The applet should connect four ideas in one inspectable causal pipeline:

`tokens -> embeddings + position -> masked self-attention -> logits / next-token probabilities`

This is the smallest coherent unit that explains why a modern autoregressive language model can use prior context to predict a next token. Classic NLP topics that do not participate directly in this mechanism (stemming, tagging, parsing, bag-of-words, etc.) are explicitly out of scope.

The applet must remain a toy deterministic model. It must not claim to reproduce a frontier LLM, human language understanding, reasoning, or semantics in general.

## 2. Why this lab belongs in the suite

The current suite contains search, logic, probabilistic reasoning, classification, neural networks, convolution, clustering, overfitting, and reinforcement learning, but no modern generative-language mechanism.

The gap is not merely "NLP." The missing conceptual bridge is how discrete text becomes a causal prediction problem and how self-attention changes the representation used for next-token prediction.

Lab 13 should therefore support AI4K12-style representation, learning, and natural-interaction ideas while preserving the suite's existing design rule: expose a mechanism that learners can predict, perturb, and explain before implementing it in code.

## 3. Differentiation from existing transformer explainers

Do **not** reproduce a full GPT-2 browser explainer.

Existing systems already provide high-fidelity end-to-end Transformer visualization with live pretrained models. Lab 13 should instead optimize for a different instructional objective:

- hand-sized deterministic matrices rather than hundreds of millions of learned parameters;
- exact arithmetic that can be inspected and regression-tested;
- prediction-before-reveal Guided Challenge states;
- bilingual/multilingual source parity inherited from the suite;
- one-file offline operation;
- explicit misconception tests;
- direct correspondence between every learner-visible number and the applet's executable calculation.

The applet is closer to a manipulable worked model than to a model-inspection dashboard.

## 4. Core learner questions

A learner should be able to answer all of the following after using the applet:

1. Why does text have to be represented numerically before a model can process it?
2. What information is contributed by token embeddings versus position information?
3. What do query, key, and value vectors do in scaled dot-product attention?
4. Why is the score divided by `sqrt(d_k)` before softmax?
5. What does a causal mask prevent?
6. Why do attention weights sum to one across the permitted source positions?
7. Why can changing one earlier token change the final next-token probabilities?
8. Why is high attention weight **not** automatically an explanation of the model's decision?
9. How does temperature change a probability distribution without changing the underlying logits?
10. Why is the model's output a probability distribution over possible next tokens rather than a stored sentence response?

## 5. Frozen toy model

Use a deliberately small decoder-only transformer-like block.

Recommended default dimensions:

- vocabulary: 10–16 tokens plus special tokens;
- context length: maximum 6 tokens;
- embedding dimension `d_model = 4`;
- one causal self-attention head with `d_k = d_v = 4`;
- one small feed-forward transform or an explicitly documented omission in R0;
- fixed rational or short-decimal weights;
- deterministic logits and probabilities;
- no stochastic sampling unless the learner explicitly activates the sampling experiment.

The canonical default sequence should be short enough that the full causal attention matrix remains readable on a phone.

All canonical fixtures must be reproducible exactly in Python regression tests independent of the browser implementation.

## 6. Visible pipeline

### Stage A — Tokenization

Use a **toy source-locked tokenizer**, not a claim about universal tokenization.

The learner can choose from prepared short prompts and optionally type text constrained to the toy vocabulary. The interface should distinguish:

- surface text;
- token strings;
- token IDs.

A secondary experiment may demonstrate that different tokenizers could segment the same text differently, but Lab 13 should not implement a full BPE trainer.

### Stage B — Token + position representation

For each token show:

- token embedding vector;
- position vector;
- resulting input vector.

Allow a position-ablation toggle. A scenario should swap two tokens and demonstrate that removing position information makes some order distinctions unavailable to this toy model.

### Stage C — Q/K/V projections

For one selected destination token show exact:

`q = x W_Q`

and, for every permitted source token:

`k_j = x_j W_K`

`v_j = x_j W_V`

The learner must be able to inspect the dot products numerically.

### Stage D — Causal masked attention

Show the score matrix and the causal mask separately.

For each permitted pair:

`score(i,j) = q_i · k_j / sqrt(d_k)`

Then:

`alpha(i,:) = softmax(masked_scores(i,:))`

Then:

`attention_output_i = sum_j alpha(i,j) v_j`

The causal mask must be visible as a structural constraint, not described as the model "choosing not to look into the future."

### Stage E — Output logits and next-token probabilities

Map the final position representation to a tiny vocabulary distribution.

Show:

- raw logits;
- softmax probabilities;
- top predicted token;
- effect of temperature on the displayed distribution.

Clarify that temperature is applied to the logits/distribution at generation time in this toy experiment; it does not retrain the model.

## 7. Primary visualizations

The applet should have four synchronized views:

1. **Token strip** — surface token, token ID, position.
2. **Vector inspector** — embedding, position, Q/K/V values for the selected token.
3. **Causal attention matrix** — numeric values plus heat intensity, with masked future cells visibly distinct.
4. **Next-token distribution** — bar chart/table of logits and probabilities.

Clicking a token or attention cell should update all relevant text-equivalent descriptions.

Color must never be the sole carrier of attention magnitude or mask state.

## 8. Guided Challenge contract

Use the suite sequence:

`Prompt -> Commit prediction -> Reveal mechanism -> Compare -> Explain -> Transfer`

### Challenge 1 — Highest permitted attention

Prepared prompt with fixed weights.

Learner predicts:

- which previous token receives the largest attention weight from the final token;
- why, in terms of the Q/K score rather than semantic intention.

Reveal:

- scaled dot products;
- masked score row;
- softmax attention row.

### Challenge 2 — Causal-mask leak

Learner predicts what changes if the mask is incorrectly removed.

Reveal should show a future-token contribution and explicitly identify that this invalidates autoregressive next-token training/inference semantics for that position.

### Challenge 3 — Token substitution

Replace one earlier token while keeping position fixed.

Learner predicts:

- which Q/K/V quantities change;
- whether the final next-token probability for one named candidate increases or decreases.

### Challenge 4 — Temperature transfer

Keep logits fixed and change temperature.

Learner predicts whether the distribution becomes sharper or flatter.

The challenge must not ask learners to predict exact probabilities until the applet has already introduced softmax numerically.

## 9. Required scenarios

At minimum:

1. **Causal next-token prediction** — canonical pipeline.
2. **Attention score perturbation** — change one key/query component.
3. **Order matters** — token swap with position information on/off.
4. **Mask ablation** — demonstrate future information leakage.
5. **Temperature** — same logits, different sampling distribution.
6. **Attention is not explanation** — construct a case where a large attention weight does not correspond monotonically to the largest output-logit contribution.

## 10. Misconceptions to test explicitly

The applet must reject or qualify all of these statements:

- "A token is one word."
- "Attention tells us what the model understands."
- "The largest attention weight is the reason for the final prediction."
- "The transformer searches the internet for the next word."
- "The causal mask makes the model forget future words it already saw."
- "Temperature changes the learned model weights."
- "The most probable next token is always selected."
- "Position encodings are word meanings."
- "The model stores complete answers and retrieves them."

## 11. Accessibility and text-equivalent state

Every numeric visualization needs a text equivalent.

The accessibility state should include at minimum:

- prompt and token sequence;
- selected token/index;
- selected Q vector;
- source K vectors or selected pair;
- masked/unmasked score;
- attention row with numeric weights;
- final logits;
- final next-token probabilities;
- current temperature;
- whether position information and causal masking are enabled.

Keyboard navigation must support selecting tokens and attention cells without requiring pointer precision.

## 12. Localization

The applet enters the suite **after** R4, so all four locales are part of the acceptance boundary from its first merge-ready version:

- English;
- Simplified Chinese;
- Vietnamese;
- Spanish.

English remains the source semantic freeze. Simplified Chinese gets a separate parity audit. Vietnamese and Spanish catalogs must pass the same machine coverage/state tests and remain explicitly subject to human review before release readiness.

Mathematical symbols, token IDs, matrix labels (`Q`, `K`, `V`) and code identifiers should not be translated when doing so would reduce correspondence with the equations.

## 13. Verification requirements

### Independent algorithm tests

Add browser-independent tests for:

- token ID lookup;
- embedding + position addition;
- Q/K/V matrix multiplication;
- scaled dot-product scores;
- causal masking;
- numerically stable softmax;
- attention weighted sum;
- final projection to logits;
- next-token softmax;
- temperature transformation.

Tests should include at least one exact hand-computable fixture and adversarial cases for:

- large logits;
- tied logits;
- fully masked illegal cells;
- one-token context;
- token substitution;
- position ablation.

### Static/pedagogical contracts

Require explicit source text covering:

- causal mask semantics;
- attention-not-explanation limitation;
- tokenizer limitation;
- temperature limitation;
- toy-model evidence boundary.

### Browser QA

Require:

- all public views render at mobile/tablet/desktop;
- token selection updates synchronized views;
- masked cells cannot become active sources in normal mode;
- Guided Challenge result remains concealed before lock;
- EN/ZH/VI/ES switching preserves experiment and challenge state;
- no locale switch mutates model arithmetic;
- share URLs do not include learner response fields;
- offline operation remains functional.

## 14. Evidence boundary

Acceptable claims:

- the applet implements the documented toy calculations;
- deterministic test fixtures reproduce the browser calculations;
- the challenge workflow enforces prediction-before-reveal in the tested cases.

Do not claim:

- that the toy attention patterns explain real frontier LLM reasoning;
- that the applet faithfully reproduces GPT/Claude/Gemini internal weights;
- learning gains without empirical study;
- classroom adoption without observed use;
- accessibility conformance without a complete human assistive-technology audit.

## 15. Implementation order

1. independent Python reference implementation and exact fixtures;
2. English single-file applet driven by the same fixtures;
3. source-language adversarial/pedagogical audit;
4. Guided Challenge integration;
5. algorithm + browser + accessibility contracts;
6. Simplified Chinese parity;
7. Vietnamese/Spanish catalogs and browser parity;
8. human VI/ES review;
9. suite navigation/curriculum/release metadata integration;
10. only then consider merge into the v1.2 release chain.

## 16. Explicit exclusions from Lab 13 R1

Defer these to separate labs or later revisions:

- RAG;
- tool calling / MCP;
- autonomous agents;
- fine-tuning;
- RLHF/RLVR;
- mixture-of-experts routing;
- long-context KV-cache optimization;
- speculative decoding;
- multimodal transformers;
- real API calls to commercial LLMs.

This scope boundary is deliberate. Lab 13 should establish the causal language-model mechanism cleanly before the suite adds systems built on top of language models.
