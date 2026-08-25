# Public Surface Locale Matrix

Date: 2026-08-25
Status: v1.6.1 candidate claim-scoping control.

## Why this exists

A green localization test for learner applets does not imply that every public support page is translated into the same languages. This matrix prevents suite-level prose, metadata, papers, and release notes from silently expanding a local claim into a site-wide claim.

The canonical safe statement at the current boundary is:

> **All 15 learner applets support English, Simplified Chinese, Vietnamese, and Spanish.**

Do not shorten that to “the whole AI Playgrounds website is available in four languages” unless every public support and educator surface is separately brought to that boundary and verified.

## Current / candidate matrix

| Surface | EN | ZH | VI | ES | Claim boundary |
|---|:---:|:---:|:---:|:---:|---|
| 12 original learner applets | yes | yes | yes | yes | R4 learner-interface overlay; state-preserving localization tests apply |
| Transformer Language Modeling | yes | yes | yes | yes | dedicated four-locale catalog/browser/state tests |
| Agent Tool Use and Context Protocols | yes | yes | yes | yes | dedicated four-locale catalog/browser/state tests |
| Game Trees: Minimax / Alpha-Beta | yes | yes | yes | yes | dedicated four-locale catalog/browser/state tests |
| **Active Level-1 Quick Assigns (first four labs)** | yes | yes | **candidate** | **candidate** | must not be called four-language until v1.6.1 Quick Assign locale gate passes |
| Landing page | yes | yes | no | no | bilingual navigation/support surface; it may truthfully state that the 15 learner applets are four-language |
| Teacher Pack | yes | yes | no | no | bilingual educator surface |
| Curriculum Map | yes | yes | no | no | bilingual educator/navigation surface |
| Research and citation page | yes | yes | no | no | bilingual research/support surface |
| NN-1 Activity Pack | yes | no | no | no | student-facing Activity Pack pilot is English-only |
| CNN-1 Activity Pack | yes | no | no | no | student-facing Activity Pack pilot is English-only |
| Activity Pack index | yes | no | no | no | explicitly labels the Activity Pack pilot English-only |

## Verification rules

1. Current landing/Teacher Pack/curriculum metadata must describe the release as **15 applets = 13 Foundations/course-track labs + 2 Modern AI extensions**.
2. Current public pages must not contain a stale current-release statement that says the suite contains fourteen applets.
3. Historical release notes, archived audit records, and version-specific documentation may truthfully retain older counts and language boundaries; the currency scan must not rewrite history.
4. Every learner applet claiming four-language support must expose EN/ZH/VI/ES in its declared localization metadata/catalog and pass its applicable state-preservation checks.
5. A support page with only EN/ZH controls must not be described as itself four-language merely because it links to four-language applets.
6. Activity Packs remain English-only until separately translated and verified.
7. Quick Assign locale status is activity-specific. The first four canaries are intended to become EN/ZH/VI/ES in the v1.6.1 candidate, but this document records that as a gate rather than assuming it.

## Paper / external-communication wording

Preferred:

> AI Playgrounds v1.6 contains 15 learner applets with English, Simplified Chinese, Vietnamese, and Spanish support. The current educator/navigation pages have a narrower language boundary, and the first Activity Pack pilot is English-only.

Avoid:

> AI Playgrounds is a fully four-language website.

Avoid:

> All teaching materials are available in four languages.

Those stronger claims are not established by the current public surface.