<template>
  <section class="px-10 py-12 bg-gradient-to-br from-white to-[#e6f6f8]">

    <!-- Table -->
    <table class="w-full bg-white rounded shadow overflow-hidden">
      <thead>
        <tr class="text-left bg-gray-100">
          <th class="p-4">#</th>
          <th class="p-4">Nom</th>
          <th class="p-4">Prix</th>
          <th class="p-4">Variation jour</th>
          <th class="p-4">Variation Période</th>
          <th class="p-4">Graphique</th>
          <th class="p-4">Fiche descriptive</th>
          <th class="p-4">Trade</th>
          
        </tr>
      </thead>
      <tbody>
  <tr v-for="(asset, index) in paginatedAssets" :key="asset.symbol">
    <td class="p-4">{{ index + 1 }}</td>
    <td class="p-4 flex items-center gap-2">
      <img :src="getLogo(asset.symbol)" class="w-20" />
      {{ asset.name || asset.symbol }}
    </td>
    <td class="p-4">{{ formatCurrency(asset.latest_price, asset.currency) }} </td>
    <td class="p-4 font-medium" :class="formatVariation(asset.variation_1d).class">
  {{ formatVariation(asset.variation_1d).text }}
</td>
    <td class="p-4 font-medium" :class="formatVariation(getVariation(asset)).class">
  {{ formatVariation(getVariation(asset)).text }}
</td>
    <td class="p-4">
      <MiniGraph :symbol="asset.symbol" 
      :period="props.graphPeriod" 
      :key="`${asset.symbol}-${props.graphPeriod}`" />

    </td>
    <td class="p-4">
      <!-- <a :href="getFicheLink(asset.symbol) + '#toolbar=0'" target="_blank" rel="noopener">
        <img src="/icons/file-icon.svg" class="w-4" />
      </a> -->
      <button @click="openPdf(asset.symbol)">
      <img src="/icons/file-icon.svg" class="w-4" />
    </button>
    <PdfModal :pdfUrl="selectedPdf" :visible="showPdf" @close="showPdf = false" />
    </td>
    <td class="p-4">
      <button class="border px-3 py-1 rounded" @click="trade(asset)" >Trade</button>
    </td>
  </tr>
</tbody>
    </table>

    <AssetDetailsModal
  :visible="showModal"
  :asset="selectedAsset"
  @close="showModal = false"
/>
    <div class="flex items-center justify-between mt-6">
  <div class="flex items-center gap-2">
    <label for="itemsPerPage" class="text-sm text-gray-600">Afficher</label>
    <select id="itemsPerPage" v-model="itemsPerPage" class="border rounded px-2 py-1 text-sm">
      <option :value="10">10</option>
      <option :value="25">25</option>
      <option :value="50">50</option>
    </select>
    <span class="text-sm text-gray-600">actifs par page</span>
  </div>

  <div class="flex gap-2">
    <button
      @click="currentPage--"
      :disabled="currentPage === 1"
      class="px-3 py-1 border rounded disabled:opacity-50"
    >
      Précédent
    </button>
    <span class="text-sm text-gray-600">Page {{ currentPage }} / {{ totalPages }}</span>
    <button
      @click="currentPage++"
      :disabled="currentPage === totalPages"
      class="px-3 py-1 border rounded disabled:opacity-50"
    >
      Suivant
    </button>
  </div>
</div>

  </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { NuxtLink } from '#components'
import PdfModal from '@/components/PdfModal.vue' // update path if 
import { usePortfolio, formatCurrency } from '@/composables/portfolio'
import { getLogo} from '@/composables/assets'
//needed
const { assets, cash, totalInvested, fetchPortfolio } = usePortfolio()
onMounted(fetchPortfolio)
const selectedAsset = ref(null)
const showModal = ref(false)
const variationFieldMap = {
  '7d': 'variation_7d',
  '1m': 'variation_1M',  // <-- match your backend naming exactly!
  '3m': 'variation_3M',
  '6m': 'variation_6M',
  '1y': 'variation_1y',
  'all': 'variation_all'
}

function getVariation(asset) {
  const field = variationFieldMap[props.graphPeriod]
  return asset[field]
}

const trade = (asset) => {
  selectedAsset.value = asset
  showModal.value = true
}

// async function buyAsset(asset, amout) {
//   await invest(
//     asset.value.id,
//     amount.value,
//     () => showNotification('success', 'Achat effectué avec succès !'),
//     (msg) => showNotification('error', msg)
//   )
//   emits('close')
// }

const showPdf = ref(false)
const selectedPdf = ref('')

function openPdf(symbol) {
  selectedPdf.value = `/fiche/${symbol}.pdf`
  showPdf.value = true
}

const props = defineProps({
  assets: Array,
  graphPeriod: {
    type: String,
    default: '7d'
  }
})

watch(() => props.graphPeriod, (val) => {
  console.log('[graphPeriod changed]', val)
})

const currentPage = ref(1)
const itemsPerPage = ref(10)

const paginatedAssets = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return props.assets.slice(start, end)
})

const totalPages = computed(() =>
  Math.ceil(props.assets.length / itemsPerPage.value)
)

// Optionnel : pour trier selon une logique
const sortedAssets = computed(() =>
  [...props.assets.value].sort((a, b) => (b.variation_1d || 0) - (a.variation_1d || 0))
)


function getFicheLink(symbol) {
  return `/fiche/${symbol.toLowerCase()}.pdf`
}

function getGraph(symbol) {
  return `/plots/${symbol.toLowerCase()}.png`
}

function formatPrice(p) {
  if (!p) return '—'
  return typeof p === 'number' ? `$${p.toFixed(2)}` : p
}

function formatVariation(v) {
  if (v === null || v === undefined || isNaN(v)) {
    return { class: 'text-gray-400', text: '—' }
  }

  const color = v >= 0 ? 'text-green-600' : 'text-red-500'
  const sign = v >= 0 ? '+' : ''
  return { class: color, text: `${sign}${v.toFixed(2)}%` }
}

watch(() => props.assets, () => {
  currentPage.value = 1
})

watch(() => props.assets, (val) => {
  console.log('[AssetsTable.vue] assets =', val)
})

watch(() => props.graphPeriod, (val) => {
  console.log('[AssetsTable.vue] graphPeriod =', val)
})


</script>
