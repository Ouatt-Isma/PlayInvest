export default defineNuxtRouteMiddleware(() => {
  // Don't run anything during SSR
  if (process.server) return

  const user = useState('user')
  const route = useRoute()

  // Pages that don't require login
  const publicPages = ['/', '/login', '/register', '/learn', '/assets', '/quiz']
  const isPublic = publicPages.some(p => route.path.startsWith(p))

  // Restore user from localStorage if needed
  if (!user.value) {
    const stored = localStorage.getItem('user')
    if (stored) {
      user.value = JSON.parse(stored)
    }
  }

  // 🚨 Final protection: prevent redirect loops
  if (!user.value && !isPublic && route.path !== '/login') {
    return navigateTo('/login')
  }

  // ✅ DO NOTHING if:
  // - already on a public page
  // - or already on /login
  // - or user is logged in
})
