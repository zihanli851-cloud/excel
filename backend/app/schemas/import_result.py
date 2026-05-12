from __future__ import annotations

from pydantic import BaseModel, Field


class ImportWarning(BaseModel):
    sheet: str | None = None
    row: int | None = None
    field: str | None = None
    message: str


class SheetImportStat(BaseModel):
    sheet_name: str
    sheet_year: int
    total_rows: int = 0
    imported_rows: int = 0
    invalid_rows: int = 0


class ImportResult(BaseModel):
    file_name: str
    total_rows: int = 0
    imported_rows: int = 0
    valid_rows: int = 0
    invalid_rows: int = 0
    skipped_rows: int = 0
    sheet_stats: list[SheetImportStat] = Field(default_factory=list)
    warnings: list[ImportWarning] = Field(default_factory=list)


class ApiResponse(BaseModel):
    success: bool
    data: ImportResult
