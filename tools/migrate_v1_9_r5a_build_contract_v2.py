#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys

import migrate_v1_9_r5a_build_contract as first

R4B_PHASE = "v1.9-r4b-token-owned-components"


def patch_exact(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"R5a phase-decoupling expected one {label}, found {count}")
    return text.replace(old, new, 1)


def main() -> None:
    try:
        first.main()
        return
    except RuntimeError as exc:
        expected = f"R4b page-component phase drift: '{R4B_PHASE}'"
        if expected not in str(exc):
            raise

    # R5a advances only the product-level architecture phase. The canonical
    # page graph and design-binding graph remain accepted R4b subgraphs and
    # therefore keep their own explicit phase identities.
    text = first.BUILD.read_text(encoding="utf-8")
    text = patch_exact(
        text,
        '    if pages.get("phase") != CURRENT_PHASE:\n        raise RuntimeError(f"R4b page-component phase drift: {pages.get(\'phase\')!r}")\n',
        f'    if pages.get("phase") != "{R4B_PHASE}":\n        raise RuntimeError(f"R4b page-component phase drift: {{pages.get(\'phase\')!r}}")\n',
        "page-component phase assertion",
    )
    text = patch_exact(
        text,
        '    if token_contract.get("binding_phase") != CURRENT_PHASE:\n        raise RuntimeError(f"R4b design binding phase drift: {token_contract.get(\'binding_phase\')!r}")\n',
        f'    if token_contract.get("binding_phase") != "{R4B_PHASE}":\n        raise RuntimeError(f"R4b design binding phase drift: {{token_contract.get(\'binding_phase\')!r}}")\n',
        "design-binding phase assertion",
    )
    first.BUILD.write_text(text, encoding="utf-8")

    subprocess.run([sys.executable, str(first.BUILD)], cwd=first.ROOT, check=True)
    evidence = first.ROOT / "release-evidence" / "v1.9-canonical-source-r5a.json"
    if not evidence.is_file():
        raise RuntimeError("R5a current build did not emit its evidence receipt after phase decoupling")
    print("R5a build contract migration v2: PASS")


if __name__ == "__main__":
    main()
