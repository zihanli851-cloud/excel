from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.schemas.audit import AuditLogListData, AuditLogListParams, AuditLogRead
from app.schemas.common import PaginationMeta


class AuditService:
    def __init__(self, db: Session):
        self.db = db

    def log_action(
        self,
        action: str,
        *,
        user_id: int | None = None,
        detail: dict | None = None,
        ip_address: str | None = None,
    ) -> AuditLog:
        log = AuditLog(user_id=user_id, action=action, detail=detail, ip_address=ip_address)
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

    def list_logs(self, params: AuditLogListParams) -> AuditLogListData:
        stmt = select(AuditLog)
        if params.action:
            stmt = stmt.where(AuditLog.action == params.action)

        total = self.db.scalar(select(func.count()).select_from(stmt.order_by(None).subquery())) or 0
        stmt = stmt.order_by(AuditLog.created_at.desc()).offset((params.page - 1) * params.page_size).limit(params.page_size)
        items = [AuditLogRead.model_validate(item) for item in self.db.scalars(stmt).all()]
        return AuditLogListData(
            items=items,
            pagination=PaginationMeta(page=params.page, page_size=params.page_size, total=total),
        )

