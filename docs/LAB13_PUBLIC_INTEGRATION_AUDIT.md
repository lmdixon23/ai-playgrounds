# Lab 13 Public v1.2 Integration Audit

Status: **PASS — public v1.2 integration accepted**.

Accepted public-integration head: `d125b4d35e231b15bf0a48be6fdbe5ce134ef744`.

Permanent Verify receipt: run #139 (`32735919506`), job `97458554190` — **PASS**.

Evidence artifact: `ai-playgrounds-verification-32735919506`, artifact ID `9523296068`, SHA-256 `14da20a605c325a7058fa25751fa49ea9f331a7a83414f84495c00e39998b78f`.

## 1. Public integration contract

The accepted v1.2 public build satisfies all of the following simultaneously:

1. The deterministic Pages artifact contains exactly thirteen applets and 53 public files.
2. Lab 13 is generated from the accepted English source and accepted EN/ZH/VI/ES catalogs into one self-contained public HTML file.
3. The public Lab 13 page contains no non-public candidate wording and supplies canonical plus EN/ZH/VI/ES hreflang metadata.
4. `?lang=zh`, `?lang=vi`, and `?lang=es` select the corresponding locale on initial load without changing model arithmetic.
5. The public applet remains free of runtime fetch, XHR, external scripts, accounts, backends, and commercial-model API calls.
6. The deployed v1.2 manifest contains thirteen entries and exposes the Transformer Language Modeling route while the inherited twelve-applet source manifest remains stable for the legacy release checker.
7. The public landing page renders thirteen applet cards.
8. The public curriculum map contains a thirteenth course row for Transformer Language Modeling.
9. The sitemap contains the public Lab 13 route.
10. v1.2 citation and CodeMeta records do not attach the immutable v1.0.1 version DOI to v1.2.0.
11. The complete inherited v1.1, Lab 13 foundation, localization, four-locale browser, public-integration, and browser/responsive gates pass together.

## 2. Public applet construction

`tools/build_transformer_public.py` promotes the previously accepted four-locale verification candidate into the public release shell without changing the frozen model arithmetic or the accepted localization catalogs.

The public layer adds:

- canonical and locale-specific hreflang metadata;
- a stable suite-back route;
- release rather than candidate labeling;
- locale initialization from the public `lang` query parameter;
- no new network dependency.

`tools/build_site.py` generates the final Lab 13 file at:

`playgrounds/transformer-language-model/index.html`

inside the deterministic `_site` artifact. The deployed file remains a single HTML document.

## 3. Manifest and legacy-source boundary

The inherited v1.1 static release checker is intentionally bound to the twelve historical source applets under `playgrounds/` and the twelve-entry root `applets.json`.

v1.2 therefore adds an explicit release manifest at:

`tools/applets_v1_2.json`

The Pages builder deploys that thirteen-entry manifest as public `applets.json`, synchronizes the built landing page from it, and separately generates Lab 13. This preserves the historical source checker without allowing it to silently certify a generated thirteenth applet.

The dedicated v1.2 integration gate verifies that the deployed manifest and deployed applet set are identical and contain exactly thirteen entries.

## 4. Dedicated public integration gate

`tools/test_transformer_public_integration.py` completed **24/24 checks**, including:

- twelve-entry legacy source-manifest preservation;
- thirteen-entry v1.2 release-manifest parity;
- exact thirteen-applet and 53-file deployment boundaries;
- landing-page route and rendered-card integration;
- curriculum and sitemap integration;
- public release-note integration;
- removal of candidate-only language;
- canonical and hreflang metadata;
- one-file/offline constraints;
- query-parameter locale initialization;
- EN/ZH/VI/ES title and document-language parity;
- frozen arithmetic preservation;
- mobile root containment.

The same exact-head workflow also passed the inherited release, pedagogical, Guided Challenge, localization, algorithm, Transformer reference, cross-runtime, prototype, English-source, semantic-catalog, four-locale browser, and complete browser/responsive gates.

## 5. Release metadata boundary

v1.2.0 is dated 2026-08-24 in `CITATION.cff`, CodeMeta, changelog, release notes, and README release metadata.

The v1.0.1 tag, GitHub release, and DOI `10.5281/zenodo.21854217` remain immutable and explicitly archived. The old version DOI is not attached to the v1.2.0 citation metadata. A new v1.2.0 DOI, if later minted, must be recorded separately.

## 6. Evidence boundary

This integration establishes that the published software implements the documented deterministic teaching model and that the tested public artifact preserves its arithmetic, localization state, links, deployment boundary, and responsive containment.

It does not establish learning gains, classroom adoption, accessibility conformance, or equivalence to a frontier language model.

## 7. Acceptance decision

**PASS.**

The public Lab 13 integration is merge-ready subject to one final exact-head Verify pass containing this receipt-only audit update. After that pass, PR #19 may be squash-merged once into `main`; the merged main/Pages result must then be checked before creating the v1.2.0 GitHub tag/release from the verified merged commit.
