# R4 Vietnamese and Spanish localization architecture

## Source baseline

R4 starts from the audited R3 verification head. English is the semantic source language and Simplified Chinese is the independently audited parity language. Vietnamese and Spanish translations must preserve the claim strength, qualifications, mechanism distinctions, and epistemic status frozen by R1-R3.

R4 supports exactly four learner-facing locales:

- English
- 简体中文
- Tiếng Việt
- Español

Research and developer documentation remains English-first.

## Required learner-facing surfaces

Each applet must localize the following surfaces, not merely the initial visible controls:

1. header, controls, labels, buttons, tooltips, errors, statuses, and dynamic hints;
2. TLDR, essay/explanation, teacher guidance, glossary/key terms, and curriculum-facing learner copy;
3. scenario gallery and lesson-tour prompts;
4. accessibility layer copy, field labels, live-region/state descriptions, and non-visual equivalents;
5. Guided Challenge mode labels, prompts, prediction objects, lock/reveal/compare/explain/transfer states, mechanism notes, and reset text;
6. copied/exported learner text or packets when the applet generates them;
7. page metadata, hreflang links, document language, structured-data inLanguage, and URL/local-storage locale state;
8. generated/fallback strings inserted after initial page load.

## Runtime contract

The final language control is a native select with self-named options. Locale switching must preserve applet state wherever the existing English/Chinese switch already preserves it. Switching locale must not alter algorithm parameters, predictions, challenge state, learner inputs, or analytics behavior.

A supported locale may not silently fall back to English on a core learner-facing surface. Technical symbols, algorithm names, variable names, and standard abbreviations may remain untranslated when that is the clearer disciplinary convention.

## Translation quality contract

Vietnamese and Spanish use conceptual equivalence rather than word-for-word substitution. Required safeguards include:

- conditional claims remain conditional;
- dependence is not weakened to correlation;
- validation data is not relabeled as untouched test data;
- affine mappings are not reduced to purely linear mappings;
- finite-run search behavior is not promoted to a global-optimality guarantee;
- k-selection and standardization are not presented as universally correct rules;
- convolution/cross-correlation and Q-learning reward/discount distinctions remain intact;
- probability terms retain the same conditioning assumptions as English.

## Verification

R4 adds two permanent gates:

- a static localization completeness/parity verifier that checks all four locales, metadata, duplicate source surfaces, and known conceptual regressions;
- a Chromium locale-switch suite that enters Vietnamese and Spanish on every applet, exercises the shared Guided Challenge surface, checks dynamic state and accessibility copy, and returns to English without state corruption.

Human review remains a release gate. Automated translation and automated QA can establish completeness and structural consistency, but R4 is not final-release-ready until a fluent Vietnamese reviewer and a fluent Spanish reviewer approve the learner-facing language or return bounded corrections.

## Completion receipt

All twelve applet catalogs are present and exact-source coverage is enforced per applet. Vietnamese and Spanish remain machine-generated drafts pending the already-required fluent human review gate. No runtime network translation is used.
