<script setup>
import { ref, watch, onMounted, onBeforeUnmount } 
from 'vue'
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


const isOpen = ref(false)

// (optional) close on Esc
const onKey = (e) => { if (e.key === 'Escape') isOpen.value = false }
onMounted(() => window.addEventListener('keydown', onKey))
onBeforeUnmount(() => window.removeEventListener('keydown', onKey))


</script>
<!-- 'icons/default.png' -->


<template>
  <header class="bg-gray-50 shadow-sm sticky top-0 z-[930]">
    <div class="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
      <!-- Logo -->
      <NuxtLink to="/" class="flex items-center gap-2">
        <img src="/logo.png" alt="PlayInvest Logo" class="h-8 w-auto" />
      </NuxtLink>

      

      <!-- Desktop nav -->
      <nav class="hidden md:flex items-center gap-6 text-sm font-medium text-gray-600">
        <NuxtLink to="/" active-class="text-teal-900 font-bold">Accueil</NuxtLink>
        <NuxtLink to="/assets" :class="{ 'font-semibold text-primary': $route.path === '/assets' }">Actifs</NuxtLink>
        <NuxtLink to="/quiz"   :class="{ 'font-semibold text-primary': $route.path === '/quiz' }">Quiz</NuxtLink>
        <NuxtLink to="/learn"  :class="{ 'font-semibold text-primary': $route.path === '/learn' }">Se former</NuxtLink>
        <NuxtLink to="/news"   :class="{ 'font-semibold text-primary': $route.path === '/news' }">Actualités</NuxtLink>
      </nav>
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
      style="z-index: 1000;"
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
      <!-- Mobile menu button -->
      <button @click="isOpen = true" class="md:hidden p-2" aria-label="Open menu">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none"
             viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"/>
        </svg>
      </button>

      <!-- Auth buttons (desktop) -->
    </div>

    

    <!-- Overlay -->
    <transition name="fade">
      <div v-if="isOpen" class="fixed inset-0 bg-black bg-opacity-40 z-[950]"
           @click="isOpen = false"></div>
    </transition>

    <!-- Right sidebar -->
    <transition name="slide-right">
      <aside v-if="isOpen"
             class="fixed top-0 right-0 w-64 h-full bg-white shadow-lg z-[1000] p-6 flex flex-col gap-4"
             role="dialog" aria-modal="true">
        <div class="flex items-center justify-between mb-4">
          <span class="font-semibold">Menu</span>
          <button @click="isOpen = false" aria-label="Close menu">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none"
                 viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <NuxtLink to="/"        class="block" @click="isOpen = false">Accueil</NuxtLink>
        <NuxtLink to="/assets"  class="block" @click="isOpen = false">Actifs</NuxtLink>
        <NuxtLink to="/quiz"    class="block" @click="isOpen = false">Quiz</NuxtLink>
        <NuxtLink to="/learn"   class="block" @click="isOpen = false">Se former</NuxtLink>
        <NuxtLink to="/news"    class="block" @click="isOpen = false">Actualités</NuxtLink>

        <!-- <div class="mt-6 border-t pt-4">
          <NuxtLink to="/login" class="block mb-2">Connexion</NuxtLink>
          <NuxtLink to="/register" class="block">S'inscrire</NuxtLink>
        </div> -->
      </aside>
    </transition>
  </header>
</template>



<style>
/* Slide in from the RIGHT */
.slide-right-enter-active, .slide-right-leave-active {
  transition: transform 0.3s ease;
}
.slide-right-enter-from, .slide-right-leave-to {
  transform: translateX(100%);
}

/* Fade overlay */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
