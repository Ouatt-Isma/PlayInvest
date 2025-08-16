<template>
  <div>
    <div v-for="(question, index) in questions" :key="question.id" class="mb-6">
      <p class="font-semibold">{{ index + 1 }}. {{ question.question }}</p>
      <div class="mt-2">
        <label
          v-for="(answer, i) in question.answers"
          :key="i"
          class="block mb-1"
        >
          <input
            type="radio"
            :name="'question-' + question.id"
            :value="i"
            v-model="userAnswers[question.id]"
            class="mr-2"
          />
          {{ answer }}
        </label>
      </div>
    </div>
    <button @click="submitQuiz" class="mt-4 px-4 py-2 bg-blue-500 text-white rounded">
      Submit
    </button>
    <div v-if="showResults" class="mt-6">
      <h2 class="text-xl font-bold mb-2">Results</h2>
      <p>You scored {{ score }} out of {{ questions.length }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  questions: {
    type: Array,
    required: true
  }
})

const userAnswers = ref({})
const showResults = ref(false)
const score = ref(0)

const submitQuiz = () => {
  let correct = 0
  props.questions.forEach((question) => {
    if (userAnswers.value[question.id] == question.correctAnswerIndex) {
      correct++
    }
  })
  score.value = correct
  showResults.value = true
}
</script>
