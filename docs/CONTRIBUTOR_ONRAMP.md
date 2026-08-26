# Contributor on-ramp

AI Playgrounds benefits most from bounded contributions that preserve algorithmic meaning, current learner-locale parity, offline portability, privacy boundaries, and deterministic verification.

## Good first contributions

1. **Translation review:** compare one English source string with its Simplified Chinese, Vietnamese, or Spanish learner-facing counterpart and open an issue describing the exact semantic or naturalness mismatch. Do not include student data.
2. **Keyboard smoke test:** record the tab order, focus visibility, and blocked operations for one applet without claiming WCAG conformance.
3. **Browser evidence:** run one named browser/viewport or text-enlargement case and attach only non-sensitive console/output evidence.
4. **Quick Assign or lesson activity review:** audit one existing `QA-*` task against `predict -> manipulate/run -> observe -> explain -> transfer`, or propose a bounded Level-2 activity tied to one applet and one objective.
5. **Deterministic edge case:** add one small algorithm test that demonstrates a boundary, tie, or failure mode.
6. **Documentation repair:** clarify one fidelity limit, prerequisite, current product boundary, or explanation that could mislead a beginner or contributor.

## Invariants

- Every public applet satisfies the current minimum contract in `docs/APPLET_DESIGN_SYSTEM_CONTRACT.md`.
- Each applet remains independently usable under the project's documented offline/self-contained boundary.
- Offline/local use sends no analytics.
- English, Simplified Chinese, Vietnamese, and Spanish learner-facing meaning/state remain aligned for the declared learner surfaces.
- A support/teacher page must not claim a locale it does not actually provide; see `docs/PUBLIC_SURFACE_LOCALE_MATRIX.md`.
- New controls, states, share parameters, catalogue/search fields, and assignment behavior receive deterministic or browser regression coverage appropriate to the change.
- New labs inherit the shared public shell/provenance and complete catalogue schema rather than copying a bespoke shell from the most recent lab.
- Every public applet has one stable Level-1 Quick Assign; changes must preserve it or deliberately revise its contract and tests.
- Simplified pedagogical models are labeled; no production-equivalence claim is introduced.
- Student work, response text, grades, or identifying data are never included in analytics, issues, fixtures, screenshots, or examples.

## Review packet

A pull request should state:

- applet/surface;
- learning objective;
- behavioral change;
- algorithm/fidelity effect;
- localization effect and declared locale scope;
- accessibility/HCI effect;
- responsive effect;
- state-sharing or local-response effect;
- Quick Assign/Activity Pack effect;
- privacy/analytics effect;
- exact validation commands.

Keep one conceptual change per pull request where practical.

## Advanced/deferred work

KNN regression mode, hill-climbing restart benchmarks, CDCL trace mode, and future modern-extension labs are intentionally not first issues. They alter the data model, explanatory layer, localization surface, assignment contract, and deterministic-test boundary together.

Before implementing a future lab or major mode, read:

- `docs/APPLET_DESIGN_SYSTEM_CONTRACT.md`
- `docs/PUBLIC_SURFACE_LOCALE_MATRIX.md`
- `docs/QUICK_ASSIGN_ARCHITECTURE.md`
- the relevant mechanism-specific audit/architecture note.
