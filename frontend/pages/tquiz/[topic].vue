<template>
  <div v-if="quiz.length" class="p-4 max-w-xl mx-auto">
    <h1 class="text-2xl font-bold mb-2">Quiz : {{ topic }}</h1>
    <p class="text-sm text-gray-600 mb-4">⏱ Temps écoulé : {{ formattedTime }}</p>

    <div class="mb-6">
      <div class="mb-4">
  <div class="flex justify-between items-center mb-1">
    <span class="font-semibold text-blue-700">🔹 Question {{ currentIndex + 1 }} sur {{ quiz.length }}</span>
    <span class="text-sm text-gray-600">{{ progressPercent }}%</span>
  </div>
  <div class="w-full h-3 bg-gray-200 rounded-full">
    <div
      class="h-full bg-blue-500 rounded-full transition-all duration-300"
      :style="{ width: progressPercent + '%' }"
    ></div>
  </div>
</div>

      <p class="mb-4">{{ currentQuestion.question }}</p>

      <div class="pl-4">
        <label
          v-for="(text, key) in currentQuestion.options"
          :key="key"
          class="block mb-2 cursor-pointer"
        >
          <input
            type="radio"
            :name="'question'"
            :value="key"
            v-model="answers[currentIndex]"
            class="mr-2"
          />
          {{ key }}: {{ text }}
        </label>
      </div>
    </div>

    <div class="flex justify-between">
      <button
        v-if="currentIndex > 0"
        @click="prev"
        class="px-4 py-2 bg-gray-300 rounded"
      >
        Précédent
      </button>

      <button
        v-if="currentIndex < quiz.length - 1"
        @click="next"
        class="ml-auto px-4 py-2 bg-blue-600 text-white rounded"
      >
        Suivant
      </button>

      <button
        v-else
        @click="submit"
        class="ml-auto px-4 py-2 bg-green-600 text-white rounded"
      >
        Valider
      </button>
    </div>

    <div v-if="showResults" class="mt-6 text-lg font-semibold">
  <p :class="scorePercent >= 80 ? 'text-green-600' : 'text-red-600'">
    {{ scoreMessage }}
  </p>
  <p class="text-sm text-gray-500">⏱ Temps : {{ formattedTime }}</p>
</div>
  </div>

  <div v-else class="text-center text-gray-500 p-4">Chargement du quiz...</div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const config = useRuntimeConfig()
const apiBase = config.public.apiBase

const route = useRoute()
const topic = decodeURIComponent(route.params.topic)

const quiz = ref([])
const answers = ref([])
const currentIndex = ref(0)
const score = ref(0)
const showResults = ref(false)

// Timer state
const secondsElapsed = ref(0)
let timer = null

onMounted(async () => {
  const res = await axios.get(`${apiBase}/api/quizzes?topic=${encodeURIComponent(topic)}`)
  quiz.value = res.data
  answers.value = Array(res.data.length).fill(null)

  // Start timer
  timer = setInterval(() => {
    secondsElapsed.value++
  }, 1000)
})

onUnmounted(() => {
  clearInterval(timer)
})

const currentQuestion = computed(() => quiz.value[currentIndex.value] || {})

function next() {
  if (currentIndex.value < quiz.value.length - 1) currentIndex.value++
}

function prev() {
  if (currentIndex.value > 0) currentIndex.value--
}

async function submit() {
  clearInterval(timer)

  let correct = 0
  quiz.value.forEach((q, i) => {
    if (answers.value[i] === q.correct_answer) correct++
  })
  score.value = correct
  showResults.value = true

  // Save result to backend
  const resultPayload = {
    topic,
    module: quiz.value[0]?.module || null,
    score: score.value,
    total: quiz.value.length,
    percent: scorePercent.value,
    time_seconds: secondsElapsed.value,
    passed: scorePercent.value >= 80,
    completed_at: new Date().toISOString()
  }

  try {
    await axios.post(`${apiBase}/api/quiz-results`, resultPayload)
    console.log("✅ Quiz result saved.")
  } catch (err) {
    console.error("❌ Failed to save quiz result:", err)
  }
}


const formattedTime = computed(() => {
  const minutes = Math.floor(secondsElapsed.value / 60)
  const seconds = secondsElapsed.value % 60
  return `${minutes}m ${seconds}s`
})

const progressPercent = computed(() =>
  Math.round(((currentIndex.value + 1) / quiz.value.length) * 100)
)

const scorePercent = computed(() =>
  Math.round((score.value / quiz.value.length) * 100)
)

const scoreMessage = computed(() =>
  scorePercent.value >= 80
    ? `🎉 Bravo ! Vous avez réussi le quiz (${scorePercent.value}%)`
    : `❌ Vous avez échoué (${scorePercent.value}%) — 80% requis`
)
</script>
