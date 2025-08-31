// composables/useAuth.ts
import { ref, computed } from 'vue'
import { useRouter, useCookie } from '#app'

const user = ref<string | null>(null)
const token = ref<string | null>(null)
const isInitialized = ref(false)

export function useAuth() {
  const router = useRouter()

  /**
   * Initialize auth state from cookies
   */
  function init() {
    if (isInitialized.value) return

    const tokenCookie = useCookie<string | null>('token')
    const userCookie = useCookie<string | null>('user')

    if (tokenCookie.value && userCookie.value) {
      token.value = tokenCookie.value
      user.value = userCookie.value
    }

    isInitialized.value = true
  }

  /**
   * Save user + token after successful login
   */
  function login(userData: string, authToken: string) {
    const tokenCookie = useCookie<string>('token', {
    sameSite: 'lax',
    secure: true,
    path: '/',
  })
    const userCookie = useCookie<string>('user', {
      sameSite: 'lax',
      secure: true,
      path: '/',
    })

    token.value = authToken
    user.value = userData

    tokenCookie.value = authToken
    userCookie.value = userData
  }

  /**
   * Logout: clear cookies + state
   */
  function logout() {
    const tokenCookie = useCookie<string| null>('token')
    const userCookie = useCookie<string| null>('user')

    token.value = null
    user.value = null

    tokenCookie.value = null
    userCookie.value = null

    router.push('/login')
  }

  /**
   * Check if user is authenticated
   */
  function checkAuth() {
    if (!isInitialized.value) {
      init()
    }
    return isAuthenticated.value
  }

  const isAuthenticated = computed(() => !!user.value && !!token.value)

  return {
    user,
    token,
    isInitialized,
    init,
    login,
    logout,
    checkAuth,
    isAuthenticated,
  }
}
