# AI Playgrounds v1.6.1

**Release date:** 2026-08-26

v1.6.1 is a teacher-adoption and cross-suite consistency release. It preserves the fifteen-lab curriculum and all v1.6.0 algorithms while repairing catalogue, localization, search, responsive, and product-shell drift exposed by a final-composition audit.

## Quick Assign canaries

- Formalizes four Level 1 Quick Assigns using existing Guided Challenge + local student response-packet machinery rather than adding a second assignment system.
- Active stable IDs: `QA-SEARCH-01`, `QA-LOCAL-01`, `QA-WUMPUS-01`, `QA-SAT-01`.
- Each is scoped to approximately 10–15 minutes and follows `predict -> manipulate/run -> observe -> explain -> transfer`.
- Teacher Pack and Curriculum links enter the canonical `Use in class` mode and resolve the stable activity anchor.
- EN/ZH/VI/ES switching preserves response text and applet state under the tested paths.

## Cross-suite consistency fixes

- Completes Lab 15 catalogue metadata so the landing card cannot render literal `undefined` fields.
- Adds full EN/ZH/VI/ES landing-page catalogue/navigation behavior and four-language discovery metadata.
- Enriches all 15 catalogue entries with likely teaching and technical search vocabulary; permanent checks cover `QKV`, `MCP`, `DPLL`, `alpha beta`, and `Bellman` aliases.
- Fixes the landing-page search lifecycle so the search box uses the enriched 15-lab renderer rather than an earlier 12-lab listener.
- Fixes VI/ES -> EN heading/title restoration across the original twelve applets, including rapid language switching by cancelling superseded delayed locale overlays.
- Gives Labs 13–15 one shared outer product shell for back navigation, title/subtitle, native four-language selection, Theme/Reset actions, and release/footer provenance while preserving concept-specific internal visualizations.
- Flattens the nested support-page language selector shell that produced a square control inside a rounded wrapper.
- Retains narrow-mobile translation-expansion containment.

## Permanent product contracts

- Adds `docs/APPLET_DESIGN_SYSTEM_CONTRACT.md`, defining the minimum shell, catalogue, localization, learning-support, HCI/accessibility-oriented, responsive, offline, privacy, search, and provenance requirements for current and future labs.
- Adds `docs/PUBLIC_SURFACE_LOCALE_MATRIX.md` so learner-app language coverage cannot be silently generalized to support pages that have a narrower translation boundary.
- Adds a final-composition browser gate over the generated `_site` artifact, including complete catalogue schema, no-undefined output, four-language landing behavior, representative search aliases, original-12 language round trips, shared modern-lab shell behavior, support-selector presentation, and 390 px containment.

## Verification boundary

The accepted pre-release consistency candidate passed:

- v1.6.1 Quick Assign/release-currency gate: **67/67**;
- v1.6.1 final-composition/design-system gate: **94/94**;
- the complete inherited release, pedagogical, guided-challenge, EN/ZH/VI/ES localization, algorithm, Lab 13/14/15, v1.4/v1.5/v1.5.1 integration/HCI, and final browser/responsive stacks.

The release process additionally requires a new exact-head pre-merge Verify pass after version/provenance staging, an exact-main push Verify pass after squash merge, successful Pages deployment from that same SHA, and a fail-closed publisher before the `v1.6.1` tag/release may be created.

Software/browser assurance establishes implementation behavior under the tested conditions. It does **not** establish learning gains, classroom adoption, universal learner preference, or accessibility conformance. The immutable v1.0.1 DOI remains historical provenance and is not reassigned to v1.6.1.
