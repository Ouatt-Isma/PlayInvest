<template>
  <footer class="bg-white border-t border-gray-200 py-10">
    <div class="max-w-screen-xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row justify-between space-y-10 md:space-y-0">
      <!-- Left section -->
      <div class="max-w-md">
        <div class="flex items-center space-x-2 mb-4">
          <img src="/logo.svg" alt="PlayInvest Logo" class="h-10 w-auto" />
        </div>
        <p class="text-gray-500">
          Pour Apprendre et Comprendre l’investissement gratuitement et de façon ludique
        </p>
      </div>

      <!-- Quick links -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-10">
        <div>
          <h3 class="text-lg font-semibold mb-4">Liens Rapides</h3>
          <ul class="space-y-2 text-gray-700">
            <li><a href="#" class="hover:text-primary">Accueil</a></li>
            <li><a href="#" class="hover:text-primary">Actifs</a></li>
            <li><a href="#" class="hover:text-primary">Quiz</a></li>
            <li><a href="#" class="hover:text-primary">Se Former</a></li>
            <li><a href="#" class="hover:text-primary">Actualités</a></li>
          </ul>
        </div>
        <div>
          <h3 class="text-lg font-semibold mb-4">Centre D'aide</h3>
          <ul class="space-y-2 text-gray-700">
            <li>Contactez-Nous</li>
            <li><a href="mailto:Contact@Playinvest.Com" class="text-teal-700 hover:underline">Contact@Playinvest.Com</a></li>
            <li><a href="#" class="hover:text-primary">Conditions D'utilisation</a></li>
            <li><a href="#" class="hover:text-primary">Politique De Confidentialité</a></li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Bottom -->
    <div class="max-w-screen-xl mx-auto mt-10 px-4 sm:px-6 lg:px-8 border-t border-gray-200 pt-6 flex flex-col md:flex-row justify-between items-center">
      <p class="text-sm text-gray-500 mb-4 md:mb-0">© 2025 Playinvest Tous droits réservés.</p>
      <div class="flex space-x-4">
        <a href="#"><img src="/logos/instagram.svg" alt="Instagram" class="h-5 w-5" /></a>
        <a href="#"><img src="/logos/facebook.webp" alt="Facebook" class="h-5 w-5" /></a>
        <a href="#"><img src="/logos/linkedin.svg" alt="LinkedIn" class="h-5 w-5" /></a>
        <a href="#"><img src="/logos/x.png" alt="X" class="h-5 w-5" /></a>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.text-primary {
  color: #005d63;
}
</style>
