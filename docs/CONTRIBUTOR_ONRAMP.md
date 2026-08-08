# Contributor on-ramp

AI Playgrounds benefits most from bounded contributions that preserve algorithmic meaning, bilingual parity, offline portability, and deterministic verification.

## Good first contributions

1. **Translation review:** compare one English/Simplified-Chinese control, explanation, limitation, or scenario and open an issue describing the exact semantic mismatch.
2. **Keyboard smoke test:** record the tab order and blocked operations for one applet without claiming WCAG conformance.
3. **Browser evidence:** run one named browser/viewport case and attach only non-sensitive console/output evidence.
4. **Lesson activity:** contribute a 15–25 minute predict–run–explain activity tied to one applet and one objective.
5. **Deterministic edge case:** add one small algorithm test that demonstrates a boundary, tie, or failure mode.
6. **Documentation repair:** clarify one fidelity limit, prerequisite, or explanation that could mislead a beginner.

## Invariants

- Each applet remains independently usable as one HTML file.
- Offline/local use sends no analytics.
- English and Simplified-Chinese learner-facing meaning remains aligned.
- New controls, states, and share parameters receive deterministic tests.
- Simplified pedagogical models are labeled; no production-equivalence claim is introduced.
- Student work or identifying data is never included in issues, fixtures, screenshots, or examples.

## Review packet

A pull request should state the applet, learning objective, behavioural change, algorithm/fidelity effect, localization effect, accessibility effect, state-sharing effect, and exact validation commands. Keep one conceptual change per pull request.

## Advanced/deferred work

KNN regression mode, hill-climbing restart benchmarks, and CDCL trace mode are intentionally not first issues. They alter the data model, explanatory layer, localization surface, and deterministic-test contract together.
