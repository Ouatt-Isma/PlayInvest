<script setup>
import { ref, watch, onMounted } from 'vue'
import axios from 'axios'
import { formatCurrency } from '@/composables/portfolio'
import { nextTick } from 'vue'
import { getLogo} from '@/composables/assets'


const notification = ref({ type: '', message: '', visible: false })
const props = defineProps({
  visible: Boolean,
  asset: Object, // should contain at least asset.id or symbol
  sell: Boolean,
 
})
const graphPeriod = ref('7d')
const emits = defineEmits(['close'])

// Dynamic state
const amount = ref()
const currentPrice = ref(null)
const variations = ref({})
const volume = ref(null)
const lastUpdate = ref('')
const isLoading = ref(false)
const selectedVariation = computed(() => variations.value[graphPeriod.value])

// Format helpers
// const formattedPrice = computed(() => {
//   if (currentPrice.value == null) return '--'
//   return new Intl.NumberFormat('en-US', {
//     style: 'currency',
//     currency: props.asset?.currency || 'USD',
//   }).format(currentPrice.value)
// })

// Fetch asset data from backend
const fetchAssetDetails = async () => {
  if (!props.asset || !props.asset.id) return
  isLoading.value = true
  try {
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase 
    const response = await axios.get(`${apiBase}/api/assets/${props.asset.id}`)
    const data = response.data
    currentPrice.value = data.latest_price
    variations.value = {
      '1d': data.variation_1d,
      '7d': data.variation_7d,
      '1m': data.variation_1M,
      '3m': data.variation_3M,
      '6m': data.variation_6M,
      '1y': data.variation_1y,
      'all': data.variation_all,
    }
    volume.value = data.volume || 0
    lastUpdate.value = new Date(data.updated_at || Date.now()).toLocaleString()
  } catch (error) {
    console.error('Failed to fetch asset data:', error)
  } finally {
    isLoading.value = false
  }
}

// Refetch every time modal is opened with new asset
watch(() => props.visible, (newVal) => {
    console.log(props.asset)
  if (newVal && props.asset?.id) fetchAssetDetails()
})

// watch(
//   () => props.asset,
//   (newAsset) => {
//     if (newAsset?.quantity) amount.value = newAsset.quantity
//   },
//   { immediate: true }
// )

// watch(
//   () => [props.visible, props.asset?.id],
//   ([visible, assetId]) => {
//     if (visible && assetId) {
//       fetchAssetDetails()
//       if (props.asset?.quantity) amount.value = props.asset.quantity
//     }
//   },
//   { immediate: true }
// )


// Close/invest actions
const close = async () => {
  await nextTick() // allow children to finish rendering
  emits('close')
}
const invest = async () => {
  try {
    const token = localStorage.getItem("token")
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase 
    const res = await axios.get(`${apiBase}/api/buy`, {
      params: {
        asset: props.asset.id,
        amount: amount.value
      },
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    showNotification('success', 'Achat effectué avec succès !')
    emits('close')  // close modal
  } catch (error) {
    const msg = error.response?.data?.detail || "Erreur inattendue lors de l'achat"
    showNotification('error', msg)
  }
  emits('close')
}

const showNotification = (type, message) => {
  notification.value = { type, message, visible: true }
  setTimeout(() => {
    notification.value.visible = false
  }, 4000)
}

const tosell = async () => {
  try {
    const token = localStorage.getItem("token")
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase 
    const res = await axios.get(`${apiBase}/api/sell`, {
      params: {
        asset: props.asset.id,
        amount: amount.value
      },
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    showNotification('success', 'Vente effectué avec succès !')
    emits('close')  // close modal
  } catch (error) {
    const msg = error.response?.data?.detail || "Erreur inattendue lors de la vente"
    showNotification('error', msg)
  }
  emits('close')
}


const showPdf = ref(false)
const selectedPdf = ref('')

function openPdf(symbol) {
  selectedPdf.value = `/fiche/${symbol}.pdf`
  showPdf.value = true
}


</script>


<template>
  <div v-if="visible" class="fixed inset-0 bg-black/40 z-50 flex items-center justify-center">
    <div class="bg-white rounded-xl shadow-xl w-[90%] max-w-2xl p-6 relative">
      <!-- Close Button -->
      <button @click="close" class="absolute top-3 right-3 text-gray-400 hover:text-black text-xl">×</button>

      <!-- Header -->
      <div class="flex items-center gap-4 mb-4">
        <img :src="getLogo(asset.symbol)" class="w-10 h-10 rounded-full" alt="logo" />
        <div>
          <h2 class="text-xl font-semibold">{{ asset.name }}</h2>
          <p class="text-gray-400 text-sm font-medium uppercase">{{ asset.symbol }}</p>
        </div>

        <button @click="openPdf(asset.symbol)">
      <img src="/icons/file-icon.svg" class="w-4" />
      </button>

      <PdfModal :pdfUrl="selectedPdf" :visible="showPdf" @close="showPdf = false" />

      </div>



      <!-- Analysis Controls -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
        
        <div>
          <label class="text-xs text-gray-500">Quantité</label>
          <input type="number" class="w-full border rounded p-2" v-model="amount" />
         
        </div>
       
      </div>

      <!-- Price + Chart -->
      <div class="mb-4">
        <p class="text-sm text-gray-500">Dernière mise à jour : {{ lastUpdate }}</p>
        <div class="text-2xl font-bold mt-1">{{ formatCurrency(currentPrice, asset.currency) }}</div>
        <!-- <div class="text-2xl font-bold mt-1">{{ formattedPrice }}</div> -->
        <div class="text-sm text-gray-400">
          <p class="text-xs text-gray-500 mt-1">
  Variation sur 
  {{
    {
      '7d': '7 jours',
      '1m': '1 mois',
      '3m': '3 mois',
      '6m': '6 mois',
      '1y': '1 an',
      'all': 'tout'
    }[graphPeriod]
  }}
</p>
        <span :class="selectedVariation >= 0 ? 'text-green-600' : 'text-red-600'">
          {{ selectedVariation != null ? selectedVariation.toFixed(2) + '%' : '–' }}
        </span>
        </div>

      </div>

      <!-- Chart Placeholder -->

        <select v-model="graphPeriod" class="border px-2 py-1 rounded text-sm">
      <option value="7d">7 jours</option>
      <option value="1m">1 mois</option>
      <option value="3m">3 mois</option>
      <option value="6m">6 mois</option>
      <option value="1y">1 an</option>
      <option value="all">tout</option>
    </select>

        <MiniGraph 
        v-if="props.asset?.symbol"
  :symbol="props.asset.symbol" 
      :period="graphPeriod" 
      :details="true"
      :key="`${props.asset.symbol}-${graphPeriod}`" />


      <!-- Description -->
      <div class="mb-6 text-sm text-gray-700 leading-relaxed">
        {{ asset.description }}
      </div>

      <!-- Action -->

        <button v-if ="!props.sell" class="bg-teal-700 text-white px-6 py-2 rounded-lg w-full" @click="invest(amount)">investir</button>

        <button v-if ="props.sell"  class="bg-teal-700 text-white px-6 py-2 rounded-lg w-full" @click="tosell(amount)">vendre</button>


      
    </div>
  </div>
  <div v-if="notification.visible"
     :class="[
       'fixed bottom-4 right-4 px-4 py-3 rounded shadow-lg text-white z-50',
       notification.type === 'success' ? 'bg-green-600' : 'bg-red-600'
     ]">
  {{ notification.message }}
</div>
</template>

