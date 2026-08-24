# Lab 14 English Source Audit

Status: **R4 candidate — acceptance pending exact-head permanent Verify PASS**.

## 1. Source construction

R4 generates one self-contained English candidate from the accepted R3 browser prototype plus the accepted independent JavaScript core:

- prototype: `tools/agent_tool_context_prototype.html`;
- independent core: `tools/agent_tool_context_core.js`;
- builder: `tools/build_agent_tool_context_english_candidate.py`;
- generated evidence candidate: `release-evidence/lab14-agent-tool-context-english-candidate.html`.

The builder embeds the JavaScript core into the prototype, removes the external script dependency, changes the R3 prototype label to an English-source candidate label, and adds the final English misconception/terminology surfaces needed before localization.

The generated candidate remains non-public. It is not copied into `playgrounds/`, added to the public manifest, or included in the deterministic Pages artifact.

## 2. Frozen English semantic boundaries

The English candidate must keep the following distinctions explicit:

1. natural-language model text is not tool execution;
2. tool availability is distinct from schema validity;
3. schema validity is distinct from authorization;
4. authorization is distinct from actual execution;
5. execution errors are distinct from invalid or denied calls;
6. observations enter context with provenance;
7. instruction-like tool content remains observation data and does not automatically become a controlling instruction;
8. the deterministic teaching policy is not represented as a frontier model's hidden reasoning;
9. MCP is one versioned protocol scenario, not the definition of an agent;
10. correct termination is part of the action policy.

The candidate explicitly rejects ten corresponding misconceptions, including claims that a catalog entry implies permission, schema validity implies correctness, model text itself creates side effects, or one toy provenance rule solves prompt injection generally.

## 3. One-file and offline boundary

The generated English candidate must contain:

- no external `<script src>` dependency;
- no runtime `fetch`;
- no `XMLHttpRequest`;
- no WebSocket or EventSource connection;
- no account/backend requirement;
- no real mail, calendar, filesystem, or network side effect.

All tool behavior remains the frozen in-memory deterministic world inherited from R1–R3.

## 4. Browser acceptance matrix

`tools/test_agent_tool_context_english_applet.py` must verify at minimum:

- exact eight-scenario inventory;
- exact five-Challenge inventory;
- complete text-equivalent state;
- canonical `weather.current -> 8 C -> unit.convert_temperature -> 46.4 F -> stop` trace;
- observation-driven next-action change;
- invalid-call rejection without context mutation;
- text output producing no tool execution or fabricated observation;
- schema-valid unauthorized call denial without side effects;
- untrusted note content retaining provenance without changing the goal or principal;
- post-observation selection of `stop` rather than injected `mail.send`;
- MCP 2026-07-28 version/method/tool envelope visibility without prior handshake/session fields;
- satisfied-goal termination rather than redundant execution;
- Guided Challenge commit/reveal/reset state contract;
- desktop and mobile root containment;
- zero page or console errors.

## 5. R4 acceptance rule

R4 is accepted only when one exact branch head contains:

- the accepted R0–R3 deterministic foundation;
- the English candidate builder;
- the English browser/semantic audit;
- the permanent English-candidate Verify workflow gate;
- this audit record;
- one complete permanent Verify PASS at that exact head.

After that pass, this document must be updated with the exact accepted head, workflow run, job, check counts, and evidence artifact before R5 ZH/VI/ES catalog work begins.

## 6. Public-release boundary

R4 does not alter AI Playgrounds v1.2.0. Public Lab 14 integration remains prohibited until English freeze, ZH/VI/ES semantic parity, four-locale browser parity, and the fourteen-applet public integration gate have each been independently accepted.
