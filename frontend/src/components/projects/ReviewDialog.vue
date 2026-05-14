<script setup lang="ts">
import { reactive, watch } from 'vue'

const visible = defineModel<boolean>({ required: true })

const props = defineProps<{
  loading?: boolean
  projectName?: string | null
}>()

const emit = defineEmits<{
  submit: [payload: { comment: string | null }]
}>()

const form = reactive({
  comment: '',
})

watch(
  () => visible.value,
  (open) => {
    if (open) {
      form.comment = ''
    }
  },
)
</script>

<template>
  <el-dialog v-model="visible" title="项目复核" width="560px">
    <div class="review-note">
      <div class="review-title">{{ projectName || '当前项目' }}</div>
      <div class="review-subtitle">当前后端会记录复核审计日志，备注会随本次复核一起提交。</div>
    </div>

    <el-form label-position="top">
      <el-form-item label="复核备注">
        <el-input
          v-model="form.comment"
          :rows="5"
          maxlength="1000"
          placeholder="填写确认或修正说明"
          show-word-limit
          type="textarea"
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="visible = false">取消</el-button>
      <el-button :loading="loading" type="primary" @click="emit('submit', { comment: form.comment || null })">
        提交复核
      </el-button>
    </template>
  </el-dialog>
</template>

<style scoped>
.review-note {
  margin-bottom: 12px;
}

.review-title {
  font-size: 15px;
  font-weight: 700;
}

.review-subtitle {
  margin-top: 6px;
  color: var(--app-muted);
  line-height: 1.5;
}
</style>
