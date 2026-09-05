# AI Playgrounds v1.9 design-token contract R4a

Status: contract-first design-system milestone inside issue #47.

## Purpose

R4a gives the frozen v1.8.1 visual system a typed, machine-validated semantic vocabulary without changing any learner-facing byte.

The governing separation is:

`describe current visual values -> prove the description matches the product -> only later transfer CSS generation to tokens`

R4a therefore does not rewrite component CSS. That transfer is R4b.

## Standards basis

`src/design/ai-playgrounds.tokens.json` uses the Design Tokens Community Group stable **2025.10** format and identifies the corresponding schema:

`https://www.designtokens.org/schemas/2025.10/format.json`

The contract uses typed DTCG values and aliases rather than project-specific untyped variables.

R4a currently exercises these token types:

- `dimension`;
- `number`;
- `fontFamily`;
- `color`;
- `shadow`.

The validator treats the repository's supported DTCG subset as a fail-closed contract. Expanding the subset later requires an explicit validator change.

## Current contract size

Accepted R4a cardinalities:

- **181 typed tokens**;
- **66 aliases**;
- **3 frozen theme/source profiles** covering all 15 labs exactly once;
- **180 theme custom-property bindings** checked against reconstructed pages;
- **15 catalogue/UI accent bindings**;
- **21 high-confidence shared-component literal bindings**.

These numbers are regression boundaries for R4a. They are not quality targets for future design work.

## Token families

### Spacing

The token contract records the spacing values that materially recur in the frozen suite rather than pretending the current product already follows a smaller idealized scale.

The current dimension set includes values from 2 px through 64 px, with heavily used values such as 6, 8, 10, 12, 14, 16, 20, and 24 px represented explicitly.

Visible scale consolidation is a later evidence-led design decision.

### Radii

Current semantic radius roles are:

- compact: 6 px;
- control: 8 px;
- panel: 10 px;
- prominent: 12 px;
- large: 14 px;
- pill: 999 px.

R4a does not assert that every current radius choice is optimal. It gives the existing values names so later normalization becomes attributable.

### Controls and touch targets

Current control-height roles are:

- inline: 36 px;
- compact: 38 px;
- standard: 42 px;
- touch: 44 px.

The presence of several roles reflects the frozen suite. R4b may transfer exact existing values to tokens; #48/#49 decide whether visible or accessibility-driven consolidation is warranted.

### Focus

R4a records the current 3 px focus-ring width and 2/3 px offset variants.

### Layout widths and gutters

Named current roles include:

- reading: 760 px;
- support: 820 px;
- learning: 980 px;
- wide: 1180 px;
- compact gutter: alias to 14 px;
- standard gutter: alias to 20 px.

### Responsive breakpoints

The contract records the current implementation variants rather than collapsing them:

- 480 px legacy phone breakpoint;
- 520 px newer phone breakpoint;
- 680 px support breakpoint;
- 720 px compact shell breakpoint;
- 820 px learning breakpoint;
- 980 px wide/newer breakpoint.

These differences are candidates for later product review, not architecture-time corrections.

### Typography

R4a records the current system UI font family, common font-size roles, line-height roles, and font-weight roles including the existing 750 action weight.

### Color and semantic state

The contract distinguishes:

- primitive frozen colors;
- legacy light/dark surfaces;
- newer light/dark surfaces;
- Minimax light surfaces;
- semantic success/warning/error roles;
- per-lab catalogue and page accent roles.

This is intentionally more explicit than a single universal palette because the current product has multiple visual lineages that must be represented before they can be safely reconciled.

### Shadows

R4a records current popover, subtle-card, and card shadows as typed shadow values.

## Implementation lineage is not curriculum taxonomy

`src/design/current-bindings.json` defines three frozen **theme/source profiles**:

1. original-twelve legacy UI lineage;
2. Transformer + Agent Tool Use newer UI lineage;
3. Minimax current visual profile.

These are implementation descriptions only.

Curriculum taxonomy remains unchanged:

- Transformer: Modern extension;
- Agent Tool Use: Modern extension;
- Minimax: Foundations.

The validator requires theme-profile membership to cover all fifteen pages exactly once while the product model separately preserves the 13 Foundations / 2 Modern-extension boundary.

## Minimax accent discrepancy is preserved as evidence

Minimax currently has:

- canonical catalogue accent: `#0d9488`;
- frozen light page accent: `#3157c8`;
- frozen dark page accent: `#93c5fd`;
- frozen dark strong accent: `#1d4ed8`.

