<template>
  <PageTitle title="Souhaits">
    <button @click="openCreateModal" class="btn btn-secondary btn-sm">
      + Ajouter un souhait
    </button>
  </PageTitle>

  <PageCard>
    <div v-if="isLoading" class="flex justify-center p-8">
      <span class="loading loading-spinner loading-lg text-primary"></span>
    </div>

    <div v-else-if="hasWishes" class="overflow-x-auto rounded-box border border-base-content/5 bg-base-100">
      <table class="table">
        <thead>
          <tr class="text-primary">
            <th v-for="head in wishesTable.tableHeads" :key="head" class="capitalize">
              {{ head }}
            </th>
            <th></th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="wishItem in wishesTable.wishes" 
            :key="wishItem.id"
            @click="openViewModal(wishItem)"
            class="cursor-pointer hover:bg-base-200/50 transition-colors"
          >
            <td v-for="attr in wishesTable.attributes" :key="attr">
              <template v-if="attr === 'price_estimate'">
                {{ wishItem[attr] ? `${wishItem[attr]} €` : '-' }}
              </template>

              <template v-else-if="['created_at', 'updated_at'].includes(attr)">
                {{ formatDate(wishItem[attr]) }}
              </template>

              <template v-else>
                {{ wishItem[attr] }}
              </template>
            </td>

            <td class="w-10">
              <button 
                v-if="alterPermission(wishItem.person_id)" 
                @click.stop="openEditModal(wishItem)" 
                class="btn btn-ghost btn-xs text-info"
              >
                Éditer
              </button>
            </td>

            <td class="w-10">
              <button 
                v-if="alterPermission(wishItem.person_id)" 
                @click.stop="handleDelete(wishItem.id)" 
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
      Aucun souhait enregistré pour le moment.
    </div>
  </PageCard>


  <Modal v-model="isViewModalOpen" :title="selectedWish?.title || 'Détails du souhait'">
    <div v-if="selectedWish" class="space-y-4">

      <div v-if="selectedWish.description" class="space-y-1">
        <p class="whitespace-pre-line text-sm p-4">
          {{ selectedWish.description }}
        </p>
      </div>

      <div v-if="selectedWish.url" class="space-y-1">
        <label class="font-medium text-sm text-base-content/70">Lien du produit</label>
        <div>
          <a :href="selectedWish.url" target="_blank" rel="noopener noreferrer" class="link link-primary text-sm break-all">
            {{ selectedWish.url }}
          </a>
        </div>
      </div>

      <div v-if="selectedWish.price_estimate" class="stat bg-base-200 rounded-box p-3">
        <div class="stat-title">Prix estimé</div>
        <div class="stat-value text-secondary text-2xl">{{ selectedWish.price_estimate }} €</div>
      </div>

      <div class="text-xs text-base-content/50 pt-2 border-t border-base-content/10 flex justify-between">
        <span>Créé le {{ formatDate(selectedWish.created_at) }}</span>
        <span v-if="selectedWish.updated_at">Mis à jour le {{ formatDate(selectedWish.updated_at) }}</span>
      </div>

      <div v-if="canCreateGift(selectedWish.person_id)" class="modal-action flex flex-col justify-between items-center">
          <button 
            @click="handleCreateGift(selectedWish)" 
            class="btn btn-secondary btn-sm gap-2 self-end"
          >
            🎁 Créer un cadeau
          </button>
      </div>
    </div>
  </Modal>

  <Modal v-model="isModalOpen" :title="isEditing ? 'Éditer le souhait' : 'Nouveau souhait'">
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <div class="form-control">
        <label class="label"><span class="label-text font-medium">Titre</span></label>
        <input v-model="form.title" type="text" class="input input-bordered w-full" placeholder="Ex: Montre connectée" required />
      </div>

      <div class="form-control">
        <label class="label"><span class="label-text font-medium">Prix estimé (€)</span></label>
        <input v-model.number="form.price_estimate" type="number" step="0.01" class="input input-bordered w-full" placeholder="199.99" />
      </div>

      <div class="form-control">
        <label class="label"><span class="label-text font-medium">Lien du produit</span></label>
        <input v-model="form.url" type="url" class="input input-bordered w-full" placeholder="https://..." />
      </div>

      <div class="form-control">
        <label class="label"><span class="label-text font-medium">Description</span></label>
        <textarea v-model="form.description" class="textarea textarea-bordered w-full" placeholder="Détails, couleur, taille..."></textarea>
      </div>

      <div class="modal-action">
        <button type="button" @click="isModalOpen = false" class="btn btn-ghost">
          Annuler
        </button>
        <button type="submit" class="btn btn-primary" :disabled="isLoading">
          <span v-if="isLoading" class="loading loading-spinner loading-xs"></span>
          <span v-else>{{ isEditing ? 'Enregistrer' : 'Créer' }}</span>
        </button>
      </div>
    </form>
  </Modal>
</template>

<script setup>
const { wishesTable, isLoading, fetchAllWishes, createWish, updateWish, deleteWishById } = useWish()
const { user } = useAuth()
const { success, error } = useToast()

const isModalOpen = ref(false)
const isViewModalOpen = ref(false)
const isEditing = ref(false)
const selectedWish = ref(null)

const form = reactive({
  id: null,
  title: '',
  description: '',
  url: '',
  price_estimate: null
})

const hasWishes = computed(() => {
  return Array.isArray(wishesTable.value?.wishes) && wishesTable.value.wishes.length > 0
})

const alterPermission = (personId) => {
  if (!user.value) return false
  if (user.value.role !== 'user') return true 
  return user.value.person?.id === personId
}

const canCreateGift = (wishPersonId) => {
  if (!user.value?.person?.id) return false
  return user.value.person.id !== wishPersonId
}

await useAsyncData('wishes-list', () => fetchAllWishes())

const openViewModal = (wishItem) => {
  selectedWish.value = wishItem
  isViewModalOpen.value = true
}

const resetForm = () => {
  form.id = null
  form.title = ''
  form.description = ''
  form.url = ''
  form.price_estimate = null
}

const openCreateModal = () => {
  isEditing.value = false
  resetForm()
  isModalOpen.value = true
}

const openEditModal = (wishItem) => {
  isEditing.value = true
  form.id = wishItem.id
  form.title = wishItem.title || ''
  form.description = wishItem.description || ''
  form.url = wishItem.url || ''
  form.price_estimate = wishItem.price_estimate ?? null
  isModalOpen.value = true
}

const handleSubmit = async () => {
  try {
    if (isEditing.value) {
      await updateWish(form)
      success('Souhait mis à jour !')
    } else {
      await createWish(form)
      success('Souhait créé avec succès !')
    }
    isModalOpen.value = false
  } catch (err) {
    error(err?.data?.detail || 'Une erreur est survenue.')
  }
}

const handleDelete = async (id) => {
  try {
    await deleteWishById(id)
    success('Souhait supprimé avec succès !')
  } catch (err) {
    error('Erreur lors de la suppression.')
  }
}

const handleCreateGift = async (wish) => {
    console.log('cadeau!')
  //try {
    // await createGiftFromWish(wish.id)
    //success(`Cadeau "${wish.title}" créé!`)
    //isViewModalOpen.value = false
  //} catch (err) {
    //error('Impossible de créer le cadeau.')
  //}
}
</script>