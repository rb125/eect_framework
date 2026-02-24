import os
import sys

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_dir)
sys.path.insert(0, os.path.join(root_dir, 'src'))

from eect_api import app  # noqa: E402,F401

# Vercel entry point for the EECT FastAPI app.
