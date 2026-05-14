<script setup lang="ts">
import type { ImportResult } from '@/types/import'

defineProps<{
  result: ImportResult | null
}>()
</script>

<template>
  <section class="panel">
    <div class="panel-body import-result-panel">
      <div class="result-title">导入结果</div>

      <el-empty v-if="!result" description="尚未执行导入" />

      <template v-else>
        <div class="import-summary">
          <div class="summary-card">
            <span>文件名</span>
            <strong>{{ result.file_name }}</strong>
          </div>
          <div class="summary-card">
            <span>总行数</span>
            <strong>{{ result.total_rows }}</strong>
          </div>
          <div class="summary-card">
            <span>导入行数</span>
            <strong>{{ result.imported_rows }}</strong>
          </div>
          <div class="summary-card">
            <span>有效行数</span>
            <strong>{{ result.valid_rows }}</strong>
          </div>
          <div class="summary-card">
            <span>无效行数</span>
            <strong>{{ result.invalid_rows }}</strong>
          </div>
          <div class="summary-card">
            <span>跳过行数</span>
            <strong>{{ result.skipped_rows }}</strong>
          </div>
        </div>

        <div class="import-section">
          <div class="section-title">Sheet 统计</div>
          <el-table :data="result.sheet_stats" border>
            <el-table-column label="Sheet 名" min-width="180" prop="sheet_name" />
            <el-table-column label="年度" min-width="90" prop="sheet_year" />
            <el-table-column label="总行数" min-width="90" prop="total_rows" />
            <el-table-column label="导入行数" min-width="100" prop="imported_rows" />
            <el-table-column label="无效行数" min-width="100" prop="invalid_rows" />
          </el-table>
        </div>

        <div class="import-section">
          <div class="section-title">Warnings</div>
          <el-empty v-if="result.warnings.length === 0" description="无 warning" />
          <el-table v-else :data="result.warnings" border>
            <el-table-column label="Sheet" min-width="140" prop="sheet" />
            <el-table-column label="行号" min-width="80" prop="row" />
            <el-table-column label="字段" min-width="140" prop="field" />
            <el-table-column label="说明" min-width="280" prop="message" />
          </el-table>
        </div>
      </template>
    </div>
  </section>
</template>

<style scoped>
.import-result-panel {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.result-title,
.section-title {
  font-size: 16px;
  font-weight: 700;
}

.import-summary {
  display: grid;
  gap: 12px;
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.summary-card {
  display: flex;
  min-height: 96px;
  flex-direction: column;
  justify-content: space-between;
  padding: 14px;
  border: 1px solid var(--app-border);
  border-radius: 8px;
  background: linear-gradient(180deg, #ffffff, #fbfcff);
}

.summary-card span {
  color: var(--app-muted);
}

.summary-card strong {
  font-size: 20px;
}

.import-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

@media (max-width: 768px) {
  .import-summary {
    grid-template-columns: 1fr;
  }
}
</style>
