from __future__ import annotations

from pydantic import BaseModel, Field


class PaginationMeta(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1)
    total: int = Field(default=0, ge=0)


class MessageResponse(BaseModel):
    success: bool = True
    message: str

