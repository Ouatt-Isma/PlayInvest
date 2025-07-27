<template>
  <div class="p-6 bg-gray-50 min-h-screen">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">Tableau de Bord des Investissements</h1>
      <NuxtLink to="/assets" class="bg-teal-800 text-white px-5 py-2 rounded hover:bg-teal-700">
        Investir
      </NuxtLink>
    </div>

    <!-- Performance Chart -->
    <div class="bg-white p-6 rounded-xl shadow-md mb-6">
      <h2 class="text-lg font-semibold mb-1">Graphique d’évolution du rendement global des investissements</h2>
      <p class="text-sm text-gray-500 mb-4">
        Suivez l’évolution de la valeur totale de votre portefeuille d'investissements, visualisez vos gains et pertes au fil du temps.
      </p>
      <PerfPlot />
    </div>

    <!-- Grid Layout -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Left column: Portfolio + History -->
      <div class="lg:col-span-2 space-y-6">
        <Portfolio />
        <InvestmentHistory />
      </div>

      <!-- Right column: Simulator -->
      <div class="space-y-6">
        <PastPerfSimulator />
      </div>
    </div>
  </div>
  <div class="bg-[#f8faff] py-10 px-6 flex justify-center">
    <div class="flex gap-6 w-full max-w-6xl">
      <!-- Challenge Card -->
      <div class="flex items-center bg-white p-6 rounded-2xl shadow w-1/2">
        <img src="/images/Challenge.png" alt="Challenge icon" class="w-24 h-24 mr-6" />
        <div>
          <h3 class="text-xl font-bold mb-1">Challenge Hebo</h3>
          <p class="text-gray-500 mb-4">
            Déposez de l’argent fictif dans votre portefeuille et participez à des challenges pour gagner des fonds fictifs.
          </p>
          <button class="flex items-center gap-2 px-4 py-2 rounded-full border border-gray-300 text-sm font-semibold hover:bg-gray-100">
            Commencer le Challenge
            <span>→</span>
          </button>
        </div>
      </div>

      <!-- Quiz Card -->
      <div class="flex items-center bg-white p-6 rounded-2xl shadow w-1/2">
        <img src="/images/image Q5.png" alt="Quiz icon" class="w-24 h-24 mr-6" />
        <div>
          <h3 class="text-xl font-bold mb-1">Quiz</h3>
          <p class="text-gray-500 mb-4">
            Répondez à des quiz interactifs pour débloquer des fonds fictifs et améliorer vos compétences en investissement.
          </p>
          <button class="flex items-center gap-2 px-4 py-2 rounded-full border border-gray-300 text-sm font-semibold hover:bg-gray-100">
            Commencer le Quiz
            <span>→</span>
          </button>
        </div>
      </div>
    </div>
  </div>

</template>


<script>
// import { useAuth } from '~/composables/useAuth'

// export default {
//   layout() {
//     const { isAuthenticated } = useAuth()
//     return isAuthenticated.value ? 'connected' : 'default'
//   }
// }


import Portfolio from '~/components/Portfolio.vue'
import InvestmentHistory from '~/components/InvestmentHistory.vue'
import PastPerfSimulator from '~/components/PastPerfSimulator.vue'
import PerfPlot from '~/components/PerfPlot.vue'
</script>


