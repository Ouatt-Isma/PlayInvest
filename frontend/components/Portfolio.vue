<template>
  <div class="p-4 bg-white rounded-xl shadow">
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-4">
  <div class="w-full">
    <h2 class="text-xl font-bold">Vue d’ensemble du Portefeuille</h2>

    <div class="flex flex-wrap gap-4 mt-2 text-sm font-medium">
      <div class="flex items-center gap-2 text-green-700">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2-1.343-2-3-2z"/>
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M12 14v4m0 0h-3m3 0h3"/>
        </svg>
        Cash Total: {{ formatCurrency(cash, currency) }}
      </div>
      <div class="flex items-center gap-2 text-blue-700">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M11 11V3h2v8h8v2h-8v8h-2v-8H3v-2h8z"/>
        </svg>
        Total Investi: {{ formatCurrency(totalInvested, currency) }}
      </div>
    </div>

    <!-- Share bar -->
    <div class="w-full h-2 bg-gray-200 rounded overflow-hidden mt-2 flex">
      <div class="h-full bg-green-500" :style="{ width: cashShare + '%' }"></div>
      <div class="h-full bg-blue-500" :style="{ width: investedShare + '%' }"></div>
    </div>
  </div>

  <NuxtLink
    to="/assets"
    class="bg-teal-700 text-white text-center px-4 py-2 rounded w-full sm:w-auto hover:bg-teal-800 transition"
  >
    Ajouter un actif
  </NuxtLink>
</div>

    <div class="overflow-x-auto rounded-lg border border-gray-200 bg-white">
    <table class="min-w-full">
      <thead>
        <tr class="text-left bg-gray-100">
          <th class="p-2">Nom de l’actif</th>
          <th class="p-2">Quantité</th>
          <th class="p-2">Prix (Unitaire)</th>
          <th class="p-2">Variation jour</th>
          <th class="p-2">Performance</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="a in assets.filter(a => !a.sold)" :key="a.symbol" class="border-t">

          <td class="p-2 flex items-center gap-2">
            <img :src="getLogo(a.symbol)" alt="logo" class="w-6 h-6 rounded-full" />
            <div>
              <div class="font-medium">{{ a.name }}</div>
              <div class="text-sm text-gray-400">{{ a.symbol }}</div>
            </div>
          </td>
          <td class="p-2">{{ a.quantity }}</td>
          <td class="p-2">{{ formatCurrency(a.latest_price, a.currency) }}</td>
            <!-- <td class="p-2">{{ a.currency }}</td> -->
          <td class="p-2" :class="a.variation_1d >= 0 ? 'text-green-600' : 'text-red-500'">
            {{ a.variation_1d >= 0 ? '+' : '' }}{{ a.variation_1d.toFixed(2) }} %
          </td>
          <td class="p-2" :class="a.performance_pct >= 0 ? 'text-green-600' : 'text-red-500'">
            {{ a.performance_pct >= 0 ? '+' : '' }}{{ a.performance_pct.toFixed(2) }}% 
          </td>
          <td class="p-2 relative">
            <button @click="toggleMenu(a.symbol)" class="text-3xl px-3 py-2 rounded-full hover:bg-gray-100 transition">
                ⋮
            </button>

            <div v-if="activeMenu === a.symbol" class="absolute right-0 mt-2 w-32 bg-white border rounded shadow z-10">
                <ul class="text-sm text-gray-700">
                <li @click="sellAsset(a)" class="px-4 py-2 hover:bg-gray-100 cursor-pointer">Vendre</li>
                <li @click="buyMore(a)" class="px-4 py-2 hover:bg-gray-100 cursor-pointer">Acheter +</li>
                <!-- <li @click="viewDetails(a)" class="px-4 py-2 hover:bg-gray-100 cursor-pointer">Détails</li> -->
                </ul>
            </div>
            </td>
        </tr>
      </tbody>
    </table>  
    </div>
    <AssetDetailsModal
  :visible="showModal"
  :asset="selectedAsset"
  :sell="sell"
  @close="() => { showModal = false; sell = false }"
/>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import axios from 'axios'
import AssetDetailsModal from '~/components/Actifs/AssetDetailsModal.vue'
import { NuxtLink } from '#components'
import { formatCurrency } from '@/composables/portfolio'

const assets = ref([])
const cash = ref(0)
const totalInvested = ref(0)
const activeMenu = ref(null)
const showModal = ref(false)
const sell = ref(false)
const selectedAsset = ref(null)
const currency = ref([])



const buyMore = (asset) => {
  selectedAsset.value = asset
  showModal.value = true
}

const toggleMenu = (symbol) => {
  activeMenu.value = activeMenu.value === symbol ? null : symbol
}

const sellAsset = (asset) => {
  selectedAsset.value = asset
  showModal.value = true
  sell.value = true
}

const viewDetails = (asset) => {
  console.log("Détails de", asset)
  activeMenu.value = null
}


onMounted(async () => {
  const token = useCookie("token").value
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase 
  const response = await axios.get(`${apiBase}/api/portfolio`,{
      headers: {
        Authorization: `Bearer ${token}`  // assure-toi que `token` est défini
      }
    })
    const data = response.data
    assets.value = data.assets
    cash.value = data.cash
    const cashcookie = useCookie("cash")
    cashcookie.value = cash.value
    totalInvested.value = data.total_investi
    currency.value = data.currency
    
})

const total = computed(() => cash.value + totalInvested.value)

const cashShare = computed(() =>
  total.value > 0 ? (cash.value / total.value) * 100 : 0
)

const investedShare = computed(() =>
  total.value > 0 ? (totalInvested.value / total.value) * 100 : 0
)
</script>
