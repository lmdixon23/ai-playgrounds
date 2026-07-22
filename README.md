# AI Playgrounds

Twelve bilingual, offline-ready interactives for foundational artificial intelligence. The suite covers search, logic, probability, machine learning, neural networks, computer vision, and reinforcement learning.

**Live site:** https://lmdixon23.github.io/ai-playgrounds/

## Why this project exists

Foundational AI concepts are dynamic: a frontier expands, evidence changes a posterior, a model begins to overfit, or value propagates through repeated experience. AI Playgrounds turns those mechanisms into direct experiments that students can manipulate before they implement them.

Each applet combines:

- one focused concept,
- English and Chinese interfaces,
- a featured experiment and scenario gallery,
- a visual mechanism explanation,
- teacher notes and fidelity limits,
- a local student response packet,
- keyboard guidance and text-state output,
- exact experiment links,
- one-file offline operation.

## Start

Open `index.html`, or open any `playgrounds/<slug>/index.html` directly. No server, account, package manager, or build step is required.

## Quality checks

```bash
python tools/release_check.py
python tools/browser_qa.py --no-screenshots
```

The public algorithmic test report is available at `tests/index.html`. Browser QA evidence is generated locally under `release-evidence/`.

## Teaching materials

- [Printable Teacher Pack](teacher-pack.html)
- [Curriculum map](curriculum.html)
- [Student lab sheet](student-lab.html)
- [How the project works](quality.html)
- [Research and citation](research-and-citation.html)

## Reuse

The project is released under the MIT License. See [CONTRIBUTING.md](CONTRIBUTING.md), [ARCHITECTURE.md](ARCHITECTURE.md), and [CITATION.cff](CITATION.cff).

Built by Logan M. Dixon · [ORCID](https://orcid.org/0009-0001-0592-462X)

## Use, adapt, or support the project

Use the applets in class, adapt them under the MIT License, or help other educators find the project by starring the repository or following releases.

- [Logan M. Dixon portfolio](https://lmdixon23.github.io/)
- [Star or fork the repository](https://github.com/lmdixon23/ai-playgrounds)
- [Follow releases](https://github.com/lmdixon23/ai-playgrounds/releases)


## Learner-facing writing

Public applet copy follows [`CONTENT_STYLE_GUIDE.md`](CONTENT_STYLE_GUIDE.md), including canonical naming, abbreviation rules, scenario structure, bilingual parity, and toolbar hierarchy.
