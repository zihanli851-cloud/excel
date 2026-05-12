from __future__ import annotations

import re
import unicodedata
from decimal import Decimal, InvalidOperation
from typing import Any

NUMBER_RE = re.compile(r"[-+]?\d+(?:\.\d+)?")


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    text = unicodedata.normalize("NFKC", text)
    return text.replace("\u3000", " ").strip()


def parse_amount(value: Any) -> Decimal | None:
    text = normalize_text(value)
    if not text:
        return None

    compact = text.replace(",", "").replace("，", "")
    match = NUMBER_RE.search(compact)
    if match is None:
        return None

    try:
        return Decimal(match.group(0))
    except InvalidOperation:
        return None
