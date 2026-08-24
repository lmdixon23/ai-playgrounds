# Lab 13 Public v1.2 Integration Audit

Status: public-integration candidate. Acceptance requires an exact-head permanent Verify PASS after the thirteen-applet deployment boundary, release metadata, navigation/catalog, curriculum, sitemap, and public Lab 13 QA are all present in one branch head.

## Public integration contract

The v1.2 public build must satisfy all of the following simultaneously:

1. The deterministic Pages artifact contains exactly thirteen applets.
2. Lab 13 is generated from the accepted English source and accepted EN/ZH/VI/ES catalogs into one self-contained public HTML file.
3. The public Lab 13 page contains no non-public candidate wording and supplies canonical plus EN/ZH/VI/ES hreflang metadata.
4. `?lang=zh`, `?lang=vi`, and `?lang=es` select the corresponding locale on initial load without changing model arithmetic.
5. The public applet remains free of runtime fetch, XHR, external scripts, accounts, backends, and commercial-model API calls.
6. The landing-page manifest contains thirteen entries and exposes the Transformer Language Modeling route.
7. The public curriculum map contains a thirteenth course row for Transformer Language Modeling.
8. The sitemap contains the public Lab 13 route.
9. v1.2 citation and CodeMeta records must not attach the immutable v1.0.1 version DOI to v1.2.0.
10. The complete inherited v1.1, Lab 13 foundation, localization, four-locale browser, public-integration, and browser/responsive gates must pass together.

## Evidence boundary

This integration can establish that the published software implements the documented deterministic teaching model and that the tested public artifact preserves its arithmetic, localization state, links, and responsive containment. It does not establish learning gains, classroom adoption, accessibility conformance, or equivalence to a frontier language model.

## Release provenance

The v1.0.1 tag, release, and version DOI remain immutable. The v1.2.0 release metadata intentionally omits the old version DOI. A new v1.2.0 DOI, if one is later minted, must be recorded separately and must not rewrite the archived v1.0.1 provenance.

## Acceptance decision

HOLD until the exact public-integration head receives a complete permanent Verify PASS. After that pass, update this audit with the exact receipt, perform one squash merge of PR #19 into `main`, verify the merged main/Pages result, and create the v1.2.0 GitHub tag/release only from the verified merged commit.
