from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Boolean, Date, DateTime, Integer, Numeric, SmallInteger, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Project(Base):
    __tablename__ = "projects"
    __table_args__ = (
        UniqueConstraint("project_code", "sheet_year", name="uq_projects_code_year"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    seq_no: Mapped[int | None] = mapped_column(Integer, nullable=True)
    project_name: Mapped[str] = mapped_column(Text, nullable=False)
    project_code: Mapped[str | None] = mapped_column(String(50), index=True, nullable=True)
    purchaser: Mapped[str | None] = mapped_column(Text, index=True, nullable=True)
    bid_open_date: Mapped[date | None] = mapped_column(Date, index=True, nullable=True)
    commission_amount: Mapped[str | None] = mapped_column(Text, nullable=True)
    commission_num: Mapped[Decimal | None] = mapped_column(Numeric(18, 4), nullable=True)
    max_price: Mapped[str | None] = mapped_column(Text, nullable=True)
    max_price_num: Mapped[Decimal | None] = mapped_column(Numeric(18, 4), nullable=True)
    bid_amount: Mapped[str | None] = mapped_column(Text, nullable=True)
    bid_amount_num: Mapped[Decimal | None] = mapped_column(Numeric(18, 4), nullable=True)
    bid_amount_detail: Mapped[str | None] = mapped_column(Text, nullable=True)
    sheet_year: Mapped[int] = mapped_column(SmallInteger, index=True, nullable=False)
    is_invalid: Mapped[bool] = mapped_column(Boolean, index=True, nullable=False, default=False)
    invalid_reason: Mapped[str | None] = mapped_column(String(50), index=True, nullable=True)
    source_file: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source_sheet: Mapped[str | None] = mapped_column(String(100), nullable=True)
    source_row: Mapped[int | None] = mapped_column(Integer, nullable=True)
    row_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
