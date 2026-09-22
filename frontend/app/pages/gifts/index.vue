<template>
  <PageTitle title="Cadeaux">
    <button @click="openCreateModal" class="btn btn-secondary btn-sm">
      + Ajouter un cadeau
    </button>
  </PageTitle>

  <PageCard>
    <div v-if="isLoading" class="flex justify-center p-8">
      <span class="loading loading-spinner loading-lg text-primary"></span>
    </div>

    <div v-else-if="hasGifts" class="overflow-x-auto rounded-box border border-base-content/5 bg-base-100">
      <table class="table">
        <thead>
          <tr class="text-primary">
            <th v-for="head in giftsTable.tableHeads" :key="head" class="capitalize">
              {{ head }}
            </th>
            <th></th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="giftItem in giftsTable.gifts" 
            :key="giftItem.id"
            @click="openViewModal(giftItem)"
            class="cursor-pointer hover:bg-base-200/50 transition-colors"
          >
            <td v-for="attr in giftsTable.attributes" :key="attr">
              <template v-if="attr === 'price_paid'">
                {{ giftItem[attr] ? `${giftItem[attr]} €` : '-' }}
              </template>

              <template v-if="attr === 'status'">
                {{ giftItem[attr] ? `${ getStatusLabel(giftItem[attr])}` : '-' }}
              </template>

              <template v-else-if="['created_at', 'updated_at'].includes(attr)">
                {{ formatDate(giftItem[attr]) }}
              </template>

              <template v-else>
                {{ giftItem[attr] }}
              </template>
            </td>

            <td class="w-10">
              <button 
                v-if="alterPermission(giftItem.giver_id)" 
                @click.stop="openEditModal(giftItem)" 
                class="btn btn-ghost btn-xs text-info"
              >
                Éditer
              </button>
            </td>

            <td class="w-10">
              <button 
                v-if="alterPermission(giftItem.giver_id)" 
                @click.stop="handleDelete(giftItem.id)" 
                class="btn btn-ghost btn-xs text-error"
              >
                Supprimer
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else class="text-center py-8 text-base-content/60">
      Aucun cadeau enregistré pour le moment.
    </div>
  </PageCard>

  <Modal v-model="isViewModalOpen">
  <div v-if="selectedGift" class="space-y-4 pt-2">
    
    <!-- En-tête : Titre & Badge de statut -->
    <div class="flex items-center justify-between gap-3 border-b border-base-200 pb-3 mt-4">
      <h3 class="text-xl font-bold text-base-content">{{ selectedGift.title }}</h3>
      <span class="badge badge-lg font-medium" :class="getStatusBadgeClass(selectedGift.status)">
        {{ getStatusLabel(selectedGift.status) }}
      </span>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
      
      <div class="bg-base-200/50 p-3 rounded-lg">
        <span class="text-xs text-base-content/60 font-medium block uppercase tracking-wider">Pour (Destinataire)</span>
        <span class="font-semibold text-base">{{ getPersonName(selectedGift.receiver_id) }}</span>
      </div>

      <div class="bg-base-200/50 p-3 rounded-lg">
        <span class="text-xs text-base-content/60 font-medium block uppercase tracking-wider">Prix payé</span>
        <span class="font-semibold text-base text-primary">
          {{ selectedGift.price_paid ? `${selectedGift.price_paid} €` : 'Non renseigné' }}
        </span>
      </div>

    </div>

    <div class="text-xs text-base-content/50 pt-2 border-t border-base-content/10 flex justify-between">
      <span>Créé le {{ formatDate(selectedGift.created_at) }}</span>
      <span v-if="selectedGift.updated_at">Mis à jour le {{ formatDate(selectedGift.updated_at) }}</span>
    </div>

  </div>
</Modal>

  <Modal v-model="isModalOpen" :title="isEditing ? 'Éditer cadeau' : 'Nouveau cadeau'">
    <form @submit.prevent="handleSubmit" class="space-y-4 pt-2">
    
    <div class="form-control">
      <label class="label"><span class="label-text font-medium">Titre *</span></label>
      <input 
        v-model="form.title" 
        type="text" 
        maxlength="100" 
        placeholder="ex: Playstation 5" 
        class="input input-bordered w-full" 
        required 
      />
    </div>

    
    <div class="form-control">
      <label class="label"><span class="label-text font-medium">Pour qui ? (Destinataire) *</span></label>
      <select v-model="form.receiver_id" class="select select-bordered w-full" required>
        <option :value="null" disabled>Sélectionner...</option>
        <option v-for="person in personsSelect" :key="person.id" :value="person.id">
          {{ person.fullname }}
        </option>
      </select>
    </div>


    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div class="form-control">
        <label class="label"><span class="label-text font-medium">Prix payé (€)</span></label>
        <input 
          v-model.number="form.price_paid" 
          type="number" 
          step="0.01" 
          min="0" 
          placeholder="0.00" 
          class="input input-bordered w-full" 
        />
      </div>

      <div class="form-control">
        <label class="label"><span class="label-text font-medium">Statut *</span></label>
        <select v-model="form.status" class="select select-bordered w-full" required>
          <option v-for="st in GIFT_STATUSES" :key="st.value" :value="st.value">
            {{ st.label }}
          </option>
        </select>
      </div>
    </div>

    <div class="modal-action pt-4">
      <button type="button" @click="isModalOpen = false" class="btn btn-ghost">
        Annuler
      </button>
      <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
        <span v-if="isSubmitting" class="loading loading-spinner loading-xs"></span>
        {{ isEditing ? 'Enregistrer les modifications' : 'Créer le cadeau' }}
      </button>
    </div>
  </form>
  </Modal> 
