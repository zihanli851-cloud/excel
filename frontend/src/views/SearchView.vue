<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Download, ListFilter } from 'lucide-vue-next'

import QueryHistoryDrawer from '@/components/search/QueryHistoryDrawer.vue'
import ProjectSearchForm from '@/components/search/ProjectSearchForm.vue'
import ProjectDetailDialog from '@/components/projects/ProjectDetailDialog.vue'
import ProjectResultTable from '@/components/projects/ProjectResultTable.vue'
import ReviewDialog from '@/components/projects/ReviewDialog.vue'
import { extractErrorMessage } from '@/api/http'
import { useMetadataStore } from '@/stores/metadata'
import { useProjectSearchStore } from '@/stores/projectSearch'
import type { ProjectSearchRequest, SortBy } from '@/types/project'

const metadataStore = useMetadataStore()
const projectSearchStore = useProjectSearchStore()

const historyVisible = ref(false)
const detailVisible = ref(false)
const reviewVisible = ref(false)
const reviewLoading = ref(false)
const selectedIds = ref<number[]>([])
const reviewingProjectId = ref<number | null>(null)

const currentProjectName = computed(() => projectSearchStore.selectedProject?.project_name || null)

async function handleSearch(resetPage = true) {
  try {
    await projectSearchStore.search(resetPage)
  } catch (error) {
    ElMessage.error(extractErrorMessage(error))
  }
}

function handleReset() {
  projectSearchStore.resetFilters()
  void handleSearch(true)
}

function handleApplyHistory(query: Partial<ProjectSearchRequest>) {
  projectSearchStore.applyHistory(query)
  void handleSearch(true)
}

async function handleView(projectId: number) {
  try {
    await projectSearchStore.loadDetail(projectId)
    detailVisible.value = true
  } catch (error) {
    ElMessage.error(extractErrorMessage(error))
  }
}

async function handleOpenReview(projectId: number) {
  reviewingProjectId.value = projectId
  if (!projectSearchStore.selectedProject || projectSearchStore.selectedProject.id !== projectId) {
    try {
      await projectSearchStore.loadDetail(projectId)
    } catch (error) {
      ElMessage.error(extractErrorMessage(error))
      return
    }
  }
  reviewVisible.value = true
}

async function handleSubmitReview(payload: { comment: string | null }) {
  if (!reviewingProjectId.value) return

  reviewLoading.value = true
  try {
    await projectSearchStore.submitReview(reviewingProjectId.value, payload)
    ElMessage.success('复核记录已提交')
    reviewVisible.value = false
  } catch (error) {
    ElMessage.error(extractErrorMessage(error))
  } finally {
    reviewLoading.value = false
  }
}

async function handleExportCurrent() {
  try {
    await projectSearchStore.exportByQuery()
    ElMessage.success('导出任务已开始')
  } catch (error) {
    ElMessage.error(extractErrorMessage(error))
  }
}

async function handleExportSelected() {
  if (selectedIds.value.length === 0) {
    ElMessage.warning('请先勾选需要导出的记录')
    return
  }

  try {
    await projectSearchStore.exportByIds(selectedIds.value)
    ElMessage.success('已导出选中记录')
  } catch (error) {
    ElMessage.error(extractErrorMessage(error))
  }
}

async function handleSortChange(sortBy: SortBy, sortOrder: 'asc' | 'desc') {
  try {
    await projectSearchStore.changeSort(sortBy, sortOrder)
  } catch (error) {
    ElMessage.error(extractErrorMessage(error))
  }
}

onMounted(async () => {
  try {
    await Promise.all([metadataStore.loadPurchasers(), metadataStore.loadInvalidStats(), projectSearchStore.search(true)])
  } catch (error) {
    ElMessage.error(extractErrorMessage(error))
  }
})
</script>

<template>
  <div class="page search-page">
    <div class="page-header">
      <div>
        <h1 class="page-title">项目查询</h1>
        <p class="page-subtitle">默认隐藏无效数据，支持组合筛选、历史复用、详情查看、复核和导出。</p>
      </div>
      <div class="toolbar">
        <el-button :icon="ListFilter" @click="historyVisible = true">查询历史</el-button>
        <el-button :icon="Download" @click="handleExportSelected">导出选中</el-button>
        <el-button :icon="Download" type="primary" @click="handleExportCurrent">导出当前查询</el-button>
      </div>
    </div>

    <ProjectSearchForm
      v-model="projectSearchStore.filters"
      :invalid-stats="metadataStore.invalidStats"
      :loading="projectSearchStore.loading"
      :purchasers="metadataStore.purchasers"
      @history="historyVisible = true"
      @reset="handleReset"
      @submit="handleSearch(true)"
    />

    <ProjectResultTable
      :items="projectSearchStore.items"
      :keyword="projectSearchStore.filters.keyword"
      :loading="projectSearchStore.loading"
      :pagination="projectSearchStore.pagination"
      @page-change="projectSearchStore.changePage"
      @page-size-change="projectSearchStore.changePageSize"
      @review="handleOpenReview"
      @selection-change="selectedIds = $event"
      @sort-change="handleSortChange"
      @view="handleView"
    />

    <QueryHistoryDrawer v-model="historyVisible" @apply="handleApplyHistory" />
    <ProjectDetailDialog
      v-model="detailVisible"
      :loading="projectSearchStore.detailLoading"
      :project="projectSearchStore.selectedProject"
      @review="handleOpenReview"
    />
    <ReviewDialog
      v-model="reviewVisible"
      :loading="reviewLoading"
      :project-name="currentProjectName"
      @submit="handleSubmitReview"
    />
  </div>
</template>

<style scoped>
.search-page {
  gap: 18px;
}
</style>
