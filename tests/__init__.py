"""Test package initialisation ensuring project root is on ``sys.path``."""

import os
import sys

# Add repository root to module search path so tests can import project modules
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

