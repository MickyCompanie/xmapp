<template>
  <aside 
    :class="[
      'fixed inset-y-0 left-0 z-50 w-64 bg-base-200 border-r border-base-300 p-4 flex flex-col justify-between transition-transform duration-300 ease-in-out md:static md:translate-x-0 md:z-auto',
      isMobileMenuOpen ? 'translate-x-0 shadow-2xl' : '-translate-x-full'
    ]"
  >
    <div class="space-y-6">
      <!-- Logo & Titre -->
      <NuxtLink 
        to="/" 
        class="flex items-center justify-between px-2 cursor-pointer select-none" 
      >
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-full bg-secondary flex items-center justify-center text-white text-xl font-bold shadow">
              <img 
                src="/logo-192.png" 
                alt="Logo xmapp" 
                class="w-6 h-6 object-contain drop-shadow-sm" 
              />
            </div>
            <div>
              <h1 class="font-bold text-lg text-primary leading-tight">xmapp</h1>
              <span class="text-xs text-neutral/70">Gestion de Noël</span>
            </div>
          </div>
          <button @click="emit('close')" class="btn btn-sm btn-circle btn-ghost md:hidden">✕</button>
      </NuxtLink>

      <!-- Menu Navigation -->
      <ul class="menu bg-base-100 rounded-box p-2 gap-1 shadow-sm">
        <li v-for="item in NAV_ITEMS" :key="item.to" >
          <NuxtLink
            :to="item.to"
            @click="emit('close')"
            class="active:!bg-accent active:!text-primary-content"
            active-class="active !bg-primary !text-secondary-content font-semibold"
          >
            <span>{{ item.icon }} </span>
            <span class="ml-1">{{ item.label }}</span>
          </NuxtLink>
        </li>
      </ul>
    </div>

    <!-- Footer Sidebar -->

    <!-- CARTE PROFIL CLIQUABLE -->
      
    <div class="p-3 bg-base-300/50 rounded-box text-xs text-center mt-6 md:mt-0 space-y-1">
      <div class="my-2 flex items-center justify-between gap-1 p-2 rounded-xl bg-base-100 border border-base-300/60 shadow-sm">
  

      <NuxtLink 
        to="/profile" 
        @click="emit('close')"
        class="flex items-center gap-3 flex-1 min-w-0 p-1 rounded-lg hover:bg-base-200/60 transition-all cursor-pointer select-none group"
      >
        <!-- Avatar (Initiales ou Image) -->
        <div class="avatar placeholder">
          <div class="bg-primary text-primary-content rounded-full w-9 ring ring-primary ring-offset-base-100 ring-offset-1">
            <span class="text-xs font-bold">JD</span>
          </div>
        </div>

        <!-- Nom & Lien -->
        <div class="flex-1 min-w-0">
          <p class="text-sm font-semibold truncate group-hover:text-primary transition-colors">
            John Doe
          </p>
          <p class="text-[11px] text-neutral/60 truncate">
            Mon profil
          </p>
        </div>
      </NuxtLink>

      <!-- Bouton de déconnexion -->
      <button 
        type="button" 
        @click="handleLogout"
        title="Déconnexion"
        class="p-2 rounded-lg text-neutral/50 hover:text-error hover:bg-error/10 transition-colors flex items-center justify-center"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
          <polyline points="16 17 21 12 16 7" />
          <line x1="21" y1="12" x2="9" y2="12" />
        </svg>
      </button>
    </div>
      
      <div class="flex items-center justify-between">
        <span>Statut API :</span>
        <span v-if="loading" class="badge badge-warning badge-sm">Connexion...</span>
        <span v-else-if="status !== 'offline'" class="badge badge-success badge-sm font-semibold">
          {{ status }}
        </span>
        <span v-else class="badge badge-error badge-sm text-white">Hors ligne</span>
      </div>
      <p v-if="message" class="text-[10px] text-neutral/70 truncate">
        {{ message }}
      </p>
    </div>
  </aside>
</template>

<script setup>
import authApi from '~/src/services/auth'

const props = defineProps({
  isMobileMenuOpen: {
    type: Boolean,
    required: true,
    default: false,
  },
  message: {
    type: String,
    default: ''
  },
  status: {
    type: String,
    default: 'Inconnu'
  },
  loading: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['close'])

const handleLogout = () => {
  emit('close')
  authApi.clearTokens()
  navigateTo('/auth/login')
}
</script>