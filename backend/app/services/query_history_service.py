from __future__ import annotations

from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from app.models.query_history import QueryHistory
from app.schemas.common import PaginationMeta
from app.schemas.query_history import QueryHistoryListData, QueryHistoryRead


class QueryHistoryService:
    def __init__(self, db: Session):
        self.db = db

    def create_history(self, *, user_id: int | None, query_params: dict, result_count: int) -> QueryHistory:
        history = QueryHistory(user_id=user_id, query_params=query_params, result_count=result_count)
        self.db.add(history)
        self.db.commit()
        self.db.refresh(history)
        return history

    def list_history(self, *, user_id: int | None, page: int, page_size: int) -> QueryHistoryListData:
        stmt = select(QueryHistory)
        if user_id is not None:
            stmt = stmt.where(QueryHistory.user_id == user_id)

        total = self.db.scalar(select(func.count()).select_from(stmt.order_by(None).subquery())) or 0
        stmt = stmt.order_by(QueryHistory.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
        items = [QueryHistoryRead.model_validate(item) for item in self.db.scalars(stmt).all()]
        return QueryHistoryListData(
            items=items,
            pagination=PaginationMeta(page=page, page_size=page_size, total=total),
        )

    def delete_history(self, *, history_id: int, user_id: int | None) -> bool:
        stmt = delete(QueryHistory).where(QueryHistory.id == history_id)
        if user_id is not None:
            stmt = stmt.where(QueryHistory.user_id == user_id)
        result = self.db.execute(stmt)
        self.db.commit()
        return result.rowcount > 0

