# Lab 14 — Agent Tool Use and Context Protocols

Status: architecture freeze candidate for AI Playgrounds v1.3.0.

## 1. Decision

Lab 14 is **Agent Tool Use and Context Protocols**, not a vendor-specific agent demo and not an MCP tutorial.

The applet exposes one causal loop:

`goal -> inspect tools -> propose action -> validate call -> check authorization -> execute tool -> receive observation -> update context -> choose next action -> stop`

The educational object is the boundary between generated model output, structured action, runtime validation, external execution, returned observation, context update, and termination.

The applet must remain deterministic and offline. It must not call a frontier model, remote API, real calendar, mailbox, filesystem, or network service.

## 2. Why this lab belongs in the suite

Lab 13 explains how a language model can map context to next-token probabilities. Lab 14 begins one layer above the model and asks what changes when a system lets model output participate in an action loop.

This adds a mechanism not represented elsewhere in AI Playgrounds:

- generation is distinct from execution;
- tools expose structured capabilities rather than arbitrary actions;
- schemas define which argument objects are valid;
- authorization can be narrower than tool availability;
- tool observations become new model context;
- external content is data and may contain irrelevant or adversarial instructions;
- multi-step tasks require state transitions across calls;
- a correct stopping decision is part of agent behavior.

The lab should make every transition inspectable before it becomes animated.

## 3. Core learner questions

A learner should be able to answer all of the following after using the applet:

1. What is the difference between model text and an executable tool call?
2. Why does a tool call need a structured name and argument object?
3. What does schema validation establish, and what does it not establish?
4. Why can a tool be available but not authorized for a particular task or principal?
5. What changes in agent context after a tool returns an observation?
6. Why can the next justified action change after an observation?
7. Why should tool-provided text not automatically become a higher-priority instruction?
8. What is the difference between an invalid call, a denied call, and a tool execution error?
9. When should an agent stop instead of making another tool call?
10. Which parts of the agent-tool loop are conceptual and which are protocol-specific?

## 4. Frozen abstract state machine

Every scenario uses the same deterministic state machine.

### State

The canonical state contains:

- `goal`: the task to complete;
- `context`: ordered facts and observations currently known;
- `tool_catalog`: tool specifications visible to the agent;
- `principal`: the acting role used by the authorization gate;
- `history`: proposed calls, validation decisions, authorization decisions, executions, and observations;
- `step`: current transition number;
- `max_steps`: hard execution budget;
- `status`: `active`, `complete`, or `blocked`.

### Action types

The model-side planner may produce exactly one of:

1. `tool_call` — a structured tool name plus arguments;
2. `text` — non-executable natural-language output;
3. `stop` — a termination proposal.

Only `tool_call` enters the execution pipeline.

### Runtime transition

For a proposed `tool_call`, the host performs, in order:

1. tool existence check;
2. argument-schema validation;
3. authorization check;
4. deterministic tool execution;
5. observation creation;
6. context update.

A failure at steps 1–3 prevents execution. A tool execution error produces an observation but does not fabricate a successful result.

## 5. Tool schema model

Use a bounded JSON-Schema-like subset sufficient for teaching:

- object arguments only;
- explicit named properties;
- primitive types: string, number, integer, boolean;
- required-property set;
- optional finite enum values;
- `additionalProperties = false`.

The applet should show the schema beside the proposed argument object and highlight the exact validation rule that passes or fails.

Do not imply that schema validity means the action is useful, authorized, factually correct, or guaranteed to succeed.

## 6. Authorization model

Authorization is a separate gate after schema validation.

Each tool specification contains an explicit set of roles permitted to execute it. The canonical roles are:

- `learner`;
- `assistant`;
- `operator`.

A scenario may expose a tool in the catalog while denying its execution to the current principal. The interface must distinguish:

- **available**: the agent can inspect the tool and schema;
- **valid**: the proposed argument object satisfies the schema;
- **authorized**: the current principal may execute the tool;
- **executed**: the runtime actually invoked the deterministic tool implementation.

These states must not be collapsed into one green/red label.

## 7. Frozen deterministic tool world

The first reference implementation uses an in-memory world with no external I/O.

Recommended tools:

### `weather.current`

Arguments:

- `city`: required string.

Returns a frozen current-temperature record for a small city table.

### `weather.forecast`

Arguments:

- `city`: required string;
- `day`: required enum such as `today`, `tomorrow`.

This overlaps semantically with `weather.current` but has a different schema, making tool selection inspectable.

### `unit.convert_temperature`

Arguments:

- `value`: required number;
- `from_unit`: required enum `C`, `F`;
- `to_unit`: required enum `C`, `F`.

Returns the deterministic converted value.

