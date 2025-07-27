<template>
  <a :href="`/Articles/${article.article_id}.html`" target="_blank" rel="noopener">
  <div class="flex gap-4 bg-white p-4 rounded-lg shadow-md">
    <img :src="`/Articles/${article.article_id}.png`" alt="Article Image" class="w-24 h-24 object-cover rounded" />
    <div class="flex flex-col justify-between">
      <h4 class="text-md font-semibold">{{ article.topic }}</h4>
      <p class="text-sm text-gray-500">
  {{ article.resume?.slice(0, 200) }}<span v-if="article.resume?.length > 200">...</span>
</p>
      <p class="text-sm text-gray-400">{{ formatDate(article.created_at) }}</p>

    </div>
  </div>
</a>
</template>

<script setup>
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
  article: {
    type: Object,
    required: true,
  },
})
</script>
