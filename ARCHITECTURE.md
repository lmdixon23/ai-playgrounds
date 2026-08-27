# Architecture

AI Playgrounds uses a no-build public-site architecture with self-contained/offline-ready applets and deterministic release composition.

## Public surfaces

- `index.html` provides the live demonstration and searchable catalogue.
- `playgrounds/<slug>/index.html` contains one complete public applet after deterministic composition.
- Teacher, curriculum, student, quality, citation, and activity pages are plain HTML.
- `applets.json` provides shared public metadata for all fifteen applets.
- `docs/APPLET_DESIGN_SYSTEM_CONTRACT.md` defines the minimum shell, metadata, localization, assignment, accessibility/HCI, responsive, privacy, and release requirements for new labs.

## Applet families

The public catalogue contains **13 Foundations/course-track labs** and **2 Modern AI extensions**.

The original twelve applets share the established learning-mode architecture, including Explore, Understand, Use in class, and Text and keyboard surfaces plus local response-packet tooling.

Labs 13–15 have concept-specific interactive bodies because Transformer internals, agent-runtime gates, and game trees require different visual organizations. They nevertheless inherit the same public product and learning contract: suite navigation, standardized outer shell/provenance, concise catalogue metadata, one featured experiment, five predict–run–explain scenarios, terminology primer, step-by-step explanation, teacher prompts, four-language learner support, bounded assignment surface, accessibility-oriented behavior, responsive containment, and exact release verification.

Consistency applies both to what learners should not have to relearn and to the depth of instructional support. A mechanism-specific layout may differ when uniformity would distort the concept; it may not use that difference to omit the scenario-led teaching sequence.

## Shared learner contract

Every released applet provides:

1. one primary interactive mechanism;
2. a meaningful initial or scenario state;
3. visible state sufficient to explain the mechanism;
4. prediction-before-reveal when a prediction is pedagogically meaningful;
5. misconception/fidelity guidance;
6. a reset/recovery path;
7. text/keyboard access to concept-defining state where feasible;
8. one stable Level-1 Quick Assign;
9. optional analytics restricted to the canonical hosted site and excluding learner-authored responses.

Each applet also supplies a featured experiment, a small scenario sequence with explicit prediction and explanation prompts, prerequisite terms, a mechanism explanation, and teacher-facing prompts. The controls and visualization may remain concept-specific; the learning depth may not silently collapse into a selector plus a few labels.

The original twelve reuse their established Student response packets for Quick Assigns. Labs 13–15 use thin local-only response surfaces aligned to their Guided Challenges. All Quick Assigns use the inquiry spine:

`predict -> manipulate/run -> observe -> explain -> transfer`

## Localization boundary

All fifteen **learner applets** and their fifteen Level-1 Quick Assigns support:

- English;
- Simplified Chinese;
- Vietnamese;
- Spanish.

Locale switching must preserve learner/algorithm state and restore the canonical English title/state on EN round-trip tests.

This does **not** mean every educator/support surface is four-language. Teacher Pack, Curriculum, research and support pages, and Level-2 Activity Packs have separately declared boundaries in `docs/PUBLIC_SURFACE_LOCALE_MATRIX.md`.

Stable machine/source literals such as URLs, filenames, identifiers, formulas, licenses, names, and standard acronyms remain unchanged while their visible labels/explanations are localized where applicable. See `docs/LOCALIZATION.md`.

## Privacy and portability

Student responses remain in the browser unless the learner deliberately copies or prints them. The site has no student accounts, response database, upload endpoint, or assignment-submission backend.

No applet requires an account, project backend, package manager, or remote runtime service. Labs 13–15 are generated deterministically into self-contained public HTML artifacts. Any future exception to the offline/self-contained boundary must be explicit in the applet design contract and public documentation.

## Visual identity

Each applet has one categorical accent defined in public metadata. Color supports recognition but is never the only identifier. The shared outer shell provides suite identity, navigation, language/theme/reset controls where applicable, and release provenance; the mechanism body is allowed to specialize.

## Browser and HCI support

The release QA covers desktop, classroom/projector, tablet, split/narrow desktop, phone portrait, phone landscape, reduced motion, and targeted text-enlargement/recovery cases. These checks establish bounded software behavior under tested conditions, not accessibility conformance or learner effectiveness.