</template>

<script setup>
const { giftsTable, isLoading, fetchAllGifts, fetchGiftById, createGift, updateGift, deleteGiftById } = useGift()
const { fetchAllPersons, personsSelect, fetchAllPersonSelect, isLoadingPersons} = usePerson()
const { user } = useAuth()
const { success, error } = useToast()

const isModalOpen = ref(false)
const isViewModalOpen = ref(false)
const isEditing = ref(false)
const isSubmitting = ref(false)
const selectedGift = ref(null)


const GIFT_STATUSES = [
  { value: 'pending', label: 'En attente' },
  { value: 'reserved', label: 'Réservé' },
  { value: 'bought', label: 'Acheté' },
  { value: 'wrapped', label: 'Emballé' },
  { value: 'under_tree', label: 'Sous le sapin' },
  { value: 'given', label: 'Offert' }
]

const form = reactive({
  id: null,
  title: '',
  price_paid: null,
  giver_id: null,
  receiver_id: null,
  wish_id: null,
  status: 'pending'
})

const resetForm = () => {
  form.id = null
  form.title = ''
  form.price_paid = null
  form.giver_id = null
  form.receiver_id = null
  form.wish_id = null
  form.status = 'pending'
}

const getStatusBadgeClass = (statusKey) => {
  switch (statusKey) {
    case 'pending': return 'badge-warning'
    case 'reserved': return 'badge-info'
    case 'bought': return 'badge-primary'
    case 'wrapped': return 'badge-secondary'
    case 'under_tree': return 'badge-accent'
    case 'given': return 'badge-success'
    default: return 'badge-ghost'
  }
}

const getStatusLabel = (statusKey) => {
  const found = GIFT_STATUSES.find(s => s.value === statusKey)
  return found ? found.label : statusKey
}

const getPersonName = (personId) => {
  if (!personId) return 'Non assigné'
  const person = personsSelect.value?.find(p => p.id === personId)
  return person ? person.fullname : `ID: ${personId}`
}

const hasGifts = computed(() => {
  return Array.isArray(giftsTable.value?.gifts) && giftsTable.value.gifts.length > 0
})

const alterPermission = (personId) => {
  if (!user.value) return false
  if (user.value.role !== 'user') return true 
  return user.value.person?.id === personId
}

await useAsyncData('gift-page-data', async () => {
  await Promise.all([
    fetchAllGifts(),
    fetchAllPersonSelect(true)
  ])
})

const openViewModal = (giftItem) => {
  console.log(giftItem)
  selectedGift.value = giftItem
  isViewModalOpen.value = true
}

const openCreateModal = () => {
  isEditing.value = false
  resetForm()
  isModalOpen.value = true
}

const openEditModal = (giftItem) => {
  isEditing.value = true
  form.id = giftItem.id
  form.title = giftItem.title || ''
  form.price_paid = giftItem.price_paid ?? null
  form.giver_id = giftItem.giver_id ?? null
  form.receiver_id = giftItem.receiver_id ?? null
  form.wish_id = giftItem.wish_id ?? null
  form.status = giftItem.status || 'pending'
  isModalOpen.value = true
}

const handleSubmit = async () => {
  try {
    isSubmitting.value = true

    if (isEditing.value) {
      await updateGift(form)
      success('Cadeau mis à jour avec succès')
    } else {
      await createGift(form)
      success('Cadeau ajouté avec succès')
    }

    isModalOpen.value = false
    await fetchAllGifts()
  } catch (err) {
    showError(err.message || 'Une erreur est survenue')
  } finally {
    isSubmitting.value = false
  }
}

const handleDelete = async (id) => {
  try {
    await deleteGiftById(id)
    success('cadeau supprimé avec succès !')
  } catch (err) {
    error('Erreur lors de la suppression.')
  }
}

</script>