<template>
  <div class="p-4 bg-white rounded-xl shadow">
    <h3 class="text-base font-semibold mb-3">Télécharger mon rapport d'analyse</h3>

    <div class="grid grid-cols-2 gap-3">
      <div class="flex flex-col">
        <label class="text-xs text-gray-500 mb-1">Début</label>
        <input type="date" v-model="start" class="border rounded px-2 py-1 text-sm" />
      </div>
      <div class="flex flex-col">
        <label class="text-xs text-gray-500 mb-1">Fin</label>
        <input type="date" v-model="end" class="border rounded px-2 py-1 text-sm" />
      </div>
    </div>

    <div class="flex gap-2 mt-3">
      <!-- <button
        class="px-3 py-1.5 text-sm rounded bg-slate-800 text-white hover:bg-slate-700 disabled:opacity-50"
        :disabled="!start || !end || start > end"
        @click="$emit('apply', { start, end })"
      >
        Appliquer
      </button> -->
      <button
        class="px-3 py-1.5 text-sm rounded border hover:bg-gray-50"
        @click="reset"
      >
        Réinitialiser
      </button>
      <!-- <button
        class="ml-auto px-3 py-1.5 text-sm rounded bg-emerald-600 text-white hover:bg-emerald-500"
        @click="$emit('download')"
      >
        
      </button> -->

      <NuxtLink to="/unavailable"  class="ml-auto px-3 py-1.5 text-sm rounded bg-emerald-600 text-white hover:bg-emerald-500">
        Télécharger le rapport
      </NuxtLink>

    </div>

    <p v-if="start && end && start > end" class="text-[11px] text-red-600 mt-2">
      La date de début doit être antérieure à la date de fin.
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const start = ref('')
const end = ref('')
const reset = () => { start.value = ''; end.value = '' }
</script>
