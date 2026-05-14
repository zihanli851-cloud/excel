<script setup lang="ts">
import { computed, watch } from 'vue'
import { CalendarDays, Filter, History, RotateCcw, Search } from 'lucide-vue-next'

import {
  amountFieldOptions,
  invalidModeOptions,
  invalidReasonOptions,
  type ProjectSearchRequest,
} from '@/types/project'
import { invalidReasonLabel } from '@/utils/format'

const model = defineModel<ProjectSearchRequest>({ required: true })

defineProps<{
  purchasers: string[]
  loading?: boolean
  invalidStats?: Record<string, number>
}>()

const emit = defineEmits<{
  submit: []
  reset: []
  history: []
}>()

const dateRange = computed<[string, string] | []>({
  get() {
    if (model.value.date_from && model.value.date_to) {
      return [model.value.date_from, model.value.date_to]
    }
    return []
  },
  set(value) {
    model.value.date_from = value?.[0] || null
    model.value.date_to = value?.[1] || null
  },
})

watch(
  () => model.value.invalid_mode,
  (mode) => {
    if (mode !== 'invalid_only') {
      model.value.invalid_reason = null
    }
  },
)
</script>

<template>
  <section class="panel">
    <div class="panel-body search-form-panel">
      <div class="search-form-header">
        <div>
          <div class="search-form-title">筛选条件</div>
          <div class="search-form-subtitle">默认仅查询有效数据，可切换查看全部或仅无效记录。</div>
        </div>
        <div class="toolbar">
          <el-button :icon="History" @click="emit('history')">查询历史</el-button>
          <el-button :icon="RotateCcw" @click="emit('reset')">重置</el-button>
          <el-button :icon="Search" :loading="loading" type="primary" @click="emit('submit')">查询</el-button>
        </div>
      </div>

      <el-form label-position="top">
        <div class="search-grid">
          <el-form-item label="项目名称关键词">
            <el-input v-model="model.keyword" clearable placeholder="输入项目名称关键词" />
          </el-form-item>

          <el-form-item label="项目编号">
            <el-input v-model="model.code" clearable placeholder="输入项目编号或前缀" />
          </el-form-item>

          <el-form-item label="采购人">
            <el-select v-model="model.purchaser" clearable filterable placeholder="请选择采购人">
              <el-option v-for="item in purchasers" :key="item" :label="item" :value="item" />
            </el-select>
          </el-form-item>

          <el-form-item label="开标时间">
            <el-date-picker
              v-model="dateRange"
              end-placeholder="结束日期"
              format="YYYY-MM-DD"
              start-placeholder="开始日期"
              type="daterange"
              value-format="YYYY-MM-DD"
            />
          </el-form-item>

          <el-form-item label="金额下限（万元）">
            <el-input-number v-model="model.amount_min" :controls="false" :min="0" class="full-width" />
          </el-form-item>

          <el-form-item label="金额上限（万元）">
            <el-input-number v-model="model.amount_max" :controls="false" :min="0" class="full-width" />
          </el-form-item>
        </div>

        <div class="segmented-row">
          <el-form-item class="segment-item" label="金额字段">
            <el-radio-group v-model="model.amount_field" size="large">
              <el-radio-button v-for="item in amountFieldOptions" :key="item.value" :label="item.value">
                {{ item.label }}
              </el-radio-button>
            </el-radio-group>
          </el-form-item>

          <el-form-item class="segment-item" label="无效数据范围">
            <el-radio-group v-model="model.invalid_mode" size="large">
              <el-radio-button v-for="item in invalidModeOptions" :key="item.value" :label="item.value">
                {{ item.label }}
              </el-radio-button>
            </el-radio-group>
          </el-form-item>
        </div>

        <div class="search-grid compact-grid">
          <el-form-item label="无效原因">
            <el-select
              v-model="model.invalid_reason"
              :disabled="model.invalid_mode !== 'invalid_only'"
              clearable
              placeholder="仅在仅无效模式下可选"
            >
              <el-option v-for="item in invalidReasonOptions" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>

          <div class="invalid-stat-card panel">
            <div class="invalid-stat-header">
              <CalendarDays :size="16" />
              <span>无效分类概览</span>
            </div>
            <div class="invalid-stat-body">
              <div v-for="item in invalidReasonOptions" :key="item.value" class="invalid-stat-item">
                <span>{{ invalidReasonLabel(item.value) }}</span>
                <strong>{{ invalidStats?.[item.value] || 0 }}</strong>
              </div>
            </div>
          </div>
        </div>
      </el-form>
    </div>
  </section>
</template>

<style scoped>
.search-form-panel {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.search-form-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}

.search-form-title {
  font-size: 16px;
  font-weight: 700;
}

.search-form-subtitle {
  margin-top: 6px;
  color: var(--app-muted);
  line-height: 1.5;
}

.search-grid {
  display: grid;
  gap: 16px;
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.compact-grid {
  align-items: start;
}

.segmented-row {
  display: grid;
  gap: 16px;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
}

.segment-item :deep(.el-form-item__content) {
  overflow-x: auto;
}

.full-width {
  width: 100%;
}

.invalid-stat-card {
  min-height: 100%;
  border-radius: 8px;
  padding: 12px 14px;
  background:
    linear-gradient(180deg, rgba(250, 245, 216, 0.85), rgba(255, 255, 255, 0.95)),
    #fff;
}

.invalid-stat-header {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #7d5b12;
  font-weight: 700;
}

.invalid-stat-body {
  display: grid;
  margin-top: 10px;
  gap: 10px;
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.invalid-stat-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding-bottom: 6px;
  border-bottom: 1px dashed rgba(125, 91, 18, 0.16);
}

.invalid-stat-item strong {
  color: #7d5b12;
}

@media (max-width: 1100px) {
  .search-grid,
  .segmented-row {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 768px) {
  .search-form-header,
  .search-grid,
  .segmented-row {
    grid-template-columns: 1fr;
    flex-direction: column;
  }

  .invalid-stat-body {
    grid-template-columns: 1fr;
  }
}
</style>
