# v1.9 R6a — Canonical Quick Assign Registry

## Purpose

R6a gives the current product one canonical Quick Assign registry without changing any learner-facing byte, activity ID, prompt, locale, state behavior, privacy boundary, or release identity.

This milestone is a bounded continuation of issue 47 after R5b. It addresses registry ownership only. Locale consolidation, release-metadata consolidation, support-page decomposition, and visible redesign remain separate work.

## Source authority

The current Quick Assign source is:

`src/product/quick-assigns.json`

It owns:

- the 15 stable Level-1 activity IDs;
- the one-to-one lab slug mapping;
- permanent classroom anchors;
- the Predict / Run / Observe / Explain / Transfer sequence;
- activity titles and objectives;
- teacher-facing success criteria;
- active status and EN/ZH/VI/ES locale declarations.

`src/product/labs.json` continues to bind each canonical lab to exactly one Quick Assign ID. The current build rejects any membership, ID, slug, anchor, status, locale, or field-boundary drift.

## Historical handoff

`tools/quick_assigns_v2.json` remains available only to the versioned v1.7/v1.8 builder and verification stack. Its frozen SHA-256 is:

`9c94549a36e72ba465b08ed1df703b3482d3a6ff72c47893bdb5660497eacc51`

The R6a gate proves that the canonical duration, inquiry sequence, and 15 activity records are semantically identical to that historical source. The direct current build does not open or depend on the historical registry.

The canonical R6a registry SHA-256 is:

`5e3c79dd905dd701dbbf475ec2621abf903d0ca9c230b07694eea904f5302552`

## Generated-product bindings

After the direct current build completes, the R6a validator requires:

- one and only one `data-quick-assign-id` surface in each matching applet;
- one and only one stable Quick Assign anchor in each matching applet;
- all 15 IDs and canonical classroom links in `teacher-pack.html`;
- all 15 IDs and canonical classroom links in `curriculum.html`;
- each canonical English title and objective exactly once in `curriculum.html`;
- each canonical English title and teacher criterion exactly once in `teacher-pack.html`.

These 150 checks bind the registry's identifiers and English semantics to the exact frozen public artifact instead of treating it as disconnected documentation.

## Frozen public boundary

R6a preserves:

- public release `v1.8.1`;
- 15 applets;
- 58 deployed files;
- 13 Foundations and 2 Modern extensions;
- 15 active Level-1 Quick Assigns;
- EN/ZH/VI/ES learner locale order;
- self-contained/offline applet operation;
- local-only learner responses;
- all frozen public SHA-256 values.

Two current builds from one SHA must remain byte-identical and match the complete v1.8.1 oracle.

## Evidence and permanent gate

`tools/test_v1_9_canonical_quick_assign_registry_r6a.py` verifies the canonical schema, historical handoff, fail-closed field rules, current-build independence, lab membership, generated applet/support-page bindings, inherited R4b/R5a/R5b architecture invariants, repeat-build determinism, and the 58-file oracle.

`release-evidence/v1.9-canonical-source-r6a.json` records the canonical digest, declared historical digest and role, activity/locale/sequence boundaries, emitted-surface checks, model counts, and artifact comparison.

The dedicated canonical-source workflow runs R6a as the top-level architecture gate while retaining the R0–R5b receipts.

## Durable source surface

R6a changes only:

- the canonical registry;
- its validator;
- the current build facade and release metadata;
- the permanent gate and workflow;
- the R6a architecture document and generated evidence receipt;
- the existing Quick Assign architecture document's source-of-truth note.

No applet template, shared component, public support page, algorithm implementation, localization catalogue, historical builder, or frozen oracle is edited.

## Remaining issue 47 work

After R6a, issue 47 remains open for:

- one canonical current learner-locale registry;
- one explicit current release/version metadata owner;
- decomposition of the 14 support-page/current snapshots into shared current primitives where useful.

Visible redesign remains deferred to issue 48.
