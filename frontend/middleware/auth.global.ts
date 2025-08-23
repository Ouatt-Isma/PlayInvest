// middleware/auth.global.ts (or auth.ts if not global)
export default defineNuxtRouteMiddleware(async (to, from) => {
  const { checkAuth, isAuthenticated } = useAuth()

  // run checkAuth only if needed
  if (to.meta.requiresAuth) {
    const ok = await checkAuth()
    if (!ok) return navigateTo("/login")
  }

  if (to.meta.guestOnly) {
    const ok = await checkAuth()
    if (ok) return navigateTo("/dashboard")
  }
})
