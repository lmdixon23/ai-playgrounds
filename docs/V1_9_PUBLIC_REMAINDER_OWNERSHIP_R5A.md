# AI Playgrounds v1.9 R5a — Public remainder source ownership

## Status

R5a is a behavior-preserving architecture milestone inside issue #47.

It establishes explicit canonical source ownership for every public file outside the 15 applet-page graph while leaving the historical v1.8.1 build ladder in place temporarily as an independent current-build equivalence witness.

R5a changes source authority, not learner-visible output.

## Starting point

R4b already provided canonical current ownership for all 15 applet pages through:

- 15 lab page templates;
- 17 shared components;
- 11 raw shared components;
- 6 DTCG token-template components;
- 21 token-template bindings;
- exact reconstruction of the frozen v1.8.1 applet pages.

The remaining architecture question was the other 43 files in the 58-file public deployment.

## Public remainder boundary

`src/product/public-remainder.json` now owns exactly those 43 non-applet public paths.

The accepted ownership split is:

- 29 files: `canonical-existing`
- 14 files: `current-snapshot`
- 43 non-applet files total
- 15 canonical applet pages
- 58 public files total

Byte ownership is:

- 3,036,276 bytes from existing canonical repository sources;
- 603,323 bytes from exact current snapshots;
- 3,639,599 bytes across the complete non-applet remainder.

## Existing canonical sources

R5a reuses an existing repository source only when its bytes are identical to the frozen public artifact.

This group includes, among other files:

- `.nojekyll`;
- project metadata and documentation copied into the public release;
- `src/product/catalogue.json` as the canonical owner of public `applets.json`;
- guided-challenge assets;
- the existing localization CSS and per-lab locale payloads;
- media assets;
- `og-image.png`;
- `robots.txt`.

No path is accepted into this group by filename convention alone. The permanent validator requires exact SHA-256 and byte-count equality with the frozen public oracle.

## Exact current snapshots

Fourteen outputs had no byte-identical current repository source because they are composed or transformed by the historical release ladder.

R5a materializes their exact accepted bytes under `src/site/current/`:

1. `404.html`
2. `activities/cnn-1.html`
3. `activities/index.html`
4. `activities/nn-1.html`
5. `assets/localization-r4.js`
6. `curriculum.html`
7. `index.html`
8. `quality.html`
9. `release-notes.html`
10. `research-and-citation.html`
11. `sitemap.xml`
12. `student-lab.html`
13. `teacher-pack.html`
14. `tests/index.html`

These snapshots are an **ownership bridge**, not the final support-page architecture.

They establish a trustworthy current source boundary so the version-layered current builder can be removed in R5b. Later support-page and registry work should decompose these snapshots into shared current primitives where that improves maintainability without conflating decomposition with the ladder-removal gate.

## Permanent ownership validator

`tools/public_remainder.py` requires:

- schema version 1;
- phase `v1.9-r5a-public-remainder-ownership`;
- exact complement of the 15 canonical applet-page paths;
- exactly 43 public remainder paths;
- exactly 29 existing canonical sources;
- exactly 14 current snapshots;
- the exact 14-path snapshot set listed above;
- unique public paths and source paths;
- exact SHA-256 and byte counts for every declared source;
- exact agreement with `src/product/public-artifact-sha256.json`;
- exact ownership byte metrics.

A snapshot may only live at `src/site/current/<public-path>`. An existing source may not point into that snapshot root.

## Product-level phase ownership

R5a introduces an important phase distinction.

The top-level product/build architecture advances to:

`v1.9-r5a-public-remainder-ownership`

The already-accepted page and design-binding subgraphs remain explicitly R4b-owned:

`v1.9-r4b-token-owned-components`

Advancing a parent architecture phase must not silently relabel independently versioned subgraphs. The current build validates those boundaries separately.

## Current build behavior

`tools/build_current.py` now validates the complete 43-file ownership map before invoking the historical v1.8.1 builder.

The historical builder is still present during R5a only as an independent equivalence witness. It does not define the newly declared canonical source ownership.

R5a writes a separate evidence receipt:

`release-evidence/v1.9-canonical-source-r5a.json`

The receipt records:

- 43-file remainder coverage;
- 29/14 ownership counts;
- ownership byte metrics;
- exact snapshot path set;
- historical-builder role as an equivalence witness until R5b;
- frozen 58-file oracle result.

R0 through R4b evidence remains separately phase-pinned.

## Permanent R5a regression gate

`tools/test_v1_9_public_remainder_r5a.py` preserves all load-bearing R4b checks and adds R5a ownership checks.

It requires:

- fail-closed DTCG alias behavior;
- six token-template components and 21 token bindings;
- 15 exact canonical applet pages;
- 17 shared components and the 247,281-byte deduplication invariant;
- 181 typed tokens and 66 aliases;
- three theme/source profiles and 180 theme-variable checks;
- preserved Minimax catalogue/page accent discrepancy evidence;
- the exact 43-file public remainder map;
- the exact 29/14 ownership split;
- two complete current builds from the same SHA with identical hash maps;
- all 58 public files matching the frozen v1.8.1 oracle on both builds;
- valid R0, R1, R2, R3, R4a, R4b, and R5a evidence receipts.

`Verify v1.9 canonical source` now runs this R5a gate.

## Non-goals

R5a intentionally does not:

- remove the historical builder from `build_current.py`;
- redesign any support page;
- change any lab layout or visual token value;
- change algorithms or learner state;
- change teaching copy or localization behavior;
- change Quick Assign behavior;
- change analytics/privacy behavior;
- change accessibility behavior;
- change deployment topology;
- change the public release identity.

The public boundary remains 15 applets / 58 files at exact frozen v1.8.1 bytes.

## Next: R5b direct canonical build

R5b removes the historical release ladder from the current build path.

The direct current builder should:

1. clean `_site`;
2. validate the current product, DTCG, page-component, and public-remainder source graphs;
3. copy/materialize the 43 non-applet files from `src/product/public-remainder.json`;
4. reconstruct the 15 applet pages from their canonical templates and shared components;
5. emit exactly 58 public files;
6. require the complete frozen SHA-256 oracle;
7. prove two direct builds from one SHA are byte-identical.

The historical v1.8.1 builder may remain temporarily as a separate test-only equivalence witness, but it must no longer be imported or invoked by `tools/build_current.py`.

After R5b, issue #47 should remain open until the remaining support-page primitives and source registries called out by the P0 architecture target are consolidated enough that the current product genuinely has one maintainable current architecture rather than only one direct build path.
