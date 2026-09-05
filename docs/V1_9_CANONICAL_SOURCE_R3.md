# AI Playgrounds v1.9 canonical source R3

Status: third bounded architecture milestone for issue #47.

## Purpose

R3 removes the two-class current-page source model without changing the public product.

All fifteen applets now have the same current source shape:

`canonical lab template + declared shared components -> exact self-contained public applet page`

The historical release-builder ladder remains only as an independent equivalence witness during this phase.

## Canonical page graph

`src/product/page-components.json` is the authoritative page-composition graph.

It declares:

- 15 canonical applet templates under `src/labs/<slug>/index.template.html`;
- 17 exact shared component blocks under `src/ui/components/`;
- the component references used by each page;
- the exact public SHA-256 and byte count for each reconstructed page;
- the exact SHA-256, byte count, and declared user set for every component;
- deterministic source-deduplication metrics.

Accepted R3 metrics:

- full frozen applet-page bytes: `3,195,013`;
- canonical template bytes: `2,890,803`;
- unique shared-component bytes: `56,929`;
- duplicate canonical-source bytes removed: `247,281`.

These figures describe source representation only. Public output size is intentionally unchanged.

## Shared blocks and explicit exceptions

R3 extracts only blocks already proven byte-identical. It does not force visual or behavioral convergence.

### Original-twelve lineage

The original twelve share exact copies of:

- `learner-interface-style`;
- `essay-language-script`;
- `learning-modes-script`;
- `v14-version-provenance-style`.

The `learning-modes-style` block has three explicit variants:

- common variant used by ten labs;
- Hill Climbing variant used only by `hill-climbing`;
- KNN variant used only by `knn-classifier`.

Those variants are preserved because they are real current-product differences. R3 does not classify them as defects or normalize them automatically.

### Newer three-page UI lineage

Transformer, Agent Tool Use, and Minimax share exact copies of eight later parity blocks:

- v1.7 Quick Assign base style;
- v1.7 Quick Assign containment;
- v1.7.2 modern parity style;
- v1.7.2 toolbar parity style;
- v1.7.2 Quick Assign parity style;
- v1.7.2 accessibility parity style;
- v1.7.2 toolbar runtime;
- v1.8.1 learner-parity style.

Transformer and Agent Tool Use additionally share two exact packet-runtime blocks that Minimax does not use.

This is an implementation lineage, not a curriculum category. Minimax remains a Foundations lab; Transformer and Agent Tool Use remain Modern extensions.

## Source ownership

`src/product/labs.json` now assigns every lab:

- `kind = canonical-template-with-shared-components-and-legacy-equivalence`;
- a canonical `primary` template under `src/labs/`;
- the shared `src/product/page-components.json` manifest;
- the prior source/builder chain nested under `legacy_equivalence`.

The legacy chain is therefore provenance and a temporary regression witness, not current final-page authority.

The three R2 full-page snapshots under `src/labs/<slug>/index.html` are removed because their complete bytes are now reproducible from the R3 template/component graph.

## Independent composer validation

`tools/page_components.py` validates the canonical graph without invoking a historical builder.

It fails closed unless:

1. page count is exactly 15;
2. component count is exactly 17;
3. every component file exists and matches its declared SHA-256 and byte count;
4. every template exists;
5. every page references only declared components and no component twice;
6. every component marker occurs exactly once where declared;
7. no unresolved component marker remains after reconstruction;
8. every reconstructed page matches its declared page SHA-256;
9. every reconstructed page matches the frozen v1.8.1 public oracle;
10. component user sets equal actual page references;
11. page slugs, public paths, and template paths are unique;
12. the four recorded byte metrics recompute exactly;
13. deduplicated source bytes remain exactly `247,281` during this frozen-equivalence phase.

## Current build handoff

`tools/build_current.py` now performs this sequence:

1. validate release, catalogue, lab, Quick Assign, and page-component ownership;
2. reconstruct all fifteen canonical pages from templates and components;
3. prove those reconstructions already match the frozen public-page oracle;
4. run the historical v1.8.1 ladder as an independent equivalence producer;
5. require every one of the fifteen legacy-produced pages to equal its canonical reconstruction byte-for-byte;
6. require the legacy-produced catalogue to equal `src/product/catalogue.json` byte-for-byte;
7. transfer final page and catalogue ownership to canonical sources;
8. verify all 58 public files against the frozen v1.8.1 SHA-256 oracle;
9. write R0, R1, R2, and R3 evidence receipts.

A legacy/canonical mismatch prevents handoff. The build does not silently prefer either result.

## R2 preservation

R2 established exact current-page ownership for Transformer, Agent Tool Use, and Minimax.

R3 supersedes the full-page representation with templates plus components, but the R2 invariant remains regression-tested: the reconstructed bytes for all three pages remain exactly the same frozen hashes.

The R2 evidence receipt explicitly records that its representation is superseded by R3 template/component composition rather than pretending the deleted full-page snapshots remain current sources.

## R3 CI gate

`tools/test_v1_9_canonical_source_r3.py` adds:

- hash-comparator self-tests for changed, added, and removed files;
- 15-page / 17-component graph validation;
- explicit Hill Climbing and KNN variant checks;
- explicit Transformer/Agent packet-runtime exception checks;
- uniform all-lab ownership checks;
- public-page equality against all canonical reconstructions;
- two complete current builds from the same SHA and exact hash-map equality between them;
- frozen 58-file oracle verification on both builds;
- R0 through R3 evidence validation.

The full inherited `Verify` workflow remains independent and unchanged.

## What R3 does not claim

R3 does not claim that the existing visual design is optimal or fully consistent.

It does not intentionally change:

- any public byte;
- algorithm behavior;
- learner copy or translation;
- Quick Assign behavior;
- locale/state semantics;
- analytics or privacy behavior;
- accessibility behavior;
- homepage behavior;
- release identity;
- deployment topology.

R3 also does not yet make semantic design tokens the current source of emitted CSS. It creates the stable shared-component boundary needed to do that safely.

## Next architecture work

### R4 — semantic design-token and shared-shell ownership

Derive canonical spacing, typography, radii, control-size, surface, semantic-state, focus, width/gutter, and responsive values from the now-stable component sources. Preserve exact public bytes while proving token/component serialization.

Mechanism-required variants remain explicit rather than being normalized for aesthetic uniformity.

### R5 — current builder independence

Replace current dependence on the historical v1.8.1 → v1.8 → v1.7.x → older release ladder one bounded dependency at a time. Historical builders remain frozen provenance/reproduction tools.

Only after the canonical architecture and token work is complete should #48 intentionally change visible design.
