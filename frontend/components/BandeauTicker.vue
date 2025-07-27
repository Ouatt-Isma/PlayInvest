<template>
  <div class="ticker-wrapper">
    <div class="ticker-content" :style="animationStyle">
      <!-- On duplique deux fois le contenu pour créer l'effet de boucle -->
      <div class="ticker-items" v-for="n in 2" :key="n">
        <div
          v-for="(item, index) in items"
          :key="`${n}-${index}`"
          class="ticker-item"
          :class="{ positive: item.variation_1d > 0, negative: item.variation_1d < 0 }"
        >
          <span v-if="item.variation_1d != null">
            <div> {{ item.name }}</div>
            <div>{{ item.symbol }}: {{ item.variation_1d.toFixed(2) }}%</div>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { getLogo} from '@/composables/assets'

// 👇 données simulées si API absente
const items = ref([])

onMounted(async () => {
  try {
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase
    const res = await axios.get(`${apiBase}/api/assets`)
    items.value = res.data
      .map(item => ({
        ...item,
        variation_1d: parseFloat(item.variation_1d),
      }))
      .sort((a, b) => Math.abs(b.variation_1d) - Math.abs(a.variation_1d))
  } catch (error) {
    console.warn('API échouée, données mockées')
    items.value = Array.from({ length: 50 }, (_, i) => ({
      symbol: `ASSET${i + 1}`,
      variation_1d: parseFloat((Math.random() * 10 - 5).toFixed(2)),
    })).sort((a, b) => Math.abs(b.variation_1d) - Math.abs(a.variation_1d))
  }
})


// 👇 durée dynamique selon nombre d’items
const animationStyle = computed(() => {
  const baseSpeed = 8 // secondes pour traverser 1 set d'items
  const factor = Math.max(1, items.value.length / 5)
  return {
    animation: `scroll-left ${baseSpeed * factor}s linear infinite`,
  }
})
</script>

<style>
.ticker-wrapper {
  position: fixed;  
  z-index: 900;  
  overflow: hidden;
  white-space: nowrap;
  background: rgba(1, 27, 45, 0.7); /* 50% opacity */
  color: rgb(255, 255, 255);
  padding: 10px 0;
}

.ticker-content {
  display: flex;
  width: max-content;
  white-space: nowrap;
  will-change: transform;
}

.ticker-items {
  display: flex;
}

.ticker-item {
  margin: 0 30px;
  font-weight: bold;
  font-size: 1rem;
  white-space: nowrap;
}

.positive {
  color: #2ecc71;
}

.negative {
  color: #e74c3c;
}

.ticker-icon {
  height: 1em;
  width: auto;
  vertical-align: middle;
  margin-right: 0.3em;
}


@keyframes scroll-left {
  0% {
    transform: translateX(0%);
  }
  100% {
    transform: translateX(-50%);
  }
}

</style>
