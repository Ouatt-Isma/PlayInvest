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

const props = defineProps({
  symbol: String,
  period: String,
  details: {
    type: Boolean,
    default: false
  }
})

const chartData = ref(null)
const chartRef = ref(null)
const isUp = ref(true)
const minValue = ref(null)
const maxValue = ref(null)
const startDate = ref('')
const endDate = ref('')


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
    x: {
      display: false
    },
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
          grid: {
            display: false
          },
          border: {
            display: false
          }
        }
      : {
          display: false
        }
  }
}))

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

const fetchGraphData = async () => {
  try {
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase 
    const res = await fetch(`${apiBase}/api/graph/${props.symbol}?period=${props.period}`)
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
    startDate.value = labels[0]
    endDate.value = labels[labels.length - 1]

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
    console.error("Erreur chargement graph:", e)
    chartData.value = null
  }
}

watch(
  () => [props.symbol, props.period],
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

    <!-- Extra Info -->
     <div v-if="props.details ">
    <div v-if="chartData" class="absolute bottom-1 left-1 right-1 flex justify-between text-[10px] text-gray-500 px-1">
      <span class="ml-12">{{ startDate }}</span>
      <span>{{ endDate }}</span>
    </div>
    <!-- <div v-if="chartData" class="absolute top-1 left-1 text-[10px] text-green-600 font-semibold">
      Max: {{ maxValue?.toFixed(2) }}
    </div>
    <div v-if="chartData" class="absolute top-1 right-1 text-[10px] text-red-500 font-semibold">
      Min: {{ minValue?.toFixed(2) }}
    </div> -->
    </div>
  </div>
</template>
