# Contributing

Contributions that preserve the classroom, accessibility, and portability goals are welcome.

## Before opening a pull request

1. Keep each applet usable as one HTML file.
2. Preserve complete English and Chinese learner and educator content, including dynamic strings.
3. Keep controls usable with a keyboard.
4. Preserve the text-state explanation.
5. Add or update tests when algorithmic behavior changes.
6. Run `python tools/release_check.py`.
7. Run `python tools/browser_qa.py --no-screenshots`.
8. Explain any intentional model simplification in the teacher notes.
9. Add a dynamic localization regression whenever an interaction creates new visible text.
10. Keep glossaries concept-sized rather than padding every applet to the same count.

## Contribution scope

Useful contributions include:

- correcting algorithm behavior,
- improving accessibility,
- clarifying learner instructions,
- adding meaningful scenarios,
- improving translations,
- repairing responsive layouts,
- strengthening tests,
- improving offline behavior.

Do not add accounts, student tracking, required external services, or runtime dependencies without first discussing the architectural impact.