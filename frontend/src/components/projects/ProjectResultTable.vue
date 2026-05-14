<script setup lang="ts">
import { computed } from 'vue'
import { CircleAlert, Download, Eye, SearchCheck } from 'lucide-vue-next'
import type { TableColumnCtx } from 'element-plus'

import type { PaginationMeta } from '@/types/common'
import type { ProjectRead, SortBy } from '@/types/project'
import { displayText, formatDate, invalidReasonLabel } from '@/utils/format'
import { highlightKeyword } from '@/utils/highlight'

const props = defineProps<{
  items: ProjectRead[]
  pagination: PaginationMeta
  loading?: boolean
  keyword?: string | null
}>()

const emit = defineEmits<{
  pageChange: [page: number]
  pageSizeChange: [pageSize: number]
  sortChange: [sortBy: SortBy, sortOrder: 'asc' | 'desc']
  view: [projectId: number]
  review: [projectId: number]
  selectionChange: [projectIds: number[]]
}>()

const hasInvalidRows = computed(() => props.items.some((item) => item.is_invalid))

function rowClassName({ row }: { row: ProjectRead }) {
  return row.is_invalid ? 'invalid-row' : ''
}

function handleSortChange({
  prop,
  order,
}: {
  column: TableColumnCtx<ProjectRead>
  prop: string
  order: 'ascending' | 'descending' | null
}) {
  if (!prop || !order) return
  emit('sortChange', prop as SortBy, order === 'ascending' ? 'asc' : 'desc')
}

function handleSelectionChange(rows: ProjectRead[]) {
  emit(
    'selectionChange',
    rows.map((item) => item.id),
  )
}
</script>

<template>
  <section class="panel">
    <div class="panel-body result-panel">
      <div class="result-header">
        <div>
          <div class="result-title">查询结果</div>
          <div class="result-subtitle">
            共 {{ pagination.total }} 条记录
            <span v-if="hasInvalidRows" class="danger-text">，当前页包含无效数据黄色标记</span>
          </div>
        </div>
        <div class="result-hint">
          <SearchCheck :size="16" />
          <span>支持排序、分页、详情查看和复核入口</span>
        </div>
      </div>

      <el-table
        :data="items"
        :loading="loading"
        :row-class-name="rowClassName"
        border
        class="result-table"
        @selection-change="handleSelectionChange"
        @sort-change="handleSortChange"
      >
        <el-table-column type="selection" width="46" />
        <el-table-column label="序号" min-width="76" prop="seq_no">
          <template #default="{ row }">
            {{ displayText(row.seq_no) }}
          </template>
        </el-table-column>
        <el-table-column label="项目名称" min-width="260" prop="project_name" sortable="custom">
          <template #default="{ row }">
            <div v-html="highlightKeyword(row.project_name, keyword)"></div>
          </template>
        </el-table-column>
        <el-table-column label="项目编号" min-width="150" prop="project_code" sortable="custom">
          <template #default="{ row }">
            {{ displayText(row.project_code) }}
          </template>
        </el-table-column>
        <el-table-column label="采购人" min-width="180" prop="purchaser" sortable="custom">
          <template #default="{ row }">
            {{ displayText(row.purchaser) }}
          </template>
        </el-table-column>
        <el-table-column label="开标时间" min-width="126" prop="bid_open_date" sortable="custom">
          <template #default="{ row }">
            {{ formatDate(row.bid_open_date) }}
          </template>
        </el-table-column>
        <el-table-column label="委托金额" min-width="150">
          <template #default="{ row }">
            {{ displayText(row.commission_amount) }}
          </template>
        </el-table-column>
        <el-table-column label="最高限价" min-width="150">
          <template #default="{ row }">
            {{ displayText(row.max_price) }}
          </template>
        </el-table-column>
        <el-table-column label="中标金额" min-width="180">
          <template #default="{ row }">
            {{ displayText(row.bid_amount) }}
          </template>
        </el-table-column>
        <el-table-column label="年度" min-width="80" prop="sheet_year" sortable="custom">
          <template #default="{ row }">
            {{ row.sheet_year }}
          </template>
        </el-table-column>
        <el-table-column label="无效原因" min-width="120">
          <template #default="{ row }">
            <el-tag v-if="row.is_invalid" class="invalid-reason-tag" effect="plain" type="warning">
              {{ invalidReasonLabel(row.invalid_reason) }}
            </el-tag>
            <span v-else class="muted">有效</span>
          </template>
        </el-table-column>
        <el-table-column fixed="right" label="操作" min-width="160">
          <template #default="{ row }">
            <div class="toolbar">
              <el-button :icon="Eye" size="small" text type="primary" @click="emit('view', row.id)">详情</el-button>
              <el-button :icon="CircleAlert" size="small" text @click="emit('review', row.id)">复核</el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <div class="result-footer">
        <div class="muted footer-left">
          <Download :size="14" />
          <span>可在页面上方导出当前查询结果，或勾选后按选中导出。</span>
        </div>
        <el-pagination
          :current-page="pagination.page"
          :page-size="pagination.page_size"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          background
          layout="total, sizes, prev, pager, next"
          @current-change="emit('pageChange', $event)"
          @size-change="emit('pageSizeChange', $event)"
        />
      </div>
    </div>
  </section>
</template>

<style scoped>
.result-panel {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.result-header,
.result-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.result-title {
  font-size: 16px;
  font-weight: 700;
}

.result-subtitle,
.result-hint {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 6px;
  color: var(--app-muted);
}

.footer-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

@media (max-width: 768px) {
  .result-header,
  .result-footer {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>
