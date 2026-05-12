from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.export import ExportRequest
from app.schemas.project import ProjectRead
from app.schemas.project_query import (
    ExportByQueryRequest,
    ProjectReviewRequest,
    ProjectReviewResponse,
    ProjectSearchRequest,
    ProjectSearchResponse,
)
from app.services.audit_service import AuditService
from app.services.excel_exporter import export_projects
from app.services.project_query_service import ProjectQueryService
from app.services.project_repository import ProjectRepository

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/search", response_model=ProjectSearchResponse)
def search_projects(
    payload: ProjectSearchRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ProjectSearchResponse:
    data = ProjectQueryService(db).search_projects(payload, user_id=current_user.id)
    return ProjectSearchResponse(data=data)


@router.post("/export")
def export_project_results(
    payload: ExportRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> FileResponse:
    projects = ProjectRepository(db).list_by_ids(payload.project_ids)
    AuditService(db).log_action(
        "export_projects_by_ids",
        user_id=current_user.id,
        detail={"project_ids": payload.project_ids, "count": len(projects)},
    )
    result = export_projects(projects, payload.file_name)
    return FileResponse(
        path=result.file_path,
        filename=result.file_name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@router.post("/export-by-query")
def export_project_results_by_query(
    payload: ExportByQueryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> FileResponse:
    projects = ProjectQueryService(db).collect_projects_for_export(payload, user_id=current_user.id)
    result = export_projects(projects, payload.file_name)
    return FileResponse(
        path=result.file_path,
        filename=result.file_name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ProjectRead:
    project = ProjectRepository(db).get_by_id(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    AuditService(db).log_action("get_project_detail", user_id=current_user.id, detail={"project_id": project_id})
    return ProjectRead.model_validate(project)


@router.post("/{project_id}/review", response_model=ProjectReviewResponse)
def review_project(
    project_id: int,
    payload: ProjectReviewRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ProjectReviewResponse:
    project = ProjectRepository(db).get_by_id(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    AuditService(db).log_action(
        "review_project",
        user_id=current_user.id,
        detail={"project_id": project_id, "comment": payload.comment},
    )
    return ProjectReviewResponse(message="Project review recorded", project_id=project_id)
