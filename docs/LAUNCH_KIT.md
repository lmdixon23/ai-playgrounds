# AI Playgrounds launch kit

## Canonical one-sentence description

AI Playgrounds is an open suite of **15 multilingual, offline-ready interactive AI labs** that makes mechanisms across search, logic, probability, machine learning, vision, reinforcement learning, game trees, Transformers, and agent systems manipulable and inspectable for teaching.

## Current proof points

- 15 public learner applets: 13 Foundations/course-track labs plus 2 Modern AI extensions.
- English, Simplified Chinese, Vietnamese, and Spanish learner-app support.
- One stable 10–15 minute Level-1 Quick Assign for every applet.
- Two longer Level-2 Activity Pack canaries: `NN-1` and `CNN-1`.
- No learner account, project backend, or installation required for ordinary use.
- Deterministic algorithm, localization/state, HCI, responsive, browser, and exact-release checks in the repository.
- Teacher materials, curriculum mapping, misconception/fidelity notes, privacy-bounded analytics, and reproducible release evidence.
- MIT license and scholarly citation metadata.

The software checks establish bounded artifact behavior under tested conditions. They do **not** establish learning gains, adoption, accessibility conformance, or superiority to another teaching method.

## Show HN title

**Show HN: AI Playgrounds – 15 multilingual, offline-ready interactive AI labs**

## Show HN body

I built AI Playgrounds because many AI visualizations are either polished black boxes or isolated demonstrations that are difficult to turn into classroom work. The current suite has 15 browser-based labs spanning classical AI mechanisms and selected modern extensions: search, local search, logical agents, SAT, Bayesian reasoning, classification, model generalization, neural networks, clustering, convolution, reinforcement learning, game trees, Transformer language modeling, and agent tool use.

The design constraint is mechanism-first: each lab exposes the state needed to explain the concept, names material simplifications, and avoids adding spectacle when it does not reveal the mechanism. The learner applets support English, Simplified Chinese, Vietnamese, and Spanish. Every applet has a 10–15 minute Quick Assign, and two labs also have longer Activity Pack canaries.

The public suite is designed for no-account, offline-ready use and is built/released deterministically. The verification suite covers algorithm behavior, localization/state preservation, responsive/HCI cases, and browser integration. Those checks establish software behavior for tested cases; they do not prove learning effectiveness or accessibility conformance.

I would especially value feedback on three questions: whether the visual state is sufficient to explain each mechanism, whether the offline/self-contained constraint is worth the implementation duplication, and which lab or teacher resource would most improve adoption next.

## LinkedIn educator post

I have released **AI Playgrounds v1.7**, an MIT-licensed suite of 15 multilingual interactive AI labs for classroom and independent exploration. The suite spans foundational topics such as search, logic, probability, machine learning, vision, reinforcement learning, and game trees, plus modern extensions on Transformer language modeling and agent tool use.

Every lab now has a stable 10–15 minute Quick Assign built around prediction, manipulation, observation, explanation, and transfer. Tiny Neural Network and Convolution also have longer Activity Pack canaries. The learner applets support English, Simplified Chinese, Vietnamese, and Spanish, and no account or project backend is required.

The software is accompanied by deterministic algorithm, localization/state, HCI, responsive, and browser checks. Those checks establish bounded software behavior—not measured learning gains—so classroom usability and adoption remain separate evidence questions.

## Engineering-focused post

AI Playgrounds is a deliberately constrained educational software system: 15 self-contained/offline-ready interactive applications, deterministic public-site construction, four-language learner surfaces, stable Quick Assign IDs, browser/HCI QA, explicit fidelity limits, and exact release provenance. The design question is not how many features fit in a demo, but how much algorithmic state can remain inspectable while the artifact still works in a school browser without a project backend.

## Résumé bullets

- Designed and released AI Playgrounds, an MIT-licensed suite of 15 multilingual interactive AI labs with all-lab Quick Assigns, responsive/HCI browser QA, teacher resources, curriculum mapping, and reproducible GitHub Pages deployment.
- Built an offline-ready educational AI visualization system spanning classical and selected modern AI mechanisms, with explicit model-fidelity limits, privacy-bounded uptake measurement, deterministic verification, and scholarly release provenance.

## Alt text for social preview

AI Playgrounds landing page showing a searchable grid of fifteen interactive AI learning labs, with multilingual learner support and teacher Quick Assign resources.

## Claim discipline

When adapting this kit, keep the public-surface locale boundary accurate:

- all 15 learner applets and all 15 Level-1 Quick Assigns: EN/ZH/VI/ES;
- some educator/support pages: narrower language scope;
- current Level-2 Activity Pack canaries: English-only.

Do not convert software verification, multilingual interfaces, or aggregate traffic into claims of learning effectiveness, accessibility conformance, equity, or classroom adoption.
