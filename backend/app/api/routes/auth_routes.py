from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.auth import CurrentUserRead, LoginData, LoginRequest, LoginResponse
from app.services.audit_service import AuditService
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, request: Request, db: Session = Depends(get_db)) -> LoginResponse:
    auth_service = AuthService(db)
    user = auth_service.authenticate(payload.username, payload.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    AuditService(db).log_action(
        "login",
        user_id=user.id,
        detail={"username": user.username},
        ip_address=request.client.host if request.client else None,
    )
    token = auth_service.create_access_token(user)
    return LoginResponse(data=LoginData(access_token=token, user=CurrentUserRead.model_validate(user)))


@router.get("/me", response_model=CurrentUserRead)
def read_current_user(current_user: User = Depends(get_current_user)) -> CurrentUserRead:
    return CurrentUserRead.model_validate(current_user)
