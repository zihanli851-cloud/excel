import { describe, expect, it } from 'vitest'

import { highlightKeyword } from '@/utils/highlight'

describe('highlight utils', () => {
  it('returns original escaped text without keyword', () => {
    expect(highlightKeyword('<项目>', '')).toBe('&lt;项目&gt;')
  })

  it('highlights keyword occurrences', () => {
    const output = highlightKeyword('人民医院建设项目', '医院')
    expect(output).toContain('<mark class="keyword-highlight">医院</mark>')
  })
})
