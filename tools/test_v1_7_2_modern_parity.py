#!/usr/bin/env python3
from __future__ import annotations

"""Stable workflow entry point for the v1.7.2 modern-lab parity QA."""

from test_v1_7_2_modern_metadata import main as metadata_main
from test_v1_7_2_modern_packet_labels import main as behavior_main
from test_v1_7_2_modern_parity_final import main as parity_main
from test_v1_7_2_modern_provenance import main as provenance_main
from test_v1_7_2_public_release import main as release_main


def main() -> int:
    # The release gate builds the exact artifact twice and checks deterministic
    # composition before every other gate inspects or drives that same output.
    for gate in (release_main, provenance_main, metadata_main, parity_main, behavior_main):
        result = gate()
        if result:
            return result
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
