import { apiFetch } from './api'


const authApi = {

  setTokens: (tokens) => {
    const config = useRuntimeConfig()
    const accessTokenMaxAge = config.public.accessTokenExpiryMin * 60
    const refreshTokenMaxAge = config.public.refreshTokenExpiryDays * 24 * 60 * 60

    const accessToken = useCookie('access_token', {
      maxAge: accessTokenMaxAge,
      sameSite: 'lax',
      path: '/'
    })

    const refreshToken = useCookie('refresh_token', {
      maxAge: refreshTokenMaxAge,
      sameSite: 'lax',
      path: '/'
    })

    accessToken.value = tokens.access_token
    refreshToken.value = tokens.refresh_token
  },

  
  clearTokens: () => {
    const accessToken = useCookie('access_token')
    const refreshToken = useCookie('refresh_token')
    accessToken.value = null
    refreshToken.value = null
  },

  signup: (data) => apiFetch('/user/signup', {
    method: 'POST',
    body: {
      first_name: data.firstname,
      last_name: data.lastname,
      email: data.email,
      password: data.password
    }
  }),

  login: async (credentials) => {
    const body = new URLSearchParams()
    body.append('username', credentials.username || credentials.email)
    body.append('password', credentials.password)

    const response = await apiFetch('/auth/login', {
      method: 'POST',
      body
    })

    if (response?.access_token) {
      authApi.setTokens(response)
    }

    return response
  }
}

export { authApi }
export default authApi