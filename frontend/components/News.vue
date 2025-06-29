<template>
    <section class="bg-gray-50 py-16 text-center">
      <h2 class="text-3xl font-bold mb-10">Actualités</h2>
      <div class="flex flex-wrap justify-center gap-8 px-4">
        <div v-for="article in news" :key="article.title" class="max-w-sm rounded overflow-hidden shadow-md text-left bg-white">
          <img :src="article.image" class="w-full h-48 object-cover" />
          <div class="p-4">
            <p class="text-sm text-gray-500 mb-1">{{ article.date }}</p>
            <h3 class="font-semibold text-lg">{{ article.title }}</h3>
            <p class="text-gray-600 text-sm mb-2">{{ article.excerpt }}</p>
            <a href="#" class="text-teal-800 font-semibold text-sm">En savoir plus</a>
          </div>
        </div>
      </div>
    </section>
  </template>
  
  <script setup>
  const news = [
    {
      title: "Maîtrisez l'Art de l'Investissement Fictif",
      excerpt: "Développez votre portefeuille virtuel et apprenez à investir sans risque réel.",
      date: "8 avril 2025",
      image: "/images/image B1.png",
    },
    {
      title: "Les Meilleures Stratégies d’Investissement à Essayer",
      excerpt: "Testez les stratégies gagnantes dans un environnement sécurisé.",
      date: "8 avril 2025",
      image: "/images/image B2.png",
    },
    {
      title: "Comment Analyser les Performances Passées des Actifs",
      excerpt: "Explorez les tendances historiques pour affiner vos choix.",
      date: "8 avril 2025",
      image: "/images/image B3.png",
    },
  ]
  </script>
  