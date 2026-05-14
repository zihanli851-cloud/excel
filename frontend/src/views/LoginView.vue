<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { LockKeyhole, UserRound } from 'lucide-vue-next'

import { extractErrorMessage } from '@/api/http'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  username: '',
  password: '',
})

const formRef = ref()

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  try {
    await authStore.loginAction(form)
    ElMessage.success('登录成功')
    router.push('/search')
  } catch (error) {
    ElMessage.error(extractErrorMessage(error))
  }
}
</script>

<template>
  <div class="login-page">
    <section class="login-hero">
      <div class="login-copy">
        <p class="login-eyebrow">项目清单筛选查询插件</p>
        <h1>把 Excel 检索工作，收进一个顺手的工具界面里。</h1>
        <p>
          面向业务查询、导出、复核和导入的轻量工作台。默认隐藏无效数据，按需追溯历史记录，尽量让每一次筛选都更直接。
        </p>
      </div>
    </section>

    <section class="login-panel panel">
      <div class="panel-body">
        <div class="login-panel-header">
          <h2>登录系统</h2>
          <p>输入账号密码后进入查询工作台</p>
        </div>

        <el-form ref="formRef" :model="form" :rules="rules" label-position="top" @submit.prevent="handleSubmit">
          <el-form-item label="用户名" prop="username">
            <el-input v-model="form.username" :prefix-icon="UserRound" placeholder="请输入用户名" />
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input
              v-model="form.password"
              :prefix-icon="LockKeyhole"
              placeholder="请输入密码"
              show-password
              type="password"
              @keyup.enter="handleSubmit"
            />
          </el-form-item>
          <el-button :loading="authStore.loading" class="login-submit" type="primary" @click="handleSubmit">
            登录
          </el-button>
        </el-form>
      </div>
    </section>
  </div>
</template>

<style scoped>
.login-page {
  display: grid;
  min-height: 100vh;
  grid-template-columns: minmax(0, 1.15fr) minmax(360px, 420px);
  background:
    radial-gradient(circle at 20% 20%, rgba(245, 189, 75, 0.35), transparent 20%),
    radial-gradient(circle at 80% 80%, rgba(31, 63, 120, 0.2), transparent 28%),
    linear-gradient(135deg, #f6f0df 0%, #f4f7fb 42%, #e5ecf6 100%);
}

.login-hero {
  display: flex;
  align-items: center;
  padding: 56px;
}

.login-copy {
  max-width: 620px;
}

.login-eyebrow {
  margin: 0 0 12px;
  color: #8f5e15;
  font-size: 14px;
  font-weight: 700;
}

.login-copy h1 {
  margin: 0;
  font-family: Georgia, "Times New Roman", serif;
  font-size: clamp(34px, 4vw, 62px);
  line-height: 1.02;
}

.login-copy p:last-child {
  max-width: 520px;
  margin: 20px 0 0;
  color: #4c5c75;
  font-size: 16px;
  line-height: 1.7;
}

.login-panel {
  align-self: stretch;
  border: none;
  border-radius: 0;
  background: rgba(255, 255, 255, 0.84);
  backdrop-filter: blur(18px);
}

.panel-body {
  display: flex;
  height: 100%;
  flex-direction: column;
  justify-content: center;
  padding: 40px;
}

.login-panel-header h2 {
  margin: 0;
  font-size: 28px;
}

.login-panel-header p {
  margin: 10px 0 24px;
  color: var(--app-muted);
}

.login-submit {
  width: 100%;
  margin-top: 8px;
}

@media (max-width: 960px) {
  .login-page {
    grid-template-columns: 1fr;
  }

  .login-hero {
    padding: 24px 20px 12px;
  }

  .panel-body {
    padding: 20px;
  }
}
</style>
