<template>
  <section class="py-16 max-w-7xl mx-auto px-4 md:px-8 flex flex-col-reverse md:flex-row items-center gap-12">
    <!-- Make this container responsive with max width -->
    <div class="container mx-auto px-4">
      <h1 class="text-4xl font-bold mb-8">
        Apprendre à investir avec Play Invest
      </h1>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <!-- Left -->
        <div class="mb-12">
           <FeaturedSlider />
        </div>

        <!-- Right -->
        <div>
          <h2 class="text-2xl font-semibold mb-4">Articles tendances</h2>
          <div class="flex flex-col gap-4">
            <TrendingArticle
              v-for="(article, index) in trendingArticles"
              :key="index"
              :article="article"
            />
          </div>
        </div>
      </div>
    </div>
  </section>

          
      <LatestArticles />
      <PopularArticles/>
      <VideoGallery/>

</template>


<script setup>
import FeaturedSlider from '~/components/FeaturedSlider.vue'
import TrendingArticle from '~/components/TrendingArticle.vue'
import LatestArticles from '~/components/LatestArticles.vue'
import PopularArticles from '~/components/PopularArticles.vue'
import VideoGallery from '~/components/VideoGallery.vue'
const trendingArticles = [
  {
    title: "Les Actifs à Suivre en 2025 : Afrique, Europe et Au-Delà",
    date: "8 avril 2025",
    author: "John Doe",
    image: "/images/B2.jpg",
  },
  {
    title: "Pourquoi l’Investissement Virtuel est Crucial pour les Nouveaux Investisseurs",
    date: "8 avril 2025",
    author: "John Doe",
    image: "/images/B3.jpg",
  },
  {
    title: "Crypto-monnaies : Pourquoi Elles Représentent l’Avenir de l’Investissement",
    date: "8 avril 2025",
    author: "John Doe",
    image: "/images/B4.jpg",
  },
  {
    title: "Comment Analyser la Performance Passée des Actifs",
    date: "8 avril 2025",
    author: "John Doe",
    image: "/images/B5.jpg",
  },
]
</script>
