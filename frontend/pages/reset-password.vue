<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()

const password = ref('')
const confirmPassword = ref('')
const message = ref('')
const error = ref('')
const loading = ref(false)


const resetPassword = async () => {
  error.value = ''
  message.value = ''
  if (password.value !== confirmPassword.value) {
    error.value = "Les mots de passe ne correspondent pas."
    return
  }

  try {
    loading.value = true
    const token = route.query.token
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase 
    await axios.post(`${apiBase}/users/reset-password`, {
      token,
      new_password: password.value
    })

    message.value = 'Mot de passe réinitialisé avec succès.'
    setTimeout(() => router.push('/login'), 2000)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erreur lors de la réinitialisation.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="bg-white p-8 rounded shadow-md w-full max-w-md">
      <h2 class="text-xl font-semibold mb-4">Réinitialisation du mot de passe</h2>

      <input
        v-model="password"
        type="password"
        placeholder="Nouveau mot de passe"
        class="w-full mb-3 border px-4 py-2 rounded"
      />
      <input
        v-model="confirmPassword"
        type="password"
        placeholder="Confirmer le mot de passe"
        class="w-full mb-4 border px-4 py-2 rounded"
      />
      <button
        @click="resetPassword"
        class="w-full bg-teal-700 text-white px-4 py-2 rounded"
        :disabled="loading"
      >
        Réinitialiser
      </button>

      <p v-if="message" class="text-green-600 mt-4">{{ message }}</p>
      <p v-if="error" class="text-red-600 mt-4">{{ error }}</p>
    </div>
  </div>
</template>
