<script setup>
const route = useRoute()
const userCookie = useCookie("user")

const layout = computed(() => {
  const authPages = ["/login", "/register"]
  const isAuthPage = authPages.includes(route.path)

  if (isAuthPage) return "auth"
  return userCookie.value ? "connected" : "default"
})
</script>

<template>
  <NuxtLayout :name="layout">
    <NuxtPage />
  </NuxtLayout>
</template>
