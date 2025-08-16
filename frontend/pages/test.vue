<template>
  <button class="px-4 py-2 rounded bg-indigo-600 text-white" @click="open = true">
    Lancer le Challenge
  </button>

  <ChallengeWeeklyModal
    v-model="open"
    :assets="pair"
    @submit="onSubmit"
  />
</template>

<script setup>
import { ref } from 'vue'
import ChallengeWeeklyModal from '~/components/ChallengeWeeklyModal.vue'

const open = ref(false)
const pair = ref([
  {
    id: 'AAPL',
    symbol: 'AAPL',
    name: 'Apple Inc.',
    type: 'Stock',
    currency: 'USD',
    price: 218.40,
    change24h: 0.86,
    logoUrl: 'https://logo.clearbit.com/apple.com',
    sparkline: [98,100,101,102,101,103,104,103,105,104,106,108]
  },
  {
    id: 'BTC',
    symbol: 'BTC',
    name: 'Bitcoin',
    type: 'Crypto',
    currency: 'USD',
    price: 65340,
    change24h: -0.42,
    logoUrl: 'https://cryptoicons.org/api/icon/btc/64',
    sparkline: [100,99,98,100,101,100,99,100,102,101,100,99]
  }
])

function onSubmit({ assetId }) {
  // For now just toast/log; backend wiring later
  console.log('Picked:', assetId)
}
</script>
