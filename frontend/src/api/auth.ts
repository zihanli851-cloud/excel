import http from './http'
import { isMockEnabled, mockGetCurrentUser, mockLogin } from './mock'

import type { CurrentUser, LoginRequest, LoginResponse } from '@/types/auth'

export async function login(payload: LoginRequest) {
  if (isMockEnabled) {
    return mockLogin(payload)
  }
  const { data } = await http.post<LoginResponse>('/auth/login', payload)
  return data
}

export async function getCurrentUser() {
  if (isMockEnabled) {
    return mockGetCurrentUser()
  }
  const { data } = await http.get<CurrentUser>('/auth/me')
  return data
}
