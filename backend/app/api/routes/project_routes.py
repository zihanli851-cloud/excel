from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.export import ExportRequest
from app.schemas.project import ProjectRead
from app.services.excel_exporter import export_projects
from app.services.project_repository import ProjectRepository

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/export")
def export_project_results(payload: ExportRequest, db: Session = Depends(get_db)) -> FileResponse:
    projects = ProjectRepository(db).list_by_ids(payload.project_ids)
    result = export_projects(projects, payload.file_name)
    return FileResponse(
        path=result.file_path,
        filename=result.file_name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, db: Session = Depends(get_db)) -> ProjectRead:
    project = ProjectRepository(db).get_by_id(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="项目不存在")
    return ProjectRead.model_validate(project)


@router.post("/{project_id}/review", status_code=501)
def review_project(project_id: int) -> dict[str, str | int]:
    return {"message": "复核接口由后端 B 实现，后端 A 仅预留路径", "project_id": project_id}
