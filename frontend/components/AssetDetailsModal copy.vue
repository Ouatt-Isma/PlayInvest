<template>
  <div v-if="visible" class="fixed inset-0 bg-black/40 z-50 flex items-center justify-center">
    <div class="bg-white rounded-xl shadow-xl w-[90%] max-w-2xl p-6 relative">
      <!-- Close Button -->
      <button @click="close" class="absolute top-3 right-3 text-gray-400 hover:text-black text-xl">×</button>

      <!-- Header -->
      <div class="flex items-center gap-4 mb-4">
        <img :src="asset.logo" class="w-10 h-10 rounded-full" alt="logo" />
        <div>
          <h2 class="text-xl font-semibold">{{ asset.name }}</h2>
          <p class="text-gray-400 text-sm font-medium uppercase">{{ asset.symbol }}</p>
        </div>
      </div>

      <!-- Analysis Controls -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
        <div>
          <label class="text-xs text-gray-500">Date de Début</label>
          <input type="date" class="w-full border rounded p-2" v-model="startDate" />
        </div>
        <div>
          <label class="text-xs text-gray-500">Date de Fin</label>
          <input type="date" class="w-full border rounded p-2" v-model="endDate" />
        </div>
        <div>
          <label class="text-xs text-gray-500">Montant investi</label>
          <input type="number" class="w-full border rounded p-2" v-model="amount" />
        </div>
        <div>
          <label class="text-xs text-gray-500">Devise</label>
          <select class="w-full border rounded p-2" v-model="currency">
            <option v-for="c in ['USD', 'XOF', 'EUR']" :key="c">{{ c }}</option>
          </select>
        </div>
      </div>

      <!-- Price + Chart -->
      <div class="mb-4">
        <p class="text-sm text-gray-500">Dernière mise à jour : {{ lastUpdate }}</p>
        <div class="text-2xl font-bold mt-1">{{ formattedPrice }}</div>
        <div class="text-sm text-gray-400">USD {{ volume.toLocaleString() }} <span class="text-green-600">(7.42%)</span></div>
      </div>

      <!-- Chart Placeholder -->
      <div class="h-32 bg-green-100 rounded-lg mb-6 flex items-center justify-center text-green-600">
        [📈 Chart goes here]
      </div>

      <!-- Description -->
      <div class="mb-6 text-sm text-gray-700 leading-relaxed">
        {{ asset.description }}
      </div>

      <!-- Action -->
      <button class="bg-teal-700 text-white px-6 py-2 rounded-lg w-full" @click="invest">investir</button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  visible: Boolean,
  asset: Object,
})
const emits = defineEmits(['close'])

const startDate = ref('2025-01-01')
const endDate = ref('2025-05-01')
const amount = ref(0)
const currency = ref('USD')
const lastUpdate = '05/15/2025, 04:15 PM'
const volume = 16095
const formattedPrice = 'USD 180,85'

const close = () => emits('close')
const invest = () => {
  console.log("Investing in", props.asset.name, "with", amount.value, currency.value)
  emits('close')
}
</script>
