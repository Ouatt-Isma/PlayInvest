<template>
  <transition name="fade">
    <div v-if="open" class="fixed inset-0 z-[100] flex items-center justify-center">
      <!-- Backdrop -->
      <div class="absolute inset-0 bg-black/50" @click="close" aria-hidden="true"></div>

      <!-- Modal -->
      <div
        class="relative z-[101] w-full max-w-3xl mx-4 bg-white rounded-2xl shadow-2xl p-6"
        role="dialog" aria-modal="true" aria-labelledby="challenge-title"
      >
        <div class="flex items-start justify-between gap-4">
          <div>
            <h3 id="challenge-title" class="text-xl font-bold">Challenge de la semaine</h3>
            <p class="text-sm text-gray-500">Choisissez l’actif qui performera le mieux d’ici la fin de la semaine à venir (vendredi). Vous devez faire votre choix durant le week end.</p>
            <p class="text-sm text-gray-600 mt-2" v-if="serverDescription">{{ serverDescription }}</p>
          </div>
          <button @click="close" aria-label="Fermer" class="p-2 rounded hover:bg-gray-100">✕</button>
        </div>

        <!-- Countdown -->
        <div class="mt-3 text-sm">
          <!-- <span class="text-gray-500" v-if="isBetweenPick">Résultats vendredi 23h59 GMT</span> -->
           <div v-if="isBetweenPick">
          <span class="text-red-500">Clôture dimanche 23h59 GMT:</span>
          <span class="ml-2 font-semibold">
            {{ countdown_selec.d }}j {{ countdown_selec.h }}h {{ countdown_selec.m }}m {{ countdown_selec.s }}s
          </span>
          </div>
          <div>
          <span class="text-gray-500">Résultats vendredi 23h59 GMT:</span>
          <span v-if="!error" class="ml-2 font-semibold">
            {{ countdown.d }}j {{ countdown.h }}h {{ countdown.m }}m {{ countdown.s }}s
          </span>
          </div>
        </div>

        <!-- Already picked notice -->
        <div
          v-if="alreadyPicked && pickedAsset"
          class="mt-4 p-3 rounded-lg bg-emerald-50 text-emerald-800 text-sm"
        >
          ✅ Vous avez déjà participé à ce challenge.
          Votre choix : <strong>{{ pickedAsset.name }}</strong>
          <span class="text-gray-500">({{ pickedAsset.symbol }})</span>
        </div>

        <!-- Loading / Error / Empty -->
        <div v-if="loading" class="mt-5 grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="h-36 rounded-xl bg-gray-100 animate-pulse"></div>
          <div class="h-36 rounded-xl bg-gray-100 animate-pulse"></div>
        </div>

        <div v-else-if="error" class="mt-5 p-4 rounded-xl bg-rose-50 text-rose-700 flex items-center justify-between">
          <!-- <span>Veuillez vous connecter en cliquant <NuxtLink to="/register">  <u>ici</u> </NuxtLink>. </span>  -->
           <span v-html="error"></span>
          <button class="px-3 py-1.5 text-sm rounded border" @click="fetchPair">Réessayer</button>
        </div>

        <div v-else-if="assets.length !== 2" class="mt-5 p-4 rounded-xl bg-amber-50 text-amber-800">
          Aucune paire disponible pour cette semaine.
        </div>

        <!-- Choices -->
        <div v-else class="mt-5 grid grid-cols-1 md:grid-cols-2 gap-4">
          <AssetPickCard
            v-for="(item, i) in assets"
            :key="item.sideId ?? i"
            :asset="item.asset"
            :selected="selectedId === item.sideId"
            @select="() => { if (!alreadyPicked) selectedId = item.sideId }"
          />
        </div>

        <!-- Footer -->
        <div class="mt-6 flex items-center justify-between">
          <div class="text-xs text-gray-500">
            Un seul choix par semaine • Votre sélection sera verrouillée après envoi
          </div>
          <div class="flex gap-2">
            <button class="px-4 py-2 rounded-md border hover:bg-gray-50" @click="close">Plus tard</button>
            <button
              class="px-4 py-2 rounded-md text-white bg-emerald-600 hover:bg-emerald-700 disabled:opacity-60"
              :disabled="alreadyPicked || !selectedId || submitting || assets.length !== 2"
              @click="submitPick"
            >
              {{ submitting ? 'Envoi…' : 'Valider mon choix' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>

import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import axios from 'axios'
import AssetPickCard from '~/components/AssetPickCard.vue'

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  endpointPair: { type: String, default: '/api/challenges/weekly/pair' },
  endpointSubmit: { type: String, default: '/api/challenges/weekly/pick' },
  endAt: { type: String, default: '' },
})
const emit = defineEmits(['update:modelValue', 'submit', 'loaded'])

