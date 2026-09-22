// composables/useAuth.js
import { authApi } from '~/src/services/auth'
import { personApi } from '~/src/services/person'

export const useAuth = () => {
  const user = useState('auth_user', () => null)
  const isLoading = useState('auth_loading', () => false)

  const config = useRuntimeConfig()
  const accessMaxAge = (config.public?.accessTokenExpiryMin || 60) * 60
  const refreshMaxAge = (config.public?.refreshTokenExpiryDays || 7) * 24 * 60 * 60

  const accessToken = useCookie('access_token', {
    maxAge: accessMaxAge,
    sameSite: 'lax',
    path: '/'
  })

  const refreshToken = useCookie('refresh_token', {
    maxAge: refreshMaxAge,
    sameSite: 'lax',
    path: '/'
  })

  const setTokens = (tokens) => {
    if (tokens?.access_token) accessToken.value = tokens.access_token
    if (tokens?.refresh_token) refreshToken.value = tokens.refresh_token
  }

  const clearTokens = () => {
    accessToken.value = null
    refreshToken.value = null
  }

  const fetchUser = async (tokenOverride = null) => {
    const activeToken = tokenOverride || accessToken.value

    if (!activeToken) {
      user.value = null
      return null
    }

    isLoading.value = true
    try {
      const data = await authApi.getUser(tokenOverride)
      user.value = data
      return data
    } catch (err) {
      const status = err?.status || err?.response?.status
      if (status === 401) {
        clearTokens()
        user.value = null
      }
      
      return null
      clearTokens()
      return null
    } finally {
      isLoading.value = false
    }
  }

  const login = async (credentials) => {
    isLoading.value = true
    try {
      const response = await authApi.login(credentials)
      if (response?.access_token) {
        setTokens(response)
        await fetchUser(response.access_token)
      }
      return response
    } catch (err) {
      clearTokens()
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const logout = () => {
    clearTokens()
    user.value = null
    navigateTo('/auth/login')
  }

  const initials = computed(() => {
    if (!user.value) return '?'
    const first = user.value.person?.first_name?.[0] || ''
    const last = user.value.person?.last_name?.[0] || ''
    return `${first}${last}`.toUpperCase() || 'U'
  })

  const updateProfile = async (form) => {
    isLoading.value = true
    try { 
      await personApi.updatePerson(form, user.value.person.id)
      return await fetchUser()
    } finally {
      isLoading.value = false
    }
  }

  return {
    user,
    isLoading,
    initials,
    login,
    fetchUser,
    updateProfile,
    logout
  }
}