from __future__ import annotations

from app.services.invalid_classifier import classify_invalid_reason


def test_classify_keyword_reasons() -> None:
    assert classify_invalid_reason("投标人不足三家，废标", False) == "BID_FAILED"
    assert classify_invalid_reason("有效供应商不足三家，终止采购", False) == "TERMINATED"
    assert classify_invalid_reason("因重大变故，采购任务取消", False) == "CANCELLED"
    assert classify_invalid_reason("中标人放弃中标，重新开展采购活动", False) == "WINNER_QUIT"
    assert classify_invalid_reason("因中标人无法履约，自愿放弃签订", False) == "BREACH"


def test_classify_other_and_valid() -> None:
    assert classify_invalid_reason("备注说明", True) == "OTHER"
    assert classify_invalid_reason("正常中标", False) is None
