<template>
  
    <div>
      <HeaderDashboard />
      
      <main class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
  <!-- your content -->
        
        <slot />
        
      </main>

      <Footer />
    </div>
  </template>
  
  <script setup>
  import HeaderDashboard from '@/components/HeaderDashboard.vue'
  import Footer from '@/components/Footer.vue'
  </script>
  