# AI Playgrounds Applet Design System — v1.8.1 Learner-Parity Addendum

**Parent contract:** `docs/APPLET_DESIGN_SYSTEM_CONTRACT.md`
**Supersedes:** the scenario-gallery, compact-learning-equivalent, and hidden secondary-action rulings in `docs/APPLET_DESIGN_SYSTEM_V1_7_2_ADDENDUM.md`

## 1. Comparable teaching depth, not identical mechanism layout

Every complex learner applet provides the same instructional entry sequence:

1. one featured experiment with a core question and run-and-watch direction;
2. approximately five scenarios, each with a core question, run direction, prediction, and explanation prompt;
3. a prerequisite primer and mechanism-specific terminology;
4. a step-by-step explanation of the central computation and evidence boundary;
5. teacher curriculum, pre-exploration prompts, post-exploration prompts, and misconceptions.

The scenario button must apply the real native controls. It must not create a second mechanism state or a disconnected demonstration.

## 2. Plain-language discovery copy

Catalogue descriptions tell a learner what to change and what to watch. Use concrete verbs and familiar nouns before specialist implementation vocabulary. English descriptions target 18 words or fewer and featured prompts 14 words or fewer; other locales should be comparably concise rather than literal expansions.

Technical terms remain available in the applet primer and search-keyword metadata.

## 3. One canonical state explanation

Each applet exposes one always-current native text-equivalent state. A collapsed Quick Assign may hold a placeholder until the learner explicitly refreshes the packet. Accessibility guidance links to the native state instead of mirroring the complete state into a second always-open block.

Intentional duplication after a learner opens and refreshes a response packet is allowed because that copy belongs to the exportable assignment evidence.

## 4. Header primitive parity

Modern applets use the same class families and visual tokens as the established applets:

- `header-theme` in the preference row;
- `lang-switch` around the native language selector;
- `header-png` for Share and secondary actions;
- `header-reset` for reset;
- a visible Share → Embed → local export → Reset action row.

Do not hide the ordinary Embed and local-export actions behind a modern-only `More` menu. Concept-specific high-level actions belong after the shared actions and may use a disclosure only when the established applets use one for the same purpose.

## 5. Dark-theme legibility

Theme variables alone are insufficient when an applet contains hard-coded light surfaces. The final artifact must explicitly cover warnings, masked cells, status pills, inputs, comparison cards, game-tree backgrounds, SVG node fills, and semantic states. Browser QA measures representative normal-text contrast at a target of at least 4.5:1 and confirms that algorithm state is unchanged by theme switching.

## 6. Final-composition gate

The v1.8.1 gate builds twice, compares every file hash, parses every HTML/JSON block, and compiles every final inline script. Browser QA then exercises:

- five scenario actions in each modern lab;
- EN/ZH/VI/ES curriculum switching with response preservation;
- desktop and phone containment;
- shared header geometry;
- explicit dark-theme contrast surfaces;
- one canonical text state and learner-triggered Quick Assign capture;
- embed-mode containment.

These are software and presentation checks. They do not establish measured learning gains, accessibility conformance, or translation naturalness for every learner population.
