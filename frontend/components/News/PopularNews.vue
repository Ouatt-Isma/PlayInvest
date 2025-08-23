<template>
  <div class="py-16 max-w-7xl mx-auto px-4 md:px-8">
    <!-- Header -->
    <div class="flex justify-between items-center mb-8">
      <h2 class="text-3xl font-bold">🌟 Actualités populaires</h2>
      <NuxtLink
        to="/learn"
        @click.prevent="scrollToTopAndNavigate"
        class="text-sm font-medium border border-gray-300 px-4 py-2 rounded-lg hover:bg-gray-100 transition"
      >
        Voir tout
      </NuxtLink>
    </div>

    <!-- Famous News Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <a
        v-for="(anews, index) in famousNews.slice(0, 3)"
        :key="index"
        :href="`${anews.url}`"
        target="_blank"
        rel="noopener"
        class="block bg-white p-4 rounded-xl shadow-md hover:shadow-lg transition"
      >
        <img
          :src="`${apiBase}${anews.image_path}`"
          :alt="anews.title"
          class="w-full h-48 object-cover rounded-lg mb-4"
        />
        <h3 class="text-lg font-semibold mb-1">{{ anews.title }}</h3>
        <p class="text-sm text-gray-500 mb-2">
          {{ formatDate(anews.published_at) }}
          <span v-if="anews.audience"> • {{ anews.audience }}</span>
        </p>
        <p class="text-sm text-gray-600">
          {{ anews.resume?.slice(0, 200) }}<span v-if="anews.resume?.length > 200">...</span>
        </p>
        <p class="text-sm mt-2 text-blue-600 font-medium hover:underline">
          En savoir plus
        </p>
      </a>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const config = useRuntimeConfig()
const apiBase = config.public.apiBase

const router = useRouter()
const news = ref([])

// Fetch all news
onMounted(async () => {
  try {
    const token = useCookie("token").value
    const res = await axios.get(`${apiBase}/api/news`, {
      headers: { Authorization: `Bearer ${token}` },
    })
    news.value = res.data.sort((a, b) => new Date(b.published_at) - new Date(a.published_at))
  } catch (err) {
    console.error('❌ Erreur chargement news:', err)
  }
})

// Filter famous news only
const famousNews = computed(() => news.value.filter(anew => anew.famous))

// Format date
function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Intl.DateTimeFormat('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(new Date(dateStr))
}

// Scroll to top and navigate
function scrollToTopAndNavigate() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
  router.push('/news')
}
</script>
