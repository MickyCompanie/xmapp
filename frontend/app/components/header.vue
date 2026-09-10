<template>
  <div class="md:hidden bg-base-200 border-b border-base-300 p-4 flex items-center justify-between sticky top-0 z-30 shadow-sm">
    
    <NuxtLink to="/" class="flex items-center gap-2 cursor-pointer select-none">
        <div class="w-8 h-8 rounded-full bg-secondary flex items-center justify-center text-white text-base font-bold shadow">
          <img 
                src="/logo-192.png" 
                alt="Logo xmapp" 
                class="w-6 h-6 object-contain drop-shadow-sm" 
              />
        </div>
        <span class="font-bold text-base text-primary">xmapp</span>
    </NuxtLink>

    <button 
      @click="toggleMenu" 
      class="btn btn-square btn-ghost btn-sm text-neutral"
      aria-label="Ouvrir le menu"
    >
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="inline-block w-6 h-6 stroke-current">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
      </svg>
    </button>
  </div>
</template>

<script setup>
const props = defineProps({
  isMobileMenuOpen: {
    type: Boolean,
    required: true
  }
})

const emit = defineEmits(['update'])

function toggleMenu() {
  emit('update', !props.isMobileMenuOpen)
}
</script>