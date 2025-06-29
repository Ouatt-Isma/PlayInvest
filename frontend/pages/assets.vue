
<template>
  <div>
    <!-- Hero Section -->
    <ActifsHero />
    <ActifFilters @update:graphPeriod="graphPeriod = $event"  @update:assets="filteredAssets = $event" />

    <AssetsTable :assets="filteredAssets" :graphPeriod="graphPeriod" :key="graphPeriod" />  
    </div>
</template>

<script setup>
import ActifFilters from '~/components/ActifFilters.vue'
import AssetsTable from '~/components/AssetsTable.vue'
import { ref } from 'vue'
const filteredAssets = ref([])
</script>
