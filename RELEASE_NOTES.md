# AI Playgrounds v1.9.6

## Changes

- Corrected regularization objectives, resolution steps, distance geometry, clustering and discounting explanations, including their language variants.
- Quick Assign prompts now agree across languages and with the teacher objectives. NN-1 and its teacher guidance specify original x-y inputs and use the current validation-control name.
- Enlarged text reflows in result cards, model controls, probability tables and long headings. KNN shows the controls for the selected classification or regression task.
- Original-lab dark themes use more readable text for scenario headings, assignment labels, essay headings and navigation links. Long translated text and lesson-tour controls wrap at enlarged text sizes.
- All fifteen labs display the current release version.

- Settings downloads preserve explicit off values and exclude challenge answers and language preferences. Native formulas and prompts remain settings.
- More disclosures, export completion, classroom clear and learning tabs now provide consistent keyboard recovery across all fifteen labs.
- Minimax challenges accept equivalent numeric predictions and hold the stated tree and trace until reveal; comparison controls no longer expose the answer prematurely.
- Classroom saves preserve different answer fields and captures from another tab, retain unsaved edits after storage failure, and report unreadable drafts. One tab per lab is recommended; the latest save wins when tabs edit the same answer.
- NN-1 and CNN-1 no longer report failed saves as successful or erase visible answers when clearing fails. Long responses flow through printed/PDF pages, including from dark theme.

- Classroom drafts now preserve answers and the explicitly captured evidence through reloads. Clearing nonempty work asks for confirmation; storage failures are reported. Copying, printing and language changes preserve learner writing and the chosen capture until the learner refreshes it.
- Shared experiment links exclude classroom answers and retain supported custom controls and language through reloads. Native formulas remain shareable.
- Pathfinding, KNN and reinforcement-learning summaries now report the relevant native results. Regression inspection remains available when moving from the plot to capture evidence.
- First-visit Monte Carlo uses the earliest visit of each state/action pair. Training reset clears its related model, counters and history together; replay pauses training and restores a consistent checkpoint when returning to live work.
- Bayesian-network exact inference now works with the Burglary, Sprinkler and Cancer presets; reset aligns the selected preset and inference method with the displayed result.
- Activity Pack footers distinguish the original v1.5.1 introduction from the current site version.

- Student and teacher materials now accept evidence that supports or challenges a prediction. The homework sequence places prediction before action, and explanations are judged by their connection to the mechanism rather than a vocabulary-word quota. English/Chinese printable packets and current English editable guides follow the same sequence.

- Starting the featured experiment now moves both the viewport and keyboard focus to a visible native experiment control in all fifteen labs. Keyboard users continue from that control with Tab. Reduced-motion preferences are honored.
- Space activates the featured button instead of being intercepted by a lab-wide play shortcut. The existing scenario settings and teaching prompts are preserved; applying a scenario is not presented as completing or mastering it.
- Focus remains undisturbed when restoring a shared experiment or switching languages. Checks cover all fifteen labs, four languages, phone and desktop sizes, both website entry forms, and renamed offline files, including classroom-answer preservation.
- Vietnamese and Spanish now translate the return-to-latest button and jump-input accessible names in all six replay-enabled labs. K-Means also gains the missing translated replay-slider name. Iteration, frame, step, episode, and epoch meanings remain distinct.
- Native regression checks verify actual labels through directory URLs, explicit HTML links, and renamed offline files, including language round trips, retained history, keyboard return, and another native action. Each newly added mapping is independently removed in a negative test to prove detection.
- Replay controls wrap within Pathfinding, Hill Climbing, Wumpus World, K-Means, and Q-Learning panels when space is limited. Neural Network retains its existing responsive replay layout.
- Selectors in Hill Climbing, Neural Network, Pathfinding, and Wumpus World stay within their panels, including long translated options. These CSS-only changes preserve algorithms, history, saved classroom responses, and all four learner languages.
- All six replay-enabled labs are checked at fifteen phone, tablet, breakpoint-neighbour, and desktop sizes in four languages, before and after creating history, including keyboard review and return to the latest frame.
- The original twelve labs retain language selection, Guided Challenge, and the correct featured experiment at directory URLs and explicit HTML links. All fifteen standalone downloads remain independently usable.
- CNF/SAT shared formulas and parser diagnostics still survive startup. Explicit scenario links retain precedence; saved experiment controls apply afterwards.
- Labs 13–15 retain their v1.9.1 shared page-layout alignment. Wumpus World retains its icon key and cell-scaled breeze and stench icons; gold remains unchanged.

The public repository contains finished website/download artifacts and public documentation, not development sources or development history. The earlier releases and their original bytes remain unchanged.

## Offline classroom use

[Download a standalone HTML or the ZIP](https://lmdixon23.github.io/ai-playgrounds/downloads.html). Extract the ZIP, then copy or rename any individual HTML and open it in a modern desktop browser. No account, server, installation, neighbouring files, or internet connection is needed for the lab, its four learner languages, or its Quick Assign. Website links remain optional online destinations.

Answers remain in the learner's browser unless deliberately copied, exported, printed, or submitted through the teacher's usual classroom system. Copying an HTML file does not copy saved answers.

## Validation limitation

The broader manual file and lab review is unfinished and will continue after this release. This release is not represented as a completed exhaustive audit.

Human learner and educator usability studies and human screen-reader testing remain deferred. Automated checks are not substitutes for these studies. No WCAG conformance, validated learning gains, or educator adoption is claimed.

New and revised translations are engineering-reviewed proposals, not a fluent-reader naturalness review. The classroom prompt correction covers English and Chinese support pages; lab mechanisms and four-language behavior remain unchanged by that correction.

The archived v1.0.1 DOI is not a DOI for v1.9.6. See [citation information](https://lmdixon23.github.io/ai-playgrounds/research-and-citation.html) and the [changelog](https://github.com/lmdixon23/ai-playgrounds/blob/v1.9.6/CHANGELOG.md).
