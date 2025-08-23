<template>
  <div class="max-w-md mx-auto space-y-4">
    <h2 class="text-xl font-bold mb-4">Changer le mot de passe</h2>
    <input v-model="currentPassword" type="password" placeholder="Mot de passe actuel" class="input" />
    <input v-model="newPassword" type="password" placeholder="Nouveau mot de passe" class="input" />
    <button @click="updatePassword" class="btn">Mettre à jour</button>
    <transition name="fade">
        <div v-if="showToast"
        class="fixed top-6 right-6 bg-white shadow-lg rounded px-6 py-4 border border-gray-200 text-sm text-gray-800 z-50"
      >
    <p v-if="success" class="text-green-600">{{ success }}</p>
    <p v-if="error" class="text-red-600">{{ error }}</p>
    </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
// import { useCookie } from 'nuxt/app'
// import type {UserCookie} from '@/composables/useUser'

const toastMessage = ref('')
const showToast = ref(false)
const currentPassword = ref('')
const newPassword = ref('')
const error = ref<string | null>(null)
const success = ref<string | null>(null)


const updatePassword = async () => {
    const token = useCookie("token").value
  try {
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase 
    await axios.put(`${apiBase}/users/update-password`, {
      current_password: currentPassword.value,
      new_password: newPassword.value,
    }, {
      headers: {
        Authorization: `Bearer ${token}`  // or however you store the token
      }
    })
    success.value = 'Mot de passe mis à jour avec succès'
    error.value = null
    showToast.value = true
    setTimeout(() => {
      showToast.value = false
    }, 3000)
  } catch (err: unknown) {
  if (axios.isAxiosError(err)) {
    error.value = err.response?.data?.detail || 'Une erreur est survenue'
    showToast.value = true
    setTimeout(() => {
      showToast.value = false
    }, 3000)
  } else {
    error.value = 'Erreur inattendue'
    showToast.value = true
    setTimeout(() => {
      showToast.value = false
    }, 3000)
  }
  success.value = null
}
}
</script>

<style scoped>
.input {
  @apply w-full border px-4 py-2 rounded;
}
.btn {
  @apply bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700;
}
</style>
