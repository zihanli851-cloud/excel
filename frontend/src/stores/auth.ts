import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

import { getCurrentUser, login } from '@/api/auth'
import { clearStoredToken, getStoredToken, setStoredToken } from '@/api/http'
import type { CurrentUser, LoginRequest } from '@/types/auth'

const USER_STORAGE_KEY = 'project-list-user'

function loadStoredUser() {
  const raw = localStorage.getItem(USER_STORAGE_KEY)
  if (!raw) return null
  try {
    return JSON.parse(raw) as CurrentUser
  } catch {
    return null
  }
}

function saveStoredUser(user: CurrentUser | null) {
  if (!user) {
    localStorage.removeItem(USER_STORAGE_KEY)
    return
  }
  localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(user))
}

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(getStoredToken())
  const user = ref<CurrentUser | null>(loadStoredUser())
  const loading = ref(false)

  const isAuthenticated = computed(() => Boolean(token.value))
  const isAdmin = computed(() => user.value?.role === 'admin')

  async function loginAction(payload: LoginRequest) {
    loading.value = true
    try {
      const response = await login(payload)
      token.value = response.data.access_token
      user.value = response.data.user
      setStoredToken(response.data.access_token)
      saveStoredUser(response.data.user)
      return response.data.user
    } finally {
      loading.value = false
    }
  }

  async function fetchCurrentUser() {
    if (!token.value) return null
    const currentUser = await getCurrentUser()
    user.value = currentUser
    saveStoredUser(currentUser)
    return currentUser
  }

  function restoreFromStorage() {
    token.value = getStoredToken()
    user.value = loadStoredUser()
  }

  function logout() {
    token.value = null
    user.value = null
    clearStoredToken()
    saveStoredUser(null)
  }

  return {
    token,
    user,
    loading,
    isAuthenticated,
    isAdmin,
    loginAction,
    fetchCurrentUser,
    restoreFromStorage,
    logout,
  }
})
