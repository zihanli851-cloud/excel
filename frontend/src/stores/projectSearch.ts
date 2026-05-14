import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

import {
  exportProjectsByIds,
  exportProjectsByQuery,
  getProjectDetail,
  reviewProject,
  searchProjects,
} from '@/api/projects'
import { downloadBlob } from '@/utils/download'
import {
  createDefaultProjectSearch,
  type ExportByQueryRequest,
  type ProjectRead,
  type ProjectReviewRequest,
  type ProjectSearchRequest,
} from '@/types/project'
import type { PaginationMeta } from '@/types/common'

function pageSize() {
  return Number(import.meta.env.VITE_PAGE_SIZE || 20)
}

export const useProjectSearchStore = defineStore('project-search', () => {
  const filters = ref<ProjectSearchRequest>(createDefaultProjectSearch(pageSize()))
  const items = ref<ProjectRead[]>([])
  const pagination = ref<PaginationMeta>({ page: 1, page_size: pageSize(), total: 0 })
  const loading = ref(false)
  const detailLoading = ref(false)
  const selectedProject = ref<ProjectRead | null>(null)

  const hasFilters = computed(() => {
    const defaults = createDefaultProjectSearch(pageSize())
    return JSON.stringify(filters.value) !== JSON.stringify(defaults)
  })

  async function search(resetPage = false) {
    if (resetPage) {
      filters.value.page = 1
    }
    loading.value = true
    try {
      const response = await searchProjects(filters.value)
      items.value = response.data.items
      pagination.value = response.data.pagination
      return response
    } finally {
      loading.value = false
    }
  }

  function resetFilters() {
    filters.value = createDefaultProjectSearch(pageSize())
  }

  function applyHistory(query: Partial<ProjectSearchRequest>) {
    filters.value = {
      ...createDefaultProjectSearch(pageSize()),
      ...query,
      page: 1,
      page_size: Number(query.page_size || pageSize()),
    }
  }

  async function changePage(page: number) {
    filters.value.page = page
    return search()
  }

  async function changePageSize(nextPageSize: number) {
    filters.value.page_size = nextPageSize
    filters.value.page = 1
    return search()
  }

  async function changeSort(sortBy: ProjectSearchRequest['sort_by'], sortOrder: ProjectSearchRequest['sort_order']) {
    filters.value.sort_by = sortBy
    filters.value.sort_order = sortOrder
    filters.value.page = 1
    return search()
  }

  async function loadDetail(projectId: number) {
    detailLoading.value = true
    try {
      selectedProject.value = await getProjectDetail(projectId)
      return selectedProject.value
    } finally {
      detailLoading.value = false
    }
  }

  function clearDetail() {
    selectedProject.value = null
  }

  async function submitReview(projectId: number, payload: ProjectReviewRequest) {
    return reviewProject(projectId, payload)
  }

  async function exportByQuery(fileName?: string) {
    const payload: ExportByQueryRequest = {
      ...filters.value,
      file_name: fileName || null,
      page: 1,
      page_size: filters.value.page_size,
    }
    const response = await exportProjectsByQuery(payload)
    downloadBlob(
      response.data,
      `查询结果_${new Date().toISOString().slice(0, 10)}.xlsx`,
      response.headers['content-disposition'],
    )
  }

  async function exportByIds(projectIds: number[], fileName?: string) {
    const response = await exportProjectsByIds({
      project_ids: projectIds,
      file_name: fileName || null,
    })
    downloadBlob(
      response.data,
      `查询结果_${new Date().toISOString().slice(0, 10)}.xlsx`,
      response.headers['content-disposition'],
    )
  }

  return {
    filters,
    items,
    pagination,
    loading,
    detailLoading,
    selectedProject,
    hasFilters,
    search,
    resetFilters,
    applyHistory,
    changePage,
    changePageSize,
    changeSort,
    loadDetail,
    clearDetail,
    submitReview,
    exportByQuery,
    exportByIds,
  }
})
