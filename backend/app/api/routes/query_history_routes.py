from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/query-history", tags=["query-history"])


@router.get("", status_code=501)
def query_history_placeholder() -> dict[str, str]:
    return {"message": "查询历史接口由后端 B 实现，后端 A 仅预留路径"}


@router.delete("/{history_id}", status_code=501)
def delete_query_history_placeholder(history_id: int) -> dict[str, str | int]:
    return {"message": "查询历史删除由后端 B 实现，后端 A 仅预留路径", "history_id": history_id}
