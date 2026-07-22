# Architecture

AI Playgrounds deliberately uses a no-build, single-file applet architecture.

## Public surface

- `index.html` provides the live demonstration and searchable catalogue.
- `playgrounds/<slug>/index.html` contains one complete applet.
- Teacher, curriculum, student-lab, quality, and citation pages are plain HTML.

## Applet structure

Each applet contains:

1. the primary interactive model,
2. Explore, Understand, Use in class, and Text and keyboard modes,
3. bilingual interface strings,
4. local response-packet logic,
5. shareable URL state,
6. optional host-scoped analytics that remains silent for local files and forks.

No applet requires a framework, package manager, account, backend, or remote runtime asset.
## Applet color identity

`applets.json` is the source of truth for the twelve applet accent colors. Each applet receives one unique categorical accent, while the icon, title, category label, and sequence number remain the primary identifiers. Public card grids may use a soft accent tint, border, and label. Dense tables use only a row rail or numbered marker so color supports scanning without overwhelming the content.


## Learner-facing writing

Public applet copy follows [`CONTENT_STYLE_GUIDE.md`](CONTENT_STYLE_GUIDE.md), including canonical naming, abbreviation rules, scenario structure, bilingual parity, and toolbar hierarchy.
