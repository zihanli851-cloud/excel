from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.core.database import SessionLocal, init_db  # noqa: E402
from app.services.excel_importer import ExcelImporter  # noqa: E402


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/import_excel.py <excel-file>")

    excel_path = Path(sys.argv[1]).resolve()
    if not excel_path.exists():
        raise SystemExit(f"Excel file not found: {excel_path}")

    init_db()
    with SessionLocal() as db:
        result = ExcelImporter(db).import_file(excel_path)
    print(json.dumps(result.model_dump(), indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
