<!-- <script setup>
const route = useRoute()
const { isAuthenticated } = useAuth()

const layout = computed(() => {
  const authPages = ["/login", "/register"]
  const isAuthPage = authPages.includes(route.path)

  if (isAuthPage) return "auth"
  return isAuthenticated.value ? "connected" : "default"
})
</script> -->

<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>
