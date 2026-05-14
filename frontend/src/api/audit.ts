import http from './http'
import { isMockEnabled, mockGetAuditLogs } from './mock'

import type { AuditLogListParams, AuditLogListResponse } from '@/types/audit'

export async function getAuditLogs(params: AuditLogListParams) {
  if (isMockEnabled) {
    return mockGetAuditLogs(params.page, params.page_size)
  }
  const { data } = await http.get<AuditLogListResponse>('/audit/logs', { params })
  return data
}
