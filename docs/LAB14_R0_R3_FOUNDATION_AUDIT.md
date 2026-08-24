# Lab 14 R0–R3 Foundation Audit

Status: **PASS — deterministic foundation accepted for continued non-public development**.

Accepted foundation head: `f526532c279448e024c4224bf0a1c78ed8b60284`.

Permanent Verify receipt: run `32741464214`, job `97476920727` — **PASS**.

## Accepted layers

### R0 architecture

The conceptual mechanism is frozen as:

`goal -> inspect tools -> propose action -> validate -> authorize -> execute -> observe -> update context -> choose next action -> stop`

The architecture keeps model output, schema validity, authorization, execution, observation provenance, context update, and termination as separate states. Retrieval/RAG remains outside Lab 14. MCP is treated as one version-scoped protocol scenario rather than the definition of an agent.

### R1 deterministic Python reference

The standard-library reference implementation contains:

- frozen in-memory tool schemas and world fixtures;
- deterministic schema validation;
- explicit principal authorization;
- separate text, tool-call, and stop actions;
- deterministic execution and execution-error observations;
- provenance-preserving context updates;
- transparent candidate scoring;
- canonical Oslo weather -> Celsius/Fahrenheit conversion -> stop trace;
- MCP 2026-07-28 envelope serialization;
- 20 regression fixtures.

### R2 independent JavaScript core

The JavaScript state machine independently implements the same mechanism rather than importing Python-generated answers. Recursive Python/JavaScript parity covers eight complete fixture families and includes a deliberate parity-harness self-test.

### R3 non-public browser prototype

The prototype exposes:

- eight mechanism scenarios;
- five prediction-before-reveal Guided Challenges;
- goal/context ledger;
- tool catalog;
- candidate-action scoring board;
- validation/authorization/execution pipeline;
- trace timeline;
- MCP envelope inspector;
- complete text-equivalent state;
- responsive containment.

## Exact verification boundary

The accepted run passed the complete inherited v1.2 verification stack plus all Lab 14 foundation gates:

- Lab 14 Python reference tests;
- Lab 14 Python/JavaScript parity;
- Lab 14 browser-prototype QA;
- the complete inherited release, localization, algorithm, Transformer, deployment, and responsive-browser checks.

No public Lab 14 route, applet manifest entry, sitemap entry, release metadata change, or deployment mutation is part of this acceptance.

## Decision

R0–R3 are accepted as the deterministic foundation for R4 English-source work. Any later change to the abstract state machine, tool semantics, authorization ordering, context-update semantics, or MCP 2026-07-28 serialization must invalidate this acceptance and rerun the corresponding reference/parity/prototype gates.
