<template>
    <section class="py-16 max-w-7xl mx-auto px-4 md:px-8 flex flex-col-reverse md:flex-row items-center gap-12">
  <div class="w-full">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-3xl font-bold">Articles populaires</h2>
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
</section>
</template>

<script setup>
const articles = [
  {
    title: "L’Évolution de l'Investissement en Afrique: Opportunités et Défis",
    date: "8 avril 2025",
    description:
      "Analyse des opportunités d’investissement en Afrique et des défis uniques.",
    image: "/images/B7.png",
    link: "/articles/investissement-afrique-opportunites",
  },
  {
    title: "Investir dans les ETF : Pourquoi Cette Option Est Devenue Si Populaire",
    date: "8 avril 2025",
    description:
      "Découvrez pourquoi les ETF (fonds négociés en bourse) sont une option idéale pour les investisseurs.",
    image: "/images/B8.png",
    link: "/articles/popularite-etf-investissement",
  },
  {
    title: "Le Leadership Financier : Leçons Inspirantes des Grands Investisseurs",
    date: "8 avril 2025",
    description:
      "Explorez les principes de leadership financier partagés par des investisseurs de renom.",
    image: "/images/B5.jpg",
    link: "/articles/leadership-financier-investisseurs",
  },
]
</script>
