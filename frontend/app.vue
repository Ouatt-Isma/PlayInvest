<script setup>
const user = useState('user')
const route = useRoute()

// Only switch to 'connected' if not on login or register page
const layout = computed(() => {
  const authPages = ['/login', '/register']
  const isAuthPage = authPages.includes(route.path)
  return isAuthPage ? 'auth' : user?.value ? 'connected' : 'default'
})
</script>

<template>
  <NuxtLayout :name="layout">
    <NuxtPage />
  </NuxtLayout>
</template>
