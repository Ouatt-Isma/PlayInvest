<template>
  
    <div>
      <HeaderDashboard />
      <BandeauTicker/>
      
       <main class="min-h-screen bg-white text-black dark:bg-gray-900 dark:text-white pt-[60px]">
 
  <!-- your content -->
        
        <slot />
        
      </main>

      <Footer />
    </div>
  </template>
  
  <script setup>
  import HeaderDashboard from '@/components/HeaderDashboard.vue'
  import Footer from '@/components/Footer.vue'
  import BandeauTicker from '@/components/BandeauTicker.vue'
  import { useAuth } from '~/composables/useAuth'
  const { init } = useAuth()
  init() // ✅ ensures user + avatar loaded before any page/component
  </script>