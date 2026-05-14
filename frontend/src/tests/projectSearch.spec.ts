import { beforeEach, describe, expect, it } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'

import { useProjectSearchStore } from '@/stores/projectSearch'

describe('project search store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('uses valid_only as the default invalid mode', () => {
    const store = useProjectSearchStore()
    expect(store.filters.invalid_mode).toBe('valid_only')
    expect(store.filters.amount_field).toBe('any')
  })

  it('resets filters to defaults', () => {
    const store = useProjectSearchStore()
    store.filters.keyword = '医院'
    store.filters.invalid_mode = 'all'

    store.resetFilters()

    expect(store.filters.keyword).toBeNull()
    expect(store.filters.invalid_mode).toBe('valid_only')
  })

  it('applies history and resets to first page', () => {
    const store = useProjectSearchStore()
    store.applyHistory({
      keyword: '学校',
      invalid_mode: 'invalid_only',
      page: 3,
    })

    expect(store.filters.keyword).toBe('学校')
    expect(store.filters.invalid_mode).toBe('invalid_only')
    expect(store.filters.page).toBe(1)
  })
})
