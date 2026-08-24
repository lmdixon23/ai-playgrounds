# Lab 14 ZH/VI/ES Semantic Localization Audit

Status: **R5 candidate — acceptance pending exact-head permanent Verify PASS**.

Frozen English source head: `9f2f5286f4de3e12a881b61d491c87efe6950166`.

## 1. Catalog architecture

R5 adds one side-by-side semantic catalog:

`tools/agent_tool_context_locales.json`

Every catalog key contains English, Simplified Chinese, Vietnamese, and Spanish values together so the source meaning can be audited directly against each translation. The catalog is explicitly bound to the frozen R4 English source head above.

The catalog covers the learner-facing semantic surfaces needed for R6 browser localization, including:

- page identity, evidence boundary, controls, scenario names, and runtime pipeline;
- context, candidate, tool, MCP, trace, Guided Challenge, and accessible-state labels;
- dynamic authorization, provenance, status, trace, and observation templates;
- all five Guided Challenge prompts, prediction options, and mechanism reveals;
- transparent candidate-scoring reasons;
- ten misconception statements and their corrections;
- core terminology for model output, tool call, schema validity, authorization, execution, observation, context update, and termination.

## 2. Protected computational identifiers

Localization is presentation-only. R5 must preserve executable and state-bearing identifiers, including:

- `weather.current`;
- `weather.forecast`;
- `unit.convert_temperature`;
- `calendar.create`;
- `mail.send`;
- `notes.search`;
- `temperature_c`;
- `temperature_f`;
- `MCP 2026-07-28`.

R6 may translate explanatory text surrounding these identifiers, but it must not translate or mutate tool names, argument keys, state keys, schema keys, protocol version values, or frozen tool data.

## 3. High-risk semantic boundaries

The catalog must preserve all R4 distinctions in every locale:

1. availability is not authorization;
2. schema validity is not correctness or permission;
3. model text is not tool execution;
4. invalid, unauthorized, and execution-error states remain distinct;
5. tool observations carry provenance;
6. instruction-like tool content remains observation data rather than automatically becoming a controlling instruction;
7. satisfying all goal conditions can justify stopping rather than making another call;
8. MCP remains a version-scoped protocol scenario rather than the definition of an agent;
9. the toy provenance rule is not represented as a general solution to prompt injection.

The translations deliberately retain technical identifiers where translation would change the computational object being taught.

## 4. Static semantic gate

`tools/test_agent_tool_context_localization.py` verifies:

- exact binding to the frozen R4 source head;
- exact EN/ZH/VI/ES coverage for every catalog key;
- placeholder parity across all dynamic templates;
- protected-token preservation;
- rejection of nontrivial English prose mapped to itself, except explicitly allowed identifiers;
- substantial Simplified-Chinese, Vietnamese, and Spanish language-specific character coverage;
- required high-risk terminology in each locale;
- explicit negation of authorization and schema misconceptions;
- bounded prompt-injection claims in each locale;
- selected English source strings still occurring in the frozen English candidate rebuilt from the R4 builder.

## 5. Acceptance rule

R5 is accepted only after one exact branch head containing the catalog, semantic verifier, permanent workflow gate, and this audit document receives a complete permanent Verify PASS.

After that pass, update this document with the exact accepted head, run, job, catalog key count, semantic check count, and evidence artifact. Then run one final receipt-bearing exact-head Verify pass. That final receipt head becomes the accepted R5 localization catalog head used by R6.

## 6. Public-release boundary

R5 does not create a public Lab 14 page and does not modify AI Playgrounds v1.2.0. Browser localization and state-preservation are R6 obligations; fourteen-applet public integration remains R7.
