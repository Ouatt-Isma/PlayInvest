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
  