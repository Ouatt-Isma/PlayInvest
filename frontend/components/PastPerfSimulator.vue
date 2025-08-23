<template>
  <div class="bg-white p-6 rounded-xl shadow-md w-full max-w-lg">
    <h2 class="text-xl font-bold mb-1">Simulateur PastPerf</h2>
    <p class="text-gray-500 mb-6">Simulateur de Performance Passée</p>

    <div class="grid grid-cols-2 gap-4 mb-4">
      <!-- Asset selection -->
      <div>
        <label class="block text-sm text-gray-600 mb-1">Choisir un actif</label>
        <select v-model="selectedAssetId" class="w-full border rounded px-3 py-2">
          <option v-for="asset in sortedAssets" :key="selectedAsset.id" :value="asset.id">
            {{ asset.name }}
          </option>
        </select>
      </div>

      <!-- Amount input -->
      <div>
        <label class="block text-sm text-gray-600 mb-1">Montant investi ({{ currency }})</label>
        <input
          v-model.number="amount"
          type="number"
          min="0"
          class="w-full border rounded px-3 py-2"
        />
      </div>

      <!-- Start date -->
      <div>
        <label class="block text-sm text-gray-600 mb-1">Date de Début</label>
        <input
          v-model="startDate"
          type="date"
          :max="yesterday"
          class="w-full border rounded px-3 py-2"
        />
      </div>

      <!-- End date -->
      <div>
        <label class="block text-sm text-gray-600 mb-1">Date de Fin</label>
        <input
          v-model="endDate"
          type="date"
          :max="yesterday"
          class="w-full border rounded px-3 py-2"
        />
      </div>
    </div>

    <button
      @click="simulate"
      class="bg-teal-800 hover:bg-teal-700 text-white font-semibold px-4 py-2 rounded w-full"
    >
      Simuler
    </button>

    <div v-if="result" class="mt-6 bg-gradient-to-br from-teal-50 to-white border border-teal-200 rounded-2xl shadow-md p-6">
    <div class="flex items-center justify-between mb-3">
        <h3 class="text-lg font-semibold text-teal-800">Résultat de la Simulation</h3>
        <svg class="w-6 h-6 text-teal-500" fill="none" stroke="currentColor" stroke-width="2"
            viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path stroke-linecap="round" stroke-linejoin="round"
                d="M13 16h-1v-4h-1m1-4h.01M12 8v.01M12 12a9 9 0 100-18 9 9 0 000 18z"/>
        </svg>
    </div>

    <div class="flex items-center space-x-4">
        <div class="flex-1">
        <p class="text-sm text-gray-500">Performance</p>
        <p :class="{
            'text-green-600': result.performance >= 0,
            'text-red-600': result.performance < 0
        }" class="text-2xl font-bold">
            {{ result.performance }}%
        </p>
        </div>
        <div class="w-px h-10 bg-gray-200"></div>
        <div class="flex-1">
        <p class="text-sm text-gray-500">Valeur actuelle</p>
        <p class="text-xl font-semibold text-gray-800">
            {{ formatCurrency(result.current_value, currency) }}
        </p>
        </div>
    </div>

    
    
    

    <div class="flex items-center space-x-4 mb-4">
        
      <!-- <img :src="getLogo(selectedAsset.symbol)" alt="logo" class="w-20 h-10 rounded-full" /> -->
      <div class="flex flex-col">
        <p class="text-sm font-semibold">{{ selectedAsset.name }} <span class="text-gray-400 font-medium">– {{ selectedAsset.symbol }}</span></p>
        <p class="text-xs text-gray-400">
        Dernière mise à jour : 
        <span class="text-gray-500">{{ formatDate(selectedAsset.updated_at) }}</span>
        </p>
      </div>
    </div>

    <MiniGraphDate 
  :symbol="selectedAsset.symbol" 
      :startDate="startDate"
      :endDate="endDate"
      :details="true"
      :key="`${selectedAsset.symbol}-${graphPeriod}`" />
    </div>
    <!-- Title -->
    <!-- <p class="text-sm font-medium text-gray-600 mb-1">l’évolution de la valeur de l’investissement</p>


    <div class="flex items-center justify-between mb-4">
      <p class="text-2xl font-bold text-gray-900">USD {{ formatCurrency(currentValue) }}</p>
      <p class="text-sm text-gray-500">
        USD {{ formatCurrency(amountInvested) }}
        <span :class="isUp ? 'text-green-600' : 'text-red-500'">({{ formattedPerformance }})</span>
      </p>
    </div> -->

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { formatCurrency } from '@/composables/portfolio'
import { getLogo} from '@/composables/assets'

