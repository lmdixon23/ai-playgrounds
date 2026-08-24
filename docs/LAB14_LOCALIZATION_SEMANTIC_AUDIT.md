# Lab 14 ZH/VI/ES Semantic Localization Audit

Status: **R5 REOPENED — expanded semantic coverage pending fresh exact-head verification**.

Frozen English source head: `9f2f5286f4de3e12a881b61d491c87efe6950166`.

The earlier 121-key catalog candidate and its receipt remain valid evidence for those keys, but they are no longer sufficient to freeze R5 because the browser-facing dynamic surface was found to contain additional English strings that also require semantic review before R6.

## 1. Catalog architecture

R5 now uses two side-by-side EN/ZH/VI/ES semantic catalogs, both bound to the same frozen R4 English source:

- `tools/agent_tool_context_locales.json` — 121 primary learner-facing keys;
- `tools/agent_tool_context_locales_dynamic.json` — dynamic goal, model-output, fixture, validation, authorization, runtime-error, trust, and role surfaces required by R6.

Every catalog key contains English, Simplified Chinese, Vietnamese, and Spanish together so the source meaning can be inspected directly against each translation.

The primary catalog covers:

- page identity, evidence boundary, controls, scenario names, and runtime pipeline;
- context, candidate, tool, MCP, trace, Guided Challenge, and accessible-state labels;
- dynamic authorization, provenance, status, trace, and observation templates;
- all five Guided Challenge prompts, prediction options, and mechanism reveals;
- transparent candidate-scoring reasons;
- ten misconception statements and their corrections;
- core terminology for model output, tool call, schema validity, authorization, execution, observation, context update, and termination.

The dynamic supplement closes the remaining browser-semantic gap by covering:

- all eight scenario goals;
- all model-side text outputs shown by the frozen teaching policy;
- trusted and adversarial note fixtures;
- schema-validation error templates;
- authorization outcomes;
- deterministic execution-error text;
- budget/invalid-action/runtime-error labels;
- trust and role display literals.

## 2. Why R5 was reopened

The initial 121-key gate passed completely, including an exact receipt-bearing Verify run. Before beginning R6, a browser-surface audit found that several English strings were still generated directly from frozen state/tool fixtures rather than represented in the primary localization catalog.

Proceeding to browser localization without reviewing those strings would have created an un-audited translation layer. R5 was therefore deliberately reopened before R6, and the missing surfaces were added as a second source-bound catalog rather than silently translated in browser code.

The previous candidate receipts are preserved as provenance:

- primary catalog candidate head `246d21b7f2b13756cc9785843bc731fc3d811519`;
- Verify run `32749753653`, job `97503973643` — PASS;
- primary gate `1309/1309` over 121 keys;
- receipt head `0ef6c3d61c54ee084bf937053301cdee0930389b`;
- Verify run `32750256129`, job `97505271372` — PASS.

Those receipts do not constitute the final R5 freeze after expansion.

## 3. Protected computational identifiers

Localization is presentation-only. Both catalogs preserve executable and state-bearing identifiers, including:

- `weather.current`;
- `weather.forecast`;
- `unit.convert_temperature`;
- `calendar.create`;
- `mail.send`;
- `notes.search`;
- `temperature_c`;
- `temperature_f`;
- `MCP 2026-07-28`;
- role/state identifiers where they are part of the executable representation.

R6 may translate explanatory text surrounding these identifiers, but it must not translate or mutate tool names, argument keys, state keys, schema keys, protocol version values, or frozen tool data.

## 4. High-risk semantic boundaries

Both catalogs must preserve all R4 distinctions in every locale:

1. availability is not authorization;
2. schema validity is not correctness or permission;
3. model text is not tool execution;
4. invalid, unauthorized, and execution-error states remain distinct;
5. tool observations carry provenance;
6. instruction-like tool content remains observation data rather than automatically becoming a controlling instruction;
7. satisfying all goal conditions can justify stopping rather than making another call;
8. MCP remains a version-scoped protocol scenario rather than the definition of an agent;
9. the toy provenance rule is not represented as a general solution to prompt injection.

Critically, the translated adversarial meeting-note fixture must remain visibly instruction-like. Localization must not sanitize away the attack that the scenario is designed to teach.

## 5. Semantic gates

`tools/test_agent_tool_context_localization.py` verifies the 121-key primary catalog, including source binding, exact four-locale coverage, placeholder parity, protected-token preservation, translated-prose coverage, high-risk terminology, misconception negations, bounded prompt-injection claims, and frozen-English source anchoring.

`tools/test_agent_tool_context_dynamic_localization.py` separately verifies the dynamic supplement, including:

- exact binding to the same R4 source freeze;
- exact EN/ZH/VI/ES coverage;
- placeholder parity;
- protected identifier preservation;
- frozen prototype/core source anchoring;
- all eight scenario-goal translations;
- all model-side text-output translations;
- adversarial note preservation as instruction-like content in ZH/VI/ES;
- distinct localized validation, authorization, and execution-error semantics;
- language-specific character coverage;
- source JavaScript syntax sanity.

Both gates are now permanent steps in `.github/workflows/verify.yml`.

## 6. Expanded R5 acceptance rule

The earlier R5 freeze is superseded. Expanded R5 is accepted only after one exact branch head containing:

- both catalogs;
- both semantic verifiers;
- both permanent workflow gates;
- this reopened audit record;

receives a complete permanent Verify PASS.

After that pass, update this document with the expanded accepted head, both catalog key counts, both gate check counts, run/job, and evidence artifact. Then run one final receipt-bearing exact-head Verify pass. That final receipt head becomes the only accepted R5 localization freeze for R6.

## 7. Public-release boundary

R5 does not create a public Lab 14 page and does not modify AI Playgrounds v1.2.0. Browser localization and state-preservation are R6 obligations; fourteen-applet public integration remains R7.
