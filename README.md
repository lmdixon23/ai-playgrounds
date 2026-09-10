# AI Playgrounds

> **Start in five minutes:** open the live site, choose one applet, make a prediction, change one variable, and explain the trace. [Live suite](https://lmdixon23.github.io/ai-playgrounds/) · [Teacher Pack](https://lmdixon23.github.io/ai-playgrounds/teacher-pack.html) · [Activity Packs](https://lmdixon23.github.io/ai-playgrounds/activities/) · [Analytics and privacy](docs/ANALYTICS_AND_PRIVACY.md)

[Public v1.9.4 release](https://github.com/lmdixon23/ai-playgrounds/releases/tag/v1.9.4)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Archived v1.0.1 DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21854217.svg)](https://doi.org/10.5281/zenodo.21854217)

AI Playgrounds is a suite of **15 multilingual, offline-ready applets** for inspecting artificial-intelligence mechanisms through controlled experiments rather than passive animations. The catalogue contains **13 Foundations/course-track labs** and **2 Modern AI extensions**, spanning search, logic, probability, machine learning, neural networks, computer vision, reinforcement learning, adversarial search, Transformer language modeling, and agent tool use.

Each learner applet runs without an account or backend. Learner-facing support is available in **English, Simplified Chinese, Vietnamese, and Spanish**. Educator and support surfaces declare their [narrower language boundaries](docs/PUBLIC_SURFACE_LOCALE_MATRIX.md) separately.

**Live site:** [Open AI Playgrounds](https://lmdixon23.github.io/ai-playgrounds/)

**Classroom downloads:** [Download any of the fifteen standalone HTML files or their ZIP](https://lmdixon23.github.io/ai-playgrounds/downloads.html). Each downloaded lab works independently, including its four learner languages and Quick Assign.

**Current release:** v1.9.4 keeps replay controls inside narrow and tablet layouts and contains long translated selectors. Pathfinding, Hill Climbing, Wumpus World, K-Means, Q-Learning, and Neural Network retain their mechanisms and keyboard replay behavior. Directory-link controls, CNF/SAT sharing, Labs 13–15 layout alignment, and Wumpus World's icon key and responsive percept icons are retained. See [release notes](RELEASE_NOTES.md) for changes and limitations.

**Archived v1.0.1 DOI:** [10.5281/zenodo.21854217](https://doi.org/10.5281/zenodo.21854217) · **All-versions DOI:** [10.5281/zenodo.21854216](https://doi.org/10.5281/zenodo.21854216). The archived DOI identifies v1.0.1, not v1.9.4.

### 15-second demo

[![AI Playgrounds demo showing the interactive suite in use](media/AI_Playgrounds_Demo_15s.gif)](https://lmdixon23.github.io/ai-playgrounds/media/AI_Playgrounds_Demo_15s.mp4)

**[▶ Open the full-resolution demo](https://lmdixon23.github.io/ai-playgrounds/media/AI_Playgrounds_Demo_15s.mp4)**

## How learners use the suite

Each applet focuses on one mechanism and follows the same inquiry pattern:

**predict → run or manipulate → observe → explain → transfer**

Shared product surfaces include:

- featured experiments and scenario-led comparison;
- visual and text-equivalent explanations;
- keyboard and accessibility guidance;
- shareable or reproducible state where the mechanism supports it;
- teacher prompts and explicit model limitations;
- local response capture that is not sent to AI Playgrounds analytics.

The [Curriculum Map](https://lmdixon23.github.io/ai-playgrounds/curriculum.html) and [curriculum guide](CURRICULUM.md) describe the course track and modern extensions. The suite is a collection of bounded experiments, not a complete course or a replacement for instruction.

## Teaching with AI Playgrounds

Every applet has one stable 10–15 minute **Quick Assign**. The complete registry includes QA-SEARCH-01 and the newer-lab activities QA-TRANSFORMER-01, QA-AGENT-01, and QA-MINIMAX-01. [Quick Assign architecture](docs/QUICK_ASSIGN_ARCHITECTURE.md) explains the assignment levels, classroom links, response handling, and teacher criteria.

Longer Level-2 Activity Pack pilots are available for:

- [NN-1 · Make it fail, then make it learn](https://lmdixon23.github.io/ai-playgrounds/activities/nn-1.html)
- [CNN-1 · Be the filter](https://lmdixon23.github.io/ai-playgrounds/activities/cnn-1.html)

Responses remain on the learner's device unless the learner or teacher deliberately copies, exports, prints, or submits them through their usual classroom system. AI Playgrounds has no assignment-submission backend, and teacher answer keys are intentionally not published on the student site.

Additional teaching materials:

- [Teacher Pack](https://lmdixon23.github.io/ai-playgrounds/teacher-pack.html) and [text guide](TEACHER_PACK.md)
- [Activity Packs](https://lmdixon23.github.io/ai-playgrounds/activities/)
- [Curriculum Map](https://lmdixon23.github.io/ai-playgrounds/curriculum.html)
- [Student Lab Sheet](https://lmdixon23.github.io/ai-playgrounds/student-lab.html) and [packet template](STUDENT_LAB_PACKET_TEMPLATE.md)
- [How the project works](https://lmdixon23.github.io/ai-playgrounds/quality.html)
- [Research and citation](https://lmdixon23.github.io/ai-playgrounds/research-and-citation.html)

## Standalone classroom downloads

1. [Download an individual HTML or the offline ZIP](https://lmdixon23.github.io/ai-playgrounds/downloads.html).
2. Extract the ZIP before opening a lab. A ZIP viewer or restricted LMS preview is not a browser substitute.
3. Copy or rename any individual HTML and give it to students. Open it in a modern desktop browser.

No installation, neighbouring files, server, account, or internet connection is required for the downloaded lab, its four learner languages, or its Quick Assign. Optional website, curriculum, and Activity Pack links still require internet access. The website versions may use neighbouring assets; use the **standalone downloads** when distributing one file.

Responses stay in the learner's browser, not inside the HTML file. Copy, export, or print answers before moving devices or clearing browser data. Copying the HTML does not copy saved answers. Distribute the HTML itself, not a device-local experiment URL.

## Website and verification

The public repository includes the finished website, independently usable classroom downloads, and documentation for learners, educators, and reusers. Development sources, build tools, tests, and development history are maintained separately. Finished HTML necessarily includes the browser-side code used by the playgrounds.

**No build is needed to use a downloaded lab.** Maintainers compose and verify the finished files before release; that preparation step is not a requirement for teachers or students. See [Architecture](ARCHITECTURE.md) and [Quality](QUALITY.md) for the delivery model and verification boundaries.

## Evidence boundary

Release checks establish bounded software behavior, deterministic composition, and deployment integrity under the tested conditions. They do not establish learning gains, classroom adoption, universal learner preference, superiority over other teaching methods, or accessibility conformance.

Human learner and educator usability studies and human screen-reader testing are deferred for this release. Automated checks are not a substitute for those studies. No WCAG conformance, validated learning gains, or educator adoption is claimed.

Historical releases and their original bytes remain unchanged. [Release history](https://lmdixon23.github.io/ai-playgrounds/release-notes.html) distinguishes earlier releases from the current distribution; an archived DOI is not a new version's DOI.

## Reuse and citation

The project is released under the [MIT License](LICENSE).

- [Architecture](ARCHITECTURE.md)
- [Applet design-system contract](docs/APPLET_DESIGN_SYSTEM_CONTRACT.md)
- [Quick Assign architecture](docs/QUICK_ASSIGN_ARCHITECTURE.md)
- [Public surface locale matrix](docs/PUBLIC_SURFACE_LOCALE_MATRIX.md)
- [Localization standard](docs/LOCALIZATION.md)
- [Analytics and privacy](docs/ANALYTICS_AND_PRIVACY.md)
- [Contributing](CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [Citation metadata](CITATION.cff)
- [Releases](https://github.com/lmdixon23/ai-playgrounds/releases)

Built by Logan M. Dixon · [Portfolio](https://lmdixon23.github.io/) · [ORCID](https://orcid.org/0009-0001-0592-462X)
