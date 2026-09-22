import { apiFetch } from './api'

const authApi = {
  signup: async (data) => await apiFetch('/user/signup', {
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

    return await apiFetch('/auth/login', {
      method: 'POST',
      body
    })
  },

  getUser: async (tokenOverride = null) => {
    const options = {}
    if (tokenOverride) {
      options.headers = { Authorization: `Bearer ${tokenOverride}` }
    }
    return await apiFetch('/user/me', options)
  }
}

export { authApi }
export default authApi