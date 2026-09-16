import { apiFetch } from './api'


const personApi = {
    updatePerson: (body, id) => apiFetch(`/person/${id}`, {
        method: 'PUT',
        body: body
  })
}

export { personApi }
export default personApi