R4a models those as distinct token roles and explicitly fails if the catalogue/page discrepancy is accidentally erased.

That discrepancy remains a #48 visual-consistency candidate. Architecture work must not silently resolve it because doing so would change the public artifact and conflate source refactoring with design judgment.

## Frozen theme binding validation

`tools/design_tokens.py` reconstructs the fifteen R3 canonical pages and validates the theme profiles directly against their CSS custom properties.

For each assigned page it checks the declared light and dark selectors and the current values of:

- `--bg`;
- `--card`;
- `--fg`;
- `--muted`;
- `--border`;
- `--soft`.

This produces **180 exact theme-variable checks** across the suite.

Equivalent CSS hex spellings such as `#fff` and `#ffffff` normalize to the same color for comparison; the typed token remains the explicit six-digit sRGB value.

## Accent validation

For every lab, the validator requires:

1. the catalogue token to equal the canonical `src/product/catalogue.json` accent;
2. the page `:root --accent` to equal the current `uiLight` token;
3. for Transformer, Agent Tool Use, and Minimax, the v1.8.1 dark-theme `--accent` and `--accent-strong` overrides to equal their declared dark token roles.

For the original twelve, the frozen contract records the same accent role across light and dark themes unless later product evidence deliberately changes it.

## Shared-component literal bindings

R4a also binds 21 high-confidence literals in the already-canonical R3 shared components to semantic tokens.

Examples include:

- 38/42/44 px control heights;
- 8 px control radius;
- 8 px shared gaps;
- 520/720/820/980 px responsive boundaries;
- 760/980/1180 px layout widths.

The validator requires:

- the component resource to exist;
- the frozen literal to occur exactly the declared number of times;
- the referenced token to resolve successfully;
- the resolved token's CSS scalar value to be the value represented by that literal.

R4a still leaves the literal in the component source. R4b will replace selected literals with token-owned build-time source while reproducing the exact same emitted bytes.

## DTCG validator behavior

`tools/design_tokens.py` validates:

- exact stable schema identifier;
- inherited and explicit `$type` ownership;
- supported typed values;
- finite numeric values;
- px/rem dimension objects;
- sRGB colors and component/hex agreement;
- alpha range;
- shadow structure;
- full-token aliases;
- alias target existence;
- alias type equality;
- alias-cycle rejection;
- theme-profile membership;
- current page CSS bindings;
- all 15 accent bindings;
- component literal bindings;
- required semantic token paths.

The R4a test also injects an unresolved alias and an alias cycle and requires both to fail closed.

## Current build integration

`tools/build_current.py` now validates the token contract **before** invoking the historical equivalence builder.

The current sequence is therefore:

1. validate catalogue ownership;
2. validate the 15-page / 17-component R3 source graph;
3. validate the R4a DTCG token contract and frozen bindings;
4. validate lab / Quick Assign / release ownership;
5. run the historical v1.8.1 ladder as an independent equivalence witness;
6. require exact catalogue/page handoffs to canonical sources;
7. verify all 58 final public SHA-256 values;
8. retain R0, R1, R2, R3, and R4a machine-readable receipts.

A token-contract failure therefore blocks the current build even though tokens do not yet synthesize CSS.

## Determinism and public-output boundary

`tools/test_v1_9_design_token_contract_r4a.py` performs two complete current builds from the same SHA and requires their 58-file hash maps to be identical.

Both builds must independently equal the frozen v1.8.1 oracle.

The design-token files themselves are source artifacts. They are not added to the public 58-file deployment in R4a.

## Evidence boundary

R4a proves that the frozen product's key design values now have typed semantic ownership and machine-checkable bindings.

It does **not** prove that those values are aesthetically optimal, accessible in every context, or internally consistent enough for the final v1.9 product.

Those questions remain owned by:

- #48 whole-suite visual evidence and regression;
- #49 WCAG 2.2 AA engineering audit;
- #50 human learner/educator validation.

## Next

### R4b — tokenized build-time shell ownership

Replace selected high-confidence literals in canonical shared-component **source** with semantic token references or token-controlled rendering, while reproducing the exact frozen component/public bytes.

R4b must preserve:

- all R0–R4a invariants;
- explicit mechanism-required variants;
- two-build determinism;
- the 58-file public oracle.

### R5 — current builder independence

After tokenized shared-source ownership is proven, remove current dependence on the historical release ladder one bounded dependency at a time.

Only after #47 is complete may #48 intentionally change visible design.
