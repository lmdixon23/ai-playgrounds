# AI Playgrounds v1.7.1

Release date: 2026-08-27

## Summary

v1.7.1 is a **consistency and compatibility patch**. It does not add a lab, algorithm, learner language, Quick Assign, or curriculum unit.

The patch closes a remaining interaction inconsistency between the original applets and Labs 13–15: theme preference now uses the same canonical `theme` storage contract across the entire suite.

## Changed

- Transformer Language Modeling, Agent Tool Use and Context Protocols, and Game Trees: Minimax / Alpha-Beta now read and write the same persisted `theme` preference used by the original applets.
- An existing `ai-playgrounds-theme` value from the temporary modern-shell implementation is used only as a one-time migration fallback and is then removed.
- If no theme preference is stored, the modern-lab shell follows the browser/system dark-mode preference, matching the established original-app behavior.
- The standardized modern-shell theme button now keeps its icon and `aria-pressed` state synchronized with the active light/dark theme.
- Current repository documentation and CI hygiene inherited from the immediately preceding main hardening remain in force, including the current-document consistency gate and retirement of obsolete v1.3–v1.6 publisher workflows.

## Preserved boundaries

v1.7.1 preserves exactly:

- 15 public applets / 58 deterministic public files;
- 13 Foundations/course-track labs + 2 Modern AI extensions;
- all 15 Level-1 Quick Assigns;
- the two Level-2 Activity Pack canaries, NN-1 and CNN-1;
- EN/ZH/VI/ES learner-app and Quick Assign support;
- all v1.7.0 algorithm, challenge, localization, privacy, HCI, and curriculum semantics.

Reset-by-reload remains the modern-shell reset mechanism in this patch. It resets the applet mechanism while preserving URL locale and local response-draft behavior. The consistency audit did not find evidence that replacing it with a different reset implementation would improve the learner model or recovery path.

## Verification

The release retains the complete inherited verification stack and adds a dedicated modern-shell continuity gate that checks:

- an original-app `theme=dark` preference is honored by Labs 13–15;
- toggling a modern lab writes the canonical shared `theme` key;
- the temporary modern-shell key migrates and is removed;
- system dark preference is honored when no stored preference exists;
- the theme control icon and accessibility state match the active theme;
- no page or console errors occur under the tested paths.

A v1.7.1 public-release gate also verifies the unchanged 15-app/58-file boundary, current version/provenance markers, all-lab Quick Assign presence, and the inherited current-document/release contracts.

## Evidence boundary

These checks establish bounded software and interaction behavior under tested conditions. They do not establish learning gains, classroom adoption, universal learner preference, accessibility conformance, or educational impact.

The archived v1.0.1 DOI remains historical provenance and is not reassigned to v1.7.1.