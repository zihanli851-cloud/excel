from __future__ import annotations

from decimal import Decimal

from app.services.amount_parser import parse_amount


def test_parse_amount_numeric_text() -> None:
    assert parse_amount("360.28万元") == Decimal("360.28")
    assert parse_amount("约 50 万元") == Decimal("50")
    assert parse_amount("1,200.50") == Decimal("1200.50")
    assert parse_amount("１２３.４５万元") == Decimal("123.45")


def test_parse_amount_empty_or_text() -> None:
    assert parse_amount(None) is None
    assert parse_amount("") is None
    assert parse_amount("无") is None
    assert parse_amount("单价限价") is None
    assert parse_amount("废标") is None
