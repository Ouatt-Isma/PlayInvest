<template>
  <div class="p-4 max-w-xl mx-auto">
    <h2 class="text-xl font-bold mb-4">Choisissez un module</h2>
    <select v-model="selectedModule" class="w-full p-2 border rounded mb-4">
      <option disabled value="">-- Sélectionnez un module --</option>
      <option v-for="mod in modules" :key="mod">{{ mod }}</option>
    </select>

    <h2 v-if="topics.length" class="text-xl font-bold mb-2">Choisissez un quiz</h2>
    <select v-model="selectedTopic" class="w-full p-2 border rounded" v-if="topics.length">
      <option disabled value="">-- Sélectionnez un quiz --</option>
      <option v-for="topic in topics" :key="topic">{{ topic }}</option>
    </select>

    <button
      v-if="selectedTopic"
      @click="goToQuiz"
      class="mt-4 bg-blue-600 text-white px-4 py-2 rounded"
    >
      Commencer le quiz
    </button>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const config = useRuntimeConfig()
const apiBase = config.public.apiBase
const router = useRouter()

const quizzes = ref([])
const selectedModule = ref('')
const selectedTopic = ref('')

// Fetch quizzes on mount
onMounted(async () => {
  const res = await axios.get(`${apiBase}/api/quizzes`)
  quizzes.value = res.data
})

const modules = computed(() => [...new Set(quizzes.value.map(q => q.module))])

const topics = computed(() => {
  const allTopics = quizzes.value
    .filter(q => q.module === selectedModule.value)
    .map(q => q.topic)

  // Return only unique topic names
  return [...new Set(allTopics)]
})
function goToQuiz() {
  router.push({ path: `/tquiz/${encodeURIComponent(selectedTopic.value)}` })
}
</script>
