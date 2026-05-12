from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.common import MessageResponse, PaginationMeta
from app.schemas.project import ProjectRead

AmountField = Literal["commission", "max_price", "bid_amount", "any"]
InvalidMode = Literal["valid_only", "all", "invalid_only"]
SortOrder = Literal["asc", "desc"]
SortBy = Literal["bid_open_date", "sheet_year", "project_code", "purchaser", "created_at", "project_name"]


class ProjectSearchRequest(BaseModel):
    keyword: str | None = None
    code: str | None = None
    purchaser: str | None = None
    date_from: date | None = None
    date_to: date | None = None
    amount_min: Decimal | None = None
    amount_max: Decimal | None = None
    amount_field: AmountField = "any"
    invalid_mode: InvalidMode = "all"
    invalid_reason: str | None = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    sort_by: SortBy = "bid_open_date"
    sort_order: SortOrder = "desc"


class ProjectSearchData(BaseModel):
    items: list[ProjectRead]
    pagination: PaginationMeta


class ProjectSearchResponse(BaseModel):
    success: bool = True
    data: ProjectSearchData


class ExportByQueryRequest(ProjectSearchRequest):
    file_name: str | None = None


class ProjectReviewRequest(BaseModel):
    comment: str | None = Field(default=None, max_length=1000)


class ProjectReviewResponse(MessageResponse):
    project_id: int

