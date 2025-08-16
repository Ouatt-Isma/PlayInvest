<template>
  <section class="mx-auto max-w-7xl px-4 sm:px-6 md:px-10 py-12 bg-gradient-to-br from-white to-[#e6f6f8]">
  <div class="overflow-x-auto -mx-4 sm:mx-0 px-4 sm:px-0">
    <table class="w-full bg-white rounded-lg shadow table-auto">
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
          <td class="p-4">{{ (currentPage - 1) * itemsPerPage + index + 1 }}</td>

          <td class="p-4 flex items-center gap-2">
            <img :src="getLogo(asset.symbol)" class="w-8 h-8 object-contain" />
            <span>{{ asset.name || asset.symbol }}</span>
          </td>

          <td class="p-4">
            {{ formatCurrency(asset.latest_price, asset.currency) }}
          </td>

          <td class="p-4 font-medium" :class="formatVariation(asset.variation_1d).class">
            {{ formatVariation(asset.variation_1d).text }}
          </td>

          <td class="p-4 font-medium" :class="formatVariation(getVariation(asset)).class">
            {{ formatVariation(getVariation(asset)).text }}
          </td>

          <td class="p-4">
            <MiniGraph
              :symbol="asset.symbol"
              :period="graphPeriod"
              :key="`${asset.symbol}-${graphPeriod}`"
            />
          </td>

          <td class="p-4">
            <button class="inline-flex items-center gap-2 hover:opacity-80" @click="openPdf(asset.symbol)">
              <img src="/icons/file-icon.svg" class="w-4" alt="PDF" />
            
            </button>
          </td>

          <td class="p-4">
            <button class="border px-3 py-1 rounded hover:bg-gray-50" @click="trade(asset)">
              Trade
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <div class="flex items-center justify-between mt-6">
      <div class="flex items-center gap-2">
        <label for="itemsPerPage" class="text-sm text-gray-600">Afficher</label>
        <select id="itemsPerPage" v-model.number="itemsPerPage" class="border rounded px-2 py-1 text-sm">
          <option :value="10">10</option>
          <option :value="25">25</option>
          <option :value="50">50</option>
        </select>
        <span class="text-sm text-gray-600">actifs par page</span>
      </div>

      <div class="flex gap-2 items-center">
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

    <!-- Modals -->
    <PdfModal :pdfUrl="selectedPdf" :visible="showPdf" @close="showPdf = false" />

    <AssetDetailsModal
      :visible="showModal"
      :asset="selectedAsset"
      :formatCurrency="formatCurrency"
      @close="showModal = false"
      @confirm="onConfirmTrade"
    />
  </div>
  </section>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import MiniGraph from '@/components/MiniGraph.vue'
import PdfModal from '@/components/PdfModal.vue'
import AssetDetailsModal from '@/components/Actifs/AssetDetailsModal.vue'
import { usePortfolio, formatCurrency } from '@/composables/portfolio'
import { getLogo } from '@/composables/assets'

/** Props **/
const props = defineProps({
  assets: { type: Array, default: () => [] },
  graphPeriod: { type: String, default: '7d' }
})

/** Data **/
const { fetchPortfolio } = usePortfolio()
onMounted(fetchPortfolio)

const selectedAsset = ref(null)
const showModal = ref(false)

const showPdf = ref(false)
const selectedPdf = ref('')

const currentPage = ref(1)
const itemsPerPage = ref(10)

/** Helpers **/
const variationFieldMap = {
  '7d': 'variation_7d',
  '1m': 'variation_1M',
  '3m': 'variation_3M',
  '6m': 'variation_6M',
  '1y': 'variation_1y',
  'all': 'variation_all'
}

function getVariation(asset) {
  const field = variationFieldMap[props.graphPeriod] || 'variation_7d'
  return asset?.[field]
}

function formatVariation(v) {
  const num = Number(v)
  if (!isFinite(num)) return { class: 'text-gray-400', text: '—' }
  const cls = num >= 0 ? 'text-green-600' : 'text-red-500'
  const sign = num >= 0 ? '+' : ''
  return { class: cls, text: `${sign}${num.toFixed(2)}%` }
}

function openPdf(symbol) {
  selectedPdf.value = `/fiche/${String(symbol).toLowerCase()}.pdf`
  showPdf.value = true
}

function trade(asset) {
  selectedAsset.value = asset
  showModal.value = true
}

/** Pagination **/
const safeAssets = computed(() => (Array.isArray(props.assets) ? props.assets : []))

const totalPages = computed(() => Math.max(1, Math.ceil(safeAssets.value.length / itemsPerPage.value)))

const paginatedAssets = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  return safeAssets.value.slice(start, start + itemsPerPage.value)
})

watch([() => props.assets, itemsPerPage], () => {
  currentPage.value = 1
})

/** Trade confirm handler **/
async function onConfirmTrade({ asset, amount }) {
  try {
    // TODO: replace with your real API/composable call:
    // await invest(asset.id, amount)
    console.log('Trade confirmed:', asset.symbol, 'amount:', amount)
    // showNotification('success', 'Achat effectué avec succès !')
  } catch (e) {
    console.error(e)
    // showNotification('error', e?.message || 'Erreur pendant le trade')
  }
}
</script>
