#!/usr/bin/env python3
from __future__ import annotations

"""Stable workflow entry point for the v1.7.1 modern-lab parity QA."""

from test_v1_7_1_modern_metadata import main as metadata_main
from test_v1_7_1_modern_parity_final import main as parity_main
from test_v1_7_1_modern_provenance import main as provenance_main


def main() -> int:
    for gate in (parity_main, provenance_main, metadata_main):
        result = gate()
        if result:
            return result
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
