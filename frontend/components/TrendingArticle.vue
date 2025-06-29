<template>
  <div class="flex gap-4 bg-white p-4 rounded-lg shadow-md">
    <img :src="article.image" alt="Article Image" class="w-24 h-24 object-cover rounded" />
    <div class="flex flex-col justify-between">
      <h4 class="text-md font-semibold">{{ article.title }}</h4>
      <p class="text-sm text-gray-500">Rédigé par {{ article.author }}</p>
      <p class="text-sm text-gray-400">{{ article.date }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  article: {
    type: Object,
    required: true,
  },
})
</script>
