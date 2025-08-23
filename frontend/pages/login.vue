<script setup>

import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
// const userCookie = useCookie('user')
// const toastMessage = ref('')
const showToast = ref(false)

import LoginForm from '~/components/LoginForm.vue'
definePageMeta({
  guestOnly: true,      
})

const error = ref(null)
const success = ref(null)
const router = useRouter()


const submitLogin = async ({ email, password }) => {
  try {
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase 
    const res = await axios.post(`${apiBase}/api/login`, {
      email,
      password
    })
    const user = res.data
    const userState = useState('user') // globally reactive state
    userState.value = user  
    if (!res.data.validated) {
      error.value = "Votre email n’est pas encore confirmé. Veuillez vérifier votre boîte mail."
      success.value = null
      showToast.value = true
    setTimeout(() => {
      showToast.value = false
    }, 3000)
    } else {
      success.value = "Connexion réussie !"
      showToast.value = true

      error.value = null
      // Assuming the backend returns user info under `res.data.user`
      // userCookie.value = {
      //   id: user.id,
      //   username: user.username,
      //   first_name: user.first_name,
      //   avatar_url: user.avatar_url,
      //   token: user.token
      // }
      console.log(user)
      localStorage.setItem("token", user.token)
      localStorage.setItem("username", user.username)
      localStorage.setItem("first_name", user.first_name)
      localStorage.setItem("avatar_url", user.avatar_url)
      localStorage.setItem("currency", user.currency)
      localStorage.setItem('user', JSON.stringify(user))


      console.log(user.avatar_url)
      setTimeout(() => {
        router.push('/dashboard')
      }, 2000)
    }
  } catch (err) {
    error.value = err.response?.data?.detail || "Erreur lors de la connexion."
    success.value = null
    showToast.value = true
    setTimeout(() => {
      showToast.value = false
    }, 3000)
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

      <!-- <p v-if="error" class="text-red-600 text-center mt-4">{{ error }}</p>
      <p v-if="success" class="text-green-600 text-center mt-4">{{ success }}</p> -->

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
