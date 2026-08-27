# Show HN readiness

## Current release boundary

This checklist is for the **current v1.7.2 product**, not the original v1.0.x launch snapshot.

Current externally safe summary:

- 15 learner applets;
- 13 Foundations/course-track labs plus 2 Modern AI extensions;
- EN/ZH/VI/ES learner-app support;
- one Level-1 Quick Assign per applet;
- two longer English-only Level-2 Activity Pack canaries;
- no learner account or project backend;
- deterministic algorithm/localization/HCI/browser/release evidence;
- no claim of measured learning effectiveness or accessibility conformance.

## Pre-submit gate

- Use the direct live-site URL, not a campaign redirect.
- Verify the first interactive opens in one click on a signed-out desktop and phone browser.
- Confirm README, current release, source, license, evidence, privacy, Teacher Pack, and Quick Assign links are public.
- Confirm the homepage shows 15 cards with no stale `undefined` fields and that representative search aliases work.
- Confirm the four learner-language options are visible and reversible on the landing page and representative applets.
- Keep the title descriptive and omit unsupported superlatives.
- Be available for the first two hours to answer technical questions if posting live.

## First-comment content

Explain:

- the self-contained/offline-ready applet architecture;
- why a large framework/backend was avoided;
- what the deterministic tests establish;
- which mechanisms are simplified;
- the distinction between the original twelve learning-mode bodies and the concept-specific Transformer/agent/game-tree bodies inside the current shared shell;
- the all-lab Quick Assign layer;
- why public analytics count only coarse aggregate page/engagement/campaign signals and exclude learner answers/state;
- that v1.7.2 is the current immutable release artifact after publication.

## Anticipated critiques

1. **This is fifteen large/self-contained applets.** Correct. Portability and offline inspectability were chosen over a shared runtime dependency. The public site is still generated deterministically, and the shared product contract prevents shell/metadata/localization drift.
2. **Why do Labs 13–15 look internally different?** Transformer matrices, an agent execution pipeline, and a game tree need different mechanism bodies. The suite standardizes navigation, catalogue metadata, localization, assignment/provenance, HCI, and release behavior while allowing concept-specific visualization layouts.
3. **The algorithms/models are simplified.** Correct. Each applet states its pedagogical scope and limitations; the product is not presented as a production solver, model, or runtime.
4. **Tests do not prove learning.** Correct. Software assurance and educational efficacy are explicitly separated.
5. **Why four languages?** The learner-facing applets support English, Simplified Chinese, Vietnamese, and Spanish to reduce language-interface friction across multilingual contexts. This is a design/access affordance, not evidence of equity or learning benefit. Some educator/support surfaces remain narrower in language scope.
6. **Why analytics at all?** Aggregate uptake signals help distinguish public interest from applet engagement while avoiding learner-entered responses, experiment-state payloads, cookies, general referrer URLs, or cross-site profiles. Offline/local copies remain unmeasured.
7. **Why not a full LMS or grader?** The current product deliberately keeps assignment work local and teacher-controlled. Quick Assigns and Activity Packs reduce teacher setup without requiring accounts, a response database, or a grading backend.

## Do not claim

- measured learning gains;
- broad classroom adoption;
- WCAG/accessibility conformance;
- equitable access outcomes;
- that all public support pages are four-language;
- that software verification validates pedagogy;
- that AI Playgrounds is technically superior to every comparator.
