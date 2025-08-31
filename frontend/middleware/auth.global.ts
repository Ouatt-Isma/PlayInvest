// middleware/auth.global.ts
import { useAuth } from '@/composables/useAuth'

export default defineNuxtRouteMiddleware((to) => {
  const auth = useAuth()
  auth.init()

  // 🚨 Requires authentication
  if (to.meta.requiresAuth && !auth.checkAuth()) {
    return navigateTo('/login', { replace: true })
  }

  // 🚨 Guest-only pages (login, register, etc.)
  if (to.meta.guestOnly && auth.checkAuth()) {
    return navigateTo('/dashboard', { replace: true })
  }
})
