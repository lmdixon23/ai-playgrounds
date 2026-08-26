#!/usr/bin/env python3
from __future__ import annotations

"""Compatibility entry point for the v1.7.1 modern-lab parity QA.

The initial harness used a textual Quick Assign token count. Keep the workflow
name stable while delegating to the corrected DOM/start-tag-aware final gate.
"""

from test_v1_7_1_modern_parity_final import main


if __name__ == "__main__":
    raise SystemExit(main())
