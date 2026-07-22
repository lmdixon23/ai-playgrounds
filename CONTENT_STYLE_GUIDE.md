# Learner-facing content house style

This guide governs public text inside AI Playgrounds. The primary audience is a multilingual secondary-school learner who may know the course idea but not the specialist vocabulary.

## 1. Name the idea before shortening it

- Write the full term at first use, followed by the abbreviation in parentheses.
- After that first definition, the abbreviation may be used within the same page section.
- Do not place an unexplained abbreviation in a page title, scenario title, control label, tooltip, or first paragraph.
- Define mathematical symbols by name before asking learners to interpret them. Example: `exploration rate (ε)`.
- Treat every scenario card as a standalone entry point. Define an abbreviation again when a learner could open that card without reading an earlier card.

## 2. Use one canonical applet name

The title in `applets.json` is the canonical public name. Use it in the catalogue, page heading, browser title, Open Graph metadata, curriculum materials, and teacher materials. A descriptive subtitle may explain the mechanism, but it must not replace the canonical name.

## 3. Write scenarios as a reasoning sequence

Every scenario card uses four moves:

1. **Core question:** the conceptual problem, written as a question.
2. **Run and watch:** the exact controls or comparison to run and the evidence to inspect.
3. **Predict first:** a specific prediction that can be checked after the state changes.
4. **Explain afterward:** the causal or algorithmic relationship the learner should explain.

Avoid repeating the scenario title as a separate concept field. Keep teacher-only facilitation advice in the teacher notes rather than the learner card.

## 4. Explain in the order learners need

Use this order for an explanation:

1. familiar purpose or observable problem,
2. names and characteristics of the main components,
3. one step of the mechanism,
4. the visible evidence that step produces,
5. the limitation or simplification.

A compact key-terms panel should appear before the detailed mechanism. The long explanation should repeat that primer at its opening so a direct jump never skips prerequisite vocabulary. Longer explanations should use informative headings and short learner-paced sections.

## 5. Prefer concrete, direct language

- Use active verbs: `compare`, `move`, `count`, `trace`, `predict`, `explain`.
- Keep one main idea per sentence.
- Address the learner directly when giving an action.
- Use a conversational professional tone, not slang and not research-audit language.
- Avoid all-caps emphasis, unexplained symbols, ornamental metaphors, and claims that an applet proves learning.
- Describe what the learner can observe rather than announcing that a result is obvious, easy, surprising, or correct.

## 6. Keep the toolbar predictable

Every applet shows the same primary action order:

1. Share
2. More
3. Reset, or an accurate applet-specific equivalent such as New world

The More menu always contains Embed in LMS and Current settings (.json). Data-table and image exports appear only when the applet can produce them. Contextual exports may differ; the position and hierarchy do not.

## 7. Maintain bilingual parity

- English and Chinese should express the same task, evidence, and limitation.
- Preserve technical abbreviations after defining them in both languages.
- Do not translate code symbols, variable names, or established algorithm names inconsistently.
- Review the Chinese as instructional writing, not as a word-for-word gloss.

## 8. Quality checks

Before release, verify that every applet has:

- one canonical title,
- a plain-language purpose statement,
- at least five defined key terms,
- five learner-first scenarios,
- no teacher-use field inside learner scenario cards,
- the standard Share / More / Reset action hierarchy,
- no unexplained high-risk abbreviation in the title or purpose statement,
- English and Chinese versions of the terms and scenario prompts.
