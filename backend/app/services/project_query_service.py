from __future__ import annotations

from decimal import Decimal

from sqlalchemy import Select, func, or_, select
from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.common import PaginationMeta
from app.schemas.project import ProjectRead
from app.schemas.project_query import ProjectSearchData, ProjectSearchRequest
from app.services.audit_service import AuditService
from app.services.project_repository import ProjectRepository
from app.services.query_history_service import QueryHistoryService


SORT_FIELDS = {
    "bid_open_date": Project.bid_open_date,
    "sheet_year": Project.sheet_year,
    "project_code": Project.project_code,
    "purchaser": Project.purchaser,
    "created_at": Project.created_at,
    "project_name": Project.project_name,
}


class ProjectQueryService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = ProjectRepository(db)
        self.audit_service = AuditService(db)
        self.history_service = QueryHistoryService(db)

    def search_projects(
        self,
        payload: ProjectSearchRequest,
        *,
        user_id: int | None,
        record_history: bool = True,
        record_audit: bool = True,
    ) -> ProjectSearchData:
        stmt = self._build_filtered_stmt(payload)
        total = self.db.scalar(select(func.count()).select_from(stmt.order_by(None).subquery())) or 0

        sort_column = SORT_FIELDS[payload.sort_by]
        order_by = sort_column.asc() if payload.sort_order == "asc" else sort_column.desc()
        stmt = stmt.order_by(order_by, Project.id.desc()).offset((payload.page - 1) * payload.page_size).limit(payload.page_size)
        items = [ProjectRead.model_validate(item) for item in self.db.scalars(stmt).all()]

        if record_history:
            self.history_service.create_history(
                user_id=user_id,
                query_params=payload.model_dump(mode="json", exclude_none=True),
                result_count=total,
            )
        if record_audit:
            self.audit_service.log_action(
                "search_projects",
                user_id=user_id,
                detail={"query": payload.model_dump(mode="json", exclude_none=True), "result_count": total},
            )

        return ProjectSearchData(
            items=items,
            pagination=PaginationMeta(page=payload.page, page_size=payload.page_size, total=total),
        )

    def collect_projects_for_export(self, payload: ProjectSearchRequest, *, user_id: int | None) -> list[Project]:
        stmt = self._build_filtered_stmt(payload)
        sort_column = SORT_FIELDS[payload.sort_by]
        order_by = sort_column.asc() if payload.sort_order == "asc" else sort_column.desc()
        projects = list(self.db.scalars(stmt.order_by(order_by, Project.id.desc())).all())
        self.audit_service.log_action(
            "export_projects_by_query",
            user_id=user_id,
            detail={"query": payload.model_dump(mode="json", exclude_none=True), "result_count": len(projects)},
        )
        return projects

    def _build_filtered_stmt(self, payload: ProjectSearchRequest) -> Select[tuple[Project]]:
        stmt = self.repository.search_base_query()

        if payload.keyword:
            stmt = stmt.where(Project.project_name.contains(payload.keyword))
        if payload.code:
            stmt = stmt.where(Project.project_code.like(f"{payload.code}%"))
        if payload.purchaser:
            stmt = stmt.where(Project.purchaser == payload.purchaser)
        if payload.date_from:
            stmt = stmt.where(Project.bid_open_date >= payload.date_from)
        if payload.date_to:
            stmt = stmt.where(Project.bid_open_date <= payload.date_to)

        if payload.invalid_mode == "valid_only":
            stmt = stmt.where(Project.is_invalid.is_(False))
        elif payload.invalid_mode == "invalid_only":
            stmt = stmt.where(Project.is_invalid.is_(True))

        if payload.invalid_reason:
            stmt = stmt.where(Project.invalid_reason == payload.invalid_reason)

        if payload.amount_min is not None or payload.amount_max is not None:
            stmt = stmt.where(self._amount_clause(payload.amount_field, payload.amount_min, payload.amount_max))

        return stmt

    @staticmethod
    def _amount_clause(field: str, amount_min: Decimal | None, amount_max: Decimal | None):
        columns = {
            "commission": [Project.commission_num],
            "max_price": [Project.max_price_num],
            "bid_amount": [Project.bid_amount_num],
            "any": [Project.commission_num, Project.max_price_num, Project.bid_amount_num],
        }[field]

        conditions = []
        for column in columns:
            local = []
            if amount_min is not None:
                local.append(column >= amount_min)
            if amount_max is not None:
                local.append(column <= amount_max)
            if local:
                conditions.append(local[0] if len(local) == 1 else local[0] & local[1])

        return or_(*conditions)
