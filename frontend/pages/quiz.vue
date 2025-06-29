
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
import QuizHero from '~/components/QuizHero.vue'
import QuizFeatures from '~/components/QuizFeatures.vue'
import QuizChallenges from '~/components/QuizChallenges.vue'
import QuizProgress from '~/components/QuizProgress.vue'
import QuizLearningResources from '~/components/QuizLearningResources.vue'
</script>
