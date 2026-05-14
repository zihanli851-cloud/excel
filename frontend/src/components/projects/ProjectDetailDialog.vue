<script setup lang="ts">
import type { ProjectRead } from '@/types/project'
import { displayText, formatDate, invalidReasonLabel } from '@/utils/format'

const visible = defineModel<boolean>({ required: true })

defineProps<{
  project: ProjectRead | null
  loading?: boolean
}>()

const emit = defineEmits<{
  review: [projectId: number]
}>()
</script>

<template>
  <el-dialog v-model="visible" title="项目详情" width="860px">
    <el-skeleton :loading="loading" animated>
      <template #default>
        <el-empty v-if="!project" description="暂无项目详情" />
        <div v-else class="detail-content">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="序号">{{ displayText(project.seq_no) }}</el-descriptions-item>
            <el-descriptions-item label="所属年度">{{ project.sheet_year }}</el-descriptions-item>
            <el-descriptions-item label="项目名称" :span="2">{{ displayText(project.project_name) }}</el-descriptions-item>
            <el-descriptions-item label="项目编号">{{ displayText(project.project_code) }}</el-descriptions-item>
            <el-descriptions-item label="采购人">{{ displayText(project.purchaser) }}</el-descriptions-item>
            <el-descriptions-item label="开标时间">{{ formatDate(project.bid_open_date) }}</el-descriptions-item>
            <el-descriptions-item label="是否无效">
              <el-tag :type="project.is_invalid ? 'warning' : 'success'" effect="plain">
                {{ project.is_invalid ? '无效' : '有效' }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="无效原因">{{ invalidReasonLabel(project.invalid_reason) }}</el-descriptions-item>
            <el-descriptions-item label="委托金额">{{ displayText(project.commission_amount) }}</el-descriptions-item>
            <el-descriptions-item label="最高限价">{{ displayText(project.max_price) }}</el-descriptions-item>
            <el-descriptions-item label="中标金额">{{ displayText(project.bid_amount) }}</el-descriptions-item>
            <el-descriptions-item label="中标金额（分包）">{{ displayText(project.bid_amount_detail) }}</el-descriptions-item>
          </el-descriptions>

          <el-collapse>
            <el-collapse-item title="解析字段（调试查看）" name="parsed">
              <el-descriptions :column="3" border size="small">
                <el-descriptions-item label="commission_num">{{ displayText(project.commission_num) }}</el-descriptions-item>
                <el-descriptions-item label="max_price_num">{{ displayText(project.max_price_num) }}</el-descriptions-item>
                <el-descriptions-item label="bid_amount_num">{{ displayText(project.bid_amount_num) }}</el-descriptions-item>
              </el-descriptions>
            </el-collapse-item>
          </el-collapse>
        </div>
      </template>
    </el-skeleton>

    <template #footer>
      <el-button @click="visible = false">关闭</el-button>
      <el-button v-if="project" type="primary" @click="emit('review', project.id)">复核</el-button>
    </template>
  </el-dialog>
</template>

<style scoped>
.detail-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
</style>
