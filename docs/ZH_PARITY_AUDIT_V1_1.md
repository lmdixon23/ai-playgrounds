# Simplified Chinese parity freeze

## R3 audit boundary

R3 is the final Simplified Chinese conceptual and language-parity pass before Vietnamese and Spanish localization begins. It is stacked on the audited R2 Guided Challenge head and does not merge, tag, release, or modify immutable v1.0.1.

The audit covers all twelve applets and the shared Guided Challenge layer across five surfaces:

1. visible learner UI and explanatory prose;
2. worksheet, tour, scenario-gallery, tooltip, and fallback strings;
3. accessibility/state-summary text;
4. Guided Challenge prompts, prediction objects, states, transfer prompts, and reveal text;
5. language switching and return-to-English behavior in a real browser.

The parity standard is conceptual rather than word-for-word. Chinese must preserve the English claim strength, conditions, epistemic status, and mechanism distinction. In particular, translation must not turn conditional statements into universal rules, dependence into correlation, validation data into test data, affine maps into purely linear maps, or finite-run evidence into proof of global optimality.

## Corrections identified in R3

The audit specifically checks and corrects the following cross-language risks:

- Bayesian Network uses 条件依赖 for conditional dependence rather than the weaker 相关 label.
- KNN keeps feature scaling conditional on whether raw units distort the intended notion of closeness; standardization is not presented as universally mandatory.
- Neural Network keeps the engineered nonlinear-feature comparison in the Chinese XOR scenario, matching the frozen English source.
- The shared Guided Challenge state copy uses applet 状态 rather than a generic tool-state label where it refers to the applet result.
- Existing R1 precision corrections remain binding in Chinese: validation versus test data, affine versus linear composition, conditional independence, k-selection caveats, convolution versus cross-correlation nuance, finite-run local-search limits, and Q-learning discount/reward distinctions.

## Regression controls

`tools/verify_zh_parity.py` performs static Chinese parity checks across all twelve applets, including required precision language and known stale-claim regressions.

`tools/zh_parity_qa.py` switches every applet to Simplified Chinese in Chromium, checks visible Chinese UI and Guided Challenge copy, enters Guided Challenge mode, verifies that English control fallbacks do not leak into the Chinese challenge surface, and switches back to English.

Both checks are part of the normal `Verify` workflow and emit evidence under `release-evidence/`.

Vietnamese and Spanish remain deferred until this R3 Chinese parity freeze is green on an exact-head normal PR verification run.
