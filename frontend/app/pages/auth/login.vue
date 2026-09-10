<template>
  <div>
        <!-- Logo & En-tête -->
        <div class="text-center space-y-2 mb-4">
          <div class="w-12 h-12 rounded-full bg-secondary mx-auto flex items-center justify-center text-2xl shadow">
            <img 
                src="/logo-192.png" 
                alt="Logo xmapp" 
                class="w-8 h-8 object-contain drop-shadow-sm" 
              />
          </div>
          <h1 class="text-2xl font-black text-primary">Connexion</h1>
          <p class="text-xs text-neutral/70">Accédez à votre espace de gestion des fêtes</p>
        </div>

        <!-- Alerte d'erreur -->
        <div v-if="errorMessage" class="alert alert-error text-xs py-2 mb-2">
          <span>{{ errorMessage }}</span>
        </div>

        <!-- Formulaire -->
        <form @submit.prevent="handleLogin" class="space-y-4">
          <div class="form-control">
            <label class="label">
              <span class="label-text font-medium">Adresse e-mail</span>
            </label>
            <input 
              v-model="email" 
              type="email" 
              placeholder="lutin@noel.com" 
              class="input input-bordered w-full bg-base-100 focus:input-primary" 
              required 
            />
          </div>

          <div class="form-control">
            <label class="label flex justify-between">
              <span class="label-text font-medium">Mot de passe</span>
              <a href="#" class="text-xs text-primary hover:underline">Oublié ?</a>
            </label>
            <input 
              v-model="password" 
              type="password" 
              placeholder="••••••••" 
              class="input input-bordered w-full bg-base-100 focus:input-primary" 
              required 
            />
          </div>

          <button type="submit" class="btn btn-primary w-full mt-2" :disabled="isLoading">
            <span v-if="isLoading" class="loading loading-spinner"></span>
            <!-- Correction ici : v-else au lieu de v-else" -->
            <span v-else>Se connecter 🎅</span>
          </button>
        </form>

        <div class="divider my-4 text-xs text-neutral/50">OU</div>

        <!-- Lien Inscription -->
        <div class="text-center text-sm">
          <span class="text-neutral/70">Vous n'avez pas de compte ? </span>
          <NuxtLink to="/auth/signup" class="text-secondary font-bold hover:underline">
            Créer un compte
          </NuxtLink>
        </div>

  </div>
</template>

<script setup>

definePageMeta({
  layout: 'auth'
})

const email = ref('')
const password = ref('')
const isLoading = ref(false)
const errorMessage = ref('')

async function handleLogin() {
  isLoading.value = true
  errorMessage.value = ''
  
  // Logique d'authentification...
}
</script>