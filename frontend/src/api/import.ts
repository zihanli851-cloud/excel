import http from './http'
import { isMockEnabled, mockUploadExcel } from './mock'

import type { ImportResponse } from '@/types/import'

export async function uploadExcel(file: File) {
  if (isMockEnabled) {
    return mockUploadExcel(file)
  }
  const formData = new FormData()
  formData.append('file', file)
  const { data } = await http.post<ImportResponse>('/import/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return data
}
