# Localization Standard

AI Playgrounds localizes complete learner and educator experiences rather than isolated interface controls.

## Translation boundary

Translate every meaning-bearing string that a learner, teacher, reviewer, or visitor reads while using the public site:

1. navigation, buttons, status messages, hints, errors, and accessibility text;
2. applet titles, descriptions, scenarios, featured experiments, explanations, glossaries, and teacher materials;
3. landing-page cards, durations, filters, resource labels, and footer text;
4. dynamic text produced after an interaction, not only text present at initial page load;
5. visible labels for technical resources.

Keep stable literals unchanged when translation would damage interoperability or source identity:

1. URLs, filenames, file extensions, query keys, and code identifiers;
2. formulas, mathematical symbols, and variable names;
3. license identifiers, author names, ORCID values, commit hashes, and DOI values;
4. established algorithm acronyms such as BFS, DFS, A*, CNF, SAT, DPLL, MSE, and LMS.

A visible label may be translated while its underlying filename or URL remains unchanged. For example, the link label Architecture guide becomes 架构说明 while the source filename remains `ARCHITECTURE.md`.

## Glossary sizing

Glossaries are sized by prerequisite load rather than a fixed quota. Each applet should define enough concepts for a new learner to read the full explanation without an unexplained term, while avoiding an encyclopedia before the interaction.

Current acceptance range: 6 to 12 terms per language, with equal English and Chinese coverage. The precise count should vary by applet.

## Dynamic-state requirement

Changing language must update the current state immediately. A reload must never be required to translate:

1. instructions generated after choosing a dataset or scenario;
2. live status and result summaries;
3. featured experiment text;
4. share, copy, export, and classroom controls;
5. accessibility state descriptions.

Every new dynamic string requires an English and Chinese source at the point where the state is created.

## New-language gate

A new language is ready only when all of the following are complete:

1. all public learner and educator content is covered;
2. dynamic-state regression tests pass;
3. terminology is reviewed by a proficient human educator or subject specialist;
4. text expansion, line breaking, mobile layout, print layout, and accessibility labels pass;
5. discoverable language-specific URLs and `hreflang` metadata are defined;
6. a named maintenance owner can review future changes.
