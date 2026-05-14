import { ref } from 'vue'
import { defineStore } from 'pinia'

import { getInvalidStats, getPurchasers } from '@/api/metadata'

export const useMetadataStore = defineStore('metadata', () => {
  const purchasers = ref<string[]>([])
  const invalidStats = ref<Record<string, number>>({})
  const loadingPurchasers = ref(false)
  const loadingStats = ref(false)

  async function loadPurchasers(force = false) {
    if (!force && purchasers.value.length > 0) return purchasers.value
    loadingPurchasers.value = true
    try {
      purchasers.value = await getPurchasers()
      return purchasers.value
    } finally {
      loadingPurchasers.value = false
    }
  }

  async function loadInvalidStats(force = false) {
    if (!force && Object.keys(invalidStats.value).length > 0) return invalidStats.value
    loadingStats.value = true
    try {
      invalidStats.value = await getInvalidStats()
      return invalidStats.value
    } finally {
      loadingStats.value = false
    }
  }

  return {
    purchasers,
    invalidStats,
    loadingPurchasers,
    loadingStats,
    loadPurchasers,
    loadInvalidStats,
  }
})
