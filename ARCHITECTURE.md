# Architecture

AI Playgrounds is a suite of browser-based AI experiments: **15 applets, 13 Foundations/course-track labs, and 2 Modern AI extensions**. The public repository contains the finished website, classroom downloads, and reader-facing documentation. Development sources, tools, tests, and their history are maintained separately.

## Delivery and offline use

- The [live website](https://lmdixon23.github.io/ai-playgrounds/) serves static HTML, CSS, JavaScript, and media. Website pages may use neighbouring assets.
- The [standalone downloads](https://lmdixon23.github.io/ai-playgrounds/downloads.html) each contain a complete lab, its four learner languages, and its Quick Assign. An individual HTML can be copied, renamed, and opened offline without neighbouring files.
- Maintainers prepare the finished files before release. Teachers and students do not need a build tool, package manager, server, account, backend, or model API.
- Optional links to the website and external sources require internet access. Browser-side code is necessarily included in finished HTML.

## Public surfaces

| Surface | Purpose |
|---|---|
| [Catalogue](https://lmdixon23.github.io/ai-playgrounds/) | Find a mechanism through search, filters, or the course track |
| [Teacher Pack](https://lmdixon23.github.io/ai-playgrounds/teacher-pack.html) | Plan a short assignment and find teacher look-for criteria |
| [Curriculum Map](https://lmdixon23.github.io/ai-playgrounds/curriculum.html) | Connect the labs to topics and prerequisites |
| [Activity Packs](https://lmdixon23.github.io/ai-playgrounds/activities/) | Longer student-facing experiment sequences |
| [Student Lab Sheet](https://lmdixon23.github.io/ai-playgrounds/student-lab.html) | Structure predictions, evidence, explanations, and transfer |
| [Downloads](https://lmdixon23.github.io/ai-playgrounds/downloads.html) | Distribute independently usable classroom HTML |
| [Quality](QUALITY.md) and [citation](https://lmdixon23.github.io/ai-playgrounds/research-and-citation.html) | Understand evidence, limitations, and reuse |

## Shared learner architecture

Each lab centers on **predict → run or manipulate → observe → explain → transfer**. Shared components include navigation, theme and language controls, experiment actions, Explore and Guided Challenge modes, featured/scenario comparisons, explanations, teacher notes, and classroom response surfaces.

Shared product surfaces should be consistent across all fifteen labs. The mechanism may require a different visualization: a grid, scatterplot, matrix, tree, or ordered tool-call trace. That difference does not justify unrelated page navigation or classroom controls. See the [design-system contract](docs/APPLET_DESIGN_SYSTEM_CONTRACT.md).

## Assignments, language, and state

All fifteen labs have one stable Level-1 Quick Assign. NN-1 and CNN-1 add longer Level-2 activities; no Level-3 unit pack is currently offered. See [Quick Assign architecture](docs/QUICK_ASSIGN_ARCHITECTURE.md).

Learner applets and Quick Assigns support English, Simplified Chinese, Vietnamese, and Spanish. Support pages and Activity Packs have narrower [language boundaries](docs/PUBLIC_SURFACE_LOCALE_MATRIX.md).

Experiment state and learner responses are distinct. A share link can encode a supported experiment configuration; it must not contain worksheet answers. Responses remain in the learner's browser unless deliberately copied, exported, printed, or submitted through a separate classroom system. Copying HTML does not move saved answers. See [privacy](docs/ANALYTICS_AND_PRIVACY.md).

## Verification boundary

Maintainer checks cover algorithms, state transitions, localization, accessibility engineering, responsive layouts, visual regression, privacy, offline delivery, and artifact integrity under tested conditions. These checks do not establish human usability, learning gains, educator adoption, or WCAG conformance. See [Quality](QUALITY.md) and [release notes](RELEASE_NOTES.md).
