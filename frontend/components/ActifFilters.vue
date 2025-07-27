<script setup>

import { onMounted, ref, computed } from 'vue'
import axios from 'axios'
import { MagnifyingGlassIcon } from '@heroicons/vue/24/solid'


const assets = ref([])
const allAssets = ref([])
const filteredAssets = ref([])

const searchQuery = ref('')
const regionFilter = ref('')
const categoryFilter = ref('')
const performanceFilter = ref('')
const brvmFilter = ref('')
const graphPeriod = ref('7d')

const resetFilters = () => {
  console.log('reset')
  searchQuery.value = ''
  regionFilter.value = ''
  categoryFilter.value = ''
  performanceFilter.value = ''
  brvmFilter.value = ''
  graphPeriod.value = '7d'
  applyFilters()
}


// Appel API
const fetchAssets = async () => {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase 
  const response = await axios.get(`${apiBase}/api/assets`)
  allAssets.value = response.data
//   console.log(`URL ==== ${apiBase}/api/assets`)
//   console.log("RESPONSE HEADERS =", response.headers)
// console.log("RESPONSE DATA =", response.data)
// console.log("CONTENT-TYPE =", response.headers['content-type'])
//   console.log("[ACTIF FILTER]", allAssets.value )
//   console.log('API base URL =', config.public.apiBase)
  applyFilters()
}

const applyFilters = () => {
  let assets = [...allAssets.value]

  if (searchQuery.value) {
    assets = assets.filter(a => a.type?.toLowerCase().includes(searchQuery.value.toLowerCase()) || a.region?.toLowerCase().includes(searchQuery.value.toLowerCase()) || a.name?.toLowerCase().includes(searchQuery.value.toLowerCase()) || a.symbol?.toLowerCase().includes(searchQuery.value.toLowerCase() ))
  }


  if (brvmFilter.value) {
    assets = assets.filter(a => a.type?.toLowerCase().includes("brvm"))
  }

  if (regionFilter.value) {
    assets = assets.filter(a => a.region?.toLowerCase().includes(regionFilter.value.toLowerCase()))
  }

  if (categoryFilter.value) {
    assets = assets.filter(a => a.type?.toLowerCase().includes(categoryFilter.value.toLowerCase()))
  }

  if (performanceFilter.value === 'Meilleure Performance') {
    assets = assets.sort((a, b) => (b.variation_1d || 0) - (a.variation_1d || 0))
  } else if (performanceFilter.value === 'Moins bonne Performance') {
    assets = assets.sort((a, b) => (a.variation_1d || 0) - (b.variation_1d || 0))
  }

  filteredAssets.value = assets

  console.log('[ActifFilters] assets sélectionnée :', assets)
  emit('update:assets', assets) // ✅ emit to parent
  
}

const applyPeriodUpdate = () => {
  console.log('[ActifFilters] période sélectionnée :', graphPeriod.value)
  emit('update:graphPeriod', graphPeriod.value)
  applyFilters()
}

onMounted(() => {
  fetchAssets()
  
})

// watch([searchQuery, regionFilter, categoryFilter, performanceFilter, regionTab], applyFilters)

const emit = defineEmits(['update:assets', 'update:graphPeriod'])
// watch(graphPeriod, () => {
//   console.log('[ActifFilters] période sélectionnée :', graphPeriod.value)
//   emit('update:graphPeriod', graphPeriod.value)})
//   emit('update:assets', filteredAssets.value)

</script>


