<template>
  <div class="w-full max-w-6xl mx-auto">
    <!-- Header -->
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-2xl font-semibold">🆕 Actualités Récentes</h2>
      <div class="flex gap-2">
        <button @click="goPrev" class="text-2xl">&lsaquo;</button>
        <button @click="goNext" class="text-2xl">&rsaquo;</button>
      </div>
    </div>

    <!-- Slider Container -->
    <div ref="sliderContainer" class="keen-slider overflow-hidden">
 
      <div
        v-for="(anews, index) in news"
        :key="index"
        class="keen-slider__slide px-4"
      >
        <a :href="`${anews.url}`" target="_blank" rel="noopener">
          <div class="rounded-xl overflow-hidden bg-white shadow-md">
            <img
              :src="`${apiBase}${anews.image_path}`"
              :alt="anews.title"
              class="w-full h-48 object-cover"
            />
            <div class="p-4">
              <h3 class="text-lg font-bold">{{ anews.title }}</h3>
              <p class="text-sm text-gray-400">
                {{ formatDate(anews.published_at) }} • {{ anews.audience }}
              </p>
            </div>
          </div>
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import KeenSlider from 'keen-slider'
import axios from 'axios'

const config = useRuntimeConfig()
const apiBase = config.public.apiBase

const news = ref([])
const sliderContainer = ref(null)
let sliderInstance = null

let autoplayTimer = null
let isMouseOver = false

function startAutoplay() {
  stopAutoplay()
  autoplayTimer = setInterval(() => {
    if (!isMouseOver && sliderInstance?.track?.details) {
      sliderInstance.next()
    }
  }, 4000)
}

function stopAutoplay() {
  clearInterval(autoplayTimer)
}

onMounted(async () => {
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get(`${apiBase}/api/news`, {
      headers: { Authorization: `Bearer ${token}` },
    })

    news.value = res.data
      .sort((a, b) => new Date(b.published_at) - new Date(a.published_at))
      .slice(0, 5)
    console.log(news.value)
    // Ensure DOM is updated with the slides
    await nextTick()

    if (sliderContainer.value) {
      sliderInstance = new KeenSlider(sliderContainer.value, {
        loop: true,
        slides: {
          perView: 1,
          spacing: 10,
        },
      })

      sliderContainer.value.addEventListener('mouseover', () => (isMouseOver = true))
      sliderContainer.value.addEventListener('mouseout', () => (isMouseOver = false))

      startAutoplay()
    }
  } catch (err) {
    console.error('❌ Erreur chargement news:', err)
  }
})

onUnmounted(() => {
  stopAutoplay()
  sliderInstance?.destroy()
})

function goPrev() {
  if (sliderInstance?.track?.details) {
    sliderInstance.prev()
  }
}

function goNext() {
  if (sliderInstance?.track?.details) {
    sliderInstance.next()
  }
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}
</script>

<style scoped>
@import 'keen-slider/keen-slider.min.css';

.keen-slider__slide {
  min-width: 100% !important;
}
</style>
