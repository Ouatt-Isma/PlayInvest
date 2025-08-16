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

      <!-- Mobile menu button -->
      <button @click="isOpen = true" class="md:hidden p-2" aria-label="Open menu">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none"
             viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"/>
        </svg>
      </button>

      <!-- Auth buttons (desktop) -->
      <div class="hidden md:flex gap-3">
        <NuxtLink to="/login" class="px-4 py-2 border border-gray-300 rounded-lg text-sm font-semibold hover:bg-gray-100">
          Connexion
        </NuxtLink>
        <NuxtLink to="/register" class="px-4 py-2 bg-teal-800 text-white rounded-lg text-sm font-semibold hover:bg-teal-900">
          S'inscrire
        </NuxtLink>
      </div>
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

        <div class="mt-6 border-t pt-4">
          <NuxtLink to="/login" class="block mb-2">Connexion</NuxtLink>
          <NuxtLink to="/register" class="block">S'inscrire</NuxtLink>
        </div>
      </aside>
    </transition>
  </header>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
const isOpen = ref(false)

// (optional) close on Esc
const onKey = (e) => { if (e.key === 'Escape') isOpen.value = false }
onMounted(() => window.addEventListener('keydown', onKey))
onBeforeUnmount(() => window.removeEventListener('keydown', onKey))
</script>

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
