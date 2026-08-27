# Public Surface Locale Matrix

Date: 2026-08-27
Status: **current v1.8.0 claim-scoping control**.

## Why this exists

A green localization test for learner applets does not imply that every public support page or Level-2 teaching resource is translated into the same languages. This matrix prevents suite-level prose, metadata, papers, and release notes from silently expanding a local claim into a site-wide claim.

The canonical safe statement at the current boundary is:

> **AI Playgrounds v1.8.0 contains 15 learner applets and 15 Level-1 Quick Assigns with English, Simplified Chinese, Vietnamese, and Spanish support. Some educator/support surfaces and the Level-2 Activity Pack pilot have narrower language boundaries.**

Do not shorten that to the whole AI Playgrounds website is available in four languages unless every public support and educator surface is separately brought to that boundary and verified.

## Current matrix

| Surface | EN | ZH | VI | ES | Claim boundary |
|---|:---:|:---:|:---:|:---:|---|
| 12 original learner applets | yes | yes | yes | yes | R4 learner-interface overlay; state-preserving locale tests apply |
| Transformer Language Modeling | yes | yes | yes | yes | dedicated four-locale semantic/browser/state tests |
| Agent Tool Use and Context Protocols | yes | yes | yes | yes | dedicated four-locale semantic/browser/state tests |
| Game Trees: Minimax / Alpha-Beta | yes | yes | yes | yes | dedicated four-locale semantic/browser/state tests |
| **All 15 Level-1 Quick Assigns** | yes | yes | yes | yes | v1.7 all-lab Quick Assign locale/state/privacy gates remain in force |
| Landing page | yes | yes | yes | yes | four-language navigation/catalogue support |
| Teacher Pack | yes | yes | no | no | educator surface currently EN/ZH |
| Curriculum Map | yes | yes | no | no | educator/navigation surface currently EN/ZH |
| Research and citation page | yes | yes | no | no | research/support surface currently EN/ZH |
| Quality/support pages | varies | varies | no unless explicitly stated | no unless explicitly stated | inspect each support page before making a locale claim |
| NN-1 Activity Pack | yes | no | no | no | Level-2 student resource remains English-only |
| CNN-1 Activity Pack | yes | no | no | no | Level-2 student resource remains English-only |
| Activity Pack index | yes | no | no | no | explicitly labels the Level-2 pilot boundary |

## Verification rules

1. Current landing/Teacher Pack/curriculum metadata must describe the release as **15 applets = 13 Foundations/course-track labs + 2 Modern AI extensions**.
2. Current public/generic documentation must not present a stale 12- or 14-applet product count as the current suite.
3. Historical release notes, archived audit records, and version-specific documentation may truthfully retain older counts and language boundaries; current-document scans must not rewrite history.
4. Every learner applet claiming four-language support must expose EN/ZH/VI/ES in its declared localization metadata/catalogue and pass its applicable state-preservation checks.
5. Every Level-1 Quick Assign claiming four-language support must preserve activity prompts, required state, and learner-authored response text through locale changes.
6. A support page with only EN/ZH controls must not be described as itself four-language merely because it links to four-language applets.
7. Level-2 Activity Packs remain English-only until separately translated and verified.
8. Automated semantic/state parity does not establish fluent-reader naturalness; human language review remains a separate evidence layer.

## Historical rollout note

v1.6.1 began with four early-course Quick Assign canaries. v1.7.0 promoted the remaining eleven after the all-lab assignment, localization/state, responsive, and release gates passed. v1.7.1 aligned modern-shell theme persistence. v1.7.2 localized the remaining modern Quick Assign packet actions and accessible field names. v1.8.0 preserves those assignment and locale boundaries while adding three translated, state-preserving mechanism modes inside existing labs.

## Paper / external-communication wording

Preferred:

> AI Playgrounds v1.8.0 contains 15 learner applets and 15 Level-1 Quick Assigns with English, Simplified Chinese, Vietnamese, and Spanish support. The current educator/support surfaces and Level-2 Activity Pack pilot have narrower language boundaries.

Avoid:

> AI Playgrounds is a fully four-language website.

Avoid:

> All teaching materials are available in four languages.

Avoid:

> Four-language support demonstrates equitable access.

Those stronger claims are not established by the current public surface or software evidence.
