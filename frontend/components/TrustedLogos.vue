<template>
    <section class="bg-teal-800 py-6">
      <div class="max-w-6xl mx-auto px-4 flex flex-wrap items-center justify-center gap-10">
        <img v-for="logo in logos" :key="logo.alt" :src="logo.src" :alt="logo.alt" class="h-8 sm:h-10 object-contain" />
      </div>
    </section>
  </template>
  
  <script setup>
  const logos = [
    { src: '/logos/bitcoin.png', alt: 'Bitcoin' },
    { src: '/logos/apple.svg', alt: 'Apple' },
    { src: '/logos/ethereum.svg', alt: 'Ethereum' },
    { src: '/logos/mtn.svg', alt: 'MTN' },
    { src: '/logos/tesla.svg', alt: 'Tesla' },
    { src: '/logos/alibaba.svg', alt: 'Alibaba' }
  ]
  </script>
  