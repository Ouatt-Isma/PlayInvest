<script setup>
import { ref, watch, nextTick } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Filler
} from 'chart.js'

ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale, Filler)

// Props
const props = defineProps({
  symbol: String,
  startDate: String,
  endDate: String,
  details: {
    type: Boolean,
    default: false
  }
})

// State
const chartData = ref(null)
const chartRef = ref(null)
const isUp = ref(true)
const minValue = ref(null)
const maxValue = ref(null)
const fromDate = ref('')
const toDate = ref('')

// Chart Options
const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  elements: {
    point: { radius: 0 },
    line: { tension: 0.3 }
  },
  plugins: {
    legend: { display: false },
    tooltip: { enabled: false }
  },
  scales: {
    x: { display: false },
    y: props.details
      ? {
          display: true,
          position: 'left',
          ticks: {
            font: { size: 10 },
            padding: 4,
            callback: (value, index, ticks) => {
              if (index === 0 || index === ticks.length - 1) {
                return value.toFixed(2)
              }
              return ''
            }
          },
          grid: { display: false },
          border: { display: false }
        }
      : { display: false }
  }
}))

// Gradient Helper
function createGradient(ctx, area, up) {
  const gradient = ctx.createLinearGradient(0, area.top, 0, area.bottom)
  if (up) {
    gradient.addColorStop(0, 'rgba(34,197,94,0.5)')
    gradient.addColorStop(1, 'rgba(34,197,94,0.05)')
  } else {
    gradient.addColorStop(0, 'rgba(239,68,68,0.5)')
    gradient.addColorStop(1, 'rgba(239,68,68,0.05)')
  }
  return gradient
}

// Data Fetcher
const fetchGraphData = async () => {
  if (!props.symbol || !props.startDate || !props.endDate) return

  try {
    const res = await fetch(
      `http://localhost:8000/api/graph/${props.symbol}?start_date=${props.startDate}&end_date=${props.endDate}`
    )
    const data = await res.json()

    const prices = data.prices.map(p => p.price)
    const labels = data.prices.map(p => p.date)

    if (!prices.length) {
      chartData.value = null
      return
    }

    isUp.value = prices[0] < prices[prices.length - 1]
    minValue.value = Math.min(...prices)
    maxValue.value = Math.max(...prices)
    fromDate.value = labels[0]
    toDate.value = labels[labels.length - 1]

    await nextTick()
    const canvas = chartRef.value?.canvasRef
    const ctx = canvas?.getContext('2d')
    const chart = chartRef.value?.chart
    const area = chart?.chartArea

    const gradient = (ctx && area)
      ? createGradient(ctx, area, isUp.value)
      : isUp.value
        ? 'rgba(34,197,94,0.2)'
        : 'rgba(239,68,68,0.2)'

    chartData.value = {
      labels,
      datasets: [
        {
          data: prices,
          fill: true,
          borderColor: isUp.value ? '#22c55e' : '#ef4444',
          backgroundColor: gradient,
          borderWidth: 2,
          tension: 0.3
        }
      ]
    }
  } catch (e) {
    console.error("Erreur chargement graphique:", e)
    chartData.value = null
  }
}

// React to changes
watch(
  () => [props.symbol, props.startDate, props.endDate],
  () => fetchGraphData(),
  { immediate: true }
)
</script>

<template>
  <div :class="props.details ? 'w-full h-40' : 'w-32 h-24'" class="relative">
    <Line
      ref="chartRef"
      v-if="chartData"
      :data="chartData"
      :options="chartOptions"
    />
    <div v-else class="text-xs text-gray-400 italic">—</div>

    <!-- Optional Date Display -->
    <div v-if="props.details && chartData" class="absolute bottom-1 left-1 right-1 flex justify-between text-[10px] text-gray-500 px-1">
      <span class="ml-12">{{ fromDate }}</span>
      <span>{{ toDate }}</span>
    </div>
  </div>
</template>
