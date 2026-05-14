<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'

import { getAuditLogs } from '@/api/audit'
import { extractErrorMessage } from '@/api/http'
import type { AuditLogRead } from '@/types/audit'
import { displayText, formatDateTime } from '@/utils/format'

const loading = ref(false)
const items = ref<AuditLogRead[]>([])
const detailVisible = ref(false)
const activeLog = ref<AuditLogRead | null>(null)

const filters = reactive({
  action: '',
  page: 1,
  page_size: 20,
  total: 0,
})

const actionOptions = [
  'login',
  'search_projects',
  'export_projects_by_query',
  'export_projects_by_ids',
  'review_project',
  'save_query_history',
  'delete_query_history',
]

const prettyDetail = computed(() => JSON.stringify(activeLog.value?.detail || {}, null, 2))

async function loadLogs() {
  loading.value = true
  try {
    const response = await getAuditLogs({
      page: filters.page,
      page_size: filters.page_size,
      action: filters.action || null,
    })
    items.value = response.data.items
    filters.total = response.data.pagination.total
  } catch (error) {
    ElMessage.error(extractErrorMessage(error))
  } finally {
    loading.value = false
  }
}

function handleFilter() {
  filters.page = 1
  void loadLogs()
}

function handleOpenDetail(log: AuditLogRead) {
  activeLog.value = log
  detailVisible.value = true
}

onMounted(() => {
  void loadLogs()
})
</script>

<template>
  <div class="page">
    <div class="page-header">
      <div>
        <h1 class="page-title">审计日志</h1>
        <p class="page-subtitle">查看登录、查询、导出、复核和查询历史相关操作记录。</p>
      </div>
      <div class="toolbar">
        <el-select v-model="filters.action" clearable placeholder="按动作筛选" style="width: 220px" @change="handleFilter">
          <el-option v-for="item in actionOptions" :key="item" :label="item" :value="item" />
        </el-select>
      </div>
    </div>

    <section class="panel">
      <div class="panel-body">
        <el-table :data="items" :loading="loading" border>
          <el-table-column label="ID" min-width="80" prop="id" />
          <el-table-column label="用户 ID" min-width="100" prop="user_id">
            <template #default="{ row }">
              {{ displayText(row.user_id) }}
            </template>
          </el-table-column>
          <el-table-column label="动作" min-width="220" prop="action" />
          <el-table-column label="来源 IP" min-width="140" prop="ip_address">
            <template #default="{ row }">
              {{ displayText(row.ip_address) }}
            </template>
          </el-table-column>
          <el-table-column label="时间" min-width="180" prop="created_at">
            <template #default="{ row }">
              {{ formatDateTime(row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="详情" min-width="120">
            <template #default="{ row }">
              <el-button text type="primary" @click="handleOpenDetail(row)">查看 JSON</el-button>
            </template>
          </el-table-column>
        </el-table>

        <div class="audit-footer">
          <el-pagination
            :current-page="filters.page"
            :page-size="filters.page_size"
            :page-sizes="[20, 50, 100]"
            :total="filters.total"
            background
            layout="total, sizes, prev, pager, next"
            @current-change="filters.page = $event; loadLogs()"
            @size-change="filters.page_size = $event; filters.page = 1; loadLogs()"
          />
        </div>
      </div>
    </section>

    <el-dialog v-model="detailVisible" title="日志详情" width="760px">
      <pre class="log-detail">{{ prettyDetail }}</pre>
    </el-dialog>
  </div>
</template>

<style scoped>
.audit-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}

.log-detail {
  overflow: auto;
  padding: 14px;
  border-radius: 8px;
  background: #0f172a;
  color: #dbe5f5;
  font-size: 12px;
  line-height: 1.6;
}
</style>
