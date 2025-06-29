<template>
  <section class="max-w-7xl mx-auto px-4 md:px-8 flex flex-col-reverse md:flex-row items-center gap-12 my-20">
    <div>
      <h2 class="text-4xl font-bold mb-6 leading-tight">Ressources de Formation sur<br />l’investissement mondial</h2>
      <p class="text-gray-600 mb-8 max-w-xl">
        Accédez à des ressources éducatives complètes pour approfondir vos connaissances sur l'investissement à l'échelle mondiale.
        Que vous soyez débutant ou expérimenté, notre contenu vous offre des articles, vidéos et fiches pratiques pour maîtriser
        les stratégies d'investissement et mieux comprendre les marchés internationaux.
      </p>
      <div class="flex gap-4">
        <button class="bg-teal-800 text-white font-semibold px-6 py-3 rounded-lg hover:bg-teal-900 transition">Commencer</button>
        <button class="border border-teal-800 text-teal-800 font-semibold px-6 py-3 rounded-lg hover:bg-teal-50 transition">En savoir plus</button>
      </div>
    </div>

    <!-- Right Feature Cards -->
    <div class="md:w-1/2 mt-12 md:mt-0 flex flex-col md:flex-row justify-center items-start gap-8 md:pl-20">
      <div class="flex flex-col items-center text-center max-w-xs">
        <div class="w-16 h-16 bg-yellow-400 rounded-full flex items-center justify-center mb-4">
            
                <img src="/icons/video-icon.svg" alt="Video icon" class="w-6 h-6" />
           
          
        </div>
        <h3 class="font-bold text-lg mb-2">Articles et vidéos</h3>
        <p class="text-gray-600 text-sm">
          Explorez des ressources détaillées sur les investissements mondiaux, des actions aux cryptos.
        </p>
      </div>

      <div class="flex flex-col items-center text-center max-w-xs">
        <div class="w-16 h-16 bg-yellow-400 rounded-full flex items-center justify-center mb-4">
          <img src="/icons/doc-icon.svg" alt="Doc icon" class="w-6 h-6" />
        </div>
        <h3 class="font-bold text-lg mb-2">Fiches pratiques</h3>
        <p class="text-gray-600 text-sm">
          Apprenez des stratégies d’investissement adaptées aux différents marchés mondiaux.
        </p>
      </div>
    </div>
  </section>
</template>
