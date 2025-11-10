<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header Section -->
    <header class="bg-white shadow-sm py-4 px-6 mb-6 flex items-center justify-between">
      <h1 class="text-xl sm:text-2xl font-bold text-gray-800 flex items-center gap-2">
        <span class="bg-gradient-to-br from-blue-600 to-green-500 text-white px-2 py-1 rounded-lg">PI</span>
        Test de Profil Investisseur
      </h1>

      <router-link
        to="/"
        class="text-blue-600 hover:underline text-sm sm:text-base"
      >
        ← Retour au tableau de bord
      </router-link>
    </header>

    <!-- Main Quiz Component -->
    <main class="max-w-6xl mx-auto px-4 sm:px-6">
      <ProfilInvestQuiz />
    </main>
  </div>
</template>

<script setup>
import ProfilInvestQuiz from "~/components/ProfilInvestQuiz.vue";
</script>

<style scoped>
/* Optional styling for consistent look */
header {
  position: sticky;
  top: 0;
  z-index: 20;
  backdrop-filter: blur(10px);
}
</style>
