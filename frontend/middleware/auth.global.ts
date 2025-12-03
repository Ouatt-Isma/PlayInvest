// middleware/auth.global.ts
import { useAuth } from '@/composables/useAuth'

export default defineNuxtRouteMiddleware((to) => {
  const { init, isAuthenticated, isTokenExpired, token, logout } = useAuth()

  // Initialize cookies/user/token
  init()

  // ------------------------------------------
  // 🔥 1. Auto-logout if token expired
  // ------------------------------------------
  if (token.value && isTokenExpired(token.value)) {
    logout()
    return navigateTo('/login', { replace: true })
  }

  // ------------------------------------------
  // 🔒 2. Routes that require authentication
  // ------------------------------------------
  if (to.meta.requiresAuth && !isAuthenticated.value) {
    return navigateTo('/login', { replace: true })
  }

  // ------------------------------------------
  // 🚫 3. Guest-only routes
  // ------------------------------------------
  if (to.meta.guestOnly && isAuthenticated.value) {
    return navigateTo('/dashboard', { replace: true })
  }

  // ------------------------------------------
  // ALL GOOD — allow navigation
  // ------------------------------------------
})
