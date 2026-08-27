# AI Playgrounds v1.7.2

Release date: 2026-08-27

## Summary

v1.7.2 is a product-consistency and release-assurance patch. It brings Labs 13-15 to the mature suite boundary for navigation, learner orientation, Quick Assign packet actions, accessibility-oriented text support, provenance, and discovery metadata without changing an AI mechanism, curriculum placement, learner language, or assignment architecture.

## Changed

- Transformer Language Modeling, Agent Tool Use and Context Protocols, and Game Trees: Minimax / Alpha-Beta now use the shared Share / More / Reset hierarchy, skip-to-mechanism link, compact Big idea / What to watch orientation, key terms, text-and-keyboard support, model-fidelity disclosure, and established suite footer.
- Share copies or invokes sharing for the current lab URL. Embed produces a local iframe snippet using `?embed=1`; embed mode removes suite chrome while retaining the learning mechanism.
- The More menu includes a local current-settings JSON export that excludes Quick Assign response fields.
- The three modern Quick Assigns now capture and refresh their existing text-equivalent mechanism state, copy state plus responses as one packet, and print only that packet.
- Quick Assign action labels and accessible field names follow English, Simplified Chinese, Vietnamese, and Spanish while learner-authored responses remain unchanged across locale switches.
- The modern labs now expose complete canonical, favicon, OpenGraph, Twitter, `hreflang`, and JSON-LD metadata generated from the final catalogue.
- The applet design-system contract now records which outer-shell affordances are shared and which concept-specific bodies must remain different.

## Fixed

- Accessibility CSS is inserted at the structural document-head boundary rather than by searching backward for a text fragment that can occur inside JavaScript.
- Final release QA counts real Quick Assign elements instead of JavaScript selector strings.
- The v1.7.1 base build runs in a clean isolated workspace, making repeated v1.7.2 builds byte-for-byte deterministic even when ignored historical release evidence exists locally.
- The one-time `ai-playgrounds-theme` migration from v1.7.1 remains intact; modern labs continue to read and write the canonical `theme` preference.
- Deployment now follows a successful exact-main-sha Verify workflow instead of racing the complete release and browser checks.
- Aggregate `CHANGELOG.md` and `RELEASE_NOTES.md` indexes are reconciled with the dedicated versioned release files without rewriting historical entries.

## Preserved boundaries

v1.7.2 preserves exactly:

- 15 public applets / 58 deterministic public files;
- 13 Foundations/course-track labs + 2 Modern AI extensions;
- all 15 Level-1 Quick Assign IDs and the one-assignment-surface-per-lab architecture;
- the NN-1 and CNN-1 Level-2 Activity Pack canaries;
- EN/ZH/VI/ES learner-app and Quick Assign support;
- all algorithm, Guided Challenge, curriculum, local-response, privacy, and analytics semantics from v1.7.1.

## Verification

The v1.7.2 final-artifact gates:

- perform two complete builds and compare every deployed file hash;
- syntax-compile every executable inline script and parse every inline JSON block in the final 58-file artifact;
- verify the accessibility stylesheet is structurally inside `document.head`;
- exercise responsive shell containment and embed mode;
- change real mechanism controls before testing Quick Assign Refresh;
- inspect copied and printed packet content;
- inspect Share and Embed clipboard payloads;
- parse the downloaded settings JSON and prove learner responses are excluded;
- preserve responses and accessible labels across EN/ZH/VI/ES;
- verify reduced-motion computed behavior and one-time legacy-theme migration;
- reject page and console errors.

## Evidence boundary

These checks establish bounded implementation, interaction, metadata, and release integrity. They do not establish learning gains, classroom adoption, universal learner preference, fluent-language naturalness, accessibility conformance, or educational impact.

The archived v1.0.1 DOI remains historical provenance and is not reassigned to v1.7.2.
