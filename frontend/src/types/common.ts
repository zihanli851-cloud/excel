export interface PaginationMeta {
  page: number
  page_size: number
  total: number
}

export interface MessageResponse {
  success: boolean
  message: string
}

export interface ListData<T> {
  items: T[]
  pagination: PaginationMeta
}
