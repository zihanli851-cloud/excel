from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.project_repository import ProjectRepository

router = APIRouter(tags=["metadata"])


@router.get("/purchasers", response_model=list[str])
def list_purchasers(db: Session = Depends(get_db)) -> list[str]:
    return ProjectRepository(db).list_purchasers()


@router.get("/stats/invalid", response_model=dict[str, int])
def invalid_stats(db: Session = Depends(get_db)) -> dict[str, int]:
    return ProjectRepository(db).count_invalid_by_reason()
