<template>
    <div>
      <Header />
      <main class="min-h-screen bg-white text-black dark:bg-gray-900 dark:text-white">
        <slot />
      </main>
      <Footer />
    </div>
  </template>
  
  <script setup>
  import Header from '@/components/Header.vue'
  import Footer from '@/components/Footer.vue'
  </script>
  