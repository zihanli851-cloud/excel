from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import PaginationMeta


class AuditLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int | None = None
    action: str
    detail: dict | None = None
    ip_address: str | None = None
    created_at: datetime


class AuditLogListData(BaseModel):
    items: list[AuditLogRead]
    pagination: PaginationMeta


class AuditLogListResponse(BaseModel):
    success: bool = True
    data: AuditLogListData


class AuditLogListParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    action: str | None = None

