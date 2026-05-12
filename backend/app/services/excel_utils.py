from __future__ import annotations

import re
import unicodedata
from datetime import date, datetime
from typing import Any

EXPECTED_HEADERS: dict[str, str] = {
    "序号": "seq_no",
    "项目名称": "project_name",
    "项目编号": "project_code",
    "采购人": "purchaser",
    "开标时间": "bid_open_date",
    "委托金额(万元)合计": "commission_amount",
    "最高限价(万元)(分包)": "max_price",
    "中标金额(万元)合计": "bid_amount",
    "中标金额(万元)(分包)": "bid_amount_detail",
}

YELLOW_RGB_VALUES = {"FFFF00", "FFFFFF00", "FFFF99", "FFFFFF99", "FFF2CC", "FFFFF2CC"}


def normalize_header(value: Any) -> str:
    text = "" if value is None else str(value)
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\n", "").replace("\r", "").replace(" ", "").strip()
    return text.replace("（", "(").replace("）", ")")


def parse_sheet_year(sheet_name: str) -> int | None:
    match = re.search(r"(19|20)\d{2}", sheet_name)
    if match is None:
        return None
    return int(match.group(0))


def parse_date(value: Any) -> date | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value

    text = unicodedata.normalize("NFKC", str(value).strip())
    if not text:
        return None
    text = text.replace(".", "-").replace("/", "-").replace("年", "-").replace("月", "-").replace("日", "")
    text = re.sub(r"\s+", "", text)
    for fmt in ("%Y-%m-%d", "%Y-%m", "%Y%m%d"):
        try:
            parsed = datetime.strptime(text, fmt)
            return parsed.date()
        except ValueError:
            continue
    return None


def find_header_row(worksheet: Any, max_scan_rows: int = 20) -> tuple[int, dict[str, int], list[str]]:
    for row_index in range(1, min(worksheet.max_row, max_scan_rows) + 1):
        mapping: dict[str, int] = {}
        extra_headers: list[str] = []
        for cell in worksheet[row_index]:
            normalized = normalize_header(cell.value)
            if normalized in EXPECTED_HEADERS:
                mapping[EXPECTED_HEADERS[normalized]] = cell.column
            elif normalized:
                extra_headers.append(str(cell.value).strip())

        if "project_name" in mapping and "project_code" in mapping:
            missing = [field for field in EXPECTED_HEADERS.values() if field not in mapping]
            if missing:
                raise ValueError(f"表头缺少字段: {', '.join(missing)}")
            return row_index, mapping, extra_headers

    raise ValueError("未找到项目清单表头")


def is_yellow_cell(cell: Any) -> bool:
    fill = getattr(cell, "fill", None)
    if fill is None or getattr(fill, "fill_type", None) is None:
        return False

    color = getattr(fill, "fgColor", None)
    rgb = getattr(color, "rgb", None)
    if not rgb:
        return False

    normalized = str(rgb).upper()
    if normalized in YELLOW_RGB_VALUES:
        return True
    if len(normalized) == 8:
        normalized = normalized[2:]
    if len(normalized) != 6:
        return False

    try:
        red = int(normalized[0:2], 16)
        green = int(normalized[2:4], 16)
        blue = int(normalized[4:6], 16)
    except ValueError:
        return False
    return red >= 220 and green >= 200 and blue <= 180


def is_yellow_row(cells: list[Any]) -> bool:
    return any(is_yellow_cell(cell) for cell in cells)


def is_empty_values(values: list[Any]) -> bool:
    return all(value is None or str(value).strip() == "" for value in values)
