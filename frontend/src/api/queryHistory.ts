import http from './http'
import { isMockEnabled, mockGetQueryHistory } from './mock'

import type {
  QueryHistoryListResponse,
  SaveQueryHistoryRequest,
  SaveQueryHistoryResponse,
} from '@/types/queryHistory'

export async function getQueryHistory(page = 1, pageSize = 20) {
  if (isMockEnabled) {
    void page
    void pageSize
    return mockGetQueryHistory()
  }
  const { data } = await http.get<QueryHistoryListResponse>('/query-history', {
    params: { page, page_size: pageSize },
  })
  return data
}

export async function saveQueryHistory(payload: SaveQueryHistoryRequest) {
  if (isMockEnabled) {
    void payload
    return { success: true, message: 'Mock query history saved', history_id: 999 }
  }
  const { data } = await http.post<SaveQueryHistoryResponse>('/query-history', payload)
  return data
}

export async function deleteQueryHistory(historyId: number) {
  if (isMockEnabled) {
    void historyId
    return { success: true, message: 'Mock query history deleted' }
  }
  const { data } = await http.delete(`/query-history/${historyId}`)
  return data
}
