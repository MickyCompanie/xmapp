<template>
  <dialog ref="dialogRef" class="modal">
    <div class="modal-box relative">
      <button type="button" @click="close" class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
      <h3 v-if="title || $slots.title" class="text-lg font-bold mb-4">
        <slot name="title">{{ title }}</slot>
      </h3>

      <div>
        <slot />
      </div>

      <div v-if="$slots.actions" class="modal-action">
        <slot name="actions" :close="close" />
      </div>
    </div>


    <form method="dialog" class="modal-backdrop" @click.prevent="close">
      <button>close</button>
    </form>
  </dialog>
</template>

<script setup>
const isOpen = defineModel({ type: Boolean, default: false })

defineProps({
  title: {
    type: String,
    default: ''
  }
})

const dialogRef = ref(null)

const close = () => {
  isOpen.value = false
}

watch(isOpen, (val) => {
  if (val) {
    dialogRef.value?.showModal()
  } else {
    dialogRef.value?.close()
  }
})
</script>