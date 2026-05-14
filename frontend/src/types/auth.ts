export interface CurrentUser {
  id: number
  username: string
  display_name?: string | null
  role: 'admin' | 'viewer' | string
  is_active: boolean
}

export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  success: boolean
  data: {
    access_token: string
    token_type: string
    user: CurrentUser
  }
}
