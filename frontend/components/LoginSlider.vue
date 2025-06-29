<script setup>
import { Swiper, SwiperSlide } from 'swiper/vue'
import 'swiper/css'
import 'swiper/css/pagination'
import { Pagination } from 'swiper/modules'
</script>

<template>
  <div class="w-full h-full flex justify-center items-center px-10 bg-[#0D5254]">
    <Swiper
      :modules="[Pagination]"
      :pagination="{ clickable: true }"
      class="w-full h-full flex justify-center items-center"
    >
      <SwiperSlide>
        <div class="flex flex-col justify-center items-center text-white text-center">
            <NuxtLink to="/">
          <img src="/logo-W.svg" alt="PlayInvest" class="mb-10 w-40" />
          </NuxtLink>
          <img src="/images/Login Image.png" alt="Illustration" class="mb-10 max-w-md" />
          <h2 class="text-xl font-semibold mb-2">
            Rejoignez PlayInvest et Lancez Votre Voyage d'Investissement
          </h2>
          <p class="text-sm max-w-md">
            Créez un compte gratuit pour accéder à des outils d'investissement ludiques, sécurisés et adaptés à vos besoins. Commencez à investir en toute confiance, à votre rythme.
          </p>
        </div>
      </SwiperSlide>

      <SwiperSlide>
        <div class="text-white text-center px-10">
          <h2 class="text-xl font-semibold mb-2">Classement & Quiz</h2>
          <p class="text-sm max-w-md mx-auto">
            Faites des quiz, débloquez des fonds fictifs et grimpez dans le classement mondial.
          </p>
        </div>
      </SwiperSlide>

      <!-- Add more SwiperSlide blocks here as needed -->
    </Swiper>
  </div>
</template>
