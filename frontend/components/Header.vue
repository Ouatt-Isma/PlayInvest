<template>
  <header class="bg-gray-50 shadow-sm sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
      <NuxtLink to="/" class="flex items-center gap-2">
        <img src="/logo.svg" alt="PlayInvest Logo" class="h-8 w-auto" />
      </NuxtLink>
      <nav class="hidden md:flex items-center gap-6 text-sm font-medium text-gray-600">
        <NuxtLink to="/" class="hover:text-black" active-class="text-teal-900 font-bold">Accueil</NuxtLink>
        <NuxtLink to="/assets" class="hover:text-black px-4 py-2"
  :class="{ 'font-semibold text-primary': $route.path === '/assets' }">Actifs</NuxtLink>
        <NuxtLink to="/quiz" class="hover:text-black px-4 py-2"
  :class="{ 'font-semibold text-primary': $route.path === '/quiz' }">Quiz</NuxtLink>
        <NuxtLink to="/learn" class="hover:text-black px-4 py-2"
  :class="{ 'font-semibold text-primary': $route.path === '/learn' }">Se former</NuxtLink>
      </nav>
      <div class="flex gap-3">
        <NuxtLink to="/login" class="px-4 py-2 border border-gray-300 rounded-lg text-sm font-semibold hover:bg-gray-100">
          Connexion
        </NuxtLink>
        <NuxtLink to="/register" class="px-4 py-2 bg-teal-800 text-white rounded-lg text-sm font-semibold hover:bg-teal-900">
          S'inscrire
        </NuxtLink>
      </div>
    </div>
  </header>
</template>
