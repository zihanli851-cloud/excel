import type { NavigationGuardNext, RouteLocationNormalized } from 'vue-router'
import { ElMessage } from 'element-plus'

import { useAuthStore } from '@/stores/auth'

export async function authGuard(to: RouteLocationNormalized, _: RouteLocationNormalized, next: NavigationGuardNext) {
  const authStore = useAuthStore()
  authStore.restoreFromStorage()

  if (to.meta.public) {
    if (to.path === '/login' && authStore.isAuthenticated) {
      next('/search')
      return
    }
    next()
    return
  }

  if (!authStore.isAuthenticated) {
    next('/login')
    return
  }

  if (!authStore.user) {
    try {
      await authStore.fetchCurrentUser()
    } catch {
      authStore.logout()
      next('/login')
      return
    }
  }

  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    ElMessage.warning('当前账号无权访问该页面')
    next('/search')
    return
  }

  next()
}
