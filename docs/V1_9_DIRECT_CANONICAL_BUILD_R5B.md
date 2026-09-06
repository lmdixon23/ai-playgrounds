# AI Playgrounds v1.9 R5b — Direct canonical current build

## Status

R5b is a behavior-preserving architecture milestone inside issue #47.

It removes the historical version-layered release builder from the **current build path**. `tools/build_current.py` now emits the complete 58-file public product directly from canonical current source graphs.

Historical builders remain in the repository only as regression and provenance inputs for the inherited historical test suite.

## Starting point

R5a established explicit source ownership for every public path:

- 15 applet pages from canonical lab templates and shared components;
- 43 non-applet public files from `src/product/public-remainder.json`;
- 29 of those 43 from byte-identical existing repository sources;
- 14 from exact accepted current snapshots under `src/site/current/`.

R5a still invoked `tools/build_site_v1_8_1.py` as an independent current-build witness. R5b removes that runtime dependency.

## Direct current-build graph

The current product now composes from four load-bearing source layers.

### 1. Public remainder

`tools/public_remainder.py` validates and emits exactly 43 non-applet public files.

`public_remainder.emit(site)`:

- reads only sources declared by `src/product/public-remainder.json`;
- verifies source SHA-256 and byte count before emission;
- writes each public path directly to the target site root;
- re-reads every emitted file;
- verifies emitted SHA-256 and byte count immediately;
- requires exactly 43 emitted files.

### 2. Applet page graph

`tools/page_components.py` reconstructs all 15 applet pages from:

- 15 canonical page templates;
- 17 shared components;
- 11 raw components;
- 6 DTCG token-template components.

Every reconstructed page remains bound to the frozen public oracle.

### 3. Design-token graph

`tools/token_values.py`, `tools/token_components.py`, and `tools/design_tokens.py` preserve:

- DTCG 2025.10 token parsing and type validation;
- 181 typed tokens;
- 66 aliases;
- six token-owned components;
- 21 token-template bindings;
- three theme/source profiles;
- 180 theme-variable checks;
- all 15 accent bindings;
- the explicit Minimax catalogue/page accent discrepancy safeguard.

### 4. Direct site composer

`tools/direct_current_site.py` is the current low-level site composer.

It:

1. validates the page, token, and remainder source graphs;
2. removes any existing `_site` directory;
3. emits all 43 remainder files;
4. emits all 15 reconstructed applet pages;
5. requires exactly 58 files;
6. compares every emitted SHA-256 against `src/product/public-artifact-sha256.json`;
7. fails closed on any added, missing, or changed public path.

It imports no historical release builder and does not import `tools/build_current.py`.

## Current facade

`tools/build_current.py` remains the canonical high-level facade because it also validates product registries and writes architecture evidence.

In R5b it imports only current source/build layers:

- `design_tokens`
- `direct_current_site`
- `page_components`
- `public_remainder`

The current facade must not contain executable historical build coupling such as:

- `from build_site_v...`
- `import build_site_v...`
- `build_legacy_v...`
- legacy handoff functions.

The string `tools/build_site_v1_8_1.py` may remain in historical evidence or release metadata solely to identify the regression/provenance builder.

## Release metadata

`src/product/release.json` now declares:

- architecture phase `v1.9-r5b-direct-canonical-build`;
- `direct_current_build: true`;
- current composer `tools/direct_current_site.py`;
- historical builder role `test-only-regression-and-provenance`.

The accepted lower-level source graphs retain their own phase identities:

- R4b page/design graph: `v1.9-r4b-token-owned-components`;
- R5a public remainder graph: `v1.9-r5a-public-remainder-ownership`.

R5b does not silently relabel those accepted subgraphs.

## Evidence

R5b adds:

`release-evidence/v1.9-canonical-source-r5b.json`

The receipt records:

- direct current-build status;
- current composer path;
- historical builder as test-only;
- explicit assertion that the current facade does not import the historical builder;
- 43-file remainder emission;
- 15-file applet-page emission;
- 58-file total boundary;
- frozen artifact-oracle result.

R0 through R5a remain separately phase-pinned historical architecture receipts. Their representation fields may note that the current product now builds directly, but their phase identities and load-bearing invariants are preserved.

## Permanent R5b regression gate

`tools/test_v1_9_direct_canonical_build_r5b.py` requires:

- all load-bearing R4b token/page invariants;
- the accepted R5a 43-file remainder ownership map;
- exact 29 existing / 14 snapshot ownership split;
- no executable historical-builder coupling in `tools/build_current.py`;
- direct composer import and invocation by the facade;
- historical builder still available as test/provenance input;
- top-level R5b release metadata;
- preserved R4b and R5a subgraph phases;
- two complete direct-composer builds with identical hash maps;
- two complete current-facade builds with identical hash maps;
- all 58 files matching the frozen v1.8.1 oracle on every accepted build;
- valid R0, R1, R2, R3, R4a, R4b, R5a, and R5b evidence receipts.

`Verify v1.9 canonical source` runs this gate and retains R0 through R5b evidence artifacts.

## Historical ladder after R5b

Historical builders are no longer part of current product construction.

They remain useful because the independent inherited `Verify` workflow still tests historical releases, candidate compositions, browser behavior, algorithm contracts, localization, and release regressions. That is an appropriate test/provenance role and no longer architectural coupling.

R5b therefore distinguishes:

- **current build authority**: current canonical source graphs only;
- **historical regression authority**: historical builders/tests where historically relevant.

## Non-goals

R5b intentionally does not:

- redesign any page;
- normalize any visual token value;
- change algorithm behavior or learner state;
- change teaching copy;
- change locale semantics;
- change Quick Assign behavior;
- change analytics/privacy behavior;
- change accessibility behavior;
- change deployment topology;
- change the public release identity;
- delete historical builders or historical verification tests.

The public boundary remains 15 applets / 58 files at exact frozen v1.8.1 bytes.

## Remaining issue #47 work

R5b completes **version-layered current-builder removal**, but issue #47 should remain open.

The remaining P0 architecture work is consolidation of current registries and support-page source primitives, especially:

1. move the active Quick Assign registry out of `tools/quick_assigns_v2.json` into canonical product source;
2. establish one current learner-locale registry instead of repeated hardcoded locale arrays/copy-key declarations;
3. make release/version metadata have one explicit current owner;
4. decompose the 14 R5a support-page/current snapshots where shared current primitives materially improve maintainability;
5. keep all of those changes behavior-preserving and frozen-byte locked until the architecture issue closes.

Visible whole-suite redesign remains deferred to issue #48.
