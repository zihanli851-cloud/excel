from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel


class ExportRequest(BaseModel):
    project_ids: list[int]
    file_name: str | None = None


class ExportResult(BaseModel):
    file_name: str
    file_path: Path
    row_count: int
