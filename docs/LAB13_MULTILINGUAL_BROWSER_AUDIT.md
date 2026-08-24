# Lab 13 Four-Locale Browser Integration Audit

Status: **PASS — EN/ZH/VI/ES browser parity accepted for the non-public Lab 13 candidate**.

English source freeze: `e89c0b5d8b166b66407fc018deb1b7eec485b6a4`.

Accepted semantic checkpoints:

- English source candidate: Verify run #118 (`32729175781`) PASS;
- Simplified Chinese semantic parity: `f550b21d37951a511c4b311b33981284fd4f9d8f`, Verify run #120 (`32730071342`) PASS;
- Vietnamese and Spanish semantic parity: `84a027795beed4b03df2af056a4ac1c68eab356e`, Verify run #131 (`32731989720`) PASS.

Accepted four-locale browser head: `5f752a3e9d0bd23f1fbba6403cdde2ad6267265d`.

Permanent Verify receipt: run #136 (`32733069544`) rerun job `97449891539` — **PASS**.

Evidence artifact: `ai-playgrounds-verification-32733069544`, artifact ID `9522291944`, SHA-256 `7ce1b51ab3719f4883de21ccce2734cba9046b323a09d81cb868e739bc576642`.

## 1. Candidate architecture

`tools/build_transformer_multilingual_candidate.py` deterministically combines:

- the frozen English single-file applet;
- the EN/ZH semantic catalog;
- the VI/ES semantic catalog;
- a small in-document localization runtime.

The resulting verification candidate is generated at:

`release-evidence/lab13-transformer-multilingual-candidate.html`

This remains a non-public verification artifact. It is not yet under `playgrounds/` and therefore does not change the deployed applet count.

The candidate is self-contained: localization catalogs are embedded into the generated HTML and the runtime performs no network request.

## 2. Locale-switch invariant

The browser gate establishes non-default model state before switching locale:

- constrained custom prompt;
- position vectors disabled;
- non-default temperature;
- Q perturbation active;
- a selected attention-matrix cell;
- a locked Guided Challenge prediction.

The test then switches through Simplified Chinese, Vietnamese, Spanish, and English and requires all of the following for every locale:

1. the expected locale-specific document language;
2. localized major semantic surfaces;
3. preservation of the complete experiment/control state;
4. byte-equivalent serialized model arithmetic for the tested state;
5. preservation of model-data tokens such as `<BOS>` and `<UNK>`.

Thus locale switching is treated as a presentation transformation rather than a model transformation.

## 3. Dynamic-state localization

Static translation alone is insufficient because scenario notes, challenge results, matrix state, and text-equivalent state are produced after interaction.

The browser gate therefore verifies dynamic rerendering after a locale switch, including:

- a Vietnamese temperature-scenario note generated after the switch;
- a Spanish substitution-challenge result generated after the switch;
- localized text-equivalent numeric state;
- preservation of protected mathematical/model identifiers inside translated prose.

The localization runtime observes newly generated learner-facing text and maps it back through the frozen semantic catalogs without changing arithmetic state.

## 4. Responsive and offline boundary

The generated candidate must:

- remain a single HTML file;
- contain no runtime `fetch` or `XMLHttpRequest` dependency;
- remain outside the public `playgrounds/` tree during this checkpoint;
- avoid document-level horizontal overflow at a 390 px mobile viewport in all four locales.

Wide matrices may continue to scroll within their own bounded containers.

## 5. Dedicated four-locale browser gate

`tools/test_transformer_multilingual_applet.py` completed **40/40 checks**, with:

- `page_errors = []`;
- `console_errors = []`.

The permanent workflow also passed the complete inherited and Lab 13 stack:

- release check: **1240 pass, 0 warn, 0 fail**;
- pedagogical contracts: **253/253**;
- existing Guided Challenge static contracts: **106/106**;
- existing Guided Challenge browser-state cases: **12/12**;
- existing Simplified-Chinese static parity: **117/117**;
- existing Simplified-Chinese browser parity: **12/12**;
- existing Vietnamese/Spanish R4 localization: **PASS**;
- Wumpus dynamic percept localization: **16/16**;
- existing Vietnamese/Spanish R4 browser QA: **12/12**;
- release metadata: **PASS**;
- deployment boundary: **52 files, PASS**;
- inherited algorithm regression: **45/45**;
- Lab 13 Transformer reference tests: **20/20**;
- Lab 13 Python/JavaScript parity: **8/8**;
- Lab 13 prototype browser QA: **26/26**;
- Lab 13 English single-file candidate QA: **46/46**;
- Lab 13 Simplified-Chinese semantic gate: **540/540**;
- Lab 13 Vietnamese/Spanish semantic gate: **794/794**;
- Lab 13 four-locale browser parity: **40/40**;
- complete browser/responsive QA: **63/63**.

## 6. Adversarial failures retained as regressions

Two failures occurred before the accepted receipt.

First, the initial multilingual browser test referenced a nonexistent semantic-catalog key for the Guided Challenge heading. The test was corrected to use the frozen `challenge.title` key; the localization semantics were not weakened.

Second, the first execution of run #136 encountered an unrelated transient timeout in the inherited KNN Guided Challenge browser test before reaching the Lab 13 gates. The same workflow job was rerun without a repository change and passed the complete stack. The accepted evidence therefore comes from the successful rerun job `97449891539`.

## 7. Deployment boundary

This checkpoint deliberately leaves the public application unchanged.

The minimal Pages artifact remained exactly **52 files** and exactly the existing **12 public applets**. Lab 13 was tested only as a generated release-evidence candidate.

That boundary is now cleared for the next phase: construct the thirteenth public applet and update navigation, applet metadata, curriculum/release surfaces, deployment scope, and the associated exact-count/static/browser contracts. The public integration must receive a fresh complete permanent-workflow PASS before PR #19 can be considered merge-ready.

## 8. Acceptance decision

**PASS.**

The non-public four-language Lab 13 browser candidate satisfies the current localization, interaction-state, arithmetic-invariance, offline, responsive, and regression boundaries. Public Lab 13 integration may proceed, but no merge or deployment is authorized by this checkpoint alone.
