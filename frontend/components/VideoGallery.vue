<template>
    <section class="py-16 max-w-7xl mx-auto px-4 md:px-8 flex flex-col-reverse md:flex-row items-center gap-12">
  <div class="w-full">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-3xl font-bold">Videos</h2>
      <NuxtLink to="/videos" class="text-sm font-medium border border-gray-300 px-4 py-2 rounded-lg hover:bg-gray-100 transition">
        Voir tout
      </NuxtLink>
    </div>

    <!-- Video Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
      <div
        v-for="(video, index) in videos"
        :key="index"
        class="space-y-3"
      >
        <!-- Video Thumbnail Placeholder -->
        <div class="relative bg-gray-900 rounded-xl w-full h-60 flex items-center justify-center">
          <!-- Play icon -->
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-12 w-12 text-white"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path d="M6.5 5.5v9l7-4.5-7-4.5z" />
          </svg>
        </div>

        <!-- Title -->
        <h3 class="text-lg font-semibold leading-tight">
          {{ video.title }}
        </h3>

        <!-- Description -->
        <p class="text-sm text-gray-500">
          {{ video.description }}
        </p>
      </div>
    </div>
  </div>
</section>
</template>

<script setup>
const videos = [
  {
    title: "Maîtrisez l'Art de l'Investissement Fictif",
    description:
      "Développez votre portefeuille virtuel et apprenez à investir sans risque réel.",
  },
  {
    title: "Les Meilleures Stratégies d'Investissement à Essayer",
    description:
      "Découvrez les stratégies gagnantes et testez-les dans un environnement sécurisé.",
  },
  {
    title: "Comment Analyser les Performances Passées des Actifs",
    description:
      "Utilisez notre simulateur pour explorer les tendances historiques et affiner vos choix d'investissement.",
  },
]
</script>
