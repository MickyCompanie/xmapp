// composables/useAuth.js
import { authApi } from '~/src/services/auth'
import { personApi } from '~/src/services/person'

export const useAuth = () => {
  // État réactif global conservé entre les pages
  const user = useState('auth_user', () => null)
  const isLoading = useState('auth_loading', () => false)


  const fetchUser = async () => {
    const token = useCookie('access_token')
    if (!token.value) {
      user.value = null
      return null
    }

    isLoading.value = true
    try {
      const data = await authApi.getUser()
      user.value = data
      return data
    } catch (err) {
      user.value = null
      authApi.clearTokens()
    } finally {
      isLoading.value = false
    }
  }


  const logout = () => {
    authApi.clearTokens()
    user.value = null
    navigateTo('/auth/login')
  }


  const initials = computed(() => {
    if (!user.value) return '?'
    const first = user.value.person?.first_name?.[0] || ''
    const last = user.value.person?.last_name?.[0] || ''
    return `${last}${first}`.toUpperCase() || 'U'
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
    fetchUser,
    updateProfile,
    logout
  }
}