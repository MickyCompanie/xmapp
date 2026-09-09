<template>
  <aside 
    :class="[
      'fixed inset-y-0 left-0 z-50 w-64 bg-base-200 border-r border-base-300 p-4 flex flex-col justify-between transition-transform duration-300 ease-in-out md:static md:translate-x-0 md:z-auto',
      isMobileMenuOpen ? 'translate-x-0 shadow-2xl' : '-translate-x-full'
    ]"
  >
    <div class="space-y-6">
      <!-- Logo & Titre -->
      <NuxtLink to="/" class="flex items-center justify-between px-2 cursor-pointer select-none" >
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-full bg-primary flex items-center justify-center text-white text-xl font-bold shadow">
              🎄
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
            active-class="active bg-primary text-primary-content font-semibold"
          >
            <span>{{ item.icon }} </span>
            <span class="ml-1">{{ item.label }}</span>
          </NuxtLink>
        </li>
      </ul>
    </div>

    <!-- Footer Sidebar -->
    <div class="p-3 bg-base-300/50 rounded-box text-xs text-center mt-6 md:mt-0 space-y-1">
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
</script>