<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'

const darkMode = ref(false)
const avatar_url = ref('')
const first_name = ref('')

const router = useRouter()
const logout = async () => {
  console.log('Logging out...')
  showDropdown.value = false

  const userState = useState('user')
  userState.value = null

  localStorage.removeItem('token')
  localStorage.removeItem('user')
  localStorage.removeItem('avatar_url')
  localStorage.removeItem('first_name')

  await navigateTo('/login', { replace: true })
}


onMounted(() => {
  const storedAvatar = localStorage.getItem('avatar_url')
  if (storedAvatar) {
    avatar_url.value = storedAvatar
  }
  const storedfirst_name = localStorage.getItem('first_name')
  if (storedfirst_name) {
    first_name.value = storedfirst_name
  }
})

watch(darkMode, (val) => {
  const html = document.documentElement
  if (val) {
    html.classList.add('dark')
  } else {
    html.classList.remove('dark')
  }
})

// import { useCookie } from 'nuxt/app'
// import type {UserCookie} from '@/composables/useUser'

// const user = useCookie<UserCookie>('user', { path: '/' })


const showDropdown = ref(false)
const dropdownRef = ref(null)

const toggleDropdown = async () => {
  showDropdown.value = !showDropdown.value

  // Wait for dropdown to render before attaching outside listener
  if (showDropdown.value) {
    await nextTick()
    setTimeout(() => {
      document.addEventListener('click', handleClickOutside)
    }, 0)
  } else {
    document.removeEventListener('click', handleClickOutside)
  }
}

const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    showDropdown.value = false
    document.removeEventListener('click', handleClickOutside)
  }
}

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
<!-- 'icons/default.png' -->

<template>
  <header class="bg-gray-50 shadow-sm px-8 py-4 flex items-center justify-between">
    <!-- Logo -->
    <div class="flex items-center space-x-2">
      <img src="/logo.svg" alt="PlayInvest Logo" class="h-8 w-auto" />
      <!-- <span class="text-2xl font-bold text-black">Play<span class="text-gray-700">Invest</span></span> -->
    </div>

    <!-- Navigation -->
    <nav class="flex space-x-6 text-gray-500 font-medium">
      <NuxtLink to="/" exact-active-class="text-black font-semibold">Accueil</NuxtLink>
      <NuxtLink to="/assets" exact-active-class="text-black font-semibold">Actifs</NuxtLink>
      <NuxtLink to="/quiz" exact-active-class="text-black font-semibold">Quiz</NuxtLink>
      <NuxtLink to="/learn" exact-active-class="text-black font-semibold">Se former</NuxtLink>
    </nav>

    <!-- Right Section -->
    <div class="flex items-center space-x-4">
      <NuxtLink to="/notifs" class="relative">
        <img src="/icons/bell.svg" alt="Notifications" class="h-6 w-6 text-gray-600" />
        <span class="absolute top-0 right-0 block h-2 w-2 bg-green-500 rounded-full ring-2 ring-white"></span>
      </NuxtLink>

      <NuxtLink to="/dashboard"  class="border px-4 py-1 rounded-lg text-gray-800 font-medium hover:bg-gray-100">
        Portefeuille
      </NuxtLink>

      <div class="relative group">
        <div class="relative">
  <img
    :src="avatar_url || '/icons/default.png'"
    alt="User Avatar"
    class="h-8 w-8 rounded-full border cursor-pointer"
    @click="toggleDropdown"
  />

    <div
      v-if="showDropdown"
      ref="dropdownRef"
      class="absolute right-0 mt-2 w-64 bg-white rounded-xl shadow-lg z-50 p-4"
    >
        <div class="mb-2">
          <div v-if="first_name && first_name !== 'null'" class="text-lg font-semibold text-gray-900">
      {{ first_name }}
    </div>
    <div class="text-sm text-gray-400">Compte personnel</div>
    </div>

    <hr class="my-2" />

    <div class="space-y-2">
      <NuxtLink to="/profile" class="flex items-center gap-2 text-gray-700 hover:text-black">
        <img src="/icons/user.svg" class="h-4 w-4" />
        Vos détails
      </NuxtLink>

      <NuxtLink to="/account" class="flex items-center gap-2 text-gray-700 hover:text-black">
        <img src="/icons/settings.svg" class="h-4 w-4" />
        Paramètres du compte
      </NuxtLink>

      <button @click="logout" class="flex items-center gap-2 text-gray-700 hover:text-black w-full text-left">
        <img src="/icons/logout.svg" class="h-4 w-4" />
        Se déconnecter
      </button>
    </div>

    <hr class="my-2" />

    <div class="flex items-center justify-between text-gray-700 px-4 py-2">
    <span class="text-sm font-medium">Mode sombre</span>
    <label class="relative inline-flex items-center cursor-pointer">
        <input type="checkbox" v-model="darkMode" class="sr-only peer" />
        <div
        class="w-11 h-6 bg-gray-300 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-teal-500 dark:bg-gray-600 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all"
        ></div>
    </label>
    </div>
  </div>
</div>

      </div>
    </div>
  </header>
</template>
