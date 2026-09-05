# AI Playgrounds v1.9 baseline capture receipt

Status: accepted pre-refactor evidence for issue #56.

## Frozen product baseline

The product baseline remains exact `main` commit:

`d1c72e10e6c5bf64b9a4bbed578b2305d1c988d0`

Current software release: `v1.8.1`.

The evidence harness was intentionally run from a temporary PR branch that changes only the capture harness and workflow invocation. It is not product code and must never be merged into `main`.

## Accepted evidence run

GitHub Actions Verify run:

`33968039477`

Conclusion: PASS.

Both required jobs passed:

- Release and browser checks, job `101311531362`;
- v1.8.1 final artifact, algorithm modes, and modern learner parity, job `101311531262`.

The added evidence step `Capture exact v1.9 baseline visual and hash evidence` passed after all inherited v1.8.1 gates.

## Evidence-only branch identity

Evidence branch head:

`ecb0803aef825bcdd5d7600352b95622f701ba25`

The CI checkout executes the pull-request merge ref, so the generated report records an ephemeral merge HEAD rather than treating the evidence branch commit as the frozen product source. The evidence payload separately and explicitly records the frozen product baseline SHA above.

The capture harness verifies that the only branch changes relative to the frozen product baseline are:

- `.github/workflows/verify.yml`;
- `tools/capture_v1_9_baseline.py`.

If any other path changes, the capture fails closed.

## Generated artifact evidence

The capture rebuilt `tools/build_site_v1_8_1.py` and required:

- exactly 58 generated files;
- exactly 15 generated applets;
- the exact expected fifteen slug set;
- v1.8.1 page identity;
- no page or console errors during capture;
- requested theme activation.

`docs/V1_9_BASELINE_ARTIFACT_SHA256.json` records the accepted SHA-256 digest of every one of the 58 generated public files.

This manifest is the direct byte-equivalence oracle for the initial #47 architecture refactor.

## Diagnostic visual census

The accepted run captured:

- 15 generated applets;
- desktop 1366×900;
- phone 390×844;
- light theme;
- dark theme;
- English initial state;
- 60 screenshots total;
- 0 capture failures.

The screenshots are retained in the GitHub Actions evidence artifact and are diagnostic pre-refactor evidence rather than permanent post-design visual-regression goldens.

## Retained GitHub Actions artifacts

### Full inherited verification

Artifact ID: `9970115330`

Name: `ai-playgrounds-verification-33968039477`

Digest:

`sha256:ca6d71da8aad1a34bfd381f80319c5c91efcc71d24a8a2d4c17686163ec8e557`

### v1.8.1 plus v1.9 baseline capture

Artifact ID: `9970085263`

Name: `ai-playgrounds-v1.8.1-verification-33968039477`

Digest:

`sha256:7f6c5d3a4ef3a8a167878779972a8e2a2f36b369c40f133037c56e87e85291a2`

The latter contains the 58-file hash manifest, machine-readable baseline report, human-readable receipt, and all 60 screenshots.

## Human-protocol migration

The reusable methodology from `planning/v1.5-human-usability-validation` has been superseded and expanded by the current v1.9 human-validation workstream.

The v1.9 protocol now covers:

- all fifteen labs rather than the earlier focused subset;
- 12 first-time learners per primary cycle with four independent observations per lab;
- six educators per primary cycle;
- separate ZH, VI, and ES fluent-reader review;
- release-candidate retest with fresh first-time participants;
- separate learner, educator, and locale evidence schemas.

Once that planning PR is accepted, the old v1.5 planning branch has no remaining unique methodological role and can be deleted under #53 after final branch-diff confirmation.

## Preliminary visual findings

The diagnostic contact-sheet review exposes genuine current inconsistencies that should be addressed only after the byte-equivalent architecture boundary closes:

1. The established twelve use `Share / More / Reset all`, while Transformer, Agent, and Minimax expose `Share / Embed / JSON / Reset lab` as a different mobile/desktop action hierarchy.
2. The modern three have different preference/header geometry, especially on phone layouts.
3. The established twelve consistently orient with `WHAT THIS APPLET SHOWS`; the modern three lead with `THE BIG IDEA` and a distinct orientation grammar.
4. Several labs intentionally or accidentally retain light mechanism canvases in dark theme. These require mechanism-by-mechanism classification rather than blanket normalization.
5. Reset/recovery wording varies between generic reset and concept-specific operations such as Wumpus `New world`; #48 must distinguish semantic difference from accidental naming drift.

These observations are now tracked in #48. The current v1.8.1 visual state must not be mistaken for a reviewed v1.9 design golden merely because release tests encode it.

## #56 closure assessment

All substantive baseline prerequisites for #47 are now present:

- exact source SHA;
- exact successful current Verify receipt;
- deterministic two-build current gate;
- explicit source/generated/build-chain inventory;
- branch disposition;
- 58-file SHA-256 manifest;
- all-fifteen desktop/phone light/dark diagnostic capture;
- retained CI evidence digests;
- reusable human-validation methodology migrated to a current v1.9 workstream.

Issue #56 may therefore close after this receipt is reviewed into the v1.9 planning evidence chain.

## Handoff to #47

The first #47 implementation must fail closed unless the current canonical builder candidate reproduces every digest in `V1_9_BASELINE_ARTIFACT_SHA256.json`.

No visual, copy, interaction, algorithm, locale, Quick Assign, analytics, or recovery change belongs in that equivalence phase.
