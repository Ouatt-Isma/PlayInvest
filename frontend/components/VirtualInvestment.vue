<template>
  <section class="bg-white py-20">
    <div class="max-w-7xl mx-auto px-4 md:px-8 flex flex-col-reverse md:flex-row items-center gap-12">
      <!-- Text Content -->
      <div class="md:w-1/2">
        <h2 class="text-4xl font-bold mb-6">Investissement Fictif</h2>
        <ul class="space-y-6">
          <li v-for="(item, index) in features" :key="index" class="flex items-start gap-4">
            <img src="/icons/check-blue.png" alt="Check Icon" class="w-6 h-6 mt-1" />
            <div>
              <p class="font-semibold" v-html="item.title" />
              <p class="text-gray-600 text-sm" v-html="item.description" />
            </div>
          </li>
        </ul>
      </div>

      <!-- Image -->
      <div class="md:w-1/2 flex justify-center">
        <img src="/images/image 2h.png" alt="Virtual Investment Illustration" class="max-w-full h-auto" />
      </div>
    </div>
  </section>
</template>

<script setup>
const features = [
  {
    title: 'Investissez de façon fictive :',
    description: 'Testez vos stratégies sans risque avec un portefeuille virtuel sur des actifs du monde entier “Afrique, BRVM, Europe, USA etc.”',
  },
  {
    title: 'Faites des quiz et débloquez des fonds :',
    description: 'Apprenez en jouant et gagnez des fonds fictifs à investir.',
  },
  {
    title: 'Classement mondial :',
    description: 'Défiez les autres PlayInvestisseurs et grimpez dans les ligues.',
  },
  {
    title: 'Simulateur PastPerf :',
    description: 'Simulez un investissement passé et découvrez ce qu’il aurait rapporté.',
  },
  {
    title: 'Module "Se Former" :',
    description: 'Accédez à des fiches, vidéos et ressources pour tout comprendre de l’investissement.',
  },
]
</script>
