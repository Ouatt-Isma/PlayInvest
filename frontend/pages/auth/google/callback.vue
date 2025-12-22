<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '~/composables/useAuth'

const route = useRoute()
const router = useRouter()
const { login } = useAuth()
const { $axios } = useNuxtApp()

const token = route.query.token as string

if (!token) {
  router.push('/login')
} else {
  try {
    // ⭐ THIS IS THE IMPORTANT PART
    const res = await $axios.post(
      '/api/auth/google/exchange',
      { token },
      {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    )

    const { token: jwt, ...user } = res.data

    // ✅ SAME login flow as email/password
    login(user, jwt)

    router.push('/dashboard')
  } catch (e) {
    console.error('Google exchange failed', e)
    router.push('/login')
  }
}
</script>

<template>
  <div class="flex items-center justify-center h-screen">
    <p>Connexion Google en cours…</p>
  </div>
</template>
