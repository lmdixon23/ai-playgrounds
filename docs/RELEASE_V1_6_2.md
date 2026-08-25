# AI Playgrounds v1.6.2

**Release date:** 2026-08-26

v1.6.2 is a narrow public-provenance hotfix over v1.6.1. It changes no applet algorithm, curriculum item, Quick Assign, Activity Pack, or learner mechanism.

## Why this patch exists

The post-deployment audit of the exact v1.6.1 GitHub Pages artifact found that several current-version markers still reported `v1.6.0` even though the functional v1.6.1 changes were deployed correctly. The remaining stale markers included the homepage version footer, analytics wrapper attributes, and hidden legacy chrome inside Labs 13–15.

This was a release-provenance consistency defect, not an algorithm or classroom-behavior defect.

## Changes

- Normalizes the homepage visible current-release marker to v1.6.2.
- Normalizes the inline analytics wrapper provenance marker to v1.6.2 across every measured public HTML surface.
- Normalizes current-version metadata across all 15 applets.
- Removes stale v1.6.0 current-version tokens from the shipped legacy chrome inside Labs 13–15 while preserving their standard shared v1.6.2 shell.
- Preserves v1.6.0 and v1.6.1 as historical release-note sections rather than rewriting release history.
- Adds `tools/test_v1_6_2_public_provenance.py` to the normal Verify stack so the exact generated `_site` artifact must agree on its current version before publication.

## Evidence boundary

The hotfix establishes consistency of current-release provenance in the tested generated artifact. It does not change or newly establish algorithm correctness, learning gains, classroom adoption, accessibility conformance, learner preference, or educational efficacy.

The release process remains fail-closed: exact-head Verify, exact-main Verify, Pages deployment from the same SHA, and a version-specific publisher are required before the v1.6.2 tag/release may be created.
