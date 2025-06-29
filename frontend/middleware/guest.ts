export default defineNuxtRouteMiddleware((to) => {
  if (process.server) return

  const user = useState('user')

  // Rehydrate user from localStorage if needed
  if (!user.value) {
    try {
      const storedUser = localStorage.getItem('user')
      if (storedUser) {
        user.value = JSON.parse(storedUser)
        console.log('[guest middleware] restored user from localStorage')
      }
    } catch (err) {
      console.warn('Failed to parse user from localStorage', err)
    }
  }
  console.log(user.value)
  // Now check redirection
  if (user.value && ['/login', '/register'].includes(to.path)) {
    console.log('[guest middleware] redirecting to /dashboard')
    return navigateTo('/dashboard')
  }
})
