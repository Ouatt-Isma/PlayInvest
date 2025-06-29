<template>
  <div class="w-full max-w-4xl mx-auto">
    <!-- Header & Arrows -->
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-2xl font-semibold">Nouveaux articles</h2>
      <div class="flex gap-2">
        <button @click="slider?.prev()" class="text-2xl">&lsaquo;</button>
        <button @click="slider?.next()" class="text-2xl">&rsaquo;</button>
      </div>
    </div>

    <!-- Slider -->
    <div ref="container" class="keen-slider overflow-hidden">
      <div
        v-for="(article, index) in articles"
        :key="index"
        class="keen-slider__slide"
      >
        <div class="w-full px-4">
          <div class="rounded-xl overflow-hidden bg-white shadow-md w-full">
            <img
              :src="article.image"
              :alt="article.title"
              class="w-full h-full object-cover"
            />
            <div class="p-4">
              <h3 class="text-xl font-semibold mb-2">{{ article.title }}</h3>
              <p class="text-sm text-gray-600">
                {{ article.date }} • Rédigé par {{ article.author }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useKeenSlider } from 'keen-slider/vue.es'

const articles = [
  {
    title: 'Comment débuter dans l’investissement sans risque',
    date: '9/5/2025',
    author: 'John Doe',
    image: '/images/B1.jpg',
  },
  {
    title: 'Stratégies d’Investissement 2025 pour l’Europe',
    date: '10/5/2025',
    author: 'John Doe',
    image: '/images/B2.jpg',
  },
  {
    title: 'L’Afrique : Un Continent d’Opportunités',
    date: '11/5/2025',
    author: 'John Doe',
    image: '/images/B3.jpg',
  },
]

const [container, slider] = useKeenSlider({
  loop: true,
  slides: {
    perView: 1,
    spacing: 0,
  },
})

let autoplayTimer
let mouseOver = false

const setupAutoplay = () => {
  const clearNextTimeout = () => clearTimeout(autoplayTimer)
  const nextTimeout = () => {
    clearTimeout(autoplayTimer)
    if (mouseOver || !slider.value) return
    autoplayTimer = setTimeout(() => {
      slider.value.next()
      nextTimeout()
    }, 3000)
  }

  if (container.value) {
    container.value.addEventListener('mouseover', () => {
      mouseOver = true
      clearNextTimeout()
    })
    container.value.addEventListener('mouseout', () => {
      mouseOver = false
      nextTimeout()
    })
  }

  nextTimeout()
}

// Wait until slider is initialized
watch(slider, (newVal) => {
  if (newVal) {
    setupAutoplay()
  }
})

onUnmounted(() => {
  clearTimeout(autoplayTimer)
})
</script>



<style scoped>
@import 'keen-slider/keen-slider.min.css';

.keen-slider__slide {
  min-width: 100% !important;
}
</style>
