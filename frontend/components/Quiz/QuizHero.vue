<template>
    <div class="max-w-7xl mx-auto px-4 md:px-8 flex flex-col-reverse md:flex-row items-center gap-12">
  <!-- <div class="flex flex-col-reverse lg:flex-row items-center justify-between gap-10 lg:gap-20 px-6 py-12 lg:px-24 bg-[#F5F7FB]"> -->
    <!-- Text content -->
    <div class="max-w-xl text-center lg:text-left">
      <h1 class="text-4xl lg:text-5xl font-extrabold text-[#121212] leading-tight mb-4">
        Quiz & Défis PlayInvest
      </h1>
      <p class="text-gray-500 text-lg mb-6">
        Testez vos connaissances financières, défiez d'autres investisseurs et gagnez des fonds virtuels pour investir !
      </p>
      <div class="flex gap-4">
      <NuxtLink to="/makequiz" class="bg-teal-800 text-white font-semibold px-6 py-3 rounded-lg hover:bg-teal-900 transition">
        Commencez un Quiz
      </NuxtLink>

      <button class="border border-teal-800 text-teal-800 font-semibold px-6 py-3 rounded-lg hover:bg-teal-50 transition" @click="open = true">
        Challenge Hebdo
      </button>

      <ChallengeWeeklyModal
        v-model="open"
        :assets="pair"
      />
      </div>
    </div>

    <!-- <div class="flex gap-4">
        <button class="bg-teal-800 text-white font-semibold px-6 py-3 rounded-lg hover:bg-teal-900 transition">Commencer</button>
        <button class="border border-teal-800 text-teal-800 font-semibold px-6 py-3 rounded-lg hover:bg-teal-50 transition">En savoir plus</button>
      </div> -->

    <!-- Image -->
    <div class="max-w-lg w-full">
      <img src="/images/Quiz image.png" alt="Quiz PlayInvest" class="w-full max-w-md lg:max-w-[400px] xl:max-w-[440px]" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ChallengeWeeklyModal from '~/components/ChallengeWeeklyModal.vue'

const open = ref(false)
const pair = ref([null
])


</script>
