from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.core.database import init_db  # noqa: E402


if __name__ == "__main__":
    init_db()
    print("Database initialized.")
    print(f"Reference SQL migration: {ROOT / 'migrations' / '001_initial_schema.sql'}")
