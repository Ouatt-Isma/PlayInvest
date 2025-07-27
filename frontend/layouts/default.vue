<template>
  <div>
    <Header />
    <BandeauTicker />

    <main class="min-h-screen bg-white text-black dark:bg-gray-900 dark:text-white pt-[60px]">
      <slot />
    </main>

    <Footer />
  </div>
</template>

  
  <script setup>
  import Header from '@/components/Header.vue'
  import Footer from '@/components/Footer.vue'
  import BandeauTicker from '@/components/BandeauTicker.vue'

  </script>
  