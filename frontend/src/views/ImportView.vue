<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

import ExcelUploadPanel from '@/components/import/ExcelUploadPanel.vue'
import ImportResultPanel from '@/components/import/ImportResultPanel.vue'
import { uploadExcel } from '@/api/import'
import { extractErrorMessage } from '@/api/http'
import type { ImportResult } from '@/types/import'

const uploading = ref(false)
const result = ref<ImportResult | null>(null)

async function handleUpload(file: File) {
  uploading.value = true
  try {
    const response = await uploadExcel(file)
    result.value = response.data
    ElMessage.success('导入完成')
  } catch (error) {
    ElMessage.error(extractErrorMessage(error))
  } finally {
    uploading.value = false
  }
}
</script>

<template>
  <div class="page">
    <div class="page-header">
      <div>
        <h1 class="page-title">数据导入</h1>
        <p class="page-subtitle">管理员可在这里上传 Excel 文件，并查看导入统计与 warning。</p>
      </div>
    </div>

    <ExcelUploadPanel v-model:loading="uploading" @submit="handleUpload" />
    <ImportResultPanel :result="result" />
  </div>
</template>
