from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import MessageResponse, PaginationMeta


class QueryHistoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int | None = None
    query_params: dict
    result_count: int
    created_at: datetime


class QueryHistoryListData(BaseModel):
    items: list[QueryHistoryRead]
    pagination: PaginationMeta


class QueryHistoryListResponse(BaseModel):
    success: bool = True
    data: QueryHistoryListData


class SaveQueryHistoryRequest(BaseModel):
    query_params: dict
    result_count: int = Field(default=0, ge=0)


class SaveQueryHistoryResponse(MessageResponse):
    history_id: int

