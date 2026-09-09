import { apiFetch } from './api'

export const giftsApi = {
  getAll: () => apiFetch('/gifts'),
  create: (data) => apiFetch('/gifts', { method: 'POST', body: data }),
}