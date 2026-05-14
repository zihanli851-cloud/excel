<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Search, Upload, ClipboardList, LogOut } from 'lucide-vue-next'

import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const menuItems = computed(() => {
  const items = [
    { path: '/search', label: '项目查询', icon: Search, adminOnly: false },
    { path: '/import', label: '数据导入', icon: Upload, adminOnly: true },
    { path: '/audit/logs', label: '审计日志', icon: ClipboardList, adminOnly: true },
  ]

  return items.filter((item) => !item.adminOnly || authStore.isAdmin)
})

function handleSelect(path: string) {
  router.push(path)
}

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <div class="app-shell">
    <aside class="app-sidebar">
      <div class="app-brand">
        <div class="app-brand-mark">PL</div>
        <div>
          <div class="app-brand-title">项目清单筛选查询</div>
          <div class="app-brand-subtitle">Project List Console</div>
        </div>
      </div>

      <el-menu
        :default-active="route.path"
        class="app-menu"
        background-color="transparent"
        text-color="#dbe5f5"
        active-text-color="#ffffff"
        @select="handleSelect"
      >
        <el-menu-item v-for="item in menuItems" :key="item.path" :index="item.path">
          <el-icon><component :is="item.icon" :size="16" /></el-icon>
          <span>{{ item.label }}</span>
        </el-menu-item>
      </el-menu>
    </aside>

    <div class="app-main">
      <header class="app-header">
        <div>
          <div class="app-header-title">{{ authStore.user?.display_name || authStore.user?.username }}</div>
          <div class="app-header-subtitle">角色：{{ authStore.user?.role || '-' }}</div>
        </div>
        <el-button :icon="LogOut" text @click="handleLogout">退出登录</el-button>
      </header>

      <main class="app-content">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<style scoped>
.app-shell {
  display: grid;
  min-height: 100vh;
  grid-template-columns: 248px minmax(0, 1fr);
  background:
    radial-gradient(circle at top left, rgba(255, 225, 149, 0.18), transparent 32%),
    linear-gradient(180deg, #f5f7fb 0%, #eef2f8 100%);
}

.app-sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 24px 18px;
  background:
    linear-gradient(180deg, rgba(12, 27, 53, 0.96), rgba(21, 36, 67, 0.98)),
    #172033;
  color: #fff;
}

.app-brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.app-brand-mark {
  display: grid;
  width: 42px;
  height: 42px;
  place-items: center;
  border-radius: 8px;
  background: linear-gradient(135deg, #f9cf6b, #f29d52);
  color: #14223d;
  font-weight: 800;
}

.app-brand-title {
  font-size: 16px;
  font-weight: 700;
}

.app-brand-subtitle {
  margin-top: 2px;
  color: rgba(219, 229, 245, 0.72);
  font-size: 12px;
}

.app-menu {
  border-right: none;
}

.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 20px 24px 0;
}

.app-header-title {
  font-size: 16px;
  font-weight: 700;
}

.app-header-subtitle {
  margin-top: 4px;
  color: var(--app-muted);
  font-size: 12px;
}

.app-content {
  padding: 20px 24px 24px;
}

@media (max-width: 960px) {
  .app-shell {
    grid-template-columns: 1fr;
  }

  .app-sidebar {
    gap: 14px;
    padding: 16px;
  }

  .app-content {
    padding: 16px;
  }
}
</style>
