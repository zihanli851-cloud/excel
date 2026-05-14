import type { ListData, MessageResponse } from './common'
import type { ProjectSearchRequest } from './project'

export interface QueryHistoryRead {
  id: number
  user_id?: number | null
  query_params: Partial<ProjectSearchRequest> & Record<string, unknown>
  result_count: number
  created_at: string
}

export interface QueryHistoryListResponse {
  success: boolean
  data: ListData<QueryHistoryRead>
}

export interface SaveQueryHistoryRequest {
  query_params: Record<string, unknown>
  result_count: number
}

export interface SaveQueryHistoryResponse extends MessageResponse {
  history_id: number
}
