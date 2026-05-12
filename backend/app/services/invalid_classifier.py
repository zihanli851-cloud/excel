from __future__ import annotations

from typing import Any

from app.services.amount_parser import normalize_text

INVALID_KEYWORDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("BID_FAILED", ("废标", "投标人不足", "有效投标人不足")),
    ("TERMINATED", ("终止采购", "供应商不足")),
    ("CANCELLED", ("采购任务取消", "重大变故")),
    ("WINNER_QUIT", ("放弃中标", "重新开展")),
    ("BREACH", ("无法履约", "自愿放弃签订")),
)


def classify_invalid_reason(text: Any, is_yellow: bool) -> str | None:
    normalized = normalize_text(text)
    for reason, keywords in INVALID_KEYWORDS:
        if any(keyword in normalized for keyword in keywords):
            return reason
    if is_yellow:
        return "OTHER"
    return None
