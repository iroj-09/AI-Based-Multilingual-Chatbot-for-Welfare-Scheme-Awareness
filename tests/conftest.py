import sys
from pathlib import Path

# Make backend modules (config, services, models, ...) importable in tests.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))
