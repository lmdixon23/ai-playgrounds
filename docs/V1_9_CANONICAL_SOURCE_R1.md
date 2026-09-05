# AI Playgrounds v1.9 canonical source R1

Status: second bounded implementation step for issue #47.

## Purpose

R1 transfers final public catalogue ownership from the historical release-builder ladder to a canonical current source while preserving the exact frozen v1.8.1 public artifact.

R1 is intentionally not a visual or semantic redesign. It changes source authority only.

## Canonical catalogue

`src/product/catalogue.json` is an exact byte-for-byte snapshot of the shipped v1.8.1 public `applets.json` recovered from retained GitHub Pages deployment evidence.

The accepted catalogue SHA-256 is:

`60ec062792c19f429edcd5aea0fc719c0c0aced66163c4c7257ac6c04149d55f`

That digest is already the `applets.json` entry in `src/product/public-artifact-sha256.json`; the canonical source therefore binds directly to the frozen 58-file product oracle rather than introducing a second checksum authority.

The catalogue contains all fifteen public records, including:

- stable slugs;
- showcase and course order;
- icons and categories;
- EN/ZH/VI/ES public titles, descriptions, featured prompts, and category labels;
- level and nominal activity time;
- course phase;
- accent metadata;
- search keywords;
- the Minimax concept field retained exactly as shipped.

## Deterministic serialization contract

The canonical catalogue itself must already be in the exact public serialization form:

- UTF-8;
- `ensure_ascii=False`;
- two-space JSON indentation;
- source key order preserved;
- one trailing newline.

`tools/build_current.py` parses the source and serializes it again with that contract. If the resulting bytes differ from the committed source, the build fails.

This prevents formatting drift from being hidden behind semantically equivalent JSON.

## Legacy-to-canonical handoff

R1 still invokes `tools/build_site_v1_8_1.py` for the non-catalogue product composition.

Immediately after the legacy build:

1. the legacy-generated `_site/applets.json` bytes are read;
2. their SHA-256 is computed;
3. those bytes must equal `src/product/catalogue.json` exactly;
4. the build fails closed if they differ;
5. only after equivalence is proven is the canonical source written back as the final `_site/applets.json` owner;
6. the complete 58-file byte oracle is recomputed.

Therefore R1 does not merely assert that the two catalogue representations are similar. It proves they are identical before changing ownership.

## Product-model cross-checks

The R1 gate requires:

- exactly 15 canonical catalogue rows;
- unique slugs;
- showcase order exactly 1 through 15;
- catalogue membership equal to `src/product/labs.json` membership;
- title, course order, and accent agreement between the lab registry and public catalogue;
- non-empty EN/ZH/VI/ES learner-facing catalogue copy for every lab;
- non-empty search keywords for every lab;
- 15 active Quick Assigns with stable IDs and EN/ZH/VI/ES coverage;
- all current implementation ownership paths declared by `labs.json` to exist.

## Evidence

`tools/build_current.py` continues writing the R0 equivalence receipt so the first architecture invariant remains regression-tested.

It additionally writes:

`release-evidence/v1.9-canonical-source-r1.json`

The R1 receipt records:

- frozen baseline SHA;
- canonical catalogue path and SHA-256;
- deterministic serializer round-trip status;
- legacy and canonical handoff digests;
- exact byte-identical handoff status;
- current lab/track/Quick Assign counts;
- canonical/public catalogue parity;
- final 58-file artifact-oracle result.

## CI ownership

R1 replaces the R0-only architecture workflow with:

`.github/workflows/verify-v1.9-canonical-source.yml`

The current workflow runs one authoritative architecture gate rather than rebuilding the site once for R0 and again for R1. R0 hash-comparator regression cases are retained inside the R1 test.

## What changed in authority

Before R1:

`historical manifests + release patches -> public applets.json`

After R1:

`historical composition -> prove exact agreement with canonical catalogue -> canonical catalogue owns public applets.json`

The historical manifests remain frozen provenance and temporary compatibility inputs. They are no longer the final authority for current catalogue reasoning.

## What did not change

R1 does not intentionally change:

- any public byte;
- homepage layout or filtering;
- applet UI;
- algorithms;
- learner copy;
- translation;
- Quick Assign behavior;
- analytics;
- accessibility behavior;
- deployment topology;
- release identity.

The public software identity remains v1.8.1 throughout architecture-equivalence work.

## Acceptance criteria

R1 closes only when:

1. the canonical catalogue source is committed;
2. its SHA-256 equals the frozen public `applets.json` oracle entry;
3. deterministic re-serialization reproduces the committed source bytes;
4. the inherited v1.8.1 builder emits exactly the same catalogue bytes before handoff;
5. the canonical source becomes the final public catalogue owner;
6. all 58 final public files remain byte-identical to the frozen v1.8.1 oracle;
7. the full inherited `Verify` workflow passes;
8. the current canonical-source workflow passes and retains R0 and R1 receipts.

## Next

R2 gives Transformer, Agent Tool Use, and Minimax peer current-source ownership instead of reconstructing them through release-era candidate builders. R2 must preserve the same 58-file byte oracle.

R3 then extracts shared shell/design-token sources while still preserving bytes. R4 removes current dependence on the historical builder ladder.

Visible consistency fixes remain owned by #48 after the architecture boundary is proven.
