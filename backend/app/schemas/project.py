from __future__ import annotations

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ProjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    seq_no: int | None = None
    project_name: str
    project_code: str | None = None
    purchaser: str | None = None
    bid_open_date: date | None = None
    commission_amount: str | None = None
    commission_num: Decimal | None = None
    max_price: str | None = None
    max_price_num: Decimal | None = None
    bid_amount: str | None = None
    bid_amount_num: Decimal | None = None
    bid_amount_detail: str | None = None
    sheet_year: int
    is_invalid: bool
    invalid_reason: str | None = None
