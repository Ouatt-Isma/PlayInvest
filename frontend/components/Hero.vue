<template>
    <section class="bg-gray-50 pt-24 pb-20">
      <div class="max-w-7xl mx-auto px-4 flex flex-col lg:flex-row items-center gap-12">
        <!-- Left: Text -->
        <div class="text-center lg:text-left max-w-xl">
          <h1 class="text-4xl lg:text-5xl font-extrabold text-gray-900 leading-tight">
            Apprendre à Investir,<br />
            Jouer pour Progresser
          </h1>
          <p class="text-gray-500 mt-4 text-lg">
            Pour Apprendre et Comprendre l’investissement gratuitement<br />
            et de façon ludique
          </p>
          <NuxtLink
            to="/register"
            class="inline-block mt-6 bg-teal-800 text-white px-6 py-3 rounded hover:bg-teal-900 font-medium"
          >
            Découvrir la Plateforme
          </NuxtLink>

          <div class="mt-4 flex gap-3 items-center">
            <NuxtLink
              href="https://play.google.com/store/apps/details?id=com.playinvesthd.playinvestMobile"
              target="_blank"
              rel="noopener noreferrer"
              class="inline-flex"
            >
              <img
                src="/app_badges/Google_Play_Store_badge_FR.png"
                class="h-12 w-auto"
                alt="Google Play"
              />
            </NuxtLink>

            <NuxtLink
              href="https://apps.apple.com/app/playinvest-hd/id6756258764"
              target="_blank"
              rel="noopener noreferrer"
              class="inline-flex"
            >
              <img
                src="/app_badges/App_Store_badge_FR.png"
                class="h-12 w-auto"
                alt="App Store"
              />
            </NuxtLink>
          </div>

          <div class="mt-4">
            <a
              href="https://chat.whatsapp.com/HycCx555KY3GsDUiqBKt5W"
              target="_blank"
              rel="noopener noreferrer"
              class="inline-flex items-center gap-2 text-sm text-green-700 hover:text-green-800 font-medium"
            >
              <svg class="w-5 h-5" viewBox="0 0 24 24" fill="#25D366" xmlns="http://www.w3.org/2000/svg">
                <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
              </svg>
              Rejoignez notre communauté WhatsApp
            </a>
          </div>

          <div class="mt-10 flex gap-12 text-gray-700 text-lg font-semibold justify-center lg:justify-start">
            <div>
              <span class="block text-2xl text-black font-bold">10k+</span>
              <span class="text-sm font-normal text-gray-500">Joueurs actifs</span>
            </div>
            <div>
              <span class="block text-2xl text-black font-bold">95%</span>
              <span class="text-sm font-normal text-gray-500">Confiance gagnée</span>
            </div>
          </div>
        </div>
  
        <!-- Right: Image -->
        <div class="w-full max-w-lg relative">
          <img src="/images/Image Header.png" alt="Investir" class="w-full" />
          <div
            class="absolute bottom-6 left-6 bg-white shadow-md rounded-md px-4 py-2 flex items-center gap-3"
          >
            <img src="/icons/dollar-blue-icon.png" class="w-8 h-8" />
            <div>
              <div class="font-bold text-sm text-gray-900">PlayInvest</div>
              <div class="text-xs text-gray-500">Le jeu sérieux pour apprendre à investir</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </template>
  