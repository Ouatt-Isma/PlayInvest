<template>
  <div class="p-4 sm:p-6 bg-gray-50 min-h-screen">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center mb-6 gap-4">
      <div>
        <h1 class="text-2xl sm:text-3xl font-bold">
          Tableau de Bord des Investissements
        </h1>
        <p class="text-xs sm:text-sm text-gray-500">
          Dernière mise à jour : {{ lastUpdate }}
        </p>
      </div>

      <NuxtLink
        to="/assets"
        class="bg-teal-800 text-white px-5 py-2 rounded hover:bg-teal-700 text-center"
      >
        Investir
      </NuxtLink>
    </div>

    <div class="space-y-10">
      <!-- Performance: chart + right-side tools -->
      <div class="bg-white p-4 sm:p-6 rounded-xl shadow-md mb-6">
        <h2 class="text-base sm:text-lg font-semibold mb-1">
          Graphique d’évolution du rendement global des investissements
        </h2>
        <p class="text-xs sm:text-sm text-gray-500 mb-4">
          Suivez l’évolution de la valeur totale de votre portefeuille d’investissements, visualisez vos gains et pertes au fil du temps.
        </p>

        <!-- 2-col layout: chart left, controls right -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 pr-2 sm:pr-4">
          <!-- Left: chart -->
          <div class="lg:col-span-8">
            <div class="w-full h-[560px] sm:h-[420px] lg:h-[500px]">
              <PerfPlot />
            </div>
          </div>

          <!-- Right: date range + ranking -->
          <div class="lg:col-span-4 space-y-6">
            <PerfDateRangeCard />
            <UserRankingCard />
          </div>
        </div>
      </div>

      <!-- Main Grid Layout -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Left column -->
        <div class="lg:col-span-2 space-y-6">
          <Portfolio />
          <InvestmentHistory />
          <ChallengeHistory />
        </div>

        <!-- Right column: Simulator -->
        <div class="space-y-6">
          <PastPerfSimulator />
        </div>
      </div>
    </div>
  </div>




  <!-- Bottom promo row -->
<div class="bg-[#f8faff] py-8 sm:py-10 px-4 sm:px-6 flex justify-center">
  <div
    class="flex flex-col lg:flex-row gap-4 sm:gap-6 w-full max-w-6xl"
  >
  
    <!-- Challenge Card -->
    <div
      class=" w-full lg:w-1/2  flex flex-col sm:flex-row items-center bg-white p-4 sm:p-6 rounded-2xl shadow w-full lg:w-1/2"
    >
      <img
        src="/images/challenge.png"
        alt="Challenge icon"
        class="w-20 h-20 sm:w-24 sm:h-24 mb-4 sm:mb-0 sm:mr-6"
      />
      <div class="text-center sm:text-left">
        <h3 class="text-lg sm:text-xl font-bold mb-1">
          Challenge Hebo
        </h3>
        <p class="text-gray-500 mb-4 text-sm sm:text-base">
          Débloquez de l’argent fictif dans votre portefeuille et participez à des challenges pour gagner des fonds fictifs.
        </p>

        <button
          class="flex items-center justify-center sm:justify-start gap-2 px-4 py-2 rounded-full border border-gray-300 text-sm font-semibold hover:bg-gray-100 mx-auto sm:mx-0"
          @click="open = true"
        >
          Commencer le Challenge
          <span>→</span>
        </button>

        <ChallengeWeeklyModal v-model="open" :assets="pair" />
      </div>
    </div>

    <!-- Quiz Card -->
    <div
      class="w-full lg:w-1/2 flex flex-col sm:flex-row items-center bg-white p-4 sm:p-6 rounded-2xl shadow w-full lg:w-1/2"
    >
      <img
        src="/images/image Q5.png"
        alt="Quiz icon"
        class="w-20 h-20 sm:w-24 sm:h-24 mb-4 sm:mb-0 sm:mr-6"
      />
      <div class="text-center sm:text-left">
        <h3 class="text-lg sm:text-xl font-bold mb-1">Quiz</h3>
        <p class="text-gray-500 mb-4 text-sm sm:text-base">
          Répondez à des quiz interactifs pour débloquer des fonds fictifs et améliorer vos compétences en investissement.
        </p>

        <NuxtLink
          to="/makequiz"
          class="inline-flex items-center justify-center sm:justify-start px-4 py-2 rounded-full border border-gray-300 text-sm font-semibold hover:bg-gray-100 mx-auto sm:mx-0"
        >
          Commencez un Quiz →
        </NuxtLink>
      </div>
    </div>
  </div>
</div>

  <!-- Bottom promo row -->
  <div class="bg-[#f8faff] py-8 sm:py-10 px-4 sm:px-6 flex justify-center">
    <div class="flex flex-col sm:flex-row gap-4 sm:gap-6 w-full max-w-6xl items-center sm:items-stretch">
      <!-- Example promo boxes -->
      <div class="flex-1 bg-white rounded-xl shadow p-4 sm:p-6 text-center">
        <h3 class="font-semibold text-gray-700 text-sm sm:text-base">Découvrez nos nouvelles stratégies</h3>
        <p class="text-xs sm:text-sm text-gray-500 mt-2">Explorez les opportunités de croissance à long terme.</p>
      </div>

      <div class="flex-1 bg-white rounded-xl shadow p-4 sm:p-6 text-center">
        <h3 class="font-semibold text-gray-700 text-sm sm:text-base">Suivi en temps réel</h3>
        <p class="text-xs sm:text-sm text-gray-500 mt-2">Gardez un œil sur les performances de vos investissements.</p>
      </div>
    </div>
  </div>

</template>



<script setup>
definePageMeta({
  requiresAuth: true,  
})
import Portfolio from '~/components/Portfolio.vue'
import InvestmentHistory from '~/components/InvestmentHistory.vue'
import PastPerfSimulator from '~/components/PastPerfSimulator.vue'
import PerfPlot from '~/components/PerfPlot.vue'

// NEW cards on the right of the chart
import PerfDateRangeCard from '~/components/PerfDateRangeCard.vue'
import UserRankingCard from '~/components/UserRankingCard.vue'

import { ref, onMounted  } from 'vue'
import axios from 'axios'

import ChallengeWeeklyModal from '~/components/ChallengeWeeklyModal.vue'

const open = ref(false)
const pair = ref([null])

import ChallengeHistory from '~/components/ChallengeHistory.vue'

const lastUpdate= ref('')
const auth = useAuth()
auth.init()


const token = useCookie("token").value
const config = useRuntimeConfig()
const apiBase = config.public.apiBase 
const response = await axios.get(`${apiBase}/api/portfolio`,{
    headers: {
      Authorization: `Bearer ${token}`  // assure-toi que `token` est défini
    }
  })

onMounted(async () => {
  console.log("✅ Dashboard mounted, fetching last update...")
  try {
    const token = useCookie("token").value
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase
    const res = await axios.get(`${apiBase}/api/portfolio/last_update`,{
      headers: {
        Authorization: `Bearer ${token}`  // assure-toi que `token` est défini
      }
    })

    lastUpdate.value = new Date(res.data.last_update)
  .toLocaleString("fr-FR", {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  })
  } catch (error) {
    console.warn('API last update portfolios error')
    console.log(error)
  
  }
})
</script>
