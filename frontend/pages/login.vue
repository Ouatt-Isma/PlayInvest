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

    const res = await axios.post(`${apiBase}/api/login`, { email, password })
    const { token, ...user } = res.data

    if (!user.validated) {
      error.value = "Votre email n’est pas encore confirmé. Veuillez vérifier votre boîte mail. Un nouvel email de confirmation vient de vous être envoyé."
      success.value = null
      showToast.value = true
      setTimeout(() => (showToast.value = false), 3000)
      return
    }

    login(user, token)
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
  <div class="flex flex-col md:flex-row w-full min-h-screen">
    <!-- Left -->
    <div class="w-full md:w-1/2">
      <LoginSlider />
    </div>

    <!-- Right -->
    <div class="w-full md:w-1/2 flex flex-col items-center justify-center bg-white px-6 md:px-10 py-8">
      <LoginForm @submit="submitLogin" />

      <transition name="fade">
        <div
          v-if="showToast"
          class="fixed top-6 right-6 bg-white shadow-lg rounded-xl px-6 py-3 text-sm font-medium border border-gray-200"
        >
          <p v-if="error" class="text-red-600">{{ error }}</p>
          <p v-if="success" class="text-green-600" style="z-index: 950;">{{ success }}</p>
        </div>
      </transition>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
