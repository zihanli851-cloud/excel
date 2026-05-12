from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("/logs", status_code=501)
def audit_logs_placeholder() -> dict[str, str]:
    return {"message": "审计日志接口由后端 B 实现，后端 A 仅预留路径"}