import { watch } from 'vue'


// State
const assets = ref([])
const selectedAssetId = ref(null)
const selectedAsset = ref('')
const amount = ref(0)
const startDate = ref('')
const endDate = ref('')
const result = ref(null)
const currency = ref('')
// Yesterday's date in yyyy-mm-dd
const yesterday = new Date()
yesterday.setDate(yesterday.getDate() - 1)
const maxDateStr = yesterday.toISOString().split('T')[0]

// Computed for input `max` attribute
const today = new Date()
const formattedToday = today.toISOString().split('T')[0]
const formattedYesterday = maxDateStr
const sortedAssets = computed(() => {
  return [...assets.value].sort((a, b) => a.name.localeCompare(b.name))
})
const loading = ref(false)

watch(
  [selectedAssetId, amount, startDate, endDate],
  async ([newId, amt, start, end]) => {
    const found = assets.value.find(asset => asset.id === newId)
    if (found) {
      selectedAsset.value = found
    }

    if (amt && start && end) {
      await simulate()
    }
  }
)

function formatDate(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleString('fr-FR', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

// On mount: fetch assets
onMounted(async () => {
  try {
    currency.value = useCookie("currency").value
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase 
    const res = await axios.get(`${apiBase}/api/assets`)
    assets.value = res.data
    console.log(assets.value)
    if (assets.value.length) {
      selectedAssetId.value = assets.value[0].id
      selectedAsset.value = assets.value[0]
      console.log("selectedAsset", selectedAsset)
    }
  } catch (err) {
    console.error("Erreur lors du chargement des actifs :", err)
  }
})

// Simulate request
// const simulate = async () => {
//   if (!selectedAssetId.value || !amount.value || !startDate.value || !endDate.value) {
//     alert("Veuillez remplir tous les champs.")
//     return
//   }

//   if (endDate.value > formattedYesterday) {
//     alert("La date de fin ne peut pas être après hier.")
//     return
//   }

//   try {
//     loading.value = true
//     const res = await axios.post(`${apiBase}/simulator/pastperf`, {
//       asset_id: selectedAssetId.value,
//       amount: amount.value,
//       start_date: startDate.value,
//       end_date: endDate.value
//     })
//     result.value = res.data
//   } catch (err) {
//     console.error("Erreur lors de la simulation :", err)
//     alert("Erreur lors de la simulation.")
//   } finally {
//     loading.value = false
//   }
// }

const simulate = async () => {
  if (!selectedAssetId.value || !amount.value || !startDate.value || !endDate.value) {
    alert("Veuillez remplir tous les champs.")
    return
  }

  if (endDate.value > formattedYesterday) {
    alert("La date de fin ne peut pas être après hier.")
    return
  }

  try {
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase 
    const res = await axios.post(`${apiBase}/simulator/pastperf`, {
      asset_id: selectedAssetId.value,
      amount: amount.value,
      start_date: startDate.value,
      end_date: endDate.value
    })
    result.value = res.data
  } catch (err) {
    console.error("Erreur lors de la simulation :", err)
    alert("Erreur lors de la simulation.")
  }
}

</script>
