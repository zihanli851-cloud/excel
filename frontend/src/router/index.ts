import { createRouter, createWebHistory } from 'vue-router'

import { authGuard } from './guards'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/search',
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
      meta: { public: true },
    },
    {
      path: '/',
      component: () => import('@/layouts/AppLayout.vue'),
      children: [
        {
          path: '/search',
          name: 'search',
          component: () => import('@/views/SearchView.vue'),
        },
        {
          path: '/import',
          name: 'import',
          component: () => import('@/views/ImportView.vue'),
          meta: { requiresAdmin: true },
        },
        {
          path: '/audit/logs',
          name: 'audit-logs',
          component: () => import('@/views/AuditLogView.vue'),
          meta: { requiresAdmin: true },
        },
      ],
    },
  ],
  scrollBehavior() {
    return { top: 0 }
  },
})

router.beforeEach(authGuard)

export default router
