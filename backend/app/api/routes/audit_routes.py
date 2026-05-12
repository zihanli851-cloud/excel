from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.audit import AuditLogListParams, AuditLogListResponse
from app.services.audit_service import AuditService

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("/logs", response_model=AuditLogListResponse)
def list_audit_logs(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    action: str | None = None,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AuditLogListResponse:
    params = AuditLogListParams(page=page, page_size=page_size, action=action)
    return AuditLogListResponse(data=AuditService(db).list_logs(params))