const open = computed({
  get: () => props.modelValue,
  set: v => emit('update:modelValue', v),
})
function close() { open.value = false }

const loading = ref(false)
const submitting = ref(false)
const error = ref('')
// normalized items: [{ sideId, side, asset: {...} }]
const assets = ref([])
const selectedId = ref(null)
const serverEndAt = ref(null)
const serverSelectionEndAt = ref(null)
const serverDescription = ref(null)

const alreadyPicked = ref(false)
const myPick = ref(null)

const pickedAsset = computed(() => {
  if (!alreadyPicked.value || !myPick.value?.sideId) return null
  const match = assets.value.find(a => a.sideId === myPick.value.sideId)
  return match?.asset || myPick.value.asset || null
})

// Countdown (GMT)
const countdown = ref({ d:'00', h:'00', m:'00', s:'00' })
const countdown_selec = ref({ d:'00', h:'00', m:'00', s:'00' })
let t = null

function toParis(date = new Date()) {
  const fmt = new Intl.DateTimeFormat('fr-FR', {
    timeZone: 'GMT',
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', second: '2-digit'
  })
  const parts = fmt.formatToParts(date)
  const get = type => parts.find(p => p.type === type)?.value
  const d = `${get('year')}-${get('month')}-${get('day')}T${get('hour')}:${get('minute')}:${get('second')}`
  return new Date(d)
}
function nextSundayEnd() {
  const now = toParis()
  const dow = now.getDay() // 0=Sun
  const add = (7 - dow) % 7
  const end = new Date(now)
  end.setDate(now.getDate() + add)
  end.setHours(23, 59, 59, 999)
  return end
}

function nextFridayEnd() {
  const now = toParis()
  const dow = now.getDay() // 0=Sun
  const add = (5 - dow) % 7
  const end = new Date(now)
  end.setDate(now.getDate() + add)
  end.setHours(23, 59, 59, 999)
  return end
}

function isBetweenPickDeadline() {
  const now = new Date()
  if (serverSelectionEndAt.value) {
    const serverSelectionDate = new Date(serverSelectionEndAt.value)
    if (serverSelectionDate > now) {
      return true
    } else {
      // server date is past → deadline expired, use nextFriday
      return false
    }
  }

  const friday = new Date(now)
  const daysUntilFriday = (5 - now.getDay() + 7) % 7 // 5 = Friday
  friday.setDate(now.getDate() + daysUntilFriday)
  friday.setHours(23, 59, 59, 999)

  return now < friday
}
const isBetweenPick = isBetweenPickDeadline()

const endTime = computed(() => {
  const now = new Date()
  // 1. If serverEndAt exists and is still in the future → use it
  if (serverEndAt.value) {
    const serverDate = new Date(serverEndAt.value)
    if (serverDate > now) {
      return serverDate
    } else {
      // server date is past → deadline expired, use nextFriday
      return nextFridayEnd()
    }
  }
})
  const endSelectionTime = computed(() => {
  const now = new Date()
  if (serverSelectionEndAt.value) {
    const serverDate = new Date(serverSelectionEndAt.value)
    if (serverDate > now) {
      return serverDate
    } else{
      return null 
    }
  }
  // 2. If props.endAt is provided → use it
  if (props.endAt) {
    return new Date(props.endAt)
  }

  // 3. Otherwise → fallback logic
  return isBetweenPickDeadline() ? nextFridayEnd() : nextSundayEnd()
})

function tick() {
  const now = toParis()
  let ms = endTime.value - now
  if (ms < 0) ms = 0
  const days = Math.floor(ms / 86400000)
  const hours = Math.floor((ms % 86400000) / 3600000)
  const minutes = Math.floor((ms % 3600000) / 60000)
  const seconds = Math.floor((ms % 60000) / 1000)
  countdown.value = {
    d: String(days).padStart(2, '0'),
    h: String(hours).padStart(2, '0'),
    m: String(minutes).padStart(2, '0'),
    s: String(seconds).padStart(2, '0'),
  }
}

