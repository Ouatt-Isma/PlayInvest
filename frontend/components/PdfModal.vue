<template>
  <div v-if="visible" class="fixed inset-0 bg-black bg-opacity-50 z-[9999] flex items-center justify-center">
    <div class="bg-white w-[90%] max-w-3xl rounded shadow-xl relative">
      <button @click="close" class="absolute top-2 right-2 text-gray-500 hover:text-black text-xl">×</button>
      <iframe
        :src="pdfUrl + '#toolbar=0'"
        width="100%"
        height="600px"
        style="border: none;"
      ></iframe>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  pdfUrl: String,
  visible: Boolean
})
const emit = defineEmits(['close'])

function close() {
  emit('close')
}
</script>
