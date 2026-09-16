<template>
    <div class="fixed bottom-5 right-5 z-50 flex flex-col gap-2 max-w-sm w-full pointer-events-none">
      <TransitionGroup name="toast">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          class="alert shadow-lg text-sm text-white pointer-events-auto flex items-center justify-between transition-all duration-300"
          :class="{
            'alert-success text-success-content': toast.type === 'success',
            'alert-error text-error-content': toast.type === 'error',
            'alert-info text-info-content': toast.type === 'info',
            'alert-warning text-warning-content': toast.type === 'warning'
          }"
        >
          <span>{{ toast.message }}</span>
          <button @click="remove(toast.id)" class="btn btn-xs btn-circle btn-ghost">✕</button>
        </div>
      </TransitionGroup>
    </div>
</template>

<script setup>
const { toasts, remove } = useToast()
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}
.toast-enter-from {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}
.toast-leave-to {
  opacity: 0;
  transform: translateX(100px);
}
</style>