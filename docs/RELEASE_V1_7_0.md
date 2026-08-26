# AI Playgrounds v1.7.0

**Release date:** 2026-08-26

v1.7.0 completes the Level 1 teacher-assignment layer across the existing fifteen-lab curriculum. It adds no sixteenth lab and changes no underlying AI algorithm.

## Quick Assigns for every public lab

- Activates one stable Quick Assign ID for all 15 applets.
- Keeps the first four v1.6.1 assignments and adds Bayes Rule, Bayesian Networks, KNN, Overfitting, Tiny Neural Network, K-Means, Convolution, Q-Learning, Minimax/Alpha-Beta, Transformer Language Modeling, and Agent Tool Use.
- Each activity is scoped to about 10-15 minutes and follows `predict -> run/manipulate -> observe -> explain -> transfer`.
- Teacher Pack and Curriculum pages expose all 15 canonical `Use in class` links.
- The original twelve labs reuse their established classroom response packets. Labs 13-15 use a local-only Quick Assign response layer aligned to their existing Guided Challenges.
- Learner response text stays in the browser unless deliberately copied or printed. Quick Assign responses are excluded from analytics requests.
- The v1.6.1 `quick_assigns_v1.json` registry remains unchanged for historical reproducibility; v1.7.0 uses `quick_assigns_v2.json` with all fifteen activities active.

## Modern-lab and mobile hardening discovered by the all-lab gate

- Canonical Quick Assign deep links for Labs 13-15 now open the targeted response surface immediately.
- Replaces a malformed generated JavaScript response-packet runtime with a deterministic local-only runtime and preserves JavaScript newline escapes byte-for-byte.
- Preserves EN/ZH/VI/ES Quick Assign presentation while retaining learner response text across locale switches.
- Constrains the Lab 15 Guided Challenge selector at narrow mobile widths while keeping the wide game tree inside its intended internal scroller.
- Removes the Activity Pack pilot footer's hard-coded current-suite version so the pilot cannot drift out of sync with future releases.

## Verification

The release inherits the complete algorithm, localization, Guided Challenge, engagement, HCI, responsive, provenance, and release-quality stack from v1.6.2 and adds a dedicated all-lab Quick Assign gate plus a final v1.7 public-release gate.

The behavioral candidate is required to verify:

- all 15 unique Quick Assign IDs are active;
- all 15 applets expose exactly one assignment surface;
- Teacher Pack and Curriculum list all 15 canonical classroom links;
- the eleven newly activated activities are browser-tested;
- modern-lab direct links open their response surface;
- modern responses survive EN/ZH/VI/ES switching;
- original-lab packet labels survive VI/ES -> EN round trips;
- Labs 13-15 remain contained at 390 px under the tested conditions;
- no page or console errors occur in the all-lab Quick Assign harness.

## Evidence boundary

Software/browser assurance establishes implementation behavior under tested conditions. It does **not** establish learning gains, classroom adoption, learner preference, or accessibility conformance.

The immutable v1.0.1 DOI `10.5281/zenodo.21854217` remains historical provenance and is not reassigned to v1.7.0.
