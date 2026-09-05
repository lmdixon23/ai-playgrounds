# AI Playgrounds v1.9 canonical source R2

Status: third bounded implementation step for issue #47.

## Purpose

R2 gives Transformer Language Modeling, Agent Tool Use and Context Protocols, and Minimax / Alpha-Beta Pruning peer current-page ownership under `src/labs/` while preserving the exact frozen v1.8.1 public product.

This is a source-authority change, not a redesign.

## Why these three pages

The original twelve applets already exist as committed applet sources under `playgrounds/` and are transformed by the release build. Transformer, Agent Tool Use, and Minimax were introduced through later candidate-era generators and then modified by subsequent release transforms.

That created two source-authority classes inside the fifteen-lab product.

R2 removes the final-output ownership asymmetry without pretending that the three pages have the same curriculum classification:

- Transformer: Modern extension;
- Agent Tool Use: Modern extension;
- Minimax: Foundations.

The phrase **peer current pages** therefore describes source architecture, not curriculum taxonomy.

## Canonical peer current-page sources

The exact shipped v1.8.1 pages are committed as:

- `src/labs/transformer-language-model/index.html`
- `src/labs/agent-tool-context/index.html`
- `src/labs/minimax-alpha-beta/index.html`

Accepted frozen digests:

| Page | Bytes | SHA-256 |
|---|---:|---|
| Transformer Language Modeling | 232,495 | `0bc827febb1b6be280cd34f8f85ced3edd80d0c5cb79fbe62f0a2072ea005488` |
| Agent Tool Use and Context Protocols | 237,751 | `7a4afac9d6bec59346e52bbc962e88a233e9b04e1580a6ce12955973c1a598bf` |
| Minimax / Alpha-Beta Pruning | 193,578 | `48d9deb32ccc74f918e167d08aecbce834289d36ab199ce77dc2932070961132` |

These are the same digests already recorded for the corresponding public paths in `src/product/public-artifact-sha256.json`; R2 does not create a competing checksum authority.

## Materialization provenance

The three committed peer sources were materialized by an evidence-only branch workflow that:

1. ran the already byte-locked R1 current build;
2. copied the final generated pages from `_site`;
3. checked each copied source against the frozen 58-file oracle;
4. committed only after all three hashes matched.

The temporary bootstrap workflow was then deleted before review. It is not part of the durable architecture.

## Lab registry ownership

`src/product/labs.json` now declares each of the three pages as:

`canonical-current-page-with-legacy-equivalence`

and identifies `src/labs/<slug>/index.html` as its primary current owner.

Candidate-era builders, historical manifests, learner-parity sources, and the v1.8.1 release patch remain declared as **legacy equivalence inputs**. They are retained for regression evidence and provenance, not as the final source authority.

## Build handoff

`tools/build_current.py` now performs two independent final-authority handoffs after the frozen historical builder completes.

### Catalogue handoff

The R1 contract remains unchanged:

1. legacy `_site/applets.json` must equal `src/product/catalogue.json` byte-for-byte;
2. failure aborts the build;
3. canonical catalogue bytes become final public catalogue bytes.

### Peer-page handoff

For each of Transformer, Agent Tool Use, and Minimax:

1. validate the committed canonical source against the frozen public-page digest before the legacy build;
2. run the complete v1.8.1 historical composition;
3. read the resulting final public page;
4. require the legacy final bytes to equal the canonical current-page source exactly;
5. fail closed on any difference;
6. write the canonical bytes as the final public owner;
7. recompute the complete 58-file oracle.

Thus the old generation chain remains an independent equivalence producer during R2, but it cannot silently override or diverge from canonical current source.

## Curriculum safeguards

R2 explicitly preserves:

- 13 Foundations applets;
- 2 Modern extensions;
- Transformer and Agent as the only Modern-extension curriculum members;
- Minimax as Foundations;
- all fifteen course orders;
- all fifteen Quick Assign mappings;
- EN/ZH/VI/ES learner locale coverage.

Source lineage and curriculum track are separate dimensions.

## Evidence

The current build continues to write R0 and R1 receipts and additionally writes:

`release-evidence/v1.9-canonical-source-r2.json`

The R2 receipt records:

- frozen baseline SHA;
- canonical catalogue handoff;
- canonical peer-source path, byte count, digest, and oracle binding for all three pages;
- legacy/canonical peer-page handoff digests;
- byte-identical handoff status;
- curriculum and Quick Assign counts;
- final catalogue parity;
- complete 58-file oracle result.

## CI

`.github/workflows/verify-v1.9-canonical-source.yml` advances to `tools/test_v1_9_canonical_source_r2.py`.

The current gate retains:

- R0 changed / added / removed artifact comparator regressions;
- R1 canonical catalogue serialization and ownership invariants;
- the complete 58-file oracle;

and adds:

- exact peer source membership;
- exact peer source hash/oracle binding;
- explicit curriculum-track preservation;
- exact legacy/canonical page handoff;
- final public page equality to canonical peer source.

## What did not change

R2 does not intentionally change:

- any public byte;
- applet UI or layout;
- algorithms;
- learner copy;
- translations;
- Quick Assign behavior;
- analytics;
- accessibility behavior;
- deployment topology;
- public release identity.

The public software version remains v1.8.1 throughout architecture-equivalence work.

## Acceptance criteria

R2 closes only when:

1. all three canonical peer current pages are committed;
2. each committed source digest equals its frozen public oracle digest;
3. `src/product/labs.json` identifies the three canonical current owners and preserves curriculum taxonomy;
4. the full legacy build produces exactly the same page bytes before handoff;
5. canonical sources become the final public owners only after exact equality is proven;
6. canonical catalogue ownership from R1 remains intact;
7. all 58 final public files remain byte-identical to frozen v1.8.1;
8. the current canonical-source workflow passes;
9. the independent full `Verify` workflow passes;
10. the temporary bootstrap workflow is absent from the final PR.

## Next: R3 shared-source extraction

R3 will extract byte-identical shared shell/runtime/style blocks from the fifteen committed/final page structures into canonical build-time components while retaining mechanism-required variants explicitly.

Pre-implementation census already shows two coherent UI lineages and multiple exact shared blocks. R3 will centralize only blocks whose byte identity has been proven, then reconstruct final pages exactly under the same 58-file oracle.

Visible visual normalization remains deferred to #48 until #47's architecture workstream is fully complete.
