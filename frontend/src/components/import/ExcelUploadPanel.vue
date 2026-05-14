<script setup lang="ts">
import { computed, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { FileUp } from 'lucide-vue-next'

const loading = defineModel<boolean>('loading', { required: true })

const emit = defineEmits<{
  submit: [file: File]
}>()

const fileList = ref<File[]>([])

const selectedFile = computed(() => fileList.value[0] || null)

function beforeUpload(file: File) {
  const lowerName = file.name.toLowerCase()
  const isExcel = lowerName.endsWith('.xlsx') || lowerName.endsWith('.xlsm')
  if (!isExcel) {
    ElMessage.error('仅支持 .xlsx 或 .xlsm 文件')
    return false
  }

  fileList.value = [file]
  return false
}

function handleRemove() {
  fileList.value = []
}

function handleSubmit() {
  if (!selectedFile.value) {
    ElMessage.warning('请先选择一个 Excel 文件')
    return
  }
  emit('submit', selectedFile.value)
}
</script>

<template>
  <section class="panel">
    <div class="panel-body upload-panel">
      <div class="upload-header">
        <div>
          <div class="upload-title">上传 Excel</div>
          <div class="upload-subtitle">支持 `.xlsx`、`.xlsm`，导入结果由后端负责表头校验、黄色识别和金额解析。</div>
        </div>
        <el-button :icon="FileUp" :loading="loading" type="primary" @click="handleSubmit">开始导入</el-button>
      </div>

      <el-upload
        :auto-upload="false"
        :before-upload="beforeUpload"
        :file-list="fileList as never[]"
        :limit="1"
        drag
        @remove="handleRemove"
      >
        <el-icon class="el-icon--upload"><FileUp :size="28" /></el-icon>
        <div class="el-upload__text">拖拽文件到此处，或点击选择 Excel 文件</div>
      </el-upload>

      <div class="upload-footer muted">
        当前文件：{{ selectedFile ? selectedFile.name : '未选择文件' }}
      </div>
    </div>
  </section>
</template>

<style scoped>
.upload-panel {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.upload-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.upload-title {
  font-size: 16px;
  font-weight: 700;
}

.upload-subtitle {
  margin-top: 6px;
  color: var(--app-muted);
  line-height: 1.5;
}

.upload-footer {
  font-size: 13px;
}

@media (max-width: 768px) {
  .upload-header {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>
