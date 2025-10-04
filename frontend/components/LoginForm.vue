<script setup>
import { ref } from 'vue'
const email = ref('')
const password = ref('')

const emit = defineEmits(['submit'])

const handleSubmit = () => {
  emit('submit', { email: email.value, password: password.value })
}
</script>

<template>
  <div class="w-full max-w-md mx-auto space-y-6 px-4 sm:px-6">
    <h1 class="text-2xl sm:text-3xl font-bold text-gray-800 text-center">
      Connectez-vous à votre compte
    </h1>

    <form class="space-y-4" @submit.prevent="handleSubmit">
      <input
        v-model="email"
        type="email"
        placeholder="Email"
        class="w-full border border-gray-300 rounded-lg px-4 py-3 text-sm sm:text-base focus:outline-none focus:ring focus:ring-teal-600 focus:border-teal-600"
      />

      <input
        v-model="password"
        type="password"
        placeholder="Mot de passe"
        class="w-full border border-gray-300 rounded-lg px-4 py-3 text-sm sm:text-base focus:outline-none focus:ring focus:ring-teal-600 focus:border-teal-600"
      />

      <div class="text-right">
        <NuxtLink
          to="/forgot-password"
          class="text-xs sm:text-sm text-teal-700 hover:underline"
        >
          Mot de passe oublié ?
        </NuxtLink>
      </div>

      <button
        type="submit"
        class="w-full bg-teal-800 hover:bg-teal-900 text-white py-3 rounded-lg font-semibold transition duration-200 text-sm sm:text-base"
      >
        Se connecter
      </button>
    </form>

    <div class="text-center text-sm text-gray-500">
      Ou connectez-vous avec
    </div>

    <div class="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-between">
      <NuxtLink
        to="/account"
        class="w-full border py-2 sm:py-3 rounded-lg flex justify-center items-center gap-2 hover:bg-gray-50 transition"
      >
        <img src="/logos/google.webp" class="h-5 sm:h-6" />
        <span class="text-sm sm:text-base">Google</span>
      </NuxtLink>

      <NuxtLink
        to="/account"
        class="w-full border py-2 sm:py-3 rounded-lg flex justify-center items-center gap-2 hover:bg-gray-50 transition"
      >
        <img src="/logos/facebook.webp" class="h-5 sm:h-6" />
        <span class="text-sm sm:text-base">Facebook</span>
      </NuxtLink>
    </div>

    <p class="text-center text-sm text-gray-500">
      Vous n'avez pas encore de compte ?
      <NuxtLink
        to="/register"
        class="text-teal-700 hover:underline font-medium"
      >
        Créez-en un
      </NuxtLink>
    </p>
  </div>
</template>
