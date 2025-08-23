<template>
  <div class="grid md:grid-cols-3 gap-6 p-6 max-w-6xl mx-auto">
    <!-- Module/Topic Selector -->
    <div class="md:col-span-1 space-y-4">
      <h2 class="text-lg font-bold">📘 Choisissez un module</h2>
      <select v-model="selectedModule" class="w-full p-2 border rounded">
        <option disabled value="">-- Module --</option>
        <option
          v-for="mod in modules"
          :key="`m-${mod}`"
          :value="mod"
        >
          {{ mod }}
        </option>
      </select>

      <h2 class="text-lg font-bold">🎯 Choisissez un quiz</h2>
      <select v-model="selectedTopic" class="w-full p-2 border rounded" @change="loadQuiz">
        <option disabled value="">-- Sujet --</option>
        <option
          v-for="topic in filteredTopics"
          :key="`t-${topic}`"
          :value="topic"
        >
          {{ topic }}
        </option>
      </select>
    </div>

    <!-- Quiz View -->
    <div class="w-full max-w-3xl mx-auto">
      <p v-if="alreadyPassed" class="text-green-600 text-sm font-medium">
        ✅ Vous avez déjà réussi ce quiz. Vous pouvez le refaire si vous le souhaitez.
      </p>

      <div v-if="quiz.length" class="space-y-6">
        <!-- Timer & Progress -->
        <div class="flex justify-between items-center">
          <div class="text-blue-700 font-semibold">
            🔹 Question {{ currentIndex + 1 }} sur {{ quiz.length }}
          </div>
          <div class="text-sm text-gray-500">⏱ {{ formattedTime }}</div>
        </div>

        <div class="w-full h-2 bg-gray-200 rounded">
          <div
            class="h-full bg-blue-500 rounded"
            :style="{ width: (quiz.length ? progressPercent : 0) + '%' }"
          ></div>
        </div>

        <!-- Current Question -->
        <div>
          <p class="mb-2 font-medium">{{ currentQuestion.question }}</p>
          <div class="pl-4">
            <label
              v-for="(text, key) in (currentQuestion.options || {})"
              :key="key"
              class="block mb-2 cursor-pointer"
            >
              <input
                type="radio"
                name="question"
                :value="key"
                v-model="answers[currentIndex]"
                class="mr-2"
              />
              {{ key }}: {{ text }}
            </label>
          </div>
        </div>

        <!-- Navigation -->
        <div class="flex justify-between">
          <button
            v-if="currentIndex > 0"
            @click="prev"
            class="px-4 py-2 bg-gray-300 rounded"
          >
            ← Précédent
          </button>

          <button
            v-if="currentIndex < quiz.length - 1"
            @click="next"
            class="ml-auto px-4 py-2 bg-blue-600 text-white rounded"
          >
            Suivant →
          </button>

          <button
            v-else
            @click="submit"
            class="ml-auto px-4 py-2 bg-green-600 text-white rounded"
          >
            Valider
          </button>
        </div>

        <!-- Result -->
        <div v-if="showResults" class="mt-4 font-semibold">
          <p :class="scorePercent >= 80 ? 'text-green-600' : 'text-red-600'">
            {{ scoreMessage }}
          </p>
        </div>
      </div>

      <div v-else-if="selectedTopic" class="text-gray-500 mt-8">
        Chargement du quiz...
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  requiresAuth: true,
})

import { ref, computed, onMounted, onUnmounted } from 'vue'
import axios from 'axios'

const alreadyPassed = ref(false)

const config = useRuntimeConfig()
const apiBase = config.public.apiBase

// State
const quizzes = ref([])
const selectedModule = ref('')
const selectedTopic = ref('')
const quiz = ref([])
const answers = ref([])
const currentIndex = ref(0)
const score = ref(0)
const showResults = ref(false)

// Timer
const secondsElapsed = ref(0)
let timer = null

// Fetch all quizzes
onMounted(async () => {
  const token = useCookie("token").value
  const res = await axios.get(`${apiBase}/api/quizzes`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  quizzes.value = res.data
})

const modules = computed(() => [...new Set(quizzes.value.map(q => q.module))])

const filteredTopics = computed(() =>
  [...new Set(quizzes.value
    .filter(q => q.module === selectedModule.value)
    .map(q => q.topic))]
)

const currentQuestion = computed(() => quiz.value[currentIndex.value] || {})

const progressPercent = computed(() => {
  const total = quiz.value.length
  if (!total) return 0
  const pct = Math.round(((currentIndex.value + 1) / total) * 100)
  return Math.min(100, Math.max(0, pct))
})

const formattedTime = computed(() => {
  const m = Math.floor(secondsElapsed.value / 60)
  const s = secondsElapsed.value % 60
  return `${m}m ${s}s`
})

const scorePercent = computed(() => {
  const total = quiz.value.length
  if (!total) return 0
  return Math.round((score.value / total) * 100)
})

const scoreMessage = computed(() =>
  scorePercent.value >= 80
    ? `🎉 Bravo ! Vous avez réussi (${scorePercent.value}%)`
    : `❌ Échec (${scorePercent.value}%) — minimum 80% requis`
)

async function loadQuiz() {
  currentIndex.value = 0
  showResults.value = false
  score.value = 0
  clearInterval(timer)
  secondsElapsed.value = 0
  alreadyPassed.value = false

  try {
    const token = useCookie("token").value
    const statusRes = await axios.get(
      `${apiBase}/api/quiz-results/status?topic=${encodeURIComponent(selectedTopic.value)}`,
      { headers: { Authorization: `Bearer ${token}` } }
    )
    alreadyPassed.value = !!statusRes.data.passed
  } catch (err) {
    console.warn('Could not check quiz status', err)
  }

  const token = useCookie("token").value
  const res = await axios.get(
    `${apiBase}/api/quizzes?topic=${encodeURIComponent(selectedTopic.value)}`,
    { headers: { Authorization: `Bearer ${token}` } }
  )
  quiz.value = res.data || []
  answers.value = Array(quiz.value.length).fill(null)

  timer = setInterval(() => { secondsElapsed.value++ }, 1000)
}

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

  const resultPayload = {
    topic: selectedTopic.value,
    module: selectedModule.value,
    score: score.value,
    total: quiz.value.length,
    percent: scorePercent.value,
    time_seconds: secondsElapsed.value,
    passed: scorePercent.value >= 80,
    completed_at: new Date().toISOString()
  }

  try {
    const token = useCookie("token").value
    await axios.post(`${apiBase}/api/quiz-results`, resultPayload, {
      headers: { Authorization: `Bearer ${token}` }
    })
    console.log('✅ Résultat enregistré.')
  } catch (err) {
    console.error("❌ Erreur d'enregistrement:", err)
  }
}

onUnmounted(() => {
  clearInterval(timer)
})
</script>
