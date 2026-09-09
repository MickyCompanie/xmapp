import { apiFetch } from './api'

export const repaymentsApi = {
  getAll: () => apiFetch('/repayments'),
  getById: (id) => apiFetch(`/repayments/${id}`),
  create: (data) => apiFetch('/repayments', { method: 'POST', body: data }),
  delete: (id) => apiFetch(`/repayments/${id}`, { method: 'DELETE' }),
}