### `calendar.create`

Arguments:

- `title`: required string;
- `day`: required string;
- `hour`: required integer.

Used primarily for validation and authorization scenarios. It writes only to an in-memory event list.

### `mail.send`

Arguments:

- `recipient`: required string;
- `body`: required string.

Visible in the catalog but restricted to the `operator` role in the canonical permission scenario.

### `notes.search`

Arguments:

- `query`: required string.

Returns frozen note snippets. One fixture contains adversarial instruction-like text so the learner can distinguish observation data from control instructions.

## 8. Deterministic planner boundary

The lab must not simulate a full language model internally and then imply that its policy is representative of arbitrary frontier agents.

Instead, each scenario supplies a small set of candidate model outputs. The deterministic planner ranks those candidates using explicit, visible rules:

1. action type fits the current task state;
2. referenced tool exists;
3. required information for the call is present in context;
4. call is schema-valid;
5. call is authorized;
6. action advances an unsatisfied goal condition;
7. redundant calls are penalized;
8. `stop` is preferred when every goal condition is satisfied.

The selected candidate is therefore a transparent teaching policy, not a claim about how a particular production model reasons.

## 9. Canonical multi-step trace

Default goal:

`Find the current temperature in Oslo, convert it to Fahrenheit, then stop.`

Initial context contains the city but no temperature.

### Step 1

The justified call is:

`weather.current({city: Oslo})`

Frozen observation:

`temperature_c = 8`

The context update makes `8 C` available to the next decision.

### Step 2

The justified call becomes:

`unit.convert_temperature({value: 8, from_unit: C, to_unit: F})`

Frozen observation:

`temperature_f = 46.4`

### Step 3

The goal conditions are satisfied, so the justified action is `stop`.

The applet should make it visually obvious that Step 2 was not justified before Step 1 returned the numeric observation.

## 10. Required scenarios

At minimum:

1. **Overlapping tool schemas** — choose `weather.current` rather than `weather.forecast` or an unrelated search tool for a current-temperature goal.
2. **Invalid arguments** — reject an underspecified `calendar.create` object, expose the missing fields, and allow a repaired call.
3. **Text is not execution** — model text saying that it will call a tool produces no tool side effect.
4. **Observation changes the next action** — canonical weather-to-conversion sequence.
5. **Permission boundary** — `mail.send` is available and schema-valid but denied to the current principal; an authorized non-executing alternative remains possible.
6. **Instruction-like tool output** — `notes.search` returns untrusted text that requests an unrelated privileged action; the deterministic policy treats it as observation data rather than a goal/system instruction.
7. **MCP 2026-07-28 stateless trace** — map one abstract `tool_call` to a version-scoped request/response envelope without redefining the conceptual agent loop as MCP.
8. **Termination** — compare a correct `stop` with a redundant extra tool call after the goal has been satisfied.

## 11. Guided Challenge contract

Use the suite sequence:

`Prompt -> Commit prediction -> Reveal mechanism -> Compare -> Explain -> Transfer`

### Challenge 1 — Which call is justified next?

Learner sees the goal, context, and three candidate tool calls.

Prediction:

- select the justified call;
- identify which context facts make its arguments available.

Reveal:

- candidate ranking;
- schema result;
- authorization result;
- selected transition.

### Challenge 2 — Will this call execute?

Learner sees a structurally invalid or unauthorized call.

Prediction:

- `execute`, `reject-invalid`, or `deny-unauthorized`;
- identify the relevant schema or permission rule.

Reveal must show that validation and authorization are different gates.

### Challenge 3 — What changes after the observation?

Learner predicts which candidate becomes justified after a tool observation is appended to context.

Reveal should compare pre-observation and post-observation candidate eligibility.

### Challenge 4 — Data or instruction?

Learner sees retrieved/tool-provided text containing an unrelated instruction.

Prediction:

- treat as observation data;
- or treat as controlling instruction.

Reveal should show the provenance label and unchanged goal/authorization state.

### Challenge 5 — Stop or call again?

Learner sees a completed goal and one plausible but redundant extra call.

Prediction:

- `stop`;
- or execute the redundant call.

Reveal should expose the satisfied-goal test and step-budget implications.

## 12. MCP scenario boundary

MCP is one protocol instantiation inside Lab 14, not the definition of agent tool use.

The versioned scenario is explicitly scoped to **MCP specification 2026-07-28**.

For this scenario, the applet may show a self-contained stateless tool request with:

- `MCP-Protocol-Version: 2026-07-28`;
- `Mcp-Method: tools/call`;
- `Mcp-Name: <tool name>`;
- a JSON-RPC request body containing the tool name, arguments, and request metadata.

