


<template>
  <div class="flex min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-800 dark:text-white">
    
    <!-- Sidebar -->
    <aside class="w-64 bg-white dark:bg-gray-800 border-r dark:border-gray-700 p-6 space-y-6">
        
      <ul class="space-y-4 text-sm font-medium">
        <li @click="currentSection = 1" :class="[
    'flex cursor-pointer items-center gap-2',
    currentSection === 1 ? 'text-black dark:text-white font-semibold' : 'text-gray-600 dark:text-gray-300'
  ]">
          <img src="/icons/user.svg" class="w-5" /> Profil
        </li>
        <li @click="currentSection = 2" :class="[
    'flex cursor-pointer items-center gap-2',
    currentSection === 2 ? 'text-black dark:text-white font-semibold' : 'text-gray-600 dark:text-gray-300'
  ]">
          <img src="/icons/settings.svg" class="w-5" /> Parrainages
        </li>
        <!-- <li class="flex items-center gap-2 text-gray-600 dark:text-gray-300">
          <img src="/icons/clock.svg" class="w-5" /> Historique
        </li> -->

        <hr class="my-2 border-gray-300 dark:border-gray-600" />

        <!-- <li class="flex items-center gap-2 text-gray-600 dark:text-gray-300">
          <img src="/icons/laptop.svg" class="w-5" /> Sessions et historique de connexion
        </li> -->
        <li @click="currentSection = 3" :class="[
    'flex cursor-pointer items-center gap-2',
    currentSection === 3 ? 'text-black dark:text-white font-semibold' : 'text-gray-600 dark:text-gray-300'
  ]">
          <img src="/icons/2fa.svg" class="w-5" /> 2FA
        </li>
        <li @click="currentSection = 4" :class="[
    'flex cursor-pointer items-center gap-2',
    currentSection === 4 ? 'text-black dark:text-white font-semibold' : 'text-gray-600 dark:text-gray-300'
  ]">
          <img src="/icons/lock.svg" class="w-5" /> Changer le mot de passe
        </li>
      </ul>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 p-10">
    <ProfileDetails v-if="currentSection === 1 || currentSection === null" />
    <Referrals v-if="currentSection === 2" />
    <FeatureUnavailable v-if="currentSection === 3" />
    <UpdatePassword v-if="currentSection === 4" />
    <!-- Add other components as needed -->
    </main>



  </div>
</template>

<script setup>
import ProfileDetails from '~/components/ProfileDetails.vue'
import Referrals from '~/components/Referrals.vue'
import FeatureUnavailable from '~/components/FeatureUnavailable.vue'
import UpdatePassword from '~/components/UpdatePassword.vue'
const currentSection = ref(1) 
// definePageMeta({
//   layout: 'connected',
//   middleware: 'auth'
// })
</script>
