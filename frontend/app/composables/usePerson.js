import { personApi } from '~/src/services/person'

export const usePerson = () => {
  const personsList = useState('persons_list', () => null)
  const personsSelect = useState('persons_select', () => null)
  const isLoadingPersons = useState('persons_loading', () => false)

  const fetchAllPersons = async () => {
    try {
      isLoadingPersons.value = true
      const data = await personApi.getAllPersons()
      personsList.value = data
      return data
    } catch (err) {
      personsList.value = []
      return []
    } finally {
      isLoadingPersons.value = false
    }
  }

  const fetchAllPersonSelect = async (forceRefresh = false) => {
    if (personsSelect.value !== null && !forceRefresh) {
      return personsSelect.value
    }

    try {
      isLoadingPersons.value = true
      const data = await personApi.getAllPersonsSelect()
      personsSelect.value = data
      return data
    } catch (err) {
      personsSelect.value = []
      return []
    } finally {
      isLoadingPersons.value = false
    }
  }

  return {
    personsList,
    personsSelect,
    isLoadingPersons,
    fetchAllPersons,
    fetchAllPersonSelect
  }
}