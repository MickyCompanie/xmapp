// src/services/api.js
import { authApi } from './auth'

export const apiFetch = async (endpoint, options = {}) => {
  const accessToken = useCookie('access_token')
  const refreshToken = useCookie('refresh_token')
  const config = useRuntimeConfig()

  const headers = { ...options?.headers }
  if (accessToken.value) {
    headers.Authorization = `Bearer ${accessToken.value}`
  }

  try {
    return await $fetch(endpoint, {
      baseURL: config.public.apiBase,
      ...options,
      headers
    })
  } catch (error) {
    // Access Token expired
    if (error?.status === 401 && refreshToken.value && endpoint !== '/auth/refresh') {
      try {
        const refreshResponse = await $fetch('/auth/refresh', {
          baseURL: config.public.apiBase,
          method: 'POST',
          body: { refresh_token: refreshToken.value }
        })

        authApi.setTokens(refreshResponse)

        headers.Authorization = `Bearer ${refreshResponse.access_token}`
        return await $fetch(endpoint, {
          baseURL: config.public.apiBase,
          ...options,
          headers
        })
      } catch (refreshError) {
        // Refresh token expired
        authApi.clearTokens()
        navigateTo('/auth/login')
        throw refreshError
      }
    }
    throw error
  }
}