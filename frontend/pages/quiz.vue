
<template>
  <div>
    <!-- Hero Section -->
    <QuizHero />
    <QuizFeatures />
    <!-- Asset Table Section -->
    <QuizChallenges />
    <QuizProgress/>
    <QuizLearningResources/>
  </div>
</template>

<script setup>
import QuizHero from '~/components/Quiz/QuizHero.vue'
import QuizFeatures from '~/components/Quiz/QuizFeatures.vue'
import QuizChallenges from '~/components/Quiz/QuizChallenges.vue'
import QuizProgress from '~/components/Quiz/QuizProgress.vue'
import QuizLearningResources from '~/components/Quiz/QuizLearningResources.vue'
</script>
