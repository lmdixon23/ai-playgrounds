#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys

import migrate_v1_9_r5a_build_contract as first


def main() -> None:
    try:
        first.main()
        return
    except RuntimeError as exc:
        expected = "R4b page-component phase drift: 'v1.9-r4b-token-owned-components'"
        if expected not in str(exc):
            raise

    # R5a advances the product-level architecture phase only. The canonical
    # page graph is still the accepted R4b token-owned component subgraph and
    # therefore must remain explicitly pinned to its own phase.
    text = first.BUILD.read_text(encoding="utf-8")
    old = '    if pages.get("phase") != CURRENT_PHASE:\n        raise RuntimeError(f"R4b page-component phase drift: {pages.get(\'phase\')!r}")\n'
    new = '    if pages.get("phase") != "v1.9-r4b-token-owned-components":\n        raise RuntimeError(f"R4b page-component phase drift: {pages.get(\'phase\')!r}")\n'
    if text.count(old) != 1:
        raise RuntimeError("R5a phase-decoupling patch did not find exactly one page-phase assertion")
    first.BUILD.write_text(text.replace(old, new, 1), encoding="utf-8")

    subprocess.run([sys.executable, str(first.BUILD)], cwd=first.ROOT, check=True)
    evidence = first.ROOT / "release-evidence" / "v1.9-canonical-source-r5a.json"
    if not evidence.is_file():
        raise RuntimeError("R5a current build did not emit its evidence receipt after phase decoupling")
    print("R5a build contract migration v2: PASS")


if __name__ == "__main__":
    main()
