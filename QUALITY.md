# How the project works

AI Playgrounds is designed around portable classroom use, inspectable software, and clear evidence limits.

## Built into the project

- Fifteen multilingual, offline-ready learner applets
- Thirteen Foundations/course-track labs plus two Modern AI extensions
- One focused mechanism per applet
- One stable Level-1 Quick Assign per applet
- Two longer Level-2 Activity Pack canaries for Tiny Neural Network and Convolution
- Featured experiments, scenarios, or equivalent bounded comparisons
- Visual mechanism explanations and synchronized text-state support where appropriate
- Teacher misconception and fidelity notes
- Local student response surfaces; response text is not sent to AI Playgrounds analytics
- Keyboard guidance, visible focus, reduced-motion handling, and non-color-only state cues where applicable
- Algorithmic regression tests
- EN/ZH/VI/ES learner-interface and state-preservation checks
- Automated browser checks across desktop, projector, tablet, split-screen, phone portrait, and phone landscape classes
- Targeted HCI checks for text enlargement, touch recovery, localized component fit, and learner-state recovery
- Deterministic public-site construction and exact release/provenance checks

## Assignment layers

**Level 1 Quick Assigns** are approximately 10–15 minutes and use the shared inquiry spine:

`predict -> manipulate/run -> observe -> explain -> transfer`

All fifteen public applets have one stable Quick Assign ID and classroom link.

**Level 2 Activity Packs** are longer inquiry sequences. The current public canaries are `NN-1` and `CNN-1`.

Level 3 lesson/unit packages remain a future option and are not implied to exist across the suite.

## Localization boundary

All 15 learner applets and all 15 Level-1 Quick Assigns support English, Simplified Chinese, Vietnamese, and Spanish under the tested release paths. Some educator/support surfaces and the current Level-2 Activity Packs have narrower language boundaries; see `docs/PUBLIC_SURFACE_LOCALE_MATRIX.md`.

Four-language learner support is an interface/design property. It is not evidence of equitable access or learning impact.

## Privacy

The site has no student accounts, backend, database, or student-upload endpoint. Response text in built-in packets, Quick Assigns, and Activity Packs stays in the learner's browser until the learner copies, prints, or clears it.

The canonical GitHub Pages site uses privacy-minimized aggregate GoatCounter requests. The project sends canonical page/event identifiers and allow-listed campaign attribution but no learner answers, experiment values, query-state payloads, names, grades, or general referrer URLs. Global Privacy Control, Do Not Track, `?analytics=off`, local opt-out, offline copies, localhost, and non-canonical mirrors disable project analytics.

## Interaction assurance

Shared and high-risk interactions are evaluated as state transitions rather than control-presence checks alone:

`initial state -> learner action -> expected state -> recovery path -> focus/accessibility/state consistency`

This supplements, rather than replaces, concept-specific interaction design. The applet design-system contract defines the minimum shared product shell while allowing concept-specific bodies where uniformity would distort the mechanism.

## Evidence limits

The software checks establish properties of the artifact under tested conditions. They do not establish learning gains, classroom adoption, universal learner preference, accessibility conformance, or educational impact. Those questions require separate human and learner evidence.
