# AI Playgrounds

[![Verify](https://github.com/lmdixon23/ai-playgrounds/actions/workflows/verify.yml/badge.svg?branch=main&event=push)](https://github.com/lmdixon23/ai-playgrounds/actions/workflows/verify.yml)
[![Deploy](https://github.com/lmdixon23/ai-playgrounds/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/lmdixon23/ai-playgrounds/actions/workflows/deploy-pages.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Twelve bilingual, offline-ready interactives for foundational artificial intelligence. The suite covers search, logic, probability, machine learning, neural networks, computer vision, and reinforcement learning.

**Live site:** https://lmdixon23.github.io/ai-playgrounds/

**Current release:** [v1.0.0](https://github.com/lmdixon23/ai-playgrounds/releases/tag/v1.0.0)

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
