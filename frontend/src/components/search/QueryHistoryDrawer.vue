<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { History, RotateCcw, Trash2 } from 'lucide-vue-next'

import { deleteQueryHistory, getQueryHistory } from '@/api/queryHistory'
import { extractErrorMessage } from '@/api/http'
import type { QueryHistoryRead } from '@/types/queryHistory'
import type { ProjectSearchRequest } from '@/types/project'
import { formatDateTime, querySummary } from '@/utils/format'

const visible = defineModel<boolean>({ required: true })

const emit = defineEmits<{
  apply: [query: Partial<ProjectSearchRequest>]
}>()

const loading = ref(false)
const deletingId = ref<number | null>(null)
const items = ref<QueryHistoryRead[]>([])
const total = ref(0)

const isEmpty = computed(() => items.value.length === 0)

async function loadHistory() {
  loading.value = true
  try {
    const response = await getQueryHistory(1, 20)
    items.value = response.data.items
    total.value = response.data.pagination.total
  } catch (error) {
    ElMessage.error(extractErrorMessage(error))
  } finally {
    loading.value = false
  }
}

watch(
  () => visible.value,
  (open) => {
    if (open) {
      void loadHistory()
    }
  },
)

async function handleDelete(item: QueryHistoryRead) {
  await ElMessageBox.confirm('删除后将无法直接复用这条查询记录，是否继续？', '删除查询历史', {
    type: 'warning',
  })

  deletingId.value = item.id
  try {
    await deleteQueryHistory(item.id)
    ElMessage.success('已删除查询历史')
    await loadHistory()
  } catch (error) {
    ElMessage.error(extractErrorMessage(error))
  } finally {
    deletingId.value = null
  }
}

function handleApply(item: QueryHistoryRead) {
  emit('apply', item.query_params as Partial<ProjectSearchRequest>)
  visible.value = false
}
</script>

<template>
  <el-drawer v-model="visible" size="420px" title="查询历史">
    <div class="history-drawer">
      <div class="history-drawer-header">
        <div>
          <div class="history-title">最近 {{ total }} 条记录中的前 20 条</div>
          <div class="history-subtitle">后端查询成功后会自动保存一次查询条件。</div>
        </div>
      </div>

      <el-skeleton :loading="loading" :rows="6" animated>
        <template #default>
          <el-empty v-if="isEmpty" description="暂无查询历史" />
          <div v-else class="history-list">
            <button v-for="item in items" :key="item.id" class="history-card" type="button" @click="handleApply(item)">
              <div class="history-card-top">
                <div class="history-card-title">
                  <History :size="16" />
                  <span class="text-ellipsis">{{ querySummary(item.query_params) }}</span>
                </div>
                <el-button
                  :icon="Trash2"
                  :loading="deletingId === item.id"
                  text
                  type="danger"
                  @click.stop="handleDelete(item)"
                />
              </div>
              <div class="history-meta">
                <span>结果 {{ item.result_count }} 条</span>
                <span>{{ formatDateTime(item.created_at) }}</span>
              </div>
              <div class="history-actions">
                <el-button :icon="RotateCcw" size="small" text type="primary">回填并查询</el-button>
              </div>
            </button>
          </div>
        </template>
      </el-skeleton>
    </div>
  </el-drawer>
</template>

<style scoped>
.history-drawer {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.history-title {
  font-size: 15px;
  font-weight: 700;
}

.history-subtitle {
  margin-top: 6px;
  color: var(--app-muted);
  line-height: 1.5;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.history-card {
  width: 100%;
  padding: 14px;
  border: 1px solid var(--app-border);
  border-radius: 8px;
  background: #fff;
  cursor: pointer;
  text-align: left;
  transition:
    border-color 0.2s ease,
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.history-card:hover {
  border-color: #d4aa44;
  box-shadow: 0 8px 20px rgba(20, 34, 61, 0.06);
  transform: translateY(-1px);
}

.history-card-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.history-card-title {
  display: flex;
  min-width: 0;
  align-items: center;
  gap: 8px;
  font-weight: 700;
}

.history-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-top: 10px;
  color: var(--app-muted);
  font-size: 12px;
}

.history-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}
</style>
