from __future__ import annotations

import shutil
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.config import get_settings
from app.schemas.import_result import ApiResponse
from app.services.excel_importer import ExcelImporter

router = APIRouter(prefix="/import", tags=["import"])


@router.post("/upload", response_model=ApiResponse)
def upload_excel(file: UploadFile = File(...), db: Session = Depends(get_db)) -> ApiResponse:
    if not file.filename or not file.filename.lower().endswith((".xlsx", ".xlsm")):
        raise HTTPException(status_code=400, detail="仅支持 .xlsx 或 .xlsm 文件")

    settings = get_settings()
    settings.upload_path.mkdir(parents=True, exist_ok=True)
    safe_name = Path(file.filename).name
    target = settings.upload_path / safe_name

    with target.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    importer = ExcelImporter(db)
    result = importer.import_file(target)
    return ApiResponse(success=True, data=result)
