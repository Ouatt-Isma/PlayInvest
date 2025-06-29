<template>
  <div class="p-4 bg-white rounded-xl shadow">
    <div class="flex justify-between items-center mb-4">
    <div>
      <h2 class="text-xl font-bold">Vue d’ensemble du Portefeuille</h2>
      <span> Cash Total: {{ cash }}</span>
      <span> Total Investi: {{totalInvested}}</span>
    </div>
      <NuxtLink to='/assets' class="bg-teal-700 text-white px-4 py-2 rounded">Ajouter un actif</NuxtLink>
    </div>
    <table class="w-full">
      <thead>
        <tr class="text-left bg-gray-100">
          <th class="p-2">Nom de l’actif</th>
          <th class="p-2">Quantité</th>
          <th class="p-2">Prix</th>
          <th class="p-2">Variation jour</th>
          <th class="p-2">Performance</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="a in assets.filter(a => !a.sold)" :key="a.symbol" class="border-t">

          <td class="p-2 flex items-center gap-2">
            <img :src="a.logo" alt="logo" class="w-6 h-6 rounded-full" />
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
    <AssetDetailsModal
  :visible="showModal"
  :asset="selectedAsset"
  :sell="sell"
  @close="() => { showModal = false; sell = false }"
/>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'
import AssetDetailsModal from '@/components/AssetDetailsModal.vue'
import { NuxtLink } from '#components'
import { formatCurrency } from '@/composables/portfolio'

const assets = ref([])
const cash = ref(0)
const totalInvested = ref(0)
const activeMenu = ref(null)
const showModal = ref(false)
const sell = ref(false)
const selectedAsset = ref(null)

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
  const token = localStorage.getItem("token")
  const response = await axios.get(`http://localhost:8000/api/portfolio/`,{
      headers: {
        Authorization: `Bearer ${token}`  // assure-toi que `token` est défini
      }
    })
    const data = response.data
    assets.value = data.assets
    cash.value = data.cash
    totalInvested.value = data.total_investi
})


</script>
