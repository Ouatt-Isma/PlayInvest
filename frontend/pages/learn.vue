<template>
  <section class="py-16 max-w-7xl mx-auto px-4 md:px-8 flex flex-col-reverse md:flex-row items-center gap-12">
    <div class="container mx-auto px-4 w-full">
      <h1 class="text-4xl font-bold mb-8">Apprendre à investir avec Play Invest</h1>

      <!-- Filters -->
      <div class="flex flex-col md:flex-row items-center gap-4 mb-8 flex-wrap">
        <!-- Region -->
        <select v-model="selectedRegion" class="border p-2 rounded">
          <option value="Tous">🌍 Tous</option>
          <option value="Afrique">🌍 Afrique</option>
          <option value="Autres">🌎 Autres</option>
        </select>

        <!-- Search -->
        <input
          v-model="searchText"
          type="text"
          placeholder="🔍 Rechercher un article"
          class="border p-2 rounded w-full md:w-1/2"
        />

        <!-- Checkboxes -->
        <div class="flex items-center gap-4">
          <!-- 📅 Récent (Sort) -->
          <label class="inline-flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              v-model="sortRecent"
              class="form-checkbox text-blue-600"
            />
            <span class="text-sm">📅 Récent</span>
          </label>

          <!-- 🔥 Populaire (Filter) -->
          <label class="inline-flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              v-model="filterFamous"
              class="form-checkbox text-blue-600"
            />
            <span class="text-sm">🔥 Populaire</span>
          </label>
        </div>
      </div>

      <!-- Article Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <!-- Featured -->
        <div class="mb-12">
          <FeaturedSlider />
        </div>

        <!-- Trending Articles -->
        <div>
          <h2 class="text-2xl font-semibold mb-4">Articles tendances</h2>
          <div class="flex flex-col gap-4">
            <TrendingArticle
              v-for="(article, index) in paginatedArticles"
              :key="index"
              :article="article"
            />
          </div>

          <!-- Pagination -->
          <div
            v-if="totalPages > 1"
            class="mt-6 flex justify-center gap-4 items-center"
          >
            <button
              @click="currentPage--"
              :disabled="currentPage === 1"
              class="px-3 py-1 rounded bg-gray-200 hover:bg-gray-300 disabled:opacity-50"
            >
              ← Précédent
            </button>

            <span class="font-medium text-sm">
              Page {{ currentPage }} sur {{ totalPages }}
            </span>

            <button
              @click="currentPage++"
              :disabled="currentPage === totalPages"
              class="px-3 py-1 rounded bg-gray-200 hover:bg-gray-300 disabled:opacity-50"
            >
              Suivant →
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Additional Sections -->
  <LatestArticles />
  <PopularArticles />
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'

// Components
import FeaturedSlider from '~/components/Articles/FeaturedSlider.vue'
import TrendingArticle from '~/components/Articles/TrendingArticle.vue'
import LatestArticles from '~/components/Articles/LatestArticles.vue'
import PopularArticles from '~/components/Articles/PopularArticles.vue'

// Runtime config
const config = useRuntimeConfig()
const apiBase = config.public.apiBase

// State
const allArticles = ref([])
const selectedRegion = ref('Tous')
const searchText = ref('')
const sortRecent = ref(false)
const filterFamous = ref(false)

// Pagination
const currentPage = ref(1)
const perPage = 4

// Fetch articles
onMounted(async () => {
  const token = localStorage.getItem('token')
  try {
    const res = await axios.get(`${apiBase}/api/articles`, {
      headers: { Authorization: `Bearer ${token}` },
    })
    allArticles.value = res.data
  } catch (err) {
    console.error('❌ Erreur lors du chargement des articles', err)
  }
})

// Filter and optionally sort
const filteredArticles = computed(() => {
  let articles = [...allArticles.value]

  // Filter: Region and search
  articles = articles.filter((article) => {
    const inAfrique = article.category?.toLowerCase().includes('afrique')
    const matchesRegion =
      selectedRegion.value === 'Tous' ||
      (selectedRegion.value === 'Afrique' ? inAfrique : !inAfrique)

    const matchesText = article.topic
      ?.toLowerCase()
      .includes(searchText.value.toLowerCase())
    console.log(matchesRegion && matchesText)
    return matchesRegion && matchesText
  })

  // Filter: Populaire
  if (filterFamous.value) {
    articles = articles.filter((a) => a.famous === true)
  }

  // Sort: Récent
  if (sortRecent.value) {
    articles.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
  }

  return articles
})

// Paginate
const paginatedArticles = computed(() => {
  const start = (currentPage.value - 1) * perPage
  return filteredArticles.value.slice(start, start + perPage)
})

const totalPages = computed(() =>
  Math.ceil(filteredArticles.value.length / perPage)
)

// Reset page when filters change
watch([selectedRegion, searchText, sortRecent, filterFamous], () => {
  currentPage.value = 1
})
</script>
