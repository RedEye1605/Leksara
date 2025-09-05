# Ensure repository root is on sys.path so the local 'leksara' package can be imported during tests.
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, os.pardir))
if REPO not in sys.path:
    sys.path.insert(0, REPO)
