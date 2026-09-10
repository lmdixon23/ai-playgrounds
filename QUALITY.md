# Quality and evidence boundaries

AI Playgrounds contains **15 applets = 13 Foundations/course-track labs + 2 Modern AI extensions**, with one Level-1 Quick Assign per lab. NN-1 and CNN-1 are longer Level-2 Activity Pack pilots.

## What release checks cover

Maintainer verification checks bounded software behavior under specified conditions:

- algorithm outputs, semantic invariants, and representative exact/reference cases;
- shared page components, responsive containment, and cross-lab visual regression;
- state transitions, reset/recovery behavior, and experiment sharing;
- dynamic language changes and preservation of experiment state and learner drafts;
- keyboard/focus behavior, labels, text-equivalent state, reduced motion, and representative contrast;
- independently movable offline HTML, blocked-network operation, and download integrity;
- exclusion of learner responses and private information from analytics and published content;
- exact release metadata, artifact bytes, and deployment identity.

These are checks of the finished product, not just its editable sources. The website and the single-file downloads have different packaging and are both checked. The development test suite and operational evidence are not distributed in this repository.

## What those checks do not establish

Human learner and educator usability studies and human screen-reader testing are deferred for this release. Automated checks are not substitutes for those activities. The project does not claim WCAG conformance, validated learning gains, educator adoption, universal browser compatibility, or superiority over another teaching approach.

Visual regression detects changes to reviewed states; it does not prove that every component is optimal or that all pre-existing differences are resolved. Mechanism-specific variations remain legitimate when they preserve the common learner experience. See the [design-system contract](docs/APPLET_DESIGN_SYSTEM_CONTRACT.md).

## Languages and classroom use

All fifteen learner applets and Quick Assigns support English, Simplified Chinese, Vietnamese, and Spanish. Educator/support pages and Level-2 activities have narrower [language boundaries](docs/PUBLIC_SURFACE_LOCALE_MATRIX.md). Automated parity does not establish fluent-reader naturalness.

Responses stay on the learner's device until deliberately copied, exported, printed, or submitted through another system. The project has no grading or student-submission backend. See [privacy](docs/ANALYTICS_AND_PRIVACY.md) and the [Teacher Pack](https://lmdixon23.github.io/ai-playgrounds/teacher-pack.html).

## Report a reproducible defect

Use [Contributing](CONTRIBUTING.md) for browser, layout, translation, or mechanism reports, and [Security](SECURITY.md) for sensitive disclosures. Version-specific fixes and limitations belong in the [release notes](RELEASE_NOTES.md), not in unsupported general claims.
