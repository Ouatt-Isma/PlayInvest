<template>
  <a :href="`${anews.url}`" target="_blank" rel="noopener">
  <div class="flex gap-4 bg-white p-4 rounded-lg shadow-md">
    <img :src="`${apiBase}${anews.image_path}`"alt="News Image" class="w-24 h-24 object-cover rounded" />
    <div class="flex flex-col justify-between">
      <h4 class="text-md font-semibold">{{ anews.title }}</h4>
      <p class="text-sm text-gray-500">
  {{ anews.resume?.slice(0, 200) }}<span v-if="anews.resume?.length > 200">...</span>
</p>
      <p class="text-sm text-gray-400">{{ formatDate(anews.published_at) }}</p>
    </div>
  </div>
</a>
</template>

<script setup>
const config = useRuntimeConfig()
const apiBase = config.public.apiBase

function formatDate(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return new Intl.DateTimeFormat('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date)
}

defineProps({
  anews: {
    type: Object,
    required: true,
  },
})
</script>