The scenario should also state that this protocol version removed the earlier required `initialize`/`initialized` handshake and session identifier from the core stateless request path. This statement is version-specific and must not be generalized to earlier MCP releases.

Protocol transport details remain secondary to the conceptual invariant:

`structured call -> external execution -> structured observation -> new context`.

If a future MCP version changes its wire details, only this scenario should need revision.

## 13. Instruction-like observation / prompt-injection model

The applet should model adversarial tool content without pretending that one simple filter solves prompt injection generally.

Each observation has provenance metadata:

- `source_tool`;
- `trust = trusted_fixture | untrusted_content`;
- `data`.

The canonical `notes.search` fixture contains text equivalent to an instruction to ignore the task and use `mail.send`.

The deterministic host policy does **not** add that text to the goal, does not change authorization, and does not execute it directly. It remains visible as untrusted observation data.

The learning claim is bounded: provenance-aware separation can prevent this toy host from treating tool content as a controlling instruction. The applet must not claim that this technique solves prompt injection in general production systems.

## 14. Primary visualizations

Use five synchronized views:

1. **Goal and context ledger** — ordered facts with provenance labels.
2. **Tool catalog** — schemas plus availability and role authorization.
3. **Candidate action board** — model-side candidate outputs with deterministic ranking reasons.
4. **Runtime pipeline** — validate -> authorize -> execute -> observe.
5. **Trace timeline** — every state transition, including rejected and denied calls.

For the MCP scenario, add a sixth protocol-envelope inspector without replacing the abstract runtime pipeline.

## 15. Accessible text-equivalent state

The complete current state must be serializable as text and include:

- goal;
- step and status;
- context facts with provenance;
- current principal;
- visible tool names and schemas;
- proposed candidate outputs;
- validation result;
- authorization result;
- executed call, if any;
- latest observation;
- satisfied and unsatisfied goal conditions;
- termination eligibility.

No critical state may exist only in color, animation, or diagram position.

## 16. Misconceptions to test explicitly

The applet must reject or qualify all of these statements:

- `If the model says it called a tool, the tool ran.`
- `If a tool appears in the catalog, the agent is authorized to use it.`
- `Schema-valid means the action is correct.`
- `A tool output is automatically an instruction to the agent.`
- `Every agent task needs multiple tool calls.`
- `The model itself executes external side effects.`
- `MCP is what makes a system an agent.`
- `An agent should keep calling tools while useful tools remain available.`
- `A failed tool call and a denied tool call are the same state.`
- `One prompt-injection defense makes arbitrary tool content safe.`

## 17. Non-goals

Lab 14 does not attempt to teach:

- autonomous web browsing;
- production credential management;
- real OAuth flows;
- distributed agent orchestration;
- generic computer-use agents;
- long-running task queues;
- production MCP server deployment;
- chain-of-thought or hidden model reasoning;
- reinforcement learning for tool policies;
- RAG, embeddings, or retrieval ranking as a primary mechanism.

Retrieval and RAG remain Lab 15.

## 18. Reference implementation contract

Before a browser prototype is accepted, create a standard-library Python reference implementation with deterministic fixtures for:

1. valid schema acceptance;
2. missing required argument rejection;
3. unexpected argument rejection;
4. type mismatch rejection;
5. enum mismatch rejection;
6. unavailable tool rejection;
7. unauthorized tool denial;
8. text output producing no execution;
9. deterministic weather observation;
10. deterministic temperature conversion;
11. observation-to-context update;
12. candidate action change after observation;
13. redundant-call suppression after goal completion;
14. step-budget blocking;
15. execution-error observation;
16. provenance preservation for untrusted content;
17. untrusted content not changing goal or authorization;
18. deterministic MCP 2026-07-28 envelope generation;
19. deterministic canonical three-step trace;
20. exact replay reproducibility.

The browser implementation must later receive an independent JavaScript implementation and recursive Python/JavaScript parity checks rather than importing Python-generated answers.

## 19. Release boundary

Lab 14 targets **v1.3.0**.

R0/R1 development remains non-public and must not alter the current v1.2.0 release, `main`, public applet count, sitemap, deployment artifact, or immutable v1.2.0 tag/release.

Recommended progression:

1. R0 architecture freeze;
2. R1 deterministic Python reference plus tests;
3. R2 independent JavaScript core and cross-runtime parity;
4. R3 non-public browser prototype;
5. R4 English source freeze;
6. R5 ZH/VI/ES semantic parity;
7. R6 four-locale browser parity;
8. R7 public fourteen-applet integration;
9. exact-head verification, one squash merge, merged-main/Pages verification, then v1.3.0 release.

No public integration should occur before the deterministic reference model and its adversarial fixtures are frozen.
