import { giftApi } from '~/src/services/gift'

export const useGift = () => {
  const giftsTable = useState('gift_table', () => null)
  const gift = useState('gift', () => null)
  const isLoading = useState('gift_loading', () => false)

  const fetchAllGifts = async () => {
    try {
      isLoading.value = true 
      const data = await giftApi.getGifts()
      giftsTable.value = data
      return data
    } catch(err) {
      giftsTable.value = null
      return null
    } finally {
      isLoading.value = false
    }
  }

  const fetchGiftById = async (id) => {
    isLoading.value = true 
    try {
      const data = await giftApi.getGiftById(id)
      gift.value = data 
      return data
    } catch (err) {
      gift.value = null
      return null
    } finally {
      isLoading.value = false
    }
  }

  const createGift = async (form) => {
    isLoading.value = true
    try { 
      await giftApi.createGift(form)
      return await fetchAllGifts()
    } finally {
      isLoading.value = false
    }
  }

  const createGiftFromWishId = async (id) => {
    isLoading.value = true
    try { 
      return await giftApi.createGiftFromWish(id)
    } finally {
      isLoading.value = false
    }
  }

  const updateGift = async (form) => {
    isLoading.value = true
    try { 
      await giftApi.updateGift(form, form.id)
      return await fetchAllGifts()
    } finally {
      isLoading.value = false
    }
  }

  const deleteGiftById = async (id) => {
    isLoading.value = true 
    try {
      await giftApi.deleteGift(id)
      return await fetchAllGifts()
    } finally {
      isLoading.value = false
    }
  }

  return {
    giftsTable,
    gift,
    isLoading,
    fetchAllGifts,
    fetchGiftById,
    createGift,
    createGiftFromWishId,
    updateGift,
    deleteGiftById,
  }
}