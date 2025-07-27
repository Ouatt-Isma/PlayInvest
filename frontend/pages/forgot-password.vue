<script setup>
import { ref } from 'vue'
import axios from 'axios'

const email = ref('')
const success = ref('')
const error = ref('')


const submit = async () => {
  console.log(email.value)
  try {
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase 
    await axios.post(`${apiBase}/users/forgot-password`, {
      email: email.value
    })
    success.value = "Un lien de réinitialisation a été envoyé à votre adresse email."
    error.value = ''
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erreur lors de l’envoi de l’email.'
    success.value = ''
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center px-4 bg-gray-50">
    <div class="max-w-md w-full space-y-6 bg-white p-8 shadow rounded-lg">
      <h2 class="text-2xl font-bold text-gray-800">Réinitialiser votre mot de passe</h2>
      <p class="text-sm text-gray-500">Entrez votre adresse email pour recevoir un lien de réinitialisation.</p>
      
      <input
        v-model="email"
        type="email"
        placeholder="Votre email"
        class="w-full border border-gray-300 rounded px-4 py-3"
      />
      
      <button
        @click="submit"
        class="w-full bg-teal-800 hover:bg-teal-900 text-white py-3 rounded-lg font-semibold transition"
      >
        Envoyer le lien
      </button>

      <p v-if="success" class="text-green-600 text-sm text-center">{{ success }}</p>
      <p v-if="error" class="text-red-600 text-sm text-center">{{ error }}</p>
    </div>
  </div>
</template>
