"""Ensure tools/ is on sys.path for unittest discovery without PYTHONPATH."""

import sys
from pathlib import Path

_TOOLS_DIR = Path(__file__).resolve().parents[1] / "tools"
if str(_TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(_TOOLS_DIR))
