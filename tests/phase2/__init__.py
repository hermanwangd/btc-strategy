"""Tests for the Phase-2 acceptance harness."""

import sys
from pathlib import Path

_TOOLS_DIR = Path(__file__).resolve().parents[2] / "tools"
if str(_TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(_TOOLS_DIR))

