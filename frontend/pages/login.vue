<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import LoginForm from '~/components/LoginForm.vue'
import { useAuth } from '~/composables/useAuth'

definePageMeta({
  guestOnly: true,
})

const error = ref<string | null>(null)
const success = ref<string | null>(null)
const showToast = ref(false)
const router = useRouter()

const { login } = useAuth()

const submitLogin = async ({ email, password }: { email: string; password: string }) => {
  try {
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase

    // call backend
    const res = await axios.post(`${apiBase}/api/login`, { email, password })
    const user = res.data

    if (!user.validated) {
      error.value = "Votre email n’est pas encore confirmé. Veuillez vérifier votre boîte mail."
      success.value = null
      showToast.value = true
      setTimeout(() => (showToast.value = false), 3000)
      return
    }

    // ✅ use useAuth helper instead of setting cookies manually
    login(user, user.token)

    success.value = "Connexion réussie !"
    error.value = null
    showToast.value = true

    setTimeout(() => {
      router.push('/dashboard')
    }, 0)
  } catch (err: any) {
    error.value = err.response?.data?.detail || "Erreur lors de la connexion."
    success.value = null
    showToast.value = true
    setTimeout(() => (showToast.value = false), 3000)
  }
}
</script>

<template>
  <div class="flex w-full min-h-screen">
    <!-- Left -->
    <div class="w-1/2">
      <LoginSlider />
    </div>

    <!-- Right -->
    <div class="w-1/2 flex flex-col items-center justify-center bg-white px-10">
      <LoginForm @submit="submitLogin" />

      <transition name="fade">
        <div
          v-if="showToast"
          class="fixed top-6 right-6 bg-white shadow-lg rounded px-6 py-4 border border-gray-200 text-sm text-gray-800 z-50"
        >
          <p v-if="error" class="text-red-600 text-center mt-4">{{ error }}</p>
          <p v-if="success" class="text-green-600 text-center mt-4">{{ success }}</p>
        </div>
      </transition>
    </div>
  </div>
</template>