function tickSelection() {
  const now = toParis()
  let ms = endSelectionTime.value - now
  if (ms < 0) ms = 0
  const days = Math.floor(ms / 86400000)
  const hours = Math.floor((ms % 86400000) / 3600000)
  const minutes = Math.floor((ms % 3600000) / 60000)
  const seconds = Math.floor((ms % 60000) / 1000)
  countdown_selec.value = {
    d: String(days).padStart(2, '0'),
    h: String(hours).padStart(2, '0'),
    m: String(minutes).padStart(2, '0'),
    s: String(seconds).padStart(2, '0'),
  }
}

function normalizePair(pairRaw) {
  // Accept either [{ sideId, asset }, ...] or plain [asset, asset]
  if (!Array.isArray(pairRaw)) return []
  if (pairRaw.length && 'asset' in pairRaw[0]) return pairRaw
  // If backend still sends pure assets, we cannot submit (no sideId).
  // We create fake sideIds to render, but submission will 422.
  return pairRaw.map((a, i) => ({ sideId: i + 1, side: i === 0 ? 'A' : 'B', asset: a }))
}

async function fetchPair() {
  loading.value = true
  error.value = ''
  selectedId.value = null
  const token = useCookie("token").value


  try {
    const token = useCookie("token").value
    if (!token) {
      error.value = 'Veuillez vous connecter en cliquant <NuxtLink to="/register">  <u>ici</u> </NuxtLink>.'
      return
    }
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase
    const res = await axios.get(`${apiBase}${props.endpointPair}`, {
      headers: { Authorization: `Bearer ${token}` }
    })

    const payload = res.data || {}
    assets.value = normalizePair(payload.pair).slice(0, 2)
    serverEndAt.value = payload.endAt || null
    serverDescription.value = payload.description || ''
    serverSelectionEndAt.value = payload.selectionEndAt || null

    alreadyPicked.value = !!payload.alreadyPicked
    myPick.value = payload.myPick || null

    // Preselect existing pick
    if (alreadyPicked.value && myPick.value?.sideId) {
      selectedId.value = myPick.value.sideId
    }

    emit('loaded', { pair: assets.value, endAt: serverEndAt.value })
  } catch (e) {
    console.log("response status: ", e.response.status)
    error.value = 'Impossible de charger la paire du challenge.'
  } finally {
    loading.value = false
  }
}

async function submitPick() {
  if (!selectedId.value || alreadyPicked.value) return
  submitting.value = true
  try {
    const token = useCookie("token").value
    if (!token) {
      error.value = 'Session expirée. Veuillez vous reconnecter.'
      return
    }
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase

    await axios.post(
      `${apiBase}${props.endpointSubmit}`,
      { sideId: Number(selectedId.value) },
      { headers: { Authorization: `Bearer ${token}` } }
    )

    emit('submit', { sideId: selectedId.value })
    close()
  } catch (e) {
    if (axios.isAxiosError(e) && e.response) {
      console.log("response status: ", e.response.status)
      if (e.response.status === 409) {
        error.value = e.response.data?.detail || 'Vous avez déjà participé à ce challenge.'
        // refresh pick and preselect
        await loadExistingPick()
      } else if (e.response.status === 400) {
        error.value = e.response.data?.detail || 'Le challenge est clôturé.'
      } else if (e.response.status === 422) {
        error.value = e.response.data?.detail || 'Données invalides.'
      } else {
        error.value = e.response.data?.detail || 'Échec de l’envoi de votre choix.'
      }
    } else {
      error.value = 'Erreur réseau ou inconnue.'
    }
  } finally {
    submitting.value = false
  }
}

async function loadExistingPick() {
  try {
    const token = useCookie("token").value
    if (!token) return
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase

    const { data } = await axios.get(
      `${apiBase}/api/challenges/weekly/mypick`,
      { headers: { Authorization: `Bearer ${token}` } }
    )

    if (data?.sideId) {
      myPick.value = data
      selectedId.value = data.sideId
    }
  } catch (err) {
    console.error('Failed to load existing pick', err)
  }
}

onMounted(async () => {
  await fetchPair()
  tick()
  tickSelection()
  t = setInterval(() => {
    tick()
    tickSelection()
  }, 1000)
})
onBeforeUnmount(() => { if (t) clearInterval(t) })


</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 200ms ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
