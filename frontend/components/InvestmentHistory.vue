<template>
  <div class="bg-white p-6 rounded-xl shadow-md">
    <h2 class="text-xl font-semibold mb-4">Historique des Investissements</h2>

    <!-- Search bar -->
    <div class="flex items-center justify-between mb-4">
      <input
        v-model="search"
        type="text"
        placeholder="Rechercher..."
        class="border border-gray-300 rounded px-4 py-2 w-full max-w-sm"
      />
      <button class="ml-4 text-gray-600 hover:text-black">
        <MagnifyingGlassIcon class="w-5 h-5" />
      </button>
    </div>

    <!-- Table -->
    <table class="w-full table-auto text-left">
      <thead class="bg-blue-50">
        <tr>
          <th class="px-4 py-2">Date</th>
          <th class="px-4 py-2">Nom de l’actif</th>
          <th class="px-4 py-2">Montant investi</th>
          <th class="px-4 py-2">Type de transaction</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(item, index) in displayedHistory"
          :key="index"
          :class="[
            'border-t',
            item.transaction_type === 'buy' ? 'bg-blue-50' :
            item.transaction_type === 'sell' ? 'bg-red-50' : ''
          ]"
        >
          <td class="px-4 py-2">{{ formatDate(item.date) }}</td>
          <td class="px-4 py-2">
            {{ item.asset_name }}
            <span class="text-gray-500 font-semibold ml-1">{{ item.symbol }}</span>
          </td>
          <td class="px-4 py-2">{{ formatCurrency(item.amount_invested, item.currency) }}</td>
          <td class="px-4 py-2 capitalize">
            {{ item.transaction_type === 'buy' ? 'Achat' : item.transaction_type === 'sell' ? 'Vente' : 'Autre' }}
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Filters and Load More -->
    <div class="mt-4 text-center">
      <div class="flex items-center justify-center gap-4 mb-2">
        <input
          v-model="selectedDate"
          type="date"
          class="border border-gray-300 rounded px-2 py-1 text-sm"
        />
        <button
          @click="() => { selectedDate = ''; visibleCount = 5 }"
          class="text-sm text-gray-600 hover:text-black"
        >
          Réinitialiser
        </button>
      </div>

      <button
        v-if="visibleCount < filteredData.length"
        @click="visibleCount += 5"
        class="bg-gray-200 px-4 py-2 rounded hover:bg-gray-300"
      >
        Voir plus
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import axios from 'axios'
import { MagnifyingGlassIcon } from '@heroicons/vue/24/outline'
import { formatCurrency } from '@/composables/portfolio'

// State
const history = ref([])
const search = ref('')
const selectedDate = ref('')
const visibleCount = ref(5)
const error = ref(null)

// Fetch data on mount
onMounted(async () => {
  const token = localStorage.getItem("token")
  try {
    const { data } = await axios.get('http://localhost:8000/investments/history', {
      headers: { Authorization: `Bearer ${token}` }
    })
    history.value = data
  } catch (e) {
    error.value = e.response?.data?.detail || 'Erreur lors du chargement'
  }
})

// Filter and sort
const filteredData = computed(() => {
  let filtered = history.value

  // Search
  if (search.value) {
    filtered = filtered.filter(item => {
      const name = item.asset_name || ''
      const symbol = item.symbol || ''
      return name.toLowerCase().includes(search.value.toLowerCase()) ||
             symbol.toLowerCase().includes(search.value.toLowerCase())
    })
  }

  // Date filter
  if (selectedDate.value) {
    filtered = filtered.filter(item =>
      new Date(item.date).toISOString().slice(0, 10) === selectedDate.value
    )
  }

  // Sort by date descending
  return filtered.sort((a, b) => new Date(b.date) - new Date(a.date))
})

// Displayed items
const displayedHistory = computed(() => {
  return filteredData.value.slice(0, visibleCount.value)
})

// Reset visibleCount when filters change
watch([search, selectedDate], () => {
  visibleCount.value = 5
})

// Date format
function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('fr-FR')
}
</script>
