from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", status_code=501)
def login_placeholder() -> dict[str, str]:
    return {"message": "登录认证由后端 B 实现，后端 A 仅预留路径"}
