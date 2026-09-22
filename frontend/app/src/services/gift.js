import { apiFetch } from './api'

const giftApi = {
  getGifts: () => apiFetch('/gift'),

  getGiftById: (id) => apiFetch(`/gift/${id}`),

  createGift: (body) => apiFetch('/gift/', { method: 'POST', body }),

  createGiftFromWish: (id) => apiFetch(`/gift/${id}`, {method: 'POST'}),

  updateGift: (body, id) => apiFetch(`/gift/${id}`, { method: 'PUT', body}),

  deleteGift: (id) => apiFetch(`/gift/${id}`, {method: 'DELETE'})
}

export { giftApi }
export default giftApi