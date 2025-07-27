<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const message = ref('Confirmation en cours...')
const success = ref(null)


onMounted(async () => {
  const token = route.query.token
  if (!token) {
    message.value = "❌ Token manquant"
    success.value = false
    return
  }

  try {
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase 
    const res = await axios.get(`${apiBase}/api/confirm?token=${token}`)
    message.value = res.data.message
    success.value = true

    // Optional: redirect after 5 seconds
    setTimeout(() => {
      router.push('/login')
    }, 5000)

  } catch (err) {
    message.value = err.response?.data?.detail || "❌ Une erreur est survenue"
    success.value = false
  }
})
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="bg-white shadow-md rounded-lg p-8 max-w-md text-center">
      <h1 :class="success ? 'text-green-600' : 'text-red-600'" class="text-xl font-semibold mb-4">
        {{ message }}
      </h1>
      <p v-if="success" class="text-gray-600 text-sm">
        Redirection vers la page de connexion...
      </p>
    </div>
  </div>
</template>
