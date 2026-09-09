<template>
  <div data-theme="christmas" class="min-h-screen bg-base-100 text-neutral font-sans flex flex-col md:flex-row relative overflow-x-hidden">

    <!-- HEADER (MOBILE) -->
    <Header 
      :is-mobile-menu-open="isMobileMenuOpen" 
      @update="updateMobileMenu" 
    />

    <!-- OVERLAY ASSOMBRI -->
    <div 
      v-if="isMobileMenuOpen" 
      @click="isMobileMenuOpen = false" 
      class="fixed inset-0 bg-black/50 z-40 md:hidden backdrop-blur-sm transition-opacity"
    ></div>

    <!-- SIDEBAR -->
    <Sidebar 
      :is-mobile-menu-open="isMobileMenuOpen" 
      :message="apiState.message" 
      :status="apiState.status" 
      :loading="apiState.loading"
      @close="isMobileMenuOpen = false"
    />

    <!-- CONTENU PRINCIPAL -->
    <main class="flex-1 p-4 sm:p-6 space-y-6 overflow-y-auto w-full">
      <slot />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const apiState = ref({
  loading: true,
  status: 'Inconnu',
  message: '',
  error: null
})

const fetchApiStatus = async () => {
  apiState.value.loading = true
  try {
    const response = await fetch('http://localhost:8000/')
    if (!response.ok) throw new Error(`Erreur HTTP: ${response.status}`)
    
    const data = await response.json()
    apiState.value = {
      loading: false,
      status: data.status,
      message: data.message,
      error: null
    }
  } catch (err) {
    apiState.value = {
      loading: false,
      status: 'offline',
      message: 'Impossible de contacter le serveur',
      error: err.message
    }
  }
}

onMounted(() => {
  fetchApiStatus()
})

const isMobileMenuOpen = ref(false)

function updateMobileMenu(val) {
  isMobileMenuOpen.value = val
}
</script>