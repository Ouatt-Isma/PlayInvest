<script setup>
import { ref, watch, computed } from 'vue'
import axios from 'axios'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  LineElement, PointElement, LinearScale, CategoryScale, Filler, Tooltip, Legend
} from 'chart.js'

ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale, Filler, Tooltip, Legend)

const filterType = ref('category')
const selected = ref([])
const period = ref('1m')
const rawData = ref({ labels: [], data: {} })
const loading = ref(false)

const periodDays = {
  '7d': 7,
  '1m': 30,
  '3m': 90,
  '6m': 180,
  '1y': 365,
  'all': Infinity
}

const fetchData = async () => {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase 
  loading.value = true

  const token = useCookie("token").value
  const res = await axios.get(`${apiBase}/api/performance`, {
    headers: { Authorization: `Bearer ${token}` },
    params: { filter: filterType.value }
  })
  // console.log('[DEBUG] Résultat API :', res.data)
  rawData.value = res.data
  selected.value = Object.keys(res.data.data)
  loading.value = false
}

watch(filterType, fetchData, { immediate: true })

const chartData = computed(() => {
  const labels = rawData.value.labels || []
  const days = periodDays[period.value]
  const cutoffIndex = Math.max(0, labels.length - days)

  const slicedLabels = days === Infinity ? labels : labels.slice(cutoffIndex)
  const datasetKeys = selected.value

  const colors = {
    Global: '#0f766e',
    ETF: '#0f766e',
    Stock: '#f59e0b',
    Crypto: '#ef4444',
    Monde: '#0ea5e9',
    Africa: '#16a34a',
    Europe: '#7c3aed',
    USA: '#f43f5e'
  }

  const datasets = datasetKeys.map(key => ({
    label: key,
    data: days === Infinity ? rawData.value.data[key] : rawData.value.data[key].slice(cutoffIndex),
    borderColor: colors[key] || '#999',
    borderWidth: 2,
    tension: 0.3,
    pointRadius: 0
  }))

  return { labels: slicedLabels, datasets }
})

// helpers to format numbers as percentage with 2 decimals
const toPct = (v) => {
  const n = Number(v)
  if (!isFinite(n)) return v
  return `${n.toFixed(2)}%`
}

const chartOptions = {
  responsive: true,
  plugins: {
    legend: { position: 'bottom' },
    tooltip: {
      mode: 'index',
      intersect: false,
      callbacks: {
        label: (ctx) => {
          const val = ctx.parsed?.y
          return `${ctx.dataset.label}: ${toPct(val)}`
        }
      }
    }
  },
  scales: {
    y: {
      title: {
        display: true,
        text: 'Performance (%)'
      },
      ticks: {
        // show e.g. -7.05% with two decimals
        callback: (val) => toPct(val)
      }
    },
    x: {
      ticks: { maxRotation: 0 }
    }
  }
}
</script>

<template>
  <section class="p-6 bg-white rounded-xl shadow">
    <div class="flex justify-between items-center mb-4">
      <div>
        <h2 class="text-xl font-bold">Évolution du rendement global</h2>
        <p class="text-sm text-gray-500">Filtrable par catégorie ou région, période personnalisable</p>
      </div>

      <div class="flex gap-2">
        <select v-model="filterType" class="border px-2 py-1 rounded text-sm">
          <option value="all">Vue d'ensemble</option>
          <option value="category">Par catégorie</option>
          <option value="region">Par région</option>        
        </select>
        <select v-model="period" class="border px-2 py-1 rounded text-sm">
          <option value="7d">7 jours</option>
          <option value="1m">1 mois</option>
          <option value="3m">3 mois</option>
          <option value="6m">6 mois</option>
          <option value="1y">1 an</option>
          <option value="all">Tout</option>
        </select>
      </div>
    </div>

    <div class="w-full h-full">
    <div v-if="loading" class="text-center text-gray-500 py-4">Chargement…</div>
    
      <Line v-else :data="chartData" :options="chartOptions" />
    </div>
    
  </section>
</template>


<style>
.chart-container {
  width: 100%;
  height: 100%; /* or auto */
}
</style>