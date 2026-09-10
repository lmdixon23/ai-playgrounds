# Contributing to AI Playgrounds

Contributions can improve a single explanation, translation, classroom activity, accessibility interaction, browser behavior, or mechanism. Small, reproducible reports are useful.

## Report a problem or suggest an improvement

[Open an issue](https://github.com/lmdixon23/ai-playgrounds/issues) with:

1. the affected lab or page, release version, and selected language;
2. browser/version, viewport or device category, and whether you used the website or a standalone download;
3. the steps taken, expected behavior, and actual result;
4. a minimal example or screenshot with private information removed.

Do not include student names, school identifiers, answers, private records, credentials, or device-local paths. Use an experiment link only after checking that it contains no private information. Report security concerns through the [Security policy](SECURITY.md), not a public issue that could expose users.

## Classroom and language feedback

For a teaching suggestion, identify the learning objective, expected prior knowledge, time available, and what evidence a learner should produce. Do not send raw student records. For a translation, quote the affected UI text, give a proposed alternative, and explain the technical meaning that must be preserved. Human naturalness review and automated language-state checks answer different questions.

## Product contracts

- Keep independently downloadable HTML usable offline, without accounts or backend services.
- Preserve the algorithm's meaning and state; distinguish an exact result from an estimate or teaching simplification.
- Follow the [shared design-system contract](docs/APPLET_DESIGN_SYSTEM_CONTRACT.md) while retaining justified mechanism-specific differences.
- Respect the [language coverage matrix](docs/PUBLIC_SURFACE_LOCALE_MATRIX.md), including dynamic text and state preservation.
- Keep Quick Assigns bounded and inquiry-led rather than duplicating the algorithm in a separate worksheet.
- Preserve keyboard access, visible focus, responsive containment, and text alternatives for essential state where practical.
- Keep learner responses out of analytics and share links.

## How changes reach the public site

This repository distributes finished website/download files and public documentation; implementation work and development history are maintained separately. Please discuss a proposed behavioral change in an issue before editing generated HTML. Documentation corrections can identify the exact public file and passage.

Maintainers review changes and run proportionate algorithm, browser, offline, localization, privacy, accessibility-engineering, and release checks before publishing finished artifacts. A green automated check does not demonstrate learning gains, adoption, or accessibility conformance. See [Quality](QUALITY.md).
