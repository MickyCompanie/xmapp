// src/services/api.js

export const apiFetch = async (endpoint, options = {}) => {
  const accessToken = useCookie('access_token')
  const refreshToken = useCookie('refresh_token')
  const config = useRuntimeConfig()

  const headers = {
    ...options?.headers
  }

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
    const isUnauthorized = error?.status === 401 || error?.response?.status === 401

    if (isUnauthorized && refreshToken.value && endpoint !== '/auth/refresh') {
      try {
        const refreshResponse = await $fetch('/auth/refresh', {
          baseURL: config.public.apiBase,
          method: 'POST',
          body: { refresh_token: refreshToken.value }
        })

        if (refreshResponse?.access_token) {
          accessToken.value = refreshResponse.access_token
          if (refreshResponse?.refresh_token) {
            refreshToken.value = refreshResponse.refresh_token
          }

          headers.Authorization = `Bearer ${refreshResponse.access_token}`
          return await $fetch(endpoint, {
            baseURL: config.public.apiBase,
            ...options,
            headers
          })
        }
      } catch (refreshError) {
        accessToken.value = null
        refreshToken.value = null

        if (import.meta.client) {
          navigateTo('/auth/login')
        }
        throw refreshError
      }
    }

    throw error
  }
}