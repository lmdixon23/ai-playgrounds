# AI Playgrounds

<!-- launch-hardening-v1.0.1 -->
> **Start in five minutes:** open the live site, choose one applet, make a prediction, change one variable, and explain the trace. The suite contains 12 bilingual, offline-ready applets with 45 deterministic algorithm checks. [Live suite](https://lmdixon23.github.io/ai-playgrounds/) · [Educator guide](docs/EDUCATOR_ADOPTION_GUIDE.md) · [Release status](docs/RESEARCH_COMPANION_STATUS.md) · [Analytics and privacy](docs/ANALYTICS_AND_PRIVACY.md)

**Evidence boundary:** release checks establish bounded software behaviour and deployment integrity; they do not establish learning gains, classroom adoption, or accessibility conformance.


[![Verify](https://github.com/lmdixon23/ai-playgrounds/actions/workflows/verify.yml/badge.svg?branch=main&event=push)](https://github.com/lmdixon23/ai-playgrounds/actions/workflows/verify.yml)
[![Deploy](https://github.com/lmdixon23/ai-playgrounds/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/lmdixon23/ai-playgrounds/actions/workflows/deploy-pages.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21854217.svg)](https://doi.org/10.5281/zenodo.21854217)

Twelve bilingual, offline-ready interactives for foundational artificial intelligence. The suite covers search, logic, probability, machine learning, neural networks, computer vision, and reinforcement learning.

**Live site:** https://lmdixon23.github.io/ai-playgrounds/

**Current release:** [v1.0.1](https://github.com/lmdixon23/ai-playgrounds/releases/tag/v1.0.1)

**Archived release DOI:** [10.5281/zenodo.21854217](https://doi.org/10.5281/zenodo.21854217) · **All versions DOI:** [10.5281/zenodo.21854216](https://doi.org/10.5281/zenodo.21854216)

## Why this project exists

Foundational AI concepts are dynamic. A search frontier expands, evidence changes a posterior probability, a model begins to overfit, or value propagates through repeated experience.

AI Playgrounds turns those mechanisms into direct experiments that learners can manipulate before implementing them in code.

Each applet includes:

- one focused AI concept,
- complete English and Chinese learner and educator experiences,
- a featured experiment and scenario gallery,
- visual and text-based explanations,
- teacher notes and model limitations,
- a local student response packet,
- keyboard guidance,
- shareable experiment links that preserve exact current controls,
- offline operation in one HTML file.

## Explore

Open `index.html`, or open any file under `playgrounds/<slug>/index.html`.

No server, account, package manager, or build step is required.

## Verification

The repository uses three complementary verification layers:

```bash
python tools/release_check.py
python tools/run_algorithm_tests.py
python tools/browser_qa.py --no-screenshots
```

The algorithm gate requires all 45 regression cases to pass with no skipped cases. The browser matrix checks every public page at mobile, tablet, and desktop viewports. GitHub Actions runs all three layers on pushes and pull requests.

## Teaching materials

- [Teacher Pack](teacher-pack.html)
- [Curriculum Map](curriculum.html)
- [Student Lab Sheet](student-lab.html)
- [How the project works](quality.html)
- [Research and citation](research-and-citation.html)

## Research status

AI Playgrounds v1.0.1 is the released and archived software artifact. The GitHub Release and Zenodo DOI identify the software, its release evidence, and its reproducibility record.

A separate design-and-tools research manuscript about the suite is still in preparation. It is not part of the v1.0.1 GitHub Release or the Zenodo software deposit, and publication of the software should not be read as publication of that manuscript.

## Reuse and citation

The project is released under the MIT License.

- [Architecture](ARCHITECTURE.md)
- [Contributing](CONTRIBUTING.md)
- [Citation metadata](CITATION.cff)
- [Release notes](RELEASE_NOTES.md)
- [Localization standard](docs/LOCALIZATION.md)

Built by Logan M. Dixon

- [Portfolio](https://lmdixon23.github.io/)
- [ORCID](https://orcid.org/0009-0001-0592-462X)
- [GitHub repository](https://github.com/lmdixon23/ai-playgrounds)
- [Releases](https://github.com/lmdixon23/ai-playgrounds/releases)

## Contributing

Start with the [bounded contributor on-ramp](docs/CONTRIBUTOR_ONRAMP.md). Educator feedback, translation review, accessibility observations, deterministic edge cases, and small lesson activities are preferred over unscoped feature requests.
