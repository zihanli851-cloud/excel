from __future__ import annotations

from collections.abc import Iterable

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.models.project import Project


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def bulk_upsert(self, projects: Iterable[Project]) -> int:
        written = 0
        for project in projects:
            existing = self.db.scalar(select(Project).where(Project.row_hash == project.row_hash))
            if existing is None and project.project_code:
                existing = self.db.scalar(
                    select(Project).where(
                        Project.project_code == project.project_code,
                        Project.sheet_year == project.sheet_year,
                    )
                )

            if existing is None:
                self.db.add(project)
            else:
                self._copy_project(project, existing)
            written += 1

        self.db.commit()
        return written

    def get_by_id(self, project_id: int) -> Project | None:
        return self.db.get(Project, project_id)

    def list_by_ids(self, project_ids: list[int]) -> list[Project]:
        if not project_ids:
            return []
        stmt = select(Project).where(Project.id.in_(project_ids)).order_by(Project.id)
        return list(self.db.scalars(stmt).all())

    def list_purchasers(self) -> list[str]:
        stmt = select(Project.purchaser).where(Project.purchaser.is_not(None)).distinct().order_by(Project.purchaser)
        return [row[0] for row in self.db.execute(stmt).all() if row[0]]

    def count_invalid_by_reason(self) -> dict[str, int]:
        stmt = (
            select(Project.invalid_reason, func.count(Project.id))
            .where(Project.is_invalid.is_(True))
            .group_by(Project.invalid_reason)
        )
        return {reason or "OTHER": count for reason, count in self.db.execute(stmt).all()}

    def search_base_query(self) -> Select[tuple[Project]]:
        return select(Project)

    @staticmethod
    def _copy_project(source: Project, target: Project) -> None:
        for name in (
            "seq_no",
            "project_name",
            "project_code",
            "purchaser",
            "bid_open_date",
            "commission_amount",
            "commission_num",
            "max_price",
            "max_price_num",
            "bid_amount",
            "bid_amount_num",
            "bid_amount_detail",
            "sheet_year",
            "is_invalid",
            "invalid_reason",
            "source_file",
            "source_sheet",
            "source_row",
            "row_hash",
        ):
            setattr(target, name, getattr(source, name))
