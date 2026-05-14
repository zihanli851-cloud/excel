import type { PaginationMeta } from './common'

export type AmountField = 'commission' | 'max_price' | 'bid_amount' | 'any'
export type InvalidMode = 'valid_only' | 'all' | 'invalid_only'
export type SortOrder = 'asc' | 'desc'
export type SortBy =
  | 'bid_open_date'
  | 'sheet_year'
  | 'project_code'
  | 'purchaser'
  | 'created_at'
  | 'project_name'

export type InvalidReason =
  | 'BID_FAILED'
  | 'TERMINATED'
  | 'CANCELLED'
  | 'WINNER_QUIT'
  | 'BREACH'
  | 'OTHER'

export interface ProjectRead {
  id: number
  seq_no?: number | null
  project_name: string
  project_code?: string | null
  purchaser?: string | null
  bid_open_date?: string | null
  commission_amount?: string | null
  commission_num?: string | null
  max_price?: string | null
  max_price_num?: string | null
  bid_amount?: string | null
  bid_amount_num?: string | null
  bid_amount_detail?: string | null
  sheet_year: number
  is_invalid: boolean
  invalid_reason?: InvalidReason | string | null
}

export interface ProjectSearchRequest {
  keyword?: string | null
  code?: string | null
  purchaser?: string | null
  date_from?: string | null
  date_to?: string | null
  amount_min?: number | null
  amount_max?: number | null
  amount_field: AmountField
  invalid_mode: InvalidMode
  invalid_reason?: string | null
  page: number
  page_size: number
  sort_by: SortBy
  sort_order: SortOrder
}

export interface ProjectSearchResponse {
  success: boolean
  data: {
    items: ProjectRead[]
    pagination: PaginationMeta
  }
}

export interface ProjectReviewRequest {
  comment?: string | null
}

export interface ProjectReviewResponse {
  success: boolean
  message: string
  project_id: number
}

export interface ExportByQueryRequest extends ProjectSearchRequest {
  file_name?: string | null
}

export interface ExportByIdsRequest {
  project_ids: number[]
  file_name?: string | null
}

export const invalidReasonOptions: Array<{ label: string; value: InvalidReason }> = [
  { label: '废标', value: 'BID_FAILED' },
  { label: '终止采购', value: 'TERMINATED' },
  { label: '采购取消', value: 'CANCELLED' },
  { label: '中标人放弃', value: 'WINNER_QUIT' },
  { label: '履约失败', value: 'BREACH' },
  { label: '其他', value: 'OTHER' },
]

export const amountFieldOptions: Array<{ label: string; value: AmountField }> = [
  { label: '任一金额', value: 'any' },
  { label: '委托金额', value: 'commission' },
  { label: '最高限价', value: 'max_price' },
  { label: '中标金额', value: 'bid_amount' },
]

export const invalidModeOptions: Array<{ label: string; value: InvalidMode }> = [
  { label: '仅有效', value: 'valid_only' },
  { label: '全部', value: 'all' },
  { label: '仅无效', value: 'invalid_only' },
]

export function createDefaultProjectSearch(pageSize = 20): ProjectSearchRequest {
  return {
    keyword: null,
    code: null,
    purchaser: null,
    date_from: null,
    date_to: null,
    amount_min: null,
    amount_max: null,
    amount_field: 'any',
    invalid_mode: 'valid_only',
    invalid_reason: null,
    page: 1,
    page_size: pageSize,
    sort_by: 'bid_open_date',
    sort_order: 'desc',
  }
}
