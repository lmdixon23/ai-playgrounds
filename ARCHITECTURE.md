# Architecture

AI Playgrounds uses a no-build, single-file applet architecture.

## Public surfaces

- `index.html` provides the live demonstration and searchable catalogue.
- `playgrounds/<slug>/index.html` contains one complete applet.
- Teacher, curriculum, student, quality, and citation pages are plain HTML.
- `applets.json` provides shared public metadata for the twelve applets.

## Applet structure

Each applet contains:

1. the primary interactive model,
2. Explore, Understand, Use in class, and Text and keyboard modes,
3. English and Chinese interface strings,
4. local response-packet tools,
5. shareable URL state,
6. optional analytics restricted to the canonical hosted site.

No applet requires a framework, account, backend, package manager, model download, or remote runtime asset.

## Privacy and portability

Student responses remain in the browser unless the learner copies or prints them. The site has no student accounts, database, upload endpoint, or response-collection backend.

## Visual identity

Each applet has one categorical accent defined in `applets.json`. Color supports recognition but is never the only identifier. Applet names, icons, categories, and sequence numbers remain visible throughout the suite.

## Browser support

The public site is designed for current desktop and mobile browsers. Each applet can also be opened directly from the local filesystem.