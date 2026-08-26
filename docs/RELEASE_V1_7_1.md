# AI Playgrounds v1.7.1

**Release date:** 2026-08-27

v1.7.1 is a product-consistency, accessibility-oriented interaction, discoverability, and assignment-parity patch over v1.7.0. It does **not** add a sixteenth lab or change the mathematical/algorithmic behavior of the Transformer, agent-runtime, Minimax/Alpha-Beta, or inherited applets.

## Modern-lab parity

Labs 13–15 now inherit the mature suite-level affordances already established across the original twelve where those affordances are concept-independent:

- skip-to-interactive-mechanism link;
- mature shared header hierarchy;
- **Share · More · Reset all** action order;
- Theme beside language in the preference row using the shared `theme` preference namespace;
- **More** menu with Embed and local current-settings JSON export;
- concise **The big idea / What to watch** orientation;
- localized key-terms and model-fidelity support;
- richer canonical suite provenance/footer;
- `?embed=1` mode;
- complete favicon, OpenGraph, Twitter, `hreflang`, and JSON-LD `WebApplication`/`LearningResource` metadata;
- responsive containment and four-locale round-trip coverage.

Concept-specific learning bodies remain concept-specific. v1.7.1 deliberately does **not** duplicate the original applets' Explore/Guided/Classroom tab shell or scenario gallery where Labs 13–15 already provide equivalent Guided Challenge, scenario-selector, and Quick Assign flows.

## Quick Assign parity for Labs 13–15

The modern Quick Assigns retain their v1.7.0 stable IDs and local-only response storage while gaining the mature packet affordances used by the original suite:

- a live **State snapshot** sourced from each lab's existing text-equivalent mechanism state;
- **Refresh state**;
- packet copy containing state plus Predict / Observe / Explain / Transfer responses;
- packet-only print rather than whole-page print;
- EN/ZH/VI/ES action labels and textarea accessible names;
- response preservation across supported locale changes.

No new assignment architecture or backend was introduced.

## Structured accessibility-oriented support

Labs 13–15 now expose an open, structured accessibility support layer aligned with the original twelve:

- **Keyboard path** guidance;
- **Text state summary** mirroring each modern lab's existing `stateText` / `textState` representation;
- **Reduced motion and non-visual support** guidance;
- explicit evidence-boundary language.

This is an engineering and interaction-parity claim under tested conditions. It is **not** a claim of WCAG conformance or universal assistive-technology compatibility.

## Assurance and design-system governance

The release adds a permanent modern-lab parity audit and v1.7.1 design-system addendum. Final-composition QA verifies shared chrome, provenance, metadata, locale reversibility, Quick Assign state/labels, embed behavior, responsive containment, and the structured accessibility layer while preserving all inherited algorithm and browser gates.

The parity work also retained control-induced failures as regression lessons: validators must count real DOM surfaces rather than JavaScript string references, release wrappers must be appended at the actual document boundary rather than the first textual `</body>` inside embedded strings, and new chrome must reuse established project provenance rather than inventing replacements.

## Unchanged product boundary

- **15 public applets**
- **13 Foundations/course-track labs + 2 Modern AI extensions**
- **15 active Level 1 Quick Assigns**
- **2 Level 2 Activity Pack canaries**
- learner-facing **EN / ZH / VI / ES** support
- no account or project backend required for core applet use
- learner answers, Quick Assign responses, experiment values, and free text remain excluded from AI Playgrounds analytics

## Evidence boundary

The release checks establish deterministic software behavior, product-shell consistency, localization behavior, bounded browser/responsive behavior, and deployment integrity for the tested conditions. They do **not** establish learning gains, classroom adoption, learner preference, equitable outcomes, or accessibility conformance.
