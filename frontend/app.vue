<script setup>
const route = useRoute()
const { isAuthenticated, checkAuth } = useAuth()

// Run auth check once on app load
onMounted(() => {
  checkAuth()
})

const layout = computed(() => {
  const authPages = ["/login", "/register"]
  const isAuthPage = authPages.includes(route.path)

  if (isAuthPage) return "auth"
  return isAuthenticated.value ? "connected" : "default"
})
</script>

<template>
  <NuxtLayout :name="layout">
    <NuxtPage />
  </NuxtLayout>
</template>