<template>
  <div class="p-6 bg-white rounded-xl shadow-md w-full max-w-full">
    <div class="flex flex-wrap items-center gap-4 mb-6">
      <!-- Search bar -->
      <div class="flex items-center px-4 py-3 border border-gray-300 rounded-xl w-full max-w-md bg-white">
        <input
          v-model="searchQuery"
          @input="applyFilters"
          type="text"
          placeholder="Rechercher un actif"
          class="flex-1 text-gray-600 focus:outline-none"
        />
        <MagnifyingGlassIcon class="w-5 h-5 text-gray-500" />
      </div>

      <!-- Dropdowns -->
      <select v-model="categoryFilter" @change="applyFilters" class="px-4 py-3 border border-gray-300 rounded-xl bg-white text-gray-700">
        <option disabled value="">Catégorie d'Actif</option>
        <option value="action">Actions</option>
        <option>Crypto</option>
        <option>ETF</option>
      </select>

      <select v-model="regionFilter" @change="applyFilters" class="px-4 py-3 border border-gray-300 rounded-xl bg-white text-gray-700">
        <option disabled value="">Région</option>
        <option >Afrique</option>
        <option value="États-Unis">USA</option>
        <option>Europe</option>
        <option>Monde</option>
      </select>

      <!-- <select v-model="performanceFilter" @change="applyFilters" class="px-4 py-3 border border-gray-300 rounded-xl bg-white text-gray-700">
        <option disabled selected>Performance</option>
        <option>Meilleure Performance</option>
        <option>Moins bonne Performance</option>
      </select> -->
      <span
        v-if="searchQuery || regionFilter || categoryFilter || performanceFilter || brvmFilter"
        @click="resetFilters"
        class="px-4 py-2 border border-gray-300 rounded-xl text-gray-600 hover:bg-gray-100"
      >
        Réinitialiser les filtres
    </span>
    </div>

    <!-- Region Tabs -->
    <div class="flex flex-wrap gap-4">
      <button :class="brvmFilter === 'true' ? 'bg-teal-700 text-white font-medium px-4 py-2 rounded-lg' : 'text-gray-700 hover:underline'"  @click="brvmFilter = 'true'; regionFilter = ''; categoryFilter=''; applyFilters()">
        Toutes les actions de la BRVM
      </button>
      <button :class="regionFilter === 'Afrique' ? 'bg-teal-700 text-white font-medium px-4 py-2 rounded-lg' : 'text-gray-700 hover:underline'" @click="regionFilter = 'Afrique'; brvmFilter = ''; applyFilters()" class="text-gray-700 hover:underline">Afrique</button>
      <button :class="regionFilter === 'Europe' ? 'bg-teal-700 text-white font-medium px-4 py-2 rounded-lg' : 'text-gray-700 hover:underline'" @click="regionFilter = 'Europe'; brvmFilter = '';applyFilters()">Europe</button>
      <button :class="regionFilter === 'États-Unis' ? 'bg-teal-700 text-white font-medium px-4 py-2 rounded-lg' : 'text-gray-700 hover:underline'" @click="regionFilter = 'États-Unis'; brvmFilter = ''; applyFilters()">USA</button>
      <button @click="regionFilter = 'Monde'; brvmFilter = ''; applyFilters()"  :class="regionFilter === 'Monde' ? 'bg-teal-700 text-white font-medium px-4 py-2 rounded-lg' : 'text-gray-700 hover:underline'"  >Monde</button>
      
      <button @click="categoryFilter = 'Crypto'; brvmFilter = ''; applyFilters()"  :class="categoryFilter === 'Crypto' ? 'bg-blue-500 text-white font-medium px-4 py-2 rounded-lg' : 'text-gray-700 hover:underline'" >Crypto</button>
      <button @click="categoryFilter = 'ETF'; brvmFilter = ''; applyFilters()" :class="categoryFilter === 'ETF' ? 'bg-blue-500 text-white font-medium px-4 py-2 rounded-lg' : 'text-gray-700 hover:underline'">ETF</button>
      <button @click="categoryFilter = 'action'; brvmFilter = ''; applyFilters()"   :class="categoryFilter === 'action' ? 'bg-blue-500 text-white font-medium px-4 py-2 rounded-lg' : 'text-gray-700 hover:underline'">Actions</button>

      <select v-model="performanceFilter" @change="applyFilters" class="px-4 py-3 border border-gray-300 rounded-xl bg-white text-gray-700">
          <option disabled value="">Performance</option>
          <option>Meilleure Performance</option>
          <option>Moins bonne Performance</option>
      </select>
      <div class="flex items-center gap-2">
    <label class="text-sm text-gray-600" >Période graphique :</label>
    <select @change="applyPeriodUpdate" v-model="graphPeriod" class="border px-2 py-1 rounded text-sm">
      <option value="7d">7 jours</option>
      <option value="1m">1 mois</option>
      <option value="3m">3 mois</option>
      <option value="6m">6 mois</option>
      <option value="1y">1 an</option>
      <option value="all">Tout</option>
    </select>
</div>
    </div>

    


  </div>
</template>
<!-- Performance -->


