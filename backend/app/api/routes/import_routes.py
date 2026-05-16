from __future__ import annotations

import shutil
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_admin
from app.core.config import get_settings
from app.models.user import User
from app.schemas.import_result import ApiResponse
from app.services.audit_service import AuditService
from app.services.excel_importer import ExcelImporter

router = APIRouter(prefix="/import", tags=["import"])


@router.post("/upload", response_model=ApiResponse)
def upload_excel(
    file: UploadFile = File(...),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
) -> ApiResponse:
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
    AuditService(db).log_action(
        "import_excel",
        user_id=current_user.id,
        detail={
            "file_name": result.file_name,
            "total_rows": result.total_rows,
            "imported_rows": result.imported_rows,
            "valid_rows": result.valid_rows,
            "invalid_rows": result.invalid_rows,
            "warning_count": len(result.warnings),
        },
    )
    return ApiResponse(success=True, data=result)
