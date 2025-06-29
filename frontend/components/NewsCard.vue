<template>
    <div class="max-w-sm rounded overflow-hidden shadow-md text-left">
      <img :src="image" class="w-full h-48 object-cover" />
      <div class="p-4">
        <p class="text-sm text-gray-500 mb-1">{{ date }}</p>
        <h3 class="font-semibold text-lg">{{ title }}</h3>
        <p class="text-gray-600 text-sm mb-2">{{ excerpt }}</p>
        <a href="#" class="text-teal-800 font-semibold text-sm">En savoir plus</a>
      </div>
    </div>
  </template>
  
  <script setup>
  defineProps({
    title: String,
    excerpt: String,
    date: String,
    image: String
  })
  </script>
  