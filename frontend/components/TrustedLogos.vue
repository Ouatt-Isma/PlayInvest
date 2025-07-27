<template>
    <section class="bg-teal-800 py-6">
      <div class="max-w-6xl mx-auto px-4 flex flex-wrap items-center justify-center gap-10">
        <img v-for="logo in logos" :key="logo.alt" :src="logo.src" :alt="logo.alt" class="h-8 sm:h-10 object-contain" />
      </div>
    </section>
  </template>
  
  <script setup>
  const logos = [
    { src: '/logos/BTC-USD.webp', alt: 'Bitcoin' },
    { src: '/logos/AAPL.webp', alt: 'Apple' },
    { src: '/logos/ETH-USD.webp', alt: 'Ethereum' },
    { src: '/logos/MTN.JO.webp', alt: 'MTN' },
    { src: '/logos/TSLA.webp', alt: 'Tesla' },
    { src: '/logos/BABA.webp', alt: 'Alibaba' }
  ]
  </script>
  