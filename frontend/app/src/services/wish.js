import { apiFetch } from './api'


const wishApi = {
    getWishes: async () => await apiFetch('/wish'),

    getWishById: async (id) => await apiFetch(`/wish/${id}`),

    createWish: async (body) => await apiFetch('/wish/', { method: 'POST', body: body}),

    updateWish: async (body, id) => await apiFetch(`/wish/${id}`, { method: 'PUT', body: body}),

    deleteWish: async (id) => await apiFetch(`/wish/${id}`, {method: 'DELETE'})
}

export { wishApi }
export default wishApi