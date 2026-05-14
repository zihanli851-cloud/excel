import dayjs from 'dayjs'

import type { InvalidMode, InvalidReason, ProjectSearchRequest } from '@/types/project'

const invalidReasonLabels: Record<string, string> = {
  BID_FAILED: '废标',
  TERMINATED: '终止采购',
  CANCELLED: '采购取消',
  WINNER_QUIT: '中标人放弃',
  BREACH: '履约失败',
  OTHER: '其他',
}

const invalidModeLabels: Record<InvalidMode, string> = {
  valid_only: '仅有效',
  all: '全部',
  invalid_only: '仅无效',
}

const amountFieldLabels: Record<string, string> = {
  any: '任一金额',
  commission: '委托金额',
  max_price: '最高限价',
  bid_amount: '中标金额',
}

export function displayText(value: unknown, fallback = '-') {
  if (value === null || value === undefined || value === '') {
    return fallback
  }
  return String(value)
}

export function formatDate(value?: string | null) {
  if (!value) {
    return '-'
  }
  const parsed = dayjs(value)
  return parsed.isValid() ? parsed.format('YYYY-MM-DD') : value
}

export function formatDateTime(value?: string | null) {
  if (!value) {
    return '-'
  }
  const parsed = dayjs(value)
  return parsed.isValid() ? parsed.format('YYYY-MM-DD HH:mm:ss') : value
}

export function invalidReasonLabel(value?: string | null) {
  return value ? invalidReasonLabels[value] || value : '-'
}

export function invalidModeLabel(value?: InvalidMode | null) {
  return value ? invalidModeLabels[value] : '-'
}

export function amountFieldLabel(value?: string | null) {
  return value ? amountFieldLabels[value] || value : '-'
}

export function querySummary(query: Partial<ProjectSearchRequest> & Record<string, unknown>) {
  const parts: string[] = []

  if (query.keyword) parts.push(`名称:${query.keyword}`)
  if (query.code) parts.push(`编号:${query.code}`)
  if (query.purchaser) parts.push(`采购人:${query.purchaser}`)
  if (query.date_from || query.date_to) parts.push(`日期:${query.date_from || '不限'} 至 ${query.date_to || '不限'}`)
  if (query.amount_min !== null && query.amount_min !== undefined) parts.push(`金额>=${query.amount_min}`)
  if (query.amount_max !== null && query.amount_max !== undefined) parts.push(`金额<=${query.amount_max}`)
  if (query.amount_field && query.amount_field !== 'any') parts.push(amountFieldLabel(String(query.amount_field)))
  if (query.invalid_mode) parts.push(invalidModeLabel(query.invalid_mode as InvalidMode))
  if (query.invalid_reason) parts.push(invalidReasonLabel(query.invalid_reason as InvalidReason))

  return parts.length > 0 ? parts.join('，') : '默认查询'
}
