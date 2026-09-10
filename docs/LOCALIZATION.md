# Localization standard

AI Playgrounds localizes learner experiences, not just isolated controls. Current language availability is scoped by the [public surface locale matrix](PUBLIC_SURFACE_LOCALE_MATRIX.md); these requirements must not be read as a claim that all support pages are already translated.

## Meaning-bearing text

Within a surface's declared language coverage, translation includes:

1. navigation, buttons, status messages, hints, errors, and accessibility text;
2. applet titles, scenarios, featured experiments, explanations, glossaries, and teacher prompts;
3. visible resource labels and footer text;
4. dynamic text created after an interaction, not just text present at initial load;
5. Quick Assign labels, prompts, placeholders, state labels, and response-packet headings.

## Stable technical literals

Keep URLs, filenames, query keys, code identifiers, formulas, mathematical symbols, variable names, license identifiers, author names, ORCID values, and DOI values stable when translation would damage their meaning or identity. Established acronyms such as BFS, DFS, A*, CNF, SAT, DPLL, MSE, and LMS retain their technical meaning.

A visible link label can be translated without renaming its target. Glossaries should cover the prerequisite vocabulary for the mechanism without becoming an encyclopedia before the interaction.

## Dynamic state and reversibility

Changing language must update the current instructions and state descriptions without requiring a reload. Round trips between English and the other learner languages should restore the expected title, controls, dynamic labels, challenges, and packet headings.

Translation must not silently restart the experiment, change the seed, switch the challenge, clear a committed prediction, alter numerical state, or erase learner-authored responses. The learner's own response text must not be machine-translated as a side effect of changing the interface language.

## Review and expansion

Review technical meaning, terminology, text expansion, line breaking, mobile layout, print layout, and accessible labels. A fluent educator or subject specialist can identify naturalness issues that automated checks cannot establish. Human language review must not be implied merely because software checks pass.

Before expanding a language claim to a new surface, cover its complete interaction sequence and verify state preservation and layout. Report the exact affected page, language, wording, and proposed improvement through [Contributing](../CONTRIBUTING.md).
