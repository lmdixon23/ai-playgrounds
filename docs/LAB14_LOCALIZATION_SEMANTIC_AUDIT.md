# Lab 14 ZH/VI/ES Semantic Localization Audit

Status: **PASS — R5 semantic catalog accepted; receipt-bearing exact-head verification pending**.

Frozen English source head: `9f2f5286f4de3e12a881b61d491c87efe6950166`.

Accepted R5 candidate head: `246d21b7f2b13756cc9785843bc731fc3d811519`.

Permanent Verify receipt: run `32749753653`, job `97503973643` — **PASS**.

Semantic catalog gate: **1309 checks PASS**, covering **121 side-by-side EN/ZH/VI/ES keys** with zero failures.

Language coverage in the accepted catalog: 1418 CJK characters, 1251 Vietnamese diacritic characters, and 137 Spanish diacritic/inverted-punctuation characters.

Evidence artifact: `ai-playgrounds-verification-32749753653`, artifact ID `9528657731`, SHA-256 `84a21ebc3f5ed1818959792308e67d76a47e6f1f5617f01f592c61e3f0468c85`.

## 1. Catalog architecture

R5 adds one side-by-side semantic catalog:

`tools/agent_tool_context_locales.json`

Every catalog key contains English, Simplified Chinese, Vietnamese, and Spanish values together so the source meaning can be audited directly against each translation. The catalog is explicitly bound to the frozen R4 English source head above.

The accepted catalog covers the learner-facing semantic surfaces needed for R6 browser localization, including:

- page identity, evidence boundary, controls, scenario names, and runtime pipeline;
- context, candidate, tool, MCP, trace, Guided Challenge, and accessible-state labels;
- dynamic authorization, provenance, status, trace, and observation templates;
- all five Guided Challenge prompts, prediction options, and mechanism reveals;
- transparent candidate-scoring reasons;
- ten misconception statements and their corrections;
- core terminology for model output, tool call, schema validity, authorization, execution, observation, context update, and termination.

## 2. Protected computational identifiers

Localization is presentation-only. R5 preserves executable and state-bearing identifiers, including:

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

The accepted catalog preserves all R4 distinctions in every locale:

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

`tools/test_agent_tool_context_localization.py` completed **1309/1309 semantic and structural checks** over 121 catalog keys. The gate verifies:

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

The same permanent Verify run also passed the inherited v1.2 stack, every Lab 13 gate, all accepted Lab 14 R0–R4 gates, and the complete 63-case responsive browser matrix.

## 5. R5 freeze decision

The semantic catalog at `246d21b7f2b13756cc9785843bc731fc3d811519` is accepted.

This receipt update is documentation-only. The exact receipt-bearing branch head produced by this commit must receive one fresh complete permanent Verify PASS before it becomes the frozen R5 localization catalog head used by R6. No catalog value, English-source binding, placeholder, protected identifier, or high-risk semantic rule may change between the accepted candidate and that final receipt-head verification.

Once the receipt-bearing head passes unchanged, R5 is frozen and R6 four-locale browser/state-preservation work may begin against that exact head.

## 6. Public-release boundary

R5 does not create a public Lab 14 page and does not modify AI Playgrounds v1.2.0. Browser localization and state-preservation are R6 obligations; fourteen-applet public integration remains R7.
