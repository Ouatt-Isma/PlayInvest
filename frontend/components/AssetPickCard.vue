<template>
  <div>
  <button
    type="button"
    class="group w-full text-left rounded-2xl border p-4 shadow-sm transition
           hover:shadow-md focus:outline-none focus:ring-2 focus:ring-offset-2
           disabled:opacity-60"
    :class="selected ? 'border-emerald-600 ring-emerald-600' : 'border-gray-200'"
    @click="$emit('select')"
    :aria-pressed="selected ? 'true' : 'false'"
  >
    <div class="flex items-center gap-3">
      <!-- logo (optional) -->
      <img
        v-if="logoUrl"
        :src="logoUrl"
        :alt="display.symbol"
        class="h-10 w-10 rounded object-contain"
      />
      <div v-else class="h-10 w-10 rounded bg-gray-100 flex items-center justify-center text-sm font-semibold">
        {{ (display.symbol || display.name || '?').slice(0,2).toUpperCase() }}
      </div>

      <div class="min-w-0">
        <div class="flex items-center gap-2 flex-wrap min-w-0">
  <h4 class="font-semibold truncate">{{ asset.name || asset.symbol }}</h4>
  <span class="text-xs px-2 py-0.5 rounded-full bg-gray-100 text-gray-600">{{ asset.type }}</span>
  <span v-if="asset.region" class="text-xs px-2 py-0.5 rounded-full bg-blue-100 text-blue-700">
    {{ asset.region }}
  </span>
</div>

        <p class="text-sm text-gray-500 truncate">{{ display.symbol }}</p>
      </div>

      <div class="ml-auto text-right">
        <div class="font-semibold">{{ formatCurrency(display.price, display.currency) }}</div>
        <div class="text-sm" :class="display.change >= 0 ? 'text-emerald-600' : 'text-rose-600'">
          {{ signed(display.change) }}%
        </div>
      </div>
    </div>

    <!-- sparkline (optional if you add it later) -->
    <div class="mt-3" v-if="sparkline?.length">
      <svg :viewBox="`0 0 ${w} ${h}`" class="w-full h-10">
        <path :d="pathD" fill="none" stroke="currentColor" stroke-width="2"
              :class="display.change >= 0 ? 'text-emerald-500' : 'text-rose-500'"/>
      </svg>
    </div>
  </button>
  <button 
    class="text-blue-600 hover:underline hover:text-blue-800"
    @click="trade(asset)"
  >
    Voir Plus
  </button>
  </div>
  <AssetDetailsModal
      :visible="showModal"
      :asset="selectedAsset"
      :formatCurrency="formatCurrency"
      @close="showModal = false"
      @confirm="onConfirmTrade"
    />
</template>

<script setup>
import { computed } from 'vue'
import AssetDetailsModal from '@/components/Actifs/AssetDetailsModal.vue'

const props = defineProps({
  asset: { type: Object, required: true },
  selected: { type: Boolean, default: false }
})
defineEmits(['select'])

const selectedAsset = ref(null)
const showModal = ref(false)

function trade(asset) {
  selectedAsset.value = asset
  showModal.value = true
}

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

/**
 * Backend sample:
 * {
 *   id, name, symbol, latest_price, buying_price,
 *   variation_1d, variation_7d, variation_1M, ...,
 *   type: 'Action' | 'ETF' | 'Crypto', region, currency, logo_url?
 * }
 *
 * We normalize to the fields the card needs.
 */
const display = computed(() => {
  const a = props.asset || {}
  return {
    id: a.id,
    name: a.name,
    symbol: a.symbol,
    type: a.type,            // e.g., 'Action'
    region: a.region,        // e.g., 'Europe'
    currency: a.currency || 'EUR',
    price: a.latest_price ?? a.price ?? 0,
    // For the weekly challenge, 1-day move is fine; change to variation_7d if you prefer
    change: Number(a.variation_1d ?? a.change24h ?? 0)
  }
})

// Optional logo: use asset.logo_url if present; otherwise null
const logoUrl = computed(() => props.asset?.logo_url || props.asset?.logoUrl || null)

// Optional sparkline (not provided by your route right now)
const sparkline = computed(() => props.asset?.sparkline || [])

// sparkline path helpers
const w = 100
const h = 30
function pathFrom(values, width, height) {
  const n = values.length
  if (!n) return ''
  const min = Math.min(...values)
  const max = Math.max(...values)
  const span = max - min || 1
  const stepX = width / (n - 1 || 1)
  return values
    .map((v, i) => {
      const x = i * stepX
      const y = height - ((v - min) / span) * height
      return `${i ? 'L' : 'M'}${x.toFixed(2)},${y.toFixed(2)}`
    })
    .join(' ')
}
const pathD = computed(() => pathFrom(sparkline.value, w, h))

const signed = v => {
  const n = Number(v || 0)
  return (n >= 0 ? '+' : '') + n.toFixed(2)
}
const formatCurrency = (n, ccy='EUR') =>
  new Intl.NumberFormat('fr-FR', { style:'currency', currency: ccy }).format(Number(n ?? 0))


</script>
