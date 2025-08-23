<template>
  <div class="py-16 max-w-7xl mx-auto px-4 md:px-8">
    <!-- Header -->
    <div class="flex justify-between items-center mb-8">
      <h2 class="text-3xl font-bold">📰 Derniers articles</h2>
      <NuxtLink
        to="/learn"
        @click.prevent="scrollToTopAndNavigate"
        class="text-sm font-medium border border-gray-300 px-4 py-2 rounded-lg hover:bg-gray-100 transition"
      >
        Voir tout
      </NuxtLink>
    </div>

    <!-- Article Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <a
  v-for="(article, index) in articles.slice(0, 3)"
  :key="index"
  :href="`/Articles/${article.article_id}.html`"
  target="_blank"
  rel="noopener"
  class="block bg-white p-4 rounded-xl shadow-md hover:shadow-lg transition"
>
  <img
    :src="`/Articles/${article.article_id}.png`"
    :alt="article.topic"
    class="w-full h-48 object-cover rounded-lg mb-4"
  />
  <h3 class="text-lg font-semibold mb-1">{{ article.topic }}</h3>
  <p class="text-sm text-gray-500 mb-2">
    {{ formatDate(article.created_at) }}<span v-if="article.audience"> • {{ article.audience }}</span>
  </p>
  <p class="text-sm text-gray-600">
    {{ article.resume?.slice(0, 200) }}<span v-if="article.resume?.length > 200">...</span>
  </p>
  <p class="text-sm mt-2 text-blue-600 font-medium hover:underline">
    En savoir plus
  </p>
</a>

      <!-- <NuxtLink
        v-for="(article, index) in articles.slice(0, 3)"
        :key="index"
        :to="`/Articles/${article.article_id}.html`"
        class="block bg-white p-4 rounded-xl shadow-md hover:shadow-lg transition"
      >
        <img
          :src="`/Articles/${article.article_id}.png`"
          :alt="article.topic"
          class="w-full h-48 object-cover rounded-lg mb-4"
        />
        <h3 class="text-lg font-semibold mb-1">{{ article.topic }}</h3>
        <p class="text-sm text-gray-500 mb-2">
          {{ formatDate(article.created_at) }}<span v-if="article.audience"> • {{ article.audience }}</span>
        </p>
        <p class="text-sm text-gray-600">
          {{ article.resume?.slice(0, 200) }}<span v-if="article.resume?.length > 200">...</span>
        </p>
        <p class="text-sm mt-2 text-blue-600 font-medium hover:underline">
          En savoir plus
        </p>
      </NuxtLink> -->
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const config = useRuntimeConfig()
const apiBase = config.public.apiBase

const router = useRouter()
const articles = ref([])

onMounted(async () => {
  try {
    const token = useCookie("token").value
    const res = await axios.get(`${apiBase}/api/articles`, {
      headers: { Authorization: `Bearer ${token}` },
    })
    articles.value = res.data
      .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
  } catch (err) {
    console.error('❌ Erreur chargement articles:', err)
  }
})

function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Intl.DateTimeFormat('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(new Date(dateStr))
}

function scrollToTopAndNavigate() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
  router.push('/learn')
}
</script>
