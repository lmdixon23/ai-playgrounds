# AI Playgrounds v1.2 Lab Roadmap

Status: strategic freeze candidate. New labs remain separate from the v1.1 hardening/localization release chain.

## Decision summary

### Lab 13 — Transformer Language Modeling

Priority: **build next**.

This is the missing foundation for modern generative language systems. It covers token representation, position information, causal self-attention, logits, next-token probabilities, masking, and temperature through a tiny exact decoder model.

Do not create a separate generic "NLP" applet before this one. NLP is too broad to provide one coherent manipulable mechanism. Lab 13 should teach the modern language-model mechanism directly; narrower NLP mechanisms can become later labs when they justify their own prediction/reveal loop.

### Lab 14 — Agent Tool Use and Context Protocols

Priority: **highest-attention follow-up** after Lab 13.

Core mechanism:

`goal -> inspect available tools -> choose tool -> construct arguments -> receive observation -> update context -> choose next action -> stop`

The lab should be vendor-neutral. MCP can be one concrete protocol scenario, not the conceptual definition of an agent.

The educational object is not "watch an AI agent do things." It is the explicit state transition between model output, structured tool call, external observation, and subsequent model context.

Recommended scenarios:

1. choose the correct tool from overlapping schemas;
2. reject an invalid or underspecified argument object;
3. distinguish model text from an executed tool call;
4. demonstrate how a tool observation changes the next action;
5. permission boundary: available tool versus authorized tool;
6. prompt-injection case in retrieved/tool-provided text;
7. MCP-style stateless request/response trace;
8. termination: identify when the task is complete rather than calling another tool.

Guided Challenge should ask the learner to predict **which tool call is justified next and which arguments are valid**, then reveal the deterministic agent trace.

### Lab 15 — Retrieval, Embeddings, and RAG

Priority: **strong curricular follow-up**.

Core mechanism:

`documents -> chunks -> embeddings -> similarity -> top-k retrieval -> context assembly -> answer`

This should not be folded into Lab 14. Retrieval errors and tool-selection errors are conceptually different failure modes.

Required experiments:

- chunk size and overlap;
- top-k;
- embedding similarity;
- irrelevant but lexically similar distractors;
- retrieved evidence versus model answer;
- retrieval failure versus generation failure;
- citation/evidence grounding.

### Lab 16 candidate — Local Inference and Quantization

Priority: **distinctive suite fit**, below agents/RAG in immediate attention.

Core mechanism:

`weights -> numeric precision -> memory footprint -> quantization error -> output change`

This aligns unusually well with AI Playgrounds' offline/local identity and would help explain why increasingly capable open models can run on consumer hardware.

### Lower-priority candidates

- Mixture of Experts / sparse routing;
- multimodal contrastive embeddings;
- diffusion language models;
- speculative decoding and KV caching;
- verifier-guided reasoning / test-time compute.

These are valuable but currently less foundational for this suite than Transformer Language Modeling, Agent Tool Use, and RAG.

## Why Agent Tool Use ranks above another pure model-architecture lab

By 2026, the important learner-facing shift is from a model producing one answer to a model operating inside a loop with tools and an environment. Agentic systems make several previously hidden boundaries teachable:

- generation is not execution;
- a schema constrains valid actions;
- external observations become new context;
- permissions constrain available actions;
- long tasks require multiple state transitions;
- tool outputs can be wrong, adversarial, or irrelevant;
- the stopping decision is part of system behavior.

This gives the suite a new class of mechanism rather than another variation on a neural-network forward pass.

## Why not make Lab 14 simply "MCP"

Protocol specifications change faster than foundational concepts.

Therefore:

- the conceptual applet is **Agent Tool Use and Context Protocols**;
- one scenario may instantiate the current MCP request structure;
- protocol-specific labels must remain scoped to the documented version;
- the applet must remain useful if a later MCP revision changes wire details.

## Why not make Lab 13 a generic NLP applet

A generic NLP applet would tend to mix mechanisms with little causal unity: tokenization, tagging, sentiment, embeddings, attention, generation, and retrieval.

The suite works best when one applet exposes one mechanism family. The cleaner decomposition is:

- Lab 13: autoregressive transformer language modeling;
- Lab 15: embeddings/retrieval/RAG;
- existing Bayes classifier: probabilistic classification;
- possible future applet: sequence labeling/classic NLP only if curriculum demand warrants it.

## Release sequencing

### v1.1

Finish hardening and localization of the existing twelve applets. Do not merge new labs into this release line.

### v1.2

Primary feature: Lab 13 Transformer Language Modeling.

A v1.2 release should not automatically include Lab 14. Lab 13 should reach the same evidence boundary as the existing suite before adding another major applet.

### v1.3 or later v1.2 minor

Lab 14 Agent Tool Use and Context Protocols.

### Following release

Lab 15 Retrieval, Embeddings, and RAG.

## Acceptance rule for any new lab

A topic is not added because it is fashionable. It must pass all five gates:

1. **mechanism clarity** — a learner can predict a state transition before reveal;
2. **suite complementarity** — it adds a mechanism not already taught well elsewhere;
3. **deterministic inspectability** — browser behavior can be independently reproduced;
4. **offline feasibility** — core learning does not require an account/backend/API;
5. **pedagogical durability** — the concept remains useful after current product names and model releases change.

Transformer Language Modeling and Agent Tool Use pass all five. MCP itself passes only when treated as a versioned scenario inside the broader agent-tool mechanism.
