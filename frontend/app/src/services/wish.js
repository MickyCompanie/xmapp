import { apiFetch } from './api'


const wishApi = {
    getWishes: () => apiFetch('/wish'),

    getWishById: (id) => apiFetch(`/wish/${id}`),

    createWish: (body) => apiFetch('/wish/', { method: 'POST', body}),

    updateWish: (body, id) => apiFetch(`/wish/${id}`, { method: 'PUT', body}),

    deleteWish: (id) => apiFetch(`/wish/${id}`, {method: 'DELETE'})
}

export { wishApi }
export default wishApi