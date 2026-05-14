import type { AuditLogListResponse } from '@/types/audit'
import type { CurrentUser, LoginRequest, LoginResponse } from '@/types/auth'
import type { ImportResponse } from '@/types/import'
import type { QueryHistoryListResponse } from '@/types/queryHistory'
import type {
  ProjectRead,
  ProjectReviewResponse,
  ProjectSearchRequest,
  ProjectSearchResponse,
} from '@/types/project'

export const isMockEnabled = import.meta.env.VITE_ENABLE_MOCK === 'true'

export const mockUser: CurrentUser = {
  id: 1,
  username: 'admin',
  display_name: '前端预览管理员',
  role: 'admin',
  is_active: true,
}

const mockProjects: ProjectRead[] = [
  {
    id: 1,
    seq_no: 1,
    project_name: '人民医院信息化升级采购项目',
    project_code: 'P202600001',
    purchaser: '市人民医院',
    bid_open_date: '2026-05-12',
    commission_amount: '360.28万元',
    commission_num: '360.28',
    max_price: '420万元',
    max_price_num: '420',
    bid_amount: '398.5万元',
    bid_amount_num: '398.5',
    bid_amount_detail: '一包：398.5万元',
    sheet_year: 2026,
    is_invalid: false,
    invalid_reason: null,
  },
  {
    id: 2,
    seq_no: 2,
    project_name: '学校智慧教室设备采购项目',
    project_code: 'P202600002',
    purchaser: '实验中学',
    bid_open_date: '2026-04-28',
    commission_amount: '120万元',
    commission_num: '120',
    max_price: '单价限价',
    max_price_num: null,
    bid_amount: '投标人不足三家，废标',
    bid_amount_num: null,
    bid_amount_detail: '',
    sheet_year: 2026,
    is_invalid: true,
    invalid_reason: 'BID_FAILED',
  },
  {
    id: 3,
    seq_no: 3,
    project_name: '政务服务中心办公家具采购项目',
    project_code: 'P202500088',
    purchaser: '政务服务中心',
    bid_open_date: '2025-11-18',
    commission_amount: '无',
    commission_num: null,
    max_price: '85万元',
    max_price_num: '85',
    bid_amount: '79.6万元',
    bid_amount_num: '79.6',
    bid_amount_detail: '一包：79.6万元',
    sheet_year: 2025,
    is_invalid: false,
    invalid_reason: null,
  },
  {
    id: 4,
    seq_no: 4,
    project_name: '公共卫生应急物资储备采购项目',
    project_code: 'P202500102',
    purchaser: '卫生健康局',
    bid_open_date: '2025-12-02',
    commission_amount: '260万元',
    commission_num: '260',
    max_price: '300万元',
    max_price_num: '300',
    bid_amount: '有效供应商不足三家，终止采购',
    bid_amount_num: null,
    bid_amount_detail: '',
    sheet_year: 2025,
    is_invalid: true,
    invalid_reason: 'TERMINATED',
  },
]

const now = new Date().toISOString()

export async function mockLogin(payload: LoginRequest): Promise<LoginResponse> {
  return {
    success: true,
    data: {
      access_token: `mock-token-${payload.username || 'admin'}`,
      token_type: 'bearer',
      user: {
        ...mockUser,
        username: payload.username || mockUser.username,
      },
    },
  }
}

export async function mockGetCurrentUser(): Promise<CurrentUser> {
  return mockUser
}

export async function mockSearchProjects(payload: ProjectSearchRequest): Promise<ProjectSearchResponse> {
  const filtered = mockProjects.filter((project) => {
    if (payload.keyword && !project.project_name.includes(payload.keyword)) return false
    if (payload.code && !project.project_code?.startsWith(payload.code)) return false
    if (payload.purchaser && project.purchaser !== payload.purchaser) return false
    if (payload.invalid_mode === 'valid_only' && project.is_invalid) return false
    if (payload.invalid_mode === 'invalid_only' && !project.is_invalid) return false
    if (payload.invalid_reason && project.invalid_reason !== payload.invalid_reason) return false
    return true
  })

  const start = (payload.page - 1) * payload.page_size
  const items = filtered.slice(start, start + payload.page_size)

  return {
    success: true,
    data: {
      items,
      pagination: {
        page: payload.page,
        page_size: payload.page_size,
        total: filtered.length,
      },
    },
  }
}

export async function mockGetProjectDetail(projectId: number): Promise<ProjectRead> {
  return mockProjects.find((item) => item.id === projectId) || mockProjects[0]
}

export async function mockReviewProject(projectId: number): Promise<ProjectReviewResponse> {
  return {
    success: true,
    message: 'Mock review recorded',
    project_id: projectId,
  }
}

export async function mockExportFile() {
  return {
    data: new Blob(['mock export file'], {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    }),
    headers: {
      'content-disposition': "attachment; filename*=UTF-8''mock-export.xlsx",
    },
  }
}

export async function mockGetPurchasers(): Promise<string[]> {
  return ['市人民医院', '实验中学', '政务服务中心', '卫生健康局']
}

export async function mockGetInvalidStats(): Promise<Record<string, number>> {
  return {
    BID_FAILED: 1,
    TERMINATED: 1,
    CANCELLED: 0,
    WINNER_QUIT: 0,
    BREACH: 0,
    OTHER: 0,
  }
}

export async function mockUploadExcel(file: File): Promise<ImportResponse> {
  return {
    success: true,
    data: {
      file_name: file.name,
      total_rows: 423,
      imported_rows: 423,
      valid_rows: 336,
      invalid_rows: 87,
      skipped_rows: 0,
      sheet_stats: [
        {
          sheet_name: '2026年',
          sheet_year: 2026,
          total_rows: 423,
          imported_rows: 423,
          invalid_rows: 87,
        },
      ],
      warnings: [
        {
          sheet: '说明',
          row: null,
          field: null,
          message: 'Mock 模式：未真正上传文件，仅用于前端预览。',
        },
      ],
    },
  }
}

export async function mockGetAuditLogs(page: number, pageSize: number): Promise<AuditLogListResponse> {
  const items = [
    {
      id: 1,
      user_id: 1,
      action: 'login',
      detail: { username: 'admin' },
      ip_address: '127.0.0.1',
      created_at: now,
    },
    {
      id: 2,
      user_id: 1,
      action: 'search_projects',
      detail: { query: { invalid_mode: 'valid_only' }, result_count: 2 },
      ip_address: '127.0.0.1',
      created_at: now,
    },
  ]

  return {
    success: true,
    data: {
      items: items.slice((page - 1) * pageSize, page * pageSize),
      pagination: { page, page_size: pageSize, total: items.length },
    },
  }
}

export async function mockGetQueryHistory(): Promise<QueryHistoryListResponse> {
  return {
    success: true,
    data: {
      items: [
        {
          id: 1,
          user_id: 1,
          query_params: {
            keyword: '医院',
            amount_field: 'any',
            invalid_mode: 'valid_only',
            page: 1,
            page_size: 20,
            sort_by: 'bid_open_date',
            sort_order: 'desc',
          },
          result_count: 1,
          created_at: now,
        },
        {
          id: 2,
          user_id: 1,
          query_params: {
            invalid_mode: 'invalid_only',
            invalid_reason: 'BID_FAILED',
            amount_field: 'any',
            page: 1,
            page_size: 20,
            sort_by: 'bid_open_date',
            sort_order: 'desc',
          },
          result_count: 1,
          created_at: now,
        },
      ],
      pagination: { page: 1, page_size: 20, total: 2 },
    },
  }
}
