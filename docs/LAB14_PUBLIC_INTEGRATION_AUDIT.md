# Lab 14 Public v1.3 Integration Audit

Status: **PASS — R7 public-integration candidate accepted; receipt-bearing exact-head verification pending**.

Frozen R4 English source head: `9f2f5286f4de3e12a881b61d491c87efe6950166`.

Frozen R5 localization head: `37bdc6a4a84b672ad564d81564e8a055c2b2c9a6`.

Frozen R6 browser/state-preservation head: `07f89d13269041d9ed66de2362bf84c288bb86de`.

R6 receipt Verify run `32757986082`, job `97529853044`: **PASS**.

Accepted R7 candidate head: `79cf4e7a35844cb329c4459c81ef180b569e9e88`.

Candidate Verify run `32759637838`, job `97535149324`: **PASS**.

Lab 14 public integration gate: **32/32 checks PASS**, with zero page or console errors. Lab 13 public v1.3 regression: **26/26 PASS**. Complete responsive browser QA: **63/63 PASS**.

Candidate evidence artifact: `ai-playgrounds-verification-32759637838`, artifact ID `9532251591`, SHA-256 `5de6f569d552db9f0c12017cf4ba6fadd54fbedca3fb1b65d8af4966efe3a9e8`.

## 1. R7 release architecture

R7 promotes the frozen Lab 14 four-locale candidate into the deterministic public Pages artifact without altering the frozen Lab 14 state machine or semantic catalogs.

The public Lab 14 builder is:

`tools/build_agent_tool_context_public.py`

The v1.3 Pages builder is:

`tools/build_site_v1_3.py`

The public integration gate is:

`tools/test_agent_tool_context_public_integration.py`

The v1.3 release inventory is composed deterministically from the frozen thirteen-entry v1.2 manifest plus exactly one Lab 14 release record in `tools/applet_v1_3_lab14.json`. The deployed `_site/applets.json` therefore contains fourteen unique applets while the historical v1.2 and legacy source manifests remain unchanged.

## 2. Public Lab 14 boundary

The accepted public Lab 14 page remains:

- one self-contained HTML file;
- offline-ready after download;
- free of runtime fetch, XHR, WebSocket, EventSource, and external script dependencies;
- linked back to the AI Playgrounds suite;
- canonicalized to the public `agent-tool-context` route;
- discoverable through EN, ZH, VI, ES, and x-default alternate metadata;
- explicitly bound to the frozen R6 head in public metadata;
- free of non-public candidate wording.

Locale switching remains presentation-only and cannot mutate the frozen state machine, tool catalog, tool data, action history, permissions, provenance, or world state.

## 3. v1.3 deployment boundary

The deterministic v1.3 Pages artifact contains exactly fourteen public applets and 54 files. It adds only the Lab 14 public page relative to the v1.2 applet inventory; the twelve legacy source applets and Lab 13 remain present and unchanged in mechanism.

The landing catalogue, curriculum sequence, release-note banner, sitemap, citation metadata, CodeMeta metadata, README release status, and versioned release notes identify v1.3.0 and the fourteen-applet inventory.

The immutable v1.0.1 DOI-bearing release remains historical provenance and is not reassigned to v1.3.0.

## 4. Public integration acceptance matrix

`tools/test_agent_tool_context_public_integration.py` completed **32/32 checks**, covering:

1. fourteen unique deployed metadata entries;
2. Lab 14 course and showcase order 14;
3. the 54-file minimal Pages boundary;
4. public Lab 14 route existence;
5. removal of non-public candidate wording;
6. exact R6 freeze metadata binding;
7. canonical and four-locale alternate metadata;
8. one-file/offline operation;
9. suite navigation and v1.3 badge;
10. landing, curriculum, release-note, and sitemap integration;
11. query-parameter locale initialization;
12. eight scenarios and five Guided Challenges retained;
13. exact machine-state preservation across all four locales;
14. canonical 8 C to 46.4 F conversion and correct stop transition;
15. permission-denial behavior;
16. adversarial observation localization without sanitization or goal/principal mutation;
17. mobile root containment;
18. zero page and console errors.

The same exact candidate head also passed the rebound Lab 13 v1.3 public regression gate at **26/26**, the R6 four-locale gate at **48/48**, the complete inherited v1.2 and Lab 13 verification stack, all Lab 14 R0-R6 gates, the 45 algorithm regressions, and the **63/63** general browser/responsive matrix.

## 5. R7 candidate decision

**PASS.** The public v1.3 integration candidate at `79cf4e7a35844cb329c4459c81ef180b569e9e88` is accepted.

This audit update and the R6 receipt-status correction are documentation-only. The exact branch head containing them must receive one fresh complete permanent Verify PASS. If that run remains green without any code, semantic-catalog, runtime, deployment, or gate change, that exact head becomes the frozen R7 receipt head and the only head eligible for merge to `main`.

## 6. Release boundary

No v1.3.0 tag or GitHub release may be created before the receipt-bearing R7 head passes unchanged on the permanent Verify workflow, PR #20 is squash-merged once, and the resulting merged `main` head passes its push verification. The tag and release must then resolve exactly to that verified merged `main` commit.
