<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-tr from-gray-100 to-gray-200 px-4">
    <div class="text-center max-w-md bg-white rounded-2xl shadow-2xl p-10 animate-fade-in">
      <div class="flex justify-center mb-6">
        <Ban class="w-16 h-16 text-red-500" />
      </div>
      <h1 class="text-3xl font-extrabold text-gray-800 mb-4">
Fonctionnalité indisponible</h1>
      <p class="text-gray-600 text-base">
        Cette fonctionnalité est actuellement en développement. Nous travaillons d'arrache-pied pour vous la proposer prochainement.
      </p>
      <p class="text-sm text-gray-400 mt-4 italic">
Restez à l'écoute des mises à jour 🚀</p>
      <button
        @click="goHome"
        class="mt-8 bg-gray-900 text-white px-6 py-2 rounded-full hover:bg-gray-800 transition"
      >
        Retour à la page d'Accueil
      </button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { Ban } from 'lucide-vue-next'

const router = useRouter()
const goHome = () => {
  router.push('/')
}
</script>

<style scoped>
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 0.8s ease-out;
}
</style>
