<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

/**
 * Props:
 *  - endpoint: API route (relative to apiBase) that returns ranking data.
 *  - map: shape mapping in case your backend keys differ.
 *      default expects:
 *        {
 *          me: 'currentUser',
 *          top: 'top',
 *          username: 'username',
 *          rank: 'rank',
 *          score: 'score'
 *        }
 */
const props = defineProps({
  endpoint: { type: String, default: '/api/ranking' },
  map: {
    type: Object,
    default: () => ({
      me: 'currentUser',
      top: 'top',
      username: 'username',
      rank: 'rank',
      score: 'score',
    }),
  },
})

const loading = ref(true)
const error = ref('')
const me = ref(null)     // { username, rank, score }
const top3 = ref([])     // [{ username, rank, score }, ...]
const totalUsers = ref(null)

const fmtPct = (v) => `${Number(v ?? 0).toFixed(2)}%`

onMounted(async () => {
  loading.value = true
  error.value = ''
  try {
    const token = useCookie("token").value
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase

    const { data } = await axios.get(`${apiBase}${props.endpoint}`, {
      headers: { Authorization: `Bearer ${token}` },
    })
    console.log("daaaaaattttaaa", data)
    // Normalize with mapping in case your keys differ
    const m = props.map

    const rawMe = data?.[m.me] ?? null
    const rawTop = Array.isArray(data?.[m.top]) ? data[m.top] : []

    me.value = rawMe
      ? {
          username: rawMe[m.username],
          rank: rawMe[m.rank],
          score: rawMe[m.score],
        }
      : null

    top3.value = rawTop
      .slice(0, 3)
      .map(u => ({
        username: u[m.username],
        rank: u[m.rank],
        score: u[m.score],
      }))
    totalUsers.value = data?.total_users ?? null

  } catch (e) {
    error.value = 'Impossible de charger le classement.'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="p-4 bg-white rounded-xl shadow">
    <h3 class="text-base font-semibold mb-3">Classement des utilisateurs</h3>

    <div v-if="loading" class="text-sm text-gray-500">Chargement…</div>
    <div v-else-if="error" class="text-sm text-red-600">{{ error }}</div>

    <template v-else>
      <!-- Current user -->
      <div class="mb-3 p-3 rounded-lg bg-slate-50 border">
        <div class="text-xs text-gray-500">Votre rang</div>
        <div class="flex items-baseline justify-between">
          <div class="text-lg font-semibold">
            #{{ me?.rank ?? '—' }}
            <span v-if="totalUsers" class="text-sm text-gray-500">
              / {{ totalUsers }}
            </span>
          </div>

          <div class="text-sm text-gray-600">
            {{ me?.username ?? '—' }} — {{ fmtPct(me?.score ?? 0) }}
          </div>
        </div>
      </div>

      <!-- Top 3 -->
      <div v-if="top3.length" class="space-y-2">
        <div
          v-for="u in top3"
          :key="u.username"
          class="flex items-center justify-between p-2 rounded border"
        >
          <div class="flex items-center gap-2">
            <span class="text-sm font-semibold">#{{ u.rank }}</span>
            <span class="text-sm">{{ u.username }}</span>
          </div>
          <span class="text-sm font-medium">{{ fmtPct(u.score) }}</span>
        </div>
      </div>

      <p v-else class="text-xs text-gray-500">Aucun utilisateur trouvé.</p>
    </template>
  </div>
</template>
