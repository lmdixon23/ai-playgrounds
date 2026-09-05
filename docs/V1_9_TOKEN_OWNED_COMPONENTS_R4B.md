# AI Playgrounds v1.9 R4b — Token-owned shared components

## Status

R4b is a behavior-preserving architecture milestone inside issue #47.

It transfers six high-confidence shared style components from raw canonical files to DTCG token-template ownership while preserving the exact public v1.8.1 product boundary.

R4b does **not** authorize visible redesign or token-value normalization. Values remain frozen to the accepted v1.8.1 output. Visual consolidation remains evidence-led work for issue #48.

## Starting point

R4a established a typed DTCG 2025.10 token contract and proved that the token graph described the frozen product. R4a remained contract-first: tokens were validated against source literals, but public component bytes were still owned by raw component files.

R4b makes the first source-ownership transfer.

## Final source model

The canonical page graph still contains:

- 15 lab page templates;
- 17 shared components;
- 247,281 duplicate source bytes removed relative to storing all 15 final pages independently.

Component ownership is now mixed and explicit:

- 11 raw canonical components;
- 6 token-template canonical components.

The six token-owned components contain:

- 21 semantic token bindings;
- 19,050 rendered component bytes;
- 19,724 token-template source bytes.

Their canonical manifest is `src/design/token-components.json`.

## Token-owned components

The six transferred components are:

1. `newer/v172-modern-parity-style`
2. `newer/v172-modern-toolbar-parity-style`
3. `newer/v181-modern-learner-parity-style`
4. `original/learner-interface-style`
5. `original/learning-modes-style-common`
6. `original/v14-version-provenance-style`

Each former raw source has been replaced by a `.template.html` source containing explicit `{{dt:<token.path>}}` markers.

The superseded raw path is retained only as historical provenance in the token-component manifest. The raw file itself must not exist after R4b.

## Layering

R4b separates the architecture into four layers.

### 1. DTCG value engine

`tools/token_values.py` owns low-level token parsing, alias resolution, type validation, CSS serialization, and fail-closed cycle or missing-alias behavior.

Higher-order tooling must not implement a second token resolver.

### 2. Token-component renderer

`tools/token_components.py` loads `src/design/token-components.json`, renders the six templates from the DTCG contract, and verifies the declared rendered hash and byte count for every component.

The final R4b renderer has no dependency on the retired raw component files.

### 3. Page composer

`tools/page_components.py` understands two explicit component source kinds:

- `raw`
- `token-template`

It renders token-template components through the token-component layer, combines all 17 components with the 15 page templates, and requires every reconstructed page to match the frozen public hash oracle.

### 4. Product-level design validation

`tools/design_tokens.py` validates the semantic contract against the reconstructed product:

- DTCG 2025.10 schema and types;
- 181 typed tokens;
- 66 aliases;
- three theme/source profiles covering all 15 labs;
- 180 theme-variable bindings;
- all 15 catalogue and UI accent bindings;
- 21 rendered shared-component bindings;
- six active token-template component owners;
- the full 15-page / 17-component graph.

## Preserved discrepancy evidence

R4b continues to preserve the current Minimax accent discrepancy as evidence rather than silently normalizing it:

- catalogue accent: `#0d9488`
- light page accent: `#3157c8`
- dark page accent: `#93c5fd`
- dark strong accent: `#1d4ed8`

That remains a visual-consistency candidate for issue #48.

## Guarded migration sequence

The source transfer was deliberately staged.

1. Materialize token templates alongside the raw component sources.
2. Prove all 21 substitutions reconstruct the exact raw component bytes.
3. Introduce one shared low-level DTCG resolver.
4. Teach the page composer both source kinds while the live graph still uses raw ownership.
5. Teach the higher-order validator both the R4a raw-binding and R4b rendered/template binding models.
6. Transfer the six component rows to token-template ownership.
7. Delete the six superseded raw component files.
8. Re-run token rendering, all-page reconstruction, design-token validation, and the complete current build after deletion.

The ownership migration was accepted only after the post-deletion graph remained exact.

## Current build boundary

`tools/build_current.py` now identifies the architecture phase as `v1.9-r4b-token-owned-components`.

R0 through R4a receipts remain preserved as historical invariants. R4b adds `release-evidence/v1.9-canonical-source-r4b.json`.

The historical v1.8.1 builder remains in the current facade only as an independent equivalence witness for public files not yet canonically owned outside the applet-page graph. Removing that dependency is R5 work.

## Permanent R4b regression gate

`tools/test_v1_9_token_owned_components_r4b.py` requires:

- fail-closed missing aliases and alias cycles;
- six token-template components and 21 bindings;
- absence of all six superseded raw sources;
- 11 raw plus six token-template component owners;
- exact 15-page reconstruction;
- exact R4b design-token and binding cardinalities;
- preserved Minimax discrepancy evidence;
- two complete builds from the same SHA with identical hash maps;
- all 58 public files matching the frozen v1.8.1 oracle on both builds;
- valid R0, R1, R2, R3, R4a, and R4b evidence receipts.

The authoritative `Verify v1.9 canonical source` workflow now runs this R4b gate. The inherited full `Verify` workflow remains an independent product-level regression suite.

## Non-goals

R4b intentionally makes no learner-facing change to:

- algorithms or simulation state;
- teaching copy or scenario structure;
- locale behavior;
- Quick Assign behavior;
- analytics or privacy behavior;
- accessibility behavior;
- layout or visual appearance;
- public file topology;
- release identity.

The public boundary remains 15 applets and 58 deployed files at v1.8.1 bytes.

## Next architecture milestone

R5 should remove `build_current.py` dependence on the historical release ladder without using a monolithic opaque snapshot as the final architecture.

A safe sequence is:

1. classify every non-applet public file by current source owner;
2. reuse existing byte-identical repository sources where they already exist;
3. materialize only genuinely generated support outputs under canonical current source paths;
4. make the current builder emit the entire 58-file product directly from canonical sources;
5. retain the historical builder only as an external equivalence test until direct canonical ownership is proven;
6. then remove it from the current build path.

Support-page primitives and registries can subsequently be decomposed further without blocking removal of the version-layered current build dependency.
