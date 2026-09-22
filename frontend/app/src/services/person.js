import { apiFetch } from './api'


const personApi = {
    getAllPersons: () => apiFetch('/person'),

    getAllPersonsSelect: () => apiFetch('/person/list'),
    
    updatePerson: (body, id) => apiFetch(`/person/${id}`, { method: 'PUT', body })
}

export { personApi }
export default personApi