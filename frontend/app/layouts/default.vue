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
      @close="isMobileMenuOpen = false"
    />

    <!-- CONTENU PRINCIPAL -->
    <main class="flex-1 p-4 sm:p-6 space-y-6 overflow-y-auto w-full">
      <slot />
    </main>

    <Toast />
  </div>
</template>

<script setup>

const { fetchUser } = useAuth()


const isMobileMenuOpen = ref(false)

function updateMobileMenu(val) {
  isMobileMenuOpen.value = val
}
</script>