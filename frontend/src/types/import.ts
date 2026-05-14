export interface ImportWarning {
  sheet?: string | null
  row?: number | null
  field?: string | null
  message: string
}

export interface SheetImportStat {
  sheet_name: string
  sheet_year: number
  total_rows: number
  imported_rows: number
  invalid_rows: number
}

export interface ImportResult {
  file_name: string
  total_rows: number
  imported_rows: number
  valid_rows: number
  invalid_rows: number
  skipped_rows: number
  sheet_stats: SheetImportStat[]
  warnings: ImportWarning[]
}

export interface ImportResponse {
  success: boolean
  data: ImportResult
}
