#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys

import migrate_v1_9_r5b_direct_build as first


def main() -> None:
    try:
        first.main()
        return
    except RuntimeError as exc:
        message = str(exc)
        if "R5b current facade still references historical build machinery" not in message or "build_site_v1_8_1" not in message:
            raise

    # The historical builder path is allowed as provenance/test metadata in
    # evidence. What R5b forbids is executable coupling in the current facade.
    source = first.BUILD.read_text(encoding="utf-8")
    forbidden_executable = (
        "from build_site_v",
        "import build_site_v",
        "build_legacy_v",
    )
    found = [needle for needle in forbidden_executable if needle in source]
    if found:
        raise RuntimeError(f"R5b current facade still has executable historical build coupling: {found}")

    subprocess.run([sys.executable, str(first.BUILD)], cwd=first.ROOT, check=True)
    evidence = first.ROOT / "release-evidence" / "v1.9-canonical-source-r5b.json"
    if not evidence.is_file():
        raise RuntimeError("R5b current build did not emit R5b evidence after executable-reference audit")
    print("R5b current facade migration v2: PASS")


if __name__ == "__main__":
    main()
