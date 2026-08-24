# Lab 14 Four-Locale Browser and State-Preservation Audit

Status: **R6 candidate — acceptance pending exact-head permanent Verify PASS**.

Frozen R4 English source head: `9f2f5286f4de3e12a881b61d491c87efe6950166`.

Frozen R5 localization head: `37bdc6a4a84b672ad564d81564e8a055c2b2c9a6`.

## 1. R6 construction

R6 builds one non-public, self-contained EN/ZH/VI/ES candidate from the accepted R4 English source and the complete accepted R5 semantic catalogs.

The builder is:

`tools/build_agent_tool_context_multilingual_candidate.py`

The browser/state-preservation gate is:

`tools/test_agent_tool_context_multilingual_applet.py`

The generated verification candidate is:

`release-evidence/lab14-agent-tool-context-multilingual-candidate.html`

No R6 file is copied into `playgrounds/`, the public manifest, the landing page, the sitemap, or the deterministic Pages artifact.

## 2. Localization architecture

The builder merges the 121-key primary R5 catalog and the 42-key dynamic R5 supplement into 163 presentation keys per locale. It embeds those catalogs and a presentation-only localization runtime into the accepted one-file English candidate.

The runtime translates static labels, scenario text, dynamic runtime templates, challenge prompts and reveals, candidate-scoring reasons, misconception corrections, terminology, JSON observations, and the text-equivalent state. Executable identifiers, state keys, tool names, argument keys, numeric values, and the underlying deterministic JavaScript objects remain unchanged.

Locale changes therefore operate on the DOM presentation layer rather than the frozen state machine.

## 3. State-preservation contract

For every locale switch, R6 must preserve exactly:

- the selected scenario;
- the complete `Lab14Prototype` state;
- the complete selected decision and candidate scores;
- the step counter and history;
- goal conditions;
- context facts and provenance;
- world side-effect state;
- challenge selection and committed prediction;
- challenge lock/reveal control state.

The accessible text-equivalent state may localize string values for the learner, but machine-state keys and the underlying object returned by `Lab14Prototype.getState()` must remain unchanged.

## 4. Dynamic localization contract

R6 must also preserve localization after the frozen English implementation rerenders content. This includes:

- scenario goals;
- model-side text candidates;
- candidate-scoring reasons;
- context values;
- validation and authorization messages;
- tool observations and provenance;
- trace entries;
- Guided Challenge prompts, options, and post-reveal explanations;
- the adversarial meeting-note observation.

The adversarial note must remain visibly instruction-like in each target language while preserving `mail.send` as the protected tool identifier. Localization must not sanitize the attack into benign prose.

## 5. Browser acceptance matrix

`tools/test_agent_tool_context_multilingual_applet.py` verifies at minimum:

1. a single-file, offline, non-public four-locale candidate;
2. exact R4 and R5 freeze bindings;
3. four locale controls and correct document-language tags;
4. 163 merged localization keys per locale;
5. major static semantic-surface localization in EN/ZH/VI/ES;
6. dynamic goal localization;
7. exact machine-state preservation across every locale switch;
8. localized accessible-state values with protected state/tool identifiers preserved;
9. protected tool/protocol identifiers visible in every locale;
10. post-switch adversarial observation localization without mutating the frozen observation object;
11. post-switch Guided Challenge reveal localization;
12. `lang` query-parameter initialization needed for the later public shell;
13. mobile root containment in all four locales;
14. zero page and console errors.

## 6. R6 acceptance rule

R6 is accepted only after one exact branch head containing the multilingual builder, browser/state-preservation gate, permanent Verify workflow gate, and this audit record receives one complete permanent Verify PASS.

After that pass, update this document with the accepted head, run, job, check count, and evidence artifact. Then run one final exact-head receipt verification. That receipt-bearing head is the only R6 freeze that R7 public integration may consume.

## 7. Public-release boundary

R6 does not alter AI Playgrounds v1.2.0. Public Lab 14 integration remains prohibited until R6 is frozen and R7 independently validates the fourteen-applet v1.3.0 public artifact.
