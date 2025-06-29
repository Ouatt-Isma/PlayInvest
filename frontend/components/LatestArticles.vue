<template>
    <div class="py-16 max-w-7xl mx-auto px-4 md:px-8 flex flex-col-reverse md:flex-row items-center gap-12">
      
  <div class="w-full">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-3xl font-bold">Derniers articles</h2>
      <NuxtLink to="/articles" class="text-sm font-medium border border-gray-300 px-4 py-2 rounded-lg hover:bg-gray-100 transition">
        Voir tout
      </NuxtLink>
    </div>

    <!-- Article Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
      <div
        v-for="(article, index) in articles"
        :key="index"
        class="space-y-3"
      >
        <!-- Image -->
        <NuxtLink :to="article.link">
          <img
            :src="article.image"
            :alt="article.title"
            class="rounded-xl w-full h-48 object-cover"
          />
        </NuxtLink>

        <!-- Date -->
        <p class="text-sm text-gray-500">Le {{ article.date }}</p>

        <!-- Title -->
        <NuxtLink :to="article.link">
          <h3 class="text-lg font-semibold leading-tight hover:underline">
            {{ article.title }}
          </h3>
        </NuxtLink>

        <!-- Description -->
        <p class="text-sm text-gray-600">
          {{ article.description }}
        </p>

        <!-- Link -->
        <NuxtLink :to="article.link" class="text-sm text-blue-600 font-medium hover:underline">
          En savoir plus
        </NuxtLink>
      </div>
    </div>
  </div>
</div>
</template>

<script setup>
const articles = [
  {
    title: "Maîtrisez l'Art de l'Investissement Fictif",
    date: "8 avril 2025",
    description:
      "Développez votre portefeuille virtuel et apprenez à investir sans risque réel.",
    image: "/images/image B1.png",
    link: "/articles/maitriser-investissement-fictif",
  },
  {
    title: "Les Meilleures Stratégies d'Investissement à Essayer",
    date: "8 avril 2025",
    description:
      "Découvrez les stratégies gagnantes et testez-les dans un environnement sécurisé.",
    image: "/images/image B2.png",
    link: "/articles/strategies-investissement-2025",
  },
  {
    title: "Comment Analyser les Performances Passées des Actifs",
    date: "8 avril 2025",
    description:
      "Utilisez notre simulateur pour explorer les tendances historiques et affiner vos choix d'investissement.",
    image: "/images/image B3.png",
    link: "/articles/analyse-performance-actifs",
  },
]
</script>
