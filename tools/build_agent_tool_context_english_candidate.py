#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOTYPE = ROOT / "tools" / "agent_tool_context_prototype.html"
CORE = ROOT / "tools" / "agent_tool_context_core.js"
DEFAULT_OUTPUT = ROOT / "release-evidence" / "lab14-agent-tool-context-english-candidate.html"

MODEL_CHECK = r'''
<section class="card" id="model-check">
  <h2 style="margin-top:0">Check your model of the agent loop</h2>
  <ul>
    <li><strong>If the model says it called a tool, the tool ran.</strong> No. Natural-language text is not an executable structured call.</li>
    <li><strong>If a tool appears in the catalog, the agent is authorized to use it.</strong> No. Availability and authorization are separate runtime states.</li>
    <li><strong>Schema-valid means the action is correct.</strong> No. Validation establishes only that the argument object satisfies the declared structural contract.</li>
    <li><strong>A tool output is automatically an instruction to the agent.</strong> No. Tool-provided content is an observation with provenance and can be untrusted data.</li>
    <li><strong>Every agent task needs multiple tool calls.</strong> No. Some goals require no call, one call, or a correct stop decision.</li>
    <li><strong>The model itself executes external side effects.</strong> Not in this architecture. A host/runtime decides whether a structured call is valid, authorized, and actually executed.</li>
    <li><strong>MCP is what makes a system an agent.</strong> No. MCP is one versioned protocol scenario; the conceptual action loop is protocol-neutral.</li>
    <li><strong>An agent should keep calling tools while useful tools remain available.</strong> No. Once the goal conditions are satisfied, termination can be the justified next action.</li>
    <li><strong>A failed tool call and a denied tool call are the same state.</strong> No. Validation failure, authorization denial, and execution error occur at different gates.</li>
    <li><strong>One prompt-injection defense makes arbitrary tool content safe.</strong> No. This toy host demonstrates bounded provenance separation only; it does not solve prompt injection generally.</li>
  </ul>
</section>
<section class="card" id="key-terms">
  <h2 style="margin-top:0">Key distinctions</h2>
  <p><strong>Model output:</strong> text or structured data proposed by the model-side policy. <strong>Tool call:</strong> an executable action candidate containing a tool name and argument object. <strong>Schema-valid:</strong> the arguments satisfy the tool's declared structural constraints. <strong>Authorized:</strong> the current principal is permitted to invoke the tool. <strong>Executed:</strong> the runtime actually invoked the deterministic tool implementation. <strong>Observation:</strong> structured data returned by execution. <strong>Context update:</strong> appending that observation with provenance so it can affect a later decision. <strong>Termination:</strong> stopping when the goal conditions are satisfied rather than making another call.</p>
</section>
'''


def build(output: Path) -> Path:
    prototype = PROTOTYPE.read_text(encoding="utf-8")
    core = CORE.read_text(encoding="utf-8")

    required = [
        "Lab 14 R3 Candidate — Agent Tool Use and Context Protocols",
        '<script src="agent_tool_context_core.js"></script>',
        "Guided Challenge · predict before reveal",
        "Accessible state",
        "MCP 2026-07-28 stateless trace",
        "window.Lab14Prototype",
    ]
    missing = [marker for marker in required if marker not in prototype]
    if missing:
        raise RuntimeError(f"R3 prototype no longer satisfies the English-source builder contract: {missing}")
    if "window.AgentToolContextCore" not in core:
        raise RuntimeError("Independent Lab 14 JavaScript core marker is missing")

    safe_core = core.replace("</script", "<\\/script")
    html = prototype.replace(
        '<script src="agent_tool_context_core.js"></script>',
        '<script id="lab14-agent-tool-context-core">\n' + safe_core + "\n</script>",
        1,
    )
    html = html.replace(
        "<title>Lab 14 R3 Candidate — Agent Tool Use and Context Protocols</title>",
        "<title>Agent Tool Use and Context Protocols — Lab 14 English Candidate</title>",
        1,
    )
    html = html.replace(
        "R3 non-public prototype: inspect the boundary between model output, a structured tool call, runtime validation, authorization, deterministic execution, returned observation, context update, and stopping.",
        "English source candidate: inspect the boundary between model output, a structured tool call, runtime validation, authorization, deterministic execution, returned observation, context update, and stopping. Every executable transition is produced by the frozen deterministic teaching policy and in-memory tool world.",
        1,
    )
    html = html.replace(
        "<span class=\"badge\">non-public v1.3 candidate</span>",
        "<span class=\"badge\">non-public v1.3 English candidate</span>",
        1,
    )
    html = html.replace("</main>", MODEL_CHECK + "\n</main>", 1)

    forbidden_runtime = [
        "<script src=",
        "fetch(",
        "XMLHttpRequest",
        "WebSocket(",
        "EventSource(",
    ]
    present = [token for token in forbidden_runtime if token in html]
    if present:
        raise RuntimeError(f"English candidate violates the one-file/offline runtime boundary: {present}")

    for required_phrase in [
        "Availability and authorization are separate runtime states.",
        "Tool-provided content is an observation with provenance",
        "Validation failure, authorization denial, and execution error occur at different gates.",
        "it does not solve prompt injection generally.",
        "MCP is one versioned protocol scenario",
    ]:
        if required_phrase not in html:
            raise RuntimeError(f"English source semantic safeguard missing: {required_phrase}")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")
    print(json.dumps({
        "builder": "tools/build_agent_tool_context_english_candidate.py",
        "prototype": str(PROTOTYPE.relative_to(ROOT)),
        "core": str(CORE.relative_to(ROOT)),
        "output": str(output.relative_to(ROOT)) if output.is_relative_to(ROOT) else str(output),
        "bytes": output.stat().st_size,
        "single_file": True,
        "pass": True,
    }, indent=2))
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    build(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
