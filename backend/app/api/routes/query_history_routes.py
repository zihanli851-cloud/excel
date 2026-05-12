from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.common import MessageResponse
from app.schemas.query_history import (
    QueryHistoryListResponse,
    SaveQueryHistoryRequest,
    SaveQueryHistoryResponse,
)
from app.services.audit_service import AuditService
from app.services.query_history_service import QueryHistoryService

router = APIRouter(prefix="/query-history", tags=["query-history"])


@router.get("", response_model=QueryHistoryListResponse)
def list_query_history(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> QueryHistoryListResponse:
    data = QueryHistoryService(db).list_history(user_id=current_user.id, page=page, page_size=page_size)
    return QueryHistoryListResponse(data=data)


@router.post("", response_model=SaveQueryHistoryResponse)
def create_query_history(
    payload: SaveQueryHistoryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SaveQueryHistoryResponse:
    history = QueryHistoryService(db).create_history(
        user_id=current_user.id,
        query_params=payload.query_params,
        result_count=payload.result_count,
    )
    AuditService(db).log_action(
        "save_query_history",
        user_id=current_user.id,
        detail={"history_id": history.id, "result_count": history.result_count},
    )
    return SaveQueryHistoryResponse(message="Query history saved", history_id=history.id)


@router.delete("/{history_id}", response_model=MessageResponse)
def delete_query_history(
    history_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> MessageResponse:
    deleted = QueryHistoryService(db).delete_history(history_id=history_id, user_id=current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Query history not found")
    AuditService(db).log_action(
        "delete_query_history",
        user_id=current_user.id,
        detail={"history_id": history_id},
    )
    return MessageResponse(message="Query history deleted")
