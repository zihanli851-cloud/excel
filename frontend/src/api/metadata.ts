import http from './http'
import { isMockEnabled, mockGetInvalidStats, mockGetPurchasers } from './mock'

export async function getPurchasers() {
  if (isMockEnabled) {
    return mockGetPurchasers()
  }
  const { data } = await http.get<string[]>('/purchasers')
  return data
}

export async function getInvalidStats() {
  if (isMockEnabled) {
    return mockGetInvalidStats()
  }
  const { data } = await http.get<Record<string, number>>('/stats/invalid')
  return data
}
