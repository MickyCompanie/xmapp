import { wishApi } from '~/src/services/wish'

export const useWish = () => {
    const wishesTable = useState('wish_table', () => null)
    const wish = useState('wish', () => null)
    const isLoading = useState('wish_loading', () => false)


    const fetchAllWishes = async () => {
        try{
            isLoading.value = true 
            const data = await wishApi.getWishes()
            wishesTable.value = data 
        } catch(err) {
            wishesTable.value = null
            
        } finally {
            isLoading.value = false
        }
    }

    const fetchWishById = async (id) => {
        isLoading.value = true 

        try {
            const data = await wishApi.getWishById(id)
            wish.value = data 
        } catch (err) {
            wish.value = null
        } finally {
            isLoading.value = false
        }
    }


    const createWish = async (form) => {
        isLoading.value = true
        try { 
            await wishApi.createWish(form)
            return await fetchAllWishes()
        } finally {
        isLoading.value = false
        }
    }

    const updateWish = async (form) => {
        isLoading.value = true
        try { 
            await wishApi.updateWish(form, form.id)
            return await fetchAllWishes()
        } finally {
        isLoading.value = false
        }
    }

    const deleteWishById = async (id) => {
        isLoading.value = true 

        try {
            const data = await wishApi.deleteWish(id)
            return await fetchAllWishes()
        } finally {
            isLoading.value = false
        }
    }

  return {
    wishesTable,
    wish,
    isLoading,
    fetchAllWishes,
    fetchWishById,
    createWish,
    updateWish,
    deleteWishById,
  }
}