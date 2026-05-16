from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session, sessionmaker

from fastapi import HTTPException

from app.api.deps import require_admin
from app.core.database import Base
from app.models.audit_log import AuditLog
from app.models.project import Project
from app.models.user import User
from app.models.query_history import QueryHistory
from app.schemas.project_query import ProjectSearchRequest
from app.services.auth_service import AuthService
from app.services.project_query_service import ProjectQueryService
from app.services.query_history_service import QueryHistoryService


def _make_session() -> Session:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
    return SessionLocal()


def test_auth_service_bootstraps_default_user_and_token() -> None:
    with _make_session() as db:
        service = AuthService(db)
        user = service.ensure_default_user()

        assert user.username == "admin"

        authenticated = service.authenticate("admin", "admin123456")
        assert authenticated is not None

        token = service.create_access_token(authenticated)
        token_user = service.get_user_from_token(token)
        assert token_user is not None
        assert token_user.id == authenticated.id


def test_project_query_service_records_history_and_audit() -> None:
    with _make_session() as db:
        user = AuthService(db).ensure_default_user()
        _seed_projects(db)

        service = ProjectQueryService(db)
        payload = ProjectSearchRequest(
            purchaser="采购人A",
            amount_min=Decimal("100"),
            amount_max=Decimal("130"),
            amount_field="any",
            invalid_mode="valid_only",
            sort_by="project_name",
            sort_order="asc",
            page=1,
            page_size=10,
        )

        result = service.search_projects(payload, user_id=user.id)

        assert result.pagination.total == 1
        assert len(result.items) == 1
        assert result.items[0].project_name == "医院项目A"

        history_count = db.scalar(select(func.count()).select_from(QueryHistory))
        audit_count = db.scalar(select(func.count()).select_from(AuditLog))
        assert history_count == 1
        assert audit_count == 1

        export_projects = service.collect_projects_for_export(payload, user_id=user.id)
        assert len(export_projects) == 1
        audit_count_after_export = db.scalar(select(func.count()).select_from(AuditLog))
        assert audit_count_after_export == 2


def test_project_search_defaults_to_valid_only() -> None:
    payload = ProjectSearchRequest()

    assert payload.invalid_mode == "valid_only"


def test_require_admin_allows_admin_user() -> None:
    user = User(username="admin", password_hash="hash", role="admin", is_active=True)

    assert require_admin(user) is user


def test_require_admin_rejects_viewer_user() -> None:
    user = User(username="viewer", password_hash="hash", role="viewer", is_active=True)

    try:
        require_admin(user)
    except HTTPException as exc:
        assert exc.status_code == 403
        assert exc.detail == "Admin role required"
    else:
        raise AssertionError("viewer should not pass admin dependency")


def test_query_history_service_deletes_only_owned_history() -> None:
    with _make_session() as db:
        user = AuthService(db).ensure_default_user()
        history = QueryHistoryService(db).create_history(
            user_id=user.id,
            query_params={"keyword": "医院"},
            result_count=3,
        )

        deleted = QueryHistoryService(db).delete_history(history_id=history.id, user_id=user.id)
        assert deleted is True
        assert db.get(QueryHistory, history.id) is None


def _seed_projects(db: Session) -> None:
    db.add_all(
        [
            Project(
                seq_no=1,
                project_name="医院项目A",
                project_code="P20230001",
                purchaser="采购人A",
                bid_open_date=date(2023, 1, 10),
                commission_amount="120",
                commission_num=Decimal("120"),
                max_price="130",
                max_price_num=Decimal("130"),
                bid_amount="110",
                bid_amount_num=Decimal("110"),
                bid_amount_detail="",
                sheet_year=2023,
                is_invalid=False,
                invalid_reason=None,
                source_file="demo.xlsx",
                source_sheet="2023年",
                source_row=2,
                row_hash="row-1",
            ),
            Project(
                seq_no=2,
                project_name="学校项目B",
                project_code="P20230002",
                purchaser="采购人A",
                bid_open_date=date(2023, 2, 15),
                commission_amount="80",
                commission_num=Decimal("80"),
                max_price="90",
                max_price_num=Decimal("90"),
                bid_amount="废标",
                bid_amount_num=None,
                bid_amount_detail="",
                sheet_year=2023,
                is_invalid=True,
                invalid_reason="BID_FAILED",
                source_file="demo.xlsx",
                source_sheet="2023年",
                source_row=3,
                row_hash="row-2",
            ),
            Project(
                seq_no=3,
                project_name="道路项目C",
                project_code="P20230003",
                purchaser="采购人B",
                bid_open_date=date(2023, 3, 20),
                commission_amount="200",
                commission_num=Decimal("200"),
                max_price="210",
                max_price_num=Decimal("210"),
                bid_amount="205",
                bid_amount_num=Decimal("205"),
                bid_amount_detail="",
                sheet_year=2023,
                is_invalid=False,
                invalid_reason=None,
                source_file="demo.xlsx",
                source_sheet="2023年",
                source_row=4,
                row_hash="row-3",
            ),
        ]
    )
    db.commit()
