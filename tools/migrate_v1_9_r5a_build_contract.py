#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "tools" / "build_current.py"
RELEASE = ROOT / "src" / "product" / "release.json"
R5A_PHASE = "v1.9-r5a-public-remainder-ownership"


def require_replace(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"R5a migration expected one {label} occurrence, found {count}")
    return text.replace(old, new, 1)


def main() -> None:
    release = json.loads(RELEASE.read_text(encoding="utf-8"))
    if release.get("architecture_phase") != "v1.9-r4b-token-owned-components":
        raise RuntimeError("R5a migration requires exact R4b release phase")
    release["architecture_phase"] = R5A_PHASE
    release["public_remainder_manifest"] = "src/product/public-remainder.json"
    release["public_remainder_count"] = 43
    release["canonical_existing_public_remainder_count"] = 29
    release["current_snapshot_public_remainder_count"] = 14
    release["historical_manifest_note"] = (
        "Historical applet sources, candidate builders, and release-layer transforms remain legacy equivalence/provenance inputs during R5a. "
        "Current applet-page authority is src/labs/*/index.template.html plus src/product/page-components.json; six shared components render from "
        "src/design/token-components.json and the DTCG token contract. The 43 non-applet public files are now canonically owned by "
        "src/product/public-remainder.json: byte-identical repository sources are reused where available and only transformed/generated current outputs "
        "are materialized under src/site/current. The historical builder remains a current-build witness until R5b."
    )
    RELEASE.write_text(json.dumps(release, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    text = BUILD.read_text(encoding="utf-8")
    text = require_replace(text, "import page_components\n", "import page_components\nimport public_remainder\n", "public_remainder import")
    text = require_replace(
        text,
        'R4B_EVIDENCE = ROOT / "release-evidence" / "v1.9-canonical-source-r4b.json"\n',
        'R4B_EVIDENCE = ROOT / "release-evidence" / "v1.9-canonical-source-r4b.json"\nR5A_EVIDENCE = ROOT / "release-evidence" / "v1.9-canonical-source-r5a.json"\n',
        "R5a evidence constant",
    )
    text = require_replace(text, 'CURRENT_PHASE = "v1.9-r4b-token-owned-components"', f'CURRENT_PHASE = "{R5A_PHASE}"', "current phase")
    text = require_replace(
        text,
        "    token_contract = design_tokens.validate_contract()\n",
        "    token_contract = design_tokens.validate_contract()\n    public_remainder_state = public_remainder.load_and_validate()\n",
        "public-remainder model load",
    )
    text = require_replace(text, 'raise RuntimeError("R4b must remain bound to exact public v1.8.1")', 'raise RuntimeError("R5a must remain bound to exact public v1.8.1")', "release error label")
    text = require_replace(text, 'raise RuntimeError("R4b baseline source SHA changed")', 'raise RuntimeError("R5a baseline source SHA changed")', "baseline error label")
    text = require_replace(text, 'raise RuntimeError("R4b public boundary must remain 58 files / 15 applets")', 'raise RuntimeError("R5a public boundary must remain 58 files / 15 applets")', "public-boundary error label")
    text = require_replace(text, 'raise RuntimeError("R4b curriculum track-count boundary changed")', 'raise RuntimeError("R5a curriculum track-count boundary changed")', "track error label")
    text = require_replace(text, 'raise RuntimeError("R4b learner locale order changed")', 'raise RuntimeError("R5a learner locale order changed")', "locale error label")
    text = require_replace(text, 'raise RuntimeError("R4b Quick Assign count changed")', 'raise RuntimeError("R5a Quick Assign count changed")', "quick-assign error label")

    release_field_anchor = '        "token_template_source_bytes": 19724,\n'
    release_field_insert = release_field_anchor + (
        '        "public_remainder_manifest": "src/product/public-remainder.json",\n'
        '        "public_remainder_count": 43,\n'
        '        "canonical_existing_public_remainder_count": 29,\n'
        '        "current_snapshot_public_remainder_count": 14,\n'
    )
    text = require_replace(text, release_field_anchor, release_field_insert, "R5a release fields")

    token_metrics_anchor = '    if token_templates.get("rendered_component_bytes") != 19050 or token_templates.get("token_template_bytes") != 19724:\n        raise RuntimeError("R4b token-template byte metrics drift")\n\n'
    token_metrics_insert = token_metrics_anchor + (
        '    if public_remainder_state.get("counts") != {"canonical_existing": 29, "current_snapshot": 14}:\n'
        '        raise RuntimeError("R5a public-remainder ownership count drift")\n'
        '    if len(public_remainder_state.get("public_paths", [])) != 43:\n'
        '        raise RuntimeError("R5a public-remainder path count drift")\n\n'
    )
    text = require_replace(text, token_metrics_anchor, token_metrics_insert, "R5a ownership assertions")

    return_anchor = '        "design_tokens": token_contract,\n'
    text = require_replace(text, return_anchor, return_anchor + '        "public_remainder": public_remainder_state,\n', "R5a model return")

    text = require_replace(
        text,
        "    # R4b still invokes the historical ladder strictly as an independent\n    # equivalence witness. Canonical token/template/page sources own final bytes\n    # only after exact equality has been proven. R5 removes this current-build\n    # dependency once the non-applet public remainder is canonically owned.\n",
        "    # R5a still invokes the historical ladder strictly as an independent\n    # equivalence witness. The complete 43-file non-applet remainder now has\n    # canonical source ownership; R5b removes this historical current-build\n    # dependency after direct 58-file composition is independently proven.\n",
        "R5a build comment",
    )

    # Once the current phase advances, R4b must remain a historical receipt.
    r4b_anchor = '    write_evidence(R4B_EVIDENCE, {\n        "phase": CURRENT_PHASE,\n'
    text = require_replace(text, r4b_anchor, '    write_evidence(R4B_EVIDENCE, {\n        "phase": "v1.9-r4b-token-owned-components",\n', "R4b evidence phase pin")

    evidence_anchor = '    if not comparison["pass"]:\n'
    evidence_block = '''    remainder_state = model["public_remainder"]
    write_evidence(R5A_EVIDENCE, {
        "phase": CURRENT_PHASE,
        "baseline_source_sha": BASELINE_SHA,
        "public_remainder_manifest": "src/product/public-remainder.json",
        "public_remainder_count": len(remainder_state["public_paths"]),
        "ownership_counts": remainder_state["counts"],
        "ownership_bytes": remainder_state["bytes"],
        "snapshot_public_paths": remainder_state["snapshot_public_paths"],
        "historical_builder_role": "independent-current-build-equivalence-witness-until-r5b",
        "model": common_model,
        "catalogue": catalogue_check,
        "artifact": comparison,
    })

'''
    text = require_replace(text, evidence_anchor, evidence_block + evidence_anchor, "R5a evidence block")
    text = require_replace(text, '"R4b current build differs from frozen v1.8.1 byte oracle: "', '"R5a current build differs from frozen v1.8.1 byte oracle: "', "R5a build error")
    text = require_replace(
        text,
        '"v1.9 R4b current build: PASS — six shared components render from DTCG token templates before canonical page/catalogue handoff; "',
        '"v1.9 R5a current build: PASS — 43 non-applet public files have canonical source ownership while the historical ladder remains an equivalence witness; "',
        "R5a build success message",
    )
    BUILD.write_text(text, encoding="utf-8")

    # Fail closed against the newly written contract.
    import sys
    sys.path.insert(0, str(ROOT / "tools"))
    import public_remainder
    public_remainder.load_and_validate()
    import build_current
    build_current.build_current()
    evidence = ROOT / "release-evidence" / "v1.9-canonical-source-r5a.json"
    if not evidence.is_file():
        raise RuntimeError("R5a current build did not emit its evidence receipt")
    print("R5a build contract migration: PASS")


if __name__ == "__main__":
    main()
