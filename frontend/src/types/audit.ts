import type { ListData } from './common'

export interface AuditLogRead {
  id: number
  user_id?: number | null
  action: string
  detail?: Record<string, unknown> | null
  ip_address?: string | null
  created_at: string
}

export interface AuditLogListResponse {
  success: boolean
  data: ListData<AuditLogRead>
}

export interface AuditLogListParams {
  page: number
  page_size: number
  action?: string | null
}
