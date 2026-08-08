# Release notes

## v1.0.1, 2026-08-08

### Launch hardening

- Added a bilingual five-minute start path and dedicated educator/reviewer routes.
- Standardized privacy-minimized aggregate analytics across public pages without loading third-party JavaScript.
- Analytics run only on the canonical GitHub Pages host, honor GPC/DNT and explicit opt-out, exclude URL query strings from page paths, and send no experiment values or learner responses.
- Added durable release-evidence tooling, educator adoption guidance, classroom-pilot guidance, contribution templates, and launch materials.
- Synchronized the active Paper 7 source with the final v1.0.0 verification record while retaining historical pre-release records as provenance.
- Fixed the print-packet JavaScript regression introduced during the initial launch-hardening pass.

### Verification boundary

Software checks establish implementation and release integrity only. They do not establish learning gains, classroom adoption, or accessibility conformance.

## v1.0.0, 2026-07-25

AI Playgrounds includes twelve bilingual, offline-ready interactive demonstrations covering:

- search,
- local optimization,
- logical agents,
- satisfiability,
- Bayesian reasoning,
- supervised learning,
- model evaluation,
- neural networks,
- clustering,
- convolution,
- reinforcement learning.

## Included with every applet

- a focused interactive model,
- five learner scenarios,
- a featured experiment,
- complete English and Chinese visual and text-based explanations,
- teacher notes,
- model limitations,
- keyboard guidance,
- a printable student response packet,
- shareable experiment settings that preserve the exact current controls.

## Teaching materials

The release includes complete English and Simplified Chinese public teaching surfaces:

- a printable Teacher Pack,
- a responsive Curriculum Map,
- a one-page Student Lab Sheet,
- course-aligned and quick-entry sequences,
- citation and reuse information.

## Reliability and instructional accuracy

Explore panels include pre-rendered scenarios, dynamic text changes language immediately, and copied experiment links preserve later manual changes after a scenario is applied. The explanatory essays now introduce notation and prerequisite terms before use and narrow technical claims to their valid assumptions.

## Privacy and portability

The applets require no account, backend, database, package manager, or build step. Student responses remain local unless the learner copies or prints them.

## Release integrity

- GitHub Pages deploys a deterministic public artifact containing only intentionally published files.
- GitHub Actions requires the static release checks, all 45 algorithm regression tests, the release-metadata check, and the full browser and responsive QA matrix.
- The annotated release tag identifies the exact verified source revision.

## Scope

The project provides interactive teaching tools. Claims about learning gains, classroom adoption, or accessibility conformance require separate classroom and user studies.
