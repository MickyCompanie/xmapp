<template>
    <header class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-base-200 p-4 sm:p-5 rounded-box shadow-sm border border-base-300">
        <div>
            <h2 class="text-xl sm:text-2xl font-extrabold text-primary">{{ props.title }}</h2>
            <p v-if="props.description" class="text-xs sm:text-sm text-neutral/70">{{ props.description }}</p>
        </div>
        
        
        <div class="flex items-center gap-2 sm:gap-3 w-full sm:w-auto justify-between sm:justify-end">
            <slot />
        </div>
    </header>
</template>

<script setup>
const props = defineProps({
    title: {
        type: String,
        required: true
    },
    description: {
        type: String,
        required: false,
        default: null
    }
})
</script>