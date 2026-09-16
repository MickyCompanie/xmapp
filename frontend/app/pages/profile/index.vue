<template>
    <PageTitle title="profile" />
    <PageCard>
        <form @submit.prevent="handleSubmit" class="space-y-4 flex flex-col">
          <!-- Prénom -->
          <div class="form-control">
            <label class="label"><span class="label-text font-medium">Prénom</span></label>
            <input 
              v-model="form.first_name" 
              type="text" 
              class="input input-bordered w-full" 
              placeholder="Jean"
              required 
            />
          </div>
    
          <!-- Nom -->
          <div class="form-control">
            <label class="label"><span class="label-text font-medium">Nom</span></label>
            <input 
              v-model="form.last_name" 
              type="text" 
              class="input input-bordered w-full" 
              placeholder="Dupont"
              required 
            />
          </div>
    
          <!-- Date de naissance -->
          <div class="form-control">
            <label class="label"><span class="label-text font-medium">Date de naissance</span></label>
            <input 
              v-model="form.birth_date" 
              type="date" 
              class="input input-bordered w-full" 
            />
          </div>
    
          <!-- Bouton d'enregistrement -->
          <button 
            type="submit" 
            class="btn btn-primary w-min-4 px-6 py-2 mt-2 self-end" 
            :disabled="isLoading"
          >
            <span v-if="isLoading" class="loading loading-spinner loading-sm"></span>
            <span v-else>Mettre à jour</span>
          </button>
        </form>
    </PageCard>
</template>

<script setup>
const { user, updateProfile, isLoading } = useAuth()
const { success, error } = useToast()

const form = reactive({
  first_name: '',
  last_name: '',
  birth_date: '',
  id: '',
})

const formatDateForInput = (dateStr) => {
  if (!dateStr) return ''
  return dateStr.split('T')[0]
}

watch(() => user.value, (newUser) => {
  if (newUser?.person) {
    form.first_name = newUser.person.first_name 
    form.last_name = newUser.person.last_name 
    form.birth_date = formatDateForInput(newUser.person.birth_date)
    form.id = newUser.person.id 
  }
}, { immediate: true })

const handleSubmit = async () => {
  try {
    await updateProfile(form)
    success('Profil mis à jour avec succès !')
    navigateTo('/')
  } catch (err) {
    error(err?.data?.detail || 'Erreur lors de la mise à jour.')
  }
}
</script>