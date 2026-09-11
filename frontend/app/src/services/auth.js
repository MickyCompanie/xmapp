import { apiFetch } from './api'


const authApi = {
    signup: (data) => apiFetch('/user/signup', {
      method: 'POST',
      body: {
        first_name: data.firstname,
        last_name: data.lastname,
        email: data.email,
        password: data.password
      }
    }),

    login: (credentials) => {
    const body = new URLSearchParams()
    body.append('username', credentials.username || credentials.email)
    body.append('password', credentials.password)

    return apiFetch('/auth/login', {
      method: 'POST',
      body
    })
  }
}

export { authApi }
export default authApi