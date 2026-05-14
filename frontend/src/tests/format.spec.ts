import { describe, expect, it } from 'vitest'

import {
  amountFieldLabel,
  displayText,
  formatDate,
  invalidModeLabel,
  invalidReasonLabel,
  querySummary,
} from '@/utils/format'

describe('format utils', () => {
  it('formats empty text with fallback', () => {
    expect(displayText(null)).toBe('-')
    expect(displayText('')).toBe('-')
    expect(displayText('项目A')).toBe('项目A')
  })

  it('formats date values', () => {
    expect(formatDate('2026-05-13')).toBe('2026-05-13')
    expect(formatDate(null)).toBe('-')
  })

  it('maps labels for enums', () => {
    expect(invalidReasonLabel('BID_FAILED')).toBe('废标')
    expect(invalidModeLabel('valid_only')).toBe('仅有效')
    expect(amountFieldLabel('max_price')).toBe('最高限价')
  })

  it('builds query summary', () => {
    const summary = querySummary({
      keyword: '医院',
      purchaser: '某采购人',
      invalid_mode: 'invalid_only',
    })
    expect(summary).toContain('名称:医院')
    expect(summary).toContain('采购人:某采购人')
    expect(summary).toContain('仅无效')
  })
})
