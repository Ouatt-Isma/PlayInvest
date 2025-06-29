<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

definePageMeta({
  layout: 'auth', // ✅ force the 'auth' layout,
   middleware: ['guest']
})

const router = useRouter()

const success = ref(false)
const error = ref(null)
const toastMessage = ref('')
const showToast = ref(false)

const submitForm = async (data) => {
  try {
    await axios.post('http://localhost:8000/api/register', data)
    toastMessage.value = '✅ Compte créé avec succès ! Veuillez vérifier votre email.'
    success.value = true
    error.value = null
    showToast.value = true

    // Redirect after 3s
    setTimeout(() => {
      showToast.value = false
      router.push('/login')
    }, 3000)
  } catch (err) {
    error.value = err.response?.data?.detail || "Erreur lors de l'inscription."
    toastMessage.value = '❌ ' + error.value
    showToast.value = true

    setTimeout(() => {
      showToast.value = false
    }, 4000)
  }
}
</script>


<template>
  <div class="relative">
    <!-- Existing layout -->
    <div class="flex w-full min-h-screen">
      <div class="w-1/2"><LoginSlider /></div>
      <div class="w-1/2 flex items-center justify-center bg-white px-10">
        <SignupForm :submitForm="submitForm" />
      </div>
    </div>

    <!-- ✅ Toast popup -->
    <transition name="fade">
      <div
        v-if="showToast"
        class="fixed top-6 right-6 bg-white shadow-lg rounded px-6 py-4 border border-gray-200 text-sm text-gray-800 z-50"
      >
        {{ toastMessage }}
      </div>
    </transition>
  </div>
</template>
