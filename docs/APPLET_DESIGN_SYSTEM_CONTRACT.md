# Applet design-system contract

This is the public product contract for a coherent fifteen-lab suite. It describes requirements and justified variations, not a claim that every possible state has been certified. See [Quality](../QUALITY.md) for evidence limitations.

## Shared page parts

| Page part | Shared requirement | Justified variation |
|---|---|---|
| Header/navigation | Recognizable suite navigation, one primary title, consistent theme and language controls | A short mechanism-specific descriptor |
| Action row | Consistent placement and treatment of sharing, embedding, reset, and supported exports | Omit an export with no honest mechanism representation |
| Orientation | Explain what to change, what to watch, and the model boundary | Length follows prerequisite load |
| Main interaction | Put the experiment before long prose; contain controls responsively | Grid, graph, scatterplot, tree, matrix, or ordered trace |
| Learning modes | Consistent Explore and Guided Challenge navigation | Challenge steps follow what can meaningfully be predicted |
| Featured experiment/scenarios | Offer a clear question, prediction, run-and-watch guidance, and comparison | Cases differ according to the mechanism |
| Explanation | Terms, step-by-step mechanism, misconceptions, and model limitations | Mathematical and conceptual depth varies |
| Classroom surface | One stable Quick Assign with local response handling and teacher guidance | Prompts and state evidence are mechanism-specific |
| Text/keyboard support | Accessible control labels, visible focus, and inspectable essential state | Tables or summaries can replace an unsuitable visual encoding |
| Footer | Consistent suite provenance, navigation, and release context | Additional mechanism-specific references |

A lab being added later is not a reason for unrelated page chrome. Equally, consistency does not require turning every mechanism into the same visualization. A matrix-heavy view may need local scrolling; an agent may need a pipeline; a game tree must keep labels legible.

## Layout, typography, and theme

Shared surfaces should retain the suite's spacing rhythm, reading width, typography, borders, radii, and focus treatment. Controls should wrap without clipping; page-level horizontal overflow should not be used to accommodate an avoidable fixed width. Large tables and trees can use intentional local scrolling.

Applet accents and concept-specific visualization colors may differ. Important state must not rely on color alone. Dark theme must preserve meaning and legibility rather than simply invert a diagram. Reduced-motion preferences should remove nonessential motion without removing the mechanism.

## Language and state

Use a consistent native language selector with English, 简体中文, Tiếng Việt, and Español on learner applets. Labels, dynamic state, challenges, explanations, and Quick Assign surfaces follow the [language contract](LOCALIZATION.md). Support pages retain their separately declared [coverage](PUBLIC_SURFACE_LOCALE_MATRIX.md).

Language changes must not reset an experiment or erase learner drafts. Shared interactions should be checked as transitions: initial state → action → expected result → recovery/reset → consistent focus and state.

## Accessibility and responsive behavior

Essential controls should be keyboard-operable, visibly focused, and meaningfully labelled. Provide a text/table/summary alternative for essential numerical or logical state where practical. Small visual marks may need a tolerant selection method or an equivalent control. Check enlarged text and desktop, projector, tablet, narrow-window, phone-portrait, and phone-landscape layouts.

These are engineering requirements under tested conditions, not proof of WCAG conformance or human screen-reader validation.

## Offline and classroom boundaries

Core interactions in [standalone HTML downloads](https://lmdixon23.github.io/ai-playgrounds/downloads.html) do not require authentication, CDN availability, a model API, analytics, or a server round trip. Optional external references may require a connection. Website pages can use neighbouring assets; a standalone download must work by itself.

The inquiry sequence is **predict → run or manipulate → observe → explain → transfer**. Quick Assigns reuse the applet's mechanism rather than inventing a second algorithm. Learner responses stay local unless deliberately exported or submitted through another system; see [Quick Assign architecture](QUICK_ASSIGN_ARCHITECTURE.md) and [privacy](ANALYTICS_AND_PRIVACY.md).

## Evaluating a difference

Record the component, the pedagogical or technical reason for changing it, the alternative affordance, and the accessibility/recovery implications. Compare against all twelve original labs and the other newer labs, not a single presumed master page. Verify the rendered finished artifact at representative states and sizes as well as reviewing HTML/CSS structure.

Conceptual correctness and learner clarity take precedence over cosmetic uniformity. A justified exception should be explicit; an accidental shared-shell mismatch should be reported through [Contributing](../CONTRIBUTING.md).
