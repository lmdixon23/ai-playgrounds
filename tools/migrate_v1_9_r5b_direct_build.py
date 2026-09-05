#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "tools" / "build_current.py"
CURRENT_PHASE = "v1.9-r5b-direct-canonical-build"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"R5b migration expected one {label}, found {count}")
    return text.replace(old, new, 1)


def main() -> None:
    text = BUILD.read_text(encoding="utf-8")

    text = replace_once(
        text,
        "from build_site_v1_8_1 import build_site as build_legacy_v181\n",
        "",
        "historical builder import",
    )
    text = replace_once(
        text,
        "import design_tokens\n",
        "import design_tokens\nimport direct_current_site\n",
        "direct composer import",
    )
    text = replace_once(
        text,
        'R5A_EVIDENCE = ROOT / "release-evidence" / "v1.9-canonical-source-r5a.json"\n',
        'R5A_EVIDENCE = ROOT / "release-evidence" / "v1.9-canonical-source-r5a.json"\nR5B_EVIDENCE = ROOT / "release-evidence" / "v1.9-canonical-source-r5b.json"\n',
        "R5b evidence constant",
    )
    text = replace_once(
        text,
        'CURRENT_PHASE = "v1.9-r5a-public-remainder-ownership"',
        f'CURRENT_PHASE = "{CURRENT_PHASE}"',
        "current architecture phase",
    )

    for old, new in (
        ("R5a must remain bound to exact public v1.8.1", "R5b must remain bound to exact public v1.8.1"),
        ("R5a baseline source SHA changed", "R5b baseline source SHA changed"),
        ("R5a public boundary must remain 58 files / 15 applets", "R5b public boundary must remain 58 files / 15 applets"),
        ("R5a curriculum track-count boundary changed", "R5b curriculum track-count boundary changed"),
        ("R5a learner locale order changed", "R5b learner locale order changed"),
        ("R5a Quick Assign count changed", "R5b Quick Assign count changed"),
    ):
        text = replace_once(text, old, new, old)

    release_anchor = '        "current_snapshot_public_remainder_count": 14,\n'
    text = replace_once(
        text,
        release_anchor,
        release_anchor
        + '        "direct_current_build": True,\n'
        + '        "current_build_composer": "tools/direct_current_site.py",\n'
        + '        "historical_builder_role": "test-only-regression-and-provenance",\n',
        "R5b release source fields",
    )

    # Legacy handoff functions are no longer valid concepts in a direct build.
    handoff_start = text.find("\ndef handoff_catalogue(")
    write_evidence_start = text.find("\ndef write_evidence(")
    if handoff_start < 0 or write_evidence_start < 0 or write_evidence_start <= handoff_start:
        raise RuntimeError("R5b migration could not isolate legacy handoff functions")
    text = text[:handoff_start] + "\n" + text[write_evidence_start:]

    build_start = text.find("def build_current() -> None:\n")
    main_start = text.find('\n\nif __name__ == "__main__":')
    if build_start < 0 or main_start < 0 or main_start <= build_start:
        raise RuntimeError("R5b migration could not isolate build_current function")

    new_build = r'''def build_current() -> None:
    model = validate_product_model()

    # R5b current output is composed directly from canonical current sources.
    # Historical release builders remain regression/provenance inputs only and
    # are neither imported nor invoked by this facade.
    direct = direct_current_site.build_direct(SITE)
    catalogue_check = validate_emitted_catalogue(model)
    comparison = compare_to_oracle(artifact_hashes())
    if not direct["artifact"]["pass"] or not comparison["pass"]:
        raise RuntimeError(
            "R5b direct current build differs from frozen v1.8.1 byte oracle: "
            f"added={comparison['added']}, removed={comparison['removed']}, changed={comparison['changed']}"
        )

    common_model = {
        "lab_count": model["lab_count"],
        "foundation_count": model["foundation_count"],
        "modern_extension_count": model["modern_extension_count"],
        "quick_assign_count": model["quick_assign_count"],
        "slugs": model["slugs"],
    }

    write_evidence(R0_EVIDENCE, {
        "phase": "v1.9-r0-equivalence",
        "baseline_source_sha": BASELINE_SHA,
        "representation": "historical-equivalence-milestone-preserved-under-direct-current-build",
        "legacy_builder": "tools/build_site_v1_8_1.py",
        "legacy_builder_role": "test-only-regression-and-provenance",
        "canonical_facade": "tools/build_current.py",
        "model": common_model,
        "catalogue": catalogue_check,
        "artifact": comparison,
    })
    write_evidence(R1_EVIDENCE, {
        "phase": "v1.9-r1-canonical-catalogue",
        "baseline_source_sha": BASELINE_SHA,
        "representation": "historical-r1-ownership-preserved-under-direct-current-build",
        "canonical_catalogue": "src/product/catalogue.json",
        "canonical_catalogue_sha256": model["catalogue"]["sha256"],
        "serializer_roundtrip": model["catalogue"]["serializer_roundtrip"],
        "model": common_model,
        "catalogue": catalogue_check,
        "artifact": comparison,
    })

    peer_pages = {slug: model["page_components"]["page_evidence"][slug] for slug in R2_PEER_SLUGS}
    write_evidence(R2_EVIDENCE, {
        "phase": "v1.9-r2-peer-current-pages",
        "baseline_source_sha": BASELINE_SHA,
        "representation": "superseded-by-r3-template-component-composition",
        "canonical_catalogue": "src/product/catalogue.json",
        "peer_current_pages": {"pages": peer_pages, "pass": True},
        "model": common_model,
        "catalogue": catalogue_check,
        "artifact": comparison,
    })
    write_evidence(R3_EVIDENCE, {
        "phase": "v1.9-r3-shared-page-components",
        "baseline_source_sha": BASELINE_SHA,
        "representation": "superseded-by-r4b-token-template-component-source",
        "canonical_catalogue": "src/product/catalogue.json",
        "canonical_page_component_manifest": "src/product/page-components.json",
        "page_component_metrics": model["page_components"]["metrics"],
        "component_count": len(model["page_components"]["components"]),
        "canonical_pages": model["page_components"]["page_evidence"],
        "model": common_model,
        "catalogue": catalogue_check,
        "artifact": comparison,
    })

    token_contract = model["design_tokens"]
    write_evidence(R4A_EVIDENCE, {
        "phase": "v1.9-r4a-design-token-contract",
        "baseline_source_sha": BASELINE_SHA,
        "representation": "preserved-through-r4b-rendered-component-bindings",
        "design_token_contract": "src/design/ai-playgrounds.tokens.json",
        "design_token_bindings": "src/design/current-bindings.json",
        "design_token_schema": token_contract["schema"],
        "design_token_format": token_contract["format"],
        "token_count": token_contract["token_count"],
        "alias_count": token_contract["alias_count"],
        "type_counts": token_contract["type_counts"],
        "theme_profiles": {
            "profiles": token_contract["theme_profiles"]["profiles"],
            "slugs": token_contract["theme_profiles"]["slugs"],
            "checks": token_contract["theme_profiles"]["checks"],
            "pass": token_contract["theme_profiles"]["pass"],
        },
        "accent_bindings": {
            "slugs": token_contract["accents"]["slugs"],
            "checks": token_contract["accents"]["checks"],
            "minimaxMismatchPreserved": token_contract["accents"]["minimaxMismatchPreserved"],
            "pass": token_contract["accents"]["pass"],
        },
        "component_literal_bindings": {
            "bindings": token_contract["component_literal_bindings"]["bindings"],
            "source_model": token_contract["component_literal_bindings"]["source_model"],
            "pass": token_contract["component_literal_bindings"]["pass"],
        },
        "page_graph": token_contract["page_graph"],
        "model": common_model,
        "catalogue": catalogue_check,
        "artifact": comparison,
    })

    source_kinds = model["page_components"]["component_source_kinds"]
    write_evidence(R4B_EVIDENCE, {
        "phase": "v1.9-r4b-token-owned-components",
        "baseline_source_sha": BASELINE_SHA,
        "token_component_manifest": "src/design/token-components.json",
        "token_template_component_count": token_contract["token_template_bindings"]["components"],
        "token_template_binding_count": token_contract["token_template_bindings"]["bindings"],
        "rendered_component_bytes": token_contract["token_template_bindings"]["rendered_component_bytes"],
        "token_template_bytes": token_contract["token_template_bindings"]["token_template_bytes"],
        "component_source_kinds": {
            "raw": sum(1 for value in source_kinds.values() if value == "raw"),
            "token-template": sum(1 for value in source_kinds.values() if value == "token-template"),
        },
        "rendered_component_literal_bindings": {
            "bindings": token_contract["component_literal_bindings"]["bindings"],
            "pass": token_contract["component_literal_bindings"]["pass"],
        },
        "token_template_bindings": {
            "components": token_contract["token_template_bindings"]["components"],
            "bindings": token_contract["token_template_bindings"]["bindings"],
            "pass": token_contract["token_template_bindings"]["pass"],
        },
        "page_graph": token_contract["page_graph"],
        "minimaxMismatchPreserved": token_contract["accents"]["minimaxMismatchPreserved"],
        "model": common_model,
        "catalogue": catalogue_check,
        "artifact": comparison,
    })

    remainder_state = model["public_remainder"]
    write_evidence(R5A_EVIDENCE, {
        "phase": "v1.9-r5a-public-remainder-ownership",
        "baseline_source_sha": BASELINE_SHA,
        "public_remainder_manifest": "src/product/public-remainder.json",
        "public_remainder_count": len(remainder_state["public_paths"]),
        "ownership_counts": remainder_state["counts"],
        "ownership_bytes": remainder_state["bytes"],
        "snapshot_public_paths": remainder_state["snapshot_public_paths"],
        "historical_builder_role": "independent-current-build-equivalence-witness-until-r5b",
        "representation": "historical-r5a-ownership-receipt-preserved-after-direct-build-cutover",
        "model": common_model,
        "catalogue": catalogue_check,
        "artifact": comparison,
    })

    write_evidence(R5B_EVIDENCE, {
        "phase": CURRENT_PHASE,
        "baseline_source_sha": BASELINE_SHA,
        "direct_current_build": True,
        "current_build_composer": "tools/direct_current_site.py",
        "historical_builder_role": "test-only-regression-and-provenance",
        "historical_builder_imported_by_current_facade": False,
        "public_remainder_emission": {
            "file_count": direct["remainder"]["file_count"],
            "bytes": direct["remainder"]["bytes"],
            "pass": direct["remainder"]["pass"],
        },
        "applet_page_emission": {
            "file_count": direct["pages"]["file_count"],
            "pass": direct["pages"]["pass"],
        },
        "total_public_file_count": direct["artifact"]["actual_files"],
        "model": common_model,
        "catalogue": catalogue_check,
        "artifact": comparison,
    })

    print(
        "v1.9 R5b current build: PASS — direct canonical composition emits 43 remainder + 15 applet pages; "
        f"{comparison['actual_files']} files remain byte-identical to frozen v1.8.1"
    )
'''

    text = text[:build_start] + new_build + text[main_start:]
    BUILD.write_text(text, encoding="utf-8")

    source = BUILD.read_text(encoding="utf-8")
    forbidden = (
        "from build_site_v",
        "import build_site_v",
        "build_legacy_v",
        "build_site_v1_8_1",
    )
    found = [needle for needle in forbidden if needle in source]
    if found:
        raise RuntimeError(f"R5b current facade still references historical build machinery: {found}")

    subprocess.run([sys.executable, str(BUILD)], cwd=ROOT, check=True)
    evidence = ROOT / "release-evidence" / "v1.9-canonical-source-r5b.json"
    if not evidence.is_file():
        raise RuntimeError("R5b current build did not emit R5b evidence")
    print("R5b current facade migration: PASS")


if __name__ == "__main__":
    main()
