import http from './http'
import {
  isMockEnabled,
  mockExportFile,
  mockGetProjectDetail,
  mockReviewProject,
  mockSearchProjects,
} from './mock'

import type {
  ExportByIdsRequest,
  ExportByQueryRequest,
  ProjectRead,
  ProjectReviewRequest,
  ProjectReviewResponse,
  ProjectSearchRequest,
  ProjectSearchResponse,
} from '@/types/project'

export async function searchProjects(payload: ProjectSearchRequest) {
  if (isMockEnabled) {
    return mockSearchProjects(payload)
  }
  const { data } = await http.post<ProjectSearchResponse>('/projects/search', payload)
  return data
}

export async function getProjectDetail(projectId: number) {
  if (isMockEnabled) {
    return mockGetProjectDetail(projectId)
  }
  const { data } = await http.get<ProjectRead>(`/projects/${projectId}`)
  return data
}

export async function reviewProject(projectId: number, payload: ProjectReviewRequest) {
  if (isMockEnabled) {
    void payload
    return mockReviewProject(projectId)
  }
  const { data } = await http.post<ProjectReviewResponse>(`/projects/${projectId}/review`, payload)
  return data
}

export async function exportProjectsByQuery(payload: ExportByQueryRequest) {
  if (isMockEnabled) {
    void payload
    return mockExportFile()
  }
  return http.post('/projects/export-by-query', payload, {
    responseType: 'blob',
  })
}

export async function exportProjectsByIds(payload: ExportByIdsRequest) {
  if (isMockEnabled) {
    void payload
    return mockExportFile()
  }
  return http.post('/projects/export', payload, {
    responseType: 'blob',
  })
}
