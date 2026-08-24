# AI Playgrounds v1.4 Product-Quality Audit

Date: 2026-08-25

Status: **PASS — product-quality behavior candidate accepted; release-metadata and final exact-head receipt pending**.

Accepted behavior candidate head: `1a30893ce0341e3063bb969921cd8b66d1243915`.

Permanent Verify run `32780480520`, job `97601258430`: **PASS**.

Evidence artifact: `ai-playgrounds-verification-32780480520`, artifact ID `9539645266`, SHA-256 `4e7e5ec532076e19967252a7805825651dd200d4002449071c47bb3f1bbd8cbf`.

## 1. Scope

v1.4 is deliberately a fourteen-app product-quality release rather than a Lab 15 release. It preserves the v1.3 public inventory while strengthening navigation, language selection, release provenance, and the learner-facing visual story in Labs 13 and 14.

The curriculum coverage matrix remains planning evidence for Lab 15+ and explicitly prevents the post-v1.3 roadmap from drifting into contemporary-only topics while classical introductory-AI gaps remain.

## 2. Lab 13 engagement pass

The accepted v1.4 Transformer wrapper is presentation-only over the frozen v1.3 public mechanism.

It adds:

- an explicit four-stage journey: Tokenize -> Represent -> Attend -> Predict;
- focusable stage controls that emphasize the existing relevant mechanism panels;
- accessible current-stage state;
- a native EN/ZH/VI/ES language selector;
- secondary rather than hero-level software-version provenance.

The v1.4 QA proves that changing the journey stage does not change prompt state, temperature, mask state, position vectors, perturbation state, scenario state, Guided Challenge state, or Transformer arithmetic. The canonical frozen final-row attention vector remains exactly within the existing numeric tolerance.

## 3. Lab 14 engagement pass

The accepted v1.4 agent wrapper preserves the frozen tool catalog, deterministic action policy, authorization rules, tool world, provenance rules, and protocol semantics.

It extends the learner-visible runtime path to:

`Propose -> Validate -> Authorize -> Execute -> Observe -> Update / choose next -> Stop`

The visual layer now makes the selected action explicit and distinguishes:

- schema rejection at validation;
- permission denial at authorization;
- execution errors after actual execution;
- successful observations entering context before a new action is chosen;
- STOP becoming the justified action after goal completion.

The canonical Oslo trace remains `weather.current -> 8 C -> unit.convert_temperature -> 46.4 F -> STOP`. Invalid and unauthorized calls remain side-effect free.

## 4. Language-control normalization

The accepted candidate removes the remaining prominent four-button locale controls from Labs 13 and 14 and replaces them with native four-option selectors while retaining the tested localization runtimes and `?lang=` deep-link behavior.

The inherited twelve applets already expose their four locales through the existing native `.r4-language-select` overlay; the legacy compatibility buttons remain hidden. The v1.4 public shell additionally adapts the landing and support-page language controls to native selectors using the locales actually available on those surfaces rather than pretending that untranslated support content exists.

State-preservation tests confirm that locale changes in Labs 13 and 14 do not mutate the learner's machine/model state.

## 5. Curriculum/navigation pass

The v1.4 candidate retains all fourteen public applets while introducing a clearer distinction between:

- Foundations / course track;
- Modern AI extensions;
- the existing quick-entry sampler.

The Foundations / course table contains thirteen entries with Transformer Language Modeling at the course/modern boundary. Agent Tool Use and Context Protocols is removed from the classical foundations table and identified as a modern extension. The curriculum applet map is regenerated from the complete fourteen-entry release inventory so no generated applet disappears from navigation.

## 6. Public integration boundary

The accepted behavior candidate preserves:

- fourteen unique public applets;
- the 54-file minimal Pages artifact;
- all inherited v1.3 Lab 13 and Lab 14 regression gates;
- all legacy algorithm, pedagogy, localization, and browser gates;
- one-file/offline operation for Labs 13 and 14;
- responsive containment including the 390 px v1.4 checks;
- zero page and console errors in the new v1.4 browser gates.

The full permanent Verify workflow passed all 33 inherited/new verification stages before the evidence upload and workflow teardown, including the new Lab 13 v1.4 gate, Lab 14 v1.4 gate, v1.4 public product-quality integration gate, and complete inherited browser/responsive QA.

## 7. Evidence boundary

This pass establishes deterministic software behavior, mechanism preservation, localization-state preservation, navigation completeness, and browser containment. It does not establish classroom learning gains, adoption, or formal accessibility conformance.

## 8. Release boundary

The candidate above is the accepted behavior baseline. Release-metadata staging may now proceed, but that staging changes the branch head and therefore requires a fresh complete Verify PASS.

No v1.4.0 tag or GitHub Release may be created before:

1. release metadata and deployment/publication workflows are staged;
2. the exact release-candidate head receives a complete permanent Verify PASS;
3. the receipt-bearing audit head receives any required final documentation-only Verify PASS;
4. PR #21 is squash-merged once into `main`;
5. the merged `main` head passes its push verification and Pages deployment;
6. the v1.4.0 tag and release resolve exactly to that deployed, verified merged-main commit.

Lab 15 implementation remains blocked until this v1.4 release boundary is complete.