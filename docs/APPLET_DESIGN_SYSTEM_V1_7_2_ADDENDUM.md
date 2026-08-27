# AI Playgrounds Applet Design System — v1.7.2 Parity Addendum

**Parent contract:** `docs/APPLET_DESIGN_SYSTEM_CONTRACT.md`
**Applies to:** all future public applets and any existing applet whose outer shell is materially revised.

This addendum records cross-generation rules discovered by comparing the mature original twelve applets against Labs 13–15. It does not require identical learning bodies.

## 1. Header action hierarchy

Unless a documented concept-specific exception is approved, the mature public header is:

- utility/preferences row:
  - Back to all playgrounds;
  - compact Theme control;
  - native language selector;
- primary row:
  - one public `h1`;
  - **Share**;
  - **More**;
  - **Reset**.

`More` contains secondary non-learning actions such as:

- Embed in LMS;
- Current settings (`.json`);
- concept-specific CSV/PNG exports when they are actually useful.

Do not place every secondary action directly in the primary row merely because the applet has space on desktop.

Reset labels must match their real boundary. A mechanism reset may preserve a local Quick Assign draft; it must not be labeled as clearing all learner work unless that behavior is implemented and tested.

## 2. Shared theme contract

All applets use the same persistent theme preference key:

```text
theme
```

Do not write applet-generation-specific keys such as `ai-playgrounds-theme`. A released legacy key may be read once as a migration fallback, copied into `theme`, and removed; that compatibility read is not a second active preference namespace.

When no explicit preference is saved, the shell should respect the system color-scheme preference where practical. Theme choice must not alter algorithm or learner-response state.

## 3. Share and Embed

Every public applet should expose Share and Embed unless there is a documented reason not to.

- **Share** may copy/share the canonical current applet URL. It must not claim to preserve dynamic state unless that state is actually serialized and restored.
- **Embed** should produce a bounded iframe URL using the suite embed convention (`?embed=1`). Embed mode hides suite-level navigation/support chrome while keeping the learning mechanism visible and operable.
- If an applet cannot safely support embedded use, fail closed and document the exception rather than producing a misleading iframe snippet.

## 4. Generic current-settings export

The mature shell provides a local JSON export of current control values where those values can be represented without exposing learner responses.

The generic export:

- contains applet/slug, export timestamp, and control values;
- excludes Quick Assign/student-response fields;
- remains local to the browser;
- is not a grading or analytics channel;
- does not imply the file can be imported unless an import path is explicitly implemented and tested.

Concept-specific CSV/PNG exports remain optional.

## 5. Skip-link contract

Each applet provides a keyboard-visible skip link that targets the beginning of the primary interactive mechanism. The target is programmatically focusable when needed.

## 6. Public orientation and support

The shared product vocabulary should be recognizable across generations:

- **The big idea** — one concise mechanism statement;
- **What to watch** — the causal/numerical relation the learner should inspect;
- **Key terms** — compact definitions for vocabulary needed to interpret the mechanism;
- **Text and keyboard support** — how non-pointer users inspect/control important state;
- **Model/fidelity boundary** — what the simplified applet does not establish or represent.

A lab may use its own stronger concept-specific explanation in place of duplicate prose, but the equivalent support must be discoverable.

## 7. Main-footer versus release provenance

The main footer uses the established suite identity and navigation:

- © 2026 Logan M. Dixon;
- established Portfolio URL;
- AI Playgrounds;
- Source;
- MIT;
- Report an issue;
- established ORCID.

Release/version provenance is secondary metadata, not a competing footer/navigation design. New applets must source identity/provenance from the established project values rather than inventing alternate portfolio or ORCID links.

## 8. Head/discovery metadata

Every public applet must expose the same minimum crawler/social contract:

- `<title>` carrying the applet name and `AI Playgrounds`;
- meta description;
- canonical URL;
- favicon;
- OpenGraph type, URL, title, description, and image;
- Twitter card, title, description, and image;
- alternate links for `en`, `zh-Hans`, `vi`, `es`, and `x-default`;
- JSON-LD declaring the applet as both `WebApplication` and `LearningResource`, with:
  - free access;
  - four learner locales;
  - MIT license;
  - high-school/undergraduate educational level;
  - AI Playgrounds parent site;
  - established project author/ORCID.

These fields should be generated from the final catalogue rather than hand-maintained separately per new lab whenever possible.

## 9. Product-shell parity is not body uniformity

The following remain concept-specific and must **not** be added simply to make counts match:

- a scenario gallery when a specialized scenario/challenge selector is clearer;
- a second learning-mode system when Guided Challenge + Quick Assign already covers the pedagogical states;
- a second response packet;
- CSV/PNG export without a meaningful tabular/visual artifact;
- decorative animations or gamification.

The burden is on a future integration PR to state whether each parent-contract capability is:

1. inherited directly;
2. supplied by a concept-specific equivalent; or
3. deliberately omitted with a tested rationale.

## 10. Release gate additions

A future new-lab integration should fail if the final public composition has any of the following:

- a separate theme namespace;
- missing skip target;
- missing Share/More/Reset hierarchy without an approved exception;
- missing canonical/social/structured metadata;
- missing canonical portfolio/ORCID provenance;
- more than one learner-response/Quick Assign surface;
- visible duplicate public titles;
- page-level horizontal overflow in required responsive classes;
- locale round trips that leave stale VI/ES/ZH title or shell text.

This addendum is an implementation/product-quality contract. It is not a claim of learning efficacy or accessibility conformance.
