// middleware/auth.global.ts
export default defineNuxtRouteMiddleware((to, from) => {
  const { isAuthenticated } = useAuth()

  // Protect routes that require login
  if (to.meta.requiresAuth && !isAuthenticated.value) {
    return navigateTo("/login")
  }

  // Redirect logged-in users away from guest-only pages
  if (to.meta.guestOnly && isAuthenticated.value) {
    return navigateTo("/dashboard")
  }
})
