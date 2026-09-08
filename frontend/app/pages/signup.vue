<template>
  <div class="min-h-screen flex items-center justify-center p-4">
    <div class="card w-full max-w-md bg-base-200 border border-base-300 shadow-xl">
      <div class="card-body">
        <!-- Logo & En-tête -->
        <div class="text-center space-y-2 mb-2">
          <div class="w-12 h-12 rounded-full bg-secondary mx-auto flex items-center justify-center text-2xl shadow">
            🎁
          </div>
          <h1 class="text-2xl font-black text-secondary">Créer un compte</h1>
          <p class="text-xs text-neutral/70">Rejoignez l'équipe des lutins organisateurs</p>
        </div>

        <!-- Alerte d'erreur -->
        <div v-if="errorMessage" class="alert alert-error text-xs py-2 mb-2">
          <span>{{ errorMessage }}</span>
        </div>

        <!-- Formulaire -->
        <form @submit.prevent="handleSignup" class="space-y-3">
          <div class="form-control">
            <label class="label">
              <span class="label-text font-medium">Nom complet</span>
            </label>
            <input 
              v-model="form.fullName" 
              type="text" 
              placeholder="Nicolas de Myre" 
              class="input input-bordered w-full bg-base-100 focus:input-secondary" 
              required 
            />
          </div>

          <div class="form-control">
            <label class="label">
              <span class="label-text font-medium">Adresse e-mail</span>
            </label>
            <input 
              v-model="form.email" 
              type="email" 
              placeholder="lutin@noel.com" 
              class="input input-bordered w-full bg-base-100 focus:input-secondary" 
              required 
            />
          </div>

          <div class="form-control">
            <label class="label">
              <span class="label-text font-medium">Mot de passe</span>
            </label>
            <input 
              v-model="form.password" 
              type="password" 
              placeholder="••••••••" 
              class="input input-bordered w-full bg-base-100 focus:input-secondary" 
              required 
            />
          </div>

          <div class="form-control">
            <label class="label">
              <span class="label-text font-medium">Confirmer le mot de passe</span>
            </label>
            <input 
              v-model="form.confirmPassword" 
              type="password" 
              placeholder="••••••••" 
              class="input input-bordered w-full bg-base-100 focus:input-secondary" 
              required 
            />
          </div>

          <button type="submit" class="btn btn-secondary w-full mt-4" :disabled="isLoading">
            <span v-if="isLoading" class="loading loading-spinner"></span>
            <span v-else>S'inscrire ⭐</span>
          </button>
        </form>

        <div class="divider my-3 text-xs text-neutral/50">OU</div>

        <!-- Lien Connexion -->
        <div class="text-center text-sm">
          <span class="text-neutral/70">Vous avez déjà un compte ? </span>
          <NuxtLink to="/login" class="text-primary font-bold hover:underline">
            Se connecter
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="js" setup>
const form = reactive({
  fullName: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const isLoading = ref(false)
const errorMessage = ref('')

function handleSignup() {
  console.log('hihi')
}
</script>