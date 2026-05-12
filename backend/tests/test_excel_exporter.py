from __future__ import annotations

from datetime import date
from pathlib import Path

from openpyxl import load_workbook

from app.models.project import Project
from app.services.excel_exporter import export_projects


def test_export_projects_keeps_original_amount_text(monkeypatch) -> None:
    artifact_dir = Path("test_artifacts/exporter")
    artifact_dir.mkdir(parents=True, exist_ok=True)
    monkeypatch.chdir(artifact_dir)
    project = Project(
        id=1,
        seq_no=1,
        project_name="废标项目",
        project_code="P20260001",
        purchaser="采购人A",
        bid_open_date=date(2026, 5, 1),
        commission_amount="360.28万元",
        max_price="单价限价",
        bid_amount="投标人不足三家，废标",
        bid_amount_detail="",
        sheet_year=2026,
        is_invalid=True,
        invalid_reason="BID_FAILED",
        row_hash="hash",
    )

    result = export_projects([project], "test_export.xlsx")
    workbook = load_workbook(result.file_path)
    worksheet = workbook.active

    assert worksheet["A1"].value == "序号"
    assert worksheet["F2"].value == "360.28万元"
    assert worksheet["H2"].value == "投标人不足三家，废标"
    assert worksheet["J2"].value == "废标"
    assert worksheet["A2"].fill.fgColor.rgb in {"00FFFF00", "FFFFFF00", "FFFF00"}
