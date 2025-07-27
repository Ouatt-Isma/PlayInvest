<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

const referrals = ref<Array<{ id: number; username: string; email: string; created_at: string; avatar_url: string | null }>>([])
const error = ref<string | null>(null)
// const usercook = useCookie<UserCookie>('user', { path: '/' })
// const token = usercook.value?.token


onMounted(async () => {
  const token = localStorage.getItem("token")
  try {
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase 
    const res = await axios.get(`${apiBase}/api/referrals`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    referrals.value = res.data
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Erreur lors du chargement'
  }
})
</script>

<template>
  <div class="min-h-screen p-8">
    <h1 class="text-2xl font-semibold mb-6">Mes Parrainages</h1>

    <div v-if="error" class="text-red-600">{{ error }}</div>
    <div v-else-if="referrals.length === 0" class="text-gray-600">Aucun parrainage pour l'instant.</div>

    <ul v-else class="space-y-4">
      <li v-for="u in referrals" :key="u.id" class="flex items-center space-x-4 p-4 border rounded-lg">
        <img :src="u.avatar_url || '/icons/default.png'" class="h-10 w-10 rounded-full border" />
        <div>
          <div class="font-medium">{{ u.username }}</div>
          <div class="text-sm text-gray-500">{{ u.email }}</div>
          <div class="text-xs text-gray-400 mt-1">Inscrit le {{ new Date(u.created_at).toLocaleDateString() }}</div>
        </div>
      </li>
    </ul>
  </div>
</template>
