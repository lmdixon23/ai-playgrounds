# AI Playgrounds v1.8.1

**Release date:** 2026-08-27
**Public boundary:** 15 applets, 58 deployed files, 15 active Level-1 Quick Assigns, EN/ZH/VI/ES learner support

v1.8.1 corrects the learner-facing parity boundary for Transformer Language Modeling, Agent Tool Use and Context Protocols, and Minimax/Alpha-Beta. The earlier v1.7.2 work aligned their shell and release mechanics, but it did not give them the instructional depth, plain-language entry points, or dark-theme finish of the first twelve applets.

## Learner-facing parity

Each modern lab now includes, in all four learner locales:

- one featured experiment;
- five scenarios with a core question, run-and-watch direction, prediction, and explanation prompt;
- one-click application through the lab's real native controls;
- a terminology primer;
- a step-by-step mechanism explanation and evidence boundary;
- teacher curriculum, pre-exploration prompts, post-exploration prompts, and misconceptions.

The Transformer, agent runtime, and game-tree mechanisms remain unchanged. The new scenario layer drives their existing selectors and does not create a second simulation state.

## Consistency and legibility

- Replaced the three dense catalogue descriptions with concise change-and-watch language in EN/ZH/VI/ES.
- Adopted the established `header-theme`, `lang-switch`, `header-png`, and `header-reset` control families and exposed Share, Embed, JSON, and Reset in one visible action row.
- Added explicit dark-theme accent and button contrast plus surfaces for Transformer boundary/warning/masked cells, agent semantic states, and Minimax inputs, metrics, trace cards, comparison cards, tree canvas, SVG nodes, and pruning states.
- Removed the always-open duplicate accessibility state mirror. Accessibility guidance now links to each lab's native text state.
- Kept the Quick Assign state placeholder compact until the learner opens the packet and explicitly selects Refresh state.

## Release hardening

- Made the historical v1.8.0 builder self-contained so advancing repository citation metadata no longer breaks a clean v1.8.0 rebuild.
- Builds the exact v1.8.1 artifact twice and compares all 58 file hashes.
- Parses final JSON blocks and compiles every executable inline script after all wrappers are composed.
- Adds browser gates for all fifteen modern scenario actions, four-locale response preservation, desktop/mobile containment, shared header geometry, dark-theme contrast, canonical state behavior, and embed mode.
- Retains the v1.8.0 mechanism gates for seeded restart benchmarking, KNN regression, and bounded CDCL tracing.

## Evidence boundary

The deterministic and browser checks establish the tested software behavior, composition, and representative contrast ratios. They do not establish measured learning gains, classroom adoption, translation naturalness for every learner group, or accessibility conformance.

The immutable v1.0.1 DOI remains historical provenance and is not reassigned to v1.8.1